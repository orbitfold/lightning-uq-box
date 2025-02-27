# Copyright (c) 2023 lightning-uq-box. All rights reserved.
# Licensed under the MIT License.

"""Test Classification Tasks."""

import glob
from pathlib import Path
from typing import Any, Dict

import pytest
from lightning import Trainer
from pytest import TempPathFactory

from lightning_uq_box.datamodules import TwoMoonsDataModule
from lightning_uq_box.main import get_uq_box_cli
from lightning_uq_box.uq_methods import DeepEnsembleClassification

model_config_paths = [
    "tests/configs/classification/temp_scaling.yaml",
    "tests/configs/classification/mc_dropout.yaml",
    "tests/configs/classification/bnn_vi_elbo.yaml",
    "tests/configs/classification/swag.yaml",
    "tests/configs/classification/sgld.yaml",
    "tests/configs/classification/dkl.yaml",
    "tests/configs/classification/due.yaml",
]

data_config_paths = ["tests/configs/classification/toy_classification.yaml"]


class TestClassificationTask:
    @pytest.mark.parametrize("model_config_path", model_config_paths)
    @pytest.mark.parametrize("data_config_path", data_config_paths)
    def test_trainer(
        self, model_config_path: str, data_config_path: str, tmp_path: Path
    ) -> None:
        args = [
            "--config",
            model_config_path,
            "--config",
            data_config_path,
            "--trainer.accelerator",
            "cpu",
            "--trainer.max_epochs",
            "1",
            "--trainer.log_every_n_steps",
            "1",
            "--trainer.default_root_dir",
            str(tmp_path),
        ]

        cli = get_uq_box_cli(args)
        cli.trainer.fit(cli.model, cli.datamodule)
        cli.trainer.test(ckpt_path="best", datamodule=cli.datamodule)


ensemble_model_config_paths = ["tests/configs/classification/mc_dropout.yaml"]


class TestDeepEnsemble:
    @pytest.fixture(
        params=[
            (model_config_path, data_config_path)
            for model_config_path in ensemble_model_config_paths
            for data_config_path in data_config_paths
        ]
    )
    def ensemble_members_dict(self, request, tmp_path_factory: TempPathFactory) -> None:
        model_config_path, data_config_path = request.param
        # train networks for deep ensembles
        ckpt_paths = []
        for i in range(5):
            tmp_path = tmp_path_factory.mktemp(f"run_{i}")

            args = [
                "--config",
                model_config_path,
                "--config",
                data_config_path,
                "--trainer.accelerator",
                "cpu",
                "--trainer.max_epochs",
                "1",
                "--trainer.log_every_n_steps",
                "1",
                "--trainer.default_root_dir",
                str(tmp_path),
            ]

            cli = get_uq_box_cli(args)
            cli.trainer.fit(cli.model, cli.datamodule)

            # Find the .ckpt file in the lightning_logs directory
            ckpt_file = glob.glob(
                f"{str(tmp_path)}/lightning_logs/version_*/checkpoints/*.ckpt"
            )[0]
            ckpt_paths.append({"base_model": cli.model, "ckpt_path": ckpt_file})

        return ckpt_paths

    def test_deep_ensemble(self, ensemble_members_dict: Dict[str, Any]) -> None:
        """Test Deep Ensemble."""
        ensemble_model = DeepEnsembleClassification(
            len(ensemble_members_dict), ensemble_members_dict, 2
        )

        datamodule = TwoMoonsDataModule()

        trainer = Trainer()

        trainer.test(ensemble_model, datamodule=datamodule)

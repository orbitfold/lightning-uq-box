(method_overview)=

# UQ Method Overview

We aim to give both a theoretical and practical overview of implemented UQ-Methods. There exist a wide variety of UQ-Methods. Similarly, there are several general tasks for which practicioners might require uncertainty estimates. The library currently supports the following four tasks:

1. **Regression** for tabular/image inputs with 1D scalar targets
2. 2D Regression / **Pixel Wise Regression**
3. **Classification** for tabular/image inputs with single classification label
4. **Segmentation** where each pixel is assigned a class

While some UQ-Methods like MC-Dropout or Deep Ensembles can be applied across tasks, other methods are specifically developed for certain tasks. The following aims to give an overview of supported methods for the different tasks.

In the tables that follow below, you can see what UQ-Method/Task combination is currently supported by the Lightning-UQ-Box via these indicators:

- ✅ supported
- ❌ not designed for this task
- ⏳ in progress

## Classification of UQ-Methods

The following sections aims to give an overview of different UQ-Methods by grouping them according to some commonalities. We agree that there could be other groupings as well and welcome suggestions to improve this overview. We also follow this grouping for the API documentation in the hopes to make navigation easier.

### Single Forward Pass Methods

| UQ-Method            | Regression            | Classification            | Segmentation              | Pixel Wise Regression      |
|----------------------|:---------------------:|:-------------------------:|:-------------------------:|:--------------------------:|
| Quantile Regression  |          ✅           |           ❌              |           ❌              |            ⏳            |
| Deep Evidential      |          ✅           |           ⏳              |           ⏳              |            ⏳            |
| MVE                  |          ✅           |           ❌              |           ❌              |            ⏳            |


### Approximate Bayesian Methods

| UQ-Method            | Regression            | Classification            | Segmentation              | Pixel Wise Regression      |
|----------------------|:---------------------:|:-------------------------:|:-------------------------:|:--------------------------:|
| BNN_VI_ELBO          |          ✅           |           ✅              |           ✅              |            ⏳            |
| BNN_VI               |          ✅           |           ⏳              |           ⏳              |            ⏳            |
| DKL                  |          ✅           |           ✅              |           ❌              |            ⏳            |
| DUE                  |          ✅           |           ✅              |           ❌              |            ⏳            |
| Laplace              |          ✅           |           ✅              |           ❌              |            ⏳            |
| MC-Dropout           |          ✅           |           ✅              |           ✅              |            ⏳            |
| SGLD                 |          ✅           |           ✅              |           ⏳              |            ⏳            |
| SWAG                 |          ✅           |           ✅              |           ✅              |            ⏳            |
| Deep Ensemble        |          ✅           |           ✅              |           ✅              |            ⏳            |

### Post-Hoc Calibration methods

| UQ-Method            | Regression            | Classification            | Segmentation              | Pixel Wise Regression      |
|----------------------|:---------------------:|:-------------------------:|:-------------------------:|:--------------------------:|
| Conformal QR         |          ✅           |           ❌              |           ❌              |            ⏳              |
| Temperature Scaling  |          ❌           |           ✅              |           ⏳              |            ❌              |

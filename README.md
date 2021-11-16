# PEACFLOW2-Manaus-drought-forecasting
This package is under the construction. It will use a similar structure as [PEACFLOW MANAUS Flood Forecasting](https://github.com/achevuturi/PEACFLOW_Manaus-flood-forecasting/tree/master/Using_Observations).

![Manaus Drought 2010](./manaus_drought_2010.png)

# Structure of this package
* Code of model development is not included.
* Developed models are provided in .pickle format.
* Rainfall masks are included in .npz format.
* Script of observed data download need to be included.

# Prepared data
## Constant data
* Rainfall mask
## Data needed for bias correction:
(Following three datasets are prepared and stored in __obs_1981-2020.cvs__ using __prepare_realtime.ipynb__)*
(__Note that:__ this file needs annual update to include the latest observations.)
* CHIRPS rainfall (Observation)
* Circulation metrics (Observation)
* Prepending maximum annual river level (Observation)
## Data to be downloaded for forecasting
* ECMWF rainfall (Seasonal Forecast)
* Circulation metrics (Seasonal Forecast)

# PEACFLOW2-Manaus-drought-forecasting
This package is used to investigate annual minimum river level on River Negro over Manaus. It will use a similar structure as [PEACFLOW MANAUS Flood Forecasting](https://github.com/achevuturi/PEACFLOW_Manaus-flood-forecasting/tree/master/Using_Observations).

![Manaus Drought 2010](./manaus_drought_2010.png)

# Usage of the packge
1. Download the package.
2. Scripts are written in __Bash__ and __Python3__. Following [tools and packages](#tools) are necessary.
3. To run the script: `sh main.sh`    
  3.1 Enter forecasting year:   
  ![Step1](./github01.png)    
  3.2 Choose forecasting lead month:    
  ![Step2](./github02.png)    
  3.3 Whether to include model uncertainty (True is recommanded):    
  ![Step3](./github03.png)    
  3.4 Choose forecasting input:    
  ![Step4](./github04.png)    
  3.4.2 For *Seasonal-Forecast* only, if *lead-month = August*, then a model-ensemble need to be specified.
    - *wiSep*: Include September rainfall forecast.
    - *woSep*: Exclude September rainfall forecast.    
  ![Step4.2](./github04_2.png)    
  3.5 Downloading input data:    
  ![Step5](./github05.png)    
  3.6 Forecasting minimum river level with the uncertainty range:    
  ![Step6](./github06.png)     
  3.7 Investigating the probability under a customised threshold:    
  ![Step7](./github07.png)

# Prepared data
## Constant data
* Rainfall mask
## Data needed for bias correction:
(Following three datasets are prepared and stored in __obs_1981-2020.cvs__ using __prepare_obs.ipynb__.)\
(__Note that:__ this file needs annual update to include the latest observations.)
* CHIRPS rainfall (Observation)
* Circulation metrics (Observation)
* Prepending maximum annual river level (Observation)
## Data to be downloaded for forecasting
* ECMWF rainfall (Seasonal Forecast)
* Circulation metrics (Seasonal Forecast)

# <a name="tools"></a>Required Tools and Packages
## Data Processing Tools
* [Climate Data Operators (CDO)](https://code.mpimet.mpg.de/projects/cdo/wiki)
  * More details can be found on its wiki page, Section: __Installation and Supported Platforms__.
## Shell unitilities
* [Zenity](https://help.gnome.org/users/zenity/stable/) to generate diaglog box in command-line and shell scripts.
  * For Mac, a [Homebrew Formulae](https://formulae.brew.sh/formula/zenity) is available.
  * For Windows, a [GitHub repository](https://github.com/kvaps/zenity-windows) is available.
## Python packages
* [cf python package](https://ncas-cms.github.io/cf-python/)
  * Installation details are available [here](https://ncas-cms.github.io/cf-python/installation.html). 
* [ECMWF/cdsapi package](https://github.com/ecmwf/cdsapi) for data download.
* Other common used packages inlcuding: numpy, pickle, sys.

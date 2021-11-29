#!/bin/bash

# dialogue_title="Forecast model for minimum water level of Negro River at Manaus"

# Forecast Year
tput setaf 1
echo "===== Forecast Year ====="
echo "Please enter a year (1981-present):"
tput sgr0
read year

# Forecast Lead Month
tput setaf 1
echo "===== Forecast Lead Month ====="
echo "Please enter a Lead Month (August or September):"
tput sgr0
read leadtime

# Forecast Model Uncertainty
tput setaf 1
echo "===== Considering Forecast Model Uncertainties ====="
echo "Please choose between Ture and False (Default is True):"
tput sgr0
read inc_uncertainty

# Forecast Input
tput setaf 1
echo "===== Forecast Input ====="
echo "Please choose between Observation and False Seasonal-Forecast:"
tput sgr0
read input

case $input in
	Observation)
		# For forecasts using Observation, forecast model is associated with forecast leadtime.
		if [ $leadtime == "August" ]
		then
			model="woSep"
		elif [ $leadtime == "September" ]
		then
			model="wiSep"
		fi
		echo ">>> Forecast model is $model."

		echo ">>> Preparing Forecast Data..."
                echo ">>> Downloading CHIRPS rainfall in $year ..."
		echo "... May"
		wget -nv https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/by_month/chirps-v2.0.$year.05.days_p05.nc
		cdo monmean chirps-v2.0.$year.05.days_p05.nc chirps-v2.0.$year.05.mons_p05.nc
		echo "... June"
		wget -nv https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/by_month/chirps-v2.0.$year.06.days_p05.nc
		cdo monmean chirps-v2.0.$year.06.days_p05.nc chirps-v2.0.$year.06.mons_p05.nc
		echo "... July"
		wget -nv https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/by_month/chirps-v2.0.$year.07.days_p05.nc
		cdo monmean chirps-v2.0.$year.07.days_p05.nc chirps-v2.0.$year.07.mons_p05.nc
		echo "... August"
		wget -nv https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/by_month/chirps-v2.0.$year.08.days_p05.nc
		cdo monmean chirps-v2.0.$year.08.days_p05.nc chirps-v2.0.$year.08.mons_p05.nc
		if [ $model == "wiSep" ]
		then
			echo "... September"
			wget -nv https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/by_month/chirps-v2.0.$year.09.days_p05.nc
			cdo monmean chirps-v2.0.$year.09.days_p05.nc chirps-v2.0.$year.09.mons_p05.nc
		fi

                echo ">>> Downloading prepending maximum river level in $year ..."
		python3 fetch_river_level_max.py -i $year

                echo ">>> Downloading SOI in $year ..."
		wget -nv ftp://ftp.bom.gov.au/anon/home/ncc/www/sco/soi/soiplaintext.html
		python3 fetch_soi.py -i $year $model

                echo ">>> Downloading IPO in $year ..."
		python3 fetch_ipo.py -i $year $model

                echo ">>> Downloading AMO in $year ..."
		python3 fetch_amo.py -i $year $model

		echo ">>> Forecasting minimum river level in $year ..."
		python3 main_obs.py -i $year $model $inc_uncertainty

		echo ">>> Cleaning up ..."
		rm soiplaintext.html ???_????.txt river_level_max_????.txt chirps-v2.0.$year.??.days_p05.nc chirps-v2.0.$year.??.mons_p05.nc
                ;;
	Seasonal-Forecast)
		# Fore forecast using Seasonal-forecast, forecast model need to be selected for the August leadtime
		if [ $leadtime == "August" ]
		then
			tput setaf 1
			echo "===== Select Forecast Model ====="
			echo "Please choose between wiSep and woSep:"
			tput sgr0
			read model
		elif [ $leadtime == "September" ]
		then
			model='wiSep'
		fi
		echo ">>> Forecast model is $model."

                echo ">>> Downloading CHIRPS rainfall in $year ..."
		echo "... May"
		wget -nv https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/by_month/chirps-v2.0.$year.05.days_p05.nc
		cdo monmean chirps-v2.0.$year.05.days_p05.nc chirps-v2.0.$year.05.mons_p05.nc
		echo "... June"
		wget -nv https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/by_month/chirps-v2.0.$year.06.days_p05.nc
		cdo monmean chirps-v2.0.$year.06.days_p05.nc chirps-v2.0.$year.06.mons_p05.nc
		echo "... July"
		wget -nv https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/by_month/chirps-v2.0.$year.07.days_p05.nc
		cdo monmean chirps-v2.0.$year.07.days_p05.nc chirps-v2.0.$year.07.mons_p05.nc
		if [ $leadtime == "September" ]
		then
			echo "... August"
			wget -nv https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/by_month/chirps-v2.0.$year.08.days_p05.nc
			cdo monmean chirps-v2.0.$year.08.days_p05.nc chirps-v2.0.$year.08.mons_p05.nc
		fi

		echo ">>> Downloading ECMWF forecast rainfall ..."
		if [ $leadtime == "August" ]
		then
			echo ">>> Downloading ECMWF seasonal forecast rainfall in $year ..."
			echo "... August"
			python3 ecmwf_forecast_rainfall_download.py $year 8
		elif [ $leadtime == "September" ]
		then
			echo "... September"
			python3 ecmwf_forecast_rainfall_download.py $year 9
		fi

                echo ">>> Downloading prepending maximum river level in $year ..."
		python3 fetch_river_level_max.py -i $year

                echo ">>> Downloading SOI in $year ..."
		wget -nv ftp://ftp.bom.gov.au/anon/home/ncc/www/sco/soi/soiplaintext.html
		python3 fetch_soi.py -i $year $model

                echo ">>> Downloading IPO in $year ..."
		python3 fetch_ipo.py -i $year $model

                echo ">>> Downloading AMO in $year ..."
		python3 fetch_amo.py -i $year $model

		echo ">>> Forecasting minimum river level in $year ..."
		python3 main_forecast.py -i $year $leadtime $model $inc_uncertainty

		echo ">>> Cleaning up ..."
		rm soiplaintext.html ???_????.txt river_level_max_????.txt chirps-v2.0.$year.??.days_p05.nc chirps-v2.0.$year.??.mons_p05.nc ecmwf_system5_forecast_*_monthly.nc
		;;
esac

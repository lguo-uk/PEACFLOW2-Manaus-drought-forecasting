#!/bin/bash

# dialogue_title="Forecast model for minimum water level of Negro River at Manaus"

# Forecast Year
year=$(zenity --entry --title="Forecast Year" --text='Please enter a year (1981-present):')
echo  ">>> Forecast Year is $year."

# Forecast Lead Month
leadtime=$(zenity --list --title="Forecast Lead Month" --column="Lead Month" August \September --width=300)
echo ">>> Forecast Lead Month is $leadtime."

# Forecast Model Uncertainty
inc_uncertainty=$(zenity --list --title="Considering Forecast Model Uncertainties" --column="Default is Ture" True \False --width=400)
echo ">>> Consider model uncertainty? $inc_uncertainty"

# Forecast Input
input=$(zenity --list --title="Forecast Input" --column="Input" Observation \Seasonal-Forecast --width=300)
echo ">>> Forecast Input is $input"

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
		(
                echo ">>> Downloading CHIRPS rainfall in $year ..."
		echo "... May"
		echo "10"
		echo "# Downloading CHIRPS rainfall in May..."
		wget -nv https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/by_month/chirps-v2.0.$year.05.days_p05.nc
		cdo monmean chirps-v2.0.$year.05.days_p05.nc chirps-v2.0.$year.05.mons_p05.nc
		echo "... June"
		echo "20"
		echo "# Downloading CHIRPS rainfall in June..."
		wget -nv https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/by_month/chirps-v2.0.$year.06.days_p05.nc
		cdo monmean chirps-v2.0.$year.06.days_p05.nc chirps-v2.0.$year.06.mons_p05.nc
		echo "... July"
		echo "30"
		echo "# Downloading CHIRPS rainfall in July..."
		wget -nv https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/by_month/chirps-v2.0.$year.07.days_p05.nc
		cdo monmean chirps-v2.0.$year.07.days_p05.nc chirps-v2.0.$year.07.mons_p05.nc
		echo "... August"
		echo "40"
		echo "# Downloading CHIRPS rainfall in August..."
		wget -nv https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/by_month/chirps-v2.0.$year.08.days_p05.nc
		cdo monmean chirps-v2.0.$year.08.days_p05.nc chirps-v2.0.$year.08.mons_p05.nc
		if [ $model == "wiSep" ]
		then
			echo "... September"
			echo "50"
			echo "# Downloading CHIRPS rainfall in September..."
			wget -nv https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/by_month/chirps-v2.0.$year.09.days_p05.nc
			cdo monmean chirps-v2.0.$year.09.days_p05.nc chirps-v2.0.$year.09.mons_p05.nc
		fi

                echo ">>> Downloading prepending maximum river level in $year ..."
		echo "60"
                echo "# Downloading prepending maximum river level..."
		python3 fetch_river_level_max.py -i $year

                echo ">>> Downloading SOI in $year ..."
		echo "70"
                echo "# Downloading SOI..."
		wget -nv ftp://ftp.bom.gov.au/anon/home/ncc/www/sco/soi/soiplaintext.html
		python3 fetch_soi.py -i $year $model

                echo ">>> Downloading IPO in $year ..."
		echo "80"
                echo "# Downloading IPO..."
		python3 fetch_ipo.py -i $year $model

                echo ">>> Downloading AMO in $year ..."
		echo "90"
                echo "# Downloading AMO..."
		python3 fetch_amo.py -i $year $model
		) |
		zenity --progress --title="Preparing Data for $year ..." --percentage=0 --width=500 --auto-close

		echo ">>> Forecasting minimum river level in $year ..."
		python3 main_obs.py -i $year $model $inc_uncertainty

		echo ">>> Cleaning up ..."
		rm soiplaintext.html ???_????.txt river_level_max_????.txt chirps-v2.0.$year.??.days_p05.nc chirps-v2.0.$year.??.mons_p05.nc
                ;;
	Seasonal-Forecast)
		# Fore forecast using Seasonal-forecast, forecast model need to be selected for the August leadtime
		if [ $leadtime == "August" ]
		then
			model=$(zenity --list --title="Select Forecast Model" --column="Model" wiSep \woSep)
		elif [ $leadtime == "September" ]
		then
			model='wiSep'
		fi
		echo ">>> Forecast model is $model."

		(
                echo ">>> Downloading CHIRPS rainfall in $year ..."
		echo "... May"
		echo "10"
		echo "# Downloading CHIRPS rainfall in May..."
		wget -nv https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/by_month/chirps-v2.0.$year.05.days_p05.nc
		cdo monmean chirps-v2.0.$year.05.days_p05.nc chirps-v2.0.$year.05.mons_p05.nc
		echo "... June"
		echo "20"
		echo "# Downloading CHIRPS rainfall in June..."
		wget -nv https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/by_month/chirps-v2.0.$year.06.days_p05.nc
		cdo monmean chirps-v2.0.$year.06.days_p05.nc chirps-v2.0.$year.06.mons_p05.nc
		echo "... July"
		echo "30"
		echo "# Downloading CHIRPS rainfall in July..."
		wget -nv https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/by_month/chirps-v2.0.$year.07.days_p05.nc
		cdo monmean chirps-v2.0.$year.07.days_p05.nc chirps-v2.0.$year.07.mons_p05.nc
		if [ $leadtime == "September" ]
		then
			echo "... August"
			echo "40"
			echo "# Downloading CHIRPS rainfall in August..."
			wget -nv https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/by_month/chirps-v2.0.$year.08.days_p05.nc
			cdo monmean chirps-v2.0.$year.08.days_p05.nc chirps-v2.0.$year.08.mons_p05.nc
		fi

		echo ">>> Downloading ECMWF forecast rainfall ..."
		if [ $leadtime == "August" ]
		then
			echo ">>> Downloading ECMWF seasonal forecast rainfall in $year ..."
			echo "... August"
			echo "40"
			echo "# Downloading ECMWF forecast rainfall in August..."
			python3 ecmwf_forecast_rainfall_download.py $year 8
		elif [ $leadtime == "September" ]
		then
			echo "... September"
			echo "50"
			echo "# Downloading ECMWF forecast rainfall in September..."
			python3 ecmwf_forecast_rainfall_download.py $year 9
		fi

                echo ">>> Downloading prepending maximum river level in $year ..."
		echo "60"
                echo "# Downloading prepending maximum river level..."
		python3 fetch_river_level_max.py -i $year

                echo ">>> Downloading SOI in $year ..."
		echo "70"
                echo "# Downloading SOI..."
		wget -nv ftp://ftp.bom.gov.au/anon/home/ncc/www/sco/soi/soiplaintext.html
		python3 fetch_soi.py -i $year $model

                echo ">>> Downloading IPO in $year ..."
		echo "80"
                echo "# Downloading IPO..."
		python3 fetch_ipo.py -i $year $model

                echo ">>> Downloading AMO in $year ..."
		echo "90"
                echo "# Downloading AMO..."
		python3 fetch_amo.py -i $year $model
		) |
		zenity --progress --title="Preparing Data for $year..." --percentage=0 --width=500 --auto-close

		echo ">>> Forecasting minimum river level in $year ..."
		python3 main_forecast.py -i $year $leadtime $model $inc_uncertainty

		echo ">>> Cleaning up ..."
		rm soiplaintext.html ???_????.txt river_level_max_????.txt chirps-v2.0.$year.??.days_p05.nc chirps-v2.0.$year.??.mons_p05.nc ecmwf_system5_forecast_*_monthly.nc
		;;
esac

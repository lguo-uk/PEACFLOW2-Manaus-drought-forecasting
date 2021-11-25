import cf
import numpy as np
import pickle
import sys
import river_level_analysis

if sys.argv[1] == '-i':
	year = sys.argv[2]
	leadtime = sys.argv[3]
	model = sys.argv[4]
	inc_uncertainty = sys.argv[5]
else:
	print('Try: python3 fetch_amo.py -i $year $model')
	exit()

# >>> Read in Forecast model ensemble
f = open('forecast_model_{}.pickle'.format(model), 'rb')
forecast_models = pickle.load(f)
scaler_model = pickle.load(f)
f.close()

# >>> Read in CHIRPS rainfall
rain_may = cf.read('chirps-v2.0.{}.05.mons_p05.nc'.format(year))[0].subspace(X=cf.wi(-85,-33), Y=cf.wi(-40,15)).squeeze()
rain_jun = cf.read('chirps-v2.0.{}.06.mons_p05.nc'.format(year))[0].subspace(X=cf.wi(-85,-33), Y=cf.wi(-40,15)).squeeze()
rain_jul = cf.read('chirps-v2.0.{}.07.mons_p05.nc'.format(year))[0].subspace(X=cf.wi(-85,-33), Y=cf.wi(-40,15)).squeeze()
if leadtime == 'September':
	rain_aug = cf.read('chirps-v2.0.{}.08.mons_p05.nc'.format(year))[0].subspace(X=cf.wi(-85,-33), Y=cf.wi(-40,15)).squeeze()

# Read mask
mask_may = np.load('mask_chirps_may.npz')['mask']
mask_jun = np.load('mask_chirps_jun.npz')['mask']
mask_jul = np.load('mask_chirps_jul.npz')['mask']
if leadtime == 'September':
	mask_aug = np.load('mask_chirps_aug.npz')['mask']

# Calcualte areal mean rainfall
rmay = np.ma.masked_invalid(rain_may.array * mask_may).mean()
rjun = np.ma.masked_invalid(rain_jun.array * mask_jun).mean()
rjul = np.ma.masked_invalid(rain_jul.array * mask_jul).mean()
if leadtime == 'September':
	raug = np.ma.masked_invalid(rain_aug.array * mask_aug).mean()

# >>> Read in ECMWF forecast rainfall
if leadtime == 'September':
	rain_sep_ec = cf.read('ecmwf_system5_forecast_{}0901_total_precipitation_monthly.nc'.format(year))[0][0].subspace(X=cf.wi(-85,-33), Y=cf.wi(-40,15)).squeeze()
elif leadtime == 'August':
	rain_aug_ec = cf.read('ecmwf_system5_forecast_{}0801_total_precipitation_monthly.nc'.format(year))[0][0].subspace(X=cf.wi(-85,-33), Y=cf.wi(-40,15)).squeeze()
	if model == 'wiSep':
		rain_sep_ec = cf.read('ecmwf_system5_forecast_{}0801_total_precipitation_monthly.nc'.format(year))[0][1].subspace(X=cf.wi(-85,-33), Y=cf.wi(-40,15)).squeeze()

# Read Mask
if leadtime == 'September':
	mask_sep_ec = np.load('mask_chirps2ec_sep.npz')['mask']
elif leadtime == 'August':
	mask_aug_ec = np.load('mask_chirps2ec_aug.npz')['mask']
	if model == 'wiSep':
		mask_sep_ec = np.load('mask_chirps2ec_sep.npz')['mask']

# Calculate areal mean rainfall
if leadtime == 'September':
	rsep_ec = np.nanmean((rain_sep_ec.array*86400.*1000.)*mask_sep_ec, axis=(1,2))
elif leadtime == 'August':
	raug_ec = np.nanmean((rain_aug_ec.array*86400.*1000.)*mask_aug_ec, axis=(1,2))
	if model == 'wiSep':
		rsep_ec = np.nanmean((rain_sep_ec.array*86400.*1000.)*mask_sep_ec, axis=(1,2))

# Bias Correction
if leadtime == 'September':
	msep = np.load('rainfall_bias_correction_chirps.npz')['msep']
	ssep = np.load('rainfall_bias_correction_chirps.npz')['ssep']
if leadtime == 'August':
	maug = np.load('rainfall_bias_correction_chirps.npz')['maug']
	saug = np.load('rainfall_bias_correction_chirps.npz')['saug']
	if model == 'wiSep':
		msep = np.load('rainfall_bias_correction_chirps.npz')['msep']
		ssep = np.load('rainfall_bias_correction_chirps.npz')['ssep']

if leadtime == 'September':
	mrsep = np.load('rainfall_bias_correction0.npz')['mrsep']
	srsep = np.load('rainfall_bias_correction0.npz')['srsep']
elif leadtime == 'August':
	mraug = np.load('rainfall_bias_correction1.npz')['mraug']
	sraug = np.load('rainfall_bias_correction1.npz')['sraug']
	if model == 'wiSep':
		mrsep = np.load('rainfall_bias_correction1.npz')['mrsep']
		srsep = np.load('rainfall_bias_correction1.npz')['srsep']

if leadtime == 'September':
	rsep_ec = (rsep_ec - mrsep) / srsep * ssep + msep
if leadtime == 'August':
	raug_ec = (raug_ec - mraug) / sraug * saug + maug
	if model == 'August':
		rsep_ec = (rsep_ec - mrsep) / srsep * ssep + msep

# Read in prepending maximum river level
f = open('river_level_max_{}.txt'.format(year), 'r')
lvl_max = np.float64(f.read())

# Read in circulation metrics
f = open('amo_{}.txt'.format(year), 'r')
amo = np.float64(f.read())

f = open('soi_{}.txt'.format(year), 'r')
soi = np.float64(f.read())

f = open('ipo_{}.txt'.format(year), 'r')
ipo = np.float64(f.read())

# Forecast
ens = [len(rsep_ec) if 'rsep_ec' in locals() else len(raug_ec)][0]
n_model = len(forecast_models)
forecasts = np.zeros((ens, n_model))
if leadtime == 'September':
	for j in range(ens):
		predictors = np.stack((rmay, rjun, rjul, raug, rsep_ec[j], amo, ipo, soi, lvl_max))
		predictors_norm = scaler_model.transform(predictors.reshape(1,-1))
		for i,forecast_model in enumerate(forecast_models):
			forecasts[j,i] = forecast_model.predict(predictors_norm)
elif leadtime == 'August' and model == 'wiSep':
	for j in range(ens):
		predictors = np.stack((rmay, rjun, rjul, raug_ec[j], rsep_ec[j], amo, ipo, soi, lvl_max))
		predictors_norm = scaler_model.transform(predictors.reshape(1,-1))
		for i,forecast_model in enumerate(forecast_models):
			forecasts[j,i] = forecast_model.predict(predictors_norm)
elif leadtime == 'August' and model == 'woSep':
	for j in range(ens):
		predictors = np.stack((rmay, rjun, rjul, raug_ec[j], amo, ipo, soi, lvl_max))
		predictors_norm = scaler_model.transform(predictors.reshape(1,-1))
		for i,forecast_model in enumerate(forecast_models):
			forecasts[j,i] = forecast_model.predict(predictors_norm)
forecasts = forecasts.flatten()

# Read in models uncertainty
models_uncertainty = np.load('models_uncertainty_{}.npz'.format(model))['models_uncertainty']

# Analysis
river_level_analysis.results_n_uncertainty(forecasts, year, model_uncertainty=inc_uncertainty, uncertainty=np.tile(models_uncertainty,(ens,1)).T.flatten())

# Probability Investigation
threshold = 0.
while threshold != 'quit':
	print('')
	print('>>> To investigate the probability of the forecasted minimum river level under a threshold <<<<<')
	threshold = input(">>> Please enter a threshold (units: m). Enter 'quit' to escape.: ")
	try:
		theshold = np.float64(threshold)
		probability = river_level_analysis.mix_norm_cdf(float(threshold), forecasts, np.tile(models_uncertainty,(ens,1)).T.flatten()) * 100.0
		print('... The probability of {} minimum river level below {}m is {:.3f}%.'.format(year, threshold, probability))
	except ValueError:
		print('Quitting the program...')

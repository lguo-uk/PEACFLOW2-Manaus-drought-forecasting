import cf
import numpy as np
import pickle
import sys
import river_level_analysis

if sys.argv[1] == '-i':
	year = sys.argv[2]
	model = sys.argv[3]
	inc_uncertainty = sys.argv[4]
else:
	print('Try: python3 fetch_amo.py -i $year $model')
	exit()

# Read in Forecast model ensemble
f = open('forecast_model_{}.pickle'.format(model), 'rb')
forecast_models = pickle.load(f)
scaler_model = pickle.load(f)
f.close()

# Read in CHIRPS rainfall
rain_may = cf.read('chirps-v2.0.{}.05.mons_p05.nc'.format(year))[0].subspace(X=cf.wi(-85,-33), Y=cf.wi(-40,15)).squeeze()
rain_jun = cf.read('chirps-v2.0.{}.06.mons_p05.nc'.format(year))[0].subspace(X=cf.wi(-85,-33), Y=cf.wi(-40,15)).squeeze()
rain_jul = cf.read('chirps-v2.0.{}.07.mons_p05.nc'.format(year))[0].subspace(X=cf.wi(-85,-33), Y=cf.wi(-40,15)).squeeze()
rain_aug = cf.read('chirps-v2.0.{}.08.mons_p05.nc'.format(year))[0].subspace(X=cf.wi(-85,-33), Y=cf.wi(-40,15)).squeeze()
if model == 'wiSep':
	rain_sep = cf.read('chirps-v2.0.{}.09.mons_p05.nc'.format(year))[0].subspace(X=cf.wi(-85,-33), Y=cf.wi(-40,15)).squeeze()

# Read mask
mask_may = np.load('mask_chirps_may.npz')['mask']
mask_jun = np.load('mask_chirps_jun.npz')['mask']
mask_jul = np.load('mask_chirps_jul.npz')['mask']
mask_aug = np.load('mask_chirps_aug.npz')['mask']
if model == 'wiSep':
	mask_sep = np.load('mask_chirps_sep.npz')['mask']

# Calcualte areal mean rainfall
rmay = np.ma.masked_invalid(rain_may.array * mask_may).mean()
rjun = np.ma.masked_invalid(rain_jun.array * mask_jun).mean()
rjul = np.ma.masked_invalid(rain_jul.array * mask_jul).mean()
raug = np.ma.masked_invalid(rain_aug.array * mask_aug).mean()
if model == 'wiSep':
	rsep = np.ma.masked_invalid(rain_sep.array * mask_sep).mean()

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
if model == 'wiSep':
	predictors = np.stack((rmay, rjun, rjul, raug, rsep, amo, ipo, soi, lvl_max))
elif model == 'woSep':
	predictors = np.stack((rmay, rjun, rjul, raug, amo, ipo, soi, lvl_max))
predictors_norm = scaler_model.transform(predictors.reshape(1,-1))
forecasts = np.zeros(len(forecast_models))
for i,forecast_model in enumerate(forecast_models):
	forecasts[i] = forecast_model.predict(predictors_norm)

# Read in models uncertainty
models_uncertainty = np.load('models_uncertainty_{}.npz'.format(model))['models_uncertainty']

# Analysis
river_level_analysis.results_n_uncertainty(forecasts, year, model_uncertainty=inc_uncertainty, uncertainty=models_uncertainty)

# Probability Investigation
threshold = 0.
while threshold != 'quit':
	print('')
	print('>>> To investigate the probability of the forecasted minimum river level under a threshold <<<<<')
	threshold = input(">>> Please enter a threshold (units: m). Enter 'quit' to escape.: ")
	try:
		theshold = np.float64(threshold)
		probability = river_level_analysis.mix_norm_cdf(float(threshold), forecasts, models_uncertainty) * 100.0
		print('... The probability of {} minimum river level below {}m is {:.3f}%.'.format(year, threshold, probability))
	except ValueError:
		print('Quitting the program...')

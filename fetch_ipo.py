import numpy as np
import pandas as pd
import requests
import sys

if sys.argv[1] == '-i':
	year = sys.argv[2]
	model = sys.argv[3]
else:
	print('Try: python3 fetch_ipo.py -i $year $model')
	exit()

url = 'https://psl.noaa.gov/data/timeseries/IPOTPI/tpi.timeseries.ersstv5.data'

response = requests.get(url)
df = pd.DataFrame([x.split() for x in response.text.split('\n')[1:-12]])
df.rename(columns={0:"year"}, inplace=True)
df.set_index('year', inplace=True)
df = df.astype(float)
df.replace(-99.00, np.nan, inplace=True)

#if model == 'wiSep':
#	ipo = df.loc[year,[5,6,7,8,9]].mean(skipna=False)
#elif model == 'woSep':
#	ipo = df.loc[year,[5,6,7,8]].mean(skipna=False)
ipo = df.loc[year,[6,7,8,9]].mean(skipna=False)

if np.isnan(ipo):
	print('Observed IPO is missing. Check {}.'.format(url))
	exit()
else:
	print('... Mean IPO in {} for {} is {}.'.format(year, model, ipo))
	f = open('ipo_{}.txt'.format(year), 'w')
	f.write(str(ipo))
	f.close()

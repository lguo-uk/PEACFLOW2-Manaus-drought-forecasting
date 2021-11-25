import numpy as np
import pandas as pd
import requests
import sys

if sys.argv[1] == '-i':
	year = sys.argv[2]
	model = sys.argv[3]
else:
	print('Try: python3 fetch_amo.py -i $year $model')
	exit()

url = 'https://psl.noaa.gov/data/correlation/amon.us.long.data'

response = requests.get(url)
df = pd.DataFrame([x.split() for x in response.text.split('\n')[1:-5]])
df.rename(columns={0:"year"}, inplace=True)
df.set_index('year', inplace=True)
df = df.astype(float)
df.replace(-99.99, np.nan, inplace=True)

#if model == 'wiSep':
#	amo = df.loc[year,[5,6,7,8,9]].mean(skipna=False)
#elif model == 'woSep':
#	amo = df.loc[year,[5,6,7,8]].mean(skipna=False)
amo = df.loc[year,[6,7,8,9]].mean(skipna=False)

if np.isnan(amo):
	print('Observed AMO is missing. Check {}.'.format(url))
	exit()
else:
	print('... Mean AMO in {} for {} is {}.'.format(year, model, amo))
	f = open('amo_{}.txt'.format(year), 'w')
	f.write(str(amo))
	f.close()

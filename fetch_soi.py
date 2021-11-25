import numpy as np
import pandas as pd
import requests
import sys

if sys.argv[1] == '-i':
	year = int(sys.argv[2])
	model = sys.argv[3]
else:
	print('Try: python3 fetch_soi.py -i $year $model')
	exit()

url = 'soiplaintext.html'
df = pd.read_csv(url, skiprows=11, skipfooter=3, engine='python', delim_whitespace=True, index_col='Year')

#if model == 'wiSep':
#	soi = df.loc[year,['May','Jun','Jul','Aug','Sep']].mean(skipna=False)
#elif model == 'woSep':
#	soi = df.loc[year,['May','Jun','Jul','Aug']].mean(skipna=False)
soi = df.loc[year,['Jun','Jul','Aug','Sep']].mean(skipna=False)

if np.isnan(soi):
	print('Observed SOI is missing. Check ftp://ftp.bom.gov.au/anon/home/ncc/www/sco/soi/soiplaintext.html.')
	exit()
else:
	print('... Mean SOI in {} for {} is {}.'.format(year, model, soi))
	f = open('soi_{}.txt'.format(year), 'w')
	f.write(str(soi))
	f.close()

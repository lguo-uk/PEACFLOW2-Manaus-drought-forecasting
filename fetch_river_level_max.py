import pandas as pd
import requests
import sys

if sys.argv[1] == '-i':
	ano = int(sys.argv[2])
else:
	print('Try: python3 fetch_river_level_max.py -i $year')
	exit()
semestres = [1,2]

url = 'https://www.portodemanaus.com.br/?pagina=nivel-do-rio-negro-hoje'

lvl_maxes = []
for semestre in semestres:
	payload = {
		'semestre': '%s' %semestre,
		'ano': '%s' %ano,
		'buscar': 'Buscar'
		}

	response = requests.post(url, data=payload)
	df = pd.read_html(response.text, decimal=',', thousands='.')[7]
	lvl_maxes.append( max( df.loc[37,[2,4,6,8,10,12]].astype(float) ) )

lvl_max = max(lvl_maxes)
print('... Maximum river level in {} is {}m.'.format(ano, lvl_max))

f = open('river_level_max_{}.txt'.format(ano), 'w')
f.write(str(lvl_max))
f.close()

import unicodecsv as csv
import urllib3, re
import pandas as pd
from bs4 import BeautifulSoup

#++++++++++++++++++++++++++++++++++++++++++++++#
# Limites del scraping map
# Bahia de sechura
lat_max = -4.5  #--> X
lat_min = -6.5 
lon_max = -79.0 #--> Y
lon_min = -81.5

#++++++++++++++++++++++++++++++++++++++++++++++#
# Leendo el archivo donde estan todas las estaciones
df = pd.read_csv('senamhi-pandas-final.csv')
# Filtrando por coordenadas
mask_1  = df['coord_x'].between(lat_min,lat_max,inclusive=False)
df      = df.loc[mask_1]
mask_2  = df['coord_y'].between(lon_min,lon_max,inclusive=False)
df      = df.loc[mask_2]

# Tamaño de la matriz
"""
size    = df['name'].size

for x in range(size):
    web         = df.iloc[x,9]
    http        = urllib3.PoolManager()
    response    = http.request('GET', web)
    soup        = BeautifulSoup(response.data, 'html.parser')
    path1       = "https://www.senamhi.gob.pe/include_mapas/_dat_esta_tipo.php?estaciones="
    path2       = "https://www.senamhi.gob.pe/include_mapas/_dat_esta_tipo02.php?estaciones="
    path3       = "&tipo="        #--> enlace con tipo
    path4       = "&CBOFiltro="   #--> enlace con fecha
    path5       = "&t_e="        #--> enlace con t_e
"""
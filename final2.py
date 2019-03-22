import unicodecsv as csv
import urllib2, re
import pandas as pd
from bs4 import BeautifulSoup
from os import walk

def converjoe(coord):
    id_gr_x = coord.find(" ")
    xx_gr   = coord[:id_gr_x-1]      
    id_mi_x = coord.find("'")
    xx_mi   = coord[id_gr_x+1:id_mi_x]
    id_se_x = coord.find("''")
    xx_se   = coord[id_mi_x+1:id_se_x]    
    mi_gr   = float(xx_mi)/60
    se_gr   = float(xx_se)/3600
    coord_x = (float(xx_gr)+mi_gr+se_gr)*-1
    print (coord+' ---> '+str(coord_x))
    return coord_x

path1 = "https://www.senamhi.gob.pe/include_mapas/_dat_esta_tipo.php?estaciones="
path2 = "https://www.senamhi.gob.pe/include_mapas/_dat_esta_tipo02.php?estaciones="
path3 = "&tipo="        #--> enlace con tipo
path4 = "&CBOFiltro="   #--> enlace con fecha
path5 = "&t_e="        #--> enlace con t_e
path6 = "/home/usuario/Documentos/ticse/ppython/sen-17-18"

files = []
for dirpath, dirnames, filenames in walk(path6):
    for filename in filenames:
        id_csv = filename.find(".csv")
        file_name = filename[:id_csv]
        files.append(file_name)
files = sorted(files)
frames_d     = []
#for joel in values[46648:]: ---> falta correr 
#No ahi ninguna estacion a partir del 10000
for joel in files:    
    web         = path1+joel
    conector    = urllib2.urlopen(web,timeout=15)
    html        = conector.read()
    soup        = BeautifulSoup(html, 'html.parser')
    fechas      = soup.find_all("option")
    fechita     = soup.find('option')
    t_e_p       = soup.find("input", id="t_e")
    print(web)
    if t_e_p:
        t_e         = t_e_p['value']    #--> enlace t_e en la web
        if fechita and t_e <> 'H':
            tipo_p      = soup.find("input", id="tipo")
            codigo_p    = soup.find('input')
            codigo      = codigo_p['value']
            tipo        = tipo_p['value']   #--> enlace tipo en la web
            soup2       = BeautifulSoup(html,'lxml')
            table       = soup2.find('table', attrs={'class':'body01'})
            df_prev     = pd.read_html(str(table), encoding='utf-8')
            df_name     = df_prev[0]
            name_pr     = df_name.iloc[1,0]
            id_i_n      = name_pr.find(":")
            id_m_n      = name_pr.find(",")
            id_f_n      = name_pr.find("-")
            name        = name_pr[id_i_n+2:id_m_n-1]
            tipo_est    = name_pr[id_m_n+2:id_f_n-1]
            coord_xx    = df_name.iloc[3,1]
            coord_yy    = df_name.iloc[3,3]
            coord_x     = converjoe(coord_xx)
            coord_y     = converjoe(coord_yy)
            coord_z     = float(df_name.iloc[3,5])
            print(name+' ---> '+tipo_est)
            print(coord_z)
            print(codigo+' ---> '+tipo+' ---> '+t_e)
            print('Siguiente, guardando Datos')
            joel_data   = pd.DataFrame({'name':name,
                                        'tipo_est':tipo_est,
                                        'coord_x':coord_x,
                                        'coord_y':coord_y,
                                        'coord_z':coord_z,
                                        'codigo':codigo,
                                        'tipo':tipo,
                                        't_e':t_e,
                                        'web':web}, index=[codigo])
            #fecha_selec = [201701,201702,201703,201801,201802,201803]
            #joel = list(filter(lambda x: x in fecha_value, fecha_selec))
            frames_d.append(joel_data)
            result2 = pd.concat(frames_d)
            result2.drop_duplicates(subset=['codigo'], keep=False)
            result2.to_csv('senamhi-17-18.csv', encoding='utf-8', index=False)



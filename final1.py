import unicodecsv as csv
import urllib2, re
import pandas as pd
from bs4 import BeautifulSoup

path1 = "https://www.senamhi.gob.pe/include_mapas/_dat_esta_tipo.php?estaciones="
path2 = "https://www.senamhi.gob.pe/include_mapas/_dat_esta_tipo02.php?estaciones="
path3 = "&tipo="        #--> enlace con tipo
path4 = "&CBOFiltro="   #--> enlace con fecha
path5 = "&t_e="        #--> enlace con t_e
#tipo_est    = "CON"
#tipo_est2   = "SUT"
#codigo_est  = 151204
#fecha       = 201806

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

#estaciones  = "/home/usuario/Documentos/ticse/ppython/senamhiest_11_jul.csv"
estaciones  = "/home/usuario/Documentos/ticse/ppython/senamhiest_8_ago.csv"
#estaciones  = "J:\\Consultorias\\06-2018-IgpTesis\\ncl\\senamhiest_11_jul.csv"
#estaciones  = "J:\\ncl\\dat_26_febrero.csv"

values = []
for x in range(300000):
    if x < 10:
        cero    = '00000'
        value   = cero + str(x)
    elif x < 100:
        cero    = '0000'
        value   = cero + str(x)
    elif x < 1000:
        cero    = '000'
        value   = cero + str(x)
    elif x < 10000:
        cero    = '00'
        value   = cero + str(x)
    elif x < 100000:
        cero    = '0'
        value   = cero + str(x)
    else:
        value   = str(x)
    values.append(value)
frames_d     = []
#for joel in values[46648:]: ---> falta correr hasta 100000
#No ahi ninguna estacion a partir del 10000
#for joel in values[124738:]: ---> falta correr hasta 200000
#No ahi ninguna estacion a partir del 120000
#for joel in values[205626:]: ---> falta correr hasta 300000
#No ahi ninguna estacion a partir del 200000
#ERROR ---> error con la 150201, 152402, 152405, 152406, 153223, 154112, 156218 
#for joel in values[168906:]: ---> falta correr hasta 200000
#No ahi ninguna estacion a partir del 160000
for joel in values[156219:]:
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
            fecha_value = []
            frames = []
            for fecha in fechas:
                selec   = fecha["value"]
                if selec == '201701' or selec == '201702' or selec == '201703' or selec == '201801' or selec == '201802' or selec == '201803':
                    fecha_value.append(selec)
            print(fecha_value)
            for fecha in fecha_value:
                web2        = path2+codigo+path3+tipo+path4+fecha+path5+t_e
                conector2   = urllib2.urlopen(web2,timeout=10)
                html2       = conector2.read()
                soup2       = BeautifulSoup(html2,'lxml')
                table2      = soup2.find('table', attrs={'class':'body01'})
                df_data_prev= pd.read_html(str(table2), encoding='utf-8')
                df_data     = df_data_prev[0]
                #### asignando nombre de columnas######
                index       = soup2.find('tr', attrs={'bgcolor':'#003366'})
                cols        = index.find_all('td')
                rows_name   = []
                for ele in cols:
                    eme = ele.get('colspan')
                    name = ele.text.strip()
                    if eme:
                        colu = ele['colspan']
                        for x in range(int(colu)):
                            rows_name.append(name)    
                    else:
                        rows_name.append(name)
                df_data.columns = rows_name
                del rows_name
                #########################################
                frames.append(df_data[2:])
            if len(fecha_value) <> 0:
                result = pd.concat(frames)
                result.to_csv(codigo+'.csv', encoding='utf-8', index=False)
                del frames
            del fecha_value
            frames_d.append(joel_data)
            result2 = pd.concat(frames_d)
            result2.to_csv('senamhi-pandas.csv', encoding='utf-8', index=False)



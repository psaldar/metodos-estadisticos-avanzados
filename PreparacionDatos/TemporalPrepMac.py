# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 23:13:20 2020

@author: nicol
"""

### Temporal prep macroeconmicas


import pandas as pd


### Diccionario 
dic_cruces = {}

### Un diccionario de years, y un diccionario para cada year
years = [2016, 2017, 2018]
years_aux = [2015, 2016, 2017, 2018]   ### Estos son para calcular variacion porcentual
for y in years:
    dic_cruces[y] = {}



### TRM
trm = pd.read_excel('MacroVars/trm.xlsx', skiprows=7)
lista_aux = []
for y in years_aux:
    lista_aux.append(trm['Annual Average Market Exchange Rate (Colombian pesos)'][trm['Year']==y].values[0])

voyvo = 0
for y in years:
    anterior = lista_aux[voyvo]
    actual = lista_aux[voyvo+1]
    dic_cruces[y]['TRM'] =  (actual-anterior)/abs(anterior)
    voyvo = voyvo+1



### PIB
pib = pd.read_excel('MacroVars/pib.xls', skiprows=4)
## La primera columna es el year, y la segunda el valor del pib
## EL formato del excel descargado es muy especifico y poco conveniente para leer en maquina
pib = pib.rename(columns={pib.columns[0]: "Year", pib.columns[1]:'pib'})
for y in years:
    ### Correccion para el de 2018
    estepib = y
    if estepib == 2018:
        estepib='2018 (p)'
    dic_cruces[y]['PIB'] = pib['Variación porcentual'][pib['Year']==estepib].values[0]/100



### Desempleo
### Aqui lo que se tiene es la tasa de desempleo mensual
### Para anualizar esta tasa, usaremos la aproximacion de usar el promedio 
### de todos los meses de cada year
desempleo = pd.read_excel('MacroVars/desempleo.xlsx', skiprows=8, nrows=225) 
desempleo['Year'] = desempleo['Año(aaaa)-Mes(mm)'].str[:4]
for y in years:
    dic_cruces[y]['Desempleo'] = desempleo['Tasa de desempleo (%)'][desempleo['Year']==str(y)].mean() / 100


    

### Inflacion
inflacion = pd.read_excel('MacroVars/inflacion.xlsx', skiprows=6)
inflacion.index=inflacion['Mes']
for y in years:
    dic_cruces[y]['Inflacion'] = inflacion[y]['En año corrido']/100 



### Tasa de intervencion
### Aqui lo que se tiene es la tasa de intervencion diaria (solo para dias habiles)
### Para anualizar esta tasa, usaremos la aproximacion de usar el promedio 
### de todos los dias de cada year en los que hay registro (todos los dias habiles)
tasa_interv = pd.read_excel('MacroVars/tasa_intervencion_diaria.xlsx', skiprows=7, nrows=5000) 
tasa_interv['Year'] = tasa_interv['Fecha (dd/mm/aaaa)'].dt.year


lista_aux = []
for y in years_aux:
    lista_aux.append(tasa_interv['Tasa de intervención de política monetaria'][tasa_interv['Year']==y].mean())

voyvo = 0
for y in years:
    anterior = lista_aux[voyvo]
    actual = lista_aux[voyvo+1]
#    dic_cruces[y]['Tasa_Intervencion'] =  (actual-anterior)/abs(anterior)   ### Como variacion porcentual
    dic_cruces[y]['Tasa_Intervencion'] =  actual  ### Como la tasa de cada year
    voyvo = voyvo+1




### Balance en cuenta corriente
bal_cc = pd.read_excel('MacroVars/balance_cc.xlsx', skiprows=10)
estos_years =  ['2015 (r)', '2016 (r)', '2017 (pr)', '2018 (pr)']
voyen = 0
bal_cc.index=bal_cc['Cuenta']
for y in years:
    anterior = bal_cc[estos_years[voyen]]['1 Cuenta corriente']
    actual = bal_cc[estos_years[voyen+1]]['1 Cuenta corriente']
    dic_cruces[y]['Balance_CC'] = (actual-anterior)/abs(anterior)
    voyen = voyen+1
    


### Balance fiscal
bal_fiscal = pd.read_excel('MacroVars/balance_fiscal.xls', skiprows=4)
bal_fiscal = bal_fiscal.rename(columns={bal_fiscal.columns[1]: "Year"})
estos_years =  ['2015 (pr)', '2016 (pr)', '2017 (pr)', '2018 (pr)']
voyen = 0
for y in years:
    anterior = bal_fiscal['DEFICIT (-) O SUPERAVIT (+)'][bal_fiscal['Year']==estos_years[voyen]].values[0]
    actual = bal_fiscal['DEFICIT (-) O SUPERAVIT (+)'][bal_fiscal['Year']==estos_years[voyen+1]].values[0]
    dic_cruces[y]['Balance_Fiscal'] = (actual-anterior)/abs(anterior)
    voyen = voyen+1
    
    
    
    
    
    



### Ahora si, hacerl el cruce y formar el dataset
    
### Leer el de salidas
salidas_son = pd.read_csv('Costos_Gastos_ventas.csv')

### Construccion de dataframe completa
data_full = salidas_son.copy()

### Creo lista para cada variable
vars_son = list(dic_cruces[2016].keys())  ### Nombres de variables

for v in vars_son:
    lista_v = []
    for y in salidas_son['Year']:
        lista_v.append(dic_cruces[y][v])
    data_full[v] = lista_v


### Guardo dataframe final
data_full.to_csv('Datos_completos.csv', index=None)


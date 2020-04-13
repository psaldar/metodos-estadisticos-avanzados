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
for y in years:
    dic_cruces[y] = {}

### TRM
trm = pd.read_excel('MacroVars/trm.xlsx', skiprows=7)
for y in years:
    dic_cruces[y]['TRM'] = trm['Annual Average Market Exchange Rate (Colombian pesos)'][trm['Year']==y].values[0]




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
    dic_cruces[y]['PIB'] = pib['pib'][pib['Year']==estepib].values[0]



#
#### Desempleo
#pib = pd.read_excel('MacroVars/desempleo.xls', skiprows=4)
### La primera columna es el year, y la segunda el valor del pib
### EL formato del excel descargado es muy especifico y poco conveniente para leer en maquina
#pib = pib.rename(columns={pib.columns[0]: "Year", pib.columns[1]:'pib'})
#for y in years:
#    ### Correccion para el de 2018
#    estepib = y
#    if estepib == 2018:
#        estepib='2018 (p)'
#    dic_cruces[y]['PIB'] = pib['pib'][pib['Year']==estepib].values[0]
    
    

### Inflacion
inflacion = pd.read_excel('MacroVars/inflacion.xlsx', skiprows=6)
inflacion.index=inflacion['Mes']
for y in years:
    dic_cruces[y]['Inflacion'] = inflacion[y]['En año corrido'] 



### Tasa de intervencion
### Aqui lo que se tiene es la tasa de intervencion diaria (solo para dias habiles)
### Para anualizar esta tasa, usaremos la aproximacion de usar el promedio 
### de todos los dias de cada año en los que hay registro (todos los dias habiles)
tasa_interv = pd.read_excel('MacroVars/tasa_intervencion_diaria.xlsx', skiprows=7, nrows=5000) 
tasa_interv['Year'] = tasa_interv['Fecha (dd/mm/aaaa)'].dt.year
for y in years:
    dic_cruces[y]['Tasa_Intervencion'] = tasa_interv['Tasa de intervención de política monetaria'][tasa_interv['Year']==y].mean()




### Balance en cuenta corriente
bal_cc = pd.read_excel('MacroVars/balance_cc.xlsx', skiprows=10)
estos_years =  ['2016 (r)', '2017 (pr)', '2018 (pr)']
voyen = 0
bal_cc.index=bal_cc['Cuenta']
for y in years:
    dic_cruces[y]['Balance_CC'] = bal_cc[estos_years[voyen]]['1 Cuenta corriente']
    voyen = voyen+1
    


### Balance fiscal
bal_fiscal = pd.read_excel('MacroVars/balance_fiscal.xlsx', skiprows=10)
estos_years =  ['2016 (r)', '2017 (pr)', '2018 (pr)']
voyen = 0
bal_cc.index=bal_cc['Cuenta']
for y in years:
    dic_cruces[y]['Balance_CC'] = bal_cc[estos_years[voyen]]['1 Cuenta corriente']
    voyen = voyen+1
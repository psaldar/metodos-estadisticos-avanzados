# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 16:42:14 2020

@author: nicol
"""

#### Temporal pruebas

import pandas as pd



### Leer dataframe de cada year (la de los ERI que es la que tiene los costos y gastos de ventas)
dat2015 = pd.read_csv('Data/EstadoResultadosIntegrales(ERI)2015.txt', sep='¬')
dat2016 = pd.read_csv('Data/EstadoResultadosIntegrales(ERI)2016.txt', sep='¬')
dat2017 = pd.read_excel('Data/NIIF Plenas Individuales2017.xlsx', sheet_name='Estado de Resultados Integrales')
dat2018 = pd.read_excel('Data/NIIF Plenas Individuales2018.xlsx', sheet_name='ERI')

### Corregir el nombre de la columna NIT de 2018 para que quede igual a la de los demas
dat2018 = dat2018.rename(columns={"Nit": "NIT"})


### Dejar solo las empresas que tengan la palabra 'construcción' en su clasificacion uniforme
### (Nos basaremos en las del 2018 para obtener los NIT de esas empresas, 
### y luego filtraremos los dataframes de years pasados para dejar solo esos NIT)
### NOTA: solo se tienen en cuenta las empresas cuyo punto de entrada es Plenas e Individuales

### Leer archivo guia donde esta la clasificacion uniforme para saber que NITs conservar
guia_empresas =  pd.read_excel('Data/NIIF Plenas Individuales2018.xlsx', sheet_name='Caratula').rename(columns={"Nit": "NIT"})



### Pasar todo a minuscula la columna de clasificacion
guia_empresas['clasificacion'] = guia_empresas['Clasificación Industrial Internacional Uniforme Versión 4 A.C'].str.lower()

### Dejar solo las que tengan la palabra "construcción" en su clasificacion
empresas_usar = guia_empresas[guia_empresas['clasificacion'].str.contains("construcción")]

### Extraer NIT de las empresas a incluir
NIT_empresas = list(empresas_usar['NIT'].values)


### Verificar cuales de esos NIT aparecen en los 4 years (2015 a 2018)
nit_todos_periodos = []
for nit in NIT_empresas:
    if nit in dat2015['NIT'].values and nit in dat2016['NIT'].values and nit in dat2017['NIT'].values and nit in dat2018['NIT'].values:
        nit_todos_periodos.append(nit)



#### Agregar la columna year a cada datafame
dat2015['Año'] = 2015
dat2016['Año'] = 2016
dat2017['Año'] = 2017
dat2018['Año'] = 2018


#### TEMPORAL
### Gastos de ventas de 2017 no esta en el indice, por ahora ponerlo en 0
dat2017['Gastos de ventas'] = 0



### Dejar solo los periodos actuales en 2017 y 2018
dat2017 = dat2017[dat2017['PERIODO']=='2017']
dat2018 = dat2018[dat2018['Periodo']=='Periodo Actual']


#### Filtrar los dataframe para dejar solo los nit indicados y
### conservar solo las columnqs de Nit, gatos de ventas y costo de ventas
dat_2015_f = dat2015[dat2015['NIT'].isin(nit_todos_periodos)][['NIT','Año','Costo de ventas', 'Gastos de ventas']]
dat_2016_f = dat2016[dat2016['NIT'].isin(nit_todos_periodos)][['NIT','Año','Costo de ventas', 'Gastos de ventas']]
dat_2017_f = dat2017[dat2017['NIT'].isin(nit_todos_periodos)][['NIT','Año','Costo de ventas', 'Gastos de ventas']]
dat_2018_f = dat2018[dat2018['NIT'].isin(nit_todos_periodos)][['NIT','Año','Costo de ventas', 'Gastos de ventas']]


### Quitar duplicados de 2015 (quedarse con el primero)
dat_2015_f.drop_duplicates(inplace=True, subset=['NIT']) 

### Ordenar cada dataframe por Nit
dat_2015_auxi = dat_2015_f.sort_values(by='NIT').reset_index(drop=True)
dat_2016_auxi = dat_2016_f.sort_values(by='NIT').reset_index(drop=True)
dat_2017_auxi = dat_2017_f.sort_values(by='NIT').reset_index(drop=True)
dat_2018_auxi = dat_2018_f.sort_values(by='NIT').reset_index(drop=True)

### Calular valores en diferencias de costo de ventas y gastos de ventas
dat_2016_auxi['Costo de ventas_dif'] = dat_2016_auxi['Costo de ventas'] - dat_2015_auxi['Costo de ventas']
dat_2017_auxi['Costo de ventas_dif'] = dat_2017_auxi['Costo de ventas'] - dat_2016_auxi['Costo de ventas']
dat_2018_auxi['Costo de ventas_dif'] = dat_2018_auxi['Costo de ventas'] - dat_2017_auxi['Costo de ventas']
dat_2016_auxi['Gastos de ventas_dif'] = dat_2016_auxi['Gastos de ventas'] - dat_2015_auxi['Gastos de ventas']
dat_2017_auxi['Gastos de ventas_dif'] = dat_2017_auxi['Gastos de ventas'] - dat_2016_auxi['Gastos de ventas']
dat_2018_auxi['Gastos de ventas_dif'] = dat_2018_auxi['Gastos de ventas'] - dat_2017_auxi['Gastos de ventas']


### Identificar empresas con un NaN en alguna de sus filas
### Eliminar las empresas que tengan al menos un NaN en algun year
nans2016 = dat_2016_auxi[dat_2016_auxi.isnull().any(axis=1)].index
nans2017 = dat_2017_auxi[dat_2017_auxi.isnull().any(axis=1)].index
nans2018 = dat_2018_auxi[dat_2018_auxi.isnull().any(axis=1)].index
#### Tambien las que tengan un 0 en costo o gasto (esto debe ser un error)
ceros2016 = dat_2016_auxi[(dat_2016_auxi==0).any(axis=1)].index
#ceros2017 = dat_2017_auxi[dat_2017_auxi.isnull().any(axis=1)].index  ### Este no hasta q se corrija el gasto de ventas 2017
ceros2018 = dat_2018_auxi[(dat_2018_auxi==0).any(axis=1)].index


### Indices a remover
indices_remover = list(set(nans2016) | set(nans2017) | set(nans2018) | set(ceros2016) | set(ceros2018))  ## falta ceros 2017 

### Indices a conservar
indices_conservar = list(set(range(len(dat_2018_auxi))) - set(indices_remover))


### Dejar solo empresas sin ningun NaN
dat_2016_fin = dat_2016_auxi.iloc[indices_conservar].reset_index(drop=True)
dat_2017_fin = dat_2017_auxi.iloc[indices_conservar].reset_index(drop=True)
dat_2018_fin = dat_2018_auxi.iloc[indices_conservar].reset_index(drop=True)


### Juntar las de 2016, 2017 y 2017 (version fin) en un solo dataframe
dataf_final = pd.concat([dat_2016_fin, dat_2017_fin, dat_2018_fin]).reset_index(drop=True)

### Guardar csv con el resultado obtenido
dataf_final.to_csv('Costos_Gastos_ventas.csv', index=False)

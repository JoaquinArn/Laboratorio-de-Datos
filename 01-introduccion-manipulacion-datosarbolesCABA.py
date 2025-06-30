# -*- coding: utf-8 -*-
"""

@author: Joaco
"""

import pandas as pd
archivo = 'arbolado-en-espacios-verdes.csv'
df = pd.read_csv(archivo, index_col = 2)

"""Datos de árboles en parques de la Ciudad de Buenos Aires.
 https://data.buenosaires.gob.ar/dataset/arbolado-espacios-verdes
 
 Ejercicios:
 1. Armar un dataframe que contenga las filas de Jacarandás y otro con los Palos 
    Borrachos.
 2. Calcular para cada especie seleccionada: 
     a. Cantidad de árboles, altura máxima, mínima y promedio, diámetro máximo, mínimo y 
        promedio.
     b. Definir una función cantidad_arboles(parque) que, dado el nombre de un parque, calcule
        la cantidad de árboles que tiene.
 3. Definir una función cantidad_nativos (parque) que calcule la cantidad de árboles 
    nativos de dicho parque"""
    
#%% Ejercicio 1
jacarandas = df[df['nombre_com'] == 'Jacarandá']
palosBorrachos = pd.concat([df[df['nombre_com'] == 'Palo borracho rosado'], df[df['nombre_com'] == 'Palo borracho']])      
#%% Ejercicio 2a jacarandás
print('hay ' + str(jacarandas.shape[0]) + ' jacarandás')
print('el jacarandá más alto mide ' + str(jacarandas['altura_tot'].max()) + ' metros')
print('el jacarandá más chico mide ' + str(jacarandas['altura_tot'].min()) + ' metros')
print('la altura promedio de los jacarandás observados es ' + str(jacarandas['altura_tot'].sum()/jacarandas.shape[0]) + ' metros')
print('el diámetro máximo visto en un jacarandá es ' + str(jacarandas['diametro'].max()) + ' metros')
print('el diámetro mínimo visto en un jacarandá es ' + str(jacarandas['diametro'].min()) + ' metros')
print('el diametro promedio de los jacarandás obervados es ' + str(jacarandas['diametro'].sum()/jacarandas.shape[0]) + ' metros')
#%% Ejercicio 2a palos borrachos
print('hay ' + str(palosBorrachos.shape[0]) + ' palos borracho')
print('el palo borracho más alto mide ' + str(palosBorrachos['altura_tot'].max()) + ' metros')
print('el palo borracho más chico mide ' + str(palosBorrachos['altura_tot'].min()) + ' metros')
print('la altura promedio de los palo borrachos observados es ' + str(palosBorrachos['altura_tot'].sum()/palosBorrachos.shape[0]) + ' metros')
print('el diámetro máximo visto en un palo borracho es ' + str(palosBorrachos['diametro'].max()) + ' metros')
print('el diámetro mínimo visto en un palo borracho es ' + str(palosBorrachos['diametro'].min()) + ' metros')
print('el diametro promedio de los palo borrachos obervados es ' + str(palosBorrachos['diametro'].sum()/palosBorrachos.shape[0]) + ' metros')
#%% Ejercicio 2b
def cantidad_arboles(parque = str)-> int:
    cantJacarandas = (jacarandas['espacio_ve'] == parque).sum()
    cantPB = (palosBorrachos['espacio_ve'] == parque).sum()
    return cantJacarandas + cantPB
#%% Ejercicio 3
def cantidad_nativos(parque = str) -> int:
    cantJacarandasNativos = ((jacarandas['espacio_ve'] == parque) & (jacarandas['origen'] == 'Nativo/Autóctono')).sum()
    cantPBNativos = ((palosBorrachos['espacio_ve'] == parque) & (palosBorrachos['origen'] == 'Nativo/Autóctono')).sum()
    return cantJacarandasNativos + cantPBNativos






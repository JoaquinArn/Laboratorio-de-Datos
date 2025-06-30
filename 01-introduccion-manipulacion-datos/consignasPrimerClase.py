# -*- coding: utf-8 -*-
"""

@author: Joaco
"""
import pandas as pd
import numpy as np
#%% datos pre-consignas
d = {'nombre':['Antonio', 'Brenda', 'Camila', 'David', 'Esteban', 'Felicitas'], 'apellido': ['Restrepo', 'Saenz', 'Torres', 'Urondo', 'Valdes', 'Wainstein'], 'lu': ['78/23', '449/22', '111/24', '1/21', '201/06', '47/20'], 'nota1': [9, 7, 7, 4, 3, np.nan], 'nota2': [10, 6, 7, 8, 5, np.nan], 'aprueba': [True, True, True, False, False, np.nan]}

df = pd.DataFrame(data = d) # creamos un df a partir de un diccionario
df.set_index('lu', inplace = True) # seteamos una columna como index
#%% Consigna1
"""
 1. mostrar sólo las columnas nombre y apellido
 2. mostrar sólo la fila de libreta 449/22
 3. mostrar las filas 2 a 4
 4. mostrar el nombre de lx estudiante de libreta 201/06
 5. armar una tabla notas parcial con libretas y notas del primer 
    examen
"""
print(df[['nombre', 'apellido']]) #1.1
print(df.loc['449/22']) #1.2
print(df.iloc[2:5]) #1.3
print(df.loc['201/06', 'nombre']) #1.4
data = df[['nota1', 'nota2']]
print(data)

#%% Consigna2
"""
 1. Completar los NULL de la columna “aprueba” con False
 2. Corregir el nombre de David, en realidad es Daniel
 3. Calcular los promedios de las notas de cada estudiante
 4. Responder: aprueban todos?
 5. Eliminar la columna “aprueba”
 6. Agregar 2 estudiantes a la lista (inventando sus datos)
 """
df['aprueba'] = df['aprueba'].fillna(False) #2.1
df.replace({'nombre':{'David':'Daniel'}}) #2.2
df['promedio'] = (df['nota1'] + df['nota2'])/2 #2.3
print ("aprueban todos? " + str(df['aprueba'].all())) #2.4
df.drop('aprueba', axis = 1) #2.5
dfAux = {'nombre': ['Carlos', 'Carla'], 'apellido':['Sainz', 'Conde'], 'lu':['20/20', '40/23'], 'nota1':[10, 8], 'nota2': [8,10], 'promedio':[9,9]} #2.6
dfaux = pd.DataFrame(data = dfAux) #2.7
dfaux.set_index('lu', inplace=True) #2.8
pd.concat([df,dfaux]) #2.9

#%% Consigna3
"""
 1.  Ver quiénes sacaron 6 o más en la nota 1
 2.  Contar cuántos estudiantes sacaron 6 o más
 3.  Armar un dataframe con quienes sacaron 6 o más
 4.  Armar un dataframe con quienes sacaron 6 o más en la nota 1 y 7 o 
     más en la nota 2
 5.  Armar un dataframe con quienes sacaron exactamente 7 en la 
     nota 1
 6.  Armar un dataframe con quienes aprobaron y sacaron 7 o menos 
     en la nota 2
 7.  Armar un dataframe con quienes sacaron menos que 6 en alguna 
     instancia
 8.  Armar un dataframe omitiendo las filas donde no hay nota 1 ni 
     nota 2
 9.  Contar cuántos estudiantes sacaron cada valor para la nota1
 10. Poner un 0 en las notas 1 que sean mayores a 4
"""

df[df['nota1'] >= 6] #3.1
(df['nota1']>=6).sum() #3.2
aprobadosPrimerParcial = df[df['nota1'] >= 6] #3.3
cumplenInciso4 = df[(df['nota1'] >= 6) & (df['nota2'] >= 7)] #3.4
logranInciso5 = df[df['nota1'] == 7] #3.5
valenParaInciso6 = df[(df['aprueba']) & (df['nota2'] >=7)] #3.6
lograronInciso7 = df[(df['nota1'] < 6) | (df['nota2'] <6)] #3.7
soloQuienesTienenNota = df[(df['nota1'].notna()) & (df['nota2'].notna())] #3.8
#%% consigna 3.9
dictCantCiertaNotaPrimerP = {1: 0, 2: 0, 3: 0, 4:0, 5: 0, 6: 0, 7:0, 8: 0, 9: 0, 10:0}
for nota in range (0, 10):
    dictCantCiertaNotaPrimerP[nota] = (df['nota1'] == nota).sum()
tablaCantCiertaNotaPrimerP = pd.DataFrame(data = dictCantCiertaNotaPrimerP, index=[0]).T
#%% consigna 3.10
df.where(df['nota1'] > 4, 0)















# -*- coding: utf-8 -*-
"""
Created on Mon May 19 13:55:36 2025

@author: Joaco
"""
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import pandas as pd
import numpy as np
import duckdb as dd


#GUÍA DE EJERCICIOS: VISUALIZACIÓN
#%% FUENTE DE DATO A UTILIZAR
data_ping = sns.load_dataset('penguins')

#%% PRIMEROS EJERCICIOS
""" 
 a. ¿Qué representa cada línea del dataframe?
 b. ¿Cuántas muestras hay en total?
 c. ¿Cuáles son las especies de pingüinos consideradas?
 d. ¿Cuáles son las islas estudiadas?
 e. Para cada pingüino, ¿con qué datos contamos?
"""

#a) Cada línea del dataframe representa un pingüino observado a través de investigaciones realizadas en la Antártida.
#b) Hay en total 344 muestras
#c) Las especies de pingüinos consideradas son Adelie, Chinstrap y Gentoo.
#d) Las islas estudiadas son Biscoe, Dream y Torgersen.
#e) Los datos que contamos para cada pingüino son:
    #- 'species': refiere a la especie del pingüino registrado.
    #- 'island': refiere a la isla en la cual fue observado el pingüino registrado.
    #- 'bill_length_mm': refiere a la longitud, medida en milímetros, del pico del pingüino registrado.
    #- 'bill_depth_mm': refiere a la profundidad, medida en milímetros, del pico del pingüino registrado.
    #- 'flipper_length_mm': refiere a la longitud, medida en milímetros, de la aleta del pingüino registrado.
    #- 'body_mass_g': refiere a la cantidad de masa corporal, medida en gramos, del pingüino registrado.
    #- 'sex': refiere al sexo del pingüino registrado.

#%% POBLACIONES POR ISLAS
""" Averiguar si las islas están pobladas mayormente por alguna especie en particular, o
 si éstas coexisten, y en ambos casos deberá notificar en qué proporciones.
 Es importante mencionar que deberá reportar sus descubrimientos de manera
 resumida a través de gráficos de barra y de torta."""

#Para la realización del gráfico de barras, decido pasar la información a otro dataframe
#La finlidad es la organización de los datos en un formato diferente que resulte más accesible respecto mi objetivo.
#Este dataframe lo generaré a partir de una consulta SQL

consultaSQL = """
                SELECT 
                    island,
                    COUNT(CASE WHEN species = 'Adelie' THEN 1 END) AS cant_ping_Adelie,
                    COUNT(CASE WHEN species = 'Chinstrap' THEN 1 END) AS cant_ping_Chinstrap,
                    COUNT(CASE WHEN species = 'Gentoo' THEN 1 END) AS cant_ping_Gentoo
                FROM data_ping
                GROUP BY island
              """
aux = dd.sql(consultaSQL).df()

#GRÁFICO DE BARRAS 
fig, ax = plt.subplots()

aux.plot(x = 'island',
                   y = ['cant_ping_Adelie', 'cant_ping_Chinstrap', 'cant_ping_Gentoo'],
                   kind = 'bar',
                   label = ['Cantidad especie: Adelie', 'Cantidad especie: Chinstrap', 'Cantidad especie: Gentoo'], #Agrega etiquetas a la serie
                   ax = ax)

ax.set_title('Cantidad de pingüinos de cada especie por isla')
ax.set_xlabel('Isla')
ax.set_ylabel('Cantidad de pingüinos observados')

ax.legend(title = 'Especie', loc='upper left', frameon=False)


#GRÁFICO DE TORTA

#Para este tipo de gráfico, uso directamente el Dataframe Original
#Armaré tres, uno por cada isla 

#Transformamos la salida del value_counts en un dataframe
conteos = pd.DataFrame(data_ping[data_ping['island'] == 'Biscoe']['species'].value_counts()).reset_index()
conteos = conteos.rename(columns = {'index':'species', 0:'count'})
#Genera el gráfico de barras torta (mejorando la info mostrada)
fig, ax = plt.subplots()

ax.pie(data = conteos,
       x = 'count',
       labels = 'species', #etiquetas
       autopct = '%1.2f%%', #porcentajes
       colors =['green', 'blue', 'orange'],
       shadow = True
       )
 
ax.set_title('Proporción de pingüinos de cada especie en la isla: Biscoe')

conteos = pd.DataFrame(data_ping[data_ping['island'] == 'Dream']['species'].value_counts()).reset_index()
conteos = conteos.rename(columns = {'index':'species', 0:'count'})
#Genera el gráfico de barras torta (mejorando la info mostrada)
fig, ax = plt.subplots()

ax.pie(data = conteos,
       x = 'count',
       labels = 'species', #etiquetas
       autopct = '%1.2f%%', #porcentajes
       colors =['orange', 'blue', 'green'],
       shadow = True
       )
 
ax.set_title('Proporción de pingüinos de cada especie en la isla: Dream')

conteos = pd.DataFrame(data_ping[data_ping['island'] == 'Torgersen']['species'].value_counts()).reset_index()
conteos = conteos.rename(columns = {'index':'species', 0:'count'})
#Genera el gráfico de barras torta (mejorando la info mostrada)
fig, ax = plt.subplots()

ax.pie(data = conteos,
       x = 'count',
       labels = 'species', #etiquetas
       autopct = '%1.2f%%', #porcentajes
       colors =['blue', 'green', 'orange'],
       shadow = True
       )
 
ax.set_title('Proporción de pingüinos de cada especie en la isla: Torgersen')

#%% VISUALIZACIÓN GROSOR PICO (GENERAL Y POR ESPECIE)
"""Realizar un histograma de la variable grosor del pico. Repetir separando por
 especies (con el mismo rango de valores en los ejes, para poder comparar)."""
# Creamos una figura con 2 filas y 2 columnas de subgráficos
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
axs = axs.flatten() #para acceder a cada figura como posición en un array
#Calculamos datos necesarios para generar barras

width = 0.5  #Agruparemos los grosores por 0.5
bins = np.arange(13.0,22.1, width) #Desde 13 a 22 (inclusive) cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping['bill_depth_mm'], bins = bins)


axs[0].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'skyblue', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[0].set_title('Frecuencia del grosor del pico de pingüinos (cada 0.5 milímetros)')
axs[0].set_xlabel('Grosor pico (en milímetros)')
axs[0].set_ylabel('Cantidad de observaciones')
axs[0].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 0.5 en 0.5
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[0].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[0].set_xticklabels(labels, rotation=90, fontsize=11)
axs[0].tick_params(axis = 'x', length = 6, width = 2)

 
#AHORA POR ESPECIES

#--Empezamos con Adelie --#
 
#Calculamos datos necesarios para generar barras

width = 0.5  #Agruparemos los grosores por 0.5
bins = np.arange(13.0,22.1, width) #Desde 13 a 22 (inclusive) cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[data_ping['species'] == 'Adelie']['bill_depth_mm'], bins = bins)


axs[1].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'blue', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[1].set_title('Frecuencia del grosor del pico de pingüinos Adelie (cada 0.5 milímetros)')
axs[1].set_xlabel('Grosor pico (en milímetros)')
axs[1].set_ylabel('Cantidad de observaciones')
axs[1].set_ylim(0, 40)
axs[1].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 0.5 en 0.5
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[1].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[1].set_xticklabels(labels, rotation=90, fontsize=11)
axs[1].tick_params(axis = 'x', length = 6, width = 2)
 

#--Seguimos con Chinstrap --#
 
#Calculamos datos necesarios para generar barras

width = 0.5  #Agruparemos los grosores por 0.5
bins = np.arange(13.0,22.1, width) #Desde 13 a 22 (inclusive) cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[data_ping['species'] == 'Chinstrap']['bill_depth_mm'], bins = bins)


axs[2].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'orange', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[2].set_title('Frecuencia del grosor del pico de pingüinos Chinstrap (cada 0.5 milímetros)')
axs[2].set_xlabel('Grosor pico (en milímetros)')
axs[2].set_ylabel('Cantidad de observaciones')
axs[2].set_ylim(0, 40)
axs[2].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 0.5 en 0.5
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[2].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[2].set_xticklabels(labels, rotation=90, fontsize=11)
axs[2].tick_params(axis = 'x', length = 6, width = 2)
 

#--Finalizamos con Gentoo --#
 
#Calculamos datos necesarios para generar barras

width = 0.5  #Agruparemos los grosores por 0.5
bins = np.arange(13.0,22.1, width) #Desde 13 a 22 (inclusive) cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[data_ping['species'] == 'Gentoo']['bill_depth_mm'], bins = bins)


axs[3].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'green', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[3].set_title('Frecuencia del grosor del pico de pingüinos Gentoo (cada 0.5 milímetros)')
axs[3].set_xlabel('Grosor pico (en milímetros)')
axs[3].set_ylabel('Cantidad de observaciones')
axs[3].set_ylim(0, 40)
axs[3].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 0.5 en 0.5
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[3].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[3].set_xticklabels(labels, rotation=90, fontsize=11)
axs[3].tick_params(axis = 'x', length = 6, width = 2)
 

plt.subplots_adjust(hspace=0.7, wspace = 1.3)

#%% VISUALIZACIÓN LONGITUD PICO (GENERAL Y POR ESPECIE)
"""Realizar un histograma de la variable longitud del pico. Repetir separando por
 especies (con el mismo rango de valores en los ejes, para poder comparar)."""
# Creamos una figura con 2 filas y 2 columnas de subgráficos
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
axs = axs.flatten() #para acceder a cada figura como posición en un array
#Calculamos datos necesarios para generar barras

width = 2  #Agruparemos los grosores por 2mm
bins = np.arange(32.0,60.1, width) #Desde 32 a 60 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping['bill_length_mm'], bins = bins)


axs[0].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'skyblue', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[0].set_title('Frecuencia de la longitud del pico de pingüinos (cada 2 milímetros)')
axs[0].set_xlabel('Longitud pico (en milímetros)')
axs[0].set_ylabel('Cantidad de observaciones')
axs[0].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 2 en 2
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[0].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[0].set_xticklabels(labels, rotation=90, fontsize=11)
axs[0].tick_params(axis = 'x', length = 6, width = 2)

 
#AHORA POR ESPECIES

#--Empezamos con Adelie --#
 
#Calculamos datos necesarios para generar barras

width = 2  #Agruparemos los grosores por 2
bins = np.arange(32.0,60.1, width) #Desde 32 a 60 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[data_ping['species'] == 'Adelie']['bill_length_mm'], bins = bins)


axs[1].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'blue', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[1].set_title('Frecuencia de la longitud del pico de pingüinos Adelie (cada 2 milímetros)')
axs[1].set_xlabel('Longitud pico (en milímetros)')
axs[1].set_ylabel('Cantidad de observaciones')
axs[1].set_ylim(0, 40)
axs[1].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 2 en 2
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[1].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[1].set_xticklabels(labels, rotation=90, fontsize=11)
axs[1].tick_params(axis = 'x', length = 6, width = 2)
 

#--Seguimos con Chinstrap --#
 
#Calculamos datos necesarios para generar barras

width = 2  #Agruparemos los grosores por 2
bins = np.arange(32.0,60.1, width) #Desde 32 a 60 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[data_ping['species'] == 'Chinstrap']['bill_length_mm'], bins = bins)


axs[2].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'orange', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[2].set_title('Frecuencia de la longitud del pico de pingüinos Chinstrap (cada 2 milímetros)')
axs[2].set_xlabel('Longitud pico (en milímetros)')
axs[2].set_ylabel('Cantidad de observaciones')
axs[2].set_ylim(0, 40)
axs[2].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 2 en 2
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[2].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[2].set_xticklabels(labels, rotation=90, fontsize=11)
axs[2].tick_params(axis = 'x', length = 6, width = 2)
 

#--Finalizamos con Gentoo --#
 
#Calculamos datos necesarios para generar barras

width = 2  #Agruparemos los grosores por 2
bins = np.arange(32.0,60.1, width) #Desde 32 a 60 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[data_ping['species'] == 'Gentoo']['bill_length_mm'], bins = bins)


axs[3].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'green', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[3].set_title('Frecuencia de la longitud del pico de pingüinos Gentoo (cada 2 milímetros)')
axs[3].set_xlabel('Longitud pico (en milímetros)')
axs[3].set_ylabel('Cantidad de observaciones')
axs[3].set_ylim(0, 40)
axs[3].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 2 en 2
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[3].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[3].set_xticklabels(labels, rotation=90, fontsize=11)
axs[3].tick_params(axis = 'x', length = 6, width = 2)
 

plt.subplots_adjust(hspace=0.7, wspace = 1.3)

#%% VISUALIZACIÓN LONGITUD ALETA (GENERAL Y POR ESPECIE)
"""Realizar un histograma de la variable longitud aleta. Repetir separando por
 especies (con el mismo rango de valores en los ejes, para poder comparar)."""
# Creamos una figura con 2 filas y 2 columnas de subgráficos
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
axs = axs.flatten() #para acceder a cada figura como posición en un array
#Calculamos datos necesarios para generar barras

width = 10  #Agruparemos los grosores por 10mm
bins = np.arange(172.0,232.1, width) #Desde 172 a 232 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping['flipper_length_mm'], bins = bins)


axs[0].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'skyblue', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[0].set_title('Frecuencia de la longitud de la aleta de pingüinos (cada 10 milímetros)')
axs[0].set_xlabel('Longitud aleta (en milímetros)')
axs[0].set_ylabel('Cantidad de observaciones')
axs[0].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 10 en 10
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[0].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[0].set_xticklabels(labels, rotation=90, fontsize=11)
axs[0].tick_params(axis = 'x', length = 6, width = 2)

 
#AHORA POR ESPECIES

#--Empezamos con Adelie --#
 
#Calculamos datos necesarios para generar barras

width = 10  #Agruparemos los grosores por 10
bins = np.arange(172.0,231.1, width) #Desde 172 a 232 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[data_ping['species'] == 'Adelie']['flipper_length_mm'], bins = bins)


axs[1].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'blue', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[1].set_title('Frecuencia de la longitud de la aleta de pingüinos Adelie (cada 10 milímetros)')
axs[1].set_xlabel('Longitud aleta (en milímetros)')
axs[1].set_ylabel('Cantidad de observaciones')
axs[1].set_ylim(0, 80)
axs[1].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 10 en 10
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[1].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[1].set_xticklabels(labels, rotation=90, fontsize=11)
axs[1].tick_params(axis = 'x', length = 6, width = 2)
 

#--Seguimos con Chinstrap --#
 
#Calculamos datos necesarios para generar barras

width = 10  #Agruparemos los grosores por 10
bins = np.arange(172.0,232.1, width) #Desde 172 a 232 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[data_ping['species'] == 'Chinstrap']['flipper_length_mm'], bins = bins)


axs[2].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'orange', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[2].set_title('Frecuencia de la longitud de la aleta de pingüinos Chinstrap (cada 10 milímetros)')
axs[2].set_xlabel('Longitud aleta (en milímetros)')
axs[2].set_ylabel('Cantidad de observaciones')
axs[2].set_ylim(0, 80)
axs[2].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 10 en 10
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[2].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[2].set_xticklabels(labels, rotation=90, fontsize=11)
axs[2].tick_params(axis = 'x', length = 6, width = 2)
 

#--Finalizamos con Gentoo --#
 
#Calculamos datos necesarios para generar barras

width = 10  #Agruparemos los grosores por 10
bins = np.arange(172.0,232.1, width) #Desde 172 a 232 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[data_ping['species'] == 'Gentoo']['flipper_length_mm'], bins = bins)


axs[3].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'green', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[3].set_title('Frecuencia de la longitud de la aleta de pingüinos Gentoo (cada 10 milímetros)')
axs[3].set_xlabel('Longitud aleta (en milímetros)')
axs[3].set_ylabel('Cantidad de observaciones')
axs[3].set_ylim(0, 80)
axs[3].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 10 en 10
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[3].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[3].set_xticklabels(labels, rotation=90, fontsize=11)
axs[3].tick_params(axis = 'x', length = 6, width = 2)
 

plt.subplots_adjust(hspace=0.9, wspace = 1.8)

#%% VISUALIZACIÓN BODY-MASS (GENERAL Y POR ESPECIE)
"""Realizar un histograma de la variable body-mass. Repetir separando por
 especies (con el mismo rango de valores en los ejes, para poder comparar)."""
# Creamos una figura con 2 filas y 2 columnas de subgráficos
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
axs = axs.flatten() #para acceder a cada figura como posición en un array
#Calculamos datos necesarios para generar barras

width = 450  #Agruparemos los grosores por 450g
bins = np.arange(2700.0,6300.1, width) #Desde 2700 a 6300 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping['body_mass_g'], bins = bins)


axs[0].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'skyblue', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[0].set_title('Frecuencia de body-mass de pingüinos (cada 450g)')
axs[0].set_xlabel('Body-mass pingüinos (en gramos)')
axs[0].set_ylabel('Cantidad de observaciones')
axs[0].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 450 en 450
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[0].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[0].set_xticklabels(labels, rotation=90, fontsize=11)
axs[0].tick_params(axis = 'x', length = 6, width = 2)

 
#AHORA POR ESPECIES

#--Empezamos con Adelie --#
 
#Calculamos datos necesarios para generar barras

width = 450  #Agruparemos los grosores por 450g
bins = np.arange(2700.0,6300.1, width) #Desde 2700 a 6300 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[data_ping['species'] == 'Adelie']['body_mass_g'], bins = bins)


axs[1].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'blue', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[1].set_title('Frecuencia del body-mass de pingüinos Adelie (cada 450g)')
axs[1].set_xlabel('Body-mass (en gramos)')
axs[1].set_ylabel('Cantidad de observaciones')
axs[1].set_ylim(0, 80)
axs[1].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 450 en 450
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[1].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[1].set_xticklabels(labels, rotation=90, fontsize=11)
axs[1].tick_params(axis = 'x', length = 6, width = 2)
 

#--Seguimos con Chinstrap --#
 
#Calculamos datos necesarios para generar barras

width = 450  #Agruparemos los grosores por 450
bins = np.arange(2700.0,6300.1, width) #Desde 2700 a 6300 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[data_ping['species'] == 'Chinstrap']['body_mass_g'], bins = bins)


axs[2].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'orange', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[2].set_title('Frecuencia del body-mass de pingüinos Chinstrap (cada 450g)')
axs[2].set_xlabel('Body-mass (en gramos)')
axs[2].set_ylabel('Cantidad de observaciones')
axs[2].set_ylim(0, 80)
axs[2].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 450 en 450
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[2].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[2].set_xticklabels(labels, rotation=90, fontsize=11)
axs[2].tick_params(axis = 'x', length = 6, width = 2)
 

#--Finalizamos con Gentoo --#
 
#Calculamos datos necesarios para generar barras

width = 450  #Agruparemos los grosores por 450
bins = np.arange(2700.0,6300.1, width) #Desde 2700 a 6300 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[data_ping['species'] == 'Gentoo']['body_mass_g'], bins = bins)


axs[3].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'green', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[3].set_title('Frecuencia del body-mass de pingüinos Gentoo (cada 450g)')
axs[3].set_xlabel('Body-mass (en gramos)')
axs[3].set_ylabel('Cantidad de observaciones')
axs[3].set_ylim(0, 80)
axs[3].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 450 en 450
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[3].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[3].set_xticklabels(labels, rotation=90, fontsize=11)
axs[3].tick_params(axis = 'x', length = 6, width = 2)
 

plt.subplots_adjust(hspace=0.9, wspace = 1.8)

#%% ANÁLISIS CARACTERÍSTICAS FÍSICAS PINGÜINOS POR ESPECIE
"""A partir de estos gráficos, responder:
 a. ¿Se puede determinar la especie de un pingüino a partir de una sola
 característica?
 b. ¿Hay alguna característica que permita discernir entre especies mejor que
 otras?"""

#La especiea se caracterizan por:
    #- Adelie: picos de gran grosor pero de baja longitud.
    #- Chinstrap: picos de importante grosor y longitud a la vez.
    #- Gentoo: aletas largas y gran cantidad de masa corporal; o también por tener pico con importante longitud pero bajo grosor.

#A partir de los histogramas, puedo determinar que el pico es un común diferenciador entre las especies; aunque para la especie Gentoo quizá sea más sencillo ver su body-mass y las aletas.

#%% VISUALIZACIÓN CARACTERÍSTICAS FÍSICAS PINGÜINOS POR SEXO

######EMPEZAMOS POR PINGÜINOS HEMBRAS##############

# Creamos una figura con 2 filas y 2 columnas de subgráficos
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
axs = axs.flatten() #para acceder a cada figura como posición en un array
#Calculamos datos necesarios para generar barras


#--GROSOR PICO--

width = 0.5  #Agruparemos los grosores por 0.5
bins = np.arange(13.0,22.1, width) #Desde 13 a 22 (inclusive) cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[data_ping['sex'] == 'Female']['bill_depth_mm'], bins = bins)


axs[0].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'skyblue', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[0].set_title('Frecuencia del grosor del pico de pingüinos hembras (cada 0.5 milímetros)')
axs[0].set_xlabel('Grosor pico (en milímetros)')
axs[0].set_ylabel('Cantidad de observaciones')
axs[0].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 0.5 en 0.5
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[0].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[0].set_xticklabels(labels, rotation=90, fontsize=11)
axs[0].tick_params(axis = 'x', length = 6, width = 2)

#--LONGITUD PICO--
width = 2  #Agruparemos los grosores por 2mm
bins = np.arange(32.0,60.1, width) #Desde 32 a 60 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[data_ping['sex'] == 'Female']['bill_length_mm'], bins = bins)


axs[1].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'skyblue', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[1].set_title('Frecuencia de la longitud del pico de pingüinos hembras (cada 2 milímetros)')
axs[1].set_xlabel('Longitud pico (en milímetros)')
axs[1].set_ylabel('Cantidad de observaciones')
axs[1].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 2 en 2
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[1].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[1].set_xticklabels(labels, rotation=90, fontsize=11)
axs[1].tick_params(axis = 'x', length = 6, width = 2)


#--LONGITUD ALETA--
width = 10  #Agruparemos los grosores por 10mm
bins = np.arange(172.0,232.1, width) #Desde 172 a 232 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[data_ping['sex'] == 'Female']['flipper_length_mm'], bins = bins)


axs[2].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'skyblue', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[2].set_title('Frecuencia de la longitud de la aleta de pingüinos hembras (cada 10 milímetros)')
axs[2].set_xlabel('Longitud aleta (en milímetros)')
axs[2].set_ylabel('Cantidad de observaciones')
axs[2].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 10 en 10
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[2].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[2].set_xticklabels(labels, rotation=90, fontsize=11)
axs[2].tick_params(axis = 'x', length = 6, width = 2)

#--BODY-MASS--
width = 450  #Agruparemos los grosores por 450g
bins = np.arange(2700.0,6300.1, width) #Desde 2700 a 6300 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[data_ping['sex'] == 'Female']['body_mass_g'], bins = bins)


axs[3].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'skyblue', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[3].set_title('Frecuencia de body-mass de pingüinos hembras(cada 450g)')
axs[3].set_xlabel('Body-mass pingüinos hembras(en gramos)')
axs[3].set_ylabel('Cantidad de observaciones')
axs[3].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 450 en 450
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[3].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[3].set_xticklabels(labels, rotation=90, fontsize=11)
axs[3].tick_params(axis = 'x', length = 6, width = 2)

plt.subplots_adjust(hspace=0.9, wspace = 1.8)


#####PINGÜINOS MACHOS#######

# Creamos una figura con 2 filas y 2 columnas de subgráficos
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
axs = axs.flatten() #para acceder a cada figura como posición en un array
#Calculamos datos necesarios para generar barras


#--GROSOR PICO--

width = 0.5  #Agruparemos los grosores por 0.5
bins = np.arange(13.0,22.1, width) #Desde 13 a 22 (inclusive) cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[data_ping['sex'] == 'Male']['bill_depth_mm'], bins = bins)


axs[0].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'skyblue', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[0].set_title('Frecuencia del grosor del pico de pingüinos machos (cada 0.5 milímetros)')
axs[0].set_xlabel('Grosor pico (en milímetros)')
axs[0].set_ylabel('Cantidad de observaciones')
axs[0].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 0.5 en 0.5
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[0].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[0].set_xticklabels(labels, rotation=90, fontsize=11)
axs[0].tick_params(axis = 'x', length = 6, width = 2)

#--LONGITUD PICO--
width = 2  #Agruparemos los grosores por 2mm
bins = np.arange(32.0,60.1, width) #Desde 32 a 60 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[data_ping['sex'] == 'Male']['bill_length_mm'], bins = bins)


axs[1].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'skyblue', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[1].set_title('Frecuencia de la longitud del pico de pingüinos machos (cada 2 milímetros)')
axs[1].set_xlabel('Longitud pico (en milímetros)')
axs[1].set_ylabel('Cantidad de observaciones')
axs[1].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 2 en 2
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[1].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[1].set_xticklabels(labels, rotation=90, fontsize=11)
axs[1].tick_params(axis = 'x', length = 6, width = 2)


#--LONGITUD ALETA--
width = 10  #Agruparemos los grosores por 10mm
bins = np.arange(172.0,232.1, width) #Desde 172 a 232 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[data_ping['sex'] == 'Male']['flipper_length_mm'], bins = bins)


axs[2].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'skyblue', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[2].set_title('Frecuencia de la longitud de la aleta de pingüinos machos (cada 10 milímetros)')
axs[2].set_xlabel('Longitud aleta (en milímetros)')
axs[2].set_ylabel('Cantidad de observaciones')
axs[2].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 10 en 10
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[2].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[2].set_xticklabels(labels, rotation=90, fontsize=11)
axs[2].tick_params(axis = 'x', length = 6, width = 2)

#--BODY-MASS--
width = 450  #Agruparemos los grosores por 450g
bins = np.arange(2700.0,6300.1, width) #Desde 2700 a 6300 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[data_ping['sex'] == 'Male']['body_mass_g'], bins = bins)


axs[3].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'skyblue', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[3].set_title('Frecuencia de body-mass de pingüinos machos (cada 450g)')
axs[3].set_xlabel('Body-mass pingüinos machos(en gramos)')
axs[3].set_ylabel('Cantidad de observaciones')
axs[3].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 450 en 450
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[3].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[3].set_xticklabels(labels, rotation=90, fontsize=11)
axs[3].tick_params(axis = 'x', length = 6, width = 2)

plt.subplots_adjust(hspace=0.9, wspace = 1.8)

#%% ANÁLISIS CARACTERÍSTICAS FÍSICAS PINGÜINOS POR SEXO
#Si bien es notorio que los machos tienden a tener métricas más elevadas, son muchas las hembras y machos con índices muy similares. 
#Por lo tanto, no es plausible la categorización del sexo a través de una de estas cuatro características.

#%% VISUALIZACIÓN CARACTERÍSTICAS FÍSICAS PINGÜINOS POR SEXO Y POR ESPECIE: PINGÜINOS ADELIE

#####PINGÜINOS HEMBRAS#######

# Creamos una figura con 2 filas y 2 columnas de subgráficos
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
axs = axs.flatten() #para acceder a cada figura como posición en un array
#Calculamos datos necesarios para generar barras


#--GROSOR PICO--
width = 0.5  #Agruparemos los grosores por 0.5
bins = np.arange(13.0,22.1, width) #Desde 13 a 22 (inclusive) cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[(data_ping['species'] == 'Adelie') & (data_ping['sex'] == 'Female')]['bill_depth_mm'], bins = bins)


axs[0].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'blue', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[0].set_title('Frecuencia del grosor del pico de pingüinos Adelie hembras (cada 0.5 milímetros)')
axs[0].set_xlabel('Grosor pico (en milímetros)')
axs[0].set_ylabel('Cantidad de observaciones')
axs[0].set_ylim(0, 40)
axs[0].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 0.5 en 0.5
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[0].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[0].set_xticklabels(labels, rotation=90, fontsize=11)
axs[0].tick_params(axis = 'x', length = 6, width = 2)

#--LONGITUD PICO--
width = 2  #Agruparemos los grosores por 2
bins = np.arange(32.0,60.1, width) #Desde 32 a 60 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[(data_ping['species'] == 'Adelie') & (data_ping['sex'] == 'Female')]['bill_length_mm'], bins = bins)


axs[1].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'blue', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[1].set_title('Frecuencia de la longitud del pico de pingüinos Adelie hembras (cada 2 milímetros)')
axs[1].set_xlabel('Longitud pico (en milímetros)')
axs[1].set_ylabel('Cantidad de observaciones')
axs[1].set_ylim(0, 40)
axs[1].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 2 en 2
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[1].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[1].set_xticklabels(labels, rotation=90, fontsize=11)
axs[1].tick_params(axis = 'x', length = 6, width = 2)

#--LONGITUD ALETA
width = 10  #Agruparemos los grosores por 10
bins = np.arange(172.0,231.1, width) #Desde 172 a 232 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[(data_ping['species'] == 'Adelie') & (data_ping['sex'] == 'Female')]['flipper_length_mm'], bins = bins)


axs[2].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'blue', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[2].set_title('Frecuencia de la longitud de la aleta de pingüinos Adelie hembras (cada 10 milímetros)')
axs[2].set_xlabel('Longitud aleta (en milímetros)')
axs[2].set_ylabel('Cantidad de observaciones')
axs[2].set_ylim(0, 80)
axs[2].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 10 en 10
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[2].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[2].set_xticklabels(labels, rotation=90, fontsize=11)
axs[2].tick_params(axis = 'x', length = 6, width = 2)

#--BODY-MASS
width = 450  #Agruparemos los grosores por 450g
bins = np.arange(2700.0,6300.1, width) #Desde 2700 a 6300 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[(data_ping['species'] == 'Adelie') & (data_ping['sex'] == 'Female')]['body_mass_g'], bins = bins)


axs[3].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'blue', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[3].set_title('Frecuencia del body-mass de pingüinos Adelie hembras (cada 450g)')
axs[3].set_xlabel('Body-mass (en gramos)')
axs[3].set_ylabel('Cantidad de observaciones')
axs[3].set_ylim(0, 80)
axs[3].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 450 en 450
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[3].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[3].set_xticklabels(labels, rotation=90, fontsize=11)
axs[3].tick_params(axis = 'x', length = 6, width = 2)

plt.subplots_adjust(hspace=0.9, wspace = 2)

#####PINGÜINOS MACHOS#######

# Creamos una figura con 2 filas y 2 columnas de subgráficos
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
axs = axs.flatten() #para acceder a cada figura como posición en un array
#Calculamos datos necesarios para generar barras


#--GROSOR PICO--
width = 0.5  #Agruparemos los grosores por 0.5
bins = np.arange(13.0,22.1, width) #Desde 13 a 22 (inclusive) cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[(data_ping['species'] == 'Adelie') & (data_ping['sex'] == 'Male')]['bill_depth_mm'], bins = bins)


axs[0].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'blue', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[0].set_title('Frecuencia del grosor del pico de pingüinos Adelie machos (cada 0.5 milímetros)')
axs[0].set_xlabel('Grosor pico (en milímetros)')
axs[0].set_ylabel('Cantidad de observaciones')
axs[0].set_ylim(0, 40)
axs[0].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 0.5 en 0.5
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[0].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[0].set_xticklabels(labels, rotation=90, fontsize=11)
axs[0].tick_params(axis = 'x', length = 6, width = 2)

#--LONGITUD PICO--
width = 2  #Agruparemos los grosores por 2
bins = np.arange(32.0,60.1, width) #Desde 32 a 60 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[(data_ping['species'] == 'Adelie') & (data_ping['sex'] == 'Male')]['bill_length_mm'], bins = bins)


axs[1].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'blue', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[1].set_title('Frecuencia de la longitud del pico de pingüinos Adelie machos (cada 2 milímetros)')
axs[1].set_xlabel('Longitud pico (en milímetros)')
axs[1].set_ylabel('Cantidad de observaciones')
axs[1].set_ylim(0, 40)
axs[1].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 2 en 2
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[1].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[1].set_xticklabels(labels, rotation=90, fontsize=11)
axs[1].tick_params(axis = 'x', length = 6, width = 2)

#--LONGITUD ALETA
width = 10  #Agruparemos los grosores por 10
bins = np.arange(172.0,231.1, width) #Desde 172 a 232 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[(data_ping['species'] == 'Adelie') & (data_ping['sex'] == 'Male')]['flipper_length_mm'], bins = bins)


axs[2].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'blue', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[2].set_title('Frecuencia de la longitud de la aleta de pingüinos Adelie machos (cada 10 milímetros)')
axs[2].set_xlabel('Longitud aleta (en milímetros)')
axs[2].set_ylabel('Cantidad de observaciones')
axs[2].set_ylim(0, 80)
axs[2].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 10 en 10
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[2].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[2].set_xticklabels(labels, rotation=90, fontsize=11)
axs[2].tick_params(axis = 'x', length = 6, width = 2)

#--BODY-MASS
width = 450  #Agruparemos los grosores por 450g
bins = np.arange(2700.0,6300.1, width) #Desde 2700 a 6300 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[(data_ping['species'] == 'Adelie') & (data_ping['sex'] == 'Male')]['body_mass_g'], bins = bins)


axs[3].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'blue', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[3].set_title('Frecuencia del body-mass de pingüinos Adelie machos (cada 450g)')
axs[3].set_xlabel('Body-mass (en gramos)')
axs[3].set_ylabel('Cantidad de observaciones')
axs[3].set_ylim(0, 80)
axs[3].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 450 en 450
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[3].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[3].set_xticklabels(labels, rotation=90, fontsize=11)
axs[3].tick_params(axis = 'x', length = 6, width = 2)

plt.subplots_adjust(hspace=0.9, wspace = 2)

#%%VISUALIZACIÓN CARACTERÍSTICAS FÍSICAS PINGÜINOS POR SEXO Y POR ESPECIE: PINGÜINOS ADELIE
#Nuevamente, en general, los machos presentan métricas más elevadas
#Esto ocurre de forma más notoria cuando se analiza la masa corporal, aunque el grosor del pico también es un factor clave.
#Si bien las frecuencias no son muy diversas entre sí, se halla cierta relación entre estas dos características y el sexo del pingüino.

#%% ANÁLISIS CARACTERÍSTICAS FÍSICAS PINGÜINOS POR SEXO Y POR ESPECIE: PINGÜINOS CHINSTRAP

#####PINGÜINOS HEMBRAS#######

# Creamos una figura con 2 filas y 2 columnas de subgráficos
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
axs = axs.flatten() #para acceder a cada figura como posición en un array
#Calculamos datos necesarios para generar barras


#--GROSOR PICO--
width = 0.5  #Agruparemos los grosores por 0.5
bins = np.arange(13.0,22.1, width) #Desde 13 a 22 (inclusive) cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[(data_ping['species'] == 'Chinstrap') & (data_ping['sex'] == 'Female')]['bill_depth_mm'], bins = bins)


axs[0].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'orange', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[0].set_title('Frecuencia del grosor del pico de pingüinos Chinstrap hembras (cada 0.5 milímetros)')
axs[0].set_xlabel('Grosor pico (en milímetros)')
axs[0].set_ylabel('Cantidad de observaciones')
axs[0].set_ylim(0, 40)
axs[0].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 0.5 en 0.5
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[0].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[0].set_xticklabels(labels, rotation=90, fontsize=11)
axs[0].tick_params(axis = 'x', length = 6, width = 2)

#--LONGITUD PICO--
width = 2  #Agruparemos los grosores por 2
bins = np.arange(32.0,60.1, width) #Desde 32 a 60 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[(data_ping['species'] == 'Chinstrap') & (data_ping['sex'] == 'Female')]['bill_length_mm'], bins = bins)


axs[1].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'orange', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[1].set_title('Frecuencia de la longitud del pico de pingüinos Chinstrap hembras (cada 2 milímetros)')
axs[1].set_xlabel('Longitud pico (en milímetros)')
axs[1].set_ylabel('Cantidad de observaciones')
axs[1].set_ylim(0, 40)
axs[1].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 2 en 2
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[1].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[1].set_xticklabels(labels, rotation=90, fontsize=11)
axs[1].tick_params(axis = 'x', length = 6, width = 2)

#--LONGITUD-ALETA
width = 10  #Agruparemos los grosores por 10
bins = np.arange(172.0,232.1, width) #Desde 172 a 232 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[(data_ping['species'] == 'Chinstrap') & (data_ping['sex'] == 'Female')]['flipper_length_mm'], bins = bins)


axs[2].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'orange', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[2].set_title('Frecuencia de la longitud de la aleta de pingüinos Chinstrap hembras (cada 10 milímetros)')
axs[2].set_xlabel('Longitud aleta (en milímetros)')
axs[2].set_ylabel('Cantidad de observaciones')
axs[2].set_ylim(0, 80)
axs[2].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 10 en 10
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[2].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[2].set_xticklabels(labels, rotation=90, fontsize=11)
axs[2].tick_params(axis = 'x', length = 6, width = 2)

#--BODY-MASS
width = 450  #Agruparemos los grosores por 450
bins = np.arange(2700.0,6300.1, width) #Desde 2700 a 6300 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[(data_ping['species'] == 'Chinstrap') & (data_ping['sex'] == 'Female')]['body_mass_g'], bins = bins)


axs[3].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'orange', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[3].set_title('Frecuencia del body-mass de pingüinos Chinstrap hembras (cada 450g)')
axs[3].set_xlabel('Body-mass (en gramos)')
axs[3].set_ylabel('Cantidad de observaciones')
axs[3].set_ylim(0, 80)
axs[3].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 450 en 450
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[3].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[3].set_xticklabels(labels, rotation=90, fontsize=11)
axs[3].tick_params(axis = 'x', length = 6, width = 2)

plt.subplots_adjust(hspace=0.9, wspace = 2.4)


#####PINGÜINOS MACHOS#######

# Creamos una figura con 2 filas y 2 columnas de subgráficos
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
axs = axs.flatten() #para acceder a cada figura como posición en un array
#Calculamos datos necesarios para generar barras


#--GROSOR PICO--
width = 0.5  #Agruparemos los grosores por 0.5
bins = np.arange(13.0,22.1, width) #Desde 13 a 22 (inclusive) cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[(data_ping['species'] == 'Chinstrap') & (data_ping['sex'] == 'Male')]['bill_depth_mm'], bins = bins)


axs[0].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'orange', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[0].set_title('Frecuencia del grosor del pico de pingüinos Chinstrap machos(cada 0.5 milímetros)')
axs[0].set_xlabel('Grosor pico (en milímetros)')
axs[0].set_ylabel('Cantidad de observaciones')
axs[0].set_ylim(0, 40)
axs[0].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 0.5 en 0.5
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[0].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[0].set_xticklabels(labels, rotation=90, fontsize=11)
axs[0].tick_params(axis = 'x', length = 6, width = 2)

#--LONGITUD PICO--
width = 2  #Agruparemos los grosores por 2
bins = np.arange(32.0,60.1, width) #Desde 32 a 60 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[(data_ping['species'] == 'Chinstrap') & (data_ping['sex'] == 'Male')]['bill_length_mm'], bins = bins)


axs[1].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'orange', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[1].set_title('Frecuencia de la longitud del pico de pingüinos Chinstrap machos (cada 2 milímetros)')
axs[1].set_xlabel('Longitud pico (en milímetros)')
axs[1].set_ylabel('Cantidad de observaciones')
axs[1].set_ylim(0, 40)
axs[1].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 2 en 2
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[1].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[1].set_xticklabels(labels, rotation=90, fontsize=11)
axs[1].tick_params(axis = 'x', length = 6, width = 2)

#--LONGITUD-ALETA
width = 10  #Agruparemos los grosores por 10
bins = np.arange(172.0,232.1, width) #Desde 172 a 232 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[(data_ping['species'] == 'Chinstrap') & (data_ping['sex'] == 'Male')]['flipper_length_mm'], bins = bins)


axs[2].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'orange', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[2].set_title('Frecuencia de la longitud de la aleta de pingüinos Chinstrap machos (cada 10 milímetros)')
axs[2].set_xlabel('Longitud aleta (en milímetros)')
axs[2].set_ylabel('Cantidad de observaciones')
axs[2].set_ylim(0, 80)
axs[2].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 10 en 10
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[2].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[2].set_xticklabels(labels, rotation=90, fontsize=11)
axs[2].tick_params(axis = 'x', length = 6, width = 2)

#--BODY-MASS
width = 450  #Agruparemos los grosores por 450
bins = np.arange(2700.0,6300.1, width) #Desde 2700 a 6300 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[(data_ping['species'] == 'Chinstrap') & (data_ping['sex'] == 'Male')]['body_mass_g'], bins = bins)


axs[3].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'orange', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[3].set_title('Frecuencia del body-mass de pingüinos Chinstrap machos (cada 450g)')
axs[3].set_xlabel('Body-mass (en gramos)')
axs[3].set_ylabel('Cantidad de observaciones')
axs[3].set_ylim(0, 80)
axs[3].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 450 en 450
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[3].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[3].set_xticklabels(labels, rotation=90, fontsize=11)
axs[3].tick_params(axis = 'x', length = 6, width = 2)

plt.subplots_adjust(hspace=0.9, wspace = 2.4)

#%% ANÁLISIS CARACTERÍSTICAS FÍSICAS PINGÜINOS POR SEXO Y POR ESPECIE: PINGÜINOS CHINSTRAP
#Las variables suelen tomar valores similares entre ambas especies.
#La distinción más notoria está en la longitud del pico. Los machos tienden a tener un pico más alargado.
#A la vez, las hembras suelen tener aletas más cortas.
#En definitiva, ante miembros de la especie, éstos son los parámetros que disciernen el sexo del pingüino.

#%% VISUALIZACIÓN CARACTERÍSTICAS FÍSICAS PINGÜINOS POR SEXO Y POR ESPECIE: PINGÜINOS GETOO

#####PINGÜINOS HEMBRAS#######

# Creamos una figura con 2 filas y 2 columnas de subgráficos
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
axs = axs.flatten() #para acceder a cada figura como posición en un array
#Calculamos datos necesarios para generar barras


#--GROSOR PICO--
width = 0.5  #Agruparemos los grosores por 0.5
bins = np.arange(13.0,22.1, width) #Desde 13 a 22 (inclusive) cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[(data_ping['species'] == 'Gentoo') & (data_ping['sex'] == 'Female')]['bill_depth_mm'], bins = bins)


axs[0].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'green', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[0].set_title('Frecuencia del grosor del pico de pingüinos Gentoo hembras (cada 0.5 milímetros)')
axs[0].set_xlabel('Grosor pico (en milímetros)')
axs[0].set_ylabel('Cantidad de observaciones')
axs[0].set_ylim(0, 40)
axs[0].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 0.5 en 0.5
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[0].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[0].set_xticklabels(labels, rotation=90, fontsize=11)
axs[0].tick_params(axis = 'x', length = 6, width = 2)
 

#--LONGITUD PICO--
width = 2  #Agruparemos los grosores por 2
bins = np.arange(32.0,60.1, width) #Desde 32 a 60 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[(data_ping['species'] == 'Gentoo') & (data_ping['sex'] == 'Female')]['bill_length_mm'], bins = bins)


axs[1].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'green', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[1].set_title('Frecuencia de la longitud del pico de pingüinos Gentoo hembras (cada 2 milímetros)')
axs[1].set_xlabel('Longitud pico (en milímetros)')
axs[1].set_ylabel('Cantidad de observaciones')
axs[1].set_ylim(0, 40)
axs[1].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 2 en 2
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[1].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[1].set_xticklabels(labels, rotation=90, fontsize=11)
axs[1].tick_params(axis = 'x', length = 6, width = 2)
 

#--LONGITUD ALETA
width = 10  #Agruparemos los grosores por 10
bins = np.arange(172.0,232.1, width) #Desde 172 a 232 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[(data_ping['species'] == 'Gentoo') & (data_ping['sex'] == 'Female')]['flipper_length_mm'], bins = bins)


axs[2].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'green', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[2].set_title('Frecuencia de la longitud de la aleta de pingüinos Gentoo hembras (cada 10 milímetros)')
axs[2].set_xlabel('Longitud aleta (en milímetros)')
axs[2].set_ylabel('Cantidad de observaciones')
axs[2].set_ylim(0, 80)
axs[2].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 10 en 10
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[2].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[2].set_xticklabels(labels, rotation=90, fontsize=11)
axs[2].tick_params(axis = 'x', length = 6, width = 2)

#--BODY-MASS
width = 450  #Agruparemos los grosores por 450
bins = np.arange(2700.0,6300.1, width) #Desde 2700 a 6300 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[(data_ping['species'] == 'Gentoo') & (data_ping['sex'] == 'Female')]['body_mass_g'], bins = bins)


axs[3].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'green', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[3].set_title('Frecuencia del body-mass de pingüinos Gentoo hembras (cada 450g)')
axs[3].set_xlabel('Body-mass (en gramos)')
axs[3].set_ylabel('Cantidad de observaciones')
axs[3].set_ylim(0, 80)
axs[3].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 450 en 450
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[3].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[3].set_xticklabels(labels, rotation=90, fontsize=11)
axs[3].tick_params(axis = 'x', length = 6, width = 2)

plt.subplots_adjust(hspace=1, wspace = 2.1)


#####PINGÜINOS MACHOS#######

# Creamos una figura con 2 filas y 2 columnas de subgráficos
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
axs = axs.flatten() #para acceder a cada figura como posición en un array
#Calculamos datos necesarios para generar barras


#--GROSOR PICO--
width = 0.5  #Agruparemos los grosores por 0.5
bins = np.arange(13.0,22.1, width) #Desde 13 a 22 (inclusive) cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[(data_ping['species'] == 'Gentoo') & (data_ping['sex'] == 'Male')]['bill_depth_mm'], bins = bins)


axs[0].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'green', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[0].set_title('Frecuencia del grosor del pico de pingüinos Gentoo machos (cada 0.5 milímetros)')
axs[0].set_xlabel('Grosor pico (en milímetros)')
axs[0].set_ylabel('Cantidad de observaciones')
axs[0].set_ylim(0, 40)
axs[0].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 0.5 en 0.5
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[0].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[0].set_xticklabels(labels, rotation=90, fontsize=11)
axs[0].tick_params(axis = 'x', length = 6, width = 2)
 

#--LONGITUD PICO--
width = 2  #Agruparemos los grosores por 2
bins = np.arange(32.0,60.1, width) #Desde 32 a 60 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[(data_ping['species'] == 'Gentoo') & (data_ping['sex'] == 'Male')]['bill_length_mm'], bins = bins)


axs[1].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'green', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[1].set_title('Frecuencia de la longitud del pico de pingüinos Gentoo machos (cada 2 milímetros)')
axs[1].set_xlabel('Longitud pico (en milímetros)')
axs[1].set_ylabel('Cantidad de observaciones')
axs[1].set_ylim(0, 40)
axs[1].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 2 en 2
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[1].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[1].set_xticklabels(labels, rotation=90, fontsize=11)
axs[1].tick_params(axis = 'x', length = 6, width = 2)
 

#--LONGITUD ALETA
width = 10  #Agruparemos los grosores por 10
bins = np.arange(172.0,232.1, width) #Desde 172 a 232 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[(data_ping['species'] == 'Gentoo') & (data_ping['sex'] == 'Male')]['flipper_length_mm'], bins = bins)


axs[2].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'green', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[2].set_title('Frecuencia de la longitud de la aleta de pingüinos Gentoo machos (cada 10 milímetros)')
axs[2].set_xlabel('Longitud aleta (en milímetros)')
axs[2].set_ylabel('Cantidad de observaciones')
axs[2].set_ylim(0, 80)
axs[2].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 10 en 10
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[2].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[2].set_xticklabels(labels, rotation=90, fontsize=11)
axs[2].tick_params(axis = 'x', length = 6, width = 2)

#--BODY-MASS
width = 450  #Agruparemos los grosores por 450
bins = np.arange(2700.0,6300.1, width) #Desde 2700 a 6300 cada width grosor

#Contamos cuántos de los datos caen en cada uno de los bins
counts, bins = np.histogram(data_ping[(data_ping['species'] == 'Gentoo') & (data_ping['sex'] == 'Male')]['body_mass_g'], bins = bins)


axs[3].bar(x = bins[:-1], 
       height = counts, #Alto de la barra 
       width = width,   #Ancho de la barra
       color = 'green', #Color de la barra
       edgecolor = 'black' #Color del borde
       )
 
 
axs[3].set_title('Frecuencia del body-mass de pingüinos Gentoo machos (cada 450g)')
axs[3].set_xlabel('Body-mass (en gramos)')
axs[3].set_ylabel('Cantidad de observaciones')
axs[3].set_ylim(0, 80)
axs[3].spines[['right','top']].set_visible(False)

#Quiero que las etiquetas del eje X muestren los rangos de los grosores de pico

centers = bins[:-1] #Para que estén centradas en la barra

# Genera el string de los labels con intervalos de 450 en 450
labels = [f'({edge:.1f}, {bins[i+1]:.1f}]' for i, edge in enumerate(bins[:-1])]

axs[3].set_xticks(centers, labels) #ubica los ticks del eje x
#Asigna los labels a los ticks del eje x
axs[3].set_xticklabels(labels, rotation=90, fontsize=11)
axs[3].tick_params(axis = 'x', length = 6, width = 2)

plt.subplots_adjust(hspace=1, wspace = 2.1)

#%% ANÁLISIS CARACTERÍSTICAS FÍSICAS PINGÜINOS POR SEXO Y POR ESPECIE: PINGÜINOS GETOO
#Los machos presentan en promedio métricas más elevadas.
#Aquellas diferencias que más frecuentemente se encuentran son las relacionadas a la masa corporal y la longitud del pico.
#Es entonces que ante miembros de la misma especie, son éstos los atributos que mejor disciernen el sexo.

#%% VISUALIZACIÓN DE SEXOS A TRAVÉS DE PARES VARIABLES CORPORALES
"""Realizar scatterplots de pares de variables corporales, separadas por sexo. A partir
 de los gráficos, responder:
 a. ¿Hay algún par de variables que permita deducir el sexo?
 """

#Quiero hacer una imágen que contenga los gráficos de GROSOR PICO-LONGITUD PICO y MASA CORPORAL-LONGITUD ALETA
fig, axs = plt.subplots(1, 2, figsize=(12, 8)) #devuelve una tupla
axs = axs.flatten()

hembras = data_ping[data_ping['sex'] == 'Female']
machos = data_ping[data_ping['sex'] == 'Male']


#GROSOR Y LONGITUD DEL PICO

axs[0].scatter(data = hembras, x = 'bill_depth_mm',
           y = 'bill_length_mm', c = 'purple', edgecolor = 'k', label = 'hembras')

axs[0].scatter(data = machos, x = 'bill_depth_mm',
           y = 'bill_length_mm', c = 'blue', edgecolor = 'k', label = 'machos')


axs[0].set_title('Relación entre el grosor y longitud del pico') # Título de gráfico
axs[0].set_xlabel('Grosor del pico (en milímetros)', fontsize = 'medium') # Nombre eje X
axs[0].set_ylabel('Longitud del pico (en milímetros)', fontsize = 'medium') # Nombre eje Y

axs[0].legend()

#--BODY MASS & LONGITUD ALETAS
axs[1].scatter(data = hembras, x = 'body_mass_g',
           y = 'flipper_length_mm', c = 'purple', edgecolor = 'k', label = 'hembras')

axs[1].scatter(data = machos, x = 'body_mass_g',
           y = 'flipper_length_mm', c = 'blue', edgecolor = 'k', label = 'machos')


axs[1].set_title('Relación entre la masa corporal y la longitud de las aletas') # Título de gráfico
axs[1].set_xlabel('Masa corporal (en gramos)', fontsize = 'medium') # Nombre eje X
axs[1].set_ylabel('Longitud de las aletas (en milímetros)', fontsize = 'medium') # Nombre eje Y

axs[1].legend()

#%% ANÁLISIS DE DISTINCIÓN DE SEXOS A TRAVÉS DE PARES VARIABLES CORPORALES

#A partir de los SCATTER-PLOTS generados, se puede observar que:
    #los machos presentan por lo general un pico con mayores dimensiones
    #en promedio los machos son más grandes corporalmente, aunque también hay varias hembras de grandes proporciones.

#%% VISUALIZACIÓN DE SEXOS DE LA ESPECIE ADELIE TRAVÉS DE PARES VARIABLES CORPORALES
"""Realizar scatterplots de pares de variables corporales, separadas por sexo. A partir
 de los gráficos, responder:
 b. ¿Y si se fija una especie en particular?"""

#Quiero hacer una imágen que contenga los gráficos de GROSOR PICO-LONGITUD PICO y MASA CORPORAL-LONGITUD ALETA
fig, axs = plt.subplots(1, 2, figsize=(12, 8)) #devuelve una tupla
axs = axs.flatten()

hembras = data_ping[(data_ping['sex'] == 'Female') & (data_ping['species'] == 'Adelie')]
machos = data_ping[(data_ping['sex'] == 'Male') & (data_ping['species'] == 'Adelie')]


#GROSOR Y LONGITUD DEL PICO

axs[0].scatter(data = hembras, x = 'bill_depth_mm',
           y = 'bill_length_mm', c = 'purple', edgecolor = 'k', label = 'hembras')

axs[0].scatter(data = machos, x = 'bill_depth_mm',
           y = 'bill_length_mm', c = 'blue', edgecolor = 'k', label = 'machos')


axs[0].set_title('Relación entre el grosor y longitud del pico pingüinos Adelie') # Título de gráfico
axs[0].set_xlabel('Grosor del pico (en milímetros)', fontsize = 'medium') # Nombre eje X
axs[0].set_ylabel('Longitud del pico (en milímetros)', fontsize = 'medium') # Nombre eje Y

axs[0].legend()

#--BODY MASS & LONGITUD ALETAS
axs[1].scatter(data = hembras, x = 'body_mass_g',
           y = 'flipper_length_mm', c = 'purple', edgecolor = 'k', label = 'hembras')

axs[1].scatter(data = machos, x = 'body_mass_g',
           y = 'flipper_length_mm', c = 'blue', edgecolor = 'k', label = 'machos')


axs[1].set_title('Relación entre la masa corporal y la longitud de las aletas pingüinos Adelie') # Título de gráfico
axs[1].set_xlabel('Masa corporal (en gramos)', fontsize = 'medium') # Nombre eje X
axs[1].set_ylabel('Longitud de las aletas (en milímetros)', fontsize = 'medium') # Nombre eje Y

axs[1].legend()

plt.subplots_adjust(wspace = 0.8)

#%% VISUALIZACIÓN DE SEXOS DE LA ESPECIE CHINSTRAP TRAVÉS DE PARES VARIABLES CORPORALES
"""Realizar scatterplots de pares de variables corporales, separadas por sexo. A partir
 de los gráficos, responder:
 b. ¿Y si se fija una especie en particular?"""

#Quiero hacer una imágen que contenga los gráficos de GROSOR PICO-LONGITUD PICO y MASA CORPORAL-LONGITUD ALETA
fig, axs = plt.subplots(1, 2, figsize=(12, 8)) #devuelve una tupla
axs = axs.flatten()

hembras = data_ping[(data_ping['sex'] == 'Female') & (data_ping['species'] == 'Chinstrap')]
machos = data_ping[(data_ping['sex'] == 'Male') & (data_ping['species'] == 'Chinstrap')]


#GROSOR Y LONGITUD DEL PICO

axs[0].scatter(data = hembras, x = 'bill_depth_mm',
           y = 'bill_length_mm', c = 'purple', edgecolor = 'k', label = 'hembras')

axs[0].scatter(data = machos, x = 'bill_depth_mm',
           y = 'bill_length_mm', c = 'blue', edgecolor = 'k', label = 'machos')


axs[0].set_title('Relación entre el grosor y longitud del pico pingüinos Chinstrap') # Título de gráfico
axs[0].set_xlabel('Grosor del pico (en milímetros)', fontsize = 'medium') # Nombre eje X
axs[0].set_ylabel('Longitud del pico (en milímetros)', fontsize = 'medium') # Nombre eje Y

axs[0].legend()

#--BODY MASS & LONGITUD ALETAS
axs[1].scatter(data = hembras, x = 'body_mass_g',
           y = 'flipper_length_mm', c = 'purple', edgecolor = 'k', label = 'hembras')

axs[1].scatter(data = machos, x = 'body_mass_g',
           y = 'flipper_length_mm', c = 'blue', edgecolor = 'k', label = 'machos')

axs[1].set_title('Relación entre la masa corporal y la longitud de las aletas pingüinos Chinstrap') # Título de gráfico
axs[1].set_xlabel('Masa corporal (en gramos)', fontsize = 'medium') # Nombre eje X
axs[1].set_ylabel('Longitud de las aletas (en milímetros)', fontsize = 'medium') # Nombre eje Y

axs[1].legend()

plt.subplots_adjust(wspace = 1)

#%% VISUALIZACIÓN DE SEXOS DE LA ESPECIE GENTOO TRAVÉS DE PARES VARIABLES CORPORALES
"""Realizar scatterplots de pares de variables corporales, separadas por sexo. A partir
 de los gráficos, responder:
 b. ¿Y si se fija una especie en particular?"""

#Quiero hacer una imágen que contenga los gráficos de GROSOR PICO-LONGITUD PICO y MASA CORPORAL-LONGITUD ALETA
fig, axs = plt.subplots(1, 2, figsize=(12, 8)) #devuelve una tupla
axs = axs.flatten()

hembras = data_ping[(data_ping['sex'] == 'Female') & (data_ping['species'] == 'Gentoo')]
machos = data_ping[(data_ping['sex'] == 'Male') & (data_ping['species'] == 'Gentoo')]


#GROSOR Y LONGITUD DEL PICO

axs[0].scatter(data = hembras, x = 'bill_depth_mm',
           y = 'bill_length_mm', c = 'purple', edgecolor = 'k', label = 'hembras')

axs[0].scatter(data = machos, x = 'bill_depth_mm',
           y = 'bill_length_mm', c = 'blue', edgecolor = 'k', label = 'machos')


axs[0].set_title('Relación entre el grosor y longitud del pico pingüinos Gentoo') # Título de gráfico
axs[0].set_xlabel('Grosor del pico (en milímetros)', fontsize = 'medium') # Nombre eje X
axs[0].set_ylabel('Longitud del pico (en milímetros)', fontsize = 'medium') # Nombre eje Y

axs[0].legend()

#--BODY MASS & LONGITUD ALETAS
axs[1].scatter(data = hembras, x = 'body_mass_g',
           y = 'flipper_length_mm', c = 'purple', edgecolor = 'k', label = 'hembras')

axs[1].scatter(data = machos, x = 'body_mass_g',
           y = 'flipper_length_mm', c = 'blue', edgecolor = 'k', label = 'machos')

axs[1].set_title('Relación entre la masa corporal y la longitud de las aletas pingüinos Gentoo') # Título de gráfico
axs[1].set_xlabel('Masa corporal (en gramos)', fontsize = 'medium') # Nombre eje X
axs[1].set_ylabel('Longitud de las aletas (en milímetros)', fontsize = 'medium') # Nombre eje Y

axs[1].legend()

plt.subplots_adjust(wspace = 0.8)


#%% ANÁLISIS DE DISTINCIÓN DE SEXOS POR ESPECIE A TRAVÉS DE PARES VARIABLES CORPORALES

#Si se analiza cada especie por separado, es claro que los machos presentan:
    #-Picos de mayores dimensiones.
    #-Cuerpos más robustos.
    
#En definitiva, los machos son fácilmente distinguibles de las hembras si analizamos poblaciones de una misma especie.

#%% VISUALIZACIÓN DIMENSIONES DEL PICO POR ESPECIE

"""Realizar un scatterplot de las variables largo y grosor del pico agregando colores
 para distinguir las especies."""

#Quiero hacer una imágen que contenga los gráficos de GROSOR PICO-LONGITUD PICO y MASA CORPORAL-LONGITUD ALETA
fig, ax = plt.subplots() #devuelve una tupla

adelie = data_ping[data_ping['species'] == 'Adelie']
chinstrap = data_ping[data_ping['species'] == 'Chinstrap']
gentoo = data_ping[data_ping['species'] == 'Gentoo']

#GROSOR Y LONGITUD DEL PICO

ax.scatter(data = adelie, x = 'bill_depth_mm',
           y = 'bill_length_mm', c = 'blue', edgecolor = 'k', label = 'Adelie')

ax.scatter(data = chinstrap, x = 'bill_depth_mm',
           y = 'bill_length_mm', c = 'orange', edgecolor = 'k', label = 'Chinstrap')


ax.scatter(data = gentoo, x = 'bill_depth_mm',
           y = 'bill_length_mm', c = 'green', edgecolor = 'k', label = 'Gentoo')

ax.set_title('Relación entre el grosor y longitud del pico pingüinos Adelie') # Título de gráfico
ax.set_xlabel('Grosor del pico (en milímetros)', fontsize = 'medium') # Nombre eje X
ax.set_ylabel('Longitud del pico (en milímetros)', fontsize = 'medium') # Nombre eje Y

ax.legend(title = 'Especies')

#%% ANÁLISIS DIMENSIONES DEL PICO POR ESPECIE
"""Responder:
 a. ¿Qué especie muestra mayor dispersión en estas variables?
 b. La relación entre estas variables, ¿es similar en las 3 especies?"""

#a) Todas los individuos de una misma especie presentan una gran similitud en las dimensiones de su pico.
    #Entre ellas, la especie que más dispersión presenta es la Adelie
    
#b) Cada especie es bien distinguible una de otra, pues sus picos poseen dimensiones diferentes:
    #Los pingüinos Adelie presentan picos gruesos pero cortos
    #Los pingüinos Chinstrap presentan picos gruesos y a la vez largos
    #Los pingüinos Gentoo presentan picos finos pero largos
    
#%% RELACIÓN LONGITUD PICO - MASA CORPORAL DE ESPECIE ADELIE
"""Realizar un gráfico (de línea) donde se vea la relación entre la variable largo del pico
 y masa corporal, para la especie Adelie. Sugerencia: reordenar el subconjunto de
 pingüinos Adelie por la variable largo del pico, y utilizarlo para graficar."""

adelie_ordenado = adelie.sort_values(by = 'bill_length_mm')

fig, ax = plt.subplots()

#Grafica la regionEste
ax.plot('bill_length_mm', 'body_mass_g', data= adelie_ordenado, 
        marker = '.',        #Tipo de punto (punto, círculo, estrella, etc)
        linestyle = '-',     #Tipo de línea (sólida, punteada, etc)
        linewidth = 0.5     #Ancho de línea
        )


#Agrega título, etiquetas a los ejes y limita el rango de valores de los ejes
ax.set_title('Masa corporal de pingüinos Adelie en función de la longitud de los picos')
ax.set_xlabel('Longitud pico (en milímetros)')
ax.set_ylabel('Masa corporal (en gramos)')

#%% CANTIDAD DE PINGÜINOS POR SEXO Y ESPECIE
""" Realizar un gráfico de barras apiladas para visualizar la cantidad de pingüinos de
 cada sexo dentro de cada especie."""

#Para este gráfico, me creo tablas auxiliares a través de consultas SQL
consultaSQL = """
                SELECT 
                    species,
                    COUNT(*) AS cantidad
                FROM data_ping
                WHERE sex = 'Male'
                GROUP BY species
                ORDER BY species
              """
aux2 = dd.sql(consultaSQL).df()

consultaSQL = """
                SELECT 
                    species,
                    COUNT(*) AS cantidad
                FROM data_ping
                WHERE sex = 'Female'
                GROUP BY species
                ORDER BY species
              """
aux3 = dd.sql(consultaSQL).df()

#Genera el gráfico de barras apiladas de ambas series temporales
fig, ax = plt.subplots()

#Grafica la especie Adelie
ax.bar(aux2['species'], aux2['cantidad'],
       label = 'machos', color = 'blue')

#Grafica la especie Chinstrap
ax.bar(aux3['species'], aux3['cantidad'],
       label = 'hembras', color = 'purple',
       bottom=aux2['cantidad'])


#Agrega título, etiquetas a los ejes y limita el rango de los valores de los ejes
ax.set_title('Poblaciones de hembras y machos por especie de pingüinos')
ax.set_xlabel('Especie')
ax.set_ylabel('Cantidad de individuos')

ax.legend()

#%% VISUALIZACIÓN CON BOXPLOT DEL ANCHO DE PICO SEPARADO POR SEXO
"""Realizar un boxplot de la variable ancho del pico, separado por sexo. ¿Qué se
 observa?"""

ax = sns.boxplot(x = 'sex',
                 y = 'bill_depth_mm',
                 data = data_ping,
                 palette = {'Female' : 'purple', 'Male' : 'blue'})

ax.set_title('Ancho de pico (en milímetros) por sexo')
ax.set_xlabel('Sexo')
ax.set_ylabel('Grosor pico (en milímetros)')

#%% ANÁLISIS BOXPLOT DEL ANCHO DE PICO SEPARADO POR SEXO

#Lo primero que se aprecia es que los machos presentan, en general, un grosor mayor.
#Sin embargo, hay grandes coincidencias entre ambos sexos, son muchas las hembras que poseen igual o mayor grosor de pico que muchos machos.
#Por otra parte, no hay outliers en ninguno de los sexos, es decir, no hay individuos que presenten la característica de forma extrema.

#%% VISUALIZACIÓN CON BOXPLOT DE LA LONGITUD DE ALETAS POR ESPECIE Y SEXO
"""Realizar un boxplot de la variable largo de aleta, separado por especie. ¿Qué se
 observa?"""

ax = sns.boxplot(x = 'species',
                 y = 'flipper_length_mm',
                 hue = 'sex',
                 data = data_ping,
                 palette = {'Female' : 'purple', 'Male' : 'blue'})

ax.set_title('Longitud de aletas (en milímetros) por especie y sexo')
ax.set_xlabel('Especie')
ax.set_ylabel('Longitud aleta (en milímetros)')
ax.legend(title = 'Sexo')

#%% ANÁLISIS BOXPLOT DE LA LONGITUD DE ALETAS SEPARADO POR SEXO Y ESPECIE

#Lo primero que se aprecia es que los machos de cada especie presentan, en general, una longitud de aleta mayor en su respectiva población.
#Sin embargo, no es cierto que todos los pingüinos machos presentan mayor longitud de aletas.
#Es visible que los machos de la especie Adelie tienen longitudes de aletas similares a las hembras de la especie Chinstrap.
#Adicionalmente, las hembras de la especie Gentoo presentan mayor longitud de aletas que practicamente toda la población de machos Adelie y la mayoría de los machos Chinstrap.
#Por otra parte, en la especie Adelie se hayan outliers, es decir que son la especie que mayor distribución presentan en cuanto a la característica analizada.

#%% VISUALIZACIÓN CON VIOLINPLOT DE LA LONGITUD DE ALETAS POR SEXO
"""Realizar un violinplot de la variable largo de aleta, separado por sexo."""

ax = sns.violinplot(x = 'sex',
                    y = 'flipper_length_mm',
                    data = data_ping,
                    palette = {'Female':'purple', 'Male':'blue'}
                    )

ax.set_title('Longitud de aletas (en milímetros) por sexo')
ax.set_xlabel('Sexo')
ax.set_ylabel('Longitud aleta (en milímetros)')
ax.set_xticklabels(['Machos', 'Hembras'])

#%%VISUALIZACIÓN CON VIOLINPLOT DE MASA CORPORAL POR SEXO Y ESPECIE
"""Realizar un violinplot de la variable masa corporal, separado por especie."""

ax = sns.violinplot(x = 'species',
                    y = 'body_mass_g',
                    hue = 'sex',
                    data = data_ping,
                    palette = {'Female':'purple', 'Male':'blue'}
                    )

ax.set_title('Masa corporal (en gramos) por sexo y especie')
ax.set_xlabel('Especie')
ax.set_ylabel('Masa corporal (en gramos)')
ax.legend(title = 'Sexo')
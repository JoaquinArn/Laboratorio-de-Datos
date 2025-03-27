# -*- coding: utf-8 -*-
"""

@author: Joaco
"""

"""Guía de ejercicios de la primera clase 
Estos ejercicios son para trabajar analizando la base de datos sobre árboles en parques y 
plazas en la Ciudad de Buenos Aires y con la de árboles en veredas. 
Primero deben descargar el archivo de árboles en parques, en formato csv desde el 
siguiente link:  Arbolado en espacios verdes."""
import numpy as np
import pandas as pd
import math
#%%
df = pd.read_csv('arbolado-en-espacios-verdes.csv')
filaMuestra = df.sample()
#%% Ejercicio 1
"""1. 
Definir una función leer_parque(nombre_archivo, parque) que abra el 
archivo indicado y devuelva una lista de diccionarios con la información del 
parque especificado. La lista debe tener un diccionario por cada árbol del parque 
elegido. Dicho diccionario debe tener los datos correspondientes a un árbol 
(recordar que cada fila del csv corresponde a un árbol).  
Probar la función en el parque ‘GENERAL PAZ’ y debería dar una lista con 690 
árboles."""
    
def leer_parque(nombre_archivo, parque):
    with open(nombre_archivo, 'rt') as archivo:
        res = []
        df = pd.read_csv(archivo) #creo un dataframe, cuyo índex sea el id del árbol
        #creo un subdataframe cuyo contenido sea la indo de los árboles de ese parque
        arbolesEnEseParque = df[df['espacio_ve'] == parque]
        for fila in arbolesEnEseParque.iterrows():
            #creo el diccionario que contendrá la info de esa fila, la cual corresponde a un arbol
                res.append(fila[1].to_dict())
        return res

parquejemplo = leer_parque('arbolado-en-espacios-verdes.csv', 'GENERAL PAZ')
#%% Ejercicio 2
"""2. Escribir una función especies(lista_arboles) que tome una lista de árboles 
como la generada en el ejercicio anterior y devuelva el conjunto de especies (la 
columna 'nombre_com' del archivo) que figuran en la lista. """
def especies(lista_arboles):
    res = [] #lista con el conjunto de especies
    for i in range(len(lista_arboles)): #recorro la lista
        if lista_arboles[i]['nombre_com'] not in res: #pregunto si la especie ya fue añadida
            res.append(lista_arboles[i]['nombre_com'])
    return res

especiesEjemplo = especies(parquejemplo)
#%% Ejercicio 3
"""3. Escribir una función contar_ejemplares(lista_arboles) que, dada una 
lista como la generada con leer_parque(...), devuelva un diccionario en el 
que las especies sean las claves y tengan como valores asociados la cantidad de 
ejemplares en esa especie en la lista dada. 
Debería verse que en el parque General Paz hay 20 Jacarandás, en el Parque Los 
Andes hay 3 Tilos y en Parque Centenario hay 1 Laurel. """
def contar_ejemplares(lista_arboles):
    res = {}
    for i in range(len(lista_arboles)): #recorro la lista
        if lista_arboles[i]['nombre_com'] not in res: #pregunto si la especie ya fue añadida
            res[lista_arboles[i]['nombre_com']] = 1 #si es que no, la agrego con valor inicial 1
        else:
            res[lista_arboles[i]['nombre_com']] +=1 #de lo contrario, le sumo uno a la cantidad
    return res

parque_general_paz = contar_ejemplares(parquejemplo)
parque_centenario = contar_ejemplares(leer_parque('arbolado-en-espacios-verdes.csv', 'CENTENARIO'))
parque_los_andes = contar_ejemplares(leer_parque('arbolado-en-espacios-verdes.csv', 'ANDES, LOS'))
#%% Ejercicio 4
"""4. Escribir una función obtener_alturas(lista_arboles, especie) que, 
dada una lista como la generada con leer_parque(...) y una especie de 
árbol (un valor de la columna 'nombre_com' del archivo), devuelva una lista con 
las alturas (columna 'altura_tot') de los ejemplares de esa especie en la lista. 
Observación: Conviene devolver las alturas como números (de punto flotante) y 
no como cadenas de caracteres. Sugerimos hacer esto modificando 
leer_parque(...) o modificando el tipo del valor antes de utilizarlo.
Usar la función para calcular la altura promedio y altura máxima de los 
'Jacarandá' en los tres parques mencionados """
def obtener_alturas(lista_arboles, especie):
    res = []
    for i in range (len(lista_arboles)): #recorro la lista
        if (lista_arboles[i]['nombre_com'] == especie): #pregunto si es la especie que busco
            res.append(float(lista_arboles[i]['altura_tot']))
    return res

alturas_jacarandas_general_paz = obtener_alturas(parquejemplo, 'Jacarandá')
altura_max_jacaranda_gp = np.array(alturas_jacarandas_general_paz).max() #para sacar max y la suma de alturas, paso a array la lista
altura_prom_jacaranda_gp = np.array(alturas_jacarandas_general_paz).sum()/parque_general_paz['Jacarandá']

alturas_jacarandas_parque_centenario = obtener_alturas(leer_parque('arbolado-en-espacios-verdes.csv', 'CENTENARIO'), 'Jacarandá')
altura_max_jacaranda_pc = np.array(alturas_jacarandas_parque_centenario).max()
altura_prom_jacaranda_pc = np.array(alturas_jacarandas_parque_centenario).sum()/parque_centenario['Jacarandá']

alturas_jacarandas_parque_los_andes = obtener_alturas(leer_parque('arbolado-en-espacios-verdes.csv', 'ANDES, LOS'), 'Jacarandá')
altura_max_jacaranda_pla = np.array(alturas_jacarandas_parque_los_andes).max()
altura_prom_jacaranda_pc = np.array(alturas_jacarandas_parque_los_andes).sum()/parque_los_andes['Jacarandá']
#%% Ejercicio 5
"""5. Escribir una función obtener_inclinaciones(lista_arboles, especie) 
que,  dada una lista como la generada con leer_parque(...) y una especie 
de árbol, devuelva una lista con las inclinaciones (columna 'inclinacio') de 
los ejemplares de esa especie."""
def obtener_inclinaciones(lista_arboles, especie):
    res = []
    for i in range (len(lista_arboles)):
        if (lista_arboles[i]['nombre_com'] == especie):
            res.append(lista_arboles[i]['inclinacio'])
    return res #misma lógica que ejercicio anterior

inclinaciones_jacaranda_gp = obtener_inclinaciones(parquejemplo, 'Jacarandá')
#%% Ejercicio 6
"""6. Combinando la función especies() con obtener_inclinaciones() escribir 
una función especimen_mas_inclinado(lista_arboles) que, dada una 
lista de árboles devuelva la especie que tiene el ejemplar más inclinado y su 
inclinación. 
Correrlo para los tres parques mencionados anteriormente. Debería obtenerse, 
por ejemplo, que en el Parque Centenario hay un Falso Guayabo inclinado 80 
grados."""
def especimen_mas_inclinado(lista_arboles):
    ejemplarMasInclinado = ' '
    inclinacionMaxima = 0
    lista_especies = especies(lista_arboles)
    for especie in lista_especies:
        #lo que haré será usar la función obtener_inclinaciones, pero pediré que lo pase a array
        infoInclinacionEspecie = np.array(obtener_inclinaciones(lista_arboles, especie))
        max_Inclinacion_De_La_Especie = infoInclinacionEspecie.max() #la razón del array es para usar max()
        if (max_Inclinacion_De_La_Especie > inclinacionMaxima):
            ejemplarMasInclinado = especie #si encuentro una especie que posee un ejemplar mas inclinado, hago los cambios correspondientes
            inclinacionMaxima = max_Inclinacion_De_La_Especie
    return ejemplarMasInclinado, inclinacionMaxima

especimen_mas_inclinado_pc = especimen_mas_inclinado(leer_parque('arbolado-en-espacios-verdes.csv', 'CENTENARIO'))
especimen_mas_inclinado_gp = especimen_mas_inclinado(parquejemplo)
especimen_mas_inclinado_pla = especimen_mas_inclinado(leer_parque('arbolado-en-espacios-verdes.csv', 'ANDES, LOS'))
#%% Ejercicio 7
"""7. Volver a combinar las funciones anteriores para escribir la función 
especie_promedio_mas_inclinada(lista_arboles) que, dada una lista 
de árboles devuelva la especie que en promedio tiene la mayor inclinación y el 
promedio calculado. 
Resultados. Debería obtenerse, por ejemplo, que los Álamos Plateados del 
Parque Los Andes tiene un promedio de inclinación de 25 grados. """

def especie_promedio_mas_inclinada(lista_arboles):
    ejemplar_mayor_promedio = ' '
    inclinacion_promedio_maxima = 0
    lista_especies = especies(lista_arboles)
    for especie in lista_especies:
        infoInclinacionEspecie = np.array(obtener_inclinaciones(lista_arboles, especie))
        #para calcular el promedio, sumo todas las inclinaciones y lo divido por la cantidad de ejemplares
        #lo hago usando las funciones auxiliares que programé
        prom_Inclinacion_De_La_Especie = infoInclinacionEspecie.sum()/contar_ejemplares(lista_arboles)[especie]
        if (prom_Inclinacion_De_La_Especie > inclinacion_promedio_maxima):
            inclinacion_promedio_maxima = prom_Inclinacion_De_La_Especie
            ejemplar_mayor_promedio = especie #si el promedio de la especie es mayor, cambio los valores correspondientes
    return ejemplar_mayor_promedio, inclinacion_promedio_maxima

especie_mas_inclinada = especie_promedio_mas_inclinada(leer_parque('arbolado-en-espacios-verdes.csv', 'ANDES, LOS'))
#%%
"""Vamos a trabajar ahora también con el archivo de árboles en veredas. Queremos 
estudiar si hay diferencias entre los ejemplares de una misma especie según si crecen 
en un un parque o en la vereda. Para eso tendremos que juntar datos de dos bases de 
datos diferentes. 
Explorar el dataset nuevo de árboles en veredas. 
Armar un DataFrame data_arboles_veredas que tenga solamente las siguiente 
columnas: 'nombre_cientifico', 'ancho_acera', 'diametro_altura_pecho', 
'altura_arbol' 
Sugerimos trabajar al menos con las siguientes especies seleccionadas: 
especies_seleccionadas = ['Tilia x moltkei', 'Jacaranda mimosifolia', 'Tipuana tipu']
Proponemos los siguientes pasos para comparar los diámetros a la altura del pecho de 
las tipas en ambos tipos de entornos.""" 
df2 = pd.read_csv('arbolado-publico-lineal-2017-2018.csv')
data_arboles_veredas = df2[['nombre_cientifico', 'ancho_acera', 'diametro_altura_pecho', 'altura_arbol'] ]
#%%Ejercicio 8
"""8. Para cada dataset, armar otro seleccionando solamente las filas correspondientes 
a las tipas (llamalos df_tipas_parques y df_tipas_veredas, respectivamente) y las 
columnas correspondientes al diámetro a la altura del pecho y alturas. Usar como 
copias (usando .copy()) para poder trabajar en estos nuevos dataframes sin 
modificar los dataframes grandes originales. Renombrar las columnas necesarias 
para que se llamen igual en ambos dataframes."""
df_tipas_parques = df[df['nombre_cie'] == 'Tipuana Tipu'][['nombre_cie', 'diametro', 'altura_tot']]
df_tipas_veredas = df2[df2['nombre_cientifico'] == 'Tipuana tipu'][['nombre_cientifico', 'diametro_altura_pecho', 'altura_arbol']]

#el armado de los dataframes fue por medio de filtros basados en el cumplimiento del nombre del arbol
#después, seleccioné las columnas que me interesaban
#Ahora, renombraré las columnas de df_tipas_veredas
df_tipas_veredas = df_tipas_veredas.rename(columns={'nombre_cientifico': 'nombre_cie', 'diametro_altura_pecho': 'diametro', 'altura_arbol': 'altura_tot'}) 
#%%Ejercicio 9
"""9. Agregar a cada dataframe (df_tipas_parques y df_tipas_veredas) una columna 
llamada 'ambiente' que en un caso valga siempre 'parque' y en el otro caso 
'vereda'."""
df_tipas_parque_copia = df_tipas_parques.copy()
df_tipas_veredas_copia = df_tipas_veredas.copy()
df_tipas_parque_copia['ambiente'] = 'parque'
df_tipas_veredas_copia['ambiente'] = 'vereda'
#%% Ejercicio 10
"""10. Concatenar los dataframes. """
df_tipas = pd.concat([df_tipas_parque_copia, df_tipas_veredas_copia])
#%% Ejercicio 11
"""11. Explorar y analizar sobre la cuestión planteada:  
¿Hay diferencias entre los ejemplares de una misma especie según si crecen en 
un parque o en la vereda?"""
#Para analizarlo, quiero conocer cuántas tipas hay en cada ambiente, y el promedio del diametro y altura
cantidad_tipas_vereda = len(df_tipas_veredas_copia)
cantidad_tipas_parques = len(df_tipas_parque_copia)
def promedio (df, clave): #la clave determinará si quiero ver la altura o el diámetro
    acumulado = 0
    for indice, fila in df.iterrows(): #me separo el índice para mejor acceso a los datos que me importan
        if ((clave == 'd') & pd.notna(fila['diametro'])): #me aseguro que no haya nan
            acumulado += fila['diametro']
        elif ((clave == 'a') & pd.notna(fila['altura_tot'])):
            acumulado += fila['altura_tot']
    return acumulado/len(df) #el promedio, pues como se ve arriba, la longitud representa la cantidad de ejemplares

promedio_altura_tipas_veredas = promedio(df_tipas_veredas_copia, 'a')
promedio_altura_tipas_parque = promedio(df_tipas_parque_copia, 'a')
promedio_diametro_tipas_veredas = promedio(df_tipas_veredas_copia, 'd')
promedio_diametro_tipas_parque = promedio(df_tipas_parque_copia, 'd')


"""el análisis que hago al respecto es que en parques las tipas poseen una mejor
capacidad de desarrollo, pues si bien es cierto que en veredas hay casi el doble de
ejemplares, la diferencias de altura y diámetro son lo suficientemente significativas
(4 metros en ambas categorías) para determinar que en parques poseen mejores condiciones"""















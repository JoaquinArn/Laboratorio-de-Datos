# -*- coding: utf-8 -*-
"""
@author: Joaco
"""
import numpy as np
import pandas as pd
import duckdb as dd
#%% 
casos = pd.read_csv("casos.csv")
departamento = pd.read_csv("departamento.csv")
grupoetario = pd.read_csv("grupoetario.csv")
provincia = pd.read_csv("provincia.csv")
tipoevento = pd.read_csv("tipoevento.csv")
#%% Segundo Set Ejercicios - Segundo punto
"""Devolver los casos registrados en la provincia de “Chaco”."""

consultaSQL = """
                SELECT d.*
                FROM departamento AS d
                INNER JOIN provincia AS p
                ON d.id_provincia = p.id
                WHERE p.descripcion = 'Chaco'
              """
dataframeResultado = dd.sql(consultaSQL).df()
#%% Segundo Set Ejercicios - Tercer punto
"""Devolver aquellos casos de la provincia de “Buenos Aires” cuyo campo 
cantidad supere los 10 casos. """

consultaSQL = """
                 SELECT d.*, c.cantidad AS cantCasos
                 FROM departamento AS d
                 INNER JOIN provincia AS p
                 ON d.id_provincia = p.id
                 INNER JOIN casos AS c
                 ON d.id = c.id_depto
                 WHERE p.descripcion = 'Buenos Aires' AND  c.cantidad > 10
              """

dataframeResultado = dd.sql(consultaSQL).df()

#%% Tercer Set Ejercicios - Primer punto
"""Devolver un listado con los nombres de los departamentos que no tienen 
ningún caso asociado."""

consultaSQL = """
                SELECT d.descripcion AS nombre_depto
                FROM departamento AS d
                LEFT OUTER JOIN casos AS c
                ON d.id = c.id_depto
                WHERE c.cantidad IS NULL
              """
# no tengo ningún departamento que no haya presentado al menos un caso
# para corroborarlo, realicé también la siguiente consulta
"""SELECT d.id
FROM departamento AS d
EXCEPT (
    SELECT  id_depto
    FROM casos)"""
dataframeResultado = dd.sql(consultaSQL).df()

#%% Tercer Set Ejercicios - Segundo punto
"""Devolver un listado con los tipos de evento que no tienen ningún caso 
asociado."""

consultaSQL = """
                SELECT e.descripcion
                FROM tipoevento AS e
                LEFT OUTER JOIN casos AS c
                ON e.id = c.id_tipoevento
                WHERE c.id_tipoevento IS NULL
              """
# esta consulta verifica que la consulta de arriba está bien; y que todo departamento presenta al menos un caso
dataframeResultado = dd.sql(consultaSQL).df()
#%% Cuarto Set Ejercicios - Primer punto
"""Calcular la cantidad total de casos que hay en la tabla casos."""

consultaSQL = """
                SELECT SUM(cantidad) AS cantidad_total_casos
                FROM casos
              """
dataframeResultado = dd.sql(consultaSQL).df()        
#%% Cuarto Set Ejercicios - Segundo punto
"""  Calcular la cantidad total de casos que hay en la tabla casos para cada año y 
cada tipo de caso. Presentar la información de la siguiente manera: 
descripción del tipo de caso, año y cantidad. Ordenarlo por tipo de caso 
(ascendente) y  año (ascendente)."""

consultaSQL = """
                SELECT DISTINCT t.descripcion AS descripcion_tipo_caso, c.anio AS anio, SUM(c.cantidad) AS cantidad_total_casos
                FROM casos AS c
                INNER JOIN tipoevento AS t
                ON c.id_tipoevento = t.id
                GROUP BY c.id_tipoevento, t.descripcion, c.anio
                ORDER BY c.id_tipoevento ASC, c.anio ASC
              """
dataframeResultado = dd.sql(consultaSQL).df()        
#%% Cuarto Set Ejercicios - Tercer punto
"""Misma consulta que el ítem anterior, pero sólo para el año 2019."""
    
consultaSQL = """
                SELECT DISTINCT t.descripcion AS descripcion_tipo_caso, c.anio AS anio, SUM(c.cantidad) AS cantidad_total_casos
                FROM casos AS c
                INNER JOIN tipoevento AS t
                ON c.id_tipoevento = t.id
                WHERE c.anio = 2019
                GROUP BY c.id_tipoevento, t.descripcion, c.anio
                ORDER BY c.id_tipoevento ASC, c.anio ASC
              """
dataframeResultado = dd.sql(consultaSQL).df()      
#%% Cuarto Set Ejercicios - Cuarto punto
"""Calcular la cantidad total de departamentos que hay por provincia. Presentar 
la información ordenada por código de provincia. """

consultaSQL = """
                SELECT DISTINCT p.descripcion AS provincia, SUM(d.id_provincia) AS cantidad_departamentos
                FROM provincia AS p
                INNER JOIN departamento AS d
                ON p.id = d.id_provincia
                GROUP BY d.id_provincia, p.descripcion
                ORDER BY d.id_provincia
              """
              
dataframeResultado = dd.sql(consultaSQL).df()                 
#%% Cuarto Set Ejercicios - Quinto punto
"""Listar los departamentos con menos cantidad de casos en el año 2019. """

consultaSQL = """
                SELECT d.descripcion, IFNULL(ANY_VALUE(c.cantidad),0) AS cantidad_casos_depto
                FROM departamento AS d
                LEFT OUTER JOIN casos AS c
                ON d.id = c.id_depto AND c.anio = 2019
                GROUP BY d.descripcion
                ORDER BY cantidad_casos_depto ASC
                """
              
dataframeResultado = dd.sql(consultaSQL).df()   
#%% Cuarto Set Ejercicios - Sexto punto
"""Listar los departamentos con más cantidad de casos en el año 2020. """

consultaSQL = """
                SELECT d.descripcion, IFNULL(ANY_VALUE(c.cantidad),0) AS cantidad_casos_depto
                FROM departamento AS d
                LEFT OUTER JOIN casos AS c
                ON d.id = c.id_depto AND c.anio = 2019
                GROUP BY d.descripcion
                ORDER BY cantidad_casos_depto DESC
              """
              
dataframeResultado = dd.sql(consultaSQL).df()   
#%% Cuarto Set Ejercicios - Séptimo punto
"""Listar el promedio de cantidad de casos por provincia y año. """

consultaSQL = """
                SELECT p.descripcion AS provincia, c.anio AS año, AVG(c.cantidad) AS promedio_casos
                FROM casos AS c
                LEFT OUTER JOIN departamento AS d
                ON d.id = c.id_depto
                LEFT OUTER JOIN provincia AS p
                ON d.id_provincia = p.id
                GROUP BY p.descripcion, c.anio
                ORDER BY c.anio ASC
              """
              
dataframeResultado = dd.sql(consultaSQL).df()   
#%% Cuarto Set Ejercicios - Octavo punto
"""Listar, para cada provincia y año, cuáles fueron los departamentos que más 
cantidad de casos tuvieron."""

consultaSQL = """
                SELECT ANY_VALUE(p.descripcion) AS provincia, d.descripcion AS departamento, c.anio AS año, SUM(c.cantidad) AS cantidad_casos
                FROM casos AS c
                LEFT OUTER JOIN departamento AS d
                ON d.id = c.id_depto
                LEFT OUTER JOIN provincia AS p
                ON d.id_provincia = p.id
                GROUP BY d.descripcion, c.anio
                ORDER BY ANY_VALUE(p.descripcion) ASC, c.anio ASC, cantidad_casos DESC
              """

dataframeResultado = dd.sql(consultaSQL).df()   
#%% Cuarto Set Ejercicios - Octavo punto parte dos
"""Misma consulta que el ítem anterior, pero sólo para aquellos casos en que la 
cantidad total es mayor a 1000 casos. """

consultaSQL = """
                SELECT ANY_VALUE(p.descripcion) AS provincia, d.descripcion AS departamento, ANY_VALUE(c.anio) AS año, SUM(c.cantidad) AS cantidad_casos
                FROM casos AS c
                LEFT OUTER JOIN departamento AS d
                ON d.id = c.id_depto
                LEFT OUTER JOIN provincia AS p
                ON d.id_provincia = p.id
                GROUP BY d.descripcion
                HAVING cantidad_casos > 1000
                ORDER BY ANY_VALUE(c.anio) ASC, cantidad_casos DESC
              """
dataframeResultado = dd.sql(consultaSQL).df()
#%% Cuarto Set Ejercicios - Noveno punto
"""Mostrar la cantidad de casos total, máxima, mínima y promedio que tuvo la 
provincia de Buenos Aires en el año 2019. """

consultaSQL = """
                SELECT COUNT(d.descripcion) AS cant_departamentos, SUM(c.cantidad) AS cant_casos_totales, MAX(c.cantidad) AS max_cant_casos, MIN(c.cantidad) AS min_cant_casos, AVG(c.cantidad) AS prom_cant_casos
                FROM casos AS c
                LEFT OUTER JOIN departamento AS d
                ON d.id = c.id_depto
                LEFT OUTER JOIN provincia AS p
                ON d.id_provincia = p.id AND p.descripcion = 'Buenos Aires'
                WHERE c.anio = 2019 
              """
#las dos primeras columnas solo están para verificar los números
dataframeResultado = dd.sql(consultaSQL).df()   
#%% Cuarto Set Ejercicios - Décimo punto
"""Misma consulta que el ítem anterior, pero sólo para aquellos casos en que la 
cantidad total es mayor a 100 casos. """

consultaSQL = """
                SELECT d.descripcion AS departamento, c.anio AS año, SUM(c.cantidad) AS cantidad_casos,  MAX(c.cantidad) AS max_cant_casos, MIN(c.cantidad) AS min_cant_casos, AVG(c.cantidad) AS prom_cant_casos
                FROM casos AS c
                LEFT OUTER JOIN departamento AS d
                ON d.id = c.id_depto
                LEFT OUTER JOIN provincia AS p
                ON d.id_provincia = p.id
                WHERE p.descripcion = 'Buenos Aires'
                GROUP BY d.descripcion, c.anio
                HAVING cantidad_casos > 100
                ORDER BY c.anio ASC, cantidad_casos DESC
              """

dataframeResultado = dd.sql(consultaSQL).df()   
#%% Cuarto Set Ejercicios - Onceavo punto
"""Listar los nombres de departamento (y nombre de provincia) que tienen 
mediciones tanto para el año 2019 como para el año 2020. Para cada uno de 
ellos devolver la cantidad de casos promedio. Ordenar por nombre de 
provincia (ascendente) y luego por nombre de departamento (ascendente)."""

consultaSQL = """
                SELECT d.descripcion AS departamento, ANY_VALUE(p.descripcion) AS provincia, AVG(c.cantidad) AS promedio_casos
                FROM departamento AS d
                INNER JOIN provincia AS p
                ON d.id_provincia = p.id
                INNER JOIN casos as c
                ON c.id_depto = d.id
                WHERE c.anio IN (2019, 2020)
                GROUP BY d.descripcion
                HAVING COUNT (DISTINCT c.anio) = 2
                ORDER BY ANY_VALUE(p.descripcion) ASC, d.descripcion ASC
              """
              
dataframeResultado = dd.sql(consultaSQL).df()   
#%% Cuarto Set Ejercicios - Doceavo punto
"""Devolver una tabla que tenga los siguientes campos: descripción de tipo de 
evento, id_depto, nombre de departamento, id_provincia, nombre de 
provincia, total de casos 2019, total de casos 2020."""

consultaSQL = """
                SELECT ANY_VALUE(t.descripcion) AS tipo_de_evento, c.id_depto,
                d.descripcion AS nombre_depto, d.id_provincia,
                ANY_VALUE(p.descripcion) AS nombre_de_provinvcia, 
                SUM(CASE WHEN c.anio = 2019 THEN c.cantidad ELSE 0 END) AS cantidad_total_2019,
                SUM(CASE WHEN c.anio = 2020 THEN c.cantidad ELSE 0 END) AS cantidad_total_2020
                FROM casos AS c
                LEFT OUTER JOIN departamento AS d
                ON c.id_depto = d.id
                LEFT OUTER JOIN provincia AS p
                ON d.id_provincia = p.id
                LEFT OUTER JOIN tipoevento AS t
                ON c.id_tipoevento = t.id
                GROUP BY c.id_depto, d.descripcion, d.id_provincia
              """
""""""
dataframeResultado = dd.sql(consultaSQL).df() 
#%% Quinto Set Ejercicios - Primer punto
"""Devolver el departamento que tuvo la mayor cantidad de casos sin hacer uso 
de MAX, ORDER BY ni LIMIT """

consultaSQL = """ 
                SELECT descripcion , cantidad_casos
                FROM  
                (SELECT d.descripcion, SUM(c.cantidad) AS cantidad_casos
                FROM casos AS c
                LEFT OUTER JOIN departamento AS d
                ON c.id_depto = d.id
                GROUP BY d.descripcion) AS subconsulta
                WHERE cantidad_casos > ALL 
                (SELECT SUM(cantidad)
                 FROM casos
                 GROUP BY id_depto)
              """


dataframeResultado = dd.sql(consultaSQL).df()
#%% Octavo Set Ejercicios - Primer Punto
"""Listar las provincias que tienen una cantidad total de casos mayor al 
promedio de casos del país. Hacer el listado agrupado por año. """

consultaSQL = """
                WITH subconsulta AS (
                    SELECT anio, AVG(cantidad) AS promedio_pais
                    FROM casos
                    GROUP BY anio)

                SELECT p.descripcion, c.anio, AVG(IFNULL(c.cantidad,0)) AS promedio_provincia
                FROM casos AS c
                LEFT OUTER JOIN departamento AS d
                ON c.id_depto = d.id
                LEFT OUTER JOIN provincia AS p
                ON d.id_provincia = p.id
                GROUP BY p.descripcion, c.anio
                HAVING AVG(IFNULL(c.cantidad,0)) > (
                    SELECT IFNULL(promedio_pais,0)
                    FROM subconsulta
                    WHERE subconsulta.anio = c.anio)
              """

dataframeResultado = dd.sql(consultaSQL).df()
#%% Octavo Set Ejercicios - Segundo punto
"""Por cada año, listar las provincias que tuvieron una cantidad total de casos 
mayor a la cantidad total de casos que la provincia de Corrientes. """

consultaSQL = """
                WITH subconsulta AS (
                    SELECT c.anio, IFNULL(AVG(c.cantidad), 0) AS promedio_corrientes
                    FROM casos AS c
                    LEFT OUTER JOIN departamento AS d
                    ON c.id_depto = d.id
                    LEFT OUTER JOIN provincia AS p
                    ON d.id_provincia = p.id
                    WHERE c.anio = 2019 OR p.descripcion = 'Corrientes'
                    GROUP BY c.anio)

                SELECT p.descripcion AS provincia, c.anio, IFNULL(AVG(c.cantidad),0) AS promedio_provincia
                FROM casos AS c
                LEFT OUTER JOIN departamento AS d
                ON c.id_depto = d.id
                LEFT OUTER JOIN provincia AS p
                ON d.id_provincia = p.id
                GROUP BY p.descripcion, c.anio
                HAVING IFNULL(AVG(c.cantidad),0) > (
                    SELECT IFNULL(promedio_corrientes,0)
                    FROM subconsulta
                    WHERE subconsulta.anio = c.anio)
              """

dataframeResultado = dd.sql(consultaSQL).df()

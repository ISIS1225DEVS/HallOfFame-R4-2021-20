"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def init():
    analyzer = model.newAnalyzer()
    return analyzer

# Funciones para la carga de datos

def loadServices(analyzer, airportsfile, routesfile, citiesfile):
    c = 0
    airportsfile = cf.data_dir + airportsfile
    input_airportsfile = csv.DictReader(open(airportsfile, encoding="utf-8"),
                                delimiter=",")
    for airport in input_airportsfile:
        model.addAirport(analyzer, airport)
        model.addLatitud(analyzer, airport)
        model.addVertex(analyzer, airport)
        model.addVertexDobles(analyzer, airport)

    routesfile = cf.data_dir + routesfile
    input_routesfile = csv.DictReader(open(routesfile, encoding="utf-8"),
                                delimiter=",")
    for route in input_routesfile:
        c += 1
        model.addConnections(analyzer, route)

    citiesfile = cf.data_dir + citiesfile
    input_citiesfile = csv.DictReader(open(citiesfile, encoding="utf-8"),
                                delimiter=",")
    for city in input_citiesfile:
        model.addCiudad(analyzer, city)
        model.addidCiudad(analyzer, city)

    model.addRutasDobles(analyzer)

    return analyzer,c

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def totalAirports(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return model.totalAirports(analyzer)

def totalAirports2(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return model.totalAirports2(analyzer)

def totalRoutesUnicas(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return model.totalRoutesUnicas(analyzer)

def totalRoutesDobles(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return model.totalRoutesDobles(analyzer)

def totalCities(analyzer):
    """
    Retorna el total de ciudades
    """
    return model.totalCities(analyzer)

def infoPrimerAeropuerto(analyzer):
    return model.infoPrimerAeropuerto(analyzer)

def infoUltimoAeropuerto(analyzer):
    return model.infoUltimoAeropuerto(analyzer)

def infoPrimeraCiudad(analyzer):
    return model.infoPrimeraCiudad(analyzer)

def infoUltimaCiudad(analyzer):
    return model.infoUltimaCiudad(analyzer)

#Requerimientos

def req_1(analyzer):
    num, lista = model.req_1(analyzer)
    return num, lista

def req_2(analyzer, a1, a2):
    num, mismo = model.req_2(analyzer, a1, a2)
    return num, mismo

def ciudades_homonimas(analyzer, ciudad):
    lista_ciudades = model.ciudades_homonimas(analyzer, ciudad)
    return lista_ciudades

def req_3(analyzer, ciudad_or, ciudad_des, a, b):
    (origen, destino, camino_minimo, distancia_tot) = model.req_3(analyzer, ciudad_or, ciudad_des, a, b)
    return (origen, destino, camino_minimo, distancia_tot)

def req_4(analyzer, iata, millas):
    (distancia_max, lista_ruta, distancia_tot, alcanza, dif_millas, distancia_km, num_aeropuertos) = model.req_4(analyzer, iata, millas)
    return (distancia_max, lista_ruta, distancia_tot, alcanza, dif_millas, distancia_km, num_aeropuertos)

def req_5(analyzer, aer):
    (analyzer, num_afectados, lista) = model.req_5(analyzer, aer)
    return (analyzer, num_afectados, lista)

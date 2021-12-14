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

from App.model import Kosajaru
import config as cf
import model
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def initAnalyzer():
    """
    Llama la funcion de inicializacion del modelo
    """
    analyzer = model.newAnalyzer()
    return analyzer

# Funciones para la carga de datos

def loadData(analyzer):
    """
    Carga los datos desde los archivos csv
    """
    # Carga de todos los datos
    loadInfo(analyzer)
    # Inicializa Kosajaru
    Kosajaru(analyzer)
    # Inicializa PrimMST
    PrimMST(analyzer)

def loadInfo(analyzer):
    """
    Airports File
    """
    airportfile = cf.data_dir + "airports-utf8-5pct.csv"
    input_file = csv.DictReader(open(airportfile, encoding="utf-8"),
                                delimiter=",")
    for airport in input_file:
        model.addAirport(analyzer, airport)
        model.addVertex(analyzer, airport)
    """
    Routes file
    """
    routesfile = cf.data_dir + "routes-utf8-5pct.csv"
    routes_file = csv.DictReader(open(routesfile, encoding="utf-8"),
                                delimiter=",")
    for routes in routes_file:
        departure = routes['Departure']
        destination = routes['Destination']
        distance = float(routes['distance_km'])
        model.AddConnections(analyzer, departure, destination, distance) 
    """
    Cities file
    """
    worldcitiesfile = cf.data_dir + "worldcities-utf8.csv"
    city_file = csv.DictReader(open(worldcitiesfile, encoding="utf-8"),
                                delimiter=",")
    for city in city_file:
        model.addCity(analyzer, city)

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def getLast(lista, num):
    """
    Retorna los ultimos 'num' elementos de una lista.
    """
    return model.getLast(lista, num)

def getFirst(lista, num):
    """
    Retorna los primeros 'num' elementos de una lista.
    """
    return model.getFirst(lista, num)

def FirtsAndLast(primeros, ultimos):
    return model.FirtsAndLast(primeros, ultimos)

def SearchbyIATA(analyzer, iata):
    """
    Buscar aeropuerto por IATA
    """
    return model.SearchbyIATA(analyzer, iata)

def totalAirperGraph(analyzer):
    """
    Total de paradas de autobus
    """
    return model.totalAirperGraph(analyzer)

def totalConnectionsperGraph(analyzer):
    """
    Total de enlaces entre las paradas
    """
    return model.totalConnectionsperGraph(analyzer)

def getFistAirportperGraph(analyzer):
    """
    Primera parada del grafo
    """
    return model.getFistAirportperGraph(analyzer)

def CitySize(analyzer):
    """
    Numero de ciudades
    """
    return model.CitySize(analyzer)

def Kosaraju(analyzer):
    """
    Kosaraju
    """
    return model.Kosaraju(analyzer)

def PrimMST(analyzer):
    """
    PrimMST
    """
    return model.PrimMST(analyzer)

def getDistance(departure, airport):
    return model.getDistance(departure, airport)

def getNearestAirport(analyzer ,city):
    return model.getNearestAirport(analyzer ,city)

def getDistancePath(analyzer, destination):
    return model.getDistancePath(analyzer, destination)


#Requerimientos

def AirInterconection (analyzer):
    """
    Req 1
    """
    return model.AirInterconection(analyzer)

def AirCluster(analyzer,vertexA, vertexB):
    """
    Req 2
    Numero de componentes fuertemente conectados
    """
    return model.AirCluster(analyzer,  vertexA, vertexB)

def SearchCity(analyzer, city):
    """
    Req 3
    """
    return model.SearchCity(analyzer, city)

def getPath(analyzer, departure, destination):
    """
    Req 3
    """
    return model.getPath(analyzer, departure, destination)

def getStops(analyzer, path):
    """
    Req 3
    """
    return model.getStops(analyzer, path)

def TravelerMiles(analyzer, millas, airport):
    """
    Req 4
    """
    return model.TravelerMiles(analyzer, millas, airport)

def OutOfService(analyzer, airIata):
    """
    Req 5
    """
    return model.OutOfService(analyzer, airIata)

def Req6(departure, arrival, city1, city2):
    """
    Req 6
    """
    return model.Req6(departure, arrival, city1, city2)

def Mapa(info):
    """
    Req 7
    """
    return model.Mapa(info)
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

def create_catalog():
    return model.create_catalog()

# Funciones para la carga de datos

def loadData(catalog):
    loadTables(catalog)
    loadGraphs(catalog)
    loadCities(catalog)
    loadMST(catalog)
    loadSCC(catalog)

def loadTables(catalog):
    file = cf.data_dir + "Skylines/airports-utf8-small.csv"
    airports = csv.DictReader(open(file, encoding="utf-8"), delimiter=",")

    for airport in airports:
        model.add_airport(catalog, airport)


def loadGraphs(catalog):
    file = cf.data_dir + "Skylines/routes-utf8-small.csv"
    routes = csv.DictReader(open(file, encoding="utf-8"), delimiter=",")

    for route in routes:
        model.add_route(catalog, route)


def loadCities(catalog):
    file = cf.data_dir + "Skylines/worldcities-utf8.csv"
    cities = csv.DictReader(open(file, encoding="utf-8"), delimiter=",")

    for city in cities:
        model.add_city(catalog, city)

def loadMST(catalog):
    model.loadMST(catalog)

def loadSCC(catalog):
    model.loadSCC(catalog)

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def getLoadingData(catalog):
    return model.getLoadingData(catalog)

def create_client(key, secretK):
    return model.create_client(key, secretK)

def getMostInterconnections(catalog):
    return model.getMostInterconnections(catalog)

def getFlightTrafficClusters(catalog, IATA1, IATA2):
    return model.getFlightTrafficClusters(catalog, IATA1, IATA2)

def getShortestRoute(catalog, city1, city2):
    return model.getShortestRoute(catalog,city1,city2)

def getFlyerMiles(catalog,city,miles):
    return model.getUseFlyerMiles(catalog,city,miles)

def getCalculateClosedAirportEffect(catalog, air):
    return model.getCalculateClosedAirportEffect(catalog, air)

def getShortestRouteAPI(catalog, origen, destino, cliente):
    return model.getShortestRouteAPI(catalog, origen, destino, cliente)

def checkCity(catalog, city):
    return model.checkCity(catalog, city)

def makeMapReq1(data,catalog):
    model.makeMapReq1(data,catalog)

def makeMapReq2(catalog, kscc, connected, IATA1, IATA2):
    model.makeMapReq2(catalog, kscc, connected, IATA1, IATA2)

def makeMapReq3(catalog, city1,city2, min_disto, min_distd, airOrigin, airDest, routePath):
    model.makeMapReq3(catalog, city1,city2, min_disto, min_distd, airOrigin, airDest, routePath)

def makeMapReq4(catalog, data):
    model.makeMapReq4(catalog,data)

def makeMapReq5(data, airC, catalog):
    model.makeMapReq5(data, airC, catalog)

def makeGraphs(catalog):
    model.makeDGraph(catalog)
    model.makeNDGraph(catalog)

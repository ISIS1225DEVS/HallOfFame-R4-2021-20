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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """





#import requests
from DISClib.DataStructures.arraylist import addLast
import config
from DISClib.ADT.graph import gr, vertices
from DISClib.ADT import map as m
from DISClib.ADT import graph as gra
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import prim as prim
from DISClib.Algorithms.Graphs import dfs as dfs
from DISClib.Utils import error as error
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.ADT import orderedmap as om
from math import radians, cos, sin, asin, sqrt
assert config


"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newAnalyzer():
    """ Inicializa el analizador


   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {
                    'AirportIATAS': None,
                    'AirportRoutesD': None,
                    'AirportRoutesND': None,
                    'CitiesMapInfo': None,
                    'Cities_lst':None,
                    'AirpotsInterconnected':None,
                    'AirpotsInterconnectedND':None,
                    'Cities-ID': None,
                    'Cities-Airport':None
                    }
        analyzer['AirportIATAS'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareAirportIATA) #Relaciona el código IATA de un aeropuerto con su información

        analyzer['airport_lst'] = lt.newList('ARRAY_LIST')

        analyzer['AirportRoutesD'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareAirportIATA)

        analyzer['AirportRoutesND'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=14000,
                                              comparefunction=compareAirportIATA) #tiene unicamente interconexiones entre aeropuertos con vuelos de ida y regreso
        analyzer['Cities_lst'] = lt.newList('ARRAY_LIST') #contiene todas las ciudades

        analyzer['CitiesMapInfo'] = m.newMap(numelements=42000,
                                     maptype='PROBING',
                                     comparefunction=compareAirportIATA) #Relaciona el id de una ciudad con su información


        analyzer['Cities-Airport'] = m.newMap(numelements=42000,
                                     maptype='PROBING',
                                     comparefunction=compareAirportIATA)#Relaciona una ciudad con el codigo IATA del aeropuerto más cercano a ella

        
        analyzer["AirpotsInterconnected"] = lt.newList('ARRAY_LIST', cmpfunction= compareinterconections)
        analyzer["AirpotsInterconnectedND"] = lt.newList('ARRAY_LIST', cmpfunction= compareinterconections)

        analyzer['Cities-ID'] = m.newMap(numelements=42000,
                                     maptype='PROBING',
                                     comparefunction=compareCityName) #Relaciona nombres de ciudades con su numero id


        return analyzer
        
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al catalogo

def addAirportVertex(analyzer, airport):

    airport1 = formatVertex(airport)

    lt.addLast(analyzer['airport_lst'], airport)

    map = analyzer['AirportIATAS']

    entry = m.get(map, airport['IATA'])

    if entry is None:
        m.put(map, airport['IATA'], airport)

    if not gr.containsVertex(analyzer['AirportRoutesD'], airport1):
        gr.insertVertex(analyzer['AirportRoutesD'], airport1)


    return analyzer


def addAirportConnection(analyzer, route):
    """
    Adiciona las estaciones al grafo como vertices y arcos entre las
    estaciones adyacentes.

    Los vertices tienen por nombre el identificador de la estacion
    seguido de la ruta que sirve.  Por ejemplo:

    75009-10

    Si la estacion sirve otra ruta, se tiene: 75009-101
    """
    origin = route['Departure']
    destination = route['Destination']

    cleanDistance(route['distance_km'])
    distance = float(route['distance_km'])
    distance = abs(distance)
    addConnection(analyzer['AirportRoutesD'], origin, destination, distance)
    addAirportNDConnection(analyzer,origin,destination,distance)

def addAirportNDConnection(analyzer,origin,destination,distance): 

    arco_origin = gr.getEdge(analyzer['AirportRoutesD'],origin,destination)
    arco_destination = gr.getEdge(analyzer['AirportRoutesD'],destination,origin)

    if arco_origin != None and arco_destination != None:

        if not gr.containsVertex(analyzer['AirportRoutesND'], origin):
            gr.insertVertex(analyzer['AirportRoutesND'], origin)

        if not gr.containsVertex(analyzer['AirportRoutesND'], destination):
            gr.insertVertex(analyzer['AirportRoutesND'], destination)

        addConnection(analyzer['AirportRoutesND'], origin, destination, distance)

    
    return analyzer

def addCity(analyzer, city):

    city_map = analyzer['CitiesMapInfo']
    city_id_map = analyzer['Cities-ID']

    entry = m.get(city_map,city['id'])

    if entry == None:

        m.put(city_map, city['id'], city)

    lt.addLast(analyzer['Cities_lst'], city)

    citynamentry = m.get(city_id_map,city['city'])

    if citynamentry == None:

        value = newCity()
        m.put(city_id_map, city['city'], value)

    else: 

        value = me.getValue(citynamentry)

    lt.addLast(value['ID'], city)
    
    return analyzer

def newCity():

    city = {'ID':lt.newList('ARRAY_LIST', cmpID)}   

    return city

def addCityAirport(analyzer, city):
    city_airport_map = analyzer['Cities-Airport']

    entry = m.get(city_airport_map,city['city'])

    if entry == None:
        value = newcityAirport(analyzer, city)
        m.put(city_airport_map, city['id'], value)
    
    return analyzer

def newcityAirport(analyzer, city):
    lat1 = float(city['lat'])
    lon1 = float(city['lng'])
    menor = 100000000000000
    menor_airport = None

    for airport in lt.iterator(analyzer['airport_lst']):
        lat2 = float(airport['Latitude'])
        lon2 = float(airport['Longitude'])

        distance_city = harvesineDistance(lat1,lat2,lon1,lon2)

        if distance_city < menor:

            menor = distance_city
            menor_airport = airport['IATA']

    city_airport = {'City': city['city'], 'AirportClosest': menor_airport, 'DistanceClosest': menor}

    return city_airport

def addConnection(graph, origin, destination, distance):

    ' Adiciona un arco entre dos aeropuertos'

    arco = gr.getEdge(graph,origin, destination)

    if arco is None:

        gr.addEdge(graph,origin, destination, distance)

    return graph

def addInterconnections(analyzer):
    graph = analyzer['AirportRoutesD']
    vertex_list = gr.vertices(graph) 
    #info_list = analyzer["AirpotsInterconnected"]

    for vertex in lt.iterator(vertex_list):
        info = relateIATA(analyzer, vertex)
        arocos_llegada = gr.indegree(graph, vertex)
        arcos_salida = gr.outdegree(graph, vertex)
        total_arcos = arocos_llegada + arcos_salida
        datos = {"Aeropueto": info["Name"],
                "IATA": vertex, 
                "Ciudad": info["City"],
                "Pais": info["Country"],
                "TotalConnections": total_arcos,
                }
        lt.addLast(analyzer["AirpotsInterconnected"], datos)

    sortInterconnected(analyzer["AirpotsInterconnected"])
    

def addInterconnectionsND(analyzer):
    graphND = analyzer['AirportRoutesND']
    vertex_listND = gr.vertices(graphND) 
    #info_listND = ["AirpotsInterconnectedND"]

    for vertex in lt.iterator(vertex_listND):
        info = relateIATA(analyzer, vertex)
        total_arcosND = gr.degree(graphND,vertex)
        datos = {"Aeropueto": info["Name"],
                "IATA": vertex, 
                "Ciudad": info["City"],
                "Pais": info["Country"],
                "TotalConnections": total_arcosND,
                }
        lt.addLast(analyzer["AirpotsInterconnectedND"], datos)

    sortInterconnected(analyzer["AirpotsInterconnectedND"])

def relateIATA(analyzer, vertex):
    mapa = analyzer['AirportIATAS']
    pareja = m.get(mapa, vertex)
    info = me.getValue(pareja)

    return info
    


# Funciones para creacion de datos

def cleanDistance(distance):
    """
    En caso de que el archivo tenga un espacio en la
    distancia, se reemplaza con cero.
    """
    if distance == '':
        distance = 0


def formatVertex(service):
    """
    Se formatea el nombrer del vertice con el id de la estación
    seguido de la ruta.
    """
    name = service['IATA']
    return name

def harvesineDistance(lat1, lat2, lon1, lon2):

    R = 6371 #radio de la tierra en km

    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2*asin(sqrt(a))

    return c * R



# Funciones de consulta



def getInterconnections(analyzer):
    
    info_list = analyzer['AirpotsInterconnected']
    info_listND = analyzer['AirpotsInterconnectedND']
    
    return info_list, info_listND
    

def getCities(analyzer, name):

    entry = m.get(analyzer['Cities-ID'], name)
    value = me.getValue(entry)

    return value['ID']

def getcluster(analyzer):

    cluster = scc.KosarajuSCC(analyzer['AirportRoutesD'])

    return cluster

def getClusterNum(cluster):

    cluster_num = scc.connectedComponents(cluster)

    return cluster_num

def getTraficClustersCon(cluster, IATA1,IATA2):

    airports_connected = scc.stronglyConnected(cluster, IATA1, IATA2)

    return airports_connected


def planViajero(analyzer, origen, distancia): 

    lista_nodos = lt.newList('ARRAY_LIST')
    posibles_caminos = lt.newList('ARRAY_LIST')#####
    largestBranch = lt.newList('ARRAY_LIST')

    graphND = analyzer['AirportRoutesND']
    mst = prim.PrimMST(graphND)
    tree = mst["mst"]    
    
    weight = prim.weightMST(graphND, mst)

    ruta = dfs.DepthFirstSearch(graphND, origen)
    for i in lt.iterator(tree):
        nodo = i['vertexA']
        nodo2 = i['vertexB']
        
        #lista de nodos
        exist = lt.isPresent(lista_nodos,nodo) 
        exist2 = lt.isPresent(lista_nodos,nodo2) 
        if (exist == 0):
            lt.addLast(lista_nodos, nodo)
        if (exist2 == 0):
            lt.addLast(lista_nodos, nodo2)
        
        #encontrar camino
        path = dfs.pathTo(ruta, nodo)
        path2 = dfs.pathTo(ruta, nodo2)
        if path and path2:
            posibles_caminos = lt.newList('ARRAY_LIST')
            lt.addLast(posibles_caminos,path)
            lt.addLast(posibles_caminos,path2)
        
        for i in lt.iterator(posibles_caminos):
            union_caminos = lt.newList('ARRAY_LIST')
            #print(i)
            for iata in lt.iterator(i):
                #hacer pareja
                posicion = (lt.isPresent(i, iata))+1
                if posicion <= lt.size(i):
                    elemento = lt.getElement(i,posicion)
                    pareja_iata = (iata, elemento)
                    lt.addLast(union_caminos,pareja_iata)
            for m in (union_caminos["elements"]):
                exist = lt.isPresent(largestBranch,m) 
                if (exist == 0):
                    lt.addLast(largestBranch, m)

    #distancia total
    lista_pesos = lt.newList('ARRAY_LIST')
    total_pesos = 0
    for element in lt.iterator(largestBranch):
        edge = gra.getEdge(graphND, element[0], element[1])
        peso = edge['weight']
        lt.addLast(lista_pesos,peso)
    for peso in lt.iterator(lista_pesos):
        total_pesos = total_pesos + peso
    
    distancia_total = total_pesos*2
    #print(distancia_total)
    
    nodesConnected = lt.size(lista_nodos)
    largestBranch = largestBranch["elements"]
    milles = ((distancia * 1.6) - distancia_total)/1.6

    return nodesConnected, weight, largestBranch, milles, distancia_total


def ClosestairportCity(analyzer,city_id):

    city_closest_map = analyzer['Cities-Airport']
    airportentry = m.get(city_closest_map,city_id)
    airportvalue = me.getValue(airportentry)
    airportIATA = airportvalue['AirportClosest']

    return airportIATA


def DijkstraAirport(analyzer, airport):

    shortest_routes = djk.Dijkstra(analyzer['AirportRoutesD'], airport)

    return shortest_routes


def getShortestRoute(dijkstra, airport2):


    if djk.hasPathTo(dijkstra,airport2):

        dijk_route = djk.pathTo(dijkstra,airport2)

        dist_total = djk.distTo(dijkstra, airport2)

        return dijk_route,dist_total


def getAffectedAirports(analyzer, IATA):

    adj = gr.adjacents(analyzer['AirportRoutesD'],IATA)
    size = lt.size(adj)

    return  adj, size

def Req6City(citycode, analyzer):

    entryinfo = m.get(analyzer['CitiesMapInfo'], citycode)

    value = me.getValue(entryinfo)

    lat = value['lat']
    lon = value['lng']

    return lat, lon


# Funciones utilizadas para comparar elementos dentro de una lista
def compareAirport():
     pass

def compareCityName(name, key):

    namekey = key['key']
    if (name == namekey):
        return 0
    elif (name > namekey):
        return 1
    else:
        return -1

def compareAirportIATA(IATA, keyvalue):
    """
    Compara dos aeropuertos
    """
    IATAcode = keyvalue['key']
    if (IATA == IATAcode):
        return 0
    elif (IATA > IATAcode):
        return 1
    else:
        return -1

def compareroutes(route1, route2):
    """
    Compara dos rutas
    """
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1

def cmpID(ID1, ID2):

    if (ID1 == ID2):
        return 0
    else:
        return -1

def compareinterconections(dict1, dict2):
    if (dict1["Aeropuerto"] == dict2["Aeropuerto"]):
        return 0
    elif (dict1["Aeropuerto"] > dict2["Aeropuerto"]):
        return 1
    else:
        return -1

def cmpconnections(con1,con2):

    return con1['TotalConnections'] > con2['TotalConnections']


# Funciones de ordenamiento

def sortInterconnected(interconnected):

    ms.sort(interconnected, cmpconnections)

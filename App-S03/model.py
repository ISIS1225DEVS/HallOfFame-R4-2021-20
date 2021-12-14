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


from DISClib.ADT.queue import size
from DISClib.DataStructures.chaininghashtable import keySet
import config
from DISClib.ADT.graph import getEdge, gr
from DISClib.ADT import map as mp
from DISClib.ADT import list as lt
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import prim
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import dijsktra as djk

from DISClib.Utils import error as error
assert config
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from math import sin, cos, acos, radians


"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newAnalyzer():
    analyzer = {"ciudades":None,
                "aeropuertos":None,
                "rutas_dobles":None,
                "rutas_unicas":None,
                "paths":None
                }
    analyzer["ciudades"] = mp.newMap(numelements=41001,
                                    maptype='PROBING',
                                    comparefunction=None)
    analyzer["id_ciudades"] = mp.newMap(numelements=41001,
                                        maptype='PROBING',
                                        comparefunction=None)
    analyzer["aeropuertos"] = mp.newMap(numelements=9100,
                                        maptype="PROBING",
                                        comparefunction=None)
    analyzer["latitudes"] = mp.newMap(numelements=9100,
                                        maptype="PROBING",
                                        comparefunction=None)
    analyzer["rutas_unicas"] = gr.newGraph(datastructure="ADJ_LIST",
                                            directed=True,
                                            size=9100,
                                            comparefunction=None)
    analyzer["rutas_dobles"] = gr.newGraph(datastructure="ADJ_LIST",
                                            directed=False,
                                            size=9100,
                                            comparefunction=None)                                            
    return analyzer

# Funciones para agregar informacion al catalogo
def addAirport (analyzer, airport):
    cod_aeropuerto = airport["IATA"]
    entry = mp.get(analyzer["aeropuertos"], cod_aeropuerto )
    if entry is None:
        datentry = newDataEntry(airport)
        mp.put(analyzer["aeropuertos"], cod_aeropuerto, datentry)
    else:
        datentry = me.getValue(entry)
    airport["num_routes"] = 0
    add(datentry, airport)
    return analyzer

def addLatitud (analyzer, airport):
    latitud = airport["Latitude"]
    entry = mp.get(analyzer["latitudes"], latitud )
    if entry is None:
        datentry = newDataEntry(airport)
        mp.put(analyzer["latitudes"], latitud, datentry)
    else:
        datentry = me.getValue(entry)
    add(datentry, airport)
    return analyzer

def addCiudad(analyzer, city):
    ciudad = city["city"]
    entry = mp.get(analyzer["ciudades"], ciudad)
    if entry is None:
        datentry = newDataEntry(city)
        mp.put(analyzer["ciudades"], ciudad, datentry)
    else:
        datentry = me.getValue(entry)
    add(datentry, city)
    return analyzer

def addidCiudad(analyzer, city):
    ciudad = city["id"]
    entry = mp.get(analyzer["id_ciudades"], ciudad)
    if entry is None:
        datentry = newDataEntry(city)
        mp.put(analyzer["id_ciudades"], ciudad, datentry)
    else:
        datentry = me.getValue(entry)
    add(datentry, city)
    return analyzer

def addConnections (analyzer, route):
    origen = route["Departure"]
    destino = route["Destination"]
    distancia = route["distance_km"]
    addConnection(analyzer, origen, destino, distancia)
    addRoute(analyzer, origen, destino)

def addVertex(analyzer, aeropuerto):
    if not gr.containsVertex(analyzer['rutas_unicas'], aeropuerto["IATA"]):
            gr.insertVertex(analyzer['rutas_unicas'], aeropuerto["IATA"])
    return analyzer

def addVertexDobles(analyzer, aeropuerto):
    if not gr.containsVertex(analyzer['rutas_dobles'], aeropuerto["IATA"]):
        gr.insertVertex(analyzer['rutas_dobles'], aeropuerto["IATA"])

def addConnection(analyzer, origin, destination, distance):
    edge = gr.getEdge(analyzer['rutas_unicas'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['rutas_unicas'], origin, destination, float(distance))
    return analyzer

def addRoute(analyzer, origen, destino):
    mp.get(analyzer["aeropuertos"], origen)["value"]["elements"][0]["num_routes"] += 1
    mp.get(analyzer["aeropuertos"], destino)["value"]["elements"][0]["num_routes"] += 1
    return analyzer

def addRutasDobles(analyzer):
    vertices_tot = gr.vertices(analyzer['rutas_unicas'])
    for va in lt.iterator(vertices_tot):
        adjacentes = gr.adjacents(analyzer['rutas_unicas'], va)
        for vb in lt.iterator(adjacentes):
            arcos = gr.adjacentEdges(analyzer['rutas_unicas'], vb)
            for a in lt.iterator(arcos):
                if a['vertexB'] == va:
                    arco = gr.getEdge(analyzer['rutas_dobles'], va, vb)
                    if arco is None:
                        gr.addEdge(analyzer['rutas_dobles'], va, vb, float(a['weight']))
            
def add(datentry, entry):
    lt.addLast(datentry, entry)
    return datentry

def newDataEntry(entry):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry=lt.newList(datastructure="ARRAY_LIST")
    return entry

# Funciones para creacion de datos

# Funciones de consulta


def totalAirports(analyzer):
    """
    Retorna el total de aeropuertos
    """
    return gr.numVertices(analyzer["rutas_unicas"])

def totalAirports2(analyzer):
    """
    Retorna el total de aeropuertos
    """
    return gr.numVertices(analyzer["rutas_dobles"])

def totalRoutesUnicas(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['rutas_unicas'])
    
def totalRoutesDobles(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['rutas_dobles'])

def totalCities(analyzer):
    """
    Retorna el total de ciudades
    """
    return mp.size(analyzer["id_ciudades"])

def infoPrimerAeropuerto(analyzer):
    aeropuerto = lt.getElement(mp.keySet(analyzer["aeropuertos"]), 1)
    return mp.get(analyzer["aeropuertos"], aeropuerto)["value"]["elements"][0]

def infoUltimoAeropuerto(analyzer):
    aeropuerto = lt.getElement(mp.keySet(analyzer["aeropuertos"]), lt.size(mp.keySet(analyzer["aeropuertos"])))
    return mp.get(analyzer["aeropuertos"], aeropuerto)["value"]["elements"][0]

def infoPrimeraCiudad(analyzer):
    ciudad = lt.getElement(mp.keySet(analyzer["ciudades"]), 1)
    return mp.get(analyzer["ciudades"], ciudad)["value"]["elements"][0]

def infoUltimaCiudad(analyzer):
    ciudad = lt.getElement(mp.keySet(analyzer["ciudades"]), lt.size(mp.keySet(analyzer["ciudades"])))
    return mp.get(analyzer["ciudades"], ciudad)["value"]["elements"][0]

def semiverseno(lat1, lat2, lng1, lng2):
    punto_1 = (radians(float(lat1)), radians(float(lng1)))
    punto_2 = (radians(float(lat2)), radians(float(lng2)))
    distancia = acos(sin(punto_1[0])*sin(punto_2[0]) + cos(punto_1[0])*cos(punto_2[0])*cos(punto_1[1]-punto_2[1]))
    return distancia * 6371.01

def minimumCostPaths(analyzer, initialStation):
    """
    Calcula los caminos de costo mínimo desde la estacion initialStation
    a todos los demas vertices del grafo
    """
    analyzer['paths'] = djk.Dijkstra(analyzer['rutas_unicas'], initialStation)
    return analyzer

def minimumCostPath(analyzer, destStation):
    """
    Retorna el camino de costo minimo entre la estacion de inicio
    y la estacion destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    path = djk.pathTo(analyzer['paths'], destStation)
    return path

def f_primeros_ultimos(lista, n):
    c = 0
    len = lt.size(lista)
    lista_def = lt.newList(datastructure="ARRAYLIST")
    for e in lt.iterator(lista):
        lt.addLast(lista_def, e)
        c += 1
        if c == n:
            c -= 1
            break
    while c >= 0:
        e = lt.getElement(lista, len-c)
        lt.addLast(lista_def, e)
        c -= 1
    return lista_def
# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

def compareNumRutas (aer1, aer2):
    if aer1["num_routes"] > aer2["num_routes"]:
        return True
    else:
        return False
#Requerimientos

def req_1(analyzer):
    rutas = analyzer["rutas_unicas"]
    aeropuertos = analyzer["aeropuertos"]
    lista = lt.newList(datastructure="ARRAY_LIST")
    for v in lt.iterator(gr.vertices(rutas)):
        if gr.degree(rutas, v) >= 1 or gr.indegree(rutas, v) >= 1:
            lt.addLast(lista, mp.get(aeropuertos, v)["value"]["elements"][0])
    lista = sa.sort(lista, compareNumRutas)
    return lt.size(lista), lista

def req_2(analyzer, a1, a2):
    rutas = analyzer["rutas_unicas"]
    clusters = scc.KosarajuSCC(rutas)
    num = scc.connectedComponents(clusters)
    mismo = scc.stronglyConnected(clusters, a1, a2)
    return num, mismo

def ciudades_homonimas(analyzer, ciudad):
    lista_ciudades = mp.get(analyzer["ciudades"], ciudad)["value"]
    return lista_ciudades

def req_3(analyzer, ciudad_or, ciudad_des, a, b):
    centinela=True
    centinela1=True
    lat_ciu_or = mp.get(analyzer["ciudades"], ciudad_or)["value"]["elements"][int(a)-1]["lat"]
    lat_ciu_des = mp.get(analyzer["ciudades"], ciudad_des)["value"]["elements"][int(b)-1]["lat"]
    lng_ciu_or = mp.get(analyzer["ciudades"], ciudad_or)["value"]["elements"][int(a)-1]["lng"]
    lng_ciu_des = mp.get(analyzer["ciudades"], ciudad_des)["value"]["elements"][int(b)-1]["lng"]
    i=1
    lista_aeropuertos_or = lt.newList(datastructure="ARRAY_LIST")
    lista_aeropuertos_des = lt.newList(datastructure="ARRAY_LIST")
    latitudes = mp.keySet(analyzer["latitudes"])
    while centinela or centinela1:
        for lat in lt.iterator(latitudes):
            if (float(lat_ciu_or)-(0.1*i)) <= float(lat) <= (float(lat_ciu_or)+(0.1*i)) or (float(lat_ciu_des)-(0.1*i)) <= float(lat) <= (float(lat_ciu_des)+(0.1*i)):
                aer_lat = mp.get(analyzer["latitudes"], lat)["value"]
                for aer in lt.iterator(aer_lat):
                    if (float(lng_ciu_or)-(0.1*i)) <= float(aer["Longitude"]) <= (float(lng_ciu_or)+(0.1*i)) and centinela:
                        lt.addLast(lista_aeropuertos_or, aer)
                        centinela = False
                    if (float(lng_ciu_des)-(0.1*i)) <= float(aer["Longitude"]) <= (float(lng_ciu_des)+(0.1*i)) and centinela1:
                        lt.addLast(lista_aeropuertos_des, aer) 
                        centinela1 = False
        i += 1
    menor=9999999
    for aer in lt.iterator(lista_aeropuertos_or):
        lat = aer["Latitude"]
        lng = aer["Longitude"]
        distancia = semiverseno(lat_ciu_or, lat, lng_ciu_or, lng)
        if distancia <= menor:
            menor = distancia
            origen = aer
    dist_origen = menor
    menor = 999999
    for aer in lt.iterator(lista_aeropuertos_des):
        lat = aer["Latitude"]
        lng = aer["Longitude"]
        distancia = semiverseno(lat_ciu_des, lat, lng_ciu_des, lng)
        if distancia <= menor:
            menor = distancia
            destino = aer
    dist_destino = menor
    minimumCostPaths(analyzer, origen["IATA"])
    camino_minimo = minimumCostPath(analyzer, destino["IATA"])
    distancia_tot = dist_origen + dist_destino
    for t in lt.iterator(camino_minimo):
        distancia_tot += float(t["weight"])
    return (origen, destino, camino_minimo, distancia_tot)

def req_4(analyzer, iata, millas):
    distancia_km = millas * 1.6
    rutas = analyzer["rutas_dobles"]
    search_prim = prim.PrimMST(rutas)
    distancia_max = round(prim.weightMST(rutas, search_prim), 2)
    lista = search_prim["mst"]
    search_dfs = dfs.DepthFirstSearch(rutas, iata)
    lista_ruta = lt.newList(datastructure="ARRAY_LIST")
    aeropuertos = []
    distancia = 0
    for viaje in lt.iterator(lista):
        va = viaje["vertexA"]
        vb = viaje["vertexB"]
        weight = viaje["weight"]
        if va not in aeropuertos:
            list.append(aeropuertos, va)
        if vb not in aeropuertos:
            list.append(aeropuertos, vb)
        if dfs.hasPathTo(search_dfs, va) and dfs.hasPathTo(search_dfs, vb):
            r = {"Deperture":va, "Destination":vb, "Distance (km)":weight}
            lt.addLast(lista_ruta, r)
            distancia += weight
    distancia_tot = distancia*2
    alcanza = False
    if distancia_tot > distancia_km:
        dif_millas = round(((distancia_tot-distancia_km)/1.6), 2)
    else:
        dif_millas = round(((distancia_km-distancia_tot)/1.6), 2)
        alcanza = True
    distancia_tot = round(distancia_tot/2, 2)
    num_aeropuertos = len(aeropuertos)
    return (distancia_max, lista_ruta, distancia_tot, alcanza, dif_millas, distancia_km, num_aeropuertos)

def req_5 (analyzer, aer):
    aeropuertos = analyzer["aeropuertos"]
    gr.removeVertex(analyzer["rutas_unicas"], aer)
    gr.removeVertex(analyzer["rutas_dobles"], aer)
    aer_afectados = gr.adjacents(analyzer["rutas_unicas"], aer)
    afectados = lt.newList(datastructure="ARRAY_LIST")
    for aer in lt.iterator(aer_afectados):
        if aer not in afectados:
            lt.addLast(afectados, aer)
    lista = lt.newList(datastructure="ARRAY_LIST")
    for af in lt.iterator(afectados):
        aer = mp.get(aeropuertos, af)["value"]["elements"][0]
        dic_aer = {"Nombre":aer["Name"], "Ciudad":aer["City"], "Pais":aer["Country"]}
        lt.addLast(lista, dic_aer)
    num_afectados = lt.size(lista)
    if lt.size(lista) >= 6:
        lista = f_primeros_ultimos(lista, 3)
    return analyzer, num_afectados, lista

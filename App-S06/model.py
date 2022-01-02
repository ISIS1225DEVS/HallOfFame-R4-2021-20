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


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import graph as gph
from DISClib.DataStructures import mapentry as me, edge as e
from DISClib.ADT import orderedmap as om, queue
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Graphs import scc,dijsktra, prim, bfs
import folium
import amadeus as am
import math
from math import radians, cos, sin, asin, sqrt
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def create_catalog():
    catalog = {
        "routesdg" : gph.newGraph(directed=True, size=10000),
        "routesndg": gph.newGraph(size=3000),
        "MST": {"TotCost":None, "NumNodes":None, "GraphMST":None},
        "IATA2name" : mp.newMap(10000,maptype="PROBING"),
        "DuplicateRoute" : mp.newMap(50000,maptype="PROBING"),
        "RouteAir" : mp.newMap(50000,maptype="PROBING"),
        "#RoutesDG" : 0,
        "#RoutesG" : 0,
        "Cities": mp.newMap(41002,maptype="PROBING"),
        "DRg" : mp.newMap(10000,maptype="PROBING"),
        "TreeAirports" : om.newMap(),
        "1AirportDG" : None,
        "LastAirportDG" : None,
        "1AirportG" : None,
        "LastAirportG" : None,
        "FirstCity" : None,
        "LastCity" : None,
        "NumCities" : 0,
        "SCC":None

    }

    return catalog

# Funciones para agregar informacion al catalogo

def add_airport(catalog, airport):
    table = catalog["IATA2name"]
    IATA = airport["IATA"]
    if not mp.contains(table,IATA):
        mp.put(table, IATA, airport)

    clean = {
        "IATA":airport["IATA"],
        "Latitude":float(airport["Latitude"]),
        "Longitude":float(airport["Longitude"])
    }

    Long = clean["Longitude"]
    Lat = clean["Latitude"]
    if om.contains(catalog["TreeAirports"], Lat):
        arbolLong = me.getValue(om.get(catalog["TreeAirports"], Lat))
        if not om.contains(arbolLong, Long):
            om.put(arbolLong, Long, clean)
        
    else:
        om.put(catalog["TreeAirports"], Lat, om.newMap())
        arbolLong = me.getValue(om.get(catalog["TreeAirports"], Lat))
        if not om.contains(arbolLong, Long):
            om.put(arbolLong, Long, clean)

    gph.insertVertex(catalog["routesdg"], IATA)
    if catalog["1AirportDG"] is None:
        catalog["1AirportDG"] = IATA
    catalog["LastAirportDG"] = IATA


    



def add_route(catalog, route):
    air = route["Airline"]
    departure = route["Departure"]
    destination = route["Destination"]

    dgraph = catalog["routesdg"]
    graph = catalog["routesndg"]

    mp.put(catalog["RouteAir"], (air,departure,destination),None)
    if mp.contains(catalog["RouteAir"], (air,destination, departure)):
        catalog["#RoutesG"] += 1

    routeOrder = tuple(sorted((departure, destination)))
    catalog["#RoutesDG"] += 1
    if not mp.contains(catalog["DuplicateRoute"], (departure, destination)):
        # if gph.containsVertex(dgraph, departure) and gph.containsVertex(dgraph, destination):
        #     gph.addEdge(dgraph,departure, destination, float(route["distance_km"]))
        # elif not gph.containsVertex(dgraph, departure) and not gph.containsVertex(dgraph, destination):
        #     gph.insertVertex(dgraph, departure)
        #     gph.insertVertex(dgraph, destination)
        #     gph.addEdge(dgraph, departure, destination, float(route["distance_km"]))
        # elif not gph.containsVertex(dgraph, departure):
        #     gph.insertVertex(dgraph, departure)
        #     gph.addEdge(dgraph, departure, destination, float(route["distance_km"]))
        # else:
        #     gph.insertVertex(dgraph, destination)
        #     gph.addEdge(dgraph, departure, destination, float(route["distance_km"]))
        gph.addEdge(dgraph,departure, destination, float(route["distance_km"]))
        mp.put(catalog["DuplicateRoute"], (departure, destination), None)



    if (mp.contains(catalog["DuplicateRoute"], (destination, departure))) and (not mp.contains(catalog["DRg"], routeOrder)):
        if gph.containsVertex(graph, departure) and gph.containsVertex(graph, destination):
            gph.addEdge(graph,departure, destination, float(route["distance_km"]))
        elif (not gph.containsVertex(graph, departure)) and (not gph.containsVertex(graph, destination)):
            gph.insertVertex(graph, departure)
            gph.insertVertex(graph, destination)
            catalog["LastAirportG"] = destination
            gph.addEdge(graph, departure, destination, float(route["distance_km"]))
        elif not gph.containsVertex(graph, departure):
            gph.insertVertex(graph, departure)
            catalog["LastAirportG"] = departure
            gph.addEdge(graph, departure, destination, float(route["distance_km"]))
        else:
            gph.insertVertex(graph, destination)
            catalog["LastAirportG"] = destination
            gph.addEdge(graph, departure, destination, float(route["distance_km"]))
        
        if catalog["1AirportG"] is None:
            catalog["1AirportG"] = departure        
        mp.put(catalog["DRg"], routeOrder, float(route["distance_km"]))
def add_city(catalog, city):
    name = city["city_ascii"]
    if catalog["FirstCity"] is None:
        catalog["FirstCity"] = city
    catalog["LastCity"] = city
    if mp.contains(catalog["Cities"], name):
        lt.addLast(me.getValue(mp.get(catalog["Cities"], name)),city)
    else:
        mp.put(catalog["Cities"], name, lt.newList("ARRAY_LIST"))
        lt.addLast(me.getValue(mp.get(catalog["Cities"], name)),city)
    catalog["NumCities"] += 1

def loadMST(catalog):
    graph = catalog["routesndg"]
    numNodes = lt.size(gph.vertices(graph))
    search = prim.PrimMST(graph)
    totCost = prim.weightMST(graph,search)
    graphMST = gph.newGraph()
    for i in lt.iterator(search["mst"]):
        addToGraph(graphMST,i)

    mst = catalog["MST"]

    mst["TotCost"] = totCost
    mst["NumNodes"] = numNodes
    mst["GraphMST"] = graphMST

def loadSCC(catalog):
    catalog["SCC"] = scc.KosarajuSCC(catalog["routesdg"])

# Funciones de consulta
def getLoadingData(catalog):
    data = {
        "#AirDG" : lt.size(gph.vertices(catalog["routesdg"])),
        "#RoutesDG" : catalog["#RoutesDG"],
        "#AirG" :  lt.size(gph.vertices(catalog["routesndg"])),
        "#RoutesG" : catalog["#RoutesG"],
        "#Cities": catalog["NumCities"],
        "FirstAirportDG" : None,
        "LastAirportDG" : None,
        "FirstAirportG": None,
        "LastAirportG": None,
        "FirstCity" : catalog["FirstCity"],
        "LastCity" : catalog["LastCity"]
    }
    data["FirstAirportDG"] = me.getValue(mp.get(catalog["IATA2name"], catalog["1AirportDG"]))
    data["FirstAirportG"] = me.getValue(mp.get(catalog["IATA2name"], catalog["1AirportG"]))
    data["LastAirportDG"] = me.getValue(mp.get(catalog["IATA2name"], catalog["LastAirportDG"]))
    data["LastAirportG"] = me.getValue(mp.get(catalog["IATA2name"], catalog["LastAirportG"]))

    return data

def getMostInterconnections(catalog):
    dg = catalog["routesdg"]
    g = catalog["routesndg"]

    l_dg = lt.newList(datastructure="ARRAY_LIST")
    l_g = lt.newList(datastructure="ARRAY_LIST")

    max_dg = 0 

    for vertex in lt.iterator(gph.vertices(dg)):
        indegree = gph.indegree(dg, vertex)
        outdegree = gph.outdegree(dg,vertex)
        degree = indegree+outdegree
        if degree > max_dg:
            max_dg = degree
            l_dg = lt.newList(datastructure="ARRAY_LIST")
            lt.addLast(l_dg,vertex)
        elif degree == max_dg:
            lt.addLast(l_dg, vertex)

    max_g = 0
    for vertex in lt.iterator(gph.vertices(g)):
        degree = gph.degree(g, vertex)
        if degree > max_g:
            max_g = degree
            l_g = lt.newList(datastructure="ARRAY_LIST")
            lt.addLast(l_g,vertex)
        elif degree == max_g:
            lt.addLast(l_g, vertex)

    mapIATA = catalog["IATA2name"]
    
    mapFunc(l_dg, lambda x: me.getValue(mp.get(mapIATA,x)))
    mapFunc(l_g, lambda x: me.getValue(mp.get(mapIATA,x)))
    return (max_dg, l_dg),(max_g, l_g)



def getFlightTrafficClusters(catalog, IATA1, IATA2):
    kscc = catalog["SCC"]
    num_clusters = scc.connectedComponents(kscc)
    connected = scc.stronglyConnected(kscc, IATA1, IATA2)
    return num_clusters, connected, kscc


def getShortestRoute(catalog, city1, city2):
    #https://stackoverflow.com/questions/1253499/simple-calculations-for-working-with-lat-lon-and-km-distance formula grado/km
    
    min_disto,airOrigin = findNearestAirport(catalog,city1)
    min_distd,airDest = findNearestAirport(catalog, city2)

    IATAo = airOrigin["IATA"]
    IATAd = airDest["IATA"]

    route = dijsktra.Dijkstra(catalog["routesdg"],IATAo)

    if dijsktra.hasPathTo(route,IATAd):
        routePath = dijsktra.pathTo(route,IATAd)
        distancePath = dijsktra.distTo(route,IATAd)
        return airOrigin, airDest, routePath, distancePath,min_disto, min_distd
    else:
        return False, airOrigin, airDest


def getUseFlyerMiles(catalog, city, miles):
    km = miles*1.60
    mst = catalog["MST"]
    numNodes = mst["NumNodes"]
    totCost = mst["TotCost"]
    graphMST = mst["GraphMST"]

    md,airport = findNearestAirport(catalog, city,False)
    IATA = airport["IATA"]

    bfsSearch = BreadhtFisrtSearch(graphMST, IATA)
    maxDist = getLongestBranch(bfsSearch)
    maxVertex = me.getKey(lt.getElement(me.getValue(mp.get(bfsSearch["DisToSource"],maxDist)),1))
    rMaxBranch = bfs.pathTo(bfsSearch,maxVertex)
    
    dest = None
    weight = km
    for i in range(maxDist,0,-1):
        lst = me.getValue(mp.get(bfsSearch["DisToSource"],i))
        for j in lt.iterator(lst):
            weightTo = getWeightTo(me.getValue(j))
            if weightTo <= weight:
                dest = j
                weight = weightTo
    
        if dest is not None:
            break
    
    if dest is not None:
        route = bfs.pathTo(bfsSearch, dest["key"])
        routeList = lt.newList("ARRAY_LIST")
        for air in lt.iterator(route):
            infoair = me.getValue(mp.get(catalog["IATA2name"],air))
            airn, cityr, country, coords = infoair["Name"],infoair["City"], infoair["Country"], (float(infoair["Latitude"]),float(infoair["Longitude"]))
            lt.addLast(routeList,(airn, cityr,country, coords))
        return (1, numNodes, totCost, rMaxBranch, routeList)
    else:
        return 2, numNodes, totCost, rMaxBranch

def getCalculateClosedAirportEffect(catalog, air):
    dgraph = catalog["routesdg"]
    destiny = lt.newList("ARRAY_LIST")
    origin = lt.newList("ARRAY_LIST")
    for vertex in lt.iterator(gph.vertices(dgraph)):
        if vertex == air:
            adj = gph.adjacents(dgraph, vertex)
            for i in lt.iterator(adj):
                lt.addLast(origin, i)
        else:
            adj = gph.adjacents(dgraph,vertex)
            if lt.isPresent(adj, air):
                lt.addLast(destiny, vertex)

    totAffected = lt.size(destiny)+lt.size(origin)

    return destiny, origin, totAffected


#Bonos
def getShortestRouteAPI(catalog, origen, destino, client):
    clientAM = client


    latO, longO = float(origen["lat"]), float(origen["lng"])
    latD, longD = float(destino["lat"]), float(destino["lng"])

    responseO = clientAM.reference_data.locations.airports.get(latitude=latO, longitude =longO)

    responseD = clientAM.reference_data.locations.airports.get(latitude=latD, longitude =longD)
    dg = catalog["routesdg"]

    if len(responseD.data) > 0 and len(responseO.data) > 0:
        airo = None
        disto = 0
        for i in responseO.data:
            iata = i["iataCode"]
            if gph.containsVertex(dg,iata):
                airo = iata
                disto = i["distance"]["value"]
                break
        aird = None
        distd = 0
        for i in responseD.data:
            iata = i["iataCode"]
            if gph.containsVertex(dg,iata):
                aird = iata
                distd = i["distance"]["value"]
                break
        
        if (airo is not None) and (aird is not None):

            path = dijsktra.Dijkstra(dg, airo)
            if dijsktra.hasPathTo(path, aird):
                route = dijsktra.pathTo(path, aird)
                dist = dijsktra.distTo(path, aird)
                return airo, aird, route, dist, disto, distd
            else:
                return False, 1 , "No hay una ruta entre los dos aeropuertos", airo, aird, disto, distd
        else:
            return False, 2,"No hay información en la base datos sobre alguno o los dos aeropuertos proporcionado por el API"
        
    else:
        return (False, 3, "El API no retorno información sobre alguna de las ciudades")


def makeMapReq1(data,catalog):
    airT = lambda iata : me.getValue(mp.get(catalog["IATA2name"], iata))
    feature1 = folium.FeatureGroup(name="Salida")
    feature2 = folium.FeatureGroup(name="Llegada")

    airDG = data[0][1]
    air = lt.getElement(airDG,1)
    lato,longo = float(air["Latitude"]), float(air["Longitude"])
    m = folium.Map(location=(lato,longo), zoom_start=3.8)

    for i in lt.iterator(gph.edges(catalog["routesdg"])):
        vA,vB,dist = i.values()
        
        if vA == air["IATA"]:
            airAff = airT(vB)
            lat,long = float(airAff["Latitude"]), float(airAff["Longitude"])
            folium.Marker(location=(lat,long),tooltip=f"{airAff['Name']}",icon=folium.Icon(icon="plane",prefix="fa",color="red")).add_to(feature1)
            folium.PolyLine(locations=((lato,longo),(lat,long)),weight=1, color ="red", tooltip=f"{air['Name']} to {airAff['Name']}, Distance = {dist} km").add_to(feature1)
        elif vB == air["IATA"]:
            airAff = airT(vA)
            lat,long = float(airAff["Latitude"]), float(airAff["Longitude"])
            folium.Marker(location=(lat,long),tooltip=f"{airAff['Name']}",icon=folium.Icon(icon="plane",prefix="fa",color="green")).add_to(feature2)
            folium.PolyLine(locations=((lato,longo),(lat,long)),weight=1, color ="green", tooltip=f"{airAff['Name']} to {air['Name']}, Distance = {dist} km").add_to(feature2)

    folium.Marker(location=(lato,longo),tooltip=f"{air['Name']}",icon=folium.Icon(icon="plane",prefix="fa"), radius=5).add_to(m)

    m.add_child(feature1)
    m.add_child(feature2)
            

    m.add_child(folium.map.LayerControl())
    m.save(cf.file_dir+"/Maps/Req1/Req1DG.html")

    air = lt.getElement(airDG,1)
    lato,longo = float(air["Latitude"]), float(air["Longitude"])
    m = folium.Map(location=(lato,longo), zoom_start=3.8)

    for i in lt.iterator(mp.keySet(catalog["DRg"])):
        air1,air2 = i
        air1 = airT(air1)
        dist = me.getValue(mp.get(catalog["DRg"],i))
        air2 = airT(air2)
        if air1["Name"] == air["Name"]:
            coordD = float(air2["Latitude"]),float(air2["Longitude"])
            folium.Marker(location=coordD,tooltip=f"{air2['Name']}",icon=folium.Icon(icon="plane",prefix="fa",color="green")).add_to(m)
            folium.PolyLine(locations=((lato,longo),coordD),weight=1, color ="green", tooltip=f"{air['Name']} - {air2['Name']}, Distance = {dist} km").add_to(m)
        elif air2["Name"] == air["Name"]:
            coordD = float(air1["Latitude"]),float(air1["Longitude"])
            folium.Marker(location=coordD,tooltip=f"{air1['Name']}",icon=folium.Icon(icon="plane",prefix="fa",color="green")).add_to(m)
            folium.PolyLine(locations=((lato,longo),coordD),weight=1, color ="green", tooltip=f"{air['Name']} - {air1['Name']}, Distance = {dist} km").add_to(m)

    folium.Marker(location=(lato,longo),tooltip=f"{air['Name']}",icon=folium.Icon(icon="plane",prefix="fa"), radius=5).add_to(m)

    m.save(cf.file_dir+"/Maps/Req1/Req1NDG.html")


def makeMapReq2(catalog, kscc, connected, IATA1, IATA2):
    if connected:
        air = me.getValue(mp.get(catalog["IATA2name"],IATA1))
        coords = float(air["Latitude"]), float(air["Longitude"])
        m = folium.Map(location=coords,zoom_start=2.5)
        kscc = kscc["idscc"]
        clust = me.getValue(mp.get(kscc,IATA1))
        
        for i in lt.iterator(mp.keySet(kscc)):
            clst = me.getValue(mp.get(kscc, i))
            if clst == clust:   
                airC = me.getValue(mp.get(catalog["IATA2name"],i))
                coords = float(airC["Latitude"]), float(airC["Longitude"])
                if i == IATA1 or i == IATA2:
                    folium.Marker(location=coords, tooltip=f"{airC['Name']}",icon=folium.Icon(icon="plane",prefix="fa")).add_to(m)
                else:
                    folium.Marker(location=coords, tooltip=f"{airC['Name']}",icon=folium.Icon(icon="plane",prefix="fa",color="green")).add_to(m)

        m.save(cf.file_dir+"/Maps/Req2/Req2.html")

    else:
        air = me.getValue(mp.get(catalog["IATA2name"],IATA1))
        coords = float(air["Latitude"]), float(air["Longitude"])
        kscc = kscc["idscc"]
        clst1 = me.getValue(mp.get(kscc, IATA1))
        clst2 = me.getValue(mp.get(kscc, IATA2))
        f1 = folium.FeatureGroup(name=f"Cluster {clst1}")
        f2 = folium.FeatureGroup(name=f"Cluster {clst2}")
        m = folium.Map(location=coords,zoom_start=2.5)
        for i in lt.iterator(mp.keySet(kscc)):
            clst = me.getValue(mp.get(kscc, i))
            if clst == clst1:
                airC = me.getValue(mp.get(catalog["IATA2name"],i))
                coords = float(airC["Latitude"]), float(airC["Longitude"])
                if i == IATA1:
                    folium.Marker(location=coords, tooltip=f"{airC['Name']}",icon=folium.Icon(icon="plane",prefix="fa")).add_to(f1)
                else:
                    folium.Marker(location=coords, tooltip=f"{airC['Name']}",icon=folium.Icon(icon="plane",prefix="fa",color="green")).add_to(f1)
            elif clst == clst2:
                airC = me.getValue(mp.get(catalog["IATA2name"],i))
                coords = float(airC["Latitude"]), float(airC["Longitude"])
                if i == IATA1:
                    folium.Marker(location=coords, tooltip=f"{airC['Name']}",icon=folium.Icon(icon="plane",prefix="fa")).add_to(f2)
                else:
                    folium.Marker(location=coords, tooltip=f"{airC['Name']}",icon=folium.Icon(icon="plane",prefix="fa",color="red")).add_to(f2)

        m.add_child(f1)
        m.add_child(f2)
        m.add_child(folium.map.LayerControl())
        m.save(cf.file_dir+"/Maps/Req2/Req2.html")

def makeMapReq3(catalog, city1,city2, min_disto, min_distd, airOrigin, airDest, routePath):
    coords1 = float(city1["lat"]),float(city1["lng"])
    coords2 = float(city2["lat"]),float(city2["lng"])
    punto_medio = (coords1[0]+coords2[0])/2, (coords1[1]+coords2[1])/2

    air = lambda iata:  me.getValue(mp.get(catalog["IATA2name"],iata))

    m = folium.Map(punto_medio, zoom_start=3)

    folium.Marker(location=coords1, tooltip=city1["city_ascii"], icon=folium.Icon(icon="building",prefix="fa",color="green")).add_to(m)
    folium.Marker(location=coords2, tooltip=city2["city_ascii"], icon=folium.Icon(icon="building",prefix="fa",color="red")).add_to(m)

    iataO, *coordsAO = airOrigin.values()
    iataD, *coordsAD = airDest.values()

    folium.Marker(coordsAO, tooltip=f"{air(iataO)['Name']}", icon=folium.Icon(icon="plane", prefrix="fa",icon_color="green")).add_to(m)
    folium.Marker(coordsAD, tooltip=f"{air(iataD)['Name']}", icon=folium.Icon(icon="plane", prefrix="fa",icon_color="red")).add_to(m)

    folium.PolyLine((coords1, coordsAO),tooltip=f"Distancia {min_disto} km", color="green", weight=1).add_to(m)
    folium.PolyLine((coords2, coordsAD),tooltip=f"Distancia {min_distd} km", color="green", weight=1).add_to(m)

    for i in lt.iterator(routePath):
        vA,vB,dist = i.values()
        airA = air(vA)
        coordsA = float(airA["Latitude"]), float(airA["Longitude"])
        airB = air(vB)
        coordsB = float(airB["Latitude"]), float(airB["Longitude"])
        folium.PolyLine((coordsA, coordsB),tooltip=f"{airA['Name']} to {airB['Name']}, Distance = {dist} km", color="blue").add_to(m)
        if vB != iataD:
            folium.Marker(coordsB, tooltip=f"{airB['Name']}", icon=folium.Icon(icon="plane", prefix="fa")).add_to(m)

    m.save(cf.file_dir+"/Maps/Req3/Req3.html")

def makeMapReq4(catalog, data):
    maxBranch = data[3]
    air = lambda iata:  me.getValue(mp.get(catalog["IATA2name"],iata))
    mBranch = folium.Map((0,0),zoom_start=2)
    maxsize = lt.size(maxBranch)

    lastAir = None 
    lastCoords = None

    for pos,i in enumerate(lt.iterator(maxBranch),1):
        airp = air(i)
        name = airp["Name"]
        coords = float(airp["Latitude"]),float(airp["Longitude"])
        if pos == 1:
            lastCoords = coords
            lastAir = name
            folium.Marker(coords, tooltip=name, icon=folium.Icon(icon="plane", prefix="fa", color="green")).add_to(mBranch)
        elif pos == maxsize:
            folium.Marker(coords, tooltip=name, icon=folium.Icon(icon="plane", prefix="fa", color="red")).add_to(mBranch)
        else:
            folium.Marker(coords, tooltip=name, icon=folium.Icon(icon="plane", prefix="fa")).add_to(mBranch)

        if pos > 1:
            folium.PolyLine((lastCoords, coords), tooltip=f"{lastAir} - {name}", weight=2).add_to(mBranch)
            lastCoords = coords
            lastAir = name
    mBranch.save(cf.file_dir+"/Maps/Req4/Req4MBranch.html")

    cities = data[-1]

    mRoute = folium.Map((0,0),zoom_start=2.2)
    lccoord = None
    lcity = None
    csize = lt.size(cities)

    for i,city in enumerate(lt.iterator(cities),1):
        name = city[0]
        citya = city[1]
        coords = city[-1]
        count = city[2]
        
        if i == 1:
            lccoord = coords
            lcity = name
            folium.Marker(location= coords, tooltip=f"{name}, {citya}, {count}", icon=folium.Icon(icon="plane", prefix="fa", color="green")).add_to(mRoute)
        elif i == csize:
            folium.Marker(location= coords, tooltip=f"{name}, {citya}, {count}", icon=folium.Icon(icon="plane", prefix="fa", color="red")).add_to(mRoute)
        else:
            folium.Marker(location= coords, tooltip=f"{name}, {citya}, {count}", icon=folium.Icon(icon="plane", prefix="fa")).add_to(mRoute)

        if i > 1:
            folium.PolyLine(locations=(lccoord,coords),tooltip=f"{lcity} to {name}", weight = 2).add_to(mRoute)
            lccoord = coords
            lcity = name

    mRoute.save(cf.file_dir+"/Maps/Req4/Req4Route.html")

def makeMapReq5(data, airC, catalog):
    aeroT = lambda iata : me.getValue(mp.get(catalog["IATA2name"], iata))

    aero = aeroT(airC)

    aecoords = float(aero["Latitude"]), float(aero["Longitude"])
    aeName = aero["Name"]


    origen = data[1]
    destino = data[0]

    f1 = folium.FeatureGroup("Destino")

    f2 = folium.FeatureGroup("Origen")


    m = folium.Map((0,0), zoom_start=2.2)

    folium.Marker(aecoords, tooltip=f"{aeName}, Cerrado", icon=folium.Icon(icon="close", prefix="fa",color="black")).add_to(m)


    for i in lt.iterator(destino):
        aeri = aeroT(i)
        aicoords = float(aeri["Latitude"]), float(aeri["Longitude"])
        aiName = aeri["Name"]
        folium.Marker(aicoords, tooltip=aiName, icon=folium.Icon(icon="plane",prefix="fa", color="black", icon_color="green")).add_to(f1)
        folium.PolyLine((aicoords, aecoords), tooltip=f"{aiName} to {aeName}", color="green", weight=1).add_to(f1)

    for i in lt.iterator(origen):
        aeri = aeroT(i)
        aicoords = float(aeri["Latitude"]), float(aeri["Longitude"])
        aiName = aeri["Name"]
        folium.Marker(aicoords, tooltip=aiName, icon=folium.Icon(icon="plane",prefix="fa", color="black", icon_color="red")).add_to(f2)
        folium.PolyLine((aicoords, aecoords), tooltip=f"{aeName} to {aiName}", color="red", weight=1).add_to(f2)


    m.add_child(f1)
    m.add_child(f2)
    m.add_child(folium.map.LayerControl())

    m.save(cf.file_dir+"/Maps/Req5/Req5.html")



#Funciones auxiliares
def checkCity(catalog, city):
    if mp.contains(catalog["Cities"], city):
        cities = me.getValue(mp.get(catalog["Cities"],city))
        if lt.size(cities) > 1:
            return 1,cities
        else:
            return 2, lt.getElement(me.getValue(mp.get(catalog["Cities"],city)),1)
    else:
        return False

def haversine(lat1, lon1, lat2, lon2):
    #https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
    R = 6372.8 # this is in miles.  For Earth radius in kilometers use 6372.8 km
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
    c = 2*asin(sqrt(a))
    return R * c

def mapFunc(l, func):
    for i in range(1,lt.size(l)+1):
        lt.changeInfo(l,i, func(lt.getElement(l,i)))


def BreadhtFisrtSearch(graph, source):
    """
    Genera un recorrido BFS sobre el grafo graph
    Args:
        graph:  El grafo a recorrer
        source: Vertice de inicio del recorrido.
    Returns:
        Una estructura para determinar los vertices
        conectados a source
    Raises:
        Exception
    """
    
    search = {
              'source': source,
              'visited': None,
              'MaxDist':0,
              "DisToSource": None
              }
    search['visited'] = mp.newMap(numelements=gph.numVertices(graph),
                                   maptype='PROBING',
                                   comparefunction=graph['comparefunction']
                                   )
    search['DisToSource'] = mp.newMap(numelements=gph.numVertices(graph),
                                   maptype='PROBING',
                                   comparefunction=graph['comparefunction']
                                   )
    mp.put(search['visited'], source, {'marked': True,
                                        'edgeTo': None,
                                        'distTo': 0,
                                        "weightTo":0
                                        })
    mp.put(search["DisToSource"], 0, mp.get(search["visited"],source))
    bfsVertex(search, graph, source)
    return search


def bfsVertex(search, graph, source):
    """
    Funcion auxiliar para calcular un recorrido BFS
    Args:
        search: Estructura para almacenar el recorrido
        vertex: Vertice de inicio del recorrido.
    Returns:
        Una estructura para determinar los vertices
        conectados a source
    Raises:
        Exception
    """
    
    adjsqueue = queue.newQueue()
    queue.enqueue(adjsqueue, source)
    while not (queue.isEmpty(adjsqueue)):
        vertex = queue.dequeue(adjsqueue)
        visited_v = mp.get(search['visited'], vertex)['value']
        adjslst = gph.adjacents(graph, vertex)
        for w in lt.iterator(adjslst):
            visited_w = mp.get(search['visited'], w)
            if visited_w is None:
                dist_to_w = visited_v['distTo'] + 1
                if dist_to_w > search["MaxDist"]:
                    search["MaxDist"] = dist_to_w
                weight_to_w = visited_v["weightTo"] + e.weight(gph.getEdge(graph, vertex, w))
                visited_w = {'marked': True,
                             'edgeTo': vertex,
                             "distTo": dist_to_w,
                             "weightTo": weight_to_w
                             }
                mp.put(search['visited'], w, visited_w)
                if mp.contains(search["DisToSource"], dist_to_w):
                    lt.addLast(me.getValue(mp.get(search["DisToSource"],dist_to_w)),me.newMapEntry(w, visited_w))
                else:
                    mp.put(search["DisToSource"],dist_to_w, lt.newList("ARRAY_LIST"))
                    lt.addLast(me.getValue(mp.get(search["DisToSource"],dist_to_w)),me.newMapEntry(w,visited_w))
                
                queue.enqueue(adjsqueue, w)
    return search

def getLongestBranch(search):
    return search["MaxDist"]

def getWeightTo(visited):
    return visited["weightTo"]

def addToGraph(graph, edge):
    vertexA = edge["vertexA"]
    vertexB = edge["vertexB"]
    weight = edge["weight"]

    if gph.containsVertex(graph,vertexA) and gph.containsVertex(graph,vertexB):
        gph.addEdge(graph,vertexA,vertexB, weight)
    elif not gph.containsVertex(graph,vertexA) and not gph.containsVertex(graph,vertexB):
        gph.insertVertex(graph,vertexA)
        gph.insertVertex(graph,vertexB)
        gph.addEdge(graph,vertexA,vertexB,weight)
    elif not gph.containsVertex(graph,vertexA):
        gph.insertVertex(graph,vertexA)
        gph.addEdge(graph,vertexA,vertexB,weight)
    else:
        gph.insertVertex(graph,vertexB)
        gph.addEdge(graph,vertexA,vertexB,weight)

def findNearestAirport(catalog, city1, typeG = True):
    # city1 = me.getValue(mp.get(catalog["Cities"], city1))

    olat, olong = float(city1["lat"]), float(city1["lng"])

    treeLat = catalog["TreeAirports"]

    foundAirport = False
    r = 10
    typeGraph = "routesdg" if typeG else "routesndg"

    airOrigin = None
    min_disto = float("inf")
    while not foundAirport and r <= 1000:
        olatSquare = r//2 * 0.009
        olongSquare = r//2 * (abs(0.009/math.cos(olat*(math.pi/180))))


        olatmin, olatmax = olat-olatSquare, olat+olatSquare
        olongmin, olongmax = olong-olongSquare, olong+olongSquare

        if airOrigin is None:
            for treeLong in lt.iterator(om.values(treeLat, olatmin, olatmax)):
                for airport in lt.iterator(om.values(treeLong, olongmin, olongmax)):
                    dist = haversine(airport["Latitude"], airport["Longitude"], olat, olong)
                    if gph.containsVertex(catalog[typeGraph], airport["IATA"]):
                        if dist < min_disto:
                            min_disto = dist
                            airOrigin = airport
            
        
        if (airOrigin is not None):
            foundAirport = True

        r += 10
    return min_disto, airOrigin

def create_client(key, secretK):
    return  am.Client(client_id=key, client_secret=secretK)

def makeDGraph(catalog):
    dg = catalog["routesdg"]
    air = lambda iata : me.getValue(mp.get(catalog["IATA2name"], iata))
    m = folium.Map(location=(0,0),zoom_start=2.2,prefer_canvas=True)

    for i in lt.iterator(gph.edges(dg)):
        ori,dest,dist = i.values()
        ori = air(ori).copy()
        dest = air(dest).copy()
        ocoords = [float(ori["Latitude"]),float(ori["Longitude"])]
        dcoords = [float(dest["Latitude"]),float(dest["Longitude"])]
        airo = ori["Name"]
        aird = dest["Name"]
        folium.PolyLine((ocoords, dcoords),weight=0.2,tooltip=f"{airo} to {aird}, Distance: {dist} km").add_to(m)
    m.save(cf.file_dir+"/Maps/Graphs/Digrafo.html")

def makeNDGraph(catalog):
    air = lambda iata : me.getValue(mp.get(catalog["IATA2name"], iata))
    m = folium.Map(location=(0,0),zoom_start=2.2,prefer_canvas=True)
    for i in lt.iterator(mp.keySet(catalog["DRg"])):
        air1,air2 = i
        dist = me.getValue(mp.get(catalog["DRg"],i))
        air1 = air(air1)
        air2 = air(air2)
        coord1 = float(air1["Latitude"]), float(air1["Longitude"])
        coord2 = float(air2["Latitude"]), float(air2["Longitude"])
        coords  = coord1,coord2
        folium.PolyLine(coords, weight=0.5,color="green" ,tooltip=f"{air1['Name']} - {air2['Name']}, Distance: {dist} km").add_to(m)
    m.save(cf.file_dir+"/Maps/Graphs/NDGraph.html")


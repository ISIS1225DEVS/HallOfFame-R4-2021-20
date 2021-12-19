"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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

from prettytable.prettytable import PrettyTable
import config as cf
import sys
import controller
from prettytable import PrettyTable
import prettytable as pt
import privateInfo as secret 
from DISClib.ADT import list as lt, map as mp
from DISClib.DataStructures import mapentry as me
assert cf

sys.setrecursionlimit(2**15)

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Crear el catálogo")
    print("2- Cargar información en el catálogo")
    print("3- REQ. 1: Encontrar puntos de interconexión aérea")
    print("4- REQ. 2: Encontrar clústeres de tráfico aéreo")
    print("5. REQ. 3: Encontrar la ruta más corta entre ciudades")
    print("6. REQ. 4: Utilizar las millas de viajero")
    print("7. REQ. 5: Cuantificar el efecto de un aeropuerto cerrado")  
    print("8. REQ. 6 (BONO): Comparar con servicio WEB externo")  
    print("9. REQ. 7 (BONO): Visualizar gráficamente los requerimientos") 
    print("0- Salir")

def printLoadingData(data):
    print("=== Airports-Routes DiGraph ===")
    print(f"Nodes: {data['#AirDG']}")
    print(f"Edges: {data['#RoutesDG']}")
  
    print("First & Last Airport loaded in the DiGraph.")
    dgTable = PrettyTable("IATA,Name,City,Country,Latitude,Longitude".split(","))
    dgTable.hrules = pt.ALL
    row = [data["FirstAirportDG"][i] for i in dgTable.field_names]
    dgTable.add_row(row)
    row = [data["LastAirportDG"][i] for i in dgTable.field_names]
    dgTable.add_row(row)
    print(dgTable)

    print("=== Airports-Routes Graph ===")
    print(f"Nodes: {data['#AirG']}")
    print(f"Edges: {data['#RoutesG']}")
  
    print(f"First & Last Airport loaded in the Graph.")
    gTable = PrettyTable("IATA,Name,City,Country,Latitude,Longitude".split(","))
    gTable.hrules = pt.ALL
    row = [data["FirstAirportG"][i] for i in gTable.field_names]
    gTable.add_row(row)
    row = [data["LastAirportG"][i] for i in gTable.field_names]
    gTable.add_row(row)
    print(gTable)

    print("\n\n=== City Network ===")
    print(f"The number of cities are: {data['#Cities']}")
    print("\nInformacíon de la ultima ciudad cargada")
    cTable = PrettyTable(["city","country","lat","lng","population"])
    cTable.hrules = pt.ALL
    row = [data["FirstCity"][i] for i in cTable.field_names]
    cTable.add_row(row)
    row = [data["LastCity"][i] for i in cTable.field_names]
    cTable.add_row(row)
    print(cTable)


def printMostInterconnections(req1):
    table = PrettyTable(["IATA", "Name", "City", "Country", "Graph", "#Interconnections"])
    table.align = "c"
    table.hrules = pt.ALL

    dg_Num = req1[0][0]
    l_dg = req1[0][1]
    for vals in lt.iterator(l_dg):
        row = []
        for val in table.field_names[:-2]:
            row += [vals[val]]
        row += ["Digraph", dg_Num]
        table.add_row(row)

    g_num = req1[1][0]
    l_g = req1[1][1]

    for vals in lt.iterator(l_g):
        row = []
        for val in table.field_names[:-2]:
            row += [vals[val]]
        row += ["Non digraph", g_num]
        table.add_row(row)

    print(table)

def printFlightTrafficClusters(req2, IATA1, IATA2):
    print("")
    print(f"En la red de transporte aeroeo existen {req2[0]} clusters")
    print(f"Los aeropuertos {IATA1} y {IATA2} {'estan en el mismo cluster' if req2[1] else 'no estan en el mismo cluster'}.")
    print("")

def printShortestRoute(catalog, req3, origen, destino):
    name = lambda x: me.getValue(mp.get(catalog['IATA2name'],x))['Name']

    print(f"\nEl codigo IATA del aeropuerto de origen es {req3[0]['IATA']}")
    print(f"El nombre es: {name(req3[0]['IATA'])}")

    print(f"El codigo IATA del aeropuerto de destino es {req3[1]['IATA']}")
    print(f"El nombre es: {name(req3[1]['IATA'])}")

    print("La ruta mas corta es la siguiente:")
    rutaT = PrettyTable(["Origen", "Destino", "Distancia (km)"])
    rutaT.hrules = pt.ALL
    for i in lt.iterator(req3[2]):
        rutaT.add_row([name(i["vertexA"]),name(i["vertexB"]),i["weight"]])
    print(rutaT)

    print(f"La distancia para llegar a {name(req3[0]['IATA'])} desde {origen} es {round(req3[-2],2)}km")
    print(f"La distancia para llegar a {destino} desde {name(req3[1]['IATA'])} es de {round(req3[-1],2)}km")
    print(f"La distancia total del viaje es {round(req3[-3]+req3[-2]+req3[-1],2)}km\n")

def printFlyerMiles(req4):
    print(f"El numero de nodos conectados a la red de expansión minima es: {req4[1]}")
    print(f"El distancia total de la red es de {req4[2]}")
    print("Rama mas larga en la red:")
    for pos,i in enumerate(lt.iterator(req4[3])):
        if pos != lt.size(req4[3])-1:
            print(i,end="->")
        else:
            print(i)
    if req4[0] == 1:   
        routeTable = PrettyTable(["Pos", "Aeropuerto","Ciudad","Pais"])
        tam = lt.size(req4[4])
        routeTable.hrules = pt.ALL
        print("Ruta optima con las millas disponibles")
        for pos, i in enumerate(lt.iterator(req4[4])):
            if pos == 0:
                routeTable.add_row(["Origen", i[0], i[1], i[2]])
            elif pos == tam-1:
                routeTable.add_row(["Destino", i[0], i[1], i[2]])
            else:
                routeTable.add_row(["Parada", i[0], i[1], i[2]])
        print(routeTable)
    else:
        print("Con las millas actual no es posible viajar a ninguna ciudad")

def printCalculateClosedAirportEffect(catalog,req5,air):
    print(f"El numero total de aeropuertos afectados por el cierre de {air} es {req5[2]}")

    print(f"Hay dos tipos de aeropuertos afectados, los que tenian vuelos hacia {air} (Destino) y los que recibian vuelos de {air} (Origen)")
    tableA = PrettyTable(["Num","IATA", "Name", "City","Country" ,"Tipo"])
    tableA.hrules = pt.ALL
    i = 1
    for airO in lt.iterator(req5[0]):
        row = [i]
        for key in tableA.field_names[1:-1]:
            row.append(me.getValue(mp.get(catalog["IATA2name"],airO))[key])
        row.append("Origen")
        tableA.add_row(row)
        i+=1
        
    for airD in lt.iterator(req5[1]):
        row = [i]
        for key in tableA.field_names[1:-1]:
            row.append(me.getValue(mp.get(catalog["IATA2name"],airD))[key])
        row.append("Destino")
        tableA.add_row(row)
        i+=1
    
    print(tableA)

def printShortestRouteAPI(catalog,req6,origen,destino,req3):

    name = lambda x: me.getValue(mp.get(catalog['IATA2name'],x))['Name']
    print("\nUtilizando el API de Amadeus se obtuvieron los siguientes resultados: ")

    print(f"\nEl codigo IATA del aeropuerto de origen es {req6[0]}")
    print(f"El nombre es: {name(req6[0])}")

    print(f"El codigo IATA del aeropuerto de destino es {req6[1]}")
    print(f"El nombre es: {name(req6[1])}")

    print("La ruta mas corta es la siguiente:")
    rutaT = PrettyTable(["Origen", "Destino", "Distancia (km)"])
    rutaT.hrules = pt.ALL
    for i in lt.iterator(req6[2]):
        rutaT.add_row([name(i["vertexA"]),name(i["vertexB"]),i["weight"]])
    print(rutaT)

    print(f"La distancia para llegar a {name(req6[0])} desde {origen} es {round(req6[-2],2)}km")
    print(f"La distancia para llegar a {destino} desde {name(req6[1])} es de {round(req6[-1],2)}km")
    print(f"La distancia total del viaje es {round(req6[-3]+req6[-2]+req6[-1],2)}km\n")

    print("Utilizando los datos de la base de datos se obtuvo: ")
    if req3[0]:
        print(f"Los aeropuertos seleccionados fueron {name(req3[0]['IATA'])} para {origen} y {name(req3[1]['IATA'])} para {destino}")
        printShortestRoute(catalog, req3,origen, destino)
        totDistAPI = req6[-3]+req6[-2]+req6[-1]
        totDistDB = req3[-3]+req3[-2]+req3[-1]
        if totDistDB < totDistAPI:
            print("Como se puede observar con los resultados de la aplicación la distancia total es menor")
        elif totDistDB == totDistAPI:
            print("Para los dos casos las distancias son iguales")
        else:
            print("Como se puede observar con los resultados de la API la distancia total es menor")
        print("")
    
    else:
        print("No se logre calcular una ruta")
        print(f"Los aeropuertos seleccionados fueron {name(req3[1])} para {origen} y {name(req3[2])} para {destino}")
        print("")

def printSelectCity(cities):
    print("")
    print("Seleccione la ciudad que desee")
    citiesT = PrettyTable(["Option", "City","State", "Country"])
    citiesT.hrules = pt.ALL
    citiesT.align = "c"
    for i, city in enumerate(lt.iterator(cities),1):
        citiesT.add_row([i,city["city_ascii"],city["admin_name"],city["country"]])
    print(citiesT,end="\n\n")
    opt = int(input("Seleccione una opción: "))
    return lt.getElement(cities,opt)


catalog = None
req1Map = True
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
 
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = controller.create_catalog()
        client = controller.create_client(secret.KEY, secret.SECRET)
        
    elif int(inputs[0]) == 2:
        controller.loadData(catalog)
        data = controller.getLoadingData(catalog)
        printLoadingData(data)
        var = input("Ingrese \"Si\" si desea crear un mapa de los grafo (Esto puede tomar varios minutos): ")
        if var == "Si":
            controller.makeGraphs(catalog)

    elif int(inputs[0]) == 3:
        req1 = controller.getMostInterconnections(catalog)
        printMostInterconnections(req1)
        if req1Map :
            controller.makeMapReq1(req1,catalog)
            req1Map = False
    
    elif int(inputs[0]) == 4:
        IATA1 = input("Ingrese el codigo IATA del primer aeropuerto (en mayusculas): ")
        IATA2 = input("Ingrese el codigo IATA del segundo aeropuerto (en mayusculas): ")
        try:
            req2 = controller.getFlightTrafficClusters(catalog,IATA1,IATA2)
            printFlightTrafficClusters(req2, IATA1, IATA2)
            mapReq2 = input("Ingrese \"Si\" para crear un mapa del requerimiento: ")
            if mapReq2 == "Si":
                controller.makeMapReq2(catalog, req2[2],req2[1],IATA1,IATA2)
        except Exception as ex:
            print("Lo siento, no tengo la información de los aeropuertos en mi base de datos")
    
    elif int(inputs[0]) == 5:
        city1 = input("Ingrese el nombre de la ciudad de origen (no utilice simbolos como tildes): ")
        city2 = input("Ingrese el nombre de la ciudad de destino (no utilice simbolos como tildes): ")

        vcity1 = controller.checkCity(catalog,city1)
        vcity2 = controller.checkCity(catalog,city2)

        if vcity1 and vcity2:
            if vcity1[0] == 1:
                vcity1 = printSelectCity(vcity1[1])
            else:
                vcity1 = vcity1[1]

            if vcity2[0] == 1:
                vcity2 = printSelectCity(vcity2[1])
            else:
                vcity2 = vcity2[1]
            req3 = controller.getShortestRoute(catalog, vcity1, vcity2)
            if req3[0]:
                printShortestRoute(catalog,req3,city1,city2)
                mapReq3 = input("Ingrese \"Si\" para crear un mapa del requerimiento: ")
                if mapReq3 == "Si":
                    controller.makeMapReq3(catalog,vcity1,vcity2,req3[-2],req3[-1],req3[0],req3[1],req3[2])
            else:
                print("No se pudo encontrar una ruta")
        else:
            print("Lo siento alguna o las dos ciudades suministradas no se encuentran en la base de datos")
    
    elif int(inputs[0]) == 6:
        city = input("Ingrese la ciudad de donde parte: ")
        valid = controller.checkCity(catalog, city)
        if valid:
            if valid[0] == 1:
                city = printSelectCity(valid[1])
            else:
                city = valid[1]
            
            miles = float(input("Ingrese las millas disponibles"))
            
            req4 = controller.getFlyerMiles(catalog, city, miles)
            printFlyerMiles(req4)
            if req4[0] == 1:
                mapReq4 = input("Ingrese \"Si\" para crear un mapa del requerimiento: ")
                if mapReq4 == "Si":
                    controller.makeMapReq4(catalog,req4)
        else:
            print("Lo siento la ciudad ingresa no esta en mi base de datos")

        
    
    elif int(inputs[0]) == 7:
        air = input("Ingrese el codigo IATA del aeropuerto del cual desea cuantificar el efecto: ")
        try:
            req5 = controller.getCalculateClosedAirportEffect(catalog,air)
            printCalculateClosedAirportEffect(catalog,req5,air)
            mapReq5 = input("Ingrese \"Si\" para crear un mapa del requerimiento: ")
            if mapReq5 == "Si":
                    controller.makeMapReq5(req5,air,catalog)
        except Exception:
            print("Lo siento el codigo IATA indicado no esta en mi base de datos")

    elif int(inputs[0]) == 8:
        city1 = input("Ingrese el nombre de la ciudad de origen (no utilice simbolos como tildes) ")
        city2 = input("Ingrese el nombre de la ciudad de destino (no utilice simbolos como tildes) ")

        vcity1 = controller.checkCity(catalog,city1)
        vcity2 = controller.checkCity(catalog,city2)

        if vcity1 and vcity2:
            if vcity1[0] == 1:
                vcity1 = printSelectCity(vcity1[1])
            else:
                vcity1 = vcity1[1]

            if vcity2[0] == 1:
                vcity2 = printSelectCity(vcity2[1])
            else:
                vcity2 = vcity2[1]
            req6 = controller.getShortestRouteAPI(catalog, vcity1, vcity2,client)
            if req6[0]:
                req3 = controller.getShortestRoute(catalog, vcity1, vcity2)
                printShortestRouteAPI(catalog,req6,city1,city2,req3)
            else:
                print(req6[2])
        else:
            print("Lo siento alguna o las dos ciudades suministradas no se encuentran en la base de datos")

    elif int(inputs[0]) == 9:
        pass


    else:
        sys.exit(0)
sys.exit(0)

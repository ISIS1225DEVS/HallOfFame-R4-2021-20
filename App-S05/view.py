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
import config as cf
import sys
import threading
import time as tm
import controller
from DISClib.ADT import list as lt
import prettytable 
from prettytable import PrettyTable
assert cf

default_limit = 1000 
sys.setrecursionlimit(default_limit*1000) 

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("\nBienvenido")
    print("1- Cargar información de los aeropuertos")
    print("2- (Req 1) Encontrar puntos de interconexión aérea")
    print("3- (Req 2) Encontrar clústeres de tráfico aéreo")
    print("4- (Req 3) Encontrar la ruta más corta entre ciudades")
    print("5- (Req 4) Utilizar las millas de viajero")
    print("6- (Req 5) Cuantificar el efecto de un aeropuerto cerrado")
    print("0- Salir")

def printFirstLastCity(cities):
   x = PrettyTable(hrules=prettytable.ALL)
   x.field_names = ['City', 'Country','Latitude', 'Longitude', 'population']
   x._max_width = {'City':20, 'Country': 20}
   city1 = lt.firstElement(cities)
   city2 = lt.lastElement(cities)
   x.add_row([city1['city_ascii'], city1['country'], city1['lat'], city1['lng'], city1['population']])
   x.add_row([city2['city_ascii'], city2['country'], city2['lat'], city2['lng'], city2['population']])
   print(x)

def printFirstLastAirport(airports):
   x = PrettyTable(hrules=prettytable.ALL)
   x.field_names = ["IATA", "Name", "City", "Country", "Latitude", "Longitude"]
   x._max_width = {'Name':20, 'City': 20, 'Country': 20}
   air1 = lt.firstElement(airports)
   air2 = lt.lastElement(airports)
   x.add_row([air1['IATA'], air1['Name'], air1['City'], air1['Country'], air1['Latitude'], air1['Longitude']])
   x.add_row([air2['IATA'], air2['Name'], air2['City'], air2['Country'], air2['Latitude'], air2['Longitude']])
   print(x)

def printAirports(airports):
   x = PrettyTable(hrules=prettytable.ALL)
   x.field_names = ["IATA", "Name", "City", "Country", "Latitude", "Longitude"]
   x._max_width = {'Name':20, 'City': 20, 'Country': 20}
   for airport in lt.iterator(airports):
        x.add_row([airport['IATA'], airport['Name'], airport['City'], airport['Country'], airport['Latitude'], airport['Longitude']])
   print(x)

def printCitiesSameName (cities):
   x = PrettyTable(hrules=prettytable.ALL)
   x.field_names = ['#','City', 'Population', 'Latitude', 'Longitude', 'Country', 'Admin_name']
   x._max_width = {'Admin_name':20, 'City': 20, 'Country': 20}
   i = 0
   for city in lt.iterator(cities):
       i+=1
       x.add_row([i, city['city_ascii'], city['population'], city['lat'], city['lng'], city['country'], city['admin_name']])
   print(x)

def printAirInterconection(airport):
   x = PrettyTable(hrules=prettytable.ALL)
   x.field_names = ['IATA', 'Airport (Name)', 'City', 'Country', 'Connections', 'Inbound', 'Outbound',]
   x._max_width = {'Airport (Name)':20, 'City': 20, 'Country': 20}
   for air in lt.iterator(airport):
       x.add_row([air['Airport'], air['Name'], air['City'], air['Country'], air['Interconnections'], air['Inbound'], air['Outbound']])
   print(x)

def printCityInfo (city):
    x = PrettyTable(hrules=prettytable.ALL)
    x.field_names = ['City', 'Population', 'Latitude', 'Longitude', 'Country', 'Admin_name']
    x._max_width = {'Admin_name':20, 'City': 20, 'Country': 20}
    
    x.add_row([city['city_ascii'], city['population'], city['lat'], city['lng'], city['country'], city['admin_name']])
    print(x)

def printAirportCity (airport, distance):
    x = PrettyTable(hrules=prettytable.ALL)
    x.field_names = ['IATA', 'Name', 'City', 'Country', 'Distance to city (km)']
    x._max_width = {'Name':20, 'City': 20, 'Country': 20}
    x.add_row([airport['IATA'], airport['Name'], airport['City'], airport['Country'], round(distance,2)])
    print(x)

def printPath(path):
    x = PrettyTable(hrules=prettytable.ALL)
    x.field_names = ['Departure', 'Destination', 'Distance (km)']
    for trip in lt.iterator(path):
        x.add_row([trip['vertexA'], trip['vertexB'], trip['weight']])
    print(x)

def printAirport(airport):
   x = PrettyTable(hrules=prettytable.ALL)
   x.field_names = ["IATA", "Name", "City", "Country", "Latitude", "Longitude"]
   x._max_width = {'Name':20, 'City': 20, 'Country': 20}
   x.add_row([airport['IATA'], airport['Name'], airport['City'], airport['Country'], airport['Latitude'], airport['Longitude']])
   print(x)

def LoadData(cont):
    print("Cargando información de los aeropuertos ....")
    start = tm.process_time()
    controller.loadData(cont)
    end = tm.process_time()
    vertex = controller.totalAirperGraph(cont)
    edges = controller.totalConnectionsperGraph(cont)
    city = lt.size(cont['lt cities'])

    print("\n=== Airport-Routes DiGraph ===")
    print("Nodes/Vertex:", vertex[0], "loaded airports.")
    print("Edges:", edges[0], "loaded routes.")
    print("First & last Airport loaded in the DiGraph:")
    printFirstLastAirport(cont['lt airports'])

    print("\n=== Airport-Routes Graph ===")
    print("Nodes/Vertex:", vertex[1], "loaded airports.")
    print("Edges:", edges[1], "loaded routes.")
    print("First & last Airport loaded in the Graph:")
    printFirstLastAirport(cont['lt airports'])

    print("\n=== City Network ===")
    print("The number of cities are:", city)
    print("First & last City loaded in data structure:")
    printFirstLastCity(cont['lt cities'])
    total_time = (end - start)
    print("The time it took to execute the data load was:", total_time*1000 ,"mseg ->",total_time, "seg\n")
    

#Requerimientos
def Req1(cont):
    start = tm.process_time()
    airports=controller.AirInterconection(cont)
    top5 = controller.getFirst(airports, 5)
    print("="*15, "Req No. 1 Inputs", "="*15)
    print("Most connected airports in network (TOP 5) ")
    print("Number of airports in network:", lt.size(cont['lt airports']), "\n")

    print("="*15, "Req No. 1 Answer", "="*15)
    print('Connected airports inside network: ',lt.size(airports))
    print("TOP 5 most connected airports...")
    printAirInterconection(top5)
    end = tm.process_time()
    total_time = (end - start)
    print("The time it took to execute the requirement was:", total_time*1000 ,"mseg ->",total_time, "seg\n")
    #Req 1 (Bono)
    print("\n¿Quieres ejecutar el req 1 (Bono): Visualizar gráficamente los requerimientos? ")
    rta = input("(si/no): ").lower()
    if rta == "si":
        controller.Mapa(top5)

def Req2(cont):
    start = tm.process_time()
    air1 = input('Ingrese el IATA del aeropuerto 1: ').upper()
    air2 = input('Ingrese el IATA del aeropuerto 2: ').upper()
    airport = controller.AirCluster(cont, air1, air2)
    print("="*15, "Req No. 2 Inputs", "="*15)
    print("Airport-1 IATA Code:", air1)
    iata1 = controller.SearchbyIATA(cont, air1)
    printAirport(iata1)
    print("Airport-2 IATA Code:", air2)
    iata2 = controller.SearchbyIATA(cont, air2)
    printAirport(iata2)
    lista = lt.newList()
    lt.addLast(lista, iata1)
    lt.addLast(lista, iata2)
    print("="*15, "Req No. 2 Answer", "="*15)
    print("Number of SCC in Airport-Route network:", airport[0])
    print("Does Airport-1 & Airport-2 with IATA code", air1, "and", air2, "belong together?", airport[1])
    end = tm.process_time()
    total_time = (end - start)
    print("The time it took to execute the requirement was:", total_time*1000 ,"mseg ->",total_time, "seg\n")
    print("\n¿Quieres ejecutar el req 2 (Bono): Visualizar gráficamente los requerimientos? ")
    rta = input("(si/no): ").lower()
    if rta == "si":
        controller.Mapa(lista)

def Req3(cont):
    start = tm.process_time()
    depa_city = input('Ingrese la ciudad de origen: ')
    arriv_city = input('\nIngrese la ciudad de destino: ')

    arriv_cities = controller.SearchCity(cont, arriv_city.lower())
    depa_cities = controller.SearchCity(cont, depa_city.lower())
    departure = lt.firstElement(depa_cities)
    arrival = lt.firstElement(arriv_cities)

    if lt.size(depa_cities) > 1:
        print("Se encontraron", lt.size(depa_cities), "ciudades de origen con el mismo nombre")
        printCitiesSameName(depa_cities)
        num_depacity = int(input("Seleccione el numero de la ciudad que quiere consultar: "))
        departure = lt.getElement(depa_cities,num_depacity)

    if lt.size(arriv_cities) > 1:
        print("Se encontraron", lt.size(arriv_cities), "ciudades de destino con el mismo nombre")
        printCitiesSameName(arriv_cities)
        num_destcity = int(input("Seleccione el numero de la ciudad que quiere consultar: "))
        arrival = lt.getElement(arriv_cities,num_destcity)
        
    DepaNearAirport = controller.getNearestAirport(cont, departure)
    ArrNearAirport = controller.getNearestAirport(cont, arrival)

    DepaDistance = controller.getDistance(departure, DepaNearAirport)
    ArrDistance = controller.getDistance(arrival, ArrNearAirport)

    path = controller.getPath(cont, DepaNearAirport['IATA'], ArrNearAirport['IATA'])
    if path == None:
        print("\nNo existe una ruta entre los aeropuertos")
    else:
        totalDistance = controller.getDistancePath(cont, ArrNearAirport['IATA'])
        stops = controller.getStops(cont, path)

        print("="*15, "Req No. 3 Inputs", "="*15)
        print("Depature city:", depa_city)
        printCityInfo(departure)
        print("Arrival city:", arriv_city)
        printCityInfo(arrival)

        print("="*15, "Req No. 3 Answer", "="*15)
        print("+++ The departure airport in", depa_city, "is +++")
        printAirportCity(DepaNearAirport, DepaDistance)
        print("\n+++ The arrival airport in", arriv_city, "is +++")
        printAirportCity(ArrNearAirport, ArrDistance)

        print("\n+++ Dijkstra's Trip details +++")
        print(" - Total distance:", totalDistance, "(km)")
        print(" - Trip Path:")
        printPath(path)
        print(" -Trip Stops:")
        printAirports(stops)
        end = tm.process_time()
        total_time = (end - start)
        print("The time it took to execute the requirement was:", total_time*1000 ,"mseg ->",total_time, "seg\n")
        print("\n¿Quieres ejecutar el req 3 (Bono): Visualizar gráficamente los requerimientos? ")

        #Req 6 (Bono)
        print("\n¿Quieres ejecutar el req 6 (Bono): Comparar con servicio WEB externo? ")
        rta = input("(si/no): ").lower()
        if rta == "si":
            controller.Req6(departure, arrival, depa_city, arriv_city)
               

def Req4(cont): 
    start = tm.process_time()
    depa_city = input('Ingrese la ciudad de origen: ')
    depa_cities = controller.SearchCity(cont, depa_city.lower())
    departure = lt.firstElement(depa_cities)
    if lt.size(depa_cities) > 1:
        print("Se encontraron", lt.size(depa_cities), "ciudades de origen con el mismo nombre")
        printCitiesSameName(depa_cities)
        num_depacity = int(input("Seleccione el numero de la ciudad que quiere consultar: "))
        departure = lt.getElement(depa_cities,num_depacity)

    millas = float(input("Ingrese la cantidad de millas disponibles: "))

    DepaNearAirport = controller.getNearestAirport(cont, departure)
    DepaDistance = controller.getDistance(departure, DepaNearAirport)

    rta = controller.TravelerMiles(cont, millas, DepaNearAirport)

    print("="*15, "Req No. 4 Inputs", "="*15)
    print("Departure IATA code:", DepaNearAirport['IATA'])
    print("Available Travel Miles:",millas, "\n")

    print("="*15, "Req No. 4 Answer", "="*15)
    print("+++ Departure Airport for IATA code:", DepaNearAirport['IATA'], "+++")
    printAirportCity(DepaNearAirport, DepaDistance)
    print("\n- Number of possible airports:", rta[0])
    print("- Max traveling distance between airports:", round(rta[1],2), "(km).")
    print("- Passenger avalaible traveling kilometers:", round(millas*1.6,2), "(km).")
    print("\n+++ Longest possible route with airport", DepaNearAirport['IATA'], "+++")
    print("- Longest possible path distance:",round(rta[3]/2,2), "(km).")
    print("- Longest possible path details:")
    printPath(rta[2])
    print("-----")
    if rta[4] < 0:
        print("The passeenger needs", round(abs(rta[4]),2) , "kilometers to complete the trip.")
        print("The passeenger needs", round(abs(rta[4]/1.6),2) , "miles to complete the trip.")
    else:
        print("The passeenger has", round(abs(rta[4]),2) , "kilometers left after the trip.")
        print("The passeenger has", round(abs(rta[4]/1.6),2) , "miles left after the trip.")
    print("-----")
    end = tm.process_time()
    total_time = (end - start)
    print("The time it took to execute the requirement was:", total_time*1000 ,"mseg ->",total_time, "seg\n")

def Req5(cont):
    start = tm.process_time()
    airIata = input('Ingrese el IATA del aeropuerto fuera de servicio: ').upper()
    vertex = controller.totalAirperGraph(cont)
    edges = controller.totalConnectionsperGraph(cont)
    affected, routesDigraph, routesGraph = controller.OutOfService(cont, airIata)

    print("="*15, " Req No. 5 Inputs ", "="*15)
    print("Closing the airport with IATA code:", airIata)
    print("\n--- Airport-Routes DiGraph ---")
    print("Original number of Airports:", vertex[0], "and Routes:", edges[0])
    print("--- Airport-Routes Graph ---")
    print("Original number of Airports:", vertex[1], "and Routes:", edges[1])

    print("\n+++ Removing Airport with IATA:", airIata, "+++")
    print("\n--- Airport-Routes DiGraph ---")
    print("Resulting number of Airports:", vertex[0]-1, "and Routes:", edges[0]-routesDigraph)
    print("--- Airport-Routes Graph ---")
    print("Resulting number of Airports:", vertex[1]-1, "and Routes:", edges[1]-routesGraph, "\n")

    print("="*15, " Req No. 5 Answer ", "="*15)
    print("There are", lt.size(affected), "Airports affected by the removal of", airIata)
    if lt.size(affected) != 0:
        if lt.size(affected) > 6:
            print("The first & last 3 Airports affected are:")
            affected_air = controller.FirtsAndLast(controller.getFirst(affected, 3), controller.getLast(affected, 3))
            printAirports(affected_air)
        else:
            print("The affected Airports are:")
            printAirports(affected)
    
    #Req 7 (Bono)
    end = tm.process_time()
    total_time = (end - start)
    print("The time it took to execute the requirement was:", total_time*1000 ,"mseg ->",total_time, "seg\n")
    print("\n¿Quieres ejecutar el req 7 (Bono): Visualizar gráficamente los requerimientos? ")
    rta = input("(si/no): ").lower()
    if rta == "si":
        controller.Mapa(affected)

cont = None #catalog

"""
Menu principal
"""
def run():
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs[0]) == 1:
            cont = controller.initAnalyzer()
            LoadData(cont)
            
        elif int(inputs[0]) == 2:
            Req1(cont)

        elif int(inputs[0]) == 3:
            Req2(cont)

        elif int(inputs[0]) == 4:
            Req3(cont)

        elif int(inputs[0]) == 5:
            Req4(cont)

        elif int(inputs[0]) == 6:
            Req5(cont)

        else:
            sys.exit(0)
    sys.exit(0)

if __name__ == "__main__":
    threading.stack_size(67108864)
    sys.setrecursionlimit(2 ** 20)  
    thread = threading.Thread(target=run)
    thread.start()
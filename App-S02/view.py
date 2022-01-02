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
import controller
import queryAPI
import getAccessToken
from DISClib.ADT import list as lt
from DISClib.ADT.graph import gr
import threading
from DISClib.ADT import map as m
from DISClib.ADT import stack
from DISClib.DataStructures import mapentry as me
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de aeropuertos")
    print('3- Encontrar puntos de interconexión aérea')
    print('4- Encontrar clústeres de tráfico aéreo')
    print('5- Encontrar la ruta más corta entre ciudades')
    print('6- Utilizar las millas de viajero')
    print('7- Cuantificar el efecto de un aeropuerto cerrado')
    print('8- Comparar con servicio WEB externo')
    print('0- Salir')


catalog = None

def printReq1(respuesta):
    print("Aeropuertos que sirven como punto de interconexión a más rutas aereas")
    print("Grafo Dirigido: A continuación se muestra el TOP 5\n")
    first5 = lt.subList(respuesta[0],1,5)
    for i in lt.iterator(first5):
        print('Aeropuerto: ' + i['Aeropueto'] + ', Ciudad: ' + i['Ciudad'] + ', País: ' + i['Pais'] + ', IATA: ' + i['IATA'] + ', Total Conexiones: ' + str(i['TotalConnections'])  + '\n')
    
    
    print("Grafo No Dirigido: A continuación se muestra el TOP 5\n")
    first_5 = lt.subList(respuesta[1],1,5)
    for i in lt.iterator(first_5):
        print('Aeropuerto: ' + i['Aeropueto'] + ', Ciudad: ' + i['Ciudad'] + ', País: ' + i['Pais'] + ', IATA: ' + i['IATA'] + ', Total Conexiones: ' + str(i['TotalConnections'])  + '\n')
    #print(lt.isPresent(respuesta[1],{'Aeropuerto': 'VLD', 'TotalConnections': 1}))
    #print(lt.getElement(respuesta[1],3291))

def printReq2(total_clusters, aeropuertos_mismo, IATA1, IATA2):

    print('El número total de clusters dentro de la red de tráfico aéreo encontrados es de ' + str(total_clusters) + ' clusters.\n')
    
    if aeropuertos_mismo == True :

        print('El aeropuerto identificado por el IATA ' + str(IATA1) + ' y el identificado por el IATA ' + str(IATA2) + ' SI pertenecen al mismo cluster.')

    else:

        print('El aeropuerto identificado por el IATA ' + str(IATA1) + ' y el identificado por el IATA ' + str(IATA2) + ' NO pertenecen al mismo cluster.')

def printReq3(analyzer, ruta, distancia_total, aero_origen, aero_destino):

    aero_origen_entry = m.get(analyzer['AirportIATAS'], aero_origen)
    aero_origen_info = me.getValue(aero_origen_entry)
    aero_destino_entry = m.get(analyzer['AirportIATAS'], aero_destino)
    aero_destino_info = me.getValue(aero_destino_entry)

    print('A continuación se muestran los aeropuertos de origen y destino respectivamente y su información: \n')

    print('IATA: ' + aero_origen_info['IATA'] + ', Nombre: ' + aero_origen_info['Name'] + ', Ciudad: ' + aero_origen_info['City'] + ', Pais: ' + aero_origen_info['Country'])
    print('IATA: ' + aero_destino_info['IATA'] + ', Nombre: ' + aero_destino_info['Name'] + ', Ciudad: ' + aero_destino_info['City'] + ', Pais: ' + aero_destino_info['Country'] + '\n')

    print('La ruta más corta hallada entre ambos aeropuertos es de ' + str(distancia_total) + ' km. \n')
    print('A continuación se mostrará la ruta tomada con sus respectivas paradas y distancias parciales: \n')

    for trayecto in lt.iterator(ruta):
        print('Origen: ' + trayecto['vertexA'] + ', Destino: ' + trayecto['vertexB'] + ', Distancia (km): ' + str(trayecto['weight']))

def printReq4(respuesta, origen, millas):

    print("Dado la ciudad de origen " + origen+ " y un total de "+str(millas)+ " millas. Se encontró que: \n")
    print("Número de posibles aeropuertos: " + str(respuesta[0]))
    print("Suma de la distanca de viaje entre aeropuertos [km]: " + str(respuesta[1]))
    print("Camino más largo posible (ida y vuelta): " + str(respuesta[2]))
    print('\n')
    print("Distancia del camino más largo posible [Km]: " + str(respuesta[4]))

    if respuesta[3] > 0:
        print("La cantidad de millas excedentes o que no se usaron según la distancia total recomendada es: " + str(abs(respuesta[3]))+ "\n")
    elif respuesta[3] < 0:
        print("La cantidad de millas faltantes o que se necesitan de más según la distancia total recomendada es: " + str(abs(respuesta[3]))+ "\n")
    elif respuesta[3] == 0:
        print("La cantidad de millas según la distancia total recomendada es exacta"+ "\n")

def printReq5(analyzer, lista, tamano, IATA):

    print('Si el aeropuerto identificado con el código IATA ' + str(IATA) + ' se encontrara fuera de servicio, ' + str(tamano) + ' aeropuertos se verían afectados.\n')

    print('A continuación se presenta la lista de los primeros 3 y últimos 3 aeropuertos que se verían afectados: ')

    if tamano > 6:
        first3 = lt.subList(lista, 1, 3)
        last3 = lt.subList(lista, tamano-2 , 3)

        for airport in lt.iterator(first3):
            entry = m.get(analyzer['AirportIATAS'], airport)
            value = me.getValue(entry)
            print('Nombre: ' + value['Name'] + ', Ciudad: ' + value['City'] + ', IATA: ' + value['IATA'])

        for airport in lt.iterator(last3):
            entry = m.get(analyzer['AirportIATAS'], airport)
            value = me.getValue(entry)

            print('Nombre: ' + value['Name'] + ', Ciudad: ' + value['City'] + ', IATA: ' + value['IATA'])

    else:
        
        for airport in lt.iterator(lista):
            entry = m.get(analyzer['AirportIATAS'], airport)
            value = me.getValue(entry)

            print('Nombre: ' + value['Name'] + ', Ciudad: ' + value['City'] + ', IATA: ' + value['IATA'])

    print('\n')


"""
Menu principal
"""


def thread_cycle():
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs[0]) == 1:
            print("Inicializando ....")

            analyzer = controller.init()

        elif int(inputs[0]) == 2:

            print('Cargando información de aeropuertos en el mundo...') 

            controller.loadData(analyzer)

            clusters = controller.getcluster(analyzer)
            cluster_num = controller.getClusterNum(clusters)

            num_airportsD = gr.numVertices(analyzer['AirportRoutesD'])
            num_airportsND = gr.numVertices(analyzer['AirportRoutesND'])

            print('Total de vértices del grafo dirigido: ' + str(num_airportsD))
            print('Total de vértices del grafo no dirigido: ' + str(num_airportsND) + '\n')

            num_routesD = gr.numEdges(analyzer['AirportRoutesD'])
            num_routesND = gr.numEdges(analyzer['AirportRoutesND'])

            print('Total de arcos del grafo dirigido: ' + str(num_routesD))
            print('Total de arcos del grafo no dirigido: ' + str(num_routesND) + '\n')

        
            num_ciudades = lt.size(analyzer['Cities_lst'])

            print('Total de ciudades cargadas: ' + str(num_ciudades) + '\n')

            airport_size = lt.size(analyzer['airport_lst'])
            airportfirst = lt.getElement(analyzer['airport_lst'],1)
            airportlast = lt.getElement(analyzer['airport_lst'],airport_size)
          

            print('\nA continuación se muestra la información del primer y último aeropuerto cargado tanto para el grafo dirigido como el no dirigido: \n')

            print('Nombre: ' + airportfirst['Name'] + ', Ciudad: ' + airportfirst['City'] + ', Pais: ' + airportfirst['Country'] + ', Latitud: ' + airportfirst['Latitude'] + ', Longitud: ' + airportfirst['Longitude'] )
            print('Nombre: ' + airportlast['Name'] + ', Ciudad: ' + airportlast['City'] + ', Pais: ' + airportlast['Country'] + ', Latitud: ' + airportlast['Latitude'] + ', Longitud: ' + airportlast['Longitude'] )

            city_first = lt.getElement(analyzer['Cities_lst'], 1)
            city_last = lt.getElement(analyzer['Cities_lst'], num_ciudades)

            print('\nA continuación se muestra la información de la primera y última ciudad cargada:')

            print('Nombre: ' + city_first['city'] + ', Población: ' + city_first['population'] + ', Latitud: ' + city_first['lat'] + ', Longitud: ' + city_first['lng'])
            print('Nombre: ' + city_last['city'] + ', Población: ' + city_last['population'] + ', Latitud: ' + city_last['lat'] + ', Longitud: ' + city_last['lng']+'\n')


        elif int(inputs[0]) == 3:

            'Requerimiento 1: interconecciones'

            respuesta = controller.getInterconnections(analyzer)
            printReq1(respuesta)
        
        
        elif int(inputs[0]) == 4:

            'Requerimiento 2: clusters de tráfico aéreo'

            IATA1 = input('Primer aeropuerto a consultar (código IATA): ')
            IATA2 = input('Segundo aeropuerto a consultar (código IATA): ')

            cluster_con = controller.getTraficClustersCon(clusters, IATA1, IATA2)

            printReq2(cluster_num,cluster_con, IATA1, IATA2)

        
        elif int(inputs[0]) == 5:

            'Requerimiento 3: Encontrar la ruta más corta entre ciudades'

            origen = input('Escoja la ciudad de origen: ')

            ciudades_o = controller.getCities(analyzer, origen)

            if lt.size(ciudades_o) > 1:

                print('Se encontraron los siguientes códigos de ciudades con el mismo nombre que usted seleccionó: ')

                for ciudad in lt.iterator(ciudades_o):

                    print(ciudad['city']+', '+ ciudad['country'] + ', ' + ciudad['lat'] + ', ' + ciudad['lng'] + ', ' + ciudad['id'])

                ciudad_o_codigo = input('De las anteriores ciudades, seleccione el código de la que quiere como ciudad de origen: ')

            else:

                ciudad_o_codigo = ciudades_o['elements'][0]['id']

            airport_origin = controller.ClosestairportCity(analyzer,ciudad_o_codigo)

            dijkstra_airport_ori = controller.DijkstraAirport(analyzer, airport_origin)
            
            destino = input('Escoja la ciudad de destino: ')

            ciudades_d = controller.getCities(analyzer, destino)

            if lt.size(ciudades_d) > 1:

                print('Se encontraron los siguientes códigos de ciudades con el mismo nombre que usted seleccionó: ')
                for ciudad in lt.iterator(ciudades_d):

                    print(ciudad['city']+', '+ ciudad['country'] + ', ' + ciudad['lat'] + ', ' + ciudad['lng'] + ', ' + ciudad['id'])

                ciudad_d_codigo = input('De las anteriores ciudades, seleccione el código de la que quiere como ciudad de destino: ')
            else:

                ciudad_d_codigo = ciudades_d['elements'][0]['id']


            airport_destination = controller.ClosestairportCity(analyzer,ciudad_d_codigo)


            respuesta = controller.getShortestRoute(dijkstra_airport_ori, airport_destination)

            if respuesta == None:

                print('No se encontró ruta entre los aeropuertos encontrados como más cercanos los cuales son, Origen: ' + str(airport_origin) + ', Destino: ' + str(airport_destination) ) 

            else:    
                printReq3(analyzer, respuesta[0],respuesta[1], airport_origin, airport_destination)


        elif int(inputs[0]) == 6:

            'Requerimiento 4: Utilizar las millas de viajero'
        
            origen= input("Ingrese la ciudad de origen: ")
            millas = int(input("Ingrese cantidad millas disponibles: "))
            distancia = millas
            ####3
            ciudades_o = controller.getCities(analyzer, origen)

            if lt.size(ciudades_o) > 1:

                print('Se encontraron los siguientes códigos de ciudades con el mismo nombre que usted seleccionó: ')

                for ciudad in lt.iterator(ciudades_o):

                    print(ciudad['city']+', '+ ciudad['country'] + ', ' + ciudad['lat'] + ', ' + ciudad['lng'] + ', ' + ciudad['id'])

                ciudad_o_codigo = input('De las anteriores ciudades, seleccione el código de la que quiere como ciudad de origen: ')

            else:

                ciudad_o_codigo = ciudades_o['elements'][0]['id']

            airport_origin = controller.ClosestairportCity(analyzer,ciudad_o_codigo)
            ######
            respuesta = controller.planViajero(analyzer, airport_origin, distancia)

            printReq4(respuesta, origen, millas)


        elif int(inputs[0]) == 7:

            'Requerimiento 5: Cuantificar el efecto de un aeropuerto cerrado'

            IATA = input('Ingrese el código IATA del aeropuerto a consultar: ')

            afectados = controller.getAffectedAirports(analyzer, IATA)

            printReq5(analyzer, afectados[0], afectados[1], IATA)

        elif int(inputs[0]) == 8:

            'Requerimiento 6: Comparar con servicio WEB externo'

            getAccessToken.accestoken()

            city_origin = input('Ingrese la ciudad de origen que desea: ')

            ciudades_o = controller.getCities(analyzer, city_origin)

            if lt.size(ciudades_o) > 1:

                print('Se encontraron los siguientes códigos de ciudades con el mismo nombre que usted seleccionó: ')

                for ciudad in lt.iterator(ciudades_o):

                    print(ciudad['city']+', '+ ciudad['country'] + ', ' + ciudad['lat'] + ', ' + ciudad['lng'] + ', ' + ciudad['id'])

                ciudad_o_codigo = input('De las anteriores ciudades, seleccione el código de la que quiere como ciudad de origen: ')

            else:

                ciudad_o_codigo = ciudades_o['elements'][0]['id']

            origen_latsylons = controller.Req6City(ciudad_o_codigo, analyzer)

            token = input('Ingrese el access token: ')

            queryAPI.Req6ClosestAirport( token,origen_latsylons[0], origen_latsylons[1])

            iata_O = input('Ingrese el código IATA del aeropuerto más cercano y más relevante: ')

            dijkstra_airport_o = controller.DijkstraAirport(analyzer, iata_O)

            city_destiny = input('Ingrese ciudad de destino que desea: ')

            ciudades_d = controller.getCities(analyzer, city_destiny)

            if lt.size(ciudades_d) > 1:

                print('Se encontraron los siguientes códigos de ciudades con el mismo nombre que usted seleccionó: ')
                for ciudad in lt.iterator(ciudades_d):

                    print(ciudad['city']+', '+ ciudad['country'] + ', ' + ciudad['lat'] + ', ' + ciudad['lng'] + ', ' + ciudad['id'])

                ciudad_d_codigo = input('De las anteriores ciudades, seleccione el código de la que quiere como ciudad de destino: ')
            else:

                ciudad_d_codigo = ciudades_d['elements'][0]['id']

            destination_latsylons = controller.Req6City(ciudad_d_codigo, analyzer)

            queryAPI.Req6ClosestAirport(token,destination_latsylons[0], destination_latsylons[1])

            iata_D = input('Ingrese el código IATA del aeropuerto más cercano y más relevante: ')

            respuesta = controller.getShortestRoute(dijkstra_airport_o, iata_D)

            printReq3(analyzer, respuesta[0],respuesta[1], iata_O, iata_D)


            

        elif int(inputs[0]) == 0:
            sys.exit(0)
            
        else:
            sys.exit(0)
    sys.exit(0)

if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()

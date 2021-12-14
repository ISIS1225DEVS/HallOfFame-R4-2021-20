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
import threading
from DISClib.ADT import stack
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

airportsfile = 'Skylines/airports-utf8-small.csv'
routesfile = 'Skylines/routes-utf8-small.csv'
citiesfile = 'Skylines/worldcities-utf8.csv'

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Encontrar puntos de interconexion")
    print("3- Encontrar clústeres de trafico aereo")
    print("4- Encontrar la ruta mas corta entre ciudades")
    print("5- Utilizar las millas de viajero")
    print("6- Cuantificar el efecto de un aeropuerto cerrado")
    print("7- Comparar con servicio web externo")

catalog = None

"""
Menu principal
"""
def thread_cycle():
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs[0]) == 1:
            print("Cargando información de los archivos ....")
            cont = controller.init()
            #cargar datos
            print("\nCargando información ....\n")
            (cont,c) = controller.loadServices(cont, airportsfile, routesfile, citiesfile)
            print("\n---GRAFO DIRIGIDO---\n")
            print("El número total de aeropuertos es: " + str(controller.totalAirports(cont)))
            print("El número total de rutas es: " + str(controller.totalRoutesUnicas(cont)))
            print("La información del primer aeropuerto cargado es: " + str(controller.infoPrimerAeropuerto(cont)))
            print("La información de la última ciudad cargada es: " + str(controller.infoUltimaCiudad(cont)))
            print("\n---GRAFO NO DIRIGIDO---\n")
            print("El número total de aeropuertos es: " + str(controller.totalAirports2(cont)))
            print("El número total de rutas es: " + str(controller.totalRoutesDobles(cont)))
            print("La información del primer aeropuerto cargado es: " + str(controller.infoPrimerAeropuerto(cont)))
            print("La información del ultimo aeropuerto cargado es: " + str(controller.infoUltimoAeropuerto(cont)))
            print("\n---CIUDADES---\n")
            print("El número total de ciudades es: " + str(controller.totalCities(cont)))
            print("La información de la primera ciudad cargada es: " + str(controller.infoPrimeraCiudad(cont)))
            print("La información de la última ciudad cargada es: " + str(controller.infoUltimaCiudad(cont))+"\n")

        elif int(inputs[0]) == 2:
            print("\nCargando aeropuertos más conectados...\n")
            num, lista = controller.req_1(cont)
            i = 0
            for a in lt.iterator(lista):
                if i < 5:
                    print("IATA : " + a["IATA"] + " - Nombre : " + a["Name"] + " - Ciudad : " + a["City"] +
                        " - Pais : "+ a["Country"] + " - Numero Rutas : " + str(a["num_routes"]))
                i += 1
            print("\nEstos son los aeropuertos interconectados. En total son " + str(num) +"\n")

        elif int(inputs[0]) == 3:
            print("\nCargando aeropuertos más conectados...\n")
            a1 = input("Ingrese el primer aeropuerto de interés: ")
            a2 = input("Ingrese el segundo aeropuerto de interés: ")
            num, mismo = controller.req_2(cont, a1, a2)
            print("\nEn total hay " + str(num) + " clústeres.")
            if mismo == True:
                print(a1 + " y " + a2 + " sí están en el mismo clúster\n")
            else:
                print(a1 + " y " + a2 + " no están en el mismo clúster\n")

        elif int(inputs[0]) == 4:
            ciudad_or = input("Introduzca la ciudad de origen: ")
            lista_ciudades = controller.ciudades_homonimas(cont, ciudad_or)
            i=1
            for ciudad in lt.iterator(lista_ciudades):
                print(str(i) + ". " + str(ciudad))
                i +=1
            a = input("Seleccione ciudad de origen: ")
            ciudad_des = input("Introduzca la ciudad de destino: ")
            lista_ciudades = controller.ciudades_homonimas(cont, ciudad_des)
            i=1
            for ciudad in lt.iterator(lista_ciudades):
                print(str(i) + ". " + str(ciudad))
                i +=1
            b = input("Seleccione ciudad de destino: ")
            (origen, destino, camino_minimo, distancia_tot) = controller.req_3(cont, ciudad_or, ciudad_des, a, b)
            print("El aeropuerto de origen es: " + origen["IATA"] + " - " + origen["Name"] + " en " + origen["City"] + "(" + origen["Country"] + ")")
            print("El aeropuerto de destino es: " + destino["IATA"] + " - " + origen["Name"] + " en " + destino["City"] + "(" + destino["Country"] + ")")
            print("El recorrido que se hace es: \n")
            for t in lt.iterator(camino_minimo):
                print(t["vertexA"] + " - " + t["vertexB"] + " - " + str(t["weight"]) + "\n")
            print("La distancia total recorrida fue: " + str(distancia_tot))

        elif int(inputs[0]) == 5:
            iata = input("Ingrese el IATA del aeropuerto de salida: ")
            millas = float(input("Ingrese el numero de millas disponibles: "))
            (distancia_max, lista_ruta, distancia_tot, alcanza, dif_millas, distancia_km, num_aeropuertos) = controller.req_4(cont, iata, millas)
            print("\nNumero de aeropuertos en la ruta: " + str(num_aeropuertos))
            print("Distancia total de todas las rutas (km): " + str(distancia_max))
            print("Distancia en km equivalente a las millas: " + str(distancia_km))
            print("Distancia de la ruta más larga: " + str(distancia_tot))
            print("\nDetalles de la ruta más larga: ")
            for d in lt.iterator(lista_ruta):
                print(d)
            if alcanza:
                print("\nEl pasajero puede completar el viaje y le sobran " + str(dif_millas) + " millas.")
            else:
                print("\nEl pasajero necesita " + str(dif_millas) + " millas para completar el viaje.\n")

        elif int(inputs[0]) == 6:
            aer = input("Digite el IATA del aeropuerto cerrado: ")
            print("\n---GRAFO DIRIGIDO---\n")
            print("El número original de aeropuertos es: " + str(controller.totalAirports(cont)))
            print("El número original de rutas es: " + str(controller.totalRoutesUnicas(cont)))
            print("\n---GRAFO NO DIRIGIDO---\n")
            print("El número original de aeropuertos es: " + str(controller.totalAirports2(cont)))
            print("El número original de rutas es: " + str(controller.totalRoutesDobles(cont)))
            print("\n\nEliminando el aeropuerto con IATA " + aer + "...\n\n")
            (cont, num_afectados, lista) = controller.req_5(cont, aer)
            print("\n---GRAFO DIRIGIDO---\n")
            print("El número resultante de aeropuertos es: " + str(controller.totalAirports(cont)))
            print("El número resultante de rutas es: " + str(controller.totalRoutesUnicas(cont)))
            print("\n---GRAFO NO DIRIGIDO---\n")
            print("El número resultante de aeropuertos es: " + str(controller.totalAirports2(cont)))
            print("El número resultante de rutas es: " + str(controller.totalRoutesDobles(cont)))
            print("\n" + str(num_afectados) + " aeropuertos fueron afectados.\n")
            print("A continuacion los primeros y ultimos 3 aeropuertos afectados: \n")
            for a in lt.iterator(lista):
                print(a)
        else:
            sys.exit(0)


if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()
        
sys.exit(0)

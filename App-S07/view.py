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

from math import dist
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from time import process_time
import prettytable
from prettytable import PrettyTable
from IPython.display import display
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

# ___________________________________________________
#  Variables
# ___________________________________________________

aeropuertosfile="airports_full.csv"
rutasfile="airports_full.csv"
ciudadesfile="worldcities.csv"
catalog = None

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("Bienvenido")
    print("0- Cargar información en el catálogo")
    print("1- Encontrar puntos de interconexión aérea")
    print("2- Encontrar clústeres de tráfico aéreo")
    print("3- Encontrar la ruta más corta entre ciudades")
    print("4- Utilizar las millas de viajero")
    print("5- Cuantificar el efecto de un aeropuerto cerrado")
    print("6- Comparar con servicio WEB externo")
    print("7- Visualizar gráficamente las respuestas anteriores")
    print("8- Salir")


def initCatalog():
    """

    """
    return controller.initCatalog()

def printInput(requerimiento,tipo):
    if tipo=="Input":
        print("-"*14 + "Requerimiento "+str(requerimiento)+" " + tipo+"s"+"-"*14)
    elif tipo=="Resultado":
        print("\n"+"-"*12 + "Requerimiento "+str(requerimiento)+" " + tipo+"s"+"-"*12)

def printPrettyTable(lista, keys, field_names, max_width, sample=3, ultimas=False):
    artPretty=PrettyTable(hrules=prettytable.ALL)
    artPretty.field_names=field_names
    artPretty._max_width = max_width

    cont=1

    for elemento in lt.iterator(lista):
        valoresFila=[]
        for key in keys:
            valoresFila.append(elemento[key])
        artPretty.add_row(tuple(valoresFila))
        if cont>=sample:
            break
        cont+=1
    
    if ultimas:
        ultimo_index=lt.size(lista) # aRRAY LIST
        cont2=1
        while cont2<=sample:
            indice=ultimo_index-sample+cont2
            if indice>cont and indice>=0 and lt.size(lista)>=indice:
                elemento=lt.getElement(lista,indice)
                valoresFila=[]
                for key in keys:
                    valoresFila.append(elemento[key])
                artPretty.add_row(valoresFila)
            cont2+=1
    
    print(artPretty)

def printAeropuertos(respuesta):
    keys=["Name","City","Country","IATA", "Latitude","Longitude"]
    fieldNames=["Name","City","Country","IATA", "Latitude","Longitude"]
    maxWidth = {"Name":20,"City":20,"Country":15,"IATA":6,"Latitude":10, "Longitude":10}
    printPrettyTable(respuesta,keys,fieldNames,maxWidth,sample=lt.size(respuesta),ultimas=False)

def printConexiones(respuesta):
    totalAeropuertosConectados=catalog["AeropuertosRutasGraph"]["AeropuertosConConexion"]
    print("\nLa cantidad de aeropuertos que están conectados en el aeropuerto son: "+str(totalAeropuertosConectados))

    print("\nEl top 5 de aeropuertos conectados son: \n")

    keys=["Name","City","Country","IATA","connections", "inbound","outbound"]
    fieldNames=["Name","City","Country","IATA","Connections", "Inbound","Outbound"]
    maxWidth = {"Name":20,"City":20,"Country":15,"IATA":6,"Connections":5, "Inbound":5,"Outbound":5}
    printPrettyTable(respuesta,keys,fieldNames,maxWidth,sample=5,ultimas=False)

###REQ 2###
def printCluster(respuesta,aeropuerto1,aeropuerto2):
    nComponentes=respuesta[0]
    aeropuertosPertenecen=respuesta[1]
    print("El número de componentes fuertemente conectados es: "+str(nComponentes))
    print("Los aeropuertos con código IATA: "+aeropuerto1 +" y "+aeropuerto2 + 
        " pertenecen al mismo componente? : "+aeropuertosPertenecen)

###REQ 3###
def printMenuCiudad(respuesta):
    ciudadRepetida=respuesta[0]
    listaCiudades=respuesta[1]
    sizeCiudades=listaCiudades["size"]

    if ciudadRepetida==0:
        print("El nombre de la ciudad buscada no existe")
    elif ciudadRepetida==1:
        print("La ciudad existe. La información de la ciudad es la siguiente: ")
    elif ciudadRepetida==2:
        print("Hay ",sizeCiudades," ciudades con este nombre.")
        print("La información de las ciudades es la siguiente: ")
        #print("Por favor seleccione la ciudad que desea: ")
    printTablaCiudades(listaCiudades)

def printTablaCiudades(listaCiudadesPrev):
    if "opcion" not in listaCiudadesPrev:
        listaCiudadesPrev["opcion"]=0
    
    if "size" not in listaCiudadesPrev:
        listaCiudades=lt.newList("ARRAY_LIST")
        lt.addLast(listaCiudades,listaCiudadesPrev)
    else:
        if "opcion" not in lt.getElement(listaCiudadesPrev,1):
            for city in lt.iterator(listaCiudadesPrev):
                city["opcion"]=0
            listaCiudades=listaCiudadesPrev
        else:
            listaCiudades=listaCiudadesPrev
    sizeCiudades=listaCiudades["size"]
    keys=["opcion","city","capital","lat","lng", "country"]
    fieldNames=["opcion","city","capital","lat","lng", "country"]
    maxWidth = {"opcion":3,"city": 20,"capital":20,"lat":10,"lng":10,"country":15}
    printPrettyTable(listaCiudades,keys,fieldNames,maxWidth,sample=sizeCiudades,ultimas=False)

def printEscogerCiudad(tipoCiudad):
    inputCiudad="Ingrese el nombre de la ciudad de "+tipoCiudad +":  "
    ciudadOr=input(inputCiudad) #Springfield
    resultadoCiudad=controller.buscarCiudad(catalog,ciudadOr)

    printMenuCiudad(resultadoCiudad)
    ciudadRepetida=resultadoCiudad[0]
    ciudadLista=resultadoCiudad[1]
    if ciudadRepetida>0:
        continuar=True
        if lt.size(ciudadLista)>1:
            posicion=int(input("Escoga que ciudad de "+tipoCiudad+" desea elegir. \nIngrese el número de la ciudad de la columna opción: "))
            ciudadOrigen=controller.coordenadasCiudad(catalog,ciudadOr,posicion)
        else:
            ciudadOrigen=controller.coordenadasCiudad(catalog,ciudadOr,pos=1)
        
        print("Información ciudad "+tipoCiudad+" elegida: \n")
        printTablaCiudades(ciudadOrigen[0])
    else:
        continuar=False
        ciudadOrigen=None
    
    return continuar,ciudadOrigen[1],ciudadOrigen[0],ciudadOrigen[2]


def printAeropuertosR3(aeropuerto1,aeropuerto2,distancia1,distancia2):
    print("*"*50)
    print("El aeropuerto de origen será: ",aeropuerto1,"Con una distancia a la ciudad de: ",distancia1)
    #Hacer pretty table
    print("El aeropuerto de salida será: ",aeropuerto2,"Con una distancia a la ciudad de: ",distancia2)
    print("*"*15+"RESULTADOS"+"*"*15)
    pass

# PRINT REQ 4

def printMstMillasViajero(res,millas_usuario):
    res_simple, millas_simple, ret, millas_cam, info = res
    print("Información del aeropuerto de partida:")
    kmUsuario=float(millas_usuario)*1.6
    lista=lt.newList()
    lt.addLast(lista,info)
    printPrettyTable(lista,['IATA','Name','City','Country'],['IATA','Nombre','Ciudad','Pais'],{'IATA':10,'Name':30,'City':20,'Country':20})
    print("\n\nDistancia de ruta más corta:",round(millas_cam,2))
    print("Suma de distancia de todos los aeropuertos desde origne:",round(millas_simple,2))
    print("Distancia en kilometros de millas:",round(kmUsuario,2))

    print("\n\n----- Ruta con mayor cantidad de paradas -------")
    printPrettyTable(ret,['vertexA','vertexB','weight'],['Origen','Destino','Distancia [km]'],{'vertexA':20,'vertexB':20,'weight':20},sample=lt.size(ret))
    print("El pasajero le quedan faltando (-) o sobrando (+)) millas",round((kmUsuario-millas_cam)/2,2),"millas para completar el viaje")

    print("\n\n----- Ruta propuesta enunciado -------")
    printPrettyTable(res_simple,['vertexA','vertexB','weight'],['Origen','Destino','Distancia [km]'],{'vertexA':20,'vertexB':20,'weight':20},sample=lt.size(res_simple))
    print("El pasajero le quedan faltando (-) o sobrando (+)) millas",round((kmUsuario-millas_simple)/1.6,2),"millas para completar el viaje")
    
    print

def printRutaMasCorta(resultado,opcion=3):
    if opcion==3:
        distCorta=resultado[0]
        print("La distancia total es: "+str(distCorta))
        ruta=resultado[1]
        paradas=resultado[2]
    elif opcion==6: #BONO API
        IATA1,IATA2,distancia1,distancia2,camino=resultado
        print("El aeropuerto de origen es: ",IATA1," El cual posee una distancia hacía la ciudad de: ",distancia1)
        print("El aeropuerto de llegada es: ",IATA2," El cual posee una distancia hacía la ciudad de: ",distancia2)
        ruta=camino[1]
        paradas=camino[2]
        print(ruta)
   
    print("La ruta es: ")
    keys=["lineaA","vertexA","vertexB","weight"]
    fieldNames=["Aerolínea","Origen","Destino","Distancia KM"]
    maxWidth = {"Aerolínea":5,"Origen":10,"Destino":10,"Distancia KM":10}
    printPrettyTable(ruta,keys,fieldNames,maxWidth,sample=lt.size(ruta),ultimas=False)
    printParadas(paradas)

def printParadas(resultado):
    listaParadas=resultado
    print("Las paradas son: ")
    keys=["IATA","Name","City","Country"]
    fieldNames=["IATA","Name","City","Country"]
    maxWidth = {"IATA":8,"Name":20,"City":20,"Country":20}
    printPrettyTable(listaParadas,keys,fieldNames,maxWidth,sample=lt.size(listaParadas),ultimas=False)

def printAeropuertosAfectados(resultado,aeropuerto):
    print("*"*50)
    print("Aeropuertos y rutas en grado dirigido ('AeropuertosRutasGraph')")
    print("Número original de rutas de aeropuertos: ",catalog["AeropuertosRutasGraph"]['vertices']["size"],
            "y rutas: ",catalog["AeropuertosRutasGraph"]['edges'])
    print("*"*50)
    print("Aeropuertos y rutas en grado no dirigido ('AeropuertosRutasDoblesGraph')")
    print("Número original de rutas de aeropuertos: ",catalog["AeropuertosRutasDoblesGraph"]['vertices']["size"],
            "y rutas: ",catalog["AeropuertosRutasDoblesGraph"]['edges'])
    
    print("\n\n"+"*"*15+"Rutas Aéreas después de la afectación........"+"*"*15)
    respuestaLista,dirigido,nodirigido=resultado
    print("*"*50)
    print("Aeropuertos y rutas en grado dirigido ('AeropuertosRutasGraph')")
    print("Número afectado de rutas de aeropuertos: ",catalog["AeropuertosRutasGraph"]['vertices']["size"],
            "y rutas: ",catalog["AeropuertosRutasGraph"]['edges']-dirigido)
    print("*"*50)
    print("Aeropuertos y rutas en grado no dirigido ('AeropuertosRutasDoblesGraph')")
    print("Número afectado de rutas de aeropuertos: ",catalog["AeropuertosRutasDoblesGraph"]['vertices']["size"],
            "y rutas: ",catalog["AeropuertosRutasDoblesGraph"]['edges']-nodirigido)
    print("En total hay ",lt.size(respuestaLista)," aeropuertos afectados con la remoción de ",aeropuerto)
    print("Los aeropuertos afectados son los siguientes: ")
    printAeropuertos(respuestaLista)



def infoCargaCatalogo():
    print("\n"+"*"*50)

    print("*"*10+"Información mapas"+"*"*10)
    print("Total de ciudades cargadas: ",catalog["CiudadesTabla"]["TotalCiudadesCargadas"])
    print("Total de ciudades con nombre único: ",catalog["CiudadesTabla"]["size"])
    print("Total de ciudades homónimas: ",catalog["CiudadesTabla"]["CiudadesHom"])
    print("Tamaño de mapa AeropuertosTabla: ",catalog["AeropuertosTabla"]["size"])

    print("*"*10+"Información grafos:"+"*"*10)
    #print("--- POR IMPLEMENTAR")
    try:
        vertices=catalog["AeropuertosRutasGraph"]['vertices']["size"]
        arcos=catalog["AeropuertosRutasGraph"]['edges']
        print("Grafo AeropuertosRutasGraph (Dirigido)"+" |Aeropuertos: " +str(vertices)+ " - total de rutas aéreas: "+ str(arcos))
    
    except:
        print("Error al obtener los vértices y/o arcos del grafo: AeropuertosRutasGraph ")

    
    try:
        #print(catalog["AeropuertosRutasDoblesGraph"].keys())
        vertices1=catalog["AeropuertosRutasDoblesGraph"]['vertices']["size"]
        arcos1=catalog["AeropuertosRutasDoblesGraph"]['edges']
        print("Grafo AeropuertosRutasDoblesGraph (No dirigido)"+" |Aeropuertos: " +str(vertices1)+ " - total de rutas aéreas: "+ str(arcos1))
    
    except:
        print("Error al obtener los vértices y/o arcos del grafo: AeropuertosRutasDoblesGraph")
    
    #print(catalog["AeropuertosRutasDoblesGraph"])
    
    print("-"*40)
    print("\n"+"*"*10+"FIN Información mapas y grafos"+"*"*10)
    print("*"*50)

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    
    if inputs!="0" and inputs!="8":
        printInput(inputs,"Input")

    print("\n")
    tiempoInicial=process_time()
    if int(inputs[0]) == 0:
        catalog=controller.initCatalog()

        info=controller.loadServices(catalog)
        infoCargaCatalogo()
        ultimaCiudadCargada=info[2]
        aeropuerto=info[1]
        #el primer aeropuerto es cargado a ambos grafos debido a la implementación que hicimos del model
        print("Aeropuerto aleatorio cargado en ambos grafos: \n")
        printAeropuertos(aeropuerto)
        print("\n Ciudad aleatoria cargada a la tabla de simbolos: \n")
        printTablaCiudades(ultimaCiudadCargada)

    elif int(inputs[0]) == 1:
        resultado=controller.puntosInterconexion(catalog)
        printConexiones(resultado)
        print(resultado)
        display(controller.bonoRequerimiento1(resultado))
        pass

    elif int(inputs[0]) == 2:
        aeropuerto1=input("Ingrese el código IATA del aeropuerto1: ")
        aeropuerto2=input("Ingrese el código IATA del aeropuerto2: ")
        resultado=controller.clustersTrafico(catalog,aeropuerto1,aeropuerto2)
        printCluster(resultado,aeropuerto1,aeropuerto2)
        display(controller.bonoRequerimiento2(catalog,resultado))

    elif int(inputs[0]) == 3:
        infoOrigen=printEscogerCiudad("Origen")
        #print(infoOrigen)
        if infoOrigen[0]:
            infoSalida=printEscogerCiudad("Destino")
            if infoSalida[0]:
                #print(infoSalida)
                aeropuerto1=infoOrigen[1]
                aeropuerto2=infoSalida[1]
                distancia1=infoOrigen[3]
                distancia2=infoOrigen[3]
                printAeropuertosR3(aeropuerto1,aeropuerto2,distancia1,distancia2)
                #print(aeropuerto1,aeropuerto2)
                resultado=controller.caminoCorto(catalog,aeropuerto1,aeropuerto2)
                printRutaMasCorta(resultado)
                mostrar=input("Desea mostrar el mapa de viaje [y/n]: ")
                if mostrar == "y":
                    display(controller.bonoRequerimiento34(catalog,resultado[1]))
            else:
                print("Error en el nombre")
        else:
            print("Error en el nombre")
            

    elif int(inputs[0]) == 4:

        
        millas_usuario = input("Ingrese millas de usuario: ")
        aeropuerto = input("Ingrese código IATA aeropuerto: ")
        resultado=controller.mstMillasViajero(catalog, millas_usuario, aeropuerto)
        printMstMillasViajero(resultado,millas_usuario)
        mostrar=input("Desea mostrar el mapa de viaje [y/n]: ")
        if mostrar == "y":
            print("\nRuta maximizando paradas")
            display(controller.bonoRequerimiento34(catalog,resultado[2]))
            print("\nRuta propuesta enunciado")
            display(controller.bonoRequerimiento34(catalog,resultado[0]))

    elif int(inputs[0]) == 5:
        aeropuertoCerrado=input("Ingrese el nombre del aeropuerto afectado: ")
        resultado=controller.efectoSuspension(catalog,aeropuertoCerrado)
        printAeropuertosAfectados(resultado,aeropuertoCerrado)
        mostrar=input("Desea mostrar el mapa de viaje [y/n]: ")
        if mostrar == "y":
            display(controller.bonoRequerimiento5(catalog,resultado[0],aeropuertoCerrado))
        pass

    elif int(inputs[0]) == 6:     
        infoOrigen=printEscogerCiudad("Origen")
        if infoOrigen[0]:
            infoSalida=printEscogerCiudad("Destino")
            if infoSalida[0]:
                ciudad1=infoOrigen[2]
                ciudad2=infoSalida[2]
                resultado=controller.bonoAPI(catalog,ciudad1,ciudad2)
                printRutaMasCorta(resultado,opcion=6)

    elif int(inputs[0]) == 7:
        print("Ejecutar las opciones anteriores y visualizar el mapa")
        pass

    else:
        sys.exit(8)
    input("\nDuración: "+str((process_time()-tiempoInicial)*1000)+"ms\nPresione enter para continuar...")
    print("")
    


if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()



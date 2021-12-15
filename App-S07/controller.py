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


def initCatalog():
    return model.initCatalog()


def loadServices(catalog):
    """
    Carga de info de archivos al catálogo
    """

    archivo_aeropuertos = cf.data_dir + "Skylines/airports-utf8-small.csv"
    archivo_rutas = cf.data_dir + "Skylines/routes-utf8-small.csv"
    archivo_ciudades = cf.data_dir + "Skylines/worldcities-utf8.csv"

    ###Se agrega info de aeropuertos y ciudades
    input_file_aeropuerts = csv.DictReader(open(archivo_aeropuertos, encoding="utf-8"),
                                delimiter=",")
    input_file_ciudades= csv.DictReader(open(archivo_ciudades, encoding="utf-8"),
                                delimiter=",")
            
    itemPrimeroB={"city": "-","capital":"-","lat":0,"lng":0,"country":"-"}

    for ciudad in input_file_ciudades:
        model.addCity(catalog,ciudad)
    


    itemPrimeroA={"Name":"-",
                    "City":"-","Country":"-","IATA":"-","Latitude":0, "Longitude":0}

    for aeropuerto in input_file_aeropuerts:
            model.addAeropuerto(catalog,aeropuerto)
    

    
    
    
    input_file_rutas = csv.DictReader(open(archivo_rutas, encoding="utf-8"),
                                delimiter=",")
    for ruta in input_file_rutas:
        model.addRutasGraphDirigido(catalog,ruta)
    
    model.addRutasNoDirigido(catalog)
    model.arbolNConexiones(catalog)
   

    aeropuertoView=model.verPrimerosYUltimos(itemPrimeroA,aeropuerto)
    ciudadView=model.verPrimerosYUltimos(itemPrimeroB,ciudad)

    return catalog,aeropuertoView,ciudadView

def primerItem(file):
    """
    Obtiene el primer item de un archivo
    """
    itemPrimero=None
    for item in csv.reader(file):
        print(item)
        itemPrimero=item
        if itemPrimero is not None:
            break
    
    return itemPrimero

def numero(catalog):
    model.densidad(catalog)

def infoGrafo(catalog,nombreGrafo):
    model.infoGrafo(catalog,nombreGrafo)

def buscarCiudad(catalog,ciudad):
    return model.buscarCiudad(catalog,ciudad)

def coordenadasCiudad(catalog,ciudad,pos=1):
    return model.coordenadasCiudad(catalog,ciudad,pos)

# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def puntosInterconexion(catalog):
    return model.puntosInterconexion(catalog)

def clustersTrafico(catalog,aeropuerto1,aeropuerto2):
    return model.clustersTrafico(catalog,aeropuerto1,aeropuerto2)

def caminoCorto(catalog,aeropuerto1,aeropuerto2):
    return model.caminoCorto(catalog,aeropuerto1,aeropuerto2)

def mstMillasViajero(catalog,millas,aeropuerto):
    return model.mstMillasViajero(catalog,millas,aeropuerto)

def efectoSuspension(catalog,aeropuerto):
    return model.efectoSuspension(catalog,aeropuerto)

def bonoRequerimiento1(resultados):
    return model.bonoRequerimiento1(resultados)

def bonoRequerimiento2(catalog,resultados):
    return model.bonoRequerimiento2(catalog,resultados)

def bonoRequerimiento34(catalog,resultados):
    return model.bonoRequerimiento34(catalog,resultados)

def bonoRequerimiento5(catalog,resultados,aer):
    return model.bonoRequerimiento5(catalog,resultados,aer)

def bonoAPI(catalog,ciudad1,ciudad2):
    return model.bonoAPI(catalog,ciudad1,ciudad2)

# Bibliotecas
import requests
import json
from random import choice
from random import randint
#Descargar la extension tabulate
from tabulate import tabulate

#Constantes del programa
PASAJE = 15000
DESCUENTO = 0.1
VENDER = 1
CERRAR = 2
SALIR = 3
FILAS = [" "," A","B","C","|","D","E","F"]
LETRAS = ["A","B","C","D","E","F"]

#Estructuras

def mostrarOpciones():
    print("Menu de opciones: ")
    print(" 1- VENDER PASAJE")
    print(" 2- CERRAR VUELO")
    print(" 3- FINALIZAR ")
    
def esquema_avion():
#Esquema de asientos
    avion = []

    avion.append(FILAS)
    
    for i in range(1,25):
        avion.append([])

        for j in range(8):

            if j == 0:
                fila =  i
                if fila < 10:
                    avion[fila].append(str(fila)+" ")
                else:
                    avion[fila].append(str(fila))
            elif j+1 != 5:
                avion[i].append("-")
            else:
                avion[i].append("|")
                
    return avion

def listado_pasajeros(lista,fila,columna,asiento):
    
    nombre = input("Ingrese su nombre: ")
    posicion = asiento
    domicilio = input("Ingrese su domicilio: ")
    domic_normalizado = normalizar(domicilio)
    costo =  precio(domic_normalizado)
    persona = {"nombre":  nombre,"asiento": posicion,"domicilio_normalizado":domic_normalizado,"costo":costo}
    lista.append(persona)
    return lista
    
    
#Funciones del programa
def vender(avion,lista):
    
    print("-------------------")
    for i in range(0,25):
        print(" ".join(avion[i]))
    print("--------------------")
    print("Elija ubicacion")
    elegir = int(input("Ingrese 1 para elegir o 0 para que se le asigne al azar: "))

    #Aca podrias usar el validarOpcion(1,0) para evitar que ingresen 2
    
    ocupado = 2
    while ocupado != 1:
        
        if elegir == 1:
            asiento =  [int(input("Ingrese la fila: ")),input("Ingrese el asiento por letra: ")]
            
        else:
            asiento = [randint(1,24), choice(LETRAS)]
        fila = asiento[0]

        #Usaria asiento[1] in ("Aa") o un asiento[1].upper() == A
        #Lo mismo para los elifs
        if asiento[1] == "A" or asiento[1] == "a":
            columna = 1
        elif asiento[1] == "B" or asiento[1] == "b":
            columna = 2
        elif asiento[1] == "C" or asiento[1] == "c":
            columna = 3
        elif asiento[1] == "D" or asiento[1] == "d":
            columna = 5
        elif asiento[1] == "E" or asiento[1] == "e":
            columna = 6
        elif asiento[1] == "F" or asiento[1] == "f":
            columna = 7
        ocupado = ocupados(avion,fila,columna)
            
        
    avion[fila][columna] = "×" #?
    
    lista = listado_pasajeros(lista,fila,columna,asiento)

    #MOSTRAR POR PANTALLA LOS DATOS DEL PASAJE
    
    return [avion,lista] #devuelve una lista?

def ocupados(avion,fila,columna): 
    #Lo haria con un booleano(true or false)
    #ocupado = False 
    #if avion[fila][columna] == "×":
    #   ocupado = True
    #return ocupado

    if avion[fila][columna] == "×":
        return 0
    else:
        return 1
    

def normalizar(domicilio):
 
    direccion = domicilio
    url = "http://servicios.usig.buenosaires.gob.ar/normalizar/?direccion="
    response = requests.get(url + direccion)

    obj = json.loads(response.content)
    
    #Usaria un try porque no se como poner la direccion correctamente

    #try:
        #direcc_normalizada = (obj["direccionesNormalizadas"][0])
    #except:
        #...
        
    direcc_normalizada = (obj["direccionesNormalizadas"][0])

    return(direcc_normalizada)

#Calculos finales
def porcentajes(avion):
    cant = 0

    for i in range (24):
        for j in range(8):
            ocupados(avion,i,j)
            if ocupados(avion,i,j)==0:
                cant += 1

    porcentaje = float(cant/120 * 100)
    imprimir = "El porcentaje de ocupación es: "+ str(porcentaje)+"%"
    return imprimir

def precio(domicilio):
    partido = domicilio["cod_partido"]
    descuento = PASAJE
    
    if partido == "caba":
        descuento = PASAJE - (PASAJE * DESCUENTO)
        
    return descuento
    
def Menu():
    avion = esquema_avion()
    listado_pasajeros = []
    
    mostrarOpciones()
    opcion = int(input("Ingrese su opcion: "))

    #Haria una funcion que se llave validarOpcion(max,min) y dentro ese while
    while opcion != 1 and opcion != 2 and opcion != 3:
        opcion = int(input("No es valida la opcion, indique devuelta :"))
    
    while opcion != SALIR:
        
        if opcion == VENDER:
            venta = vender(avion,listado_pasajeros)
            avion = venta[0]
            listado_pasajeros = venta[1]
           
        if opcion == CERRAR:
           
            listado = [{"asiento":"ASIENTO","nombre":"NOMBRE","domicilio":"DIRECCION","costo":"COSTO"}]
            for pasajeros in listado_pasajeros:
                listado.append({"asiento":pasajeros["asiento"],"nombre":pasajeros["nombre"],"domicilio":pasajeros["domicilio_normalizado"]["direccion"],"costo":pasajeros["costo"]})
            print(tabulate(listado))
            
            print("La cantidad de pasajeros es ",len(listado_pasajeros))
            print(porcentajes(avion))
            
            #creo el archivo de texto
            f = open("vuelo_nnn", "w")
            for i in listado_pasajeros:
                 f.write(str(i))
            f.close()


        
            
        
        mostrarOpciones()
        opcion = int(input("Igrese otra opcion: "))

        #Aca volverias a llamar a la funcion de validar(SALIR,VENDER)
        while opcion != 1 and opcion != 2 and opcion != 3:
            opcion = int(input("No es valida la opcion, indique devuelta: "))




  





Menu()

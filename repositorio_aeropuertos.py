from time import sleep
import json
from utils import readFile, writeFile

archivoAeropuertos = 'aeropuertos.json'


aeropuertos = readFile(archivoAeropuertos)

def get_aeropuertos(aeropuertos = aeropuertos):
    return aeropuertos

def get_aeropuerto_por_nombre(nombre, aeropuertos = aeropuertos ):
    """Busca y retorna un aeropuerto por su código"""
    for aeropuerto in aeropuertos:
        if aeropuerto["codigo"] == nombre.upper():
            return aeropuerto
    return False

def cargar_aeropuerto( aeropuertos = aeropuertos):
    """Funcion encargada de cargar un nuevo aeropuerto al sistema en caso de que un administrador lo necesite.
    No recibe parametros y no retorna parametros"""

    
    codigo = input("Ingrese el código del aeropuerto a ingresar: \n").upper()
    while len(codigo) != 3:
        codigo = input("Ingrese un codigo de aeropuerto valido de 3 letras: \n").upper()
    ciudad = input("Ingrese ciudad del aeropuerto: \n")
    pais = input("Ingrese el pais del aeropuerto: \n").capitalize()
    eje_X = float(input("Ingrese la ubicacion sobre el eje X del aeropuerto: \n"))
    eje_y = float(input("Ingrese la ubicacion sobre el eje Y del aeropuerto: \n"))
    coordenadas = [eje_X, eje_y]
    
    nuevo_aeropuerto = {
        "codigo": codigo,
        "ciudad": ciudad, 
        "pais": pais,
        "posicion": coordenadas,
        "salavip": [
            {
                "nombre": "GOLD",
                "capacidad": 40,
                "precio": "$100",
                "reservados": 0
            }
        ],
        "estacionamiento": {
            "capacidadtotal": 50,
            "lugares": {
                "A": 10,
                "B": 10, 
                "C": 15,
                "D": 15
            },
            "reservados": {}
        }
    }
    
    writeFile(archivoAeropuertos, aeropuertos, nuevo_aeropuerto )
        
    print("Aeropuerto cargado correctamente!")
    sleep(1)
    return
from time import sleep
import json

def get_aeropuertos():
    """Función que lee y retorna la lista de aeropuertos desde el archivo JSON"""
    try:
        with open('aeropuertos.json', 'rt') as archivo:
            return json.load(archivo)
    except (FileNotFoundError, IOError):
        print("Error al leer el archivo de aeropuertos")

def get_aeropuerto_por_nombre(nombre):
    """Busca y retorna un aeropuerto por su código"""
    aeropuertos = get_aeropuertos()
    for aeropuerto in aeropuertos:
        if aeropuerto["codigo"] == nombre.upper():
            return aeropuerto
    return False

def cargar_aeropuerto():
    """Funcion encargada de cargar un nuevo aeropuerto al sistema en caso de que un administrador lo necesite.
    No recibe parametros y no retorna parametros"""

    aeropuertos = get_aeropuertos()
    
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
    
    aeropuertos.append(nuevo_aeropuerto)
    
    with open('aeropuertos.json', 'wt') as archivo:
        json.dump(aeropuertos, archivo, indent=4)
        
    print("Aeropuerto cargado correctamente!")
    sleep(1)
    return
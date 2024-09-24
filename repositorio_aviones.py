#Este repositorio almacenara los datos de los aviones, los cuales se podran utilizar para mostrar solo la info o poder utilizarlo para armar vuelos a los distintos vuelos
#avion = [nombre, capacidad de pasajero, maxima distancia, altura de vuelo maximo, velocidad maxima]
# Diccionarios para cada avión
avion1 = {
    "id":1,
    "modelo": "Boing 737",
    "capacidad": 230,
    "alcance": "6,570 km",
    "altitud_maxima": "12,497 m",
    "velocidad_maxima": "876 km/h"
}

avion2 = {
    "id":2,
    "modelo": "Airbus A320",
    "capacidad": 240,
    "alcance": "6,300 km",
    "altitud_maxima": "12,131 m",
    "velocidad_maxima": "871 km/h"
}

avion3 = {
    "id":3,
    "modelo": "Boeing 777",
    "capacidad": 396,
    "alcance": "15,843 km",
    "altitud_maxima": "13,140 m",
    "velocidad_maxima": "950 km/h"
}

avion4 = {
    "id":4,
    "modelo": "Airbus A350",
    "capacidad": 410,
    "alcance": "16,100 km",
    "altitud_maxima": "13,106 m",
    "velocidad_maxima": "903 km/h"
}

avion5 = {
    "id":5,
    "modelo": "Boeing 787",
    "capacidad": 330,
    "alcance": "14,140 km",
    "altitud_maxima": "13,137 m",
    "velocidad_maxima": "903 km/h"
}

avion6 = {
    "id":6,
    "modelo": "Airbus A380",
    "capacidad": 853,
    "alcance": "15,200 km",
    "altitud_maxima": "13,100 m",
    "velocidad_maxima": "1,020 km/h"
}

avion7 = {
    "id":7,
    "modelo": "Boeing 747",
    "capacidad": 524,
    "alcance": "14,320 km",
    "altitud_maxima": "13,716 m",
    "velocidad_maxima": "988 km/h"
}

# Lista de diccionarios
aviones = [avion1, avion2, avion3, avion4, avion5, avion6, avion7]

def get_aviones():
    return aviones

def mostrar_aviones():
    """Función que imprime los detalles de cada avión almacenado."""
    for avion in aviones:
        print(f"ID: {avion['id']}")
        print(f"Modelo: {avion['modelo']}")
        print(f"Capacidad: {avion['capacidad']} pasajeros")
        print(f"Alcance: {avion['alcance']}")
        print(f"Altitud Máxima: {avion['altitud_maxima']}")
        print(f"Velocidad Máxima: {avion['velocidad_maxima']}")
        print("-" * 40)
    return  

def avion_asignado(codigo):
    for avion in aviones:
        if avion.get("id") == codigo:
            return avion
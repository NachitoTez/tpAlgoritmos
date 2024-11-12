import json
from utils import readFile
archivoAviones = 'aviones.json'
listaAviones = []

aviones = readFile(archivoAviones, listaAviones)

def mostrar_aviones(aviones):
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

def avion_asignado(id, aviones):
    """Devuelve el avión que corresponde al id proporcionado.
    Parámetro: id del avión a buscar
    Retorna: diccionario con los datos del avión o None si no se encuentra"""
    for avion in aviones:
        if avion.get("id") == id:
            avion = avion
            return avion
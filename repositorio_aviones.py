import json
from utils import readFile
from tabulate import tabulate
archivoAviones = 'aviones.json'

aviones = readFile(archivoAviones)
def get_aviones(aviones = aviones):
    return aviones
def mostrar_aviones(aviones):
    """Función que imprime los detalles de cada avión almacenado."""
    print(tabulate(aviones, headers="keys", tablefmt="fancy_grid"))
    return

def avion_asignado(id, aviones):
    """Devuelve el avión que corresponde al id proporcionado.
    Parámetro: id del avión a buscar
    Retorna: diccionario con los datos del avión o None si no se encuentra"""
    for avion in aviones:
        if avion.get("id") == id:
            avion = avion
            return avion
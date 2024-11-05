import json

def get_aviones():
    """Función que lee y retorna la lista de aviones desde el archivo JSON"""
    try:
        with open('aviones.json', 'rt') as archivo:
            return json.load(archivo)
    except (FileNotFoundError, IOError):
        print("Error al leer el archivo de aviones")

def mostrar_aviones():
    """Función que imprime los detalles de cada avión almacenado."""
    aviones = get_aviones()
    for avion in aviones:
        print(f"ID: {avion['id']}")
        print(f"Modelo: {avion['modelo']}")
        print(f"Capacidad: {avion['capacidad']} pasajeros")
        print(f"Alcance: {avion['alcance']}")
        print(f"Altitud Máxima: {avion['altitud_maxima']}")
        print(f"Velocidad Máxima: {avion['velocidad_maxima']}")
        print("-" * 40)
    return

def avion_asignado(id):
    """Devuelve el avión que corresponde al id proporcionado.
    Parámetro: id del avión a buscar
    Retorna: diccionario con los datos del avión o None si no se encuentra"""
    aviones = get_aviones()
    for avion in aviones:
        if avion.get("id") == id:
            return avion
#Como todavía no sabemos trabajar con archivos, en este repositorio vamos a generar los datos de prueba temporalmente.
#Para manipular los datos se van a llamar a funciones creadas en este repositorio, las cuales nos van a permitir no
#modificar la lógica de la funcion main/de la funcion que llame a los datos del repositorio.
#Una vez que cambiemos a archivos se reemplazan los datos de prueba con el acceso al archivo y todo seguiría funcionando igual

#aeropuerto= {"Nombre: string, latitud, longitud: number[]"}
from time import sleep
eze = {
    "codigo": "EZE",
    "ciudad": "Buenos Aires",
    "pais": "Argentina",
    "latitud": [0, 0]
}

aep = {
    "codigo": "AEP",
    "ciudad": "Buenos Aires",
    "pais": "Argentina",
    "latitud": [2, 3]
}

mdq = {
    "codigo": "MDQ",
    "ciudad": "Mar del Plata",
    "pais": "Argentina",
    "latitud": [4, -20]
}

lhr = {
    "codigo": "LHR",
    "ciudad": "London",
    "pais": "United Kingdom",
    "latitud": [4, -20]
}

cdg = {
    "codigo": "CDG",
    "ciudad": "Paris",
    "pais": "France",
    "latitud": [4, -20]
}

iah = {
    "codigo": "IAH",
    "ciudad": "Houston",
    "pais": "United States",
    "latitud": [4, -20]
}

cdm = {
    "codigo": "CDM",
    "ciudad": "Ciudad de México",
    "pais": "Mexico",
    "latitud": [4, -20]
}


aeropuertos = [eze, aep, mdq, lhr, cdg, iah, cdm]


def get_aeropuertos():
    return aeropuertos


def get_aeropuerto_por_nombre(nombre):
    for aeropuerto in aeropuertos:
        if aeropuerto["codigo"] == nombre.upper():
            return aeropuerto
    return False

def cargar_aeropuerto():
    """Funcion encargada de cargar un nuevo aeropuerto al sistema en caso de que un administrador lo necesite.
    No recibe parametros y no retorna parametros"""
    codigo = input("Ingrese el código del aeropuerto a ingresar: \n").upper()
    while len(codigo) !=3:
        codigo = input("Ingrese un codigo de aeropuerto valido de 3 letras: \n").upper()
    ciudad = input("Ingrese ciudad del aeropuerto: \n")
    pais = input("Ingrese el pais del aeropuerto: \n").capitalize()
    eje_X=float(input("Ingrese la ubicacion sobre el eje X del aeropuerto: \n"))
    eje_y=float(input("Ingrese la ubicacion sobre el eje Y del aeropuerto: \n"))
    coordenadas = [eje_X, eje_y]
    aeropuertos.append({"codigo":codigo, "ciudad": ciudad, "pais": pais, "latitud": coordenadas})
    print("Aeropuerto cargado correctamente!")
    sleep(1)
    return 
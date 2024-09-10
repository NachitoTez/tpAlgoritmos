#Como todavía no sabemos trabajar con archivos, en este repositorio vamos a generar los datos de prueba temporalmente.
#Para manipular los datos se van a llamar a funciones creadas en este repositorio, las cuales nos van a permitir no
#modificar la lógica de la funcion main/de la funcion que llame a los datos del repositorio.
#Una vez que cambiemos a archivos se reemplazan los datos de prueba con el acceso al archivo y todo seguiría funcionando igual

#aeropuerto= {"Nombre: string, latitud, longitud: number[]"}

eze = ["EZE", [0, 0]]
aep = ["AEP", [2, 3]]
mdq = ["MDQ", [4, -20]]

aeropuertos = [eze, aep, mdq]


def get_aeropuertos():
    return aeropuertos


def get_aeropuerto_por_nombre(nombre):
    for aeropuerto in aeropuertos:
        if aeropuerto[0] == nombre.upper():
            return aeropuerto
    return False

def ingresar_aeropuerto():
    pass


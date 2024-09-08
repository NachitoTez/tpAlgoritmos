from datetime import datetime, timedelta
from repositorio_aeropuertos import get_aeropuerto_por_nombre
#Como todavía no sabemos trabajar con archivos, en este repositorio vamos a generar los datos de prueba temporalmente
#Para manipular los datos se van a llamar a funciones creadas en este repositorio, las cuales nos van a permitir no
#modificar la lógica de la funcion main/de la funcion que llame a los datos del repositorio.
#Una vez que cambiemos a archivos se reemplazan los datos de prueba con el acceso al archivo y todo sigue igual


#Esto estaría bueno que sea una tupla en un futuro
#vuelo = {id: number, aerolinea: string, modelo: string, capacidad: number, fecha_salida-llegada: number?, origen-destino: string, puerta_embarque: string, terminal: string, tripulacion: tupla, pasajeros: tupla?}
#Por ahora solo va a tener id, aerolinea, orige, destino, estado, fecha salida, fecha llegada (por ahora no consideramos zona hoaria)
vuelo1 = ["AA1234", "Aerolineas Argentinas", get_aeropuerto_por_nombre("EZE"), get_aeropuerto_por_nombre("AEP"), "En horario", "2024-11-11 12:00:00", "2024-11-11 13:00:00"]
vuelo2 = ["BA4321", "British Airways", get_aeropuerto_por_nombre("EZE"), get_aeropuerto_por_nombre("LHR"), "Retrasado", "2024-11-15 18:00:00", "2024-11-16 09:00:00"]
vuelo3 = ["AF5678", "Air France", get_aeropuerto_por_nombre("EZE"), get_aeropuerto_por_nombre("CDG"), "Cancelado", "2024-11-20 13:00:00", "2024-11-20 22:00:00"]
vuelo4 = ["UA8765", "United Airlines", get_aeropuerto_por_nombre("EZE"), get_aeropuerto_por_nombre("IAH"), "En horario", "2024-11-25 23:30:00", "2024-11-26 07:30:00"]
vuelo5 = ["UA8765", "United Airlines", get_aeropuerto_por_nombre("EZE"), get_aeropuerto_por_nombre("IAH"), "Arribado", "2024-11-25 23:30:00", "2024-11-26 07:30:00"]
vuelo6 = ["UA8765", "United Airlines", get_aeropuerto_por_nombre("EZE"), get_aeropuerto_por_nombre("IAH"), "Arribado", "2024-09-08 16:43:03", "2024-09-09 16:43:03"]
vuelos = [vuelo1, vuelo2, vuelo3, vuelo4, vuelo5, vuelo6]

def get_vuelos():
    return vuelos


#Por ahora estos son los unicos atributos modificables de un vuelo.
def modificar_estado_vuelos(id, estado):
    for vuelo in vuelos:
        if vuelo[0] == id:
            vuelo[4] = estado
            return True
    return False

def modificar_destino_vuelos(id, destino):
    for vuelo in vuelos:
        if vuelo[0] == id:
            vuelo[3] = destino
            return True
    return False

def modificar_fecha_salida_vuelos(id, fecha_salida):
    for vuelo in vuelos:
        if vuelo[0] == id:
            vuelo[5] = fecha_salida
            return True
    return False

def modificar_fecha_llegada_vuelos(id, fecha_llegada):
    for vuelo in vuelos:
        if vuelo[0] == id:
            vuelo[6] = fecha_llegada
            return True
    return False

def eliminar_vuelo(id):
    for vuelo in vuelos:
        if vuelo[0] == id:
            del vuelo[0]
            return True
    return False

def vuelo_esta_en_curso(vuelo, tiempo):
    hora_salida = vuelo[5]
    hora_llegada = vuelo[6]
        
    return hora_salida <= tiempo <= hora_llegada


def filtrar_vuelos_en_curso():

    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(ahora)

    vuelos_en_curso = list(filter(lambda vuelo : vuelo_esta_en_curso(vuelo, ahora), vuelos))

    return vuelos_en_curso


def calcular_posicion_vuelo(vuelo):
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if ahora < vuelo[5]:
        return vuelo[2][1]
    elif ahora > vuelo[6]:
        return vuelo[3][1]

# Dejo hasta acá, tengo que pensar como hacer hora_llegada - hora_salida y ahora - hora_salida porque son strings/datetime

    

def mostrar_mapa_vuelos():
    vuelos_en_curso = filtrar_vuelos_en_curso()
    #para todos los vuelos calcular la posicion con calcularposicion
    #mostrar en un mapa los vuelos, idealmente estaría bueno hacer una linea punteada desde el vuelo hasta el destino




from datetime import datetime, timedelta
from repositorio_aeropuertos import get_aeropuerto_por_nombre, ingresar_aeropuerto
from repositorio_aviones import avion_asignado
import re #regex
from utils import validar_input
#Como todavía no sabemos trabajar con archivos, en este repositorio vamos a generar los datos de prueba temporalmente
#Para manipular los datos se van a llamar a funciones creadas en este repositorio, las cuales nos van a permitir no
#modificar la lógica de la funcion main/de la funcion que llame a los datos del repositorio.
#Una vez que cambiemos a archivos se reemplazan los datos de prueba con el acceso al archivo y todo sigue igual

#Esto estaría bueno que sea una tupla en un futuro
#vuelo = {id: number, aerolinea: string, modelo: string, capacidad: number, fecha_salida-llegada: number?, origen-destino: string, puerta_embarque: string, terminal: string, tripulacion: tupla, pasajeros: tupla?}
#Por ahora solo va a tener id, aerolinea, orige, destino, estado, fecha salida, fecha llegada (por ahora no consideramos zona hoaria)
vuelo1 = ["AA1234", "Aerolineas Argentinas", get_aeropuerto_por_nombre("EZE"), get_aeropuerto_por_nombre("AEP"), "En horario", "2024-11-11 12:00:00", "2024-11-11 13:00:00", avion_asignado(4)]
vuelo2 = ["BA4321", "British Airways", get_aeropuerto_por_nombre("EZE"), get_aeropuerto_por_nombre("LHR"), "Retrasado", "2024-11-15 18:00:00", "2024-11-16 09:00:00", avion_asignado(5)]
vuelo3 = ["AF5678", "Air France", get_aeropuerto_por_nombre("EZE"), get_aeropuerto_por_nombre("CDG"), "Cancelado", "2024-11-20 13:00:00", "2024-11-20 22:00:00", avion_asignado(3)]
vuelo4 = ["UA8765", "United Airlines", get_aeropuerto_por_nombre("EZE"), get_aeropuerto_por_nombre("IAH"), "En horario", "2024-11-25 23:30:00", "2024-11-26 07:30:00", avion_asignado(1)]
vuelo5 = ["UA8765", "United Airlines", get_aeropuerto_por_nombre("EZE"), get_aeropuerto_por_nombre("IAH"), "Arribado", "2024-11-25 23:30:00", "2024-11-26 07:30:00", avion_asignado(0)]
vuelo6 = ["UA8765", "United Airlines", get_aeropuerto_por_nombre("EZE"), get_aeropuerto_por_nombre("CDM"), "Arribado", "2024-09-08 16:43:03", "2024-09-09 16:43:03", avion_asignado(2)]
vuelos = [vuelo1, vuelo2, vuelo3, vuelo4, vuelo5, vuelo6]

def get_vuelos():
    return vuelos

def validacion_aeropuerto(regex):
    MAX_INTENTOS = 3
    aeropuerto= input().upper()
    while (aeropuerto == "" or not re.match(regex, aeropuerto)) and MAX_INTENTOS>0:
        aeropuerto= input("Ingrese codigo de aeropuerto correctamente: ").upper()   
        MAX_INTENTOS-=1   
    if(not get_aeropuerto_por_nombre(aeropuerto)): #si el aeropuerto no esta cargado al sistema, nos solicitará ingresarlo
        print("""El aeropuerto ingresado no se encuentra en sistema.
              Elija la opcion a ejecutar:
              1) Reingresar por error.
              2) Cargar el nuevo aeropuerto.""")
        opcion = validar_input(2)
        if(opcion == "1"):
            return "Reintento"
        else:
            return False
    return aeropuerto

def ingresar_vuelo():
    """Funcion encargada de ingresar un nuevo vuelo e ingresarlo a la lista de vuelos."""
     #Importado dentro de la funcion porque como desde main yo importo este archivo, si yo importo main globalmente aqui, se genera un circulo de importacion y rompe
    #El codigo de vuelo al ingresarlo verificar con regex que cumpla AA0000
    regex_numero_vuelo = r'^[A-Z]{2}[0-9]{4}$' #REGEX QUE VALIDE 2 LETRAS AL PRINCIPIO Y 4 NUMEROS AL FINAL
    regex_aerolinea = r'^[0-9]+$' #Matchea si son solo numeros
    regex_codigo_aerupuerto = r'^[A-Z]{3}$'
    regex_fecha = r'^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}'
    numero_vuelo = input("Ingrese el numero de vuelo en formato (XX1111): ").upper()
    while not re.match(regex_numero_vuelo,numero_vuelo): #Si mi regex no matchea con el ingreso, vuelve a solicitarlo
        numero_vuelo = input("Ingrese el numero de vuelo correctamente: ").upper()
    aerolinea = input("Ingrese la Aerolinea prestadora del vuelo: ").capitalize() #al momento de mostrarla .capitalize()
    while aerolinea == "" or re.match(regex_aerolinea,aerolinea):
        aerolinea = input("Ingrese la Aerolinea prestadora del vuelo correctamente: ").capitalize()
    print("Ingrese el codigo de aeropuerto de origen: ")
    aeropuerto_origen= validacion_aeropuerto(regex_codigo_aerupuerto)
    if(aeropuerto_origen == "Reintento"):
        print("Ingrese el codigo de aeropuerto de origen: ")
        aeropuerto_origen=validacion_aeropuerto(regex_codigo_aerupuerto)
    elif(aeropuerto_origen == False):
        administrador()
    print("Ingrese el codigo de aeropuerto de destino: ")
    aeropuerto_destino = validacion_aeropuerto(regex_codigo_aerupuerto)
    if(aeropuerto_destino == "Reintento"):
        print("Ingrese el codigo de aeropuerto de destino: ")
        aeropuerto_destino=validacion_aeropuerto(regex_codigo_aerupuerto)
    elif(aeropuerto_destino == False):
        administrador()
    estado = "En horario" #Los vuelos ingresados al sistema siempre estan en horario
    fecha_hora_despegue= input("Ingrese fecha y hora de despegue en el siguiente formato: AAAA-MM-DD HH:MM:SS : \n")
    while not(re.match(regex_fecha, fecha_hora_despegue)):
        fecha_hora_despegue= input("Ingrese fecha y hora correctamente en el siguiente formato: AAAA-MM-DD HH:MM:SS \n")
    fecha_hora_arribo = input("Ingrese fecha y hora de arribo en el siguiente formato: AAAA-MM-DD HH:MM:SS : \n")
    while not(re.match(regex_fecha, fecha_hora_arribo)):
        fecha_hora_arribo= input("Ingrese fecha y hora correctamente en el siguiente formato: AAAA-MM-DD HH:MM:SS \n")
    vuelos.append([numero_vuelo, aerolinea, aeropuerto_origen, aeropuerto_destino, fecha_hora_despegue, fecha_hora_arribo])
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




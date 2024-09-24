from datetime import datetime, timedelta
from repositorio_aeropuertos import get_aeropuerto_por_nombre, cargar_aeropuerto
from repositorio_aviones import avion_asignado, mostrar_aviones
from os import system
from time import sleep
import re #regex
from utils import validar_input, cantidad_dias
#Como todavía no sabemos trabajar con archivos, en este repositorio vamos a generar los datos de prueba temporalmente
#Para manipular los datos se van a llamar a funciones creadas en este repositorio, las cuales nos van a permitir no
#modificar la lógica de la funcion main/de la funcion que llame a los datos del repositorio.
#Una vez que cambiemos a archivos se reemplazan los datos de prueba con el acceso al archivo y todo sigue igual

#Esto estaría bueno que sea una tupla en un futuro
#vuelo = {id: number, aerolinea: string, modelo: string, capacidad: number, fecha_salida-llegada: number?, origen-destino: string, puerta_embarque: string, terminal: string, tripulacion: tupla, pasajeros: tupla?}
#Por ahora solo va a tener id, aerolinea, orige, destino, estado, fecha salida, fecha llegada (por ahora no consideramos zona hoaria)
vuelo1 = {
    "numero_vuelo": "AA1234",
    "aerolinea": "Aerolineas Argentinas",
    "origen": get_aeropuerto_por_nombre("EZE"),
    "destino": get_aeropuerto_por_nombre("AEP"),
    "estado": "En horario",
    "despegue": "2024-11-11 12:00:00",
    "arribo": "2024-11-11 13:00:00",
    "avion": avion_asignado(4)
}

vuelo2 = {
    "numero_vuelo": "BA4321",
    "aerolinea": "British Airways",
    "origen": get_aeropuerto_por_nombre("EZE"),
    "destino": get_aeropuerto_por_nombre("LHR"),
    "estado": "Retrasado",
    "despegue": "2024-11-15 18:00:00",
    "arribo": "2024-11-16 09:00:00",
    "avion": avion_asignado(5)
}

vuelo3 = {
    "numero_vuelo": "AF5678",
    "aerolinea": "Air France",
    "origen": get_aeropuerto_por_nombre("EZE"),
    "destino": get_aeropuerto_por_nombre("CDG"),
    "estado": "Cancelado",
    "despegue": "2024-11-20 13:00:00",
    "arribo": "2024-11-20 22:00:00",
    "avion": avion_asignado(3)
}

vuelo4 = {
    "numero_vuelo": "UA8764",
    "aerolinea": "United Airlines",
    "origen": get_aeropuerto_por_nombre("EZE"),
    "destino": get_aeropuerto_por_nombre("IAH"),
    "estado": "En horario",
    "despegue": "2024-11-25 23:30:00",
    "arribo": "2024-11-26 07:30:00",
    "avion": avion_asignado(1)
}

vuelo5 = {
    "numero_vuelo": "UA8762",
    "aerolinea": "United Airlines",
    "origen": get_aeropuerto_por_nombre("EZE"),
    "destino": get_aeropuerto_por_nombre("IAH"),
    "estado": "Arribado",
    "despegue": "2024-11-25 23:30:00",
    "arribo": "2024-11-26 07:30:00",
    "avion": avion_asignado(6)
}

vuelo6 = {
    "numero_vuelo": "UA8761",
    "aerolinea": "United Airlines",
    "origen": get_aeropuerto_por_nombre("EZE"),
    "destino": get_aeropuerto_por_nombre("CDM"),
    "estado": "Arribado",
    "despegue": "2024-09-08 16:43:03",
    "arribo": "2024-09-09 16:43:03",
    "avion": avion_asignado(2)
}
vuelos = [vuelo1, vuelo2, vuelo3, vuelo4, vuelo5, vuelo6]

def get_vuelos():
    return vuelos

def mostrar_vuelos():
    """Función que imprime los detalles de cada vuelo almacenado."""
    for vuelo in vuelos:
        print(f"Número de vuelo: {vuelo['numero_vuelo']}")
        print(f"Aerolínea: {vuelo['aerolinea']}")
        print(f"Origen: {vuelo['origen']}")  # Esto puede requerir un __str__ en tu clase Aeropuerto
        print(f"Destino: {vuelo['destino']}")
        print(f"Estado: {vuelo['estado']}")
        print(f"Despegue: {vuelo['despegue']}")
        print(f"Arribo: {vuelo['arribo']}")
        
        # Detalles del avión asignado
        avion = vuelo["avion"]
        print(f"Avión Asignado:")
        print(f"    Modelo: {avion['modelo']}")
        print(f"    Capacidad: {avion['capacidad']} pasajeros")
        print(f"    Alcance: {avion['alcance']}")
        print(f"    Altitud Máxima: {avion['altitud_maxima']}")
        print(f"    Velocidad Máxima: {avion['velocidad_maxima']}")
        print("-" * 40)

    return  

def get_vuelo(numero_vuelo):
    for vuelo in vuelos:
        if vuelo.get("numero_vuelo") == numero_vuelo:
            return vuelo
    return -1

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

def carga_aeropuerto(regex_codigo_aeropuerto, lugar):
    while True:
        print(f"Ingrese el codigo de aeropuerto de {lugar}: ")
        aeropuerto= validacion_aeropuerto(regex_codigo_aeropuerto)
        if(aeropuerto == "Reintento"):
            continue
        elif(aeropuerto == False):
            cargar_aeropuerto()
            system("cls")
            print(f"Ingrese el codigo de aeropuerto de {lugar}: ")
            aeropuerto=validacion_aeropuerto(regex_codigo_aeropuerto)
        return aeropuerto

def ingresar_fecha_y_hora(tipo): #Falta agregar validaciones
    """Función para ingresar fecha y hora y validar los ingresos.
    Recibe por parametro un string si es "fecha y hora de despegue" o "fecha y hora de arribo"
    devuelve la fecha completa"""
    print(f"Ingrese la {tipo}:")
    anio = int(input("Año (AAAA): \n"))
    print("Mes (1-12): ")
    mes = int(validar_input(12))
    dias = cantidad_dias(anio, mes)
    print(f"Día (1-{dias}):")
    dia = int(validar_input(dias))
    print("Hora (0-23):")
    hora = int(validar_input(23, 0))
    print("Minutos (0-59):")
    minutos = int(validar_input(59, 0))
    fecha_hora = datetime(anio, mes, dia, hora, minutos) # convierte la fecha al estandar AAAA-MM-DD HH:MM:SS.
    return fecha_hora
   
def ingreso_numero_vuelo():
    """Funcion que valida y retorna un numero de vuelo"""
    regex_numero_vuelo = r'^[A-Z]{2}[0-9]{4}$' #REGEX QUE VALIDE 2 LETRAS AL PRINCIPIO Y 4 NUMEROS AL FINAL
    numero_vuelo = input("Ingrese el numero de vuelo en formato (XX1111): \n").upper()
    while not re.match(regex_numero_vuelo,numero_vuelo): #Si mi regex no matchea con el ingreso, vuelve a solicitarlo
        numero_vuelo = input("Ingrese el numero de vuelo correctamente: \n").upper()
    return numero_vuelo

def ingresar_vuelo():
    """Funcion encargada de ingresar un nuevo vuelo e ingresarlo a la lista de vuelos."""
    #El codigo de vuelo al ingresarlo verificar con regex que cumpla AA0000
    regex_aerolinea = r'^[0-9]+$' #Matchea si son solo numeros
    regex_codigo_aeropuerto = r'^[A-Z]{3}$'

    numero_vuelo = ingreso_numero_vuelo()

    aerolinea = input("Ingrese la Aerolinea prestadora del vuelo: \n").capitalize() #al momento de mostrarla .capitalize()
    while aerolinea == "" or re.match(regex_aerolinea,aerolinea):
        aerolinea = input("Ingrese la Aerolinea prestadora del vuelo correctamente: \n").capitalize()
    
    aeropuerto_origen = carga_aeropuerto(regex_codigo_aeropuerto, "origen")
    aeropuerto_destino = carga_aeropuerto(regex_codigo_aeropuerto, "destino")

    estado = "En horario" #Los vuelos ingresados al sistema siempre estan en horario

    fecha_hora_despegue = ingresar_fecha_y_hora("fecha y hora de despegue")
    fecha_hora_arribo = ingresar_fecha_y_hora("fecha y hora de arribo")
    
    while fecha_hora_arribo <= fecha_hora_despegue:
        print("La fecha de arribo debe ser posterior a la de despegue. Intente nuevamente.\n")
        fecha_hora_arribo = ingresar_fecha_y_hora("fecha y hora de arribo")
    print("Seleccione el id del avion designado para el vuelo:")
    mostrar_aviones()
    avion = int(validar_input(7))
    vuelo = {
        "numero_vuelo": numero_vuelo,
        "aerolinea": aerolinea,
        "origen": aeropuerto_origen,
        "destino": aeropuerto_destino,
        "estado": estado,
        "despegue": fecha_hora_despegue,
        "arribo": fecha_hora_arribo,
        "avion": avion_asignado(avion)
    }
    vuelos.append(vuelo)
    system("cls")
    print("Vuelo cargado al sistema correctamente!")
    print(vuelo)
    sleep(2)
    system("cls")
    return

def modificar_estado_vuelos(numero_vuelo, key, estado):
    vuelo = get_vuelo(numero_vuelo)
    vuelo[key] = estado

def modificacion_vuelo():
  """Funcion encargada de modificar el atributo del vuelo que se desee."""
  numero_vuelo = ingreso_numero_vuelo()
  
  print("""Ingrese la opción (numero) que quiera modificar:
  -1) Estado del vuelo.
  -2) Destino.
  -3) Fecha-hora de salida.
  -4) Fecha-hora de llegada""")
  opcion = int(validar_input(4))

  if opcion == 1:
    print("""Ingrese el nuevo estado:
  -1) En horario.
  -2) Retrasado.
  -3) Cancelado.""")  
    estado = validar_input(3)

    if estado == "1":
      estado = "En horario"
    elif estado == "2":
      estado = "Retrasado"
    elif estado == "3":
      estado = "Cancelado"
    else:
     return "Error asignando estado" #Acá deberíamos volver a llamar a la funcion en realidad
    
    modificar_estado_vuelos(numero_vuelo,"estado",estado)

    ## Continuar con el resto de modificaciones
  return

def consultar_estado_vuelo():
    numero_vuelo = ingreso_numero_vuelo()
    vuelo = get_vuelo(numero_vuelo)
    if(vuelo == -1):
        print("Vuelo no encontrado en el sistema.")
        return
    print(f"El estado del vuelo es: {vuelo.get("estado")}")


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




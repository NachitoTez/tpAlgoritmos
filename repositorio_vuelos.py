from datetime import datetime, timedelta
import time
from repositorio_aeropuertos import get_aeropuerto_por_nombre, cargar_aeropuerto, get_aeropuertos
from repositorio_aviones import avion_asignado, mostrar_aviones
from os import system
from time import sleep
import re, json #regex
from utils import validar_input, cantidad_dias
import curses



archivoVuelos = "vuelos.json"



def get_vuelos():
    """Obtengo los vuelos del archivo vuelos.json y los devuelvo en una lista.
    En caso de que el archivo no exista o no pueda ser leído, devuelvo una lista vacía.
    Parametro de salida: lista de vuelos [{}]"""
    try:
        with open(archivoVuelos, "rt") as archivo:
            vuelos = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        vuelos = []
    return vuelos
    
def imprimir_vuelo(vuelos): 
    for vuelo in vuelos:
        print(f"Número de vuelo: {vuelo['numero_vuelo']}")
        print(f"Aerolínea: {vuelo['aerolinea']}")
        print(f"Origen: {(vuelo['origen'])}")
        print(f"Destino: {(vuelo['destino'])}")
        print(f"Estado: {vuelo['estado']}")
        print(f"Despegue: {vuelo['despegue']}")
        print(f"Arribo: {vuelo['arribo']}")
        print(f"Asientos disponibles: {vuelo['asientos_disponibles']}")

        # Detalles del avión asignado
        avion = avion_asignado(vuelo["avion"])
        print(f"Avión Asignado:")
        print(f"    Modelo: {avion['modelo']}")
        print(f"    Capacidad: {avion['capacidad']} pasajeros")
        print(f"    Alcance: {avion['alcance']}")
        print(f"    Altitud Máxima: {avion['altitud_maxima']}")
        print(f"    Velocidad Máxima: {avion['velocidad_maxima']}")
        print("-" * 40)

def validacion_aeropuerto():
    regex = r'^[A-Z]{3}$'
    MAX_INTENTOS = 3
    aeropuerto= input().upper()
    while (aeropuerto == "" or not re.match(regex, aeropuerto)) and MAX_INTENTOS>0:
        aeropuerto= input("Ingrese codigo de aeropuerto correctamente: ").upper()   
        MAX_INTENTOS-=1   
    if(not get_aeropuerto_por_nombre(aeropuerto)): #si el aeropuerto no esta cargado al sistema, nos solicitará ingresarlo
        print("""El aeropuerto ingresado no se encuentra en sistema. Deberá Reingresarlo.""")
        return "Reintento"
    return aeropuerto

def filtrar_vuelos(key, valor):
    """Funcion General para poder filtrar nuestra lista de vuelos segun la key que querramos visualizar
    Parametro: key (Numero de vuelo, Aerolinea, etc) y valor (input del user).
    Return: Lista filtrada de vuelos"""
    vuelos = get_vuelos()
    lista = list(filter(lambda vuelo: vuelo.get(key) == valor, vuelos))
    return lista

def mostrar_vuelos():
    """Función que imprime los detalles de cada vuelo almacenado."""
    print("""Ingrese la opcion por la cual desea filtrar la muestra de vuelos:
    1. Numero de vuelo.
    2. Aerolinea.
    3. Aeropuerto de origen.
    4. Aeropuerto de destino.
    5. Estado de vuelo.
    6. Vuelo con Asientos disponibles.
    7. Mostrar todos los vuelos del sistema.
    8. Volver Atras.""")
    bandera = False
    while not bandera:
        opcion = validar_input(8)
        if opcion == "1":
            numero_vuelo = ingreso_numero_vuelo(True)
            vuelo = get_vuelo(numero_vuelo)
            imprimir_vuelo([vuelo])
            bandera = True
        elif opcion == "2":
            aerolinea = input("Ingrese la aerolinea que desea visualizar: \n").title()
            print(aerolinea)
            vuelos = filtrar_vuelos("aerolinea", aerolinea)
            imprimir_vuelo(vuelos)
            bandera = True
        elif opcion == "3":
            aeropuerto = input("Ingrese el codigo de aeropuerto de origen que desea filtrar 'XXX': \n").upper()
            vuelos = filtrar_vuelos("origen", aeropuerto)
            imprimir_vuelo(vuelos)
            bandera = True
        elif opcion == "4":
            aeropuerto = validacion_aeropuerto()
            vuelos = filtrar_vuelos("destino", aeropuerto)
            imprimir_vuelo(vuelos)
            bandera = True
        elif opcion == "5":
            print("""Seleccione el estado por el que quiere filtrar los vuelos: 
            1. En horario.
            2. Retrasado.
            3. Cancelado""")
            estado = validar_input(3)
            if estado == "1":
                estado = "En horario"
            elif estado == "2":
                estado = "Retrasado"
            elif estado == "3":
                estado = "Cancelado"
            vuelos = filtrar_vuelos("estado", estado)
            imprimir_vuelo(vuelos)
            bandera = True
        elif opcion == "6":
            vuelos = filtrar_vuelos_asientos_disponibles()
            imprimir_vuelo(vuelos)
            bandera = True
        elif opcion == "7":
            vuelos = get_vuelos()
            imprimir_vuelo(vuelos)
            bandera = True
        elif opcion == "8":
            return
    return



def get_vuelo(numero_vuelo):
    vuelos = get_vuelos()
    for vuelo in vuelos:
        if vuelo.get("numero_vuelo") == numero_vuelo:
            return vuelo
    return -1

def reescribir_vuelos(vuelos):
    try:
        with open('vuelos.json', 'wt') as archivo:
            json.dump(vuelos, archivo, indent=4)
    except (IOError):
        print("Error al escribir en el archivo")

def carga_aeropuerto(lugar):
    while True:
        print(f"Ingrese el codigo de aeropuerto de {lugar}: ")
        aeropuerto= validacion_aeropuerto()
        if(aeropuerto == "Reintento"):
            continue
        elif(aeropuerto == False):
            cargar_aeropuerto()
            system("cls")
            print(f"Ingrese el codigo de aeropuerto de {lugar}: ")
            aeropuerto=validacion_aeropuerto()
        return aeropuerto

def ingresar_fecha_y_hora(tipo):
    """Función para ingresar fecha y hora y validar los ingresos.
    Recibe por parametro un string si es "fecha y hora de despegue" o "fecha y hora de arribo"
    devuelve la fecha completa"""
    print(f"Ingrese la {tipo}:")
    bandera = True
    while bandera:
            bandera = False
            anio = int(input("Año (AAAA): \n"))
            if anio < 2024 or anio > 2025:
                print("Por favor ingrese un año válido entre 2024 y 2025")
                bandera = True
    
    print("Mes (1-12): ")
    mes = int(validar_input(12))
    dias = cantidad_dias(anio, mes)
    print(f"Día (1-{dias}):")
    dia = int(validar_input(dias))
    print("Hora (0-23):")
    hora = int(validar_input(23, 0))
    print("Minutos (0-59):")
    minutos = int(validar_input(59, 0))
    
    fecha_hora = datetime(anio, mes, dia, hora, minutos)
    
    # Validar que la fecha no sea anterior a la actual
    if fecha_hora < datetime.now():
        print("La fecha ingresada es anterior a la fecha actual")
        return ingresar_fecha_y_hora(tipo)
    return fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
    

def verificar_numero_vuelo_unico(numero_vuelo):
    flag = False
    vuelos = get_vuelos()
    for vuelo in vuelos:
        if(vuelo.get("numero_vuelo") == numero_vuelo):
            flag = True
    return flag

def ingreso_numero_vuelo(flag=False):
    """Funcion que valida y retorna un numero de vuelo"""
    regex_numero_vuelo = r'^[A-Z]{2}[0-9]{4}$' #REGEX QUE VALIDE 2 LETRAS AL PRINCIPIO Y 4 NUMEROS AL FINAL
    numero_vuelo = input("Ingrese el numero de vuelo en formato (XX1111): \n").upper()
    while not re.match(regex_numero_vuelo,numero_vuelo): #Si mi regex no matchea con el ingreso, vuelve a solicitarlo
        numero_vuelo = input("Ingrese el numero de vuelo correctamente (XX1111): \n").upper()
    if flag:
        while not verificar_numero_vuelo_unico(numero_vuelo) and flag:
            numero_vuelo = input("Ingrese un numero de vuelo que exista en el programa: \n").upper()
    else:
        while verificar_numero_vuelo_unico(numero_vuelo):
            numero_vuelo = input("Ingrese un numero de vuelo que no exista en el programa: \n").upper()
    return numero_vuelo

def ingresar_vuelo():
    """Funcion encargada de ingresar un nuevo vuelo e ingresarlo a la lista de vuelos."""
    regex_aerolinea = r'^[0-9]+$' #Matchea si son solo numeros
    numero_vuelo = ingreso_numero_vuelo()
    
    aerolinea = input("Ingrese la Aerolinea prestadora del vuelo: \n").strip().capitalize()
    while aerolinea == "" or re.match(regex_aerolinea,aerolinea) or len(aerolinea) < 2:
        aerolinea = input("Ingrese la Aerolinea prestadora del vuelo correctamente: \n").strip().capitalize()
    
    aeropuerto_origen = carga_aeropuerto("origen")
    aeropuerto_destino = carga_aeropuerto("destino")
    
    while aeropuerto_origen == aeropuerto_destino:
        print("El origen y destino no pueden ser iguales")
        aeropuerto_destino = carga_aeropuerto("destino")

    estado = "En horario" #Los vuelos ingresados al sistema siempre estan en horario

    fecha_hora_despegue = ingresar_fecha_y_hora("fecha y hora de despegue")
    fecha_hora_arribo = ingresar_fecha_y_hora("fecha y hora de arribo")
    
    while fecha_hora_arribo <= fecha_hora_despegue:
        print("La fecha de arribo debe ser posterior a la de despegue. Intente nuevamente.\n")
        fecha_hora_arribo = ingresar_fecha_y_hora("fecha y hora de arribo")
        
    print("Seleccione el id del avion designado para el vuelo:")
    mostrar_aviones()
    avion = int(validar_input(7))
    avion = avion_asignado(avion)
    
    vuelo = {
        "numero_vuelo": numero_vuelo,
        "aerolinea": aerolinea,
        "origen": aeropuerto_origen,
        "destino": aeropuerto_destino,
        "estado": estado,
        "despegue": fecha_hora_despegue,
        "arribo": fecha_hora_arribo,
        "avion": avion,
        "asientos_disponibles": 50 # Valor inicial por defecto
    }

    vuelos = get_vuelos()
    vuelos.append(vuelo)
    reescribir_vuelos(vuelos)

    system("cls")
    print("Vuelo cargado al sistema correctamente!")
    print(vuelo)
    sleep(2)
    system("cls")
    return




def modificar_estado_vuelo(numero_vuelo, key, estado):
    vuelo = get_vuelo(numero_vuelo)
    vuelo[key] = estado

def modificacion_vuelo():
  """Funcion encargada de modificar el atributo del vuelo que se desee."""
  numero_vuelo = ingreso_numero_vuelo(True)
  print("""Ingrese la opción (numero) que quiera modificar:
  -1) Estado del vuelo.
  -2) Destino.
  -3) Origen.
  -4) Fecha-hora de salida.
  -5) Fecha-hora de llegada.
  -6) Volver Atras.""")
  opcion = int(validar_input(5))

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
    modificar_estado_vuelo(numero_vuelo,"estado",estado)
  elif opcion == 2:
    aeropuerto_destino = carga_aeropuerto("nuevo destino")
    modificar_estado_vuelo(numero_vuelo,"destino",get_aeropuerto_por_nombre(aeropuerto_destino))
  elif opcion == 3:
    aeropuerto_origen = carga_aeropuerto("nuevo origen")
    modificar_estado_vuelo(numero_vuelo,"origen",get_aeropuerto_por_nombre(aeropuerto_origen))
  elif opcion == 4:
    fecha_hora_salida = ingresar_fecha_y_hora("fecha y hora de despegue")
    modificar_estado_vuelo(numero_vuelo,"despegue",fecha_hora_salida)
  elif opcion == 5:
    fecha_hora_llegada = ingresar_fecha_y_hora("fecha y hora de arribo")
    modificar_estado_vuelo(numero_vuelo,"arribo",fecha_hora_llegada)
  elif opcion == 6:
      return
    ## Continuar con el resto de modificaciones
  return

def eliminar_vuelo():
    numero_vuelo = ingreso_numero_vuelo(True)
    indice_a_eliminar = 0
    vuelos = get_vuelos()
    for indice, vuelo in enumerate(vuelos):
        if vuelo["numero_vuelo"] == numero_vuelo:
            indice_a_eliminar = indice
    del(vuelos[indice_a_eliminar])
    reescribir_vuelos(vuelos)

def vuelo_esta_en_curso(vuelo, tiempo):
    hora_salida = vuelo["despegue"]
    hora_llegada = vuelo["arribo"]
    return hora_salida <= tiempo <= hora_llegada


def filtrar_vuelos_en_curso():
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(ahora)
    vuelos = get_vuelos()
    vuelos_en_curso = list(filter(lambda vuelo : vuelo_esta_en_curso(vuelo, ahora), vuelos))
    return vuelos_en_curso

def filtrar_vuelos_asientos_disponibles():
    vuelos = get_vuelos()
    vuelos_disponibles = list(filter(lambda vuelo:  vuelo["asientos_disponibles"]> 0, vuelos))
    return vuelos_disponibles


def calcular_posicion_vuelo(vuelo):
    """Calcula la posición actual del vuelo basado en el tiempo transcurrido"""
    ahora = datetime.now()
    despegue = datetime.strptime(vuelo["despegue"], "%Y-%m-%d %H:%M:%S")
    arribo = datetime.strptime(vuelo["arribo"], "%Y-%m-%d %H:%M:%S")
    
    aeropuertos = get_aeropuertos()
    origen = next(a for a in aeropuertos if a["codigo"] == vuelo["origen"])
    destino = next(a for a in aeropuertos if a["codigo"] == vuelo["destino"])

    tiempo_total = (arribo - despegue).total_seconds()
    tiempo_transcurrido = (ahora - despegue).total_seconds()
    
    if tiempo_total > 0:
        x = origen["posicion"][0] + ((destino["posicion"][0] - origen["posicion"][0]) / tiempo_total) * tiempo_transcurrido
        y = origen["posicion"][1] + ((destino["posicion"][1] - origen["posicion"][1]) / tiempo_total) * tiempo_transcurrido
        return [x, y]
    else:
        return None

def inicializar_terminal():
    """Configura la pantalla de curses y los colores"""

    #en la documentación de curses se usa este nombre 'stdscr' es como el objeto para controlar todo
    stdscr = curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)   
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)   
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)    
    return stdscr

def dibujar_borde(stdscr, ancho_maximo, altura_maxima):
    """Dibuja el borde del mapa en la terminal"""
    for i in range(ancho_maximo):
        stdscr.addstr(0, i, "─")
        stdscr.addstr(altura_maxima-1, i, "─")
    for i in range(altura_maxima):
        stdscr.addstr(i, 0, "│")
        stdscr.addstr(i, ancho_maximo-1, "│")

def dibujar_aeropuertos(stdscr, aeropuertos, ancho_maximo, altura_maxima):
    """Dibuja los aeropuertos en el mapa"""
    for aeropuerto in aeropuertos:
        ancho, altura = aeropuerto["posicion"]
        if 0 <= altura < altura_maxima-1 and 0 <= ancho < ancho_maximo-1:
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(altura, ancho, "◉")
            if altura < altura_maxima-2:
                stdscr.addstr(altura, ancho + 2, f"{aeropuerto['codigo']}")
            stdscr.attroff(curses.color_pair(2))

def dibujar_vuelos(stdscr, ancho_maximo, altura_maxima):
    """Dibuja los vuelos en tránsito y devuelve la cantidad en vuelo"""
    vuelos = filtrar_vuelos_en_curso()
    if len(vuelos) > 0:
        for vuelo in vuelos:
            pos = calcular_posicion_vuelo(vuelo)
            if pos:
                ancho, altura = pos
                if 0 <= altura < altura_maxima-1 and 0 <= ancho < ancho_maximo-1:
                    stdscr.attron(curses.color_pair(1))
                    stdscr.addstr(int(altura), int(ancho), "✈")
                    if altura < altura_maxima-2:
                        stdscr.addstr(int(altura) + 1, int(ancho), vuelo["numero_vuelo"][:4])
                    stdscr.attroff(curses.color_pair(1))
    return len(vuelos)


def mostrar_leyenda(stdscr, altura_maxima, vuelos_en_transito):
    """Muestra la leyenda y el mensaje de vuelos en tránsito"""
    stdscr.attron(curses.color_pair(2))
    stdscr.addstr(altura_maxima+1, 2, "◉ Aeropuertos")
    stdscr.attroff(curses.color_pair(2))
    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(altura_maxima+2, 2, "✈ Vuelos en tránsito")
    stdscr.attroff(curses.color_pair(1))

    if vuelos_en_transito == 0:
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(altura_maxima+4, 2, "NO HAY VUELOS EN EL AIRE")
        stdscr.attroff(curses.color_pair(3))

    stdscr.addstr(altura_maxima+3, 2, "Presione Ctrl+C para salir")

def mostrar_mapa_terminal():
    """Muestra un mapa en la terminal con la posición de los vuelos y aeropuertos"""
    stdscr = inicializar_terminal()
    try:
        while True:
            altura_maxima, ancho_maximo = stdscr.getmaxyx()
            #para la leyenda
            altura_maxima -= 5
            ancho_maximo -= 2

            stdscr.clear()
            #TODO arreglar las esquinas
            dibujar_borde(stdscr, ancho_maximo, altura_maxima)
            dibujar_aeropuertos(stdscr, get_aeropuertos(), ancho_maximo, altura_maxima)
            vuelos_en_transito = dibujar_vuelos(stdscr, ancho_maximo, altura_maxima)
            mostrar_leyenda(stdscr, altura_maxima, vuelos_en_transito)

            #para actualizar la pantalla
            stdscr.refresh()
            time.sleep(1)
            
    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()

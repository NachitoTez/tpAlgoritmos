from datetime import datetime, timedelta
from time import sleep

from colorama import Fore
from repositorio_aeropuertos import get_aeropuerto_por_nombre, cargar_aeropuerto, get_aeropuertos
from repositorio_aviones import avion_asignado, mostrar_aviones, get_aviones
from os import system
import re, json #regex
from utils import validar_input, readFile, writeFile, ingresar_fecha_y_hora, bloquear_teclado, limpiar_consola
import curses
from tabulate import tabulate



archivoVuelos = "vuelos.json"
global vuelosLista
def get_vuelos():
    return readFile(archivoVuelos)
vuelosLista = get_vuelos()
listaDeAviones = get_aviones()

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

def filtrar_vuelos(key, valor, listaVuelos = vuelosLista):
    """Funcion General para poder filtrar nuestra lista de vuelos segun la key que querramos visualizar
    Parametro: key (Numero de vuelo, Aerolinea, etc) y valor (input del user).
    Return: Lista filtrada de vuelos"""
    listaVuelos = get_vuelos()
    lista = list(filter(lambda vuelo: vuelo.get(key) == valor, listaVuelos))
    return lista



def mostrar_vuelo_por_numero(vuelosLista=vuelosLista):
    vuelosLista = get_vuelos()
    numero_vuelo = ingreso_numero_vuelo(vuelosLista, True)
    vuelo = get_vuelo(numero_vuelo, vuelosLista)
    if vuelo is None:
        print(f"No se encontró ningún vuelo con el número '{numero_vuelo}'.")
    else:
        print(tabulate([vuelo], headers="keys", tablefmt="fancy_grid"))

def mostrar_vuelos_por_aerolinea(vuelosLista=vuelosLista):
    vuelosLista = get_vuelos()
    aerolinea = input("Ingrese la aerolínea que desea visualizar: \n").title()
    vuelos = filtrar_vuelos("aerolinea", aerolinea, vuelosLista)
    if len(vuelos) == 0:
        print(Fore.LIGHTRED_EX + f"No se encontró ninguna aerolinea con el nombre '{aerolinea}", flush=True)
    print(tabulate(vuelos, headers="keys", tablefmt="fancy_grid"))

def mostrar_vuelos_por_origen(vuelosLista=vuelosLista):
    vuelosLista = get_vuelos()
    print("Ingrese el código de aeropuerto de origen que desea filtrar 'XXX': ")
    aeropuerto = validacion_aeropuerto()
    vuelos = filtrar_vuelos("origen", aeropuerto, vuelosLista)
    if(aeropuerto == "Reintento"):
        print(Fore.LIGHTRED_EX + f"No se encontró ningun aeropuerto con el nombre indicado", flush=True)
    print(tabulate(vuelos, headers="keys", tablefmt="fancy_grid"))


def mostrar_vuelos_por_destino(vuelosLista=vuelosLista):
    vuelosLista = get_vuelos()
    print("Ingrese el código de aeropuerto de destino que desea filtrar 'XXX': ")
    aeropuerto = validacion_aeropuerto()
    vuelos = filtrar_vuelos("destino", aeropuerto, vuelosLista)
    if(aeropuerto == "Reintento"):
        print(Fore.LIGHTRED_EX + f"No se encontró ningun aeropuerto con el nombre indicado", flush=True)
    print(tabulate(vuelos, headers="keys", tablefmt="fancy_grid"))

def mostrar_vuelos_por_estado(vuelosLista=vuelosLista):
    vuelosLista = get_vuelos()
    print("""Seleccione el estado por el que quiere filtrar los vuelos: 
    1. En horario.
    2. Retrasado.
    3. Cancelado""")
    estado = validar_input(3)
    estados = {"1": "En horario", "2": "Retrasado", "3": "Cancelado"}
    vuelos = filtrar_vuelos("estado", estados[estado], vuelosLista)
    if len(vuelos) == 0:
        print(Fore.LIGHTRED_EX + "No hay vuelos disponibles con ese estado", flush=True)
    print(tabulate(vuelos, headers="keys", tablefmt="fancy_grid"))

def mostrar_vuelos_con_asientos(vuelosLista=vuelosLista):
    vuelosLista = get_vuelos()
    vuelos = filtrar_vuelos_asientos_disponibles(vuelosLista)
    if len(vuelos) == 0:
        print(Fore.LIGHTRED_EX + "No hay vuelos con asientos disponibles disponibles", flush=True)
    print(tabulate(vuelos, headers="keys", tablefmt="fancy_grid"))

def mostrar_todos_vuelos(vuelosLista=vuelosLista):
    vuelosLista = get_vuelos()
    if len(vuelosLista) == 0:
        print(Fore.LIGHTRED_EX + "No hay vuelos disponibles", flush=True)
    print(tabulate(vuelosLista, headers="keys", tablefmt="fancy_grid"))




def get_vuelo(numero_vuelo, vuelosLista=vuelosLista):
    """
    Busca un vuelo por su número en la lista de vuelos.
    Devuelve el vuelo como un diccionario si lo encuentra, o None si no existe.
    """
    vuelosLista = get_vuelos()
    for vuelo in vuelosLista:
        if vuelo.get("numero_vuelo", "").strip().upper() == numero_vuelo.strip().upper():
            return vuelo
    
    return None


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


    

def verificar_numero_vuelo_unico(numero_vuelo , vuelosLista=vuelosLista):
    vuelosLista = get_vuelos()
    flag = False
    for vuelo in vuelosLista:
        if(vuelo.get("numero_vuelo") == numero_vuelo):
            flag = True
    return flag

def ingreso_numero_vuelo( vuelosLista=vuelosLista, flag=False):
    """Funcion que valida y retorna un numero de vuelo"""
    vuelosLista = get_vuelos()
    regex_numero_vuelo = r'^[A-Z]{2}[0-9]{4}$' #REGEX QUE VALIDE 2 LETRAS AL PRINCIPIO Y 4 NUMEROS AL FINAL
    numero_vuelo = input("Ingrese el numero de vuelo en formato (XX1111): \n").upper()
    while not re.match(regex_numero_vuelo,numero_vuelo): #Si mi regex no matchea con el ingreso, vuelve a solicitarlo
        numero_vuelo = input("Ingrese el numero de vuelo correctamente (XX1111): \n").upper()
    if flag:
        while not verificar_numero_vuelo_unico(numero_vuelo,vuelosLista) and flag:
            numero_vuelo = input("Ingrese un numero de vuelo que exista en el programa: \n").upper()
    else:
        while verificar_numero_vuelo_unico(numero_vuelo, vuelosLista):
            numero_vuelo = input("Ingrese un numero de vuelo que no exista en el programa: \n").upper()
    return numero_vuelo

def ingresar_vuelo(vuelosLista):
    """Funcion encargada de ingresar un nuevo vuelo e ingresarlo a la lista de vuelos."""
    vuelosLista = get_vuelos()
    regex_aerolinea = r'^[0-9]+$' #Matchea si son solo numeros
    numero_vuelo = ingreso_numero_vuelo(vuelosLista)
    
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
    mostrar_aviones(listaDeAviones)
    avion = int(validar_input(len(listaDeAviones)))
    
    
    vuelo = {
        "numero_vuelo": numero_vuelo,
        "aerolinea": aerolinea,
        "origen": aeropuerto_origen,
        "destino": aeropuerto_destino,
        "estado": estado,
        "despegue": fecha_hora_despegue,
        "arribo": fecha_hora_arribo,
        "avion": avion,
        "asientos_disponibles": avion_asignado(avion, listaDeAviones)["capacidad"] 
    }

    writeFile(archivoVuelos, vuelosLista, vuelo )
    system("cls")
    print("Vuelo cargado al sistema correctamente!")
    bloquear_teclado(2)
    system("cls")
    return




def modificar_estado_vuelo(numero_vuelo, key, estado):
    vuelos = readFile(archivoVuelos)
    for vuelo in vuelos:
        if vuelo["numero_vuelo"] == numero_vuelo:
            vuelo[key] = estado
            writeFile(archivoVuelos, vuelos, None)
            return True
    return False

def modificacion_vuelo(vuelosLista):
  """Funcion encargada de modificar el atributo del vuelo que se desee."""
  vuelosLista = get_vuelos()
  print(tabulate(vuelosLista, headers="keys", tablefmt="fancy_grid"))
  numero_vuelo = ingreso_numero_vuelo(vuelosLista, True)
  vuelo = get_vuelo(numero_vuelo, vuelosLista)
  print("""Ingrese la opción (numero) que quiera modificar:
  -1) Estado del vuelo.
  -2) Destino.
  -3) Origen.
  -4) Fecha-hora de salida.
  -5) Fecha-hora de llegada.
  -6) Volver Atras.""")
  opcion = int(validar_input(6))

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
    modificar_estado_vuelo(numero_vuelo,"destino",aeropuerto_destino)
  elif opcion == 3:
    aeropuerto_origen = carga_aeropuerto("nuevo origen")
    modificar_estado_vuelo(numero_vuelo,"origen",aeropuerto_origen)
  elif opcion == 4:
    fecha_hora_salida = ingresar_fecha_y_hora("fecha y hora de despegue")
    while vuelo["arribo"] <= fecha_hora_salida:
        print("La fecha de arribo debe ser posterior a la de despegue. Intente nuevamente.\n")
        fecha_hora_salida = ingresar_fecha_y_hora("fecha y hora de arribo")
    modificar_estado_vuelo(numero_vuelo,"despegue",fecha_hora_salida)
  elif opcion == 5:
    fecha_hora_llegada = ingresar_fecha_y_hora("fecha y hora de arribo")
    while fecha_hora_llegada <= vuelo["despegue"]:
        print("La fecha de arribo debe ser posterior a la de despegue. Intente nuevamente.\n")
        fecha_hora_llegada = ingresar_fecha_y_hora("fecha y hora de arribo")
    modificar_estado_vuelo(numero_vuelo,"arribo",fecha_hora_llegada)
  elif opcion == 6:
      return
    ## Continuar con el resto de modificaciones
  return

def eliminar_vuelo(vuelosLista):
    vuelosLista = get_vuelos()
    print(tabulate(vuelosLista, headers="keys", tablefmt="fancy_grid"))
    numero_vuelo = ingreso_numero_vuelo(vuelosLista, True)
    indice_a_eliminar = 0
    for indice, vuelo in enumerate(vuelosLista):
        if vuelo["numero_vuelo"] == numero_vuelo:
            indice_a_eliminar = indice
    del(vuelosLista[indice_a_eliminar])
    reescribir_vuelos(vuelosLista)

def vuelo_esta_en_curso(vuelo, tiempo):
    hora_salida = vuelo["despegue"]
    hora_llegada = vuelo["arribo"]
    return hora_salida <= tiempo <= hora_llegada

def vuelo_ya_despego(vuelo, tiempo):
    hora_salida = vuelo["despegue"]
    return hora_salida <= tiempo


def filtrar_vuelos_en_curso(vuelosLista = vuelosLista):
    vuelosLista = get_vuelos()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    vuelos_en_curso = list(filter(lambda vuelo : vuelo_esta_en_curso(vuelo, ahora), vuelosLista))
    return vuelos_en_curso

def filtrar_vuelos_despegados(vuelosLista = vuelosLista):
    vuelosLista = get_vuelos()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    vuelos_despegados = list(filter(lambda vuelo : not vuelo_ya_despego(vuelo, ahora), vuelosLista))
    return vuelos_despegados

def filtrar_vuelos_asientos_disponibles(vuelosLista = vuelosLista):
    vuelosLista = get_vuelos()
    vuelos_disponibles = list(filter(lambda vuelo:  vuelo["asientos_disponibles"]> 0, vuelosLista))
    vuelos_disponibles = filtrar_vuelos_despegados(vuelos_disponibles)
    return vuelos_disponibles


def calcular_posicion_vuelo(vuelo):
    """Calcula la posición actual del vuelo basado en el tiempo transcurrido y la escala del mapa"""
    ahora = datetime.now()
    despegue = datetime.strptime(vuelo["despegue"], "%Y-%m-%d %H:%M:%S")
    arribo = datetime.strptime(vuelo["arribo"], "%Y-%m-%d %H:%M:%S")
    
    aeropuertos = get_aeropuertos()
    origen = next(a for a in aeropuertos if a["codigo"] == vuelo["origen"])
    destino = next(a for a in aeropuertos if a["codigo"] == vuelo["destino"])

    tiempo_total = (arribo - despegue).total_seconds()
    tiempo_transcurrido = (ahora - despegue).total_seconds()
    
    if tiempo_total > 0:
        # Calculamos la posición interpolada
        x = origen["posicion"][0] + ((destino["posicion"][0] - origen["posicion"][0]) / tiempo_total) * tiempo_transcurrido
        y = origen["posicion"][1] + ((destino["posicion"][1] - origen["posicion"][1]) / tiempo_total) * tiempo_transcurrido
        
        # Encontrar los límites del mapa
        x_min = min(a["posicion"][0] for a in aeropuertos)
        x_max = max(a["posicion"][0] for a in aeropuertos)
        y_min = min(a["posicion"][1] for a in aeropuertos)
        y_max = max(a["posicion"][1] for a in aeropuertos)
        
        # Escalar las coordenadas
        margen = 2
        altura_maxima, ancho_maximo = curses.LINES - 5, curses.COLS - 2
        x_escalada = int(((x - x_min) / (x_max - x_min)) * (ancho_maximo - 2*margen)) + margen
        y_escalada = int(((y - y_min) / (y_max - y_min)) * (altura_maxima - 2*margen)) + margen
        
        return [x_escalada, y_escalada]
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
    """Dibuja los aeropuertos en el mapa escalando sus coordenadas al tamaño de la pantalla"""
    # Encontrar los límites del mapa
    x_min = min(aeropuerto["posicion"][0] for aeropuerto in aeropuertos)
    x_max = max(aeropuerto["posicion"][0] for aeropuerto in aeropuertos)
    y_min = min(aeropuerto["posicion"][1] for aeropuerto in aeropuertos)
    y_max = max(aeropuerto["posicion"][1] for aeropuerto in aeropuertos)
    
    # Agregar un pequeño margen
    margen = 2
    
    for aeropuerto in aeropuertos:
        x, y = aeropuerto["posicion"]
        
        # Escalar las coordenadas al tamaño de la pantalla
        x_escalada = int(((x - x_min) / (x_max - x_min)) * (ancho_maximo - 2*margen)) + margen
        y_escalada = int(((y - y_min) / (y_max - y_min)) * (altura_maxima - 2*margen)) + margen
        
        try:
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(y_escalada, x_escalada, "◉")
            # Dibujar el código del aeropuerto a la derecha del símbolo
            if x_escalada + 2 < ancho_maximo - len(aeropuerto["codigo"]):
                stdscr.addstr(y_escalada, x_escalada + 2, f"{aeropuerto['codigo']}")
            stdscr.attroff(curses.color_pair(2))
        except curses.error:
            continue  # Ignorar errores de dibujado fuera de pantalla

def dibujar_vuelos(stdscr, ancho_maximo, altura_maxima):
    """Dibuja los vuelos en tránsito y devuelve la cantidad en vuelo"""
    vuelos = filtrar_vuelos_en_curso()
    vuelos_dibujados = 0
    
    if len(vuelos) > 0:
        for vuelo in vuelos:
            pos = calcular_posicion_vuelo(vuelo)
            if pos:
                ancho, altura = pos
                # Ajustamos las coordenadas para que queden dentro del mapa
                ancho_ajustado = max(1, min(int(ancho), ancho_maximo-2))
                altura_ajustada = max(1, min(int(altura), altura_maxima-2))
                
                try:
                    stdscr.attron(curses.color_pair(1))
                    # Dibujamos el avión
                    stdscr.addstr(altura_ajustada, ancho_ajustado, "✈")
                    
                    # Dibujamos el número de vuelo completo debajo si hay espacio
                    if altura_ajustada < altura_maxima-2:
                        numero_vuelo = vuelo["numero_vuelo"]  # Quitamos el slice [:4]
                        # Centramos el número respecto al avión
                        pos_x = max(1, min(ancho_ajustado - len(numero_vuelo)//2, ancho_maximo-len(numero_vuelo)-1))
                        stdscr.addstr(altura_ajustada + 1, pos_x, numero_vuelo)
                    
                    stdscr.attroff(curses.color_pair(1))
                    vuelos_dibujados += 1
                except curses.error:
                    continue  # Ignoramos errores de dibujado fuera de pantalla
                    
    return vuelos_dibujados


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
            bloquear_teclado(1)
            
    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()
        limpiar_consola()


def reservar_asiento(numero_vuelo):
    """Permite modificar un vuelo para hacer efectiva una reserva"""
    try:
        vuelos = readFile(archivoVuelos)
        
        if not isinstance(numero_vuelo, str):
            raise ValueError("El número de vuelo debe ser un string")
            
        for vuelo in vuelos:
            if vuelo["numero_vuelo"] == numero_vuelo:
                if vuelo["estado"] == "Arribado":
                    print("No se pueden reservar asientos en vuelos ya arribados")
                    return False
                    
                if vuelo["asientos_disponibles"] > 0:
                    vuelo["asientos_disponibles"] -= 1
                    writeFile(archivoVuelos, vuelos, None)
                    print(f"Reserva exitosa. Quedan {vuelo['asientos_disponibles']} asientos disponibles.")
                    vuelosLista = get_vuelos()
                    return True
                else:
                    print("No hay asientos disponibles para este vuelo.")
                    return False
                    
        print("Vuelo no encontrado.")
        return False
        
    except Exception as e:
        print(f"Error al procesar la reserva: {str(e)}")
        return False
    
def revision_vuelos_fecha():
    """
    Realiza la revisión de los vuelos por fecha y actualiza las fechas de despegue y arribo si es necesario.
    """
    for vuelo in vuelosLista:
        if datetime.strptime(vuelo["arribo"], "%Y-%m-%d %H:%M:%S") < datetime.now():
            vuelo["despegue"] = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")
            vuelo["arribo"] = (datetime.now() + timedelta(days=8)).strftime("%Y-%m-%d %H:%M:%S")
    writeFile(archivoVuelos, vuelosLista, None)

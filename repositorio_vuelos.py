from datetime import datetime, timedelta
from repositorio_aeropuertos import get_aeropuerto_por_nombre, cargar_aeropuerto, get_aeropuertos
from repositorio_aviones import avion_asignado, mostrar_aviones, get_aviones
from os import system
import re, json #regex
from utils import validar_input, readFile, writeFile, ingresar_fecha_y_hora, bloquear_teclado
import curses
from tabulate import tabulate

def get_vuelos():
    return readFile(archivoVuelos)

archivoVuelos = "vuelos.json"
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
    lista = list(filter(lambda vuelo: vuelo.get(key) == valor, listaVuelos))
    return lista

def mostrar_vuelos(vuelosLista = vuelosLista):
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
            numero_vuelo = ingreso_numero_vuelo(vuelosLista, True)
            vuelo = get_vuelo(numero_vuelo, vuelosLista)
            if vuelo is None:
                print(f"No se encontró ningún vuelo con el número '{numero_vuelo}'.")
            print(tabulate([vuelo], headers="keys", tablefmt="fancy_grid"))
            bandera = True
        elif opcion == "2":
            aerolinea = input("Ingrese la aerolinea que desea visualizar: \n").title()
            print(aerolinea)
            vuelos = filtrar_vuelos("aerolinea", aerolinea, vuelosLista)
            print(tabulate(vuelos, headers="keys", tablefmt="fancy_grid"))
            bandera = True
        elif opcion == "3":
            print("Ingrese el codigo de aeropuerto de destino que desea filtrar 'XXX': ")
            aeropuerto = validacion_aeropuerto()
            vuelos = filtrar_vuelos("origen", aeropuerto, vuelosLista)
            print(tabulate(vuelos, headers="keys", tablefmt="fancy_grid"))
            bandera = True
        elif opcion == "4":
            print("Ingrese el codigo de aeropuerto de destino que desea filtrar 'XXX': ")
            aeropuerto = validacion_aeropuerto()
            vuelos = filtrar_vuelos("destino", aeropuerto, vuelosLista)
            print(tabulate(vuelos, headers="keys", tablefmt="fancy_grid"))
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
            vuelos = filtrar_vuelos("estado", estado, vuelosLista)
            print(tabulate(vuelos, headers="keys", tablefmt="fancy_grid"))
            bandera = True
        elif opcion == "6":
            vuelos = filtrar_vuelos_asientos_disponibles(vuelosLista)
            print(tabulate(vuelos, headers="keys", tablefmt="fancy_grid"))
            bandera = True
        elif opcion == "7":
            print(tabulate(vuelosLista, headers="keys", tablefmt="fancy_grid"))
            bandera = True
        elif opcion == "8":
            return
    return



def get_vuelo(numero_vuelo, vuelosLista):
    """
    Busca un vuelo por su número en la lista de vuelos.
    Devuelve el vuelo como un diccionario si lo encuentra, o None si no existe.
    """
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


    

def verificar_numero_vuelo_unico(numero_vuelo , vuelosLista = vuelosLista):
    flag = False
    for vuelo in vuelosLista:
        if(vuelo.get("numero_vuelo") == numero_vuelo):
            flag = True
    return flag

def ingreso_numero_vuelo( vuelosLista = vuelosLista, flag=False):
    """Funcion que valida y retorna un numero de vuelo"""
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
    modificar_estado_vuelo(numero_vuelo,"destino",get_aeropuerto_por_nombre(aeropuerto_destino))
  elif opcion == 3:
    aeropuerto_origen = carga_aeropuerto("nuevo origen")
    modificar_estado_vuelo(numero_vuelo,"origen",get_aeropuerto_por_nombre(aeropuerto_origen))
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


def filtrar_vuelos_en_curso(vuelosLista = vuelosLista):
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(ahora)
    vuelos_en_curso = list(filter(lambda vuelo : vuelo_esta_en_curso(vuelo, ahora), vuelosLista))
    return vuelos_en_curso

def filtrar_vuelos_asientos_disponibles(vuelosLista = vuelosLista):
    vuelos_disponibles = list(filter(lambda vuelo:  vuelo["asientos_disponibles"]> 0, vuelosLista))
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
            bloquear_teclado(1)
            
    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()


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
                    writeFile(archivoVuelos, vuelos)
                    print(f"Reserva exitosa. Quedan {vuelo['asientos_disponibles']} asientos disponibles.")
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

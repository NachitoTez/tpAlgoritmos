import curses
from datetime import datetime, time
import random
import shutil
import sys
from time import sleep
from colorama import Fore
from keyboard import block_key, unblock_key
from os import system, name
import json

def validar_input(cantidad_de_opciones, inicio=1):
    """Función creada para validar si la opción ingresada por teclado esta dentro del numero de opciones posibles
    Recibe por parámetro la cantidad de opciones disponibles y devuelve la opcion "String" ingresada por el usuario ya validada
    """
    opcion = input()
    while not(opcion.isdigit()):
        opcion = input("Ingrese una opción válida: ")
    opcion = int(opcion)
    opciones_validas = []
    for i in range(inicio,cantidad_de_opciones+1):
        opciones_validas.append(i)
    
    while opcion not in opciones_validas:
        opcion = input("Ingrese una opción válida: ")
        opcion = int(opcion)
    return str(opcion)

def bisiesto(anio):
    return anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0)
def cantidad_dias(anio, mes):
    dias = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if(mes==2 and bisiesto(anio)):
        return dias[mes-1]+1
    else:
        return dias[mes-1]
    
def randonAprobado():
    valido = random.randint(0,10)
    if valido > 2:
        return True
    else:
        return False
    
def limpiar_consola():
    if name == "nt":  # Windows
        system("cls")
    else:  # macOS y Linux
        system("clear")
    return

def writeFile(archivo, listaDatos, nuevoDato ):
    """Funcin que permite escribir en json """
    try:
        with open(archivo, "wt") as archivo:
            if nuevoDato is not None:
                listaDatos.append(nuevoDato)
            json.dump(listaDatos, archivo, indent = 4) 
    except ValueError as e:
            print(e)   
def readFile(nombreArchivo):
    """Funcion para leer archivos"""
    try:
        with open(nombreArchivo, "rt") as archivo:
            nombreJSon = json.load(archivo)
            return nombreJSon
    except (FileNotFoundError, json.JSONDecodeError):
        nombreJSon = []
        return nombreJSon
    
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

def bloquear_teclado(tiempo):
    if name == "nt":  # Windows
        block_key('*')
    sleep(tiempo)
    if name == "nt":  # Windows
        unblock_key('*')

def calcularPrecioEstacionamiento(fecha_inicio, fecha_fin, tarifa_por_dia):
    """
    Funcion que calcula el valor total de la reserva de estacionamiento basado en las fechas y horas de inicio y fin.
    """
    inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d %H:%M:%S")
    fin = datetime.strptime(fecha_fin, "%Y-%m-%d %H:%M:%S")

    diferencia_horas = (fin - inicio).total_seconds() / 3600

    valor_total = (diferencia_horas / 24) * tarifa_por_dia

    if diferencia_horas <= 0:
        raise ValueError("La fecha de fin debe ser posterior a la fecha de inicio.")

    return valor_total

def escribir_lento(texto, delay=0.05, color=Fore.WHITE):
    """
    Función para hacer que el texto se escriba pausado.
    """
    for letra in texto:
        print(color + letra, end="", flush=True)
        bloquear_teclado(delay)
    print()

def centrar_texto(ascii_art):
    """
    Función para hacer que el texto se centre en la terminal.
    """
    terminal_width = shutil.get_terminal_size().columns
    lineas_centradas = [
        linea.center(terminal_width) for linea in ascii_art.splitlines()
    ]
    return "\n".join(lineas_centradas)

def escribir_ascii_lento(ascii_art, delay=0.001, color=Fore.LIGHTBLACK_EX):
    for linea in ascii_art.splitlines():
        escribir_lento(linea , delay, color)

def imprimible_menu_regreso(funcion):
	bandera = False
	volver = input("seleccione 0 para volver al menu principal o -1 para salir del sistema: ")
	while not bandera:    
		if volver == "0":
			bandera = True
			funcion()
		elif volver == "-1":
			print("Muchas gracias")
			bandera = True
		else:
			print("Seleccione un valor valido")
			volver = input("seleccione 0 para volver al menu principal o -1 para salir del sistema: ")

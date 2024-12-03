import shutil
from colorama import Fore, init
import pyfiglet
import repositorio_reservas
import repositorio_usuarios
from repositorio_vuelos import mostrar_mapa_terminal, ingresar_vuelo, mostrar_todos_vuelos, mostrar_vuelo_por_numero, modificacion_vuelo, eliminar_vuelo, filtrar_vuelos_asientos_disponibles, get_vuelos, mostrar_vuelos_con_asientos, mostrar_vuelos_por_aerolinea, mostrar_vuelos_por_destino, mostrar_vuelos_por_estado, mostrar_vuelos_por_origen, revision_vuelos_fecha
from utils import centrar_texto, escribir_ascii_lento, imprimible_menu_regreso, validar_input, limpiar_consola
from repositorio_aeropuertos import get_aeropuertos
from repositorio_usuarios import getDataUser, usuarios
from utils import escribir_lento, bloquear_teclado, readFile
from repositorio_pagos import registrarTarjeta

 
#Es solo para hacer mas legible el codigo y no tener magic numbers
NUMERO_DE_OPCIONES_1 = 1
NUMERO_DE_OPCIONES_2 = 2
NUMERO_DE_OPCIONES_3 = 3
NUMERO_DE_OPCIONES_4 = 4
NUMERO_DE_OPCIONES_5 = 5
NUMERO_DE_OPCIONES_6 = 6



init(autoreset=True)

listaAeropuertos = get_aeropuertos()


def administrador():
    """Listado de funciones disponibles que se pueden ejecutar. Exclusivo de Administradores"""
    limpiar_consola()
    listaDeVuelos=get_vuelos()
    titulo = "MENÚ DE ADMINISTRADOR"
    titulo_centrado = centrar_texto(titulo)
    print(Fore.LIGHTBLUE_EX + titulo_centrado + Fore.RESET)
    
    ancho_terminal = shutil.get_terminal_size().columns
    print(Fore.BLACK + "=" * ancho_terminal + Fore.RESET)
    print()
    
    opciones = [
        (f"{Fore.LIGHTBLUE_EX}1){Fore.WHITE} Ingresar vuelo al sistema{Fore.RESET} ✈️"),
        (f"{Fore.LIGHTBLUE_EX}2){Fore.WHITE} Modificar vuelo{Fore.RESET} ✏️"),
        (f"{Fore.LIGHTBLUE_EX}3){Fore.WHITE} Consulta de estados de vuelos{Fore.RESET} 🔍"),
        (f"{Fore.LIGHTBLUE_EX}4){Fore.WHITE} Eliminar vuelo{Fore.RESET} 🗑️"),
        (f"{Fore.RED}5){Fore.WHITE} Cerrar Sesión{Fore.RESET} ❌")
    ]
    
    for opcion in opciones:
        print(opcion)
        print()
    
    opciones_admin = {
        "1": lambda: ingresar_vuelo(listaDeVuelos),
        "2": lambda: modificacion_vuelo(listaDeVuelos),
        "3": lambda: mostrar_vuelos(get_aeropuertos(), usuarios),
        "4": lambda: eliminar_vuelo(listaDeVuelos),
        "5": lambda: cerrar_sesion()
    }

    while True:
        opcion = validar_input(NUMERO_DE_OPCIONES_5)
        
        accion = opciones_admin.get(opcion)
        
        if accion:
            limpiar_consola()
            accion()
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")
        if opcion != "5":
            administrador()

def cerrar_sesion():
    """Función para manejar el cierre de sesión"""
    limpiar_consola()
    print("Ha cerrado la sesión con éxito!")
    bloquear_teclado(1)
    limpiar_consola()
    main(False)

def consultante(aeropuertos, listaUsuario):
    """Listado de funciones disponibles Exclusivo de Consultante"""
    limpiar_consola()
    
    titulo = "MENU PRINCIPAL"
    titulo_centrado = centrar_texto(titulo)
    print(Fore.LIGHTCYAN_EX + titulo_centrado + Fore.RESET)
    
    ancho_terminal = shutil.get_terminal_size().columns
    
    print(Fore.BLACK + "=" * ancho_terminal + Fore.RESET)
    print()
	    
    opciones = [
        (f"{Fore.LIGHTGREEN_EX}1) Vuelos{Fore.RESET} ✈️"),
        (f"{Fore.LIGHTMAGENTA_EX}2) Reservas{Fore.RESET} 🎟️"),
        (f"{Fore.LIGHTBLUE_EX}3) Registrar tarjeta{Fore.RESET}  💳"),
        (f"{Fore.RED}4) Cerrar sesión{Fore.RESET} ❌")
    ]
    
    for opcion in opciones:
        print(opcion)
        print()
    
    
    menu_opciones_principal(aeropuertos, listaUsuario)

def menu_opciones_principal(aeropuertos, listaUsuario):
    """Menú principal dividido en submenús"""
    user = getDataUser()
    archivoUser = "user.json"
    listaUsuario = readFile(archivoUser)
    
    opciones_principal = {
        "1": lambda: menu_vuelos(aeropuertos, listaUsuario),
        "2": lambda: menu_reservas(user, aeropuertos, listaUsuario),
        "3": lambda: registrarTarjeta(user),
        "4": lambda: cerrar_sesion()
    }
    
    bandera = False
    while not bandera:
        opcion = validar_input(NUMERO_DE_OPCIONES_4)
        accion = opciones_principal.get(opcion)
        
        if accion:
            limpiar_consola()
            accion()
            bandera = True
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")
        if opcion != "4":
            consultante(aeropuertos, listaUsuario)


# Submenú de vuelos
def menu_vuelos(aeropuertos, listaUsuario):
    """Opciones relacionadas con vuelos"""
    limpiar_consola()
    
    titulo = "VUELOS"
    titulo_centrado = centrar_texto(titulo)
    print(Fore.LIGHTGREEN_EX + titulo_centrado + Fore.RESET)
    
    ancho_terminal = shutil.get_terminal_size().columns
    
    print(Fore.BLACK + "=" * ancho_terminal + Fore.RESET)
    print()
    
    opciones = [
        (f"{Fore.LIGHTGREEN_EX}1){Fore.WHITE} Consulta de vuelos{Fore.RESET} ✈️"),
        (f"{Fore.LIGHTGREEN_EX}2){Fore.WHITE} Consulta de vuelos con asientos disponibles{Fore.RESET} 🔎"),
        (f"{Fore.LIGHTGREEN_EX}3){Fore.WHITE} Mostrar mapa de vuelos{Fore.RESET} 🗺️"),
        (f"{Fore.RED}4){Fore.WHITE} Volver al menú principal{Fore.RESET} 🔙")
    ]
    
    for opcion in opciones:
        print(opcion)
        print()
    
    opciones_vuelos = {
        "1": lambda: mostrar_vuelos(aeropuertos, listaUsuario),
        "2": lambda: consultarAsientosDisponibles(),
        "3": lambda: mostrar_mapa_terminal(),
        "4": lambda: consultante(aeropuertos, listaUsuario)
    }

    bandera = False
    while not bandera:
        opcion = validar_input(NUMERO_DE_OPCIONES_4)
        accion = opciones_vuelos.get(opcion)
        
        if accion:
            limpiar_consola()
            accion()
            bandera = True
            limpiar_consola()
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")
            
def mostrar_vuelos(aeropuertos, listaUsuario):
    """Función que imprime los detalles de cada vuelo almacenado."""
    limpiar_consola()
    
    titulo = "SUBMENÚ VUELOS"
    titulo_centrado = centrar_texto(titulo)
    print(Fore.GREEN + titulo_centrado + Fore.RESET)
    
    ancho_terminal = shutil.get_terminal_size().columns
    
    print(Fore.BLACK + "=" * ancho_terminal + Fore.RESET)
    print()
    
    opciones = [
        (f"{Fore.LIGHTGREEN_EX}1){Fore.WHITE} Número de vuelo{Fore.RESET} 🔢"),
        (f"{Fore.LIGHTGREEN_EX}2){Fore.WHITE} Aerolínea{Fore.RESET} ✈️"),
        (f"{Fore.LIGHTGREEN_EX}3){Fore.WHITE} Aeropuerto de origen{Fore.RESET} 🛫"),
        (f"{Fore.LIGHTGREEN_EX}4){Fore.WHITE} Aeropuerto de destino{Fore.RESET} 🛬"),
        (f"{Fore.LIGHTGREEN_EX}5){Fore.WHITE} Estado de vuelo{Fore.RESET} 📊"),
        (f"{Fore.LIGHTGREEN_EX}6){Fore.WHITE} Vuelo con Asientos disponibles{Fore.RESET} 💺"),
        (f"{Fore.LIGHTGREEN_EX}7){Fore.WHITE} Mostrar todos los vuelos del sistema{Fore.RESET} 📋"),
        (f"{Fore.RED}8){Fore.WHITE} Volver Atrás{Fore.RESET} 🔙")
    ]
    
    for opcion in opciones:
        print(opcion)
        print()
    
    opciones_vuelos = {
        "1": lambda: mostrar_vuelo_por_numero(),
        "2": lambda: mostrar_vuelos_por_aerolinea(),
        "3": lambda: mostrar_vuelos_por_origen(),
        "4": lambda: mostrar_vuelos_por_destino(),
        "5": lambda: mostrar_vuelos_por_estado(),
        "6": lambda: mostrar_vuelos_con_asientos(),
        "7": lambda: mostrar_todos_vuelos(),
        "8": lambda: menu_vuelos(aeropuertos, listaUsuario)
    }

    bandera = False
    while not bandera:
        opcion = validar_input(8)
        accion = opciones_vuelos.get(opcion)
        
        if accion:
            limpiar_consola()
            accion()
            if opcion == "8":
                return
            
            print(Fore.LIGHTRED_EX + "Presione enter para salir", flush=True)
            input()
            bandera = True
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

# Submenú de reservas
def menu_reservas(user, aeropuertos, listaUsuario):
   """Opciones relacionadas con reservas"""
   limpiar_consola()
   
   titulo = "RESERVAS"
   titulo_centrado = centrar_texto(titulo)
   print(Fore.LIGHTMAGENTA_EX + titulo_centrado + Fore.RESET)
   
   ancho_terminal = shutil.get_terminal_size().columns
   
   print(Fore.BLACK + "=" * ancho_terminal + Fore.RESET)
   print()
   
   opciones = [
       (f"{Fore.LIGHTMAGENTA_EX}1){Fore.WHITE} Reservar vuelo{Fore.RESET} 🎫"),
       (f"{Fore.LIGHTMAGENTA_EX}2){Fore.WHITE} Consultar reserva{Fore.RESET} 🔍"),
       (f"{Fore.LIGHTMAGENTA_EX}3){Fore.WHITE} Cancelar reserva{Fore.RESET} ❌"),
       (f"{Fore.LIGHTMAGENTA_EX}4){Fore.WHITE} Reserva sala VIP{Fore.RESET} 🌟"),
       (f"{Fore.LIGHTMAGENTA_EX}5){Fore.WHITE} Reserva de cochera{Fore.RESET} 🚗"),
       (f"{Fore.RED}6){Fore.WHITE} Volver al menú principal{Fore.RESET} 🔙")
   ]
   
   for opcion in opciones:
       print(opcion)
       print()
   
   opciones_reservas = {
       "1": lambda: repositorio_reservas.reservar_vuelo(),
       "2": lambda: repositorio_usuarios.consultarReserva(user),
       "3": lambda: repositorio_usuarios.cancelarReserva(user),
       "4": lambda: repositorio_reservas.reservaSalaVIP(user, aeropuertos, listaUsuario),
       "5": lambda: repositorio_reservas.reservaEstacionamiento(user, aeropuertos, listaUsuario),
       "6": lambda: consultante(aeropuertos, listaUsuario)
   }

   bandera = False
   while not bandera:
       opcion = validar_input(NUMERO_DE_OPCIONES_6)
       accion = opciones_reservas.get(opcion)
       
       if accion:
           accion()
           bandera = True
       else:
           print("Opción inválida. Por favor, seleccione una opción válida.")
	

		


def consultarAsientosDisponibles():
		"""
		Consulta y muestra los vuelos que tienen asientos disponibles.
		
		Utiliza la función filtrar_vuelos_asientos_disponibles() para obtener los vuelos
		con asientos libres y extrae sus números de vuelo para mostrarlos.
		
		Returns:
				None. Imprime por pantalla la lista de códigos de vuelos con asientos disponibles.
		"""
		mostrar_vuelos_con_asientos()
		print(Fore.LIGHTRED_EX + "Presione enter para salir", flush=True)
		input()
		return

def bienvenida():
    limpiar_consola()
    avioncito = '''
                             |
                       --====|====--
                             |  

                         .-"""""-. 
                       .'_________'. 
                      /_/_|__|__|_\\_\\
                     ;'-._       _.-';
,--------------------|    `-. .-'    |--------------------,
 ``""--..__    ___   ;       '       ;    ___    __..--""``
           `"-// \\\.._\\              /_..// \\\-"`
              \\\_//    '._        _.'    \\\_//
               `"`        ``---``         `"`
    '''


    escribir_ascii_lento(avioncito)

    bloquear_teclado(0.7)
    limpiar_consola()

    titulo = pyfiglet.figlet_format("Sistema de gestion de aeropuertos", font="standard")
    titulo_centrado = centrar_texto(titulo)
    
    print(Fore.LIGHTCYAN_EX + titulo_centrado)
    
    print(Fore.LIGHTBLACK_EX + "=" * shutil.get_terminal_size().columns)

    
    escribir_lento("\nGrupo 8: Guido Contartese - Frank Lopez - Ignacio Ramirez.", delay=0.02, color=Fore.LIGHTCYAN_EX)
    escribir_lento("\nPresione Enter para continuar...", delay=0.02, color=Fore.LIGHTCYAN_EX)
    input()


def main(primera_vez=True):
    """Función encargada de dirigir la ejecución completa de nuestro programa"""
    if primera_vez == True:
        bienvenida()
    limpiar_consola()
    titulo = "INGRESO"
    titulo_centrado = centrar_texto(titulo)
    print(Fore.LIGHTCYAN_EX + titulo_centrado + Fore.RESET)
    
    ancho_terminal = shutil.get_terminal_size().columns
    
    print(Fore.BLACK + "=" * ancho_terminal + Fore.RESET)
    print()
    
    opciones = [
        (f"{Fore.LIGHTGREEN_EX}1) {Fore.RESET}Registración de Usuario 📝"),
        (f"{Fore.LIGHTBLUE_EX}2) {Fore.RESET}Ingreso como Administrador 🔐"),
        (f"{Fore.LIGHTMAGENTA_EX}3) {Fore.RESET}Ingreso como Consultante 👤")
    ]
    
    for opcion in opciones:
        print(opcion)
        print()
    
    opciones_main = {
        "1": lambda: submenu_registracion(),
        "2": lambda: login_administrador(),
        "3": lambda: login_consultante()
    }
    
    def submenu_registracion():
        limpiar_consola()
        titulo = "REGISTRACIÓN"
        titulo_centrado = centrar_texto(titulo)
        print(Fore.LIGHTCYAN_EX + titulo_centrado + Fore.RESET)
        print(Fore.BLACK + "=" * ancho_terminal + Fore.RESET)
        print()
        
        opciones_registracion = [
            (f"{Fore.LIGHTGREEN_EX}1) {Fore.RESET}Registración de usuario {Fore.LIGHTGREEN_EX}Consultante{Fore.RESET} 👥"),
            (f"{Fore.LIGHTBLUE_EX}2) {Fore.RESET}Registración de usuario {Fore.LIGHTBLUE_EX}Administrador{Fore.RESET} 🛡️"),
            (f"{Fore.LIGHTRED_EX}3) {Fore.RESET}Volver Atrás 🔙")
        ]
        
        for opcion in opciones_registracion:
            print(opcion)
            print()
        
        def registrar_consultante():
            repositorio_usuarios.registracion_usuarios(False)
            limpiar_consola()
            print("Registración concretada")
            main(False)
        
        def registrar_administrador():
            validacion_codigos = repositorio_usuarios.validar_codigos_admin()
            if validacion_codigos:
                repositorio_usuarios.registracion_usuarios(True)
                limpiar_consola()
                print("Registración concretada")
                main(False)
            else:
                limpiar_consola()
                print("No cuenta con el código para registrarse como administrador.") 
                main(False)
        
        opciones_registro = {
            "1": registrar_consultante,
            "2": registrar_administrador,
            "3": lambda: main(False)
        }
        
        opcion = validar_input(NUMERO_DE_OPCIONES_3)
        accion = opciones_registro.get(opcion)
        
        if accion:
            accion()
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")
    
    def login_administrador():
        if repositorio_usuarios.inicio_sesion(True):
            administrador()
        else:
            limpiar_consola()
            print("Ha llegado al máximo de intentos posibles de inicio de sesión")
            main(False)
    
    def login_consultante():
        if repositorio_usuarios.inicio_sesion(False):
            consultante(listaAeropuertos, usuarios)
        else:
            limpiar_consola()
            print("Ha llegado al máximo de intentos posibles de inicio de sesión")
            main(False)
    
    opcion = validar_input(NUMERO_DE_OPCIONES_3)
    accion = opciones_main.get(opcion)
    
    if accion:
        accion()
    else:
        print("Opción inválida. Por favor, seleccione una opción válida.")
revision_vuelos_fecha(None)
main(True)

import repositorio_usuarios
from repositorio_vuelos import mostrar_mapa_terminal, ingresar_vuelo, mostrar_vuelos, modificacion_vuelo, eliminar_vuelo, filtrar_vuelos_asientos_disponibles, get_vuelos
from utils import validar_input, limpiar_consola
from repositorio_aeropuertos import get_aeropuertos
from repositorio_usuarios import getDataUser, usuarios
from utils import ingresar_fecha_y_hora, randonAprobado, writeFile, bloquear_teclado, readFile
from repositorio_pagos import tieneTarjeta, registrarTarjeta
import random
from datetime import timedelta

 
#Es solo para hacer mas legible el codigo y no tener magic numbers
NUMERO_DE_OPCIONES_1 = 1
NUMERO_DE_OPCIONES_2 = 2
NUMERO_DE_OPCIONES_3 = 3
NUMERO_DE_OPCIONES_4 = 4
NUMERO_DE_OPCIONES_5 = 5


listaDeVuelos = get_vuelos()
listaAeropuertos = get_aeropuertos()
				
def cerrar_sesion():
		limpiar_consola()
		print("Ha cerrado la sesión con éxito!")
		print("Volviendo al menú principal...")

		bloquear_teclado(2)
		limpiar_consola()
		main()

def imprimible_menu_regreso(funcion):
	bandera = False
	volver = input("seleccione 0 para volver al menu anterior o -1 para salir del sistema: ")
	while not bandera:    
		if volver == "0":
			bandera = True
			funcion()
		elif volver == "-1":
			print("Muchas gracias")
			bandera = True
		else:
			print("Seleccione un valor valido")
			volver = input("seleccione 0 para volver al menu anterior o -1 para salir del sistema: ")

def administrador():
	"""Listado de funciones disponibles que se pueden ejecutar Exclusivo de Administradores"""
	limpiar_consola()
	print("OPCIONES")
	print("""
				1. Ingresar vuelo al sistema.
				2. Modificar vuelo.
				3. Consulta de estados de vuelos.
				4. Eliminar vuelo.
				5. Cerrar Sesión.
				""")
	menu_opciones_administrador()

def menu_opciones_administrador():
	#Selecciona la opccion deseada
	bandera = True
	while bandera:
		opcion = validar_input(5)
		if opcion == "1":
			ingresar_vuelo(listaDeVuelos)
			administrador()
			bandera = False
		elif opcion == "2":
			modificacion_vuelo(listaDeVuelos)
			bandera = False
		elif opcion == "3":
			mostrar_vuelos(listaDeVuelos)
			bandera = False
		elif opcion == "4":
			eliminar_vuelo(listaDeVuelos)
			bandera = False
		elif opcion == "5":
			limpiar_consola()
			print("Ha cerrado la sesión con éxito!")
			bloquear_teclado(2)
			limpiar_consola()
			main()
			bandera = False
	imprimible_menu_regreso(administrador)
	#modificar

#Mostrar el menu
def consultante(aeropuertos, listaUsuario):
    """Listado de funciones disponibles Exclusivo de Consultante"""
    limpiar_consola()
    print("MENÚ PRINCIPAL")
    print("""
                1. Vuelos.
                2. Reservas.
                3. Registrar tarjeta.
                4. Cerrar sesión.
                """)
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
        opcion = validar_input(4)
        accion = opciones_principal.get(opcion)
        
        if accion:
            accion()
            bandera = True
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

    imprimible_menu_regreso(lambda: consultante(aeropuertos, listaUsuario))

# Submenú de vuelos
def menu_vuelos(aeropuertos, listaUsuario):
    """Opciones relacionadas con vuelos"""
    limpiar_consola()
    print("SUBMENÚ - VUELOS")
    print("""
                1. Consulta de vuelos.
                2. Consulta de vuelos con asientos disponibles.
                3. Mostrar mapa de vuelos.
                4. Volver al menú principal.
                """)
    opciones_vuelos = {
        "1": lambda: mostrar_vuelos(listaDeVuelos),
        "2": lambda: consultarAsientosDisponibles(),
        "3": lambda: mostrar_mapa_terminal(),
        "4": lambda: consultante(aeropuertos, listaUsuario)
    }

    bandera = False
    while not bandera:
        opcion = validar_input(4)
        accion = opciones_vuelos.get(opcion)
        
        if accion:
            accion()
            bandera = True
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

# Submenú de reservas
def menu_reservas(user, aeropuertos, listaUsuario):
    """Opciones relacionadas con reservas"""
    limpiar_consola()
    print("SUBMENÚ - RESERVAS")
    print("""
                1. Consultar reserva.
                2. Cancelar reserva.
                3. Reserva sala VIP.
                4. Reserva de cochera.
                5. Volver al menú principal.
                """)
    opciones_reservas = {
        "1": lambda: repositorio_usuarios.consultarReserva(user),
        "2": lambda: repositorio_usuarios.cancelarReserva(user),
        "3": lambda: reservaSalaVIP(user, aeropuertos, listaUsuario),
        "4": lambda: reservaEstacionamiento(user, aeropuertos, listaUsuario),
        "5": lambda: consultante(aeropuertos, listaUsuario)
    }

    bandera = False
    while not bandera:
        opcion = validar_input(5)
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
		vuelos_filtrados = filtrar_vuelos_asientos_disponibles()
		codigos_de_vuelos = []
		for vuelo in vuelos_filtrados:
				codigos_de_vuelos.append(vuelo["numero_vuelo"])

		print(codigos_de_vuelos)
		return

def reservaSalaVIP(user, aeropuertos, listaUsuario):
    valida = False
    bandera = False
    banderaReserva = False
    seleccionSala = 0
    salaValida = False
    archivoUser = "user.json"

    while not bandera:
        for index, aeropuerto in enumerate(aeropuertos):
            print(index + 1, aeropuerto["codigo"], aeropuerto["ciudad"])

        seleccion = int(input("Seleccione el aeropuerto donde se encuentra o quiere reservar: "))
        if 1 <= seleccion <= len(aeropuertos):
            if "salavip" in aeropuertos[seleccion - 1]:
                for ind, salaVIP in enumerate(aeropuertos[seleccion - 1]["salavip"]):
                    if salaVIP["reservados"] < salaVIP["capacidad"]:
                        print(ind + 1, "Nombre: ", salaVIP["nombre"], "Precio: ", salaVIP["precio"])

                while not salaValida:
                    try:
                        seleccionSala = int(input("Seleccione la sala: "))
                        if 1 <= seleccionSala <= len(aeropuertos[seleccion - 1]["salavip"]):
                            salaValida = True
                        else:
                            print("Por favor, ingrese un número de sala válido.")
                    except ValueError:
                        print("Entrada no válida. Por favor, ingrese un número.")

                fecha = ingresar_fecha_y_hora("fecha y hora de reserva")

                reservar = {
                    "aeropuerto": aeropuertos[seleccion - 1]["ciudad"],
                    "codigo": aeropuertos[seleccion - 1]["codigo"],
                    "fecha": fecha,
                    "salavip": aeropuertos[seleccion - 1]["salavip"][seleccionSala - 1]["nombre"]
                }

                print("Debe seleccionar o registrar una tarjeta para realizar el pago")
                while not banderaReserva:
                    tarjeta = tieneTarjeta(user)
                    if tarjeta:
                        valida = randonAprobado()
                        if valida:
                            aeropuertos[seleccion - 1]["salavip"][seleccionSala - 1]["reservados"] += 1
                            for usuario in listaUsuario:
                                if usuario["id"] == user["id"]:
                                    usuario["reservas"].append(reservar)
                                    listaUsuarioActualizado = readFile(archivoUser)
                                    writeFile(archivoUser, listaUsuarioActualizado, None)
                                    bandera = True
                                    banderaReserva = valida
                        else:
                            print("Fondos insuficientes")
                    else:
                        print("Ocurrió un problema")
        else:
            print("Seleccione un aeropuerto correctamente.")

    print("Reserva realizada con éxito", user)

	
def reservaEstacionamiento(user, aeropuertos, listaUsuario):
    flag = False
    reserva = False
    fechas_rango = []
    archivoUser = "user.json"
    
    while not flag:    
        # Mostrar aeropuertos disponibles
        for idx, aeropuerto in enumerate(aeropuertos):
            print(f"{idx + 1}. {aeropuerto['codigo']} - {aeropuerto['ciudad']}")
        
        # Seleccionar aeropuerto
        seleccion = int(input("Seleccione el aeropuerto donde quiere reservar: "))
        if 1 <= seleccion <= len(aeropuertos):
            aeropuerto_seleccionado = aeropuertos[seleccion - 1]
            
            if "estacionamiento" in aeropuerto_seleccionado:
                estacionamiento = aeropuerto_seleccionado["estacionamiento"]
                
                fechaInicio = ingresar_fecha_y_hora("fecha y hora de inicio de estacionamiento")
                fechaFin = ingresar_fecha_y_hora("fecha y hora de fin de estacionamiento")
                while fechaFin <= fechaInicio:
                    print("La fecha de fin de estacionamiento debe ser posterior a la de inicio. Intente nuevamente.\n")
                    fechaFin = ingresar_fecha_y_hora("fecha y hora de fin de estacionamiento")
                # Lista de fechas en el rango		
                fechas_rango.append(fechaInicio)
                    

                # Verificar disponibilidad en todas las fechas del rango
                lugares_disponibles = []
                for letra, capacidad in estacionamiento["lugares"].items():
                    for i in range(1, capacidad + 1):
                        lugar = f"{letra}{i}"
                        # Verificar que el lugar esté disponible en todas las fechas del rango
                        lugar_disponible = all(
                            lugar not in estacionamiento["reservados"].get(fecha, [])
                            for fecha in fechas_rango
                        )
                        if lugar_disponible:
                            lugares_disponibles.append(lugar)

                if lugares_disponibles:
                    lugarSeleccionado = random.choice(lugares_disponibles)
                    reservar = {
                        "aeropuerto": aeropuerto_seleccionado["ciudad"],
                        "codigo": aeropuerto_seleccionado["codigo"],
                        "fechainicio": str(fechaInicio),
                        "fechafin": str(fechaFin),
                        "estacionamiento": lugarSeleccionado
                    }
                    
                    print("Debe seleccionar o registrar una tarjeta para realizar el pago")
                    while not reserva:
                        tarjeta = tieneTarjeta(user)
                        if tarjeta:
                            valida = randonAprobado()
                            if valida:
                                # Corregir la lógica de guardado de reservas
                                for fecha in fechas_rango:
                                    if fecha not in estacionamiento["reservados"]:
                                        estacionamiento["reservados"][fecha] = []
                                    estacionamiento["reservados"][fecha].append(lugarSeleccionado)
                                
                                for usuario in listaUsuario:
                                    if usuario["id"] == user["id"]:
                                        usuario["reservas"].append(reservar)
                                        writeFile(archivoUser, listaUsuario, None)
                                        flag = True
                                        reserva = True
                                print(f"Lugar {lugarSeleccionado} reservado para {user['usuario']} desde {fechaInicio} hasta {fechaFin}")
                            else:
                                print("Fondos insuficientes")
                                break
                else:
                    print(f"No hay lugares disponibles para el rango de fechas {fechaInicio} a {fechaFin}")
            else:
                print("Este aeropuerto no tiene estacionamiento disponible.")
        else:
            print("Selección inválida. Por favor, elija un aeropuerto válido.")



def main():
	"""Función encargada de dirigir la ejecución completa de nuestro programa"""
	limpiar_consola()
	print("""Ingrese la opción (numero) que quiera ejecutar:
	-1) Registración de usuario Consultante/Administrador.
	-2) Ingreso como Administrador.
	-3) Ingreso como Consultante.""")
	opcion = validar_input(NUMERO_DE_OPCIONES_3)
	if(opcion == "1"):
		print("""Ingrese la opción (numero) que quiera ejecutar:
		-1) Registración de usuario Consultante.
		-2) Registración de usuario Administrador.""")
		opcion = validar_input(NUMERO_DE_OPCIONES_2)
		if(opcion == "1"):
			repositorio_usuarios.registracion_usuarios(False)
			limpiar_consola()
			print("Registracion concretada")
			main()
		else:
			validacion_codigos = repositorio_usuarios.validar_codigos_admin()
			if validacion_codigos:
				repositorio_usuarios.registracion_usuarios(True)
				limpiar_consola()
				print("Registracion concretada")
				main()       
			else:
				limpiar_consola()
				print("No cuenta con el código para registrarse como administrador.") 
				main()
				
	elif(opcion == "2"):
		if(repositorio_usuarios.inicio_sesion(True)):
			administrador()
		else:
			limpiar_consola()
			print("Ha llegado al máximo de intentos posibles de inicio de sesion")
			main()
	else:
		if(repositorio_usuarios.inicio_sesion(False)):
			consultante(listaAeropuertos, usuarios)
		else:
			limpiar_consola()
			print("Ha llegado al máximo de intentos posibles de inicio de sesion")
			main()

main()
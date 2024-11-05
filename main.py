from time import sleep
import repositorio_usuarios
from repositorio_vuelos import ingresar_vuelo, mostrar_vuelos, modificacion_vuelo, eliminar_vuelo, filtrar_vuelos_asientos_disponibles
from utils import validar_input, limpiar_consola
from repositorio_aviones import avion_asignado
from repositorio_aeropuertos import get_aeropuertos
from repositorio_usuarios import getDataUser
from utils import validarFecha, randonAprobado
from repositorio_pagos import tieneTarjeta
import random
from datetime import datetime, timedelta

 
#Es solo para hacer mas legible el codigo y no tener magic numbers
NUMERO_DE_OPCIONES_1 = 1
NUMERO_DE_OPCIONES_2 = 2
NUMERO_DE_OPCIONES_3 = 3
NUMERO_DE_OPCIONES_4 = 4
NUMERO_DE_OPCIONES_5 = 5

user = getDataUser()
  
        
def cerrar_sesion():
    limpiar_consola()
    print("Ha cerrado la sesión con éxito!")
    print("Volviendo al menú principal...")

    sleep(2)
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
      ingresar_vuelo()
      administrador()
      bandera = False
    elif opcion == "2":
      modificacion_vuelo()
      bandera = False
    elif opcion == "3":
      mostrar_vuelos()
      bandera = False
    elif opcion == "4":
      eliminar_vuelo()
      bandera = False
    elif opcion == "5":
      limpiar_consola()
      print("Ha cerrado la sesión con éxito!")
      sleep(2)
      limpiar_consola()
      main()
      bandera = False
  imprimible_menu_regreso(administrador)
  #modificar

#Mostrar el menu
def consultante():
  """Listado de funciones disponibles Exclusivo de Consultante"""
  limpiar_consola()
  print("OPCIONES")
  print("""
    OPCIONES
        1. Consulta de vuelos.
        2. Consulta de vuelos con asientos disponibles.
        3. Consultar reserva.
        4. Cancelar reserva.
        5. Reserva sala VIP.
        6. Reserva de cochera.
        7. Cerrar sesión.
        """)
  menu_opciones_consultante()



def menu_opciones_consultante():
  """"Menu de opciones de usuario consultante"""
  opciones = {
      "1": mostrar_vuelos,
      "2": consultarAsientosDisponibles,
      "3": consultarReserva,
      "4": cancelarReserva,
      "5": lambda: reservaSalaVIP(user),
      "6": lambda: reservaEstacionamiento(user),
      "7": cerrar_sesion
  }
  
  bandera = False
  while not bandera:
      opcion = validar_input(8)  # Recoge la opción
      accion = opciones.get(opcion)  # Obtiene la función asociada a la opción
      
      if accion:
          accion()  # Llama a la función
          bandera = True
      else:
          print("Opción inválida. Por favor, seleccione una opción válida.")

  imprimible_menu_regreso(consultante)

    


def consultarAsientosDisponibles():

  vuelos_filtrados = filtrar_vuelos_asientos_disponibles()
  codigos_de_vuelos = []
  for vuelo in vuelos_filtrados:
    codigos_de_vuelos.append(vuelo["numero_vuelo"])

  print(codigos_de_vuelos)
  return

def reservaSalaVIP(user):
  valida = False
  aeropuertos = get_aeropuertos()
  counterSala = 0
  bandera = False
  fechaValida = False
  banderaReserva = False
  seleccionSala = 0
  while not bandera:    
    for index, aeropuerto in enumerate(aeropuertos):

      print(index + 1 ,aeropuerto["codigo"], aeropuerto["ciudad"])
    seleccion = int(input("Seleccione el aeropuerto donde se encuentra o quiere reservar: "))
    if 1 <= seleccion <= len(aeropuertos):
      if "salavip" in aeropuertos[seleccion - 1]:
        for ind, salaVIP in enumerate(aeropuertos[seleccion - 1]["salavip"]):
          counterSala += 1 
          if salaVIP["reservados"] < salaVIP["capacidad"]:
            print(ind + 1, "Nombre: ", salaVIP["nombre"], "Precio: ",  salaVIP["precio"]  )
        seleccionSala = int(input("Seleccione la sala: "))
        while not fechaValida:
           fecha = input("Inque en que fecha DD/MM/AAAA: ")
           fechaValida, _ = validarFecha(fecha)
           if fechaValida:
             reservar = {
               "aeropuerto": aeropuertos[seleccion - 1]["ciudad"],
               "codigo": aeropuertos[seleccion - 1]["codigo"],
               "fecha": fecha,
               "salavip":  aeropuertos[seleccion - 1]["salavip"][seleccionSala - 1]["nombre"]
             }
             print("Debe seleccionar o registar una tarjeta para realizar el pago")
             while not banderaReserva:
               tarjeta = tieneTarjeta(user)
               if tarjeta:
                 valida = randonAprobado()
                 if valida:
                   aeropuertos[seleccion - 1]["salavip"][seleccionSala - 1]["reservados"] += 1
                   if "reservas" in user:
                     user["reservas"].append(reservar)
                     bandera = True
                     banderaReserva = valida
                   else:
                     user["reservas"] = [reservar]
                     bandera = True
                     banderaReserva = valida
                 else:
                   print("Fondo insuficiente")
               else:
                 print("Ocurrio un problema")
           else:
             print("Fecha no valida")
             fechaValida = False
             bandera = False
    else:
      seleccion = input("Seleccione un aeropuerto correctamente: ")
  print("Reserva realizada, con exito", user)

  
def reservaEstacionamiento(user):
    aeropuertos = get_aeropuertos()
    flag = False
    reserva = False
    validaFechaInicio = False
    validaFechaFin = False
    fechas_rango = []
    
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
                
                while not validaFechaInicio:
                  inicioFecha = input("Ingrese la fecha de inicio de la reserva (DD/MM/AAAA): ")
                  validaFechaInicio, fechaInicio = validarFecha(inicioFecha)
                  if not validaFechaInicio:
                    print("Fecha no valida, agregue una fecha valida ")

                while not validaFechaFin:
                  finFecha = input("Ingrese la fecha de fin de la reserva (DD/MM/AAAA ): ")
                  validaFechaFin, fechaFin = validarFecha(finFecha)
                  if not validaFechaFin:
                    print("Fecha no valida, agregue una fecha valida ")

                # Lista de fechas en el rango
                fecha_actual = fechaInicio
                while fecha_actual <= fechaFin:
                    fechas_rango.append(fechaInicio.strftime("%d/%m/%Y"))
                    fecha_actual += timedelta(days=1)

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
                    # Seleccionar un lugar aleatoriamente
                    lugarSeleccionado = random.choice(lugares_disponibles)

                    reservar = {
                     "aeropuerto": aeropuertos[seleccion - 1]["ciudad"],
                     "codigo": aeropuertos[seleccion - 1]["codigo"],
                     "fechainicio": fechaInicio,
                     "fechafin": fechaFin,
                     "estacionamiento": lugarSeleccionado
                   }
                    
                    print("Debe seleccionar o registar una tarjeta para realizar el pago")
                    while not reserva:
                      tarjeta = tieneTarjeta(user)
                      if tarjeta:
                        valida = randonAprobado()
                        if valida:
                          for fecha in fechas_rango:
                            if fecha not in estacionamiento["reservados"]:
                              estacionamiento["reservados"][fecha] = []  
                              estacionamiento["reservados"][fecha].append(lugarSeleccionado)
                          if "reservas" in user:
                            user["reservas"].append(reservar)
                            flag = True
                            reserva = valida
                          else:
                            user["reservas"] = [reservar]
                            flag = True
                            reserva = valida
                        else:
                          print("Fondo insuficiente")
                    print(f"Lugar {lugarSeleccionado} reservado para {user['usuario']} desde {fechaInicio} hasta {fechaFin}")
                else:
                    print(f"No hay lugares disponibles para el rango de fechas {fechaInicio} a {fechaFin}")
            else:
                print("Este aeropuerto no tiene estacionamiento disponible.")
        else:
            print("Selección inválida. Por favor, elija un aeropuerto válido.")

def consultarReserva():
  pass

def cancelarReserva():
  pass

# Podríamos modularizar este código
# Si modularizamos mucho el código podemos volver para atras (ejemplo, si hay un error  algo volvemos a llamar a la funcion y estamos parados en el mismo lugar que antes)
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
      repositorio_usuarios.registracion_usuarios(False) ##parece que pueden acceder a las variables sin el get -> preguntar a la profe
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
    #se me ocurre que podríamos tener una variable tipo current_user para saber qué tipo de usuario es el actual
    #podemos pasarle el current_user a las funciones que hagan cosas y que determinen qué cosas pueden o no hacer
    if(repositorio_usuarios.inicio_sesion(True)):
      administrador()
    else:
      limpiar_consola()
      print("Ha llegado al máximo de intentos posibles de inicio de sesion")
      main()
  else:
    if(repositorio_usuarios.inicio_sesion(False)):
      consultante()
    else:
      limpiar_consola()
      print("Ha llegado al máximo de intentos posibles de inicio de sesion")
      main()

main()
from os import system
from time import sleep
import repositorio_usuarios
from repositorio_vuelos import ingresar_vuelo, mostrar_vuelos, consultar_estado_vuelo
from utils import validar_input
from repositorio_aviones import avion_asignado
 
 
#Es solo para hacer mas legible el codigo y no tener magic numbers
NUMERO_DE_OPCIONES_1 = 1
NUMERO_DE_OPCIONES_2 = 2
NUMERO_DE_OPCIONES_3 = 3
NUMERO_DE_OPCIONES_4 = 4
NUMERO_DE_OPCIONES_5 = 5



def eliminacion_vuelo(current_user):
  # if current_user != admin: return // Al menos con los codigos ya es un poco mas seguro el código (igual no se si importa acá)
  print("Ingrese el número de vuelo que quiere eliminar")
  numero_vuelo = input()
  print("""Estas seguro de que queres eliminar un vuelo? No se puede volver atrás:
  -1) Estoy seguro, eliminar.
  -2) Me arrepiento.""")
  segundo_input = validar_input(NUMERO_DE_OPCIONES_2)
  if segundo_input == 2:
    return False
  elif segundo_input == 1:
    validacion_codigos = repositorio_usuarios.validar_codigos_admin()
    if validacion_codigos == False:
      return "EXCEPCION Usuario bloqueado" #A definir
    return eliminacion_vuelo(numero_vuelo) #como no manejamos excepciones los returns son variados. Acá devuelve true -> si pudo eliminar ; false ->si no
  else: return "EXCEPCION Error al eliminar vuelo"
  
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
  system("cls")
  print("OPCIONES")
  print("""
        1. Ingresar vuelo al sistema.
        2. Modificar vuelo.
        3. Consulta de estados de vuelos.
        4. Cerrar Sesión.
        """)
  menu_opciones_administrador()

def menu_opciones_administrador():
  #Selecciona la opccion deseada
  bandera = True
  while bandera:
    opcion = validar_input(4)
    if opcion == "1":
      ingresar_vuelo()
      administrador()
      bandera = False
    elif opcion == "2":
      #consultarVuelosPartidos()
      bandera = False
    elif opcion == "3":
      mostrar_vuelos()
      bandera = False
    elif opcion == "4":
      system("cls")
      print("Ha cerrado la sesión con éxito!")
      sleep(2)
      system("cls")
      main()
      bandera = False
    else:
      print("Ingrese una opcion valida")
  imprimible_menu_regreso(administrador)
  #modificar

#Mostrar el menu
def consultante():
  """Listado de funciones disponibles Exclusivo de Consultante"""
  system("cls")
  print("OPCIONES")
  print("""
        1. Consulta de vuelos.
        2. Consulta de vuelos con asientos disponibles.
        3. Consultar estado de vuelo.
        4. Consultar reserva.
        5. Cancelar reserva.
        6. Cerrar sesión.
        """)
  menu_opciones_consultante()


def menu_opciones_consultante():
  #Selecciona la opccion deseada
  bandera = False
  while not bandera:
    opcion = input("Ingrese la opcion que desee: ")
    if opcion == "1":
      mostrar_vuelos()
      bandera = True
    elif opcion == "2":
      consultarAsientosDisponibles()
      bandera = True
    elif opcion == "3":
      consultar_estado_vuelo()
      bandera = True
    elif opcion == "4":
      consultarReserva()
      bandera = True
    elif opcion == "5":
      cancelarReserva()
      bandera = True
    elif opcion == "6":
      system("cls")
      print("Ha cerrado la sesión con éxito!")
      sleep(2)
      system("cls")
      main()
    else:
      print("Ingrese una opcion valida")
      bandera = False
  imprimible_menu_regreso(consultante)


  
    


def consultarAsientosDisponibles():
  pass


  

def consultarReserva():
  pass

def cancelarReserva():
  pass

# Podríamos modularizar este código
# Si modularizamos mucho el código podemos volver para atras (ejemplo, si hay un error  algo volvemos a llamar a la funcion y estamos parados en el mismo lugar que antes)
def main():
  """Función encargada de dirigir la ejecución completa de nuestro programa"""
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
      system("cls")
      print("Registracion concretada")
      main()
    else:
      validacion_codigos = repositorio_usuarios.validar_codigos_admin()
      if validacion_codigos:
        repositorio_usuarios.registracion_usuarios(True)
        system("cls")
        print("Registracion concretada")
        main()       
      else:
        system("cls")
        print("No cuenta con el código para registrarse como administrador.") 
        main()
        
  elif(opcion == "2"):
    #se me ocurre que podríamos tener una variable tipo current_user para saber qué tipo de usuario es el actual
    #podemos pasarle el current_user a las funciones que hagan cosas y que determinen qué cosas pueden o no hacer
    if(repositorio_usuarios.inicio_sesion(True)):
      administrador()
    else:
      system("cls")
      print("Ha llegado al máximo de intentos posibles de inicio de sesion")
      main()
  else:
    if(repositorio_usuarios.inicio_sesion(False)):
      consultante()
    else:
      system("cls")
      print("Ha llegado al máximo de intentos posibles de inicio de sesion")
      main()

main()
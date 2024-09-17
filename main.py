from os import system
import repositorio_usuarios
import repositorio_vuelos
 
 
#Es solo para hacer mas legible el codigo y no tener magic numbers
NUMERO_DE_OPCIONES_1 = 1
NUMERO_DE_OPCIONES_2 = 2
NUMERO_DE_OPCIONES_3 = 3
NUMERO_DE_OPCIONES_4 = 4
NUMERO_DE_OPCIONES_5 = 5


def validar_input(cantidad_de_opciones):
    opcion = input()
    opciones_validas = []
    for i in range(1,cantidad_de_opciones +1):
        opciones_validas.append(str(i))
    
    while opcion not in opciones_validas:
        opcion = input("Ingrese una opción válida: ")
    
    return opcion


def modificacion_vuelo(current_user):
  # if current_user != admin: return ; esto es lo que dije más abajo
  print("""Ingrese la opción (numero) que quiera modificar:
  -1) Estado del vuelo.
  -2) Destino.
  -3) Fecha-hora de salida.
  -4) Fecha-hora de llegada""")
  opcion = validar_input(NUMERO_DE_OPCIONES_4)

  if opcion == 1:
    print("""Ingrese el nuevo estado:
  -1) En horario.
  -2) Retrasado.
  -3) Cancelado.""")  
    estado = validar_input(NUMERO_DE_OPCIONES_3)

    if estado == "1":
      estado = "En horario"
    elif estado == "2":
      estado = "Retrasado"
    elif estado == "3":
      estado = "Cancelado"
    else:
     return "Error asignando estado" #Acá deberíamos volver a llamar a la funcion en realidad
    
    id = input("Inserte el numero de vuelo: ")
    repositorio_vuelos.modificar_estado_vuelos(id, estado)

    ## Continuar con el resto de modificaciones
  return

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
  





def administrador():
  """Listado de funciones disponibles Exclusivo de Administradores"""
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
  bandera = False
  while not bandera:
    opcion = input("Ingrese la opcion que desee: ")
    if opcion == "1":
      repositorio_vuelos.ingresar_vuelo()
      bandera = True
    elif opcion == "2":
      consultarVuelosPartidos()
      bandera = True
    elif opcion == "3":
      consultarVuelos()
      bandera = True
    elif opcion == "4":
      consultarAsientosDisponibles()
      bandera = True
    else:
      print("Ingrese una opcion valida")
  #modificar

#Mostrar el menu
def consultante():
  """Listado de funciones disponibles Exclusivo de Consultante"""
  system("cls")
  print("OPCIONES")
  print("""
        1. Consultar vuelos arribados.
        2. Consulta de vuelos partidos.
        3. Consulta de vuelos.
        4. Consulta de vuelos con asientos disponibles.
        5. Consulta de estados de vuelos.
        6. Consulta de reserva de vuelos.
        7. Cancelar reserva.
        """)
  menu_opciones_consultante()
  


def menu_opciones_consultante():
  #Selecciona la opccion deseada
  bandera = False
  while not bandera:
    opcion = input("Ingrese la opcion que desee: ")
    if opcion == "1":
      consultarVuelosArribados()
      bandera = True
    elif opcion == "2":
      consultarVuelosPartidos()
      bandera = True
    elif opcion == "3":
      consultarVuelos()
      bandera = True
    elif opcion == "4":
      consultarAsientosDisponibles()
      bandera = True
    elif opcion == "5":
      consultarEstadoDeVuelo()
      bandera = True
    elif opcion == "6":
      consultarReserva()
      bandera = True
    elif opcion == "7":
      cancelarReserva()
      bandera = True
    else:
      print("Ingrese una opcion valida")
      bandera = False

def consultarVuelosArribados():
  vuelosArribados = repositorio_vuelos.get_vuelos()
  for vuelo in vuelosArribados:
    if vuelo[4] == "Arribado":
      print("=================\n"
        f"El vuelo {vuelo[0]} \n"
        f"de la aerolinea {vuelo[1]} \n"
        f"Esta {vuelo[4]} \n"
        "=================\n"
            )

def consultarVuelosPartidos():
  pass

def consultarVuelos():
  pass

def consultarAsientosDisponibles():
  pass

def consultarEstadoDeVuelo():
  pass

def consultarReserva():
  pass

def cancelarReserva():
  pass

# Podríamos modularizar este código
# Si modularizamos mucho el código podemos volver para atras (ejemplo, si hay un error  algo volvemos a llamar a la funcion y estamos parados en el mismo lugar que antes)
def main():
  usuarios_consultantes = repositorio_usuarios.get_usuarios_consultantes()
  usuarios_admin = repositorio_usuarios.get_usuarios_admin()
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
      if validacion_codigos == False:
        return "EXCEPCION Usuario bloqueado" #A definir
      repositorio_usuarios.registracion_usuarios(True)
      system("cls")
      print("Registracion concretada")
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

print(main())
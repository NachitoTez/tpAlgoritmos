from os import system
from repositorio_vuelos import *
from repositorio_usuarios import *

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
    modificar_estado_vuelos(id, estado)

    ## Continuar con el resto de modificaciones
  return

def eliminacion_vuelo(current_user):
  vuelos = get_vuelos()
  # if current_user != admin: return
  print("""Ingrese el número de vuelo que quiere eliminar""")
  opcion = input()
  print("""¿Está segurisimo que quiere hacer esto?""")

  return
def chequeo_usuario_existente(lista_usuarios, nuevo_usuario):
  """Funcion a utilizar para chequear si el nombre del nuevo usuario no se encuentra ya en el sistema"""
  bandera = False
  for usuario in lista_usuarios:
    if usuario[0] == nuevo_usuario:
      bandera = True
  return bandera

def registracion_usuarios(lista_usuarios):
  """Funcion a utilizar para poder hacer la registracion de un nuevo usuario, mejoras a implementar a futuro,
   cuando falla el registro por usuario O contrasenia te diga mas especificamente el porque"""
  system("cls")
  usuario = ""
  contrasenia = ""
  usuario = input("Ingrese el usuario a utilizar en el sistema: ")
  while usuario == "" or chequeo_usuario_existente(lista_usuarios, usuario):
     usuario = input("Ingrese un usuario a utilizar en el sistema que sea correcto: ")
  contrasenia = input("Ingrese la contrasenia a utilizar en el sistema, debe tener minimo 6 digitos y un maximo de 12 digitos: \n")
  while contrasenia == "" or len(contrasenia) < 6 or len(contrasenia) > 12:
     contrasenia = input("Ingrese una contrasenia a utilizar en el sistema que sea correcta: \n")
  lista_usuarios.append([usuario, contrasenia])

def administrador():
  pass

def consultante():
  pass


# Podríamos modularizar este código
# Si modularizamos mucho el código podemos volver para atras (ejemplo, si hay un error  algo volvemos a llamar a la funcion y estamos parados en el mismo lugar que antes)
def main():
  usuarios_consultantes = get_usuarios_consultantes()
  codigos_admin = get_codigos_admin()
  usuarios_admin = get_usuarios_admin()
  print("""Ingrese la opción (numero) que quiera ejecutar:
  -1) Registración de usuario Consultante/Administrador.
  -2) Ingreso como Administrador.
  -3) Ingreso como Consultante.""")
  opcion = input()
  while opcion != "1" and opcion != "2" and opcion != "3":
    opcion = input("Ingrese una opción valida: ")
  if(opcion == "1"):
    print("""Ingrese la opción (numero) que quiera ejecutar:
    -1) Registración de usuario Consultante.
    -2) Registración de usuario Administrador.""")
    opcion = input()
    while opcion != "1" and opcion != "2" :
      opcion = input("Ingrese una opción valida: ")
    if(opcion == "1"):
      registracion_usuarios(usuarios_consultantes) ##parece que pueden acceder a las variables sin el get -> preguntar a la profe
    else:
      validacion = int(input("Ingrese el codigo de acceso para registrarse como nuevo administrador: "))
      if validacion in codigos_admin:
        registracion_usuarios(usuarios_admin)
      else:
        system("cls")
        print("Código inválido, lo devolveremos al menu principal")
        main()
  elif(opcion == "2"):
    #se me ocurre que podríamos tener una variable tipo current_user para saber qué tipo de usuario es el actual
    #podemos pasarle el current_user a las funciones que hagan cosas y que determinen qué cosas pueden o no hacer
    administrador()
  else:
    consultante()
main()
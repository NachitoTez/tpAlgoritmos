from os import system
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

def main():
  usuarios_consultantes= [["guido", "holabebe"], ["matias", "123456"]]
  usuarios_admin = [["nacho", "playstation"], ["yiya", "654321"]]
  codigos_admin = [415465, 11123, 999846] #Codigos que debe al momento de registrarse un nuevo admin debera tener uno de ellos para validar el registro
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
      registracion_usuarios(usuarios_consultantes)
    else:
      validacion = int(input("Ingrese el codigo de acceso para registrarse como nuevo administrador: "))
      if validacion in codigos_admin:
        registracion_usuarios(usuarios_admin)
      else:
        system("cls")
        print("Código inválido, lo devolveremos al menu principal")
        main()
  elif(opcion == "2"):
    administrador()
  else:
    consultante()
main()
from os import system, name
import json
archivoUser = "user.json"
#Como todavía no sabemos trabajar con archivos, en este repositorio vamos a generar los datos de prueba temporalmente.
#Para manipular los datos se van a llamar a funciones creadas en este repositorio, las cuales nos van a permitir no
#modificar la lógica de la funcion main/de la funcion que llame a los datos del repositorio.
#Una vez que cambiemos a archivos se reemplazan los datos de prueba con el acceso al archivo y todo seguiría funcionando igual



codigos_admin = [415465, 11123, 999846] #Codigos que debe tener al momento de registrarse un nuevo admin para validar el registro
userLoguin = {}
def getUser(nombreArchivo):
    try:
        with open(nombreArchivo, "rt") as archivo:
            usuarios = json.load(archivo)
            return usuarios
    except (FileExistsError(), json.JSONDecodeError):
        usuarios = []


def limpiar_consola():
    if name == "nt":  # Windows
        system("cls")
    else:  # macOS y Linux
        system("clear")
    return

def validar_codigos_admin():
    """Función encargada de validar si el nuevo usuario que quiere registrarse como administrador cuenta
    con alguno de los códigos validadores que le permitan registrarse como tal.
    Devuelve True en caso de que haya sido exitosa la validación"""
    MAXIMO_INTENTOS_CODIGOS_ADMIN = 3
    validacion = int(input("Ingrese el código de administrador para poder registrarse: "))
    intentos = 1
    while validacion not in codigos_admin and intentos < MAXIMO_INTENTOS_CODIGOS_ADMIN:
        validacion = int(input("Código incorrecto, ingréselo nuevamente: "))
        intentos += 1
    if intentos == MAXIMO_INTENTOS_CODIGOS_ADMIN and validacion not in codigos_admin:
        return False
    return True

def validar_usuario_registrado(usuario, contrasenia, privilegio):
    """Función encargada de validar si el usuario que intenta ingresar al sistema esta registrado.
    Utilizo una bandera y filtro mi listado de usuarios segun el tipo de privilegio, luego por cada 
    Recibe 3 parametros: Usuario, Contrasenia y privilegio(admin(true) o no(false))"""
    with open(archivoUser, "rt") as archivo:
        usuarios = json.load(archivo)
        consultante= list(filter(lambda usuario: usuario["admin"] == privilegio, usuarios))
    bandera = 0
    for user in consultante:
        for clave, valor in user.items():
            if clave == "usuario" and valor == usuario or clave=="contrasenia" and valor == contrasenia:
                userLoguin.update(user)
                bandera+=1
        if bandera == 2: #Consulto en este paso si es que ya se encontro con el usuario y contrasenia buscado.
            return True
        else:
            bandera=0 #Si 2 usuarios comparten contrasenia en este caso limpiaremos la variable bandera para no confundir la validacion.
    return False

    
def inicio_sesion(privilegio):
    """Funcion principal de inicio de sesion llamada desde el main, la misma recibe por parámetro que tipo de usuario esta intentando iniciar sesión, admin o no.
    Devuelve True en caso de inicio de sesion y False si la misma no fue exitosa"""
    usuario = input("Ingrese su nombre de usuario: ").lower()
    contrasenia = input("Ingrese su contraseña de usuario: ")
    CANTIDAD_INTENTOS = 3
    intentos = 1
    while not(validar_usuario_registrado(usuario, contrasenia, privilegio)) and intentos<3:
            print("Usuario o contraseña inválidos")
            usuario = input("Ingrese su nombre de usuario: ").lower()
            contrasenia = input("Ingrese su contraseña de usuario: ")
            intentos+=1
    if intentos >= CANTIDAD_INTENTOS and not validar_usuario_registrado(usuario, contrasenia, privilegio):
        return False
    else:
        return True

def chequeo_usuario_existente(nuevo_usuario):
    """Funcion a utilizar para chequear si el nombre del nuevo usuario no se encuentra ya en el sistema.
    Recibe por parámetro el nombre de usuario a ingresar al sistema y devuelve True si ya se encuentra o
    False si no."""
    usuarios = getDataUser()
    bandera = False
    for user in usuarios:
        for clave, valor in user.items():
            if clave == "usuario" and valor == nuevo_usuario:
                bandera = True
    return bandera
  
def registracion_usuarios(privilegio):
  """Funcion a utilizar para poder hacer la registracion de un nuevo usuario. Recibe por parametro el tipo de usuario a registrar
  True= Admin"""
  limpiar_consola()
  usuario = ""
  contrasenia = ""
  usuarios = getUser(archivoUser)
  print(usuarios)
  usuario = input("Ingrese el usuario a utilizar en el sistema: ").lower()
  while usuario == "" or chequeo_usuario_existente(usuario):
     usuario = input("Ingrese un usuario a utilizar en el sistema que sea correcto o que no se este utilizando: \n").lower()
  contrasenia = input("Ingrese la contrasenia a utilizar en el sistema, debe tener minimo 6 digitos y un maximo de 12 digitos: \n")
  while contrasenia == "" or len(contrasenia) < 6 or len(contrasenia) > 12:
     contrasenia = input("Ingrese una contrasenia a utilizar en el sistema que sea correcta: \n")
  try:
    with open(archivoUser, "w") as archivo:
        nuevoUsuario = {"admin":privilegio, "usuario":usuario, "contrasenia":contrasenia}
        usuarios.append(nuevoUsuario)
        json.dump(usuarios, archivo, indent = 4) 
        print("Usuario creado exitosamente...")
  except ValueError as e:
            print(e)   
  return

def getDataUser():
    return userLoguin
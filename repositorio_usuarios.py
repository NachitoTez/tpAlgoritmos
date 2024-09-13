from os import system
#Como todavía no sabemos trabajar con archivos, en este repositorio vamos a generar los datos de prueba temporalmente.
#Para manipular los datos se van a llamar a funciones creadas en este repositorio, las cuales nos van a permitir no
#modificar la lógica de la funcion main/de la funcion que llame a los datos del repositorio.
#Una vez que cambiemos a archivos se reemplazan los datos de prueba con el acceso al archivo y todo seguiría funcionando igual

usuarios=[{"admin": True, "usuario":"nacho", "contrasenia":"playstation"},
           {"admin": True, "usuario":"yiya", "contrasenia":"654321"},
           {"admin": False, "usuario":"guido", "contrasenia":"holabebe"},
           {"admin": False, "usuario":"matias", "contrasenia":"123456"}]
codigos_admin = [415465, 11123, 999846] #Codigos que debe tener al momento de registrarse un nuevo admin para validar el registro


def get_codigos_admin():
    return codigos_admin

def validar_codigos_admin():
    MAXIMO_INTENTOS_CODIGOS_ADMIN = 5
    validacion = int(input("Ingrese el código de administrador para poder registrarse: "))
    intentos = 1
    while validacion not in codigos_admin and intentos < MAXIMO_INTENTOS_CODIGOS_ADMIN:
        validacion = int(input("Código incorrecto, ingréselo nuevamente: "))
        intentos += 1
    if intentos == MAXIMO_INTENTOS_CODIGOS_ADMIN and validacion not in codigos_admin:
        return False
    return True

def validar_usuario_registrado(usuario, contrasenia, privilegio):
    consultante= list(filter(lambda usuario: usuario.get("admin") == privilegio, usuarios))
    bandera = 0
    for user in consultante:
        for clave, valor in user.items():
            if clave == "usuario" and valor == usuario or clave=="contrasenia" and valor == contrasenia:
                bandera+=1
    return bandera==2


def validar_ingreso_usuario(funcion, usuario, contrasenia):
    """Valido los intentos de inicio de sesion de los usuarios"""
    CANTIDAD_INTENTOS = 3
    intentos = 1
    while not(funcion(usuario, contrasenia)) and intentos<3:
            print("Usuario o contraseña inválidos")
            usuario = input("Ingrese su nombre de usuario: ").lower()
            contrasenia = input("Ingrese su contraseña de usuario: ")
            intentos+=1
    if intentos >= CANTIDAD_INTENTOS and not funcion(usuario, contrasenia):
        return False
    else:
        return True
    
def inicio_sesion(privilegio):
    """Funcion principal de inicio de sesion llamada desde el main"""
    usuario = input("Ingrese su nombre de usuario: ").lower()
    contrasenia = input("Ingrese su contraseña de usuario: ")
    return validar_usuario_registrado(usuario, contrasenia, privilegio)

def chequeo_usuario_existente(nuevo_usuario):
    """Funcion a utilizar para chequear si el nombre del nuevo usuario no se encuentra ya en el sistema"""
    bandera = False
    for user in usuarios:
        for clave, valor in user.items():
            if clave == "usuario" and valor == nuevo_usuario:
                bandera = True
    return bandera
  
def registracion_usuarios(privilegio):
  """Funcion a utilizar para poder hacer la registracion de un nuevo usuario, mejoras a implementar a futuro,
   cuando falla el registro por usuario O contrasenia te diga mas especificamente el porque"""
  system("cls")
  usuario = ""
  contrasenia = ""
  usuario = input("Ingrese el usuario a utilizar en el sistema: ").lower()
  while usuario == "" or chequeo_usuario_existente(usuario):
     usuario = input("Ingrese un usuario a utilizar en el sistema que sea correcto o que no se este utilizando: \n").lower()
  contrasenia = input("Ingrese la contrasenia a utilizar en el sistema, debe tener minimo 6 digitos y un maximo de 12 digitos: \n")
  while contrasenia == "" or len(contrasenia) < 6 or len(contrasenia) > 12:
     contrasenia = input("Ingrese una contrasenia a utilizar en el sistema que sea correcta: \n")
  usuarios.append({"admin":privilegio, "usuario":usuario, "contrasenia":contrasenia})


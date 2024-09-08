#Como todavía no sabemos trabajar con archivos, en este repositorio vamos a generar los datos de prueba temporalmente.
#Para manipular los datos se van a llamar a funciones creadas en este repositorio, las cuales nos van a permitir no
#modificar la lógica de la funcion main/de la funcion que llame a los datos del repositorio.
#Una vez que cambiemos a archivos se reemplazan los datos de prueba con el acceso al archivo y todo seguiría funcionando igual

usuarios_consultantes= [["guido", "holabebe"], ["matias", "123456"]]
usuarios_admin = [["nacho", "playstation"], ["yiya", "654321"]]
codigos_admin = [415465, 11123, 999846] #Codigos que debe tener al momento de registrarse un nuevo admin para validar el registro

def get_usuarios_consultantes():
    return usuarios_consultantes

def get_usuarios_admin():
    return usuarios_admin

def get_codigos_admin():
    return codigos_admin

def validar_codigos_admin():
    MAXIMO_INTENTOS_CODIGOS_ADMIN = 5
    validacion = int(input("Ingrese el código de administrador: "))
    intentos = 1
    while validacion not in codigos_admin and intentos < MAXIMO_INTENTOS_CODIGOS_ADMIN:
        validacion = int(input("Código incorrecto, ingréselo nuevamente: "))
        intentos += 1
    if intentos == MAXIMO_INTENTOS_CODIGOS_ADMIN and validacion not in codigos_admin:
        return False
    return True

def validar_usuario_registrado_consultante(usuario, contrasenia):
    return [usuario, contrasenia] in usuarios_consultantes

def validar_usuario_registrado_administrador(usuario, contrasenia):
    return [usuario, contrasenia] in usuarios_admin

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
    
def inicio_sesion(tipo):
    """Funcion principal de inicio de sesion llamada desde el main"""
    usuario = input("Ingrese su nombre de usuario: ").lower()
    contrasenia = input("Ingrese su contraseña de usuario: ")
    if(tipo == "consultante"):
        return validar_ingreso_usuario(validar_usuario_registrado_consultante, usuario, contrasenia)
    else:
        return validar_ingreso_usuario(validar_usuario_registrado_administrador, usuario, contrasenia)


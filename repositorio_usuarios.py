from os import system, name
import uuid
from utils import writeFile, readFile, bloquear_teclado, validar_input
from repositorio_pagos import registrarTarjeta
archivoUser = "user.json"
usuarios = readFile(archivoUser)




codigos_admin = [415465, 11123, 999846] #Codigos que debe tener al momento de registrarse un nuevo admin para validar el registro
userLoguin = {}  #Diccionario que se actualiza con el usuario y contrasenia ingresado.

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
    usuarios = readFile(archivoUser)
    consultante= list(filter(lambda usuario: usuario["admin"] == privilegio, usuarios))
    bandera = 0
    for user in consultante:
        for clave, valor in user.items():
            if clave == "usuario" and valor == usuario or clave=="contrasenia" and valor == contrasenia:
                userLoguin.update(user) #Actualizo el diccionario userLoguin con el usuario y contrasenia ingresado.
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
  usuarios = readFile(archivoUser)
  usuario = input("Ingrese el usuario a utilizar en el sistema: ").lower()
  while usuario == "" or chequeo_usuario_existente(usuario):
     usuario = input("Ingrese un usuario a utilizar en el sistema que sea correcto o que no se este utilizando: \n").lower()
  contrasenia = input("Ingrese la contrasenia a utilizar en el sistema, debe tener minimo 6 digitos y un maximo de 12 digitos: \n")
  while contrasenia == "" or len(contrasenia) < 6 or len(contrasenia) > 12:
     contrasenia = input("Ingrese una contrasenia a utilizar en el sistema que sea correcta: \n")

  idGenerate = str(uuid.uuid4())
  nuevoUsuario = {"id" : idGenerate , "admin":privilegio, "usuario":usuario, "contrasenia":contrasenia, "vuelos": [], "reservas": [], "tarjetas":[]}
  writeFile(archivoUser, usuarios,nuevoUsuario )
  if not(privilegio):
    print("Si desea agregar una tarjeta de crédito, ingrese S, de lo contrario ingrese N")
    agregarTarjeta = input("Ingrese su respuesta: ").upper()
    if agregarTarjeta == "S":
        registrarTarjeta(nuevoUsuario)
  print("Usuario registrado exitosamente")
  bloquear_teclado(2)
  return

def getDataUser():
    return userLoguin


def consultarReserva(user):
    print("Ingrese que tipo de reserva desea consultar:")
    print("1. Sala VIP")
    print("2. Estacionamiento")
    opcion = validar_input(2)
    
    if opcion == "1":
        reservas_salavip = [reserva for reserva in user["reservas"] if "salavip" in reserva]
        if not reservas_salavip:
            print("No hay reservas de sala vip para consultar")
        else:
            print("\n--- Reservas de Sala VIP ---")
            for reserva in reservas_salavip:
                for clave, valor in reserva.items():
                    print(f"{clave}: {valor}")
                print("---")
    
    elif opcion == "2":
        reservas_estacionamiento = [reserva for reserva in user["reservas"] if "estacionamiento" in reserva]
        if not reservas_estacionamiento:
            print("No hay reservas de estacionamiento para consultar")
        else:
            print("\n--- Reservas de Estacionamiento ---")
            for reserva in reservas_estacionamiento:
                for clave, valor in reserva.items():
                    print(f"{clave}: {valor}")
                print("---")

def cancelar_reserva_por_tipo(user, tipo_reserva, usuarios):
    reservas = [reserva for reserva in user["reservas"] if tipo_reserva in reserva]
    if not reservas:
        print(f"No hay reservas de {tipo_reserva.title()} para cancelar")
        return
        
    cantidad_reservas = len(reservas)
    
    print(f"\n--- Reservas de {tipo_reserva.title()} ---")
    for i, reserva in enumerate(reservas, 1):
        print(f"# {i}")
        for clave, valor in reserva.items():
            print(f"{clave}: {valor}")
        print("---")
    
    print("Ingrese el número de reserva que desea cancelar: ")
    seleccion = int(validar_input(cantidad_reservas))
    
    for usuario in usuarios:
        if usuario["id"] == user["id"]:
            reserva_a_eliminar = reservas[seleccion - 1]
            usuario["reservas"].remove(reserva_a_eliminar)
            user["reservas"].remove(reserva_a_eliminar)
            writeFile(archivoUser, usuarios, None)
            print("Reserva cancelada exitosamente")
            break

        
def cancelarReserva(user):
    """
    Permite al usuario cancelar una reserva existente de Sala VIP o Estacionamiento.

    Args:
        user (dict): Diccionario con la información del usuario logueado

    Returns:
        None. Actualiza el archivo de usuarios si se cancela una reserva.
    """
    usuarios = readFile(archivoUser)
    
    print("Ingrese que tipo de reserva desea cancelar:")
    print("1. Sala VIP")
    print("2. Estacionamiento")
    opcion = validar_input(2)
    
    if opcion == "1":
        cancelar_reserva_por_tipo(user, "salavip", usuarios)
    elif opcion == "2":
        cancelar_reserva_por_tipo(user, "estacionamiento", usuarios)
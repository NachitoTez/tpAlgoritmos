from datetime import datetime
import re #regex
from utils import writeFile, readFile

archivoUser = "user.json"
usuarios = readFile(archivoUser)

def actualizaUsuario(user):
    Listausuarios = readFile(archivoUser)
    for usuario in Listausuarios:
        if user["id"] == usuario["id"]:  
            return usuario

def tieneTarjeta(user):
    flag = False
    counter = 0 
    user = actualizaUsuario(user)
    if len(user["tarjetas"]) == 0:
      tarjeta =  registrarTarjeta(user)
      return tarjeta
    else:
        while not flag:
            seleccion = input("""
              Desea usar alguna de sus tarjetas o agregar otra:
              1. Usar tarjeta guardada
              2. Agregar una tarjeta nueva
              """)
            if seleccion == "1":
                for tarjeta in user["tarjetas"]:
                    counter += 1
                    print(counter, tarjeta["nombretitular"], tarjeta["numerotareja"])
                seleccionTarjeta = int(input("Seleccione la tarjeta que quiere utilizar "))
                if seleccionTarjeta <= counter:
                    nuevaTarjeta = user["tarjetas"][seleccionTarjeta - 1]
                    return nuevaTarjeta
                else:
                    print("Seleccione una tarjeta correctamente")
            elif seleccion == "2":
               nuevaTarjeta = registrarTarjeta(user)
               if nuevaTarjeta:
                flag = True
                return nuevaTarjeta
            else:
                print("Seleccione una opcion correcta")

def registrarTarjeta(user):
    guardar = ""
    flag = False
    tarjeta = imputTarjeta()
    usuarios = readFile(archivoUser)
    while not flag:
        try:
            for usuario in usuarios:
                if usuario["id"] == user["id"]:
                    usuario["tarjetas"].append(tarjeta)
                    writeFile(archivoUser, usuarios, None)
                    print("Registro exitoso!")
                    flag = True 
                    return tarjeta
        except ValueError as e:
            print(e)

def imputTarjeta():
    numero_Tarjeta = numeroTarjeta()
    nombre_Titulr = nombreTarjeta()
    fechaVenci = añoTarjeta()
    codigo = codigoSeguridad()
    tarjeta = {
        "numerotareja": numero_Tarjeta,
        "nombretitular": nombre_Titulr,
        "fechavencimiento": fechaVenci,
        "codigo": codigo
    }
    return tarjeta

def numeroTarjeta():
    flag = False
    regexNumeroTarjeta = r'^\d{16}$'
    while not flag:
        try:
            print("Ingrese los 16 números de la tarjeta")
            numeroTarjeta = input("Número de la tarjeta: ") 
            if not numeroTarjeta.isdigit():
                 ValueError("Dato no válido. Solo debe ingresar números.")
            if not re.match(regexNumeroTarjeta, numeroTarjeta):
                print("Tarjeta no válida. Debe contener exactamente 16 números.")
            else:
                flag = True
                return numeroTarjeta
        except ValueError as e:
            print(e)

def nombreTarjeta():
    flag = False
    regexNombre = r'^[a-zA-Z\s]+$'
    while not flag:
        nombreTitular = input("Nombre del titular de la tarjeta: ")
        if not re.match(regexNombre, nombreTitular):
            print("Nombre no válido. Solo se permiten letras y espacios.")
        else:
            flag = True
            return nombreTitular
        

def añoTarjeta():
    flag = False
    regexFechaVencimiento = r'^(0[1-9]|1[0-2])\/\d{2}$'
    while not flag:
        fechaVencimiento = input("Fecha de vencimiento (MM/AA): ")
        if not re.match(regexFechaVencimiento, fechaVencimiento):
            print("Fecha no válida. Debe tener el formato MM/AA.")
        else:
            mes, año = fechaVencimiento.split('/')
            mes = int(mes)
            año = int("20" + año)
            fecha_actual = datetime.now()
            if (año < fecha_actual.year) or (año == fecha_actual.year and mes < fecha_actual.month):
                print("La tarjeta está vencida.")
            else:
                flag = True
                return fechaVencimiento

def codigoSeguridad():
    flag = False
    regexCodigoSeguridad = r'^\d{3}$' 
    while not flag:
        codigoSeguridad = input("Código de seguridad (CVV de 3 dígitos): ")
        if not re.match(regexCodigoSeguridad, codigoSeguridad):
            print("Código de seguridad no válido. Debe tener exactamente 3 dígitos.")
        else:
            flag = True
            return codigoSeguridad
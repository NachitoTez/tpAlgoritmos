from datetime import datetime
import random

def validar_input(cantidad_de_opciones, inicio=1):
    """Función creada para validar si la opción ingresada por teclado esta dentro del numero de opciones posibles
    Recibe por parámetro la cantidad de opciones disponibles y devuelve la opcion "String" ingresada por el usuario ya validada
    """
    opcion = input()
    opciones_validas = []
    for i in range(inicio,cantidad_de_opciones +1):
        opciones_validas.append(str(i))
    
    while opcion not in opciones_validas:
        opcion = input("Ingrese una opción válida: ")
    return opcion

def bisiesto(anio):
    return anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0)
def cantidad_dias(anio, mes):
    dias = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if(mes==2 and bisiesto(anio)):
        return dias[mes-1]+1
    else:
        return dias[mes-1]
    
def validarFecha(fecha):
    try:
        fechaValida =  datetime.strptime(fecha, "%d/%m/%Y")
        return True, fechaValida
    except ValueError:
        return False, None
    
def randonAprobado():
    valido = random.randint(0,10)
    if valido > 3:
        return True
    else:
        return False
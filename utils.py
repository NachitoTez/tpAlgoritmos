def validar_input(cantidad_de_opciones):
    """Función creada para validar si la opción ingresada por teclado esta dentro del numero de opciones posibles
    Recibe por parámetro la cantidad de opciones disponibles y devuelve la opcion ingresada por el usuario ya validada
    """
    opcion = input()
    opciones_validas = []
    for i in range(1,cantidad_de_opciones +1):
        opciones_validas.append(str(i))
    
    while opcion not in opciones_validas:
        opcion = input("Ingrese una opción válida: ")
    
    return opcion
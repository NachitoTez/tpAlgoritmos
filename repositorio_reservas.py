import random
from repositorio_pagos import tieneTarjeta
from repositorio_vuelos import filtrar_vuelos_asientos_disponibles, reservar_asiento
from utils import ingresar_fecha_y_hora, randonAprobado, readFile, writeFile
#por ahora, solo vamos a poder hacer reservas de vuelos disponibles. Para el 100 podríamos intentar elegir por fecha, destino y demás


def reservar_vuelo(user):
    """Permite al usuario reservar un vuelo de la lista de vuelos disponibles."""
    vuelos_disponibles = filtrar_vuelos_asientos_disponibles()
    
    if not vuelos_disponibles:
        print("No hay vuelos disponibles para reservar en este momento.")
        return

    print("VUELOS DISPONIBLES:")
#Continuar con la reserva
    for i, vuelo in enumerate(vuelos_disponibles, 1):
        print(f"{i}. Vuelo {vuelo['numero_vuelo']} - {vuelo['aerolinea']}")
        print(f"   Origen: {vuelo['origen']} - Destino: {vuelo['destino']}")
        print(f"   Asientos disponibles: {vuelo['asientos_disponibles']}")
        print("---")

    try:
        # Solicitar al usuario que elija un vuelo
        seleccion = int(input("Ingrese el número del vuelo que desea reservar: ")) - 1
        
        # Validar la selección
        if seleccion < 0 or seleccion >= len(vuelos_disponibles):
            print("Selección inválida.")
            return

        # Obtener el número de vuelo seleccionado
        vuelo_seleccionado = vuelos_disponibles[seleccion]
        numero_vuelo = vuelo_seleccionado['numero_vuelo']

        # Intentar realizar la reserva
        reserva_exitosa = reservar_asiento(numero_vuelo)

        if reserva_exitosa:
            # Aquí podrías agregar lógica adicional como:
            # - Guardar la reserva en un archivo/base de datos de reservas
            # - Asociar la reserva al usuario
            print(f"¡Reserva confirmada para el vuelo {numero_vuelo}!")
        else:
            print("No se pudo completar la reserva.")

    except ValueError:
        print("Por favor, ingrese un número válido.")
    except Exception as e:
        print(f"Ocurrió un error: {str(e)}")


def reservaSalaVIP(user, aeropuertos, listaUsuario):
    valida = False
    bandera = False
    banderaReserva = False
    seleccionSala = 0
    salaValida = False
    archivoUser = "user.json"

    while not bandera:
        for index, aeropuerto in enumerate(aeropuertos):
            print(index + 1, aeropuerto["codigo"], aeropuerto["ciudad"])

        seleccion = int(input("Seleccione el aeropuerto donde se encuentra o quiere reservar: "))
        if 1 <= seleccion <= len(aeropuertos):
            if "salavip" in aeropuertos[seleccion - 1]:
                for ind, salaVIP in enumerate(aeropuertos[seleccion - 1]["salavip"]):
                    if salaVIP["reservados"] < salaVIP["capacidad"]:
                        print(ind + 1, "Nombre: ", salaVIP["nombre"], "Precio: ", salaVIP["precio"])

                while not salaValida:
                    try:
                        seleccionSala = int(input("Seleccione la sala: "))
                        if 1 <= seleccionSala <= len(aeropuertos[seleccion - 1]["salavip"]):
                            salaValida = True
                        else:
                            print("Por favor, ingrese un número de sala válido.")
                    except ValueError:
                        print("Entrada no válida. Por favor, ingrese un número.")

                fecha = ingresar_fecha_y_hora("fecha y hora de reserva")

                reservar = {
                    "aeropuerto": aeropuertos[seleccion - 1]["ciudad"],
                    "codigo": aeropuertos[seleccion - 1]["codigo"],
                    "fecha": fecha,
                    "salavip": aeropuertos[seleccion - 1]["salavip"][seleccionSala - 1]["nombre"]
                }

                print("Debe seleccionar o registrar una tarjeta para realizar el pago")
                while not banderaReserva:
                    tarjeta = tieneTarjeta(user)
                    if tarjeta:
                        valida = randonAprobado()
                        if valida:
                            aeropuertos[seleccion - 1]["salavip"][seleccionSala - 1]["reservados"] += 1
                            for usuario in listaUsuario:
                                if usuario["id"] == user["id"]:
                                    usuario["reservas"].append(reservar)
                                    listaUsuarioActualizado = readFile(archivoUser)
                                    writeFile(archivoUser, listaUsuarioActualizado, None)
                                    bandera = True
                                    banderaReserva = valida
                        else:
                            print("Fondos insuficientes")
                    else:
                        print("Ocurrió un problema")
        else:
            print("Seleccione un aeropuerto correctamente.")

    print("Reserva realizada con éxito", user)

	
def reservaEstacionamiento(user, aeropuertos, listaUsuario):
    flag = False
    reserva = False
    fechas_rango = []
    archivoUser = "user.json"
    
    while not flag:    
        # Mostrar aeropuertos disponibles
        for idx, aeropuerto in enumerate(aeropuertos):
            print(f"{idx + 1}. {aeropuerto['codigo']} - {aeropuerto['ciudad']}")
        
        # Seleccionar aeropuerto
        seleccion = int(input("Seleccione el aeropuerto donde quiere reservar: "))
        if 1 <= seleccion <= len(aeropuertos):
            aeropuerto_seleccionado = aeropuertos[seleccion - 1]
            
            if "estacionamiento" in aeropuerto_seleccionado:
                estacionamiento = aeropuerto_seleccionado["estacionamiento"]
                
                fechaInicio = ingresar_fecha_y_hora("fecha y hora de inicio de estacionamiento")
                fechaFin = ingresar_fecha_y_hora("fecha y hora de fin de estacionamiento")
                while fechaFin <= fechaInicio:
                    print("La fecha de fin de estacionamiento debe ser posterior a la de inicio. Intente nuevamente.\n")
                    fechaFin = ingresar_fecha_y_hora("fecha y hora de fin de estacionamiento")
                # Lista de fechas en el rango		
                fechas_rango.append(fechaInicio)
                    

                # Verificar disponibilidad en todas las fechas del rango
                lugares_disponibles = []
                for letra, capacidad in estacionamiento["lugares"].items():
                    for i in range(1, capacidad + 1):
                        lugar = f"{letra}{i}"
                        # Verificar que el lugar esté disponible en todas las fechas del rango
                        lugar_disponible = all(
                            lugar not in estacionamiento["reservados"].get(fecha, [])
                            for fecha in fechas_rango
                        )
                        if lugar_disponible:
                            lugares_disponibles.append(lugar)

                if lugares_disponibles:
                    lugarSeleccionado = random.choice(lugares_disponibles)
                    reservar = {
                        "aeropuerto": aeropuerto_seleccionado["ciudad"],
                        "codigo": aeropuerto_seleccionado["codigo"],
                        "fechainicio": str(fechaInicio),
                        "fechafin": str(fechaFin),
                        "estacionamiento": lugarSeleccionado
                    }
                    
                    print("Debe seleccionar o registrar una tarjeta para realizar el pago")
                    while not reserva:
                        tarjeta = tieneTarjeta(user)
                        if tarjeta:
                            valida = randonAprobado()
                            if valida:
                                # Corregir la lógica de guardado de reservas
                                for fecha in fechas_rango:
                                    if fecha not in estacionamiento["reservados"]:
                                        estacionamiento["reservados"][fecha] = []
                                    estacionamiento["reservados"][fecha].append(lugarSeleccionado)
                                
                                for usuario in listaUsuario:
                                    if usuario["id"] == user["id"]:
                                        usuario["reservas"].append(reservar)
                                        writeFile(archivoUser, listaUsuario, None)
                                        flag = True
                                        reserva = True
                                print(f"Lugar {lugarSeleccionado} reservado para {user['usuario']} desde {fechaInicio} hasta {fechaFin}")
                            else:
                                print("Fondos insuficientes")
                                break
                else:
                    print(f"No hay lugares disponibles para el rango de fechas {fechaInicio} a {fechaFin}")
            else:
                print("Este aeropuerto no tiene estacionamiento disponible.")
        else:
            print("Selección inválida. Por favor, elija un aeropuerto válido.")


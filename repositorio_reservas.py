from repositorio_vuelos import filtrar_vuelos_asientos_disponibles, reservar_asiento
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

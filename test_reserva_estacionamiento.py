import pytest
from unittest.mock import patch
from repositorio_reservas import reservaEstacionamiento

    # Datos simulados
usuario = {
        "id": "f7bd9d80-771e-4e6f-100f-b8fafcff506e",
        "admin": True,
        "usuario": "nacho",
        "contrasenia": "playstation",
        "vuelos": [],
        "reservas": [],
        "tarjetas": []
    }
aeropuertos = [
        {
            "codigo": "EZE",
            "ciudad": "Buenos Aires",
            "pais": "Argentina",
            "posicion": [20, 24],
            "salavip": [
                {"nombre": "EZE GOLD", "capacidad": 50, "precio": "$100", "reservados": 0},
                {"nombre": "EZE Diamante", "capacidad": 10, "precio": "$100", "reservados": 0},
                {"nombre": "EZE Silver", "capacidad": 30, "precio": "$100", "reservados": 0},
            ],
            "estacionamiento": {
                "capacidadtotal": 50,
                "lugares": {"A": 10, "B": 10, "C": 15, "D": 15},
                "reservados": {}
            }
        }
    ]
listaUsuarios = [usuario]

def test_reservaEstacionamiento():
    # Simular input usando mock.patch
    with patch("builtins.input", side_effect=[
      "1",  # Selección de aeropuerto (EZE)
    "1",  # Selección de sala VIP (EZE GOLD)

    # Fecha inicio
    "2025",  # Año
    "2",  # Mes
    "3",  # Día
    "12",  # Hora
    "30",   # Minutos

    # Fecha fin
    "2025",  # Año
    "5",  # Mes
    "3",  # Día
    "12",  # Hora
    "30",   # Minutos

    "2",  # Agregar tarjeta
    "1234567890987654",  # Número tarjeta
    "Carlosa",  # Nombre tarjeta
    "09/29",  # Vencimiento tarjeta
    "258",  # C
    ]):
        resultado = reservaEstacionamiento(usuario, aeropuertos, listaUsuarios)

         # Verificar que la reserva se haya realizado correctamente
        assert resultado

        # Fecha esperada
        fecha_esperada = "2025-02-03 12:30:00"

        # Verificar que se haya registrado algo en la fecha esperada
        assert fecha_esperada in aeropuertos[0]["estacionamiento"]["reservados"]
        
        # Verificar que al menos un lugar haya sido reservado para esa fecha
        lugares_reservados = aeropuertos[0]["estacionamiento"]["reservados"][fecha_esperada]
        assert len(lugares_reservados) > 0
        assert usuario["reservas"][0]["estacionamiento"] == True
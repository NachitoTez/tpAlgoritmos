import pytest
from unittest.mock import patch
from repositorio_reservas import reservaSalaVIP

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

def test_reservaVIP():


    # Simular input usando mock.patch
    with patch("builtins.input", side_effect=[
        "1",  # Selección de aeropuerto (EZE)
        "1",  # Selección de sala VIP (EZE GOLD)
        "2025",  # Año
        "11",  # Mes
        "39",  # Día invalido
        "3",  # Día
        "12",  # Hora
        "30",   # Minutos
        "2", #agregar tarjeta
        "1234567890987654",   # numeroT
        "Carlosa",   # nombreT
        "09/29",   # vencimientoT
        "258",   # codigoT
    ]):
        resultado = reservaSalaVIP(usuario, aeropuertos, listaUsuarios)

        # Verificar que la reserva se haya hecho correctamente
        assert resultado
        assert aeropuertos[0]["salavip"][0]["reservados"] == 1
        assert usuario["reservas"][0]["salavip"] == "EZE GOLD"



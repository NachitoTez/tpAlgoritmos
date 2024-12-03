import pytest
from datetime import datetime, timedelta
from unittest.mock import patch

from repositorio_vuelos import (
    get_vuelo,
    filtrar_vuelos,
    reservar_asiento,
    vuelo_esta_en_curso,
    filtrar_vuelos_asientos_disponibles
)

MOCK_VUELOS = [
    {
        "numero_vuelo": "AA1234",
        "aerolinea": "Aerolineas",
        "origen": "EZE",
        "destino": "MIA",
        "estado": "En horario",
        "despegue": "2024-12-25 10:00:00",
        "arribo": "2024-12-25 15:00:00",
        "avion": 1,
        "asientos_disponibles": 50
    },
    {
        "numero_vuelo": "BB5678",
        "aerolinea": "Latam",
        "origen": "MIA",
        "destino": "EZE",
        "estado": "Cancelado",
        "despegue": "2024-12-26 12:00:00",
        "arribo": "2024-12-26 17:00:00",
        "avion": 2,
        "asientos_disponibles": 0
    }
]

def test_get_vuelo():
    vuelo = get_vuelo("AA1234", MOCK_VUELOS)
    assert vuelo is not None
    assert vuelo["numero_vuelo"] == "AA1234"
    
    assert get_vuelo("CC9999", MOCK_VUELOS) is None

def test_filtrar_vuelos():
    vuelos_aerolinea = filtrar_vuelos("aerolinea", "Aerolineas", MOCK_VUELOS)
    assert len(vuelos_aerolinea) == 1
    assert vuelos_aerolinea[0]["numero_vuelo"] == "AA1234"

    vuelos_estado = filtrar_vuelos("estado", "Cancelado", MOCK_VUELOS)
    assert len(vuelos_estado) == 1
    assert vuelos_estado[0]["numero_vuelo"] == "BB5678"

def test_vuelo_esta_en_curso():
    vuelo_en_curso = {
        "despegue": "2024-05-15 10:00:00",
        "arribo": "2024-05-15 15:00:00"
    }
    
    with patch('repositorio_vuelos.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2024, 5, 15, 12, 30)
        mock_datetime.strptime.side_effect = datetime.strptime
        
        assert vuelo_esta_en_curso(vuelo_en_curso, "2024-05-15 12:30:00") is True

def test_filtrar_vuelos_asientos_disponibles():
    vuelos_disponibles = filtrar_vuelos_asientos_disponibles(MOCK_VUELOS)
    
    assert len(vuelos_disponibles) == 1
    assert vuelos_disponibles[0]["numero_vuelo"] == "AA1234"

def test_reservar_asiento():
    with patch('repositorio_vuelos.readFile', return_value=MOCK_VUELOS), \
         patch('repositorio_vuelos.writeFile'):
        
        resultado = reservar_asiento("AA1234")
        assert resultado is True
        assert MOCK_VUELOS[0]["asientos_disponibles"] == 49

        resultado = reservar_asiento("BB5678")
        assert resultado is False

def test_reservar_asiento_vuelo_inexistente():
    with patch('repositorio_vuelos.readFile', return_value=MOCK_VUELOS):
        resultado = reservar_asiento("XX9999")
        assert resultado is False
import sys
import os

#python -B -m pytest

#pytest --cache-clear
# Agrega el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from repositorio_usuarios import validar_usuario_registrado

def test_validar_usuario():
    assert validar_usuario_registrado("matias", "123456", False) == True
    assert validar_usuario_registrado("matias", "123456", True) == False
    assert validar_usuario_registrado("usuario_inexistente", "123456", False) == False
    assert validar_usuario_registrado("matias", "contraseña_incorrecta", False) == False

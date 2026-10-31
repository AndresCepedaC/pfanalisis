"""
Configuración de pytest.

Agrega el directorio raíz del proyecto a sys.path
para que los imports ``from src...`` funcionen en los tests.
"""

import sys
from pathlib import Path

# Raíz del proyecto (directorio que contiene main.py y src/)
PROYECTO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROYECTO_ROOT))

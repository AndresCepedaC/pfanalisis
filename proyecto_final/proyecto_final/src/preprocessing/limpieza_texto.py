"""
Funciones para normalizar el texto de los abstracts.

Transforma el texto crudo en una cadena limpia y uniforme,
apta para el análisis de frecuencias.
"""

import re
import unicodedata
from typing import List


def normalizar_texto(texto: str) -> str:
    """Normaliza un texto para análisis de frecuencias.

    Operaciones aplicadas en orden:
        1. Une palabras partidas por saltos de línea.
        2. Normaliza caracteres Unicode (NFKD).
        3. Elimina tildes y marcas diacríticas.
        4. Convierte a minúsculas.
        5. Reemplaza la puntuación por espacios.
        6. Reduce espacios repetidos.

    Args:
        texto: Texto crudo a normalizar.

    Returns:
        Texto normalizado como cadena de tokens separados por espacios.
    """
    if not texto:
        return ""

    # 1. Unimos palabras partidas por un salto de línea.
    # Ejemplo: "educa-\nción" -> "educación".
    texto = re.sub(r"(?<=\w)-\s*\n\s*(?=\w)", "", texto)

    # 2. Normalizamos los caracteres Unicode.
    texto = unicodedata.normalize("NFKD", texto)

    # 3. Eliminamos las tildes y marcas diacríticas.
    texto = "".join(
        caracter
        for caracter in texto
        if not unicodedata.combining(caracter)
    )

    # 4. Convertimos todo a minúsculas.
    texto = texto.lower()

    # 5. Reemplazamos la puntuación por espacios.
    texto = re.sub(r"[^\w\s]", " ", texto)

    # 6. Reducimos espacios repetidos.
    texto = re.sub(r"\s+", " ", texto).strip()

    return texto


def tokenizar(texto_normalizado: str) -> List[str]:
    """Divide un texto normalizado en tokens individuales.

    Args:
        texto_normalizado: Texto ya procesado por ``normalizar_texto``.

    Returns:
        Lista de tokens (palabras).
    """
    if not texto_normalizado:
        return []
    return texto_normalizado.split()

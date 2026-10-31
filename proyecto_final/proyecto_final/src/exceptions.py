"""
Excepciones personalizadas del proyecto.

Proporcionan mensajes descriptivos para cada tipo de fallo,
facilitando el diagnóstico y el manejo de errores.
"""


class ExtractionError(Exception):
    """Error durante la extracción de texto o abstract de un PDF."""


class PreprocessingError(Exception):
    """Error durante la normalización de texto o el cálculo de frecuencias."""


class SortingError(Exception):
    """Error cuando un algoritmo de ordenamiento recibe datos inválidos."""

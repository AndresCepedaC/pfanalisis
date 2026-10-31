"""
Guarda las frecuencias de las palabras en un archivo CSV.
"""

import csv
import logging
from collections import Counter
from pathlib import Path

from src.config import FREQUENCIES_CSV

logger = logging.getLogger(__name__)


def guardar_frecuencias(
    frecuencias: Counter,
    ruta_salida: Path = FREQUENCIES_CSV,
) -> Path:
    """Escribe las frecuencias de palabras en un archivo CSV.

    Args:
        frecuencias: Contador con pares (palabra, frecuencia).
        ruta_salida: Ruta del archivo CSV de salida.

    Returns:
        Ruta absoluta del archivo generado.
    """
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)

    with open(ruta_salida, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["palabra", "frecuencia"])

        for palabra, cantidad in frecuencias.most_common():
            escritor.writerow([palabra, cantidad])

    logger.info(
        "Frecuencias guardadas: %d palabras → %s",
        len(frecuencias),
        ruta_salida,
    )

    return ruta_salida.resolve()


if __name__ == "__main__":
    # Ejecutar con: python -m src.preprocessing.guardar_frecuencias
    from src.config import configurar_logging
    from src.preprocessing.frecuencia_palabras import calcular_frecuencias

    configurar_logging()

    frecuencias, procesados, total = calcular_frecuencias()
    ruta = guardar_frecuencias(frecuencias)

    print(f"Artículos procesados: {procesados}/{total}")
    print(f"Palabras diferentes: {len(frecuencias)}")
    print(f"Archivo guardado en: {ruta}")

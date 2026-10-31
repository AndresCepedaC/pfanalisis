"""
Obtiene las N palabras más frecuentes usando
los resultados de Counting Sort, Radix Sort y Bucket Sort.
"""

import csv
import logging
from pathlib import Path
from typing import Dict, List, Tuple

from src.config import FREQUENCIES_CSV, TOP_15_CSV, TOP_N
from src.sorting.counting_sort import counting_sort
from src.sorting.radix_sort import radix_sort
from src.sorting.bucket_sort import bucket_sort

logger = logging.getLogger(__name__)


def cargar_datos(
    ruta: Path = FREQUENCIES_CSV,
) -> Tuple[List[str], List[int]]:
    """Lee las palabras y sus frecuencias desde el CSV.

    Args:
        ruta: Ruta del archivo CSV.

    Returns:
        Tupla ``(palabras, frecuencias)`` con listas paralelas.
    """
    palabras: List[str] = []
    frecuencias: List[int] = []

    with open(ruta, "r", encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            palabras.append(fila["palabra"])
            frecuencias.append(int(fila["frecuencia"]))

    return palabras, frecuencias


def obtener_top_n(
    palabras: List[str],
    frecuencias: List[int],
    ordenadas: List[int],
    n: int = TOP_N,
) -> List[Tuple[str, int]]:
    """Recupera las palabras asociadas a las N frecuencias mayores.

    Args:
        palabras: Lista de palabras (orden original del CSV).
        frecuencias: Lista de frecuencias (orden original).
        ordenadas: Frecuencias ordenadas por el algoritmo.
        n: Cantidad de palabras a incluir.

    Returns:
        Lista de tuplas ``(palabra, frecuencia)`` ordenada de mayor a menor.
    """
    palabras_por_frecuencia: Dict[int, List[str]] = {}

    for palabra, frecuencia in zip(palabras, frecuencias):
        if frecuencia not in palabras_por_frecuencia:
            palabras_por_frecuencia[frecuencia] = []
        palabras_por_frecuencia[frecuencia].append(palabra)

    top: List[Tuple[str, int]] = []
    frecuencias_visitadas: set = set()

    # Recorremos las frecuencias de mayor a menor.
    for frecuencia in reversed(ordenadas):
        if frecuencia in frecuencias_visitadas:
            continue

        frecuencias_visitadas.add(frecuencia)

        for palabra in palabras_por_frecuencia[frecuencia]:
            top.append((palabra, frecuencia))
            if len(top) == n:
                return top

    return top


def guardar_top_n(
    resultados: Dict[str, List[Tuple[str, int]]],
    ruta_salida: Path = TOP_15_CSV,
) -> Path:
    """Guarda los resultados del top N en un archivo CSV.

    Args:
        resultados: Diccionario ``{algoritmo: [(palabra, freq), ...]}``.
        ruta_salida: Ruta del archivo CSV de salida.

    Returns:
        Ruta absoluta del archivo generado.
    """
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)

    with open(ruta_salida, "w", encoding="utf-8", newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["algoritmo", "posicion", "palabra", "frecuencia"])

        for nombre, top in resultados.items():
            for posicion, (palabra, frecuencia) in enumerate(top, start=1):
                escritor.writerow([nombre, posicion, palabra, frecuencia])

    logger.info("Top N guardado en: %s", ruta_salida)
    return ruta_salida.resolve()


def obtener_y_guardar_top_n(
    ruta_entrada: Path = FREQUENCIES_CSV,
    ruta_salida: Path = TOP_15_CSV,
    n: int = TOP_N,
) -> Dict[str, List[Tuple[str, int]]]:
    """Ejecuta los tres algoritmos y guarda las top N palabras.

    Args:
        ruta_entrada: CSV con frecuencias de palabras.
        ruta_salida: CSV de salida con el ranking.
        n: Cantidad de palabras a incluir.

    Returns:
        Diccionario ``{algoritmo: [(palabra, freq), ...]}``.
    """
    palabras, frecuencias = cargar_datos(ruta_entrada)

    algoritmos = {
        "Counting Sort": counting_sort,
        "Radix Sort": radix_sort,
        "Bucket Sort": bucket_sort,
    }

    resultados: Dict[str, List[Tuple[str, int]]] = {}

    for nombre, algoritmo in algoritmos.items():
        ordenadas = algoritmo(frecuencias)
        resultados[nombre] = obtener_top_n(
            palabras, frecuencias, ordenadas, n
        )

    # Verificamos consistencia.
    valores = list(resultados.values())
    coinciden = all(v == valores[0] for v in valores[1:])

    if not coinciden:
        logger.warning("Los algoritmos produjeron resultados diferentes.")
    else:
        logger.info("Los tres algoritmos coinciden en el top %d.", n)

    guardar_top_n(resultados, ruta_salida)

    return resultados


if __name__ == "__main__":
    # Ejecutar con: python -m src.sorting.top_15_algoritmos
    from src.config import configurar_logging

    configurar_logging()

    resultados = obtener_y_guardar_top_n()

    for nombre, top in resultados.items():
        print(f"\n{nombre}")
        print(f"{'Pos':<5}{'Palabra':<20}{'Frecuencia':>12}")

        for pos, (palabra, freq) in enumerate(top, start=1):
            print(f"{pos:<5}{palabra:<20}{freq:>12}")

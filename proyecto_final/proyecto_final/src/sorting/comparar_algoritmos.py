"""
Compara Counting Sort, Radix Sort y Bucket Sort
usando las mismas frecuencias y varias mediciones.
"""

import csv
import logging
import time
from pathlib import Path
from statistics import median
from typing import Any, Callable, Dict, List, Tuple

from src.config import (
    BENCHMARK_EXECUTIONS,
    BENCHMARK_REPETITIONS,
    FREQUENCIES_CSV,
)
from src.sorting.counting_sort import counting_sort
from src.sorting.radix_sort import radix_sort
from src.sorting.bucket_sort import bucket_sort

logger = logging.getLogger(__name__)


def cargar_frecuencias(ruta_csv: Path = FREQUENCIES_CSV) -> List[int]:
    """Carga las frecuencias numéricas del CSV.

    Args:
        ruta_csv: Ruta del archivo CSV con columnas ``palabra,frecuencia``.

    Returns:
        Lista de enteros con las frecuencias.
    """
    with open(ruta_csv, "r", encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo)
        return [int(fila["frecuencia"]) for fila in lector]


def medir_tiempo(
    algoritmo: Callable,
    datos: List[int],
    repeticiones: int = BENCHMARK_REPETITIONS,
    ejecuciones: int = BENCHMARK_EXECUTIONS,
) -> float:
    """Calcula la mediana del tiempo por ejecución en milisegundos.

    Realiza una ejecución de calentamiento y luego mide
    ``repeticiones`` bloques de ``ejecuciones`` cada uno.

    Args:
        algoritmo: Función de ordenamiento a evaluar.
        datos: Lista de enteros a ordenar.
        repeticiones: Cantidad de bloques de medición.
        ejecuciones: Ejecuciones por bloque.

    Returns:
        Mediana del tiempo por ejecución individual (ms).
    """
    # Ejecución de calentamiento.
    algoritmo(datos)

    mediciones: List[float] = []

    for _ in range(repeticiones):
        inicio = time.perf_counter()

        for _ in range(ejecuciones):
            algoritmo(datos)

        fin = time.perf_counter()

        tiempo_por_ejecucion = (fin - inicio) * 1000 / ejecuciones
        mediciones.append(tiempo_por_ejecucion)

    return median(mediciones)


def comparar_algoritmos(
    ruta_csv: Path = FREQUENCIES_CSV,
) -> Dict[str, Dict[str, Any]]:
    """Ejecuta y compara los tres algoritmos de ordenamiento.

    Args:
        ruta_csv: Ruta del CSV con las frecuencias.

    Returns:
        Diccionario ``{nombre: {resultado, correcto, tiempo_ms}}``.
    """
    frecuencias = cargar_frecuencias(ruta_csv)

    algoritmos: Dict[str, Callable] = {
        "Counting Sort": counting_sort,
        "Radix Sort": radix_sort,
        "Bucket Sort": bucket_sort,
    }

    resultados: Dict[str, Dict[str, Any]] = {}

    logger.info(
        "Comparando %d algoritmos con %d frecuencias",
        len(algoritmos),
        len(frecuencias),
    )

    for nombre, algoritmo in algoritmos.items():
        ordenados = algoritmo(frecuencias)

        correcto = (
            len(ordenados) == len(frecuencias)
            and all(
                ordenados[i] <= ordenados[i + 1]
                for i in range(len(ordenados) - 1)
            )
        )

        tiempo = medir_tiempo(algoritmo, frecuencias)

        resultados[nombre] = {
            "resultado": ordenados,
            "correcto": correcto,
            "tiempo_ms": tiempo,
        }

        logger.info(
            "%s — correcto: %s — mediana: %.6f ms",
            nombre,
            correcto,
            tiempo,
        )

    return resultados


if __name__ == "__main__":
    # Ejecutar con: python -m src.sorting.comparar_algoritmos
    from src.config import configurar_logging

    configurar_logging()

    resultados = comparar_algoritmos()

    print("=" * 50)
    print("COMPARACIÓN DE ALGORITMOS")
    print("=" * 50)

    for nombre, datos in resultados.items():
        print(f"\n{nombre}")
        print(f"  Ordenamiento correcto: {datos['correcto']}")
        print(f"  Mediana por ejecución: {datos['tiempo_ms']:.6f} ms")

    todos_iguales = (
        resultados["Counting Sort"]["resultado"]
        == resultados["Radix Sort"]["resultado"]
        == resultados["Bucket Sort"]["resultado"]
    )

    print(f"\nLos tres resultados coinciden: {todos_iguales}")

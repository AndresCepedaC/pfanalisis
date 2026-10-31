"""
Genera una gráfica de barras con las N palabras más frecuentes
obtenidas mediante los tres algoritmos de ordenamiento.
"""

import csv
import logging
from pathlib import Path
from typing import Dict, List, Tuple

from src.config import TOP_15_CSV, TOP_15_CHART

logger = logging.getLogger(__name__)


def cargar_top_n(
    ruta_csv: Path = TOP_15_CSV,
) -> Dict[str, List[Tuple[str, int]]]:
    """Lee los resultados de los tres algoritmos desde el CSV.

    Args:
        ruta_csv: Ruta del archivo CSV generado por ``top_15_algoritmos``.

    Returns:
        Diccionario ``{algoritmo: [(palabra, frecuencia), ...]}``.
    """
    resultados: Dict[str, List[Tuple[str, int]]] = {}

    with open(ruta_csv, "r", encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            algoritmo = fila["algoritmo"]

            if algoritmo not in resultados:
                resultados[algoritmo] = []

            resultados[algoritmo].append(
                (fila["palabra"], int(fila["frecuencia"]))
            )

    return resultados


def graficar_top_15(
    ruta_csv: Path = TOP_15_CSV,
    ruta_grafica: Path = TOP_15_CHART,
    mostrar: bool = False,
) -> Path:
    """Genera y guarda la gráfica de barras del top 15.

    Args:
        ruta_csv: Ruta del CSV con los datos del ranking.
        ruta_grafica: Ruta de salida para la imagen PNG.
        mostrar: Si es ``True``, muestra la gráfica interactivamente.

    Returns:
        Ruta absoluta de la imagen generada.

    Raises:
        ValueError: Si los resultados de los algoritmos no coinciden.
    """
    import matplotlib.pyplot as plt

    resultados = cargar_top_n(ruta_csv)

    # Usamos Counting Sort como referencia.
    datos = resultados["Counting Sort"]
    palabras = [palabra for palabra, _ in datos]
    frecuencias = [frecuencia for _, frecuencia in datos]

    # Verificamos que los tres algoritmos coincidan.
    coinciden = all(
        resultados[nombre] == datos for nombre in resultados
    )

    if not coinciden:
        raise ValueError(
            "Los resultados de los algoritmos no coinciden."
        )

    plt.figure(figsize=(12, 6))
    barras = plt.bar(palabras, frecuencias, color="#4C72B0", edgecolor="white")

    # Añadimos los valores sobre las barras.
    for barra, freq in zip(barras, frecuencias):
        plt.text(
            barra.get_x() + barra.get_width() / 2,
            barra.get_height() + 0.5,
            str(freq),
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
        )

    plt.title(
        "15 palabras más frecuentes en los abstracts",
        fontsize=14,
        fontweight="bold",
    )
    plt.xlabel("Palabras", fontsize=12)
    plt.ylabel("Frecuencia", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    ruta_grafica.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(ruta_grafica, dpi=300, bbox_inches="tight")

    if mostrar:
        plt.show()

    plt.close()

    logger.info("Gráfica guardada en: %s", ruta_grafica)
    return ruta_grafica.resolve()


if __name__ == "__main__":
    # Ejecutar con: python -m src.visualization.graficar_top_15
    from src.config import configurar_logging

    configurar_logging()
    graficar_top_15(mostrar=True)

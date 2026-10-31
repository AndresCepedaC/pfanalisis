"""
Configuración centralizada del proyecto.

Define las rutas de directorios, archivos de salida
y constantes utilizadas en todos los módulos.
"""

import logging
from pathlib import Path


# ── Rutas del proyecto ──────────────────────────────────────────────

BASE_DIR = Path(__file__).resolve().parent.parent
"""Directorio raíz del proyecto (padre de ``src/``)."""

DATA_DIR = BASE_DIR / "data"
"""Directorio que contiene los datos de entrada y salida."""

ARTICLES_DIR = DATA_DIR / "articulos"
"""Directorio con los 20 artículos científicos en PDF."""

FREQUENCIES_CSV = DATA_DIR / "frecuencias_palabras.csv"
"""Ruta del CSV con todas las frecuencias de palabras."""

TOP_15_CSV = DATA_DIR / "top_15_algoritmos.csv"
"""Ruta del CSV con las 15 palabras más frecuentes por algoritmo."""

TOP_15_CHART = DATA_DIR / "top_15_palabras.png"
"""Ruta de la gráfica de barras con el top 15."""


# ── Constantes de análisis ──────────────────────────────────────────

TOP_N = 15
"""Cantidad de palabras a incluir en el ranking final."""

BENCHMARK_REPETITIONS = 7
"""Repeticiones externas al medir el rendimiento de cada algoritmo."""

BENCHMARK_EXECUTIONS = 100
"""Ejecuciones internas por cada repetición de benchmark."""


# ── Logging ─────────────────────────────────────────────────────────

def configurar_logging(nivel: int = logging.INFO) -> None:
    """Configura el sistema de logging con formato legible.

    Args:
        nivel: Nivel mínimo de severidad (por defecto ``INFO``).
    """
    logging.basicConfig(
        level=nivel,
        format="%(asctime)s │ %(name)s │ %(levelname)s │ %(message)s",
        datefmt="%H:%M:%S",
    )

"""
Pipeline principal del análisis bibliométrico.

Ejecuta secuencialmente:
    1. Extracción de abstracts desde los archivos PDF.
    2. Normalización del texto y filtrado de stop words.
    3. Cálculo y almacenamiento de frecuencias de palabras.
    4. Ordenamiento con Counting Sort, Radix Sort y Bucket Sort.
    5. Comparación de rendimiento entre los tres algoritmos.
    6. Obtención de las 15 palabras más frecuentes.
    7. Generación de la gráfica de barras.

Uso::

    python main.py                 # Pipeline completo
    python main.py --top 20        # Cambiar el número de palabras
    python main.py --sin-grafica   # Omitir la generación de gráfica
    python main.py --verbose       # Activar logging detallado
"""

import argparse
import io
import logging
import sys

# Asegurar codificación utf-8 en consola para compatibilidad con Windows cp1252
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from src.config import (
    ARTICLES_DIR,
    FREQUENCIES_CSV,
    TOP_15_CSV,
    TOP_15_CHART,
    TOP_N,
    configurar_logging,
)
from src.preprocessing.frecuencia_palabras import calcular_frecuencias
from src.preprocessing.guardar_frecuencias import guardar_frecuencias
from src.sorting.comparar_algoritmos import comparar_algoritmos
from src.sorting.top_15_algoritmos import obtener_y_guardar_top_n
from src.visualization.graficar_top_15 import graficar_top_15

logger = logging.getLogger(__name__)


def crear_parser() -> argparse.ArgumentParser:
    """Crea el parser de argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description="Análisis bibliométrico de artículos científicos.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Ejemplos:\n"
            "  python main.py\n"
            "  python main.py --top 20 --verbose\n"
            "  python main.py --sin-grafica\n"
        ),
    )

    parser.add_argument(
        "--top",
        type=int,
        default=TOP_N,
        metavar="N",
        help=f"Número de palabras en el ranking (por defecto: {TOP_N}).",
    )

    parser.add_argument(
        "--sin-grafica",
        action="store_true",
        help="Omitir la generación de la gráfica.",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Activar logging detallado (nivel DEBUG).",
    )

    return parser


def main() -> None:
    """Punto de entrada del pipeline completo."""
    parser = crear_parser()
    args = parser.parse_args()

    # ── Configurar logging ──────────────────────────────────────────
    nivel = logging.DEBUG if args.verbose else logging.INFO
    configurar_logging(nivel)

    print("=" * 60)
    print("      ANÁLISIS DE ALGORITMOS - PROYECTO FINAL")
    print("=" * 60)

    # ── Fase 1: Extracción y frecuencias ────────────────────────────
    print("\n[*] Fase 1: Extracción de abstracts y cálculo de frecuencias")

    frecuencias, procesados, total = calcular_frecuencias(ARTICLES_DIR)

    if procesados == 0:
        logger.error("No se procesó ningún artículo. Abortando.")
        sys.exit(1)

    print(f"    Artículos procesados: {procesados}/{total}")
    print(f"    Palabras únicas encontradas: {len(frecuencias)}")

    # ── Fase 2: Guardar frecuencias ─────────────────────────────────
    print("\n[*] Fase 2: Guardando frecuencias en CSV")

    ruta_csv = guardar_frecuencias(frecuencias, FREQUENCIES_CSV)
    print(f"    Archivo: {ruta_csv}")

    # ── Fase 3: Comparación de algoritmos ───────────────────────────
    print("\n[*] Fase 3: Comparación de algoritmos de ordenamiento")

    resultados = comparar_algoritmos(FREQUENCIES_CSV)

    for nombre, datos in resultados.items():
        estado = "[OK]" if datos["correcto"] else "[ERROR]"
        print(
            f"    {estado} {nombre:<16} - "
            f"mediana: {datos['tiempo_ms']:.6f} ms"
        )

    todos_iguales = (
        resultados["Counting Sort"]["resultado"]
        == resultados["Radix Sort"]["resultado"]
        == resultados["Bucket Sort"]["resultado"]
    )
    print(f"    Resultados consistentes entre los 3 algoritmos: {todos_iguales}")

    # ── Fase 4: Top N palabras ──────────────────────────────────────
    print(f"\n[*] Fase 4: Obteniendo las {args.top} palabras más frecuentes")

    top_resultados = obtener_y_guardar_top_n(
        ruta_entrada=FREQUENCIES_CSV,
        ruta_salida=TOP_15_CSV,
        n=args.top,
    )

    # Mostramos el ranking usando Counting Sort como referencia.
    top_counting = top_resultados["Counting Sort"]

    print(f"\n    {'Pos':<5}{'Palabra':<20}{'Frecuencia':>12}")
    print(f"    {'-' * 5}{'-' * 20}{'-' * 12}")

    for pos, (palabra, freq) in enumerate(top_counting, start=1):
        print(f"    {pos:<5}{palabra:<20}{freq:>12}")

    # ── Fase 5: Gráfica ────────────────────────────────────────────
    if not args.sin_grafica:
        print("\n[*] Fase 5: Generando gráfica de barras")

        ruta_img = graficar_top_15(
            ruta_csv=TOP_15_CSV,
            ruta_grafica=TOP_15_CHART,
            mostrar=False,
        )
        print(f"    Gráfica guardada en: {ruta_img}")
    else:
        print("\n[*] Fase 5: Gráfica omitida (--sin-grafica)")

    # ── Resumen final ───────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("      PIPELINE COMPLETADO EXITOSAMENTE")
    print("=" * 60)


if __name__ == "__main__":
    main()

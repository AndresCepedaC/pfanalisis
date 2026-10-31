"""
Calcula la frecuencia de las palabras de los abstracts
de los artículos científicos del corpus.
"""

import logging
from collections import Counter
from pathlib import Path
from typing import Tuple

from src.config import ARTICLES_DIR
from src.extraction.pdf_reader import extraer_texto_pdf, extraer_abstract
from src.preprocessing.limpieza_texto import normalizar_texto, tokenizar
from src.preprocessing.stop_words import filtrar_stop_words

logger = logging.getLogger(__name__)


def calcular_frecuencias(
    carpeta: Path = ARTICLES_DIR,
) -> Tuple[Counter, int, int]:
    """Extrae los abstracts de todos los PDF y cuenta las palabras.

    Args:
        carpeta: Directorio que contiene los archivos PDF.

    Returns:
        Tupla con:
        - ``Counter`` de frecuencias de palabras.
        - Cantidad de artículos procesados exitosamente.
        - Cantidad total de archivos PDF encontrados.
    """
    frecuencias: Counter = Counter()
    articulos_procesados = 0

    archivos_pdf = sorted(carpeta.glob("*.pdf"))

    if not archivos_pdf:
        logger.warning("No se encontraron archivos PDF en: %s", carpeta)
        return frecuencias, 0, 0

    for archivo in archivos_pdf:
        try:
            texto_pdf = extraer_texto_pdf(str(archivo))
        except Exception:
            logger.error("Error al leer: %s", archivo.name)
            continue

        abstract = extraer_abstract(texto_pdf)

        if abstract is None:
            logger.warning("Sin abstract: %s", archivo.name)
            continue

        texto_limpio = normalizar_texto(abstract)
        palabras = tokenizar(texto_limpio)
        palabras = filtrar_stop_words(palabras)

        frecuencias.update(palabras)
        articulos_procesados += 1

    logger.info(
        "Frecuencias calculadas: %d artículos de %d",
        articulos_procesados,
        len(archivos_pdf),
    )

    return frecuencias, articulos_procesados, len(archivos_pdf)


if __name__ == "__main__":
    # Ejecutar con: python -m src.preprocessing.frecuencia_palabras
    from src.config import configurar_logging

    configurar_logging()

    frecuencias, procesados, total = calcular_frecuencias()

    print(f"PDF encontrados: {total}")
    print(f"Artículos procesados: {procesados}")
    print(f"Palabras diferentes: {len(frecuencias)}")

    print("\n15 palabras más frecuentes:")
    for palabra, cantidad in frecuencias.most_common(15):
        print(f"  {palabra}: {cantidad}")

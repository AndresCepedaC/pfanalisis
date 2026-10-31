"""
Módulo encargado de leer archivos PDF y extraer sus abstracts.

Utiliza PyMuPDF para obtener el texto de los artículos científicos
del corpus del proyecto.
"""

import logging
import re
from typing import Optional

import pymupdf

from src.exceptions import ExtractionError

logger = logging.getLogger(__name__)


def extraer_texto_pdf(ruta_pdf: str) -> str:
    """Extrae el texto completo de un archivo PDF.

    Args:
        ruta_pdf: Ruta del archivo PDF.

    Returns:
        Texto completo del documento.

    Raises:
        ExtractionError: Si el archivo no existe o no puede leerse.
    """
    try:
        with pymupdf.open(ruta_pdf) as documento:
            partes_texto = [pagina.get_text() for pagina in documento]
            texto_completo = "\n".join(partes_texto)

        logger.debug("PDF leído: %s (%d caracteres)", ruta_pdf, len(texto_completo))
        return texto_completo

    except Exception as error:
        raise ExtractionError(
            f"No se pudo leer el PDF '{ruta_pdf}': {error}"
        ) from error


def extraer_abstract(texto: str) -> Optional[str]:
    """Busca el abstract en el texto de un artículo científico.

    Aplica reglas generales y casos especiales para artículos
    cuya estructura no sigue el patrón estándar.

    Args:
        texto: Texto completo extraído de un PDF.

    Returns:
        Texto del abstract, o ``None`` si no se encontró.
    """
    if not texto or not texto.strip():
        return None

    # ── Casos especiales por artículo ───────────────────────────────

    # Artículo 7: las palabras clave aparecen antes del resumen.
    marcador_7 = "The rapid expansion of Learning Analytics"
    if marcador_7 in texto:
        inicio = texto.find(marcador_7)
        patron_final_7 = re.compile(
            r"(?im)^[ \t]*1\.\s*Introduction[ \t]*$"
        )
        final = patron_final_7.search(texto, inicio)
        if final:
            return texto[inicio:final.start()].strip()

    # Artículo 9: el resumen termina antes del primer párrafo
    # de la introducción, que no tiene encabezado visible.
    marcador_9 = "From unique educational perspectives"
    final_9 = "Since Alan Turing first articulated"
    if marcador_9 in texto and final_9 in texto:
        inicio = texto.find(marcador_9)
        fin = texto.find(final_9, inicio)
        if fin > inicio:
            return texto[inicio:fin].strip()

    # Artículo 17: el encabezado Keywords incluye los términos
    # en la misma línea.
    marcador_17 = (
        "Artificial intelligence (AI), as an emerging technology"
    )
    if marcador_17 in texto:
        inicio = texto.find(marcador_17)
        patron_final_17 = re.compile(r"(?im)^[ \t]*Keywords\b")
        final = patron_final_17.search(texto, inicio)
        if final:
            return texto[inicio:final.start()].strip()

    # ── Patrón general ──────────────────────────────────────────────

    # Reconocemos los encabezados con y sin espacios.
    patron_inicio = re.compile(
        r"(?im)^[ \t]*(?:"
        r"A\s*B\s*S\s*T\s*R\s*A\s*C\s*T"
        r"|Abstract"
        r")[ \t]*:?[ \t]*$"
    )

    inicio_encontrado = patron_inicio.search(texto)

    # Algunos PDF ponen Abstract y el resumen en la misma línea.
    if inicio_encontrado is None:
        patron_inicio = re.compile(
            r"(?i)\b(?:A\s*B\s*T\s*R\s*A\s*C\s*T|Abstract)"
        )
        inicio_encontrado = patron_inicio.search(texto)

    if inicio_encontrado is None:
        logger.warning("No se encontró el encabezado del abstract.")
        return None

    inicio = inicio_encontrado.end()

    # Buscamos los posibles límites posteriores al encabezado.
    patron_final = re.compile(
        r"(?im)^[ \t]*(?:"
        r"K\s*E\s*Y\s*W\s*O\s*R\s*D\s*S"
        r"|Keywords?"
        r"|Key words"
        r")[^\r\n]*"
        r"|^[ \t]*\d+(?:\.\d+)*\.?[ \t]*"
        r"INTRODUCTION[^\r\n]*$"
    )

    final_encontrado = patron_final.search(texto, inicio)

    if final_encontrado is None:
        logger.warning("No se encontró el final del abstract.")
        return None

    abstract = texto[inicio:final_encontrado.start()].strip()
    # Eliminamos signos sobrantes al comienzo del resumen.
    abstract = abstract.lstrip(" :\t\n\r")

    if not abstract:
        return None

    return abstract

"""
Tests unitarios para el módulo de extracción de PDFs.

Utiliza textos simulados para verificar la lógica de
extracción de abstracts sin depender de archivos PDF reales.
"""

import pytest

from src.extraction.pdf_reader import extraer_abstract


class TestExtraerAbstract:
    """Tests para la función extraer_abstract."""

    def test_texto_vacio(self):
        assert extraer_abstract("") is None

    def test_texto_none(self):
        assert extraer_abstract(None) is None

    def test_texto_solo_espacios(self):
        assert extraer_abstract("   \n\t  ") is None

    def test_abstract_estandar_con_keywords(self):
        """Patrón más común: Abstract ... Keywords."""
        texto = (
            "Some header text\n"
            "Abstract\n"
            "This study investigates the impact of AI on education.\n"
            "Results show significant improvements.\n"
            "Keywords\n"
            "artificial intelligence, education"
        )
        resultado = extraer_abstract(texto)

        assert resultado is not None
        assert "investigates" in resultado
        assert "improvements" in resultado
        assert "Keywords" not in resultado

    def test_abstract_con_espaciado(self):
        """Patrón A B S T R A C T."""
        texto = (
            "Journal title\n"
            "A B S T R A C T\n"
            "This paper reviews AI literacy programs.\n"
            "K E Y W O R D S\n"
            "AI literacy"
        )
        resultado = extraer_abstract(texto)

        assert resultado is not None
        assert "reviews" in resultado

    def test_abstract_seguido_de_introduction(self):
        """Abstract terminado por una sección INTRODUCTION."""
        texto = (
            "Title\n"
            "Abstract\n"
            "We present a framework for teaching AI.\n"
            "1. INTRODUCTION\n"
            "The rapid growth of AI..."
        )
        resultado = extraer_abstract(texto)

        assert resultado is not None
        assert "framework" in resultado
        assert "INTRODUCTION" not in resultado

    def test_sin_abstract(self):
        """Texto que no contiene encabezado de abstract."""
        texto = (
            "Introduction\n"
            "This is a paper about AI.\n"
            "Methods\n"
            "We used surveys."
        )
        resultado = extraer_abstract(texto)
        assert resultado is None

    def test_abstract_inline(self):
        """Abstract y texto en la misma línea."""
        texto = (
            "Header\n"
            "Abstract This paper analyzes AI in education.\n"
            "Keywords: AI, education\n"
        )
        resultado = extraer_abstract(texto)

        assert resultado is not None
        assert "analyzes" in resultado

    def test_caso_especial_articulo_7(self):
        """Artículo 7: marcador especial al inicio."""
        texto = (
            "Some header\n"
            "The rapid expansion of Learning Analytics "
            "has led to increased interest in AI.\n"
            "This study examines the intersection.\n"
            "1. Introduction\n"
            "AI has become prevalent..."
        )
        resultado = extraer_abstract(texto)

        assert resultado is not None
        assert "Learning Analytics" in resultado
        assert "Introduction" not in resultado

    def test_caso_especial_articulo_9(self):
        """Artículo 9: marcadores de inicio y fin específicos."""
        texto = (
            "Title\n"
            "From unique educational perspectives "
            "this research reviews AI technologies.\n"
            "The findings suggest improvements.\n"
            "Since Alan Turing first articulated "
            "the possibility of thinking machines..."
        )
        resultado = extraer_abstract(texto)

        assert resultado is not None
        assert "educational perspectives" in resultado
        assert "Alan Turing" not in resultado

    def test_caso_especial_articulo_17(self):
        """Artículo 17: keywords en la misma línea."""
        texto = (
            "Header\n"
            "Artificial intelligence (AI), as an emerging technology "
            "has shown potential in STEM education.\n"
            "This review explores current applications.\n"
            "Keywords AI, STEM, assessment\n"
        )
        resultado = extraer_abstract(texto)

        assert resultado is not None
        assert "emerging technology" in resultado
        assert "Keywords" not in resultado

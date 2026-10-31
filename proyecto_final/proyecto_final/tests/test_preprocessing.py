"""
Tests unitarios para el módulo de preprocesamiento:
normalización de texto, tokenización y filtrado de stop words.
"""

import pytest

from src.preprocessing.limpieza_texto import normalizar_texto, tokenizar
from src.preprocessing.stop_words import STOP_WORDS, filtrar_stop_words


class TestNormalizarTexto:
    """Tests para la función normalizar_texto."""

    def test_texto_vacio(self):
        assert normalizar_texto("") == ""

    def test_none_como_entrada(self):
        assert normalizar_texto(None) == ""

    def test_minusculas(self):
        resultado = normalizar_texto("HELLO World")
        assert resultado == "hello world"

    def test_elimina_tildes(self):
        resultado = normalizar_texto("educación lingüística")
        assert resultado == "educacion linguistica"

    def test_une_palabras_partidas(self):
        resultado = normalizar_texto("educa-\nción")
        assert resultado == "educacion"

    def test_reemplaza_puntuacion(self):
        resultado = normalizar_texto("AI supports learning!")
        assert resultado == "ai supports learning"

    def test_reduce_espacios(self):
        resultado = normalizar_texto("  multiple   spaces  ")
        assert resultado == "multiple spaces"

    def test_texto_academico_completo(self):
        texto = (
            "Artificial Intelligence (AI) is transform-\n"
            "ing education. AI supports learning!"
        )
        resultado = normalizar_texto(texto)

        assert "artificial" in resultado
        assert "intelligence" in resultado
        assert "transforming" in resultado
        assert "!" not in resultado
        assert "(" not in resultado

    def test_caracteres_unicode(self):
        resultado = normalizar_texto("naïve café résumé")
        assert resultado == "naive cafe resume"

    def test_numeros_se_conservan(self):
        resultado = normalizar_texto("In 2022, there were 100 studies.")
        assert "2022" in resultado
        assert "100" in resultado


class TestTokenizar:
    """Tests para la función tokenizar."""

    def test_texto_vacio(self):
        assert tokenizar("") == []

    def test_una_palabra(self):
        assert tokenizar("hello") == ["hello"]

    def test_varias_palabras(self):
        resultado = tokenizar("hello world test")
        assert resultado == ["hello", "world", "test"]


class TestStopWords:
    """Tests para el filtrado de stop words."""

    def test_set_no_vacio(self):
        assert len(STOP_WORDS) > 0

    def test_contiene_articulos(self):
        assert "the" in STOP_WORDS
        assert "a" in STOP_WORDS
        assert "an" in STOP_WORDS

    def test_contiene_preposiciones(self):
        assert "of" in STOP_WORDS
        assert "in" in STOP_WORDS
        assert "for" in STOP_WORDS

    def test_contiene_conjunciones(self):
        assert "and" in STOP_WORDS
        assert "or" in STOP_WORDS
        assert "but" in STOP_WORDS

    def test_no_contiene_palabras_clave(self):
        """Palabras significativas del dominio no deben ser stop words."""
        assert "education" not in STOP_WORDS
        assert "learning" not in STOP_WORDS
        assert "artificial" not in STOP_WORDS
        assert "intelligence" not in STOP_WORDS
        assert "research" not in STOP_WORDS

    def test_es_frozenset(self):
        """Debe ser inmutable."""
        assert isinstance(STOP_WORDS, frozenset)

    def test_filtrar_lista(self):
        palabras = ["the", "artificial", "intelligence", "is", "transforming"]
        resultado = filtrar_stop_words(palabras)
        assert resultado == ["artificial", "intelligence", "transforming"]

    def test_filtrar_numeros(self):
        palabras = ["education", "2022", "learning", "100"]
        resultado = filtrar_stop_words(palabras)
        assert resultado == ["education", "learning"]

    def test_filtrar_lista_vacia(self):
        assert filtrar_stop_words([]) == []

    def test_todas_son_stop_words(self):
        palabras = ["the", "a", "and", "of"]
        assert filtrar_stop_words(palabras) == []

"""
Tests unitarios para los algoritmos de ordenamiento:
Counting Sort, Radix Sort y Bucket Sort.
"""

import pytest

from src.sorting.counting_sort import counting_sort
from src.sorting.radix_sort import radix_sort
from src.sorting.bucket_sort import bucket_sort
from src.exceptions import SortingError


# ── Parametrización: cada test se ejecuta para los 3 algoritmos ────

ALGORITMOS = [
    pytest.param(counting_sort, id="counting_sort"),
    pytest.param(radix_sort, id="radix_sort"),
    pytest.param(bucket_sort, id="bucket_sort"),
]


class TestCasosBasicos:
    """Casos básicos que los tres algoritmos deben manejar."""

    @pytest.mark.parametrize("algoritmo", ALGORITMOS)
    def test_lista_vacia(self, algoritmo):
        assert algoritmo([]) == []

    @pytest.mark.parametrize("algoritmo", ALGORITMOS)
    def test_un_solo_elemento(self, algoritmo):
        assert algoritmo([42]) == [42]

    @pytest.mark.parametrize("algoritmo", ALGORITMOS)
    def test_dos_elementos_ordenados(self, algoritmo):
        assert algoritmo([1, 2]) == [1, 2]

    @pytest.mark.parametrize("algoritmo", ALGORITMOS)
    def test_dos_elementos_desordenados(self, algoritmo):
        assert algoritmo([5, 3]) == [3, 5]

    @pytest.mark.parametrize("algoritmo", ALGORITMOS)
    def test_lista_ya_ordenada(self, algoritmo):
        datos = [1, 2, 3, 4, 5]
        assert algoritmo(datos) == [1, 2, 3, 4, 5]

    @pytest.mark.parametrize("algoritmo", ALGORITMOS)
    def test_orden_inverso(self, algoritmo):
        datos = [5, 4, 3, 2, 1]
        assert algoritmo(datos) == [1, 2, 3, 4, 5]


class TestDuplicados:
    """Manejo de valores duplicados."""

    @pytest.mark.parametrize("algoritmo", ALGORITMOS)
    def test_todos_iguales(self, algoritmo):
        datos = [7, 7, 7, 7]
        assert algoritmo(datos) == [7, 7, 7, 7]

    @pytest.mark.parametrize("algoritmo", ALGORITMOS)
    def test_con_duplicados(self, algoritmo):
        datos = [4, 2, 4, 1, 2, 3]
        assert algoritmo(datos) == [1, 2, 2, 3, 4, 4]

    @pytest.mark.parametrize("algoritmo", ALGORITMOS)
    def test_muchos_duplicados(self, algoritmo):
        datos = [3, 1, 3, 1, 3, 1]
        assert algoritmo(datos) == [1, 1, 1, 3, 3, 3]


class TestCasosEspeciales:
    """Valores extremos y entradas especiales."""

    @pytest.mark.parametrize("algoritmo", ALGORITMOS)
    def test_incluye_cero(self, algoritmo):
        datos = [3, 0, 1]
        assert algoritmo(datos) == [0, 1, 3]

    @pytest.mark.parametrize("algoritmo", ALGORITMOS)
    def test_valores_grandes(self, algoritmo):
        datos = [170, 45, 75, 90, 802, 24, 2, 66]
        assert algoritmo(datos) == [2, 24, 45, 66, 75, 90, 170, 802]

    @pytest.mark.parametrize("algoritmo", ALGORITMOS)
    def test_datos_reales(self, algoritmo):
        """Simula frecuencias de palabras del proyecto."""
        datos = [29, 3, 15, 8, 3, 42, 17, 1]
        assert algoritmo(datos) == [1, 3, 3, 8, 15, 17, 29, 42]


class TestValidacion:
    """Validación de entradas inválidas."""

    @pytest.mark.parametrize("algoritmo", ALGORITMOS)
    def test_negativos_lanza_error(self, algoritmo):
        with pytest.raises(SortingError):
            algoritmo([-1, 2, 3])

    @pytest.mark.parametrize("algoritmo", ALGORITMOS)
    def test_negativo_mezclado(self, algoritmo):
        with pytest.raises(SortingError):
            algoritmo([5, -3, 10])


class TestInmutabilidad:
    """Verificación de que los datos originales no se modifican."""

    @pytest.mark.parametrize("algoritmo", ALGORITMOS)
    def test_no_modifica_original(self, algoritmo):
        datos = [5, 3, 8, 1, 4]
        copia = datos.copy()
        algoritmo(datos)
        assert datos == copia


class TestConsistencia:
    """Los tres algoritmos deben producir el mismo resultado."""

    def test_resultados_iguales_basico(self):
        datos = [29, 3, 15, 8, 3, 42, 17, 1]
        resultado_cs = counting_sort(datos)
        resultado_rs = radix_sort(datos)
        resultado_bs = bucket_sort(datos)

        assert resultado_cs == resultado_rs == resultado_bs

    def test_resultados_iguales_grandes(self):
        datos = [170, 45, 75, 90, 802, 24, 2, 66, 100, 55, 1, 999]
        resultado_cs = counting_sort(datos)
        resultado_rs = radix_sort(datos)
        resultado_bs = bucket_sort(datos)

        assert resultado_cs == resultado_rs == resultado_bs

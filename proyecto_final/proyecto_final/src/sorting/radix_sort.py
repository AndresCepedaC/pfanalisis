"""
Implementación de Radix Sort para enteros no negativos.

Ordena los números por sus dígitos, comenzando
por las unidades, luego las decenas y así sucesivamente.

Complejidad temporal: O(d · (n + b)) donde d = dígitos, b = base.
Complejidad espacial: O(n + b).
"""

from typing import List

from src.exceptions import SortingError


def _ordenar_por_digito(datos: List[int], exponente: int) -> List[int]:
    """Ordena establemente según un dígito decimal.

    Args:
        datos: Lista de enteros no negativos.
        exponente: Potencia de 10 que identifica el dígito a evaluar.

    Returns:
        Nueva lista ordenada por el dígito seleccionado.
    """
    cantidad = len(datos)
    resultado = [0] * cantidad
    conteo = [0] * 10

    # Contamos las apariciones de cada dígito.
    for numero in datos:
        digito = (numero // exponente) % 10
        conteo[digito] += 1

    # Calculamos las posiciones acumuladas.
    for i in range(1, 10):
        conteo[i] += conteo[i - 1]

    # Colocamos los números de derecha a izquierda
    # para conservar la estabilidad del ordenamiento.
    for i in range(cantidad - 1, -1, -1):
        numero = datos[i]
        digito = (numero // exponente) % 10
        resultado[conteo[digito] - 1] = numero
        conteo[digito] -= 1

    return resultado


def radix_sort(datos: List[int]) -> List[int]:
    """Devuelve una nueva lista ordenada con Radix Sort.

    Args:
        datos: Lista de enteros no negativos.

    Returns:
        Nueva lista con los mismos elementos en orden ascendente.

    Raises:
        SortingError: Si la lista contiene enteros negativos.
    """
    if not datos:
        return []

    if any(numero < 0 for numero in datos):
        raise SortingError(
            "Radix Sort requiere enteros no negativos."
        )

    resultado = datos.copy()
    maximo = max(resultado)
    exponente = 1

    while maximo // exponente > 0:
        resultado = _ordenar_por_digito(resultado, exponente)
        exponente *= 10

    return resultado

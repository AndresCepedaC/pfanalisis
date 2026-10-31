"""
Implementación de Counting Sort.

Ordena una lista de enteros no negativos
sin realizar comparaciones entre elementos.

Complejidad temporal: O(n + k) donde k es el valor máximo.
Complejidad espacial: O(n + k).
"""

from typing import List

from src.exceptions import SortingError


def counting_sort(datos: List[int]) -> List[int]:
    """Devuelve una nueva lista ordenada con Counting Sort.

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
            "Counting Sort requiere enteros no negativos."
        )

    maximo = max(datos)

    # Contamos cuántas veces aparece cada valor.
    conteo = [0] * (maximo + 1)

    for numero in datos:
        conteo[numero] += 1

    # Reconstruimos la lista ordenada.
    resultado = []

    for numero, cantidad in enumerate(conteo):
        resultado.extend([numero] * cantidad)

    return resultado

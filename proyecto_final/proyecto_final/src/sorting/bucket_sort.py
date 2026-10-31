"""
Implementación de Bucket Sort para enteros no negativos.

Distribuye los elementos en cubetas proporcionales a su valor
y ordena cada cubeta con inserción directa.

Complejidad temporal: O(n + k) en caso promedio.
Complejidad espacial: O(n + k).
"""

from typing import List

from src.exceptions import SortingError


def bucket_sort(datos: List[int]) -> List[int]:
    """Devuelve una nueva lista ordenada con Bucket Sort.

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
            "Bucket Sort requiere enteros no negativos."
        )

    minimo = min(datos)
    maximo = max(datos)

    cantidad_buckets = len(datos)
    buckets: List[List[int]] = [[] for _ in range(cantidad_buckets)]

    # Distribuimos los números en los buckets.
    rango = maximo - minimo + 1

    for numero in datos:
        indice = (numero - minimo) * cantidad_buckets // rango
        indice = min(indice, cantidad_buckets - 1)
        buckets[indice].append(numero)

    # Ordenamos cada bucket mediante inserción directa.
    resultado: List[int] = []

    for bucket in buckets:
        for i in range(1, len(bucket)):
            actual = bucket[i]
            j = i - 1

            while j >= 0 and bucket[j] > actual:
                bucket[j + 1] = bucket[j]
                j -= 1

            bucket[j + 1] = actual

        resultado.extend(bucket)

    return resultado

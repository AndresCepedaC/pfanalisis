"""
Lista de stop words para el análisis bibliométrico.

Contiene palabras funcionales del inglés que carecen de valor
analítico en el contexto de frecuencias de términos académicos.
"""

from typing import List

STOP_WORDS: frozenset = frozenset({
    # ── Artículos ───────────────────────────────────────────────────
    "a", "an", "the",

    # ── Preposiciones ───────────────────────────────────────────────
    "about", "above", "across", "after", "against", "along", "among",
    "around", "at", "before", "behind", "below", "beneath", "beside",
    "between", "beyond", "by", "down", "during", "for", "from", "in",
    "inside", "into", "near", "of", "off", "on", "onto", "out",
    "outside", "over", "past", "through", "throughout", "to", "toward",
    "towards", "under", "underneath", "until", "up", "upon", "with",
    "within", "without",

    # ── Conjunciones ────────────────────────────────────────────────
    "and", "but", "or", "nor", "so", "yet", "both", "either",
    "neither", "not", "only",

    # ── Pronombres ──────────────────────────────────────────────────
    "i", "me", "my", "myself", "we", "us", "our", "ours", "ourselves",
    "you", "your", "yours", "yourself", "yourselves",
    "he", "him", "his", "himself", "she", "her", "hers", "herself",
    "it", "its", "itself", "they", "them", "their", "theirs",
    "themselves",
    "what", "which", "who", "whom", "whose",
    "this", "that", "these", "those",

    # ── Verbos auxiliares y comunes ─────────────────────────────────
    "am", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "having",
    "do", "does", "did", "doing", "done",
    "will", "would", "shall", "should", "may", "might",
    "can", "could", "must",

    # ── Adverbios y palabras funcionales ────────────────────────────
    "as", "if", "than", "because", "while", "although", "though",
    "where", "when", "how", "why",
    "then", "there", "here", "now",
    "also", "too", "very", "just", "even", "still",
    "already", "always", "never", "often", "sometimes",
    "however", "therefore", "thus", "hence", "moreover",
    "furthermore", "nevertheless", "nonetheless",
    "rather", "quite", "somewhat", "somehow",

    # ── Determinantes y adjetivos comunes ───────────────────────────
    "all", "each", "every", "any", "some", "no", "many", "much",
    "few", "several", "most", "more", "less", "other", "another",
    "such", "own", "same", "different",

    # ── Artefactos de texto académico ───────────────────────────────
    "et", "al", "eg", "ie", "etc", "e", "g", "p", "pp", "vol",
    "doi", "http", "https", "www", "org", "com",

    # ── Palabras muy frecuentes sin valor analítico ─────────────────
    "one", "two", "three", "four", "five", "first", "second", "third",
    "new", "well", "way", "part", "made", "make",
    "like", "use", "used", "using", "based",
})
"""Conjunto inmutable de stop words en inglés académico."""


def filtrar_stop_words(palabras: List[str]) -> List[str]:
    """Elimina las stop words y tokens numéricos de una lista.

    Args:
        palabras: Lista de tokens normalizados.

    Returns:
        Lista filtrada sin stop words ni tokens puramente numéricos.
    """
    return [
        palabra for palabra in palabras
        if palabra not in STOP_WORDS and not palabra.isdigit()
    ]

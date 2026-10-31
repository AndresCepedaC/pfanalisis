# Análisis de Algoritmos en el Contexto de la Bibliometría

Proyecto de análisis computacional y bibliométrico aplicado al estudio de **20 artículos científicos** sobre **Inteligencia Artificial Generativa en la Educación**, diseñado bajo estándares de Clean Code, principios SOLID y arquitectura modular.

---

## 📋 Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Stack Tecnológico](#stack-tecnológico)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Instalación y Configuración](#instalación-y-configuración)
6. [Guía de Uso](#guía-de-uso)
7. [Algoritmos de Ordenamiento Implementados](#algoritmos-de-ordenamiento-implementados)
8. [Filtrado de Stop Words y Normalización](#filtrado-de-stop-words-y-normalización)
9. [Batería de Pruebas (Testing)](#batería-de-pruebas-testing)
10. [Herramientas de Desarrollo](#herramientas-de-desarrollo)

---

## 🎯 Descripción General

El sistema automatiza el pipeline bibliométrico completo:
1. **Extracción:** Lectura de artículos científicos en formato PDF mediante `PyMuPDF` y extracción de sus abstracts utilizando expresiones regulares robustas y casos especiales documentados.
2. **Preprocesamiento:** Normalización de texto (unión de guiones de corte de línea, normalización Unicode NFKD, eliminación de acentos/diacríticos, conversión a minúsculas, eliminación de puntuación) y filtrado de **stop words** académicas en inglés.
3. **Frecuencias:** Conteo determinista de frecuencias de palabras y exportación a formato CSV.
4. **Ordenamiento:** Implementación y comparación experimental de tres algoritmos de tiempo lineal/subcuadrático:
   - **Counting Sort**
   - **Radix Sort** (LSD)
   - **Bucket Sort** (con inserción directa por cubeta)
5. **Ranking y Validación:** Recuperación del Top 15 (o Top N configurable) de términos más frecuentes y verificación cruzada de coincidencia estricta entre los tres algoritmos.
6. **Visualización:** Generación automatizada de gráficos de barras en alta resolución (PNG, 300 DPI) con etiquetas cuantitativas.

---

## 🏗️ Arquitectura del Sistema

El proyecto sigue una arquitectura desacoplada por capas:

```
[ PDF Corpora ] (data/articulos/*.pdf)
       │
       ▼
┌─────────────────────────┐
│     src.extraction      │  ──> Lectura con PyMuPDF y extracción de abstracts
└──────────┬──────────────┘
           ▼
┌─────────────────────────┐
│   src.preprocessing     │  ──> Normalización, tokenización, stop words y frecuencias
└──────────┬──────────────┘
           ▼
     [ CSV Frecuencias ] (data/frecuencias_palabras.csv)
           │
           ▼
┌─────────────────────────┐
│       src.sorting       │  ──> Counting Sort, Radix Sort, Bucket Sort & Benchmark
└──────────┬──────────────┘
           ▼
     [ CSV Top N ] (data/top_15_algoritmos.csv)
           │
           ▼
┌─────────────────────────┐
│    src.visualization    │  ──> Gráfica de distribución de términos
└──────────┬──────────────┘
           ▼
     [ Gráfica PNG ] (data/top_15_palabras.png)
```

---

## 💻 Stack Tecnológico

- **Lenguaje:** Python 3.10+
- **Procesamiento de Documentos:** `PyMuPDF` (`pymupdf >= 1.24.0`)
- **Visualización Científica:** `matplotlib` (`matplotlib >= 3.8.0`)
- **Suite de Pruebas:** `pytest` (`pytest >= 8.0.0`)
- **Biblioteca Estándar:** `collections.Counter`, `unicodedata`, `re`, `csv`, `time`, `statistics`, `argparse`, `logging`, `pathlib`.

---

## 📁 Estructura del Proyecto

```
proyecto_final/
├── data/
│   ├── articulos/               # 20 artículos científicos en PDF
│   ├── frecuencias_palabras.csv # Frecuencias calculadas de todas las palabras
│   ├── top_15_algoritmos.csv    # Ranking de las 15 palabras más frecuentes
│   └── top_15_palabras.png      # Gráfica generada en alta resolución
├── scripts/
│   └── dev/                     # Scripts auxiliares y herramientas de desarrollo
├── src/
│   ├── __init__.py
│   ├── config.py                # Rutas y configuración centralizada
│   ├── exceptions.py            # Jerarquía de excepciones personalizadas
│   ├── extraction/
│   │   ├── __init__.py
│   │   └── pdf_reader.py        # Extractor PyMuPDF con regex avanzada
│   ├── preprocessing/
│   │   ├── __init__.py
│   │   ├── stop_words.py        # Lista inmutable de stop words y filtrado
│   │   ├── limpieza_texto.py    # Pipeline de normalización de texto
│   │   ├── frecuencia_palabras.py # Conteo y agregación de frecuencias
│   │   └── guardar_frecuencias.py # Serialización a CSV
│   ├── sorting/
│   │   ├── __init__.py
│   │   ├── counting_sort.py     # Implementación O(n + k)
│   │   ├── radix_sort.py        # Implementación O(d * (n + b))
│   │   ├── bucket_sort.py       # Implementación O(n + k)
│   │   ├── comparar_algoritmos.py # Benchmark con repeticiones y mediana
│   │   └── top_15_algoritmos.py # Extracción de top términos y validación
│   └── visualization/
│       ├── __init__.py
│       └── graficar_top_15.py   # Generación de visualizaciones matplotlib
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Configuración del entorno de tests
│   ├── test_extraction.py       # Tests unitarios del módulo de extracción
│   ├── test_preprocessing.py    # Tests de normalización y stop words
│   └── test_sorting.py          # Tests parametrizados de los 3 algoritmos
├── main.py                      # Punto de entrada CLI del pipeline
├── requirements.txt             # Dependencias del proyecto
└── README.md                    # Documentación técnica completa
```

---

## 🚀 Instalación y Configuración

### 1. Clonar o acceder al directorio del proyecto

```bash
cd proyecto_final
```

### 2. Crear y activar un entorno virtual

En Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

En Linux / macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 📖 Guía de Uso

### Ejecución del pipeline completo

El script `main.py` orquesta todas las fases de forma secuencial:

```bash
python main.py
```

### Opciones de línea de comandos (CLI)

| Parámetro | Tipo | Descripción | Por defecto |
|---|---|---|---|
| `--top N` | `int` | Cantidad de palabras a incluir en el ranking | `15` |
| `--sin-grafica` | `flag` | Omite la generación del archivo PNG | Desactivado |
| `--verbose` | `flag` | Activa la salida de logs en nivel `DEBUG` | Desactivado |

**Ejemplos:**

```bash
# Obtener las 20 palabras más frecuentes con logs detallados
python main.py --top 20 --verbose

# Ejecutar el pipeline sin generar la gráfica
python main.py --sin-grafica
```

### Ejecución modular

Cada módulo puede ser invocado de forma independiente gracias al soporte de módulos de Python (`-m`):

```bash
# Calcular y mostrar frecuencias
python -m src.preprocessing.frecuencia_palabras

# Comparar algoritmos de ordenamiento
python -m src.sorting.comparar_algoritmos

# Generar el top 15
python -m src.sorting.top_15_algoritmos

# Regenerar la gráfica
python -m src.visualization.graficar_top_15
```

---

## ⚡ Algoritmos de Ordenamiento Implementados

| Algoritmo | Complejidad Temporal (Mejor / Promedio / Peor) | Complejidad Espacial | Estabilidad |
|---|---|---|---|
| **Counting Sort** | $O(n + k)$ | $O(n + k)$ | Estable |
| **Radix Sort (LSD)** | $O(d \cdot (n + b))$ | $O(n + b)$ | Estable |
| **Bucket Sort** | $O(n + k)$ / $O(n + k)$ / $O(n^2)$ | $O(n + k)$ | Estable |

*Donde $n$ es la cantidad de frecuencias distintas, $k$ el valor de la frecuencia máxima, $d$ la cantidad de dígitos y $b$ la base numérica (10).*

### Metodología de Benchmark

La función `medir_tiempo()` en `src/sorting/comparar_algoritmos.py`:
- Realiza una corrida inicial de calentamiento (*warm-up*).
- Ejecuta 7 repeticiones independientes de 100 ejecuciones cada una.
- Calcula la **mediana** de los tiempos individuales por ejecución para descartar anomalías de planificación del sistema operativo.
- Valida que los tres algoritmos produzcan resultados idénticos y en orden no decreciente.

---

## 🧹 Filtrado de Stop Words y Normalización

Para garantizar resultados bibliométricos útiles y con valor analítico real, el módulo `src/preprocessing/stop_words.py` implementa un conjunto inmutable (`frozenset`) con más de 120 palabras funcionales en inglés académico (artículos, preposiciones, conjunciones, pronombres, verbos auxiliares y marcadores bibliográficos como *et, al, doi, http*).

**Impacto:**
- **Sin filtrado:** El ranking era dominado por palabras vacías como *"and"*, *"the"*, *"of"*, *"in"*, *"to"*.
- **Con filtrado:** El ranking resalta los conceptos centrales de la investigación: *"ai"*, *"education"*, *"learning"*, *"aied"*, *"research"*, *"educational"*, *"students"*, *"assessment"*, *"literacy"*.

---

## 🧪 Batería de Pruebas (Testing)

El proyecto incluye pruebas automatizadas exhaustivas con `pytest`:

```bash
pytest tests/ -v
```

### Cobertura de pruebas:
- **`tests/test_sorting.py`:** Pruebas parametrizadas para Counting Sort, Radix Sort y Bucket Sort:
  - Listas vacías, elementos únicos, dos elementos ordenados/inversos.
  - Listas de gran tamaño, elementos con valor 0.
  - Manejo de duplicados masivos y elementos repetidos.
  - Validación de excepciones ante entradas negativas (`SortingError`).
  - Verificación de inmutabilidad (el arreglo original no es alterado).
  - Consistencia estricta (los tres algoritmos arrojan exactamente la misma salida).
- **`tests/test_preprocessing.py`:** Pruebas de normalización, desacentuación, unión de palabras con guión, reducción de espacios y filtrado de stop words y tokens numéricos.
- **`tests/test_extraction.py`:** Pruebas de extracción de abstracts con sintaxis estándar, con espacios espaciados (`A B S T R A C T`), delimitadas por `Introduction`, y los casos especiales de los artículos 7, 9 y 17.

---

## 🛠️ Herramientas de Desarrollo

Los scripts auxiliares creados durante la fase de exploración y ajuste fino se conservan en `scripts/dev/` para propósitos de auditoría e inspección futura:
- `scripts/dev/inspeccionar_pdf.py`: Diagnóstico de encabezados y delimitadores en PDFs complejos.
- `scripts/dev/prueba_corpus.py`: Validador de cobertura de extracción en todo el directorio de artículos.
- `scripts/dev/evaluar_*.py` y `scripts/dev/probar_*.py`: Verificaciones independientes previas al marco de `pytest`.

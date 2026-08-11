# -*- coding: utf-8 -*-
"""
build_nb1.py -- Genera DOS notebooks para la Mision 1: Recuperacion de Datos

  nb1_semana1_recuperacion_datos.ipynb -- Clase 1 (Semana 1)
  nb1_semana2_recuperacion_datos.ipynb -- Clase 2 (Semana 2)

Divididos en dos archivos porque son dos sesiones de clase reales, una semana aparte
(decision del usuario, 2026-08-05) -- no dos secciones de un mismo notebook largo.

Fuente de contenido:
  - Teoria_Semanas1-2_Mision1_RecuperacionDeDatos.md (bloques de teoria)
  - Preguntas_Teoricas_Semanas1-2.md (banco de preguntas check_t1..check_t12 --
    fuente de verdad del enunciado/opciones; el notebook YA NO las reproduce en
    Markdown porque el autograder las renderiza como HTML interactivo)
  - WORKFORCE_HANDOFF.md Done log 2026-08-05 (estructura, datasets, revision SOFIA,
    decision de division en 2 archivos)

Datasets: vgsales_es.csv (Semana 1, Secciones A-B), athlete_events_es.csv (Semana 2,
Secciones C-D + Integracion). Semana 2 usa UNICAMENTE df_atletas -- ya no recarga
df_games/vgsales (decision del usuario, 2026-08-11: Semana 2 es una tarea nueva y
autocontenida, no una continuacion de la mision de videojuegos).
Tema visual: placeholder neutro -- pendiente PIXEL (ticket #2, WORKFORCE_HANDOFF.md).

Convenciones:
  - check_tN: una sola celda de codigo (`grader.check_tN()`). El autograder renderiza
    la pregunta + opciones como HTML y captura la respuesta.
  - check_exN etiquetados 🔨 CONSTRUYE: el notebook NO trae la solucion escrita, solo
    instrucciones + un bloque "Tu codigo aqui" en blanco.
  - check_exN etiquetados 🧩 COMPLETA: mantienen el patron de blancos `___`.
  - La numeracion de check_exN/check_debugN/check_tN es GLOBAL a la Mision 1 dentro de
    Semana 1 (no cambia). **Semana 2 tiene su PROPIA numeracion independiente,
    reiniciada en 0** (check_ex0, check_debug0, check_t0...) -- decision del usuario,
    2026-08-11: Semana 2 se trata como una tarea nueva y separada, no una continuacion
    numerica de Semana 1. Esto es seguro de hacer ahora porque ningun autograder de
    Semana 2 existe todavia (ticket #10) -- ver nota para ATLAS abajo.

Nota para ATLAS (ticket #10, WORKFORCE_HANDOFF.md): esto implica DOS autograders
separados -- autograder_nb1_semana1.py (check_ex1-5, debug1, t1-9, mini_a, mini_b,
resumen) y autograder_nb1_semana2.py (check_ex0-6, debug0-3, t0-4, mini_c, mini_d,
intex0-4, reto1, resumen) -- no un autograder compartido entre archivos, y con
numeracion que NO continua la de Semana 1. Cada uno necesita su propio `notebook` id
en el payload de Supabase (sugerido: "nb1_semana1" / "nb1_semana2") para que el
lookup de "tu mejor puntaje previo" en el formulario de registro no mezcle las dos
sesiones.

Semana 2 `check_tN` -- de donde sale el contenido: t0-t2 reutilizan (verbatim) las
preguntas t10-t12 de Preguntas_Teoricas_Semanas1-2.md bajo su nuevo numero local
(ver el argumento `banco=` en cada llamada a `teoria_check` mas abajo, y el
"Bloque 5" agregado a ese archivo con la referencia completa). t3 y t4 son preguntas
NUEVAS, escritas para esta reestructuracion (no estaban en el banco original) --
su enunciado completo tambien vive en el "Bloque 5" de Preguntas_Teoricas_Semanas1-2.md
para que ATLAS no tenga que extraerlo del codigo generado.
"""
import json

def md(cell_id, source):
    return {"cell_type": "markdown", "id": cell_id, "metadata": {}, "source": source}

def code(cell_id, source):
    return {"cell_type": "code", "id": cell_id, "metadata": {}, "source": source,
            "outputs": [], "execution_count": None}

def teoria_check(cell_id, n, banco=None):
    """Celda unica para una pregunta de teoria: el HTML lo renderiza el autograder.

    `banco`: si la pregunta reutiliza contenido de Preguntas_Teoricas_Semanas1-2.md bajo
    otro numero (p.ej. la numeracion independiente de Semana 2, ver build_nb1.py docstring),
    referencia ese numero original aqui para que quede trazable.
    """
    banco_nota = f" (banco: t{banco})" if banco is not None else ""
    return code(cell_id, f"""\
# ❓ Pregunta t{n}{banco_nota} -- ejecuta esta celda para verla y responder
grader.check_t{n}()""")

LEYENDA_ICONOS = """\
### Leyenda de iconos

| Icono | Accion | Que significa |
|---|---|---|
| 👀 | **OBSERVA** | Ejecuta y observa -- no cambies nada |
| ✏️ | **MODIFICA** | Edita y vuelve a ejecutar |
| 🔮 | **PREDICE** | Escribe tu prediccion *antes* de ejecutar |
| 🧩 | **COMPLETA** | Reemplaza `___` por el valor correcto |
| 🔨 | **CONSTRUYE** | Escribe codigo desde cero en el bloque "Tu codigo aqui" |
| 🔧 | **DEBUG** | Ejecuta, lee el error, corrigelo |
| ✅ | **VERIFICA** | El autograder revisa tu respuesta |
| ❓ | **TEORIA** | Pregunta de opcion multiple (se muestra al ejecutar la celda) |
| 💭 | **REFLEXIONA** | Respuesta abierta, NO calificada por el autograder -- tu profesor la revisa |

---
"""

s1 = []  # Semana 1
s2 = []  # Semana 2

# ═══════════════════════════════════════════════════════════════════════
# SEMANA 1
# ═══════════════════════════════════════════════════════════════════════

s1.append(md("nb1s1-titulo", f"""\
# Mision 1: Recuperacion de Datos
### Semana 1 -- Bootcamp de Pandas con Datos Reales

**Hoy vas a trabajar con un dataset real:** un registro global de ventas de
videojuegos (~16,600 juegos). Llego "crudo" -- nadie lo limpio para ti. Tu trabajo
hoy es aprender a leerlo con honestidad antes de sacar cualquier conclusion.

---

{LEYENDA_ICONOS}"""))

s1.append(md("nb1s1-pandas-intro", """\
## 🧠 Antes de empezar -- ¿que es pandas?

Python por si solo no sabe leer un archivo CSV ni organizar una tabla. Para eso existen
las **librerias**: codigo que ya escribio alguien mas y que tu puedes reutilizar en vez
de escribirlo desde cero. `import` es la palabra que le dice a Python **"trae esa
libreria para que pueda usarla en esta sesion."**

**pandas** es la libreria de Python para trabajar con datos en forma de tabla (filas y
columnas) -- piensa en ella como un Excel programable. Por convencion casi universal se
importa asi:

```python
import pandas as pd
```

`as pd` es solo un apodo (alias) -- evita escribir `pandas` completo cada vez que la
uses. Durante todo el bimestre vas a escribir `pd.algo()`, que siempre significa "usa la
funcion `algo` de la libreria pandas."

La primera funcion que vas a usar es `pd.read_csv('archivo.csv')`: **lee un archivo CSV
y lo convierte en un DataFrame** -- el nombre que pandas le da a una tabla en memoria.
Cada DataFrame que uses en este curso va a vivir en una variable como `df_games`.
"""))

s1.append(code("nb1s1-setup", """\
# Autograder y dataset (repo: Santa-Maria-de-los-Andes/intro_to_stats)
!wget -q "https://raw.githubusercontent.com/Santa-Maria-de-los-Andes/intro_to_stats/main/course-python-stats/Weeks%201-2/autograder_nb1_semana1.py"
!wget -q "https://raw.githubusercontent.com/Santa-Maria-de-los-Andes/intro_to_stats/main/course-python-stats/Weeks%201-2/vgsales_es.csv"
from autograder_nb1_semana1 import Autograder
grader = Autograder()

import pandas as pd  # pd.algo() = "usa la funcion algo de la libreria pandas"

df_games = pd.read_csv('vgsales_es.csv')

print("Dataset cargado.")"""))

s1.append(md("nb1-apertura-md", """\
## 🎬 Apertura -- Dos Titulares

> *"Dos titulares. Los dos hablan de lo mismo. Los dos son 'correctos'. ¿Cual le creerias?"*

**Titular A:** *"En promedio, cada videojuego lanzado vendio 0.54 millones de copias en
todo el mundo."*

**Titular B:** *"El videojuego tipico vendio apenas 0.17 millones de copias en todo el
mundo."*

Ambos numeros salen exactamente de la misma columna (`Ventas_Globales`), del mismo
dataset. Ninguno esta mal calculado. Antes de seguir: **¿cual crees que es "la
verdad"?** Discutan en grupos de dos antes de correr la siguiente celda.
"""))

s1.append(code("nb1-apertura-reveal", """\
# 👀 OBSERVA: la revelacion
promedio = df_games['Ventas_Globales'].mean()
mediana = df_games['Ventas_Globales'].median()
porcentaje_sobre_promedio = (df_games['Ventas_Globales'] > promedio).mean() * 100

print(f"Promedio (media): {promedio:.2f} millones de copias")
print(f"Mediana: {mediana:.2f} millones de copias")
print(f"Solo el {porcentaje_sobre_promedio:.1f}% de los juegos vende MAS que el promedio")"""))

s1.append(md("nb1-apertura-explicacion", """\
**Los dos titulares son correctos.** La diferencia no es un error de calculo -- es que
"promedio" nunca fue una sola cosa. Un pequeño grupo de exitos masivos (Wii Sports vendio
82.74 millones de copias) empuja la media hacia arriba, aunque la mayoria de los juegos
vende mucho menos. Por eso solo ~23% de los juegos supera el "promedio."

> *Se recibio una señal de datos. Esta cruda, sin depurar, posiblemente engañosa si la
> lees mal. Tu mision antes de cerrar la Mision 1: recuperarla, estabilizarla, y aprender
> a leerla con honestidad.*

Para lograrlo necesitas cuatro herramientas: **mirar antes de tocar** (Seccion A),
**resumir con honestidad** (Seccion B) -- esta semana -- y, la proxima semana,
**hacerle preguntas especificas a los datos** (Seccion C) y **comparar grupos sin
sacar conclusiones apresuradas** (Seccion D).
"""))

s1.append(md("nb1-teoria0-md", """\
## 🔓 Teoria Desbloqueada -- Fundamentos

Antes de tocar mas codigo, estos son los conceptos que vas a nombrar y usar durante
todo el bimestre.

### ¿Que es la estadistica?

La estadistica es la ciencia de **recolectar, organizar, analizar e interpretar datos**
para tomar decisiones informadas y entender el mundo. No es un ejercicio academico
abstracto -- es la herramienta que separa "la opinion de alguien" de "lo que realmente
muestra la evidencia":

- **Periodismo:** verificar si un titular sobre "el colegio mas exigente" realmente dice
  lo que parece decir.
- **Medicina:** decidir si un tratamiento funciona mejor que otro.
- **Deporte:** decidir que jugador fichar segun su rendimiento real, no su fama.
- **Gobierno:** decidir donde invertir recursos segun necesidad real.
- **Negocios:** decidir que producto funciona, para quien, y por que.

### Las tres ramas de la estadistica

| Rama | Pregunta que responde | ¿Donde aparece en este curso? |
|---|---|---|
| **Descriptiva** | ¿Que paso? | Semanas 1-5 -- el nucleo de este modulo |
| **Predictiva** | ¿Que es probable que pase? | Semana 6 (regresion lineal) |
| **Prescriptiva** | ¿Que deberiamos hacer al respecto? | Se nombra por completitud -- este curso no construye una herramienta prescriptiva |

> ⚠️ El agrupamiento (k-means, Semana 7) es **descriptivo/exploratorio** -- agrupa lo
> que ya existe -- **no es predictivo**. Es un error comun confundirlo con prediccion.
"""))

s1.append(teoria_check("nb1-t1-check", 1))
s1.append(teoria_check("nb1-t2-check", 2))
s1.append(teoria_check("nb1-t3-check", 3))

# ─── Seccion A -- Aterrizaje ─────────────────────────────────────────────
s1.append(md("nb1-a-header", """\
---
## 📡 Seccion A -- Aterrizaje

Un dataset es una tabla de **observaciones** (filas) y **variables** (columnas) -- no
es "la verdad absoluta," es un **registro** de algo, que puede estar incompleto o tener
errores. `.head()` e `.info()` no son sintaxis para memorizar: son **reconocimiento**
-- antes de analizar cualquier cosa, hay que revisar que se tiene realmente entre manos.
"""))

s1.append(code("nb1-a-guiado", """\
# 👀 OBSERVA: las primeras 5 filas de df_games
df_games.head()"""))

s1.append(md("nb1-a-ex1-md", "#### ✅ Ejercicio 1 -- ¿Cuantas filas y columnas tiene? (8 pts)"))
s1.append(code("nb1-a-ex1-code", """\
# 🧩 COMPLETA
num_filas = ___
num_columnas = ___

print(f"df_games tiene {num_filas} filas y {num_columnas} columnas")"""))
s1.append(code("nb1-a-ex1-check", "grader.check_ex1()"))

s1.append(md("nb1-a-ex2-md", """\
#### ✅ Ejercicio 2 -- Predice antes de mirar (8 pts)

🔮 Antes de ejecutar `.info()`, escribe tu prediccion: ¿cuales columnas crees que son
numericas y cuales son texto?
"""))
s1.append(code("nb1-a-ex2-predice", """\
# 🔮 PREDICE (no se califica, es solo para ti)
mi_prediccion = "___"  # ej: "Año y las columnas de Ventas son numericas"""))
s1.append(code("nb1-a-ex2-guiado", """\
# 👀 OBSERVA
df_games.info()"""))
s1.append(code("nb1-a-ex2-code", """\
# 🧩 COMPLETA: ¿cual columna tiene mas valores faltantes (Non-Null Count mas bajo)?
columna_con_mas_nulos = "___"

print(f"La columna con mas valores faltantes es: {columna_con_mas_nulos}")"""))
s1.append(code("nb1-a-ex2-check", "grader.check_ex2()"))

s1.append(teoria_check("nb1-t9-check", 9))

s1.append(md("nb1-a-practica-md", """\
### 🔁 Practica rapida (no calificada)

`.head()` y `.info()` se aprenden usandolos con distintos argumentos, no solo una vez.
"""))
s1.append(code("nb1-a-practica-head", """\
# ✏️ MODIFICA: cambia el 5 por otro numero (prueba 3, prueba 15) y vuelve a correr
df_games.head(5)"""))
s1.append(code("nb1-a-practica-tail", """\
# ✏️ MODIFICA: .tail() funciona igual que .head() pero desde el final. Prueba distintos numeros.
df_games.tail(5)"""))

s1.append(md("nb1-a-reflexiona-md", """\
#### 💭 Reflexiona (respuesta abierta -- tu profesor la revisa, no el autograder)

En tus propias palabras: ¿por que revisar `.info()` **antes** de calcular cualquier
promedio o hacer cualquier grafico? Da un ejemplo de una conclusion que se veria mal si
te saltas este paso.
"""))
s1.append(code("nb1-a-reflexiona-code", """\
# 💭 REFLEXIONA -- escribe 2-3 oraciones, no hay una unica respuesta correcta
reflexion_a = "___" """))

s1.append(code("nb1-a-checkpoint", """\
# ✅ CHECKPOINT -- necesitas 80% en esta seccion para continuar
grader.check_mini_a()"""))

# ─── Seccion B -- Reconocimiento ─────────────────────────────────────────
s1.append(md("nb1-b-header", """\
---
## 🔎 Seccion B -- Reconocimiento

Aqui formalizamos con datos reales el conflicto de la apertura.

- **Media (promedio):** suma de todos los valores dividida entre la cantidad de
  valores. Sensible a valores extremos -- un solo valor muy alto puede "jalar" la media.
- **Mediana:** el valor central de los datos ordenados de menor a mayor. Resistente a
  valores extremos.
- **Moda:** el valor que se repite con mas frecuencia. Es la mas util cuando los datos
  son categoricos (no numericos).

**Cuando media y mediana difieren mucho, eso es informacion, no ruido** -- indica que la
distribucion esta sesgada. No se trata de que "la mediana es mas correcta"; se trata de
que **cual usar depende de que quieres describir con honestidad**.
"""))

s1.append(code("nb1-b-guiado", """\
# 👀 OBSERVA
df_games['Ventas_Globales'].describe()"""))

s1.append(md("nb1-b-ex3-md", "#### ✅ Ejercicio 3 -- Media vs. mediana, otra vez (10 pts)"))
s1.append(code("nb1-b-ex3-code", """\
# 🧩 COMPLETA: repite el calculo de la apertura, esta vez guardando ambos valores
media_ventas = ___
mediana_ventas = ___
diferencia = media_ventas - mediana_ventas

print(f"Media: {media_ventas:.2f} | Mediana: {mediana_ventas:.2f} | Diferencia: {diferencia:.2f}")"""))
s1.append(code("nb1-b-ex3-check", "grader.check_ex3()"))

s1.append(teoria_check("nb1-t4-check", 4))
s1.append(teoria_check("nb1-t5-check", 5))
s1.append(teoria_check("nb1-t6-check", 6))
s1.append(teoria_check("nb1-t7-check", 7))

s1.append(md("nb1-b-dispersion-md", """\
### Dispersion -- ¿que tan lejos esta cada dato del centro?

Ademas de "donde esta el centro" (media/mediana/moda), otra pregunta igual de
importante es "que tan dispersos estan los datos" -- se mide con la **desviacion
estandar**: en lenguaje simple, "en promedio, que tan lejos esta cada dato del centro."
"""))
s1.append(code("nb1-b-dispersion-guiado", """\
# 👀 OBSERVA
desviacion_ventas = df_games['Ventas_Globales'].std()
print(f"Desviacion estandar: {desviacion_ventas:.2f}")"""))

s1.append(md("nb1-b-ex4-md", """\
#### ✅ Ejercicio 4 -- Repite el patron: media, mediana Y dispersion (10 pts)

🔨 Igual que arriba, pero con `Ventas_NA` (ventas solo en Norteamerica -- un
subconjunto de `Ventas_Globales`) y agregando la desviacion estandar, que todavia no
habias calculado tu mismo.

Variables que espera el autograder: `media_na`, `mediana_na`, `desviacion_na`.
"""))
s1.append(code("nb1-b-ex4-code", """\
# ============================
#      Tu codigo aqui
# ============================


print(f"Media: {media_na:.2f} | Mediana: {mediana_na:.2f} | Desviacion: {desviacion_na:.2f}")"""))
s1.append(code("nb1-b-ex4-check", "grader.check_ex4()"))

s1.append(md("nb1-b-filtro-adelanto-md", """\
### 🔍 Adelanto: quedarte solo con algunas filas

Para encontrar los atipicos necesitas quedarte solo con las filas que cumplen una
condicion -- por ejemplo, "solo los juegos que vendieron mas de 5 millones de copias."
El patron general en pandas es siempre el mismo:

```python
df[df['columna'] operador valor]
```

**La Seccion C de la proxima semana explica en detalle por que funciona esto** (que es
una "mascara booleana" y como combinar condiciones) -- por ahora solo necesitas
reconocer y repetir el patron para el Ejercicio 5.
"""))
s1.append(code("nb1-b-filtro-adelanto-guiado", """\
# 👀 OBSERVA: el patron df[df['columna'] operador valor]
juegos_populares = df_games[df_games['Ventas_Globales'] > 5]
print(f"{len(juegos_populares)} juegos vendieron mas de 5 millones de copias")"""))

s1.append(md("nb1-b-ex5-md", """\
#### ✅ Ejercicio 5 -- Encuentra los atipicos (10 pts)

🔨 Igual que el ejemplo de arriba, pero en vez de un numero fijo (5), el "corte" es
`umbral = media + desviacion_estandar`, y en vez de quedarte con los que venden mas de
un numero fijo, te quedas con los que venden mas que `umbral`.

Variables que espera el autograder: `umbral`, `juegos_atipicos` (el DataFrame filtrado).
"""))
s1.append(code("nb1-b-ex5-code", """\
# 🔨 CONSTRUYE (usa `umbral` como nombre de variable para el limite)

# ============================
#      Tu codigo aqui
# ============================


print(f"Hay {len(juegos_atipicos)} juegos con ventas atipicamente altas")"""))
s1.append(code("nb1-b-ex5-check", "grader.check_ex5()"))

s1.append(teoria_check("nb1-t8-check", 8))

s1.append(md("nb1-b-reflexiona-md", """\
#### 💭 Reflexiona (respuesta abierta -- tu profesor la revisa, no el autograder)

`juegos_atipicos` en Ejercicio 5 son ventas atipicamente **altas**. Piensa en un
contexto real (no videojuegos) donde un valor atipico **bajo** -- no alto -- seria la
señal importante a investigar. ¿Por que ese valor bajo importaria?
"""))
s1.append(code("nb1-b-reflexiona-code", """\
# 💭 REFLEXIONA -- escribe 2-3 oraciones, no hay una unica respuesta correcta
reflexion_b = "___" """))

s1.append(md("nb1-b-debug1-md", """\
#### ✅ Debug 1 -- Corrige el error (10 pts)

🔧 Este codigo deberia calcular el promedio de ventas globales, pero tiene un error.
"""))
s1.append(code("nb1-b-debug1-code", """\
# 🔧 DEBUG: corrige el nombre de la columna
promedio_ventas = df_games['Venta_Globales'].mean()
print(promedio_ventas)"""))
s1.append(code("nb1-b-debug1-check", "grader.check_debug1()"))

s1.append(code("nb1-b-checkpoint", "grader.check_mini_b()"))

s1.append(md("nb1s1-cierre", """\
---
## 🏁 Fin de la Semana 1

Dataset cargado, explorado, y resumido con honestidad. La **Semana 2** continua la
Mision 1 con un segundo dataset mucho mas grande -- abre el siguiente notebook cuando
llegue el momento.
"""))
s1.append(code("nb1s1-resumen", "grader.resumen()"))

# ═══════════════════════════════════════════════════════════════════════
# SEMANA 2
# ═══════════════════════════════════════════════════════════════════════

s2.append(md("nb1s2-titulo", f"""\
# Mision 1: Recuperacion de Datos
### Semana 2 -- Tarea Nueva

La semana pasada aterrizaste y resumiste con honestidad un dataset de videojuegos.
Esta semana es una **tarea nueva y separada**: otro dataset (`df_atletas`), y tus
propios ejercicios -- empiezan otra vez desde el Ejercicio 0.

{LEYENDA_ICONOS}"""))

s2.append(code("nb1s2-setup", """\
# Autograder (aun no publicado -- ver nota al pie de build_nb1.py) y dataset
# (repo: Santa-Maria-de-los-Andes/intro_to_stats)
!wget -q "https://raw.githubusercontent.com/Santa-Maria-de-los-Andes/intro_to_stats/main/course-python-stats/Weeks%201-2/autograder_nb1_semana2.py"
!wget -q "https://raw.githubusercontent.com/Santa-Maria-de-los-Andes/intro_to_stats/main/course-python-stats/Weeks%201-2/athlete_events_es.csv"
from autograder_nb1_semana2 import Autograder
grader = Autograder()

import pandas as pd

df_atletas = pd.read_csv('athlete_events_es.csv')

print("Dataset cargado.")"""))

s2.append(md("nb1-c-pivot", """\
## 🌐 Un Dataset Nuevo, Mucho Mas Grande

Esta semana trabajas con `df_atletas`: 271,116 registros de atletas olimpicos
(1896-2016). Es demasiado grande para leerlo fila por fila -- necesitas **hacerle
preguntas especificas**.

De aqui en adelante, todo lo que hagas en este notebook usa **unicamente**
`df_atletas`. No vuelves a tocar el dataset de videojuegos de la semana pasada.
"""))

s2.append(md("nb1-repaso-header", """\
---
## 🧮 Antes de Filtrar -- Repaso de tus Herramientas de Resumen

Ya usaste `.mean()`, `.median()` y `.std()` la semana pasada sobre otro dataset. Aqui
repites exactamente los mismos metodos, ahora sobre `df_atletas`, antes de aprender a
filtrar (Seccion C) y agrupar (Seccion D).

| Metodo | Que calcula | Cuando usarlo |
|---|---|---|
| `.mean()` | La **media** -- suma de todos los valores dividida entre la cantidad de valores | "El promedio," cuando no hay valores extremos que lo distorsionen |
| `.median()` | La **mediana** -- el valor central de los datos ordenados de menor a mayor | Cuando hay valores extremos (atipicos) que pueden arrastrar la media |
| `.std()` | La **desviacion estandar** -- en promedio, que tan lejos esta cada dato del centro | Para medir que tan dispersos (o concentrados) estan los datos |

Los tres se llaman igual: `df['columna'].metodo()` -- solo cambia la columna y el
metodo, el patron no cambia.
"""))

s2.append(code("nb1-repaso-guiado", """\
# 👀 OBSERVA: los tres metodos, sobre la columna Peso de TODOS los atletas
print("Media de Peso:", df_atletas['Peso'].mean().round(1))               # promedio -- sensible a valores extremos
print("Mediana de Peso:", df_atletas['Peso'].median())                     # centro real, resistente a extremos
print("Desviacion estandar de Peso:", df_atletas['Peso'].std().round(1))   # que tan dispersos estan los pesos"""))

s2.append(md("nb1-ex0-md", """\
#### ✅ Ejercicio 0 -- Repite el patron: mean, median, std (10 pts)

🔨 Igual que arriba, pero sobre la columna `Altura` en vez de `Peso`.

Variables que espera el autograder: `media_altura`, `mediana_altura`, `desviacion_altura`.
"""))
s2.append(code("nb1-ex0-code", """\
# ============================
#      Tu codigo aqui
# ============================


print(f"Media: {media_altura:.1f} | Mediana: {mediana_altura} | Desviacion: {desviacion_altura:.1f}")"""))
s2.append(code("nb1-ex0-check", "grader.check_ex0()"))

s2.append(md("nb1-c-header", """\
---
## 🎯 Seccion C -- Filtra el Ruido

Filtrar es **hacerle una pregunta especifica a los datos** ("muestrame solo los
atletas mayores de 30 años"), no un truco de sintaxis. El filtro no borra nada del
dataset original -- crea una vista para responder tu pregunta.

Ya usaste este patron una vez, sin explicacion, en el Ejercicio 5 de la semana pasada
(`df[df['columna'] > umbral]` para encontrar atipicos). Ahora vemos **por que funciona**.
"""))

s2.append(md("nb1-c-teoria-mascara", """\
### 🔍 ¿Como funciona un filtro booleano?

Cuando escribes `df['Edad'] > 20`, pandas no te devuelve un numero -- te devuelve una
columna de `True`/`False`, una por cada fila, segun si esa fila cumple la condicion.
Eso se llama una **mascara booleana**.

```python
df_atletas['Edad'] > 20
# 0      True
# 1      False
# 2      True
# ...
```

Cuando pones esa mascara dentro de `df[...]`, pandas te devuelve **solo las filas
donde la mascara es `True`**:

```python
df_atletas[df_atletas['Edad'] > 20]
```

El dataset original **no cambia** -- esto crea una vista nueva con el subconjunto que
cumple tu pregunta. El patron general es siempre: `df[df['columna'] operador valor]`.
"""))

s2.append(code("nb1-c-mascara-guiado", """\
# 👀 OBSERVA: la mascara booleana, antes de filtrar
mascara = df_atletas['Edad'] > 20   # compara CADA fila: True si Edad > 20, False si no -- no filtra nada todavia
print(mascara.head())                # confirma visualmente que es una columna de True/False, no un numero
print(mascara.sum(), "filas cumplen la condicion")   # .sum() cuenta los True (True=1, False=0 al sumar)"""))

s2.append(md("nb1-c-repeticion-md", """\
### 🔁 Practica repetida: mismo patron, distintos datos

El filtrado se aprende repitiendolo con preguntas distintas. Cada ejemplo guiado va
seguido de un ejercicio que usa **exactamente el mismo patron** con otra columna o
otro valor.
"""))

s2.append(md("nb1-c-ejemplo1-md", "**Ejemplo guiado 1 -- filtro numerico + estadisticas sobre el subconjunto:**"))
s2.append(code("nb1-c-ejemplo1-code", """\
# 👀 OBSERVA: filtrar crea un DataFrame NUEVO -- no un resumen, no un numero
df_mayores20 = df_atletas[df_atletas['Edad'] > 20]   # aplica la mascara: solo sobreviven las filas con Edad > 20

print(df_mayores20.head())      # las primeras 5 filas del SUBCONJUNTO -- es una tabla real, se puede explorar
print("Media de edad (mayores de 20):", df_mayores20['Edad'].mean().round(1))   # .mean() sobre el subconjunto
print("Mediana de edad (mayores de 20):", df_mayores20['Edad'].median())        # .median() sobre el mismo subconjunto
df_mayores20.info()              # .info() confirma cuantas filas quedaron y que columnas conserva"""))

s2.append(md("nb1-c-leverage-md", """\
☝️ **`df_mayores20` es un DataFrame completo**, no un resumen ni un numero suelto.
Lo puedes seguir usando exactamente igual que `df_atletas`: filtrarlo de nuevo,
agruparlo (Seccion D), graficarlo, o pasarlo a otra funcion. Filtrar nunca "gasta" el
dato -- solo crea una vista nueva que puedes seguir aprovechando.
"""))

s2.append(md("nb1-ex1-md", """\
#### ✅ Ejercicio 1 -- Repite el patron (numerico) (10 pts)

🔨 Igual que el ejemplo guiado, pero con **Edad > 25**. Guarda el resultado en
`df_mayores25`, muestra sus primeras filas con `.head()`, y calcula la media y la
mediana de `Edad` sobre ese subconjunto.

Variables que espera el autograder: `df_mayores25`, `media_c1`, `mediana_c1`.
"""))
s2.append(code("nb1-ex1-code", """\
# ============================
#      Tu codigo aqui
# ============================


"""))
s2.append(code("nb1-ex1-check", "grader.check_ex1()"))

s2.append(md("nb1-c-ejemplo2-md", "**Ejemplo guiado 2 -- filtro categorico + estadisticas sobre el subconjunto:**"))
s2.append(code("nb1-c-ejemplo2-code", """\
# 👀 OBSERVA: mismo patron, ahora con una columna de TEXTO (categorica) en vez de numerica
df_basket = df_atletas[df_atletas['Deporte'] == 'Baloncesto']   # == compara texto exacto, no un rango

print(df_basket.head())    # otra vez: un DataFrame completo que puedes seguir usando
print("Edad promedio (Baloncesto):", df_basket['Edad'].mean().round(1))
print("Altura promedio (Baloncesto):", df_basket['Altura'].mean().round(1))"""))

s2.append(md("nb1-ex2-md", """\
#### ✅ Ejercicio 2 -- Repite el patron (categorico) (10 pts)

🔨 Igual que el ejemplo guiado, pero con **Deporte == 'Natacion'**. Guarda el
resultado en `df_natacion`, muestra sus primeras filas con `.head()`, y calcula la
edad promedio y el peso promedio de ese subconjunto.

Variables que espera el autograder: `df_natacion`, `edad_promedio_natacion`,
`peso_promedio_natacion`.
"""))
s2.append(code("nb1-ex2-code", """\
# ============================
#      Tu codigo aqui
# ============================


"""))
s2.append(code("nb1-ex2-check", "grader.check_ex2()"))

s2.append(md("nb1-c-outlier-md", """\
### ⚠️ Un aviso importante antes de seguir

Un **valor atipico (outlier)** es una observacion inusual, **no** es automaticamente un
error o "dato malo." En `df_atletas` hay un jugador de baloncesto de 226 cm de altura
(Yao Ming) y una gimnasta de 127 cm (Rosario Briones) -- ambos son datos reales y
validos, no errores de registro.
"""))

s2.append(teoria_check("nb1-t0-check", 0, banco=10))
s2.append(teoria_check("nb1-t1-check", 1, banco=11))

s2.append(md("nb1-c-debug0-md", """\
#### ✅ Debug 0 -- Corrige el error (10 pts)

🔧 Este codigo deberia filtrar solo a las mujeres, pero tiene un error.
"""))
s2.append(code("nb1-c-debug0-code", """\
# 🔧 DEBUG: ejecuta, lee el mensaje completo, e identifica que tipo de error es antes de corregirlo
df_mujeres = df_atletas[df_atletas['Sexo'] = 'F']
print(len(df_mujeres))"""))
s2.append(code("nb1-c-debug0-check", "grader.check_debug0()"))

s2.append(md("nb1-c-teoria-combinar", """\
### 🔗 Combinando condiciones: `&` y `|`

Puedes hacerle preguntas mas especificas a los datos combinando condiciones:
- `&` significa **Y** (ambas condiciones deben cumplirse)
- `|` significa **O** (basta con que se cumpla una)

⚠️ Dos reglas que rompen el codigo si las olvidas:
1. Cada condicion va entre **parentesis**: `(df['Edad'] > 20) & (df['Deporte'] == 'Voleibol')`
2. Se usa `&` / `|` -- **no** las palabras de Python `and`/`or`. Esas no funcionan
   sobre columnas de pandas y producen un error.
"""))

s2.append(code("nb1-c-combinar-guiado", """\
# 👀 OBSERVA: filtro combinado -- mayores de 20 años que juegan Voleibol
df_voley_mayores = df_atletas[
    (df_atletas['Edad'] > 20) & (df_atletas['Deporte'] == 'Voleibol')   # ambas condiciones entre parentesis, unidas con &
]

print(df_voley_mayores.head())    # sigue siendo un DataFrame completo, ahora con dos condiciones aplicadas
print(f"{len(df_voley_mayores)} registros")
print("Altura promedio:", df_voley_mayores['Altura'].mean().round(1))"""))

s2.append(teoria_check("nb1-t2-check", 2))

s2.append(md("nb1-ex3-md", """\
#### ✅ Ejercicio 3 -- Repite el patron (combinado) (12 pts)

🔨 Igual que el ejemplo guiado, pero con **Edad > 25 Y Deporte == 'Baloncesto'**.
Reporta cuantos hay y su altura promedio.

Variables que espera el autograder: `df_basket_mayores25`, `cantidad_c3`,
`altura_promedio_c3`.
"""))
s2.append(code("nb1-ex3-code", """\
# ============================
#      Tu codigo aqui
# ============================


"""))
s2.append(code("nb1-ex3-check", "grader.check_ex3()"))

s2.append(md("nb1-c-debug1-md", """\
#### ✅ Debug 1 -- Corrige el error (10 pts)

🔧 Este codigo deberia filtrar a los mayores de 20 años que juegan Voleibol, pero tiene
un error -- ejecutalo, lee el mensaje, y recuerda la regla de arriba.
"""))
s2.append(code("nb1-c-debug1-code", """\
# 🔧 DEBUG: "and" no funciona sobre columnas de pandas -- ¿que simbolo va en su lugar?
df_resultado = df_atletas[df_atletas['Edad'] > 20 and df_atletas['Deporte'] == 'Voleibol']
print(len(df_resultado))"""))
s2.append(code("nb1-c-debug1-check", "grader.check_debug1()"))

s2.append(code("nb1-c-checkpoint", "grader.check_mini_c()"))

# ─── Seccion D -- Compara Grupos ─────────────────────────────────────────
s2.append(md("nb1-d-header", """\
---
## 📊 Seccion D -- Compara Grupos

Comparar promedios por subgrupo es donde vive el verdadero hallazgo: el promedio
general puede esconder lo que realmente pasa dentro de cada grupo.

> ⚠️ Comparar grupos muestra **que** es diferente, **no por que** es diferente. Si un
> pais tiene mas medallas en promedio que otro, eso es una diferencia observada -- no
> una explicacion. (La Semana 5 esta dedicada por completo a esta distincion.)
"""))

s2.append(md("nb1-d-teoria-groupby", """\
### 🔍 ¿Como funciona `groupby()`?

`.groupby('columna')` no calcula nada por si solo -- **separa** las filas de tu
DataFrame en grupos segun los valores de esa columna (un grupo por cada deporte, por
ejemplo). Para obtener un resultado todavia necesitas decir **que columna resumir** y
**con que metodo**:

```python
df_atletas.groupby('Deporte')['Altura'].mean()
#          1. separa en grupos   2. elige la columna   3. resume CADA grupo
```

Los mismos metodos que ya conoces -- `.mean()`, `.median()`, `.std()` -- funcionan
igual aqui, solo que ahora se aplican **por grupo** en vez de sobre toda la columna a
la vez.
"""))

s2.append(code("nb1-d-groupby-guiado", """\
# 👀 OBSERVA: groupby() separa en grupos -- el resumen es un paso APARTE
grupos = df_atletas.groupby('Deporte')['Altura']   # solo agrupa: todavia no hay ningun numero calculado
print(type(grupos))                                  # confirma que esto NO es un DataFrame ni un numero todavia

print(grupos.mean().head())    # ahora si: .mean() calcula el promedio DENTRO de cada grupo"""))

s2.append(teoria_check("nb1-t3-check", 3))

s2.append(md("nb1-d-repeticion-md", """\
### 🔁 Practica repetida: mismo patron, distintos datos

Igual que en la Seccion C -- cada ejemplo guiado va seguido de un ejercicio que repite
el mismo patron con otra columna.
"""))

s2.append(md("nb1-d-ejemplo1-md", "**Ejemplo guiado 1 -- agrupar por una columna categorica:**"))
s2.append(code("nb1-d-guiado", """\
# 👀 OBSERVA: altura promedio por deporte (los 5 deportes con mas registros)
deportes_top = df_atletas['Deporte'].value_counts().head(5).index   # .value_counts() cuenta filas por deporte; .head(5) se queda con los 5 mas frecuentes
df_atletas[df_atletas['Deporte'].isin(deportes_top)] \\
    .groupby('Deporte')['Altura'].mean().round(1)   # .isin() filtra solo esos 5 deportes ANTES de agrupar y promediar"""))

s2.append(md("nb1-ex4-md", """\
#### ✅ Ejercicio 4 -- Repite el patron (12 pts)

🔨 Compara el **peso** promedio entre los mismos 5 deportes (`deportes_top`, ya
definido arriba).

Variable que espera el autograder: `peso_por_deporte`.
"""))
s2.append(code("nb1-ex4-code", """\
# ============================
#      Tu codigo aqui
# ============================


print(peso_por_deporte.sort_values(ascending=False))"""))
s2.append(code("nb1-ex4-check", "grader.check_ex4()"))

s2.append(md("nb1-d-debug2-md", """\
#### ✅ Debug 2 -- Corrige el error (10 pts)

🔧 Este codigo deberia agrupar por deporte y promediar la edad, pero tiene un error.
Ejecutalo, lee el mensaje completo, e identifica que tipo de error es antes de
corregirlo.
"""))
s2.append(code("nb1-d-debug2-code", """\
# 🔧 DEBUG
edad_por_deporte = df_atletas.groupby('Deporte')['Edd'].mean()
print(edad_por_deporte.head())"""))
s2.append(code("nb1-d-debug2-check", "grader.check_debug2()"))

s2.append(md("nb1-d-ejemplo2-md", "**Ejemplo guiado 2 -- agrupar por otra columna categorica:**"))
s2.append(code("nb1-d-ejemplo2-code", """\
# 👀 OBSERVA: mismo patron -- agrupar() + mean(), ahora por Sexo en vez de Deporte
df_atletas.groupby('Sexo')['Edad'].mean().round(1)"""))

s2.append(md("nb1-ex5-md", """\
#### ✅ Ejercicio 5 -- Repite el patron (11 pts)

🔨 Compara la edad promedio entre **Verano** e **Invierno** (columna `Temporada`).

Variable que espera el autograder: `edad_por_temporada`.
"""))
s2.append(code("nb1-ex5-code", """\
# ============================
#      Tu codigo aqui
# ============================


print(edad_por_temporada)"""))
s2.append(code("nb1-ex5-check", "grader.check_ex5()"))

s2.append(teoria_check("nb1-t4-check", 4, banco=12))

s2.append(md("nb1-d-teoria-combinar", """\
### 🔗 Combina lo que ya sabes

Ya sabes filtrar (Seccion C) y agrupar (esta seccion) -- se pueden combinar: primero
filtras a un subconjunto, despues agrupas *ese* subconjunto.
"""))

s2.append(md("nb1-d-ejemplo3-md", "**Ejemplo guiado 3 -- filtrar y despues agrupar:**"))
s2.append(code("nb1-d-ejemplo3-code", """\
# 👀 OBSERVA: primero filtra (Seccion C), despues agrupa (esta seccion) -- el mismo df_verano se reutiliza en las dos lineas
df_verano = df_atletas[df_atletas['Temporada'] == 'Verano']              # 1. filtra: solo temporada de Verano
deportes_verano_top = df_verano['Deporte'].value_counts().head(5).index  # 2. de ESE subconjunto, los 5 deportes mas frecuentes

df_verano[df_verano['Deporte'].isin(deportes_verano_top)] \\
    .groupby('Deporte')['Edad'].mean().round(1)   # 3. agrupa y promedia, todo sobre el subconjunto ya filtrado"""))

s2.append(md("nb1-ex6-md", """\
#### ✅ Ejercicio 6 -- Repite el patron (combinado) (12 pts)

🔨 Filtra a las **mujeres** (`Sexo == 'F'`), y calcula la **altura** promedio por
deporte entre los 5 deportes con mas registros dentro de ese subconjunto.

Variables que espera el autograder: `df_mujeres`, `altura_por_deporte_mujeres`.
"""))
s2.append(code("nb1-ex6-code", """\
# ============================
#      Tu codigo aqui
# ============================


print(altura_por_deporte_mujeres.sort_values(ascending=False))"""))
s2.append(code("nb1-ex6-check", "grader.check_ex6()"))

s2.append(md("nb1-d-debug3-md", """\
#### ✅ Debug 3 -- Corrige el error (10 pts)

🔧 Este codigo deberia agrupar por pais (`CON`) y promediar la edad, pero tiene un
error. Ejecutalo, lee el mensaje completo, e identifica que tipo de error es antes de
corregirlo.
"""))
s2.append(code("nb1-d-debug3-code", """\
# 🔧 DEBUG
edad_por_pais = df_atletas.groupby('CON')['Edad'].means()
print(edad_por_pais.head())"""))
s2.append(code("nb1-d-debug3-check", "grader.check_debug3()"))

s2.append(code("nb1-d-checkpoint", "grader.check_mini_d()"))

s2.append(md("nb1-fin-clase2", """\
---
## 🏁 Fin del trabajo en clase

Todo lo de arriba se trabaja en sesion. **Lo que sigue -- Integracion y el Reto bonus
-- es tarea**: completalo antes de la proxima clase.
"""))

# ─── Integracion (Tarea) ─────────────────────────────────────────────────
s2.append(md("nb1-intex-header", """\
---
## 🧬 Integracion -- Pipeline Completo (Tarea)

Ya no son ejercicios aislados: aqui usas **cargar → filtrar → agrupar → interpretar**
en un solo flujo, siempre sobre `df_atletas`. En cada uno, responde: ¿cual es el
promedio? ¿cual es la dispersion? ¿que dice -- y que NO dice -- el resultado?
"""))

s2.append(md("nb1-intex0-md", """\
#### ✅ Integracion 0 -- ¿Que tan alto es un jugador olimpico de Baloncesto? (8 pts)

🔨 Filtra `df_atletas` a `Deporte == 'Baloncesto'`. Calcula la altura promedio y la
desviacion estandar de la altura de ese subconjunto. Escribe una frase con tu
hallazgo.

Variables que espera el autograder: `df_basket`, `altura_promedio_basket`,
`desviacion_altura_basket`, `interpretacion_intex0` (string).
"""))
s2.append(code("nb1-intex0-code", """\
# ============================
#      Tu codigo aqui
# ============================



interpretacion_intex0 = "___"  # una frase: ¿que encontraste?"""))
s2.append(code("nb1-intex0-check", "grader.check_intex0()"))

s2.append(md("nb1-intex1-md", """\
#### ✅ Integracion 1 -- ¿Quienes son mas jovenes: Baloncesto o Gimnasia? (8 pts)

🔨 Calcula la edad promedio de los atletas de `Baloncesto` y, por separado, de
`Gimnasia`. Resta ambos promedios para obtener la diferencia. Escribe una frase con tu
hallazgo: ¿cual de los dos deportes tiene, en promedio, atletas mas jovenes?

Variables que espera el autograder: `edad_promedio_basket`, `edad_promedio_gimnasia`,
`diferencia_edad_basket_gimnasia`, `interpretacion_intex1` (string).
"""))
s2.append(code("nb1-intex1-code", """\
# ============================
#      Tu codigo aqui
# ============================



interpretacion_intex1 = "___"  # una frase: ¿que encontraste?"""))
s2.append(code("nb1-intex1-check", "grader.check_intex1()"))

s2.append(md("nb1-intex2-md", """\
#### ✅ Integracion 2 -- Peru en los Juegos Olimpicos (7 pts)

🔨 Filtra `df_atletas` a Peru (`CON == 'PER'`), cuenta cuantos registros hay por
`Deporte`. Escribe una frase con tu hallazgo.

Variables que espera el autograder: `df_peru`, `deportes_peru`,
`interpretacion_intex2` (string).
"""))
s2.append(code("nb1-intex2-code", """\
# ============================
#      Tu codigo aqui
# ============================



interpretacion_intex2 = "___"  # una frase: ¿que encontraste?"""))
s2.append(code("nb1-intex2-check", "grader.check_intex2()"))

s2.append(md("nb1-intex3-md", """\
#### ❓ Integracion 3 -- Opcion multiple sobre tu propio hallazgo (5 pts)

En Integracion 1 encontraste una diferencia de edad promedio entre Baloncesto y
Gimnasia. Ejecuta la celda para ver la pregunta y responder: ¿que se puede concluir
correctamente de esa diferencia?
"""))
s2.append(code("nb1-intex3-check", """\
# ❓ Integracion 3 -- pregunta de opcion multiple sobre tu hallazgo de Integracion 1
grader.check_intex3()"""))

s2.append(md("nb1-intex4-md", """\
#### ✅ Integracion 4 -- ¿Que deporte tiene la altura MAS variable? (7 pts)

🔨 Entre los 5 deportes con mas registros (`deportes_top`, calculado en la Seccion D),
agrupa por `Deporte` y calcula la **desviacion estandar** de `Altura` para cada uno --
no el promedio esta vez. ¿Cual deporte tiene la altura mas dispersa (menos uniforme)?
Escribe una frase con tu hallazgo.

Variables que espera el autograder: `desviacion_altura_por_deporte`,
`interpretacion_intex4` (string).
"""))
s2.append(code("nb1-intex4-code", """\
# ============================
#      Tu codigo aqui
# ============================



interpretacion_intex4 = "___"  # una frase: ¿que encontraste?
print(desviacion_altura_por_deporte.sort_values(ascending=False))"""))
s2.append(code("nb1-intex4-check", "grader.check_intex4()"))

# ─── Bonus ────────────────────────────────────────────────────────────
s2.append(md("nb1-reto-md", """\
---
## 🏆 Reto Bonus (opcional)

🔨 Elige tu propia combinacion de filtro + `.groupby()` sobre `df_atletas`. Encuentra
algo que te parezca interesante y escribe una frase explicandolo.
"""))
s2.append(code("nb1-reto-code", """\
# ============================
#      Tu codigo aqui
# ============================



hallazgo_reto1 = "___"  # tu frase"""))
s2.append(code("nb1-reto-check", "grader.check_reto1()"))

# ─── Cierre ───────────────────────────────────────────────────────────
s2.append(md("nb1-final-header", "---\n## 🏁 Puntaje Final -- Mision 1 Completa"))
s2.append(code("nb1-resumen", "grader.resumen()"))

# ═══════════════════════════════════════════════════════════════════════
# ESCRIBIR AMBOS NOTEBOOKS
# ═══════════════════════════════════════════════════════════════════════

def write_notebook(cells, filename):
    nb = {
        "nbformat": 4, "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.10.0"},
        },
        "cells": cells,
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print(f"OK: {filename} generado - {len(cells)} celdas")

write_notebook(s1, "nb1_semana1_recuperacion_datos.ipynb")
write_notebook(s2, "nb1_semana2_recuperacion_datos.ipynb")

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
Secciones C-D). Semana 2 tambien recarga df_games porque intex1 (tarea) lo usa.
Tema visual: placeholder neutro -- pendiente PIXEL (ticket #2, WORKFORCE_HANDOFF.md).

Convenciones:
  - check_tN: una sola celda de codigo (`grader.check_tN()`). El autograder renderiza
    la pregunta + opciones como HTML y captura la respuesta.
  - check_exN etiquetados 🔨 CONSTRUYE: el notebook NO trae la solucion escrita, solo
    instrucciones + un bloque "Tu codigo aqui" en blanco.
  - check_exN etiquetados 🧩 COMPLETA: mantienen el patron de blancos `___`.
  - La numeracion de check_exN/check_debugN/check_tN es GLOBAL a la Mision 1 (no se
    reinicia en Semana 2) para que el progreso se pueda rastrear como una sola mision
    aunque viva en dos archivos.

Nota para ATLAS (ticket #10, WORKFORCE_HANDOFF.md): esto implica DOS autograders
separados -- autograder_nb1_semana1.py (check_ex1-5, debug1, t1-9, mini_a, mini_b,
resumen) y autograder_nb1_semana2.py (check_ex6-11, debug2-5, t10-12, mini_c, mini_d,
intex1-2, reto1, resumen) -- no un autograder compartido entre archivos. Cada uno
necesita su propio `notebook` id en el payload de Supabase (sugerido:
"nb1_semana1" / "nb1_semana2") para que el lookup de "tu mejor puntaje previo" en el
formulario de registro no mezcle las dos sesiones.
"""
import json

def md(cell_id, source):
    return {"cell_type": "markdown", "id": cell_id, "metadata": {}, "source": source}

def code(cell_id, source):
    return {"cell_type": "code", "id": cell_id, "metadata": {}, "source": source,
            "outputs": [], "execution_count": None}

def teoria_check(cell_id, n):
    """Celda unica para una pregunta de teoria: el HTML lo renderiza el autograder."""
    return code(cell_id, f"""\
# ❓ Pregunta t{n} -- ejecuta esta celda para verla y responder
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
!wget -q https://raw.githubusercontent.com/Santa-Maria-de-los-Andes/intro_to_stats/main/autograder_nb1_semana1.py
!wget -q "https://raw.githubusercontent.com/Santa-Maria-de-los-Andes/intro_to_stats/main/Weeks%201-2/vgsales_es.csv"
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
mi_prediccion = "___"  # ej: "Anio y las columnas de Ventas son numericas"""))
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
### Semana 2 -- continuacion

La semana pasada aterrizaste y resumiste con honestidad un dataset de videojuegos.

{LEYENDA_ICONOS}"""))

s2.append(code("nb1s2-setup", """\
# Autograder (aun no publicado -- ver nota al pie de build_nb1.py) y datasets
# (repo: Santa-Maria-de-los-Andes/intro_to_stats)
!wget -q https://raw.githubusercontent.com/Santa-Maria-de-los-Andes/intro_to_stats/main/autograder_nb1_semana2.py
!wget -q "https://raw.githubusercontent.com/Santa-Maria-de-los-Andes/intro_to_stats/main/Weeks%201-2/vgsales_es.csv"
!wget -q "https://raw.githubusercontent.com/Santa-Maria-de-los-Andes/intro_to_stats/main/Weeks%201-2/athlete_events_es.csv"
from autograder_nb1_semana2 import Autograder
grader = Autograder()

import pandas as pd

df_games = pd.read_csv('vgsales_es.csv')       # se vuelve a usar en la Integracion (tarea)
df_athletes = pd.read_csv('athlete_events_es.csv')

print("Datasets cargados.")"""))

s2.append(md("nb1-c-pivot", """\
## 🌐 Segundo Paquete de Datos

El primer paquete esta estabilizado. Llega un segundo paquete, mucho mas grande:
271,116 registros de atletas olimpicos (1896-2016). Demasiado grande para leerlo fila
por fila -- necesitas **hacerle preguntas especificas**.
"""))

s2.append(md("nb1-c-header", """\
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
df_athletes['Edad'] > 20
# 0      True
# 1      False
# 2      True
# ...
```

Cuando pones esa mascara dentro de `df[...]`, pandas te devuelve **solo las filas
donde la mascara es `True`**:

```python
df_athletes[df_athletes['Edad'] > 20]
```

El dataset original **no cambia** -- esto crea una vista nueva con el subconjunto que
cumple tu pregunta. El patron general es siempre: `df[df['columna'] operador valor]`.
"""))

s2.append(code("nb1-c-mascara-guiado", """\
# 👀 OBSERVA: la mascara booleana, antes de filtrar
mascara = df_athletes['Edad'] > 20
print(mascara.head())        # True/False por fila
print(mascara.sum(), "filas cumplen la condicion")"""))

s2.append(md("nb1-c-repeticion-md", """\
### 🔁 Practica repetida: mismo patron, distintos datos

El filtrado se aprende repitiendolo con preguntas distintas. Cada ejemplo guiado va
seguido de un ejercicio que usa **exactamente el mismo patron** con otra columna o
otro valor.
"""))

s2.append(md("nb1-c-ejemplo1-md", "**Ejemplo guiado 1 -- filtro numerico + estadisticas sobre el subconjunto:**"))
s2.append(code("nb1-c-ejemplo1-code", """\
# 👀 OBSERVA
df_mayores20 = df_athletes[df_athletes['Edad'] > 20]

print("Media de edad (mayores de 20):", df_mayores20['Edad'].mean().round(1))
print("Mediana de edad (mayores de 20):", df_mayores20['Edad'].median())
df_mayores20.info()"""))

s2.append(md("nb1-c-ex6-md", """\
#### ✅ Ejercicio 6 -- Repite el patron (numerico) (10 pts)

🔨 Igual que el ejemplo guiado, pero con **Edad > 25**. Calcula la media y la mediana
de `Edad` sobre ese subconjunto, y ejecuta `.info()` sobre el resultado.

Variables que espera el autograder: `df_mayores25`, `media_c1`, `mediana_c1`.
"""))
s2.append(code("nb1-c-ex6-code", """\
# ============================
#      Tu codigo aqui
# ============================


"""))
s2.append(code("nb1-c-ex6-check", "grader.check_ex6()"))

s2.append(md("nb1-c-ejemplo2-md", "**Ejemplo guiado 2 -- filtro categorico + estadisticas sobre el subconjunto:**"))
s2.append(code("nb1-c-ejemplo2-code", """\
# 👀 OBSERVA
df_basket = df_athletes[df_athletes['Deporte'] == 'Baloncesto']

print("Edad promedio (Baloncesto):", df_basket['Edad'].mean().round(1))
print("Altura promedio (Baloncesto):", df_basket['Altura'].mean().round(1))"""))

s2.append(md("nb1-c-ex7-md", """\
#### ✅ Ejercicio 7 -- Repite el patron (categorico) (10 pts)

🔨 Igual que el ejemplo guiado, pero con **Deporte == 'Natacion'**. Calcula la edad
promedio y el peso promedio de ese subconjunto.

Variables que espera el autograder: `df_natacion`, `edad_promedio_natacion`,
`peso_promedio_natacion`.
"""))
s2.append(code("nb1-c-ex7-code", """\
# ============================
#      Tu codigo aqui
# ============================


"""))
s2.append(code("nb1-c-ex7-check", "grader.check_ex7()"))

s2.append(md("nb1-c-outlier-md", """\
### ⚠️ Un aviso importante antes de seguir

Un **valor atipico (outlier)** es una observacion inusual, **no** es automaticamente un
error o "dato malo." En `df_athletes` hay un jugador de baloncesto de 226 cm de altura
(Yao Ming) y una gimnasta de 127 cm (Rosario Briones) -- ambos son datos reales y
validos, no errores de registro.
"""))

s2.append(teoria_check("nb1-t10-check", 10))
s2.append(teoria_check("nb1-t11-check", 11))

s2.append(md("nb1-c-debug1-md", """\
#### ✅ Debug 2 -- Corrige el error (10 pts)

🔧 Este codigo deberia filtrar solo a las mujeres, pero tiene un error.
"""))
s2.append(code("nb1-c-debug1-code", """\
# 🔧 DEBUG: un solo signo "=" no compara -- asigna. ¿Que operador falta?
df_mujeres = df_athletes[df_athletes['Sexo'] = 'F']
print(len(df_mujeres))"""))
s2.append(code("nb1-c-debug1-check", "grader.check_debug2()"))

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
df_voley_mayores = df_athletes[
    (df_athletes['Edad'] > 20) & (df_athletes['Deporte'] == 'Voleibol')
]

print(f"{len(df_voley_mayores)} registros")
print("Altura promedio:", df_voley_mayores['Altura'].mean().round(1))"""))

s2.append(md("nb1-c-ex8-md", """\
#### ✅ Ejercicio 8 -- Repite el patron (combinado) (12 pts)

🔨 Igual que el ejemplo guiado, pero con **Edad > 25 Y Deporte == 'Baloncesto'**.
Reporta cuantos hay y su altura promedio.

Variables que espera el autograder: `df_basket_mayores25`, `cantidad_c3`,
`altura_promedio_c3`.
"""))
s2.append(code("nb1-c-ex8-code", """\
# ============================
#      Tu codigo aqui
# ============================


"""))
s2.append(code("nb1-c-ex8-check", "grader.check_ex8()"))

s2.append(md("nb1-c-debug2-md", """\
#### ✅ Debug 3 -- Corrige el error (10 pts)

🔧 Este codigo deberia filtrar a los mayores de 20 años que juegan Voleibol, pero tiene
un error -- ejecutalo, lee el mensaje, y recuerda la regla de arriba.
"""))
s2.append(code("nb1-c-debug2-code", """\
# 🔧 DEBUG: "and" no funciona sobre columnas de pandas -- ¿que simbolo va en su lugar?
df_resultado = df_athletes[df_athletes['Edad'] > 20 and df_athletes['Deporte'] == 'Voleibol']
print(len(df_resultado))"""))
s2.append(code("nb1-c-debug2-check", "grader.check_debug3()"))

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

s2.append(md("nb1-d-repeticion-md", """\
### 🔁 Practica repetida: mismo patron, distintos datos

Igual que en la Seccion C -- cada ejemplo guiado va seguido de un ejercicio que repite
el mismo patron con otra columna.
"""))

s2.append(md("nb1-d-ejemplo1-md", "**Ejemplo guiado 1 -- agrupar por una columna categorica:**"))
s2.append(code("nb1-d-guiado", """\
# 👀 OBSERVA: altura promedio por deporte (los 5 deportes con mas registros)
deportes_top = df_athletes['Deporte'].value_counts().head(5).index
df_athletes[df_athletes['Deporte'].isin(deportes_top)].groupby('Deporte')['Altura'].mean().round(1)"""))

s2.append(md("nb1-d-ex9-md", """\
#### ✅ Ejercicio 9 -- Repite el patron (12 pts)

🔨 Compara el **peso** promedio entre los mismos 5 deportes (`deportes_top`, ya
definido arriba).

Variable que espera el autograder: `peso_por_deporte`.
"""))
s2.append(code("nb1-d-ex9-code", """\
# ============================
#      Tu codigo aqui
# ============================


print(peso_por_deporte.sort_values(ascending=False))"""))
s2.append(code("nb1-d-ex9-check", "grader.check_ex9()"))

s2.append(teoria_check("nb1-t12-check", 12))

s2.append(md("nb1-d-debug1-md", """\
#### ✅ Debug 4 -- Corrige el error (10 pts)

🔧 Este codigo deberia agrupar por deporte y promediar la edad, pero tiene un error.
Ejecutalo, lee el mensaje completo, e identifica que tipo de error es antes de
corregirlo.
"""))
s2.append(code("nb1-d-debug1-code", """\
# 🔧 DEBUG
edad_por_deporte = df_athletes.groupby('Deporte')['Edd'].mean()
print(edad_por_deporte.head())"""))
s2.append(code("nb1-d-debug1-check", "grader.check_debug4()"))

s2.append(md("nb1-d-ejemplo2-md", "**Ejemplo guiado 2 -- agrupar por otra columna categorica:**"))
s2.append(code("nb1-d-ejemplo2-code", """\
# 👀 OBSERVA: edad promedio por sexo
df_athletes.groupby('Sexo')['Edad'].mean().round(1)"""))

s2.append(md("nb1-d-ex10-md", """\
#### ✅ Ejercicio 10 -- Repite el patron (11 pts)

🔨 Compara la edad promedio entre **Verano** e **Invierno** (columna `Temporada`).

Variable que espera el autograder: `edad_por_temporada`.
"""))
s2.append(code("nb1-d-ex10-code", """\
# ============================
#      Tu codigo aqui
# ============================


print(edad_por_temporada)"""))
s2.append(code("nb1-d-ex10-check", "grader.check_ex10()"))

s2.append(md("nb1-d-teoria-combinar", """\
### 🔗 Combina lo que ya sabes

Ya sabes filtrar (Seccion C) y agrupar (esta seccion) -- se pueden combinar: primero
filtras a un subconjunto, despues agrupas *ese* subconjunto.
"""))

s2.append(md("nb1-d-ejemplo3-md", "**Ejemplo guiado 3 -- filtrar y despues agrupar:**"))
s2.append(code("nb1-d-ejemplo3-code", """\
# 👀 OBSERVA: solo temporada de Verano, edad promedio por deporte
df_verano = df_athletes[df_athletes['Temporada'] == 'Verano']
deportes_verano_top = df_verano['Deporte'].value_counts().head(5).index

df_verano[df_verano['Deporte'].isin(deportes_verano_top)].groupby('Deporte')['Edad'].mean().round(1)"""))

s2.append(md("nb1-d-ex11-md", """\
#### ✅ Ejercicio 11 -- Repite el patron (combinado) (12 pts)

🔨 Filtra a las **mujeres** (`Sexo == 'F'`), y calcula la **altura** promedio por
deporte entre los 5 deportes con mas registros dentro de ese subconjunto.

Variables que espera el autograder: `df_mujeres`, `altura_por_deporte_mujeres`.
"""))
s2.append(code("nb1-d-ex11-code", """\
# ============================
#      Tu codigo aqui
# ============================


print(altura_por_deporte_mujeres.sort_values(ascending=False))"""))
s2.append(code("nb1-d-ex11-check", "grader.check_ex11()"))

s2.append(md("nb1-d-debug2-md", """\
#### ✅ Debug 5 -- Corrige el error (10 pts)

🔧 Este codigo deberia agrupar por pais (`CON`) y promediar la edad, pero tiene un
error. Ejecutalo, lee el mensaje completo, e identifica que tipo de error es antes de
corregirlo.
"""))
s2.append(code("nb1-d-debug2-code", """\
# 🔧 DEBUG
edad_por_pais = df_athletes.groupby('CON')['Edad'].means()
print(edad_por_pais.head())"""))
s2.append(code("nb1-d-debug2-check", "grader.check_debug5()"))

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
en un solo flujo, sobre cada dataset completo. Responde en cada uno: ¿cual es el
promedio? ¿cual es la dispersion? ¿quien es un atipico?
"""))

s2.append(md("nb1-intex1-md", """\
#### ✅ Integracion 1 -- Videojuegos (8 pts)

🔨 Elige un genero (`Genero`), filtra `df_games`, agrupa por `Plataforma` y calcula el
promedio de `Ventas_Globales`. Escribe una frase con tu hallazgo.

Variables que espera el autograder: `df_genero`, `ventas_por_plataforma`,
`interpretacion_intex1` (string).
"""))
s2.append(code("nb1-intex1-code", """\
# ============================
#      Tu codigo aqui
# ============================



interpretacion_intex1 = "___"  # una frase: ¿que encontraste?"""))
s2.append(code("nb1-intex1-check", "grader.check_intex1()"))

s2.append(md("nb1-intex2-md", """\
#### ✅ Integracion 2 -- Atletas (7 pts)

🔨 Filtra `df_athletes` a Peru (`CON == 'PER'`), cuenta cuantos registros hay por
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

# ─── Bonus ────────────────────────────────────────────────────────────
s2.append(md("nb1-reto-md", """\
---
## 🏆 Reto Bonus (opcional)

🔨 Elige tu propia combinacion de filtro + `.groupby()` en cualquiera de los dos
datasets. Encuentra algo que te parezca interesante y escribe una frase explicandolo.
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

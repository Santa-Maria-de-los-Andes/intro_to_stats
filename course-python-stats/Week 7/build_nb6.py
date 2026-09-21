# -*- coding: utf-8 -*-
"""
build_nb6.py -- Genera nb6_clustering.ipynb (Semana 7, "Misión 4: El
Cartógrafo de Patrones" -- k-means clustering). Sigue el mismo patrón que
build_nb3.py/build_nb4.py/build_nb5.py: helpers `md`/`code`/`teoria_check`/
`reflexion_check`/`LEYENDA_ICONOS` duplicados aquí a propósito -- cada
build_nbN.py es autocontenido, no importa de otro build script
(COURSE_TEMPLATE.md §3).

check_ex/check_t/check_reto empiezan frescos en 1 -- Semana 7 es una sola
sesión ("one notebook, one session"), igual que Semana 6 (nb5) lo fue
frente a Misión 2 (WORKFORCE_CONTRACT.md §2).

2026-09-19 (revisión): el usuario proveyó un CSV real de Spotify
(`spotify.csv`, 114,000 pistas x 21 columnas, 114 géneros x 1000 pistas
c/u -- el "Spotify Tracks Dataset" de Kaggle) DESPUÉS de la primera
versión de este notebook, que había usado `vgsales_es.csv` como sustituto
porque no existía ningún CSV de audio en el repo todavía. Este notebook
fue reconstruido alrededor del dataset real: `translate_to_spanish.py`
(mismo folder) traduce encabezados y los 114 géneros al español,
produciendo `spotify_es.csv`. Un solo dataset en todo el notebook:
`Bailabilidad`+`Tempo` para el ejemplo guiado, el 🧩 de géneros y el
Ejercicio 1; `Energia` se agrega en el Ejercicio 2. Ver autograder_nb6.py
para la validación empírica completa (rangos reales, comportamiento
escalado/sin escalar, cruce cluster×género, efecto de agregar `Energia`).

Limpieza de datos (guiada, no escrita por el estudiante): 1 fila sin
`Artistas`/`Nombre_Cancion` y 157 filas con `Tempo` = 0 (fallo de
detección del tempo, no una canción real de 0 BPM) se descartan antes de
cualquier ejercicio -- 113,842 filas quedan.

Todo el código de los ejemplos guiados fue verificado ejecutándolo contra
el CSV real (ver _test_nb6.py, mismo folder, y el docstring de
autograder_nb6.py) antes de congelar este build script.

2026-09-21 (adición, no una desviación silenciosa): agregado Concepto 4
("¿por qué importa que un agrupamiento generalice?") + un ejemplo guiado +
Ejercicio 3 ("Prueba tu mapa en territorio nuevo") + una reflexión nueva
("generalizacion"), entre el Ejercicio 2 y el quiz de teoría. Motivación:
la Semana 6 (nb5) ya enseñó train/test para regresión (¿el modelo
generaliza a países que nunca vio?) -- este notebook no tenía el
equivalente para clustering. k-means no tiene una "respuesta correcta" que
un train/test pueda medir como error (no hay R² de prueba), así que el
marco se reformula como generalización/estabilidad: ¿el mismo modelo,
ajustado solo con train, asigna clusters con perfiles parecidos en datos
de prueba que nunca vio? Motivado con dos casos de uso reales
(recomendación de la próxima canción por cluster, segmentación de
canciones para marketing) en vez de una "prueba de accuracy" -- ver
autograder_nb6.py para el rationale completo de por qué "accuracy" no
aplica a un algoritmo sin etiquetas reales. _CORE_MAX sube de 102 a 127
(+20 ex3, +5 refl_generalizacion). Ver WORKFORCE_HANDOFF.md, Done log
2026-09-21, para el registro completo de esta ampliación de alcance.

2026-09-21 (revisión, mismo día -- simplificación deliberada, no una
desviación silenciosa): el usuario, tras revisar el notebook completo,
decidió que Semana 7 es "extra credit para quienes ya avanzaron bien" y
por lo tanto debe ser mayoritariamente muestra + interpretación, con
ejercicios de construcción simples, no tres builds separados sumando 80
pts. Cambios: (1) Ejercicio 2 ("agrega Energia") deja de ser un
`🔨 CONSTRUYE` calificado -- se convierte en una celda `👀 OBSERVA` de
muestra (`nb6-demo-energia-*`) que el estudiante ve pero no construye,
colocada ANTES del Ejercicio 1 para informar su elección de predictores.
(2) Ejercicio 1 se fusiona con la idea de Ejercicio 2: ahora acepta 2 O 3
predictores del menú (antes exactamente 2), así que un solo build cubre
lo que antes eran dos ejercicios separados. (3) Ejercicio 3 ("prueba tu
mapa en territorio nuevo", el build train/test) se elimina por completo
-- el concepto de generalización ya lo enseña el ejemplo guiado
correspondiente (`nb6-guiado-generaliza-*`, sin cambios) y ya lo evalúa la
reflexión `nb6_generalizacion` (conservada, solo reescrita para referirse
"al ejemplo guiado de arriba" en vez de "tu Ejercicio 3"). La reflexión
`nb6_ex2` también se conserva (mismo id, para no requerir un redeploy de
`grade-reflexion/index.ts`) pero ahora compara el resultado propio del
estudiante con la muestra de Energia, no "tu Ejercicio 1 vs. tu Ejercicio
2". _CORE_MAX baja de 127 a 87 (-20 ex2, -20 ex3; ex1 se mantiene en 40).
Ver WORKFORCE_HANDOFF.md, Done log 2026-09-21 (segunda entrada), para el
registro completo.
"""
import json


def md(cell_id, source):
    return {"cell_type": "markdown", "id": cell_id, "metadata": {}, "source": source}


def code(cell_id, source):
    return {"cell_type": "code", "id": cell_id, "metadata": {}, "source": source,
            "outputs": [], "execution_count": None}


def teoria_check(cell_id, n):
    return code(cell_id, f"""\
# ❓ Pregunta t{n} -- ejecuta esta celda para verla y responder
grader.check_t{n}()""")


def reflexion_check(cell_id, id):
    return code(cell_id, f"""\
# 💭 Reflexiona -- ejecuta esta celda para responder
grader.check_reflexion_{id}()""")


LEYENDA_ICONOS = """\
### Leyenda de iconos

| Icono | Acción | Qué significa |
|---|---|---|
| 👀 | **OBSERVA** | Ejecuta y observa -- no cambies nada |
| ✏️ | **MODIFICA** | Edita y vuelve a ejecutar |
| 🔮 | **PREDICE** | Escribe tu predicción en el cuadro de texto antes de ver el resultado -- participación, sin respuesta incorrecta (+1 XP) |
| 📝 | **ANOTA** | Escribe tu idea en el cuadro de texto -- participación, sin respuesta incorrecta (+1 XP) |
| 🧩 | **COMPLETA** | Reemplaza `___` por el valor correcto |
| 🔨 | **CONSTRUYE** | Escribe código desde cero en el bloque "Tu código aquí" |
| 🔧 | **DEBUG** | Ejecuta, lee el error, corrígelo |
| ✅ | **VERIFICA** | El autograder revisa tu respuesta |
| ❓ | **TEORÍA** | Pregunta de opción múltiple (se muestra al ejecutar la celda) |
| 💭 | **REFLEXIONA** | Respuesta abierta -- calificada por IA, feedback instantáneo (+5 XP) |

---
"""


s6 = []

# ─── Apertura ─────────────────────────────────────────────────────────
s6.append(md("nb6-titulo", """\
# Misión 4: El Cartógrafo de Patrones
### Semana 7 -- K-Means Clustering

**Dónde quedamos:** en la Misión 3 construiste un oráculo que, a partir de
lo que ya sabes, predice un número que no sabes -- **cuánto** va a valer
algo. Pero hay preguntas que no son "¿cuánto?". Son "¿qué tipo?" -- sin que
nadie te haya dicho de antemano cuáles son los tipos.

Hoy construyes esa otra herramienta: un mapa que agrupa datos parecidos
entre sí, sin que tú (ni el algoritmo) sepan de antemano qué grupos
existen. En este curso vas a ser su **cartógrafo**.
"""))
s6.append(md("nb6-leyenda", LEYENDA_ICONOS))

s6.append(code("nb6-setup", """\
# Carga el autograder y el dataset de esta lección
!wget -q "https://raw.githubusercontent.com/Santa-Maria-de-los-Andes/intro_to_stats/main/course-python-stats/Week%207/autograder_nb6.py"
!wget -q "https://raw.githubusercontent.com/Santa-Maria-de-los-Andes/intro_to_stats/main/course-python-stats/Week%207/spotify_es.csv"
from autograder_nb6 import Autograder
grader = Autograder()

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

df_canciones = pd.read_csv('spotify_es.csv')
df_canciones = df_canciones.dropna(subset=['Artistas', 'Nombre_Cancion']).copy()
df_canciones = df_canciones[df_canciones['Tempo'] > 0].copy()  # unas pocas filas con Tempo=0 son fallos de deteccion, no canciones reales de 0 BPM

print(f"Canciones cargadas: {len(df_canciones)}")"""))

# ─── Visualize before formalizing ───────────────────────────────────────
s6.append(md("nb6-scatter-md", """\
## 👀 Antes de cualquier código: ¿cuántos grupos ves?

Mira el siguiente gráfico. Cada punto es una canción real de Spotify: en
el eje X, qué tan **bailable** es (de 0 a 1); en el eje Y, su **tempo**
(BPM -- beats por minuto, qué tan rápida es). No hay colores ni etiquetas
todavía -- son solo puntos.

**No te preocupes por el código todavía** -- solo mira el gráfico y
piensa: si tuvieras que separar estas canciones en grupos "parecidas entre
sí", ¿cuántos grupos usarías? ¿en qué te fijarías para decidir?
"""))
s6.append(code("nb6-scatter-code", """\
# 👀 OBSERVA -- no cambies nada, solo mira el resultado
plt.figure(figsize=(7, 5))
plt.scatter(df_canciones['Bailabilidad'], df_canciones['Tempo'], alpha=0.15, s=8)
plt.xlabel('Bailabilidad (0 a 1)')
plt.ylabel('Tempo (BPM)')
plt.title(f'{len(df_canciones)} canciones -- sin agrupar todavía')
plt.show()"""))
s6.append(md("nb6-cuantos-grupos-md", """\
🔮 Antes de seguir leyendo: ¿cuántos grupos "parecidos entre sí" crees que
hay en este gráfico? Ejecuta la celda de abajo y escribe tu predicción --
no hay respuesta incorrecta, ni siquiera un algoritmo te va a dar una
única respuesta "correcta".
"""))
s6.append(code("nb6-cuantos-grupos-code", """\
# 🔮 PREDICE -- ejecuta esta celda para escribir tu predicción
grader.check_cuantos_grupos()"""))

# ─── Concepto 1 ──────────────────────────────────────────────────────────
s6.append(md("nb6-concepto1-md", """\
---
## 🧠 Concepto 1 -- ¿Qué hace k-means?

k-means es un algoritmo que agrupa puntos parecidos **sin que nadie le
diga de antemano** qué significa cada grupo. Así es como decide:

1. Coloca **k** "centros" (centroides) en el espacio de tus datos -- al
   azar, para empezar.
2. Cada punto se asigna al centro **más cercano**.
3. Cada centro se recalcula como el **promedio** de los puntos que le
   tocaron.
4. Repite los pasos 2 y 3 hasta que las asignaciones casi no cambian.

Fíjate en lo que **nunca** usa: ninguna etiqueta real (como el género de
una canción). Solo usa la posición de los puntos. Tú le dices cuántos
grupos quieres (k) -- el algoritmo decide cuáles son.
"""))
s6.append(code("nb6-como-agrupa-code", """\
# 📝 ANOTA -- ejecuta esta celda para escribir tu idea
grader.check_como_agrupa()"""))

# ─── Guided demo: raw (unscaled) ────────────────────────────────────────
s6.append(md("nb6-guiado-raw-md", """\
---
## ✨ Ejemplo guiado -- tu primer mapa (sin escalar)

Vas a pedirle a k-means que agrupe las canciones en k=3 grupos, usando
`Bailabilidad` y `Tempo` -- las mismas dos columnas del scatter de arriba.
Todavía no te preocupes por nada más: solo mira qué hace.
"""))
s6.append(code("nb6-guiado-raw-code", """\
# 👀 OBSERVA -- k-means sobre los datos SIN escalar
X_demo = df_canciones[['Bailabilidad', 'Tempo']]

modelo_demo_raw = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X_demo)
df_canciones['cluster_demo_raw'] = modelo_demo_raw.labels_

plt.figure(figsize=(7, 5))
plt.scatter(df_canciones['Bailabilidad'], df_canciones['Tempo'],
            c=df_canciones['cluster_demo_raw'], cmap='viridis', alpha=0.2, s=8)
plt.xlabel('Bailabilidad (0 a 1)')
plt.ylabel('Tempo (BPM)')
plt.title('k=3, SIN escalar -- ¿qué separó realmente a estos grupos?')
plt.show()

print(df_canciones.groupby('cluster_demo_raw')[['Bailabilidad', 'Tempo']].mean())"""))

# ─── Reveal: real ranges ─────────────────────────────────────────────────
s6.append(md("nb6-reveal-md", """\
Fíjate en la tabla de arriba: entre los tres grupos, `Tempo` cambia
muchísimo (de ≈91 a ≈167 BPM) mientras que `Bailabilidad` casi no se mueve
(de ≈0.50 a ≈0.61) -- los colores del gráfico probablemente forman
**bandas horizontales**, separadas casi solo por `Tempo`. Antes de
explicar por qué, mira los rangos reales de cada columna.
"""))
s6.append(code("nb6-reveal-code", """\
# 👀 OBSERVA -- los rangos reales de cada columna
print("Rango real de Bailabilidad:", df_canciones['Bailabilidad'].min(), "a", df_canciones['Bailabilidad'].max())
print("Rango real de Tempo:       ", df_canciones['Tempo'].min(), "a", df_canciones['Tempo'].max())
print()
print("Promedio de Bailabilidad:", round(df_canciones['Bailabilidad'].mean(), 3))
print("Promedio de Tempo:       ", round(df_canciones['Tempo'].mean(), 1))"""))

# ─── Concepto 2 ──────────────────────────────────────────────────────────
s6.append(md("nb6-concepto2-md", """\
---
## 🧠 Concepto 2 -- Por qué escalar es un no-negociable

`Bailabilidad` vive en el rango 0 a 1. `Tempo` vive en el rango de las
decenas a los cientos (≈30-243 BPM, promedio ≈122). k-means mide qué tan
"cerca" está un punto de otro con **distancia** -- y una diferencia de 50
BPM ya vale 50, mientras que la diferencia **máxima posible** de
Bailabilidad es 1.

Eso significa que, sin hacer nada especial, `Tempo` domina casi por
completo la distancia -- y k-means termina agrupando casi solo por
`Tempo`, dejando que `Bailabilidad` apenas influya. Esto no es un detalle
menor: **es el error más común al usar k-means**, y la solución es
sencilla -- escalar cada columna antes de ajustar, con `StandardScaler`
(resta el promedio y divide entre la desviación estándar, dejando cada
columna con promedio 0 y desviación 1).
"""))

# ─── Guided demo: scaled ─────────────────────────────────────────────────
s6.append(md("nb6-guiado-scaled-md", """\
### Repite el ejemplo, esta vez escalando primero
"""))
s6.append(code("nb6-guiado-scaled-code", """\
# 👀 OBSERVA -- las mismas dos columnas, esta vez escaladas antes de ajustar
X_escalado_demo = StandardScaler().fit_transform(X_demo)

modelo_demo_escalado = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X_escalado_demo)
df_canciones['cluster_demo_escalado'] = modelo_demo_escalado.labels_

plt.figure(figsize=(7, 5))
plt.scatter(df_canciones['Bailabilidad'], df_canciones['Tempo'],
            c=df_canciones['cluster_demo_escalado'], cmap='viridis', alpha=0.2, s=8)
plt.xlabel('Bailabilidad (0 a 1)')
plt.ylabel('Tempo (BPM)')
plt.title('k=3, escalado -- ahora Bailabilidad sí influye')
plt.show()

print(df_canciones.groupby('cluster_demo_escalado')[['Bailabilidad', 'Tempo']].agg(['mean', 'count']))"""))

# ─── Concepto 3 ──────────────────────────────────────────────────────────
s6.append(md("nb6-concepto3-md", """\
---
## 🧠 Concepto 3 -- Las etiquetas de cluster son arbitrarias hasta que TÚ las interpretas

Fíjate en la tabla de arriba: ahora los tres clusters tienen tamaños
comparables, y se distinguen tanto por `Bailabilidad` **como** por
`Tempo` -- uno agrupa canciones muy bailables de tempo medio, otro
canciones poco bailables y rápidas, otro canciones poco bailables y
lentas. Pero el **número** que le tocó a cada cluster (0, 1 o 2) es
completamente arbitrario: si vuelves a ejecutar k-means en otra
computadora, esos mismos grupos de canciones pueden terminar con otros
números.

Lo único con significado real son los puntos que quedaron agrupados y sus
centroides -- **nunca el índice**. Interpretar un cluster significa
describir qué tienen en común sus puntos, en tus propias palabras y con
tus propios números -- no inventarle un nombre "oficial".

Una pregunta natural: si agrupas canciones por bailabilidad y tempo... ¿los
clusters terminan siendo, básicamente, los géneros de la canción (Pop,
Rock, Reggaetón...)? Este dataset tiene **114 géneros reales** distintos
-- vamos a comprobarlo con datos.
"""))

# ─── Guided crosstab: cluster × Género ──────────────────────────────────
s6.append(md("nb6-cluster-genero-setup-md", """\
### Comprueba: ¿los clusters se parecen a los géneros reales?

`spotify_es.csv` sí tiene una columna `Genero` con el género real de cada
canción (114 géneros distintos: Pop, Rock, Reggaetón, K-Pop, Jazz...) --
pero nunca se la diste a k-means como predictor. Si el género no tuviera
ninguna relación con `Bailabilidad`/`Tempo`, cada género representaría
apenas ≈1/114 ≈ 0.9% de cualquier cluster al azar. Compara eso con lo que
realmente aparece.
"""))
s6.append(code("nb6-cluster-genero-setup-code", """\
# 👀 OBSERVA -- el género MÁS COMÚN dentro de cada cluster, como % de ese cluster
for c in sorted(df_canciones['cluster_demo_escalado'].unique()):
    sub = df_canciones[df_canciones['cluster_demo_escalado'] == c]
    top_genero = sub['Genero'].value_counts(normalize=True).head(1)
    print(f"Cluster {c} (n={len(sub)}): género más común = {top_genero.index[0]} "
          f"({top_genero.iloc[0] * 100:.1f}% de este cluster)")"""))

s6.append(md("nb6-cluster-genero-ex-md", """\
#### 🧩 Completa -- ¿los clusters SON géneros reales? (5 pts)

Mira los porcentajes que imprimiste arriba (todos rondan apenas el 2-3%,
con 114 géneros posibles). Completa:
- `respuesta_cluster_es_genero`: escribe `"si"` o `"no"`
- `explicacion_cluster_es_genero`: en 1 frase, cita uno de los números de
  arriba para justificar tu respuesta
"""))
s6.append(code("nb6-cluster-genero-ex-code", """\
# 🧩 COMPLETA

respuesta_cluster_es_genero = "___"
explicacion_cluster_es_genero = "___"

print(f"Respuesta: {respuesta_cluster_es_genero}")"""))
s6.append(code("nb6-cluster-genero-check", "grader.check_cluster_es_genero()"))

# ─── Muestra: ¿qué cambia si agregas una tercera variable? ─────────────
s6.append(md("nb6-demo-energia-md", """\
---
## ✨ Muestra -- ¿qué cambia si agregas una tercera variable?

Antes de trazar tu propio mapa, mira qué pasa si al modelo de arriba
(`Bailabilidad` + `Tempo`, escalado, k=3) le agregas `Energia` -- la
tercera columna del menú que vas a usar en el Ejercicio 1.
"""))
s6.append(code("nb6-demo-energia-code", """\
# 👀 OBSERVA -- mismo k=3, esta vez con Bailabilidad + Tempo + Energia
X_demo3 = df_canciones[['Bailabilidad', 'Tempo', 'Energia']]
X_demo3_escalado = StandardScaler().fit_transform(X_demo3)

modelo_demo3 = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X_demo3_escalado)
df_canciones['cluster_demo3'] = modelo_demo3.labels_

print(df_canciones.groupby('cluster_demo3')[['Bailabilidad', 'Tempo', 'Energia']].agg(['mean', 'count']))"""))
s6.append(md("nb6-demo-energia-debrief-md", """\
#### 🔍 Un patrón que quizás no esperabas

Agregar `Energia` sí cambia el agrupamiento de forma notoria -- ni total,
ni trivial (Adjusted Rand Index ≈0.53 frente al mapa de solo 2 variables).
`Energia` está débilmente correlacionada con `Bailabilidad` y `Tempo`
(r≈0.13 y r≈0.24), así que aporta información genuinamente nueva: el mapa
se redibuja en parte en vez de quedar casi igual. Tenlo en mente al elegir
tus predictores para el Ejercicio 1."""))

# ─── Ejercicio 1 (predictores propios, 2 o 3 del menú) ──────────────────
s6.append(md("nb6-ex1-md", """\
---
#### ✅ Ejercicio 1 -- Traza tu mapa (40 pts)

🔨 Elige **2 o 3** predictores de este menú: `Bailabilidad`, `Tempo`,
`Energia` (puedes incluir `Energia`, como en la muestra de arriba, o
quedarte con las 2 del ejemplo guiado).

Pasos:
1. Guarda tu elección en `predictores_ex1` (lista de 2 o 3 nombres)
2. Escala esas columnas con `StandardScaler`
3. Ajusta `KMeans(n_clusters=3, random_state=42)` sobre los datos
   **escalados** -- guarda el modelo en `modelo_ex1`
4. Elige un cluster para interpretar y guarda su número (0, 1 o 2) en
   `cluster_interes_ex1`
5. Escribe 1-2 oraciones interpretando el centroide de ese cluster en
   `interpretacion_ex1` -- describe el grupo con tus propias variables/
   números, sin afirmar que ES un género real (como practicaste arriba)

Variables que espera el autograder: `predictores_ex1` (lista de 2 o 3),
`modelo_ex1` (KMeans ya ajustado), `cluster_interes_ex1` (entero),
`interpretacion_ex1` (string).
"""))
s6.append(code("nb6-ex1-code", """\
# 🔨 CONSTRUYE

# ============================
#      Tu código aquí
# ============================


print(f"Predictores: {predictores_ex1}")
print(f"Centroide del cluster {cluster_interes_ex1}: {modelo_ex1.cluster_centers_[cluster_interes_ex1]}")"""))
s6.append(code("nb6-ex1-check", "grader.check_ex1()"))

s6.append(code("nb6-checkpoint-a", """\
# ✅ CHECKPOINT -- necesitas 80% en esta sección para continuar
grader.check_mini_a()"""))

s6.append(md("nb6-ex1-reflexiona-md", """\
#### 💭 Reflexiona (respuesta abierta -- calificada por IA, +5 XP)

Arriba viste qué pasó al agregar `Energia` a `Bailabilidad`+`Tempo` (un
cambio moderado, ni total ni trivial). Compara eso con tu propio
Ejercicio 1.
"""))
s6.append(reflexion_check("nb6-ex1-reflexiona-code", "ex2"))

# ─── Concepto 4 -- por qué importa que un agrupamiento generalice ───────
s6.append(md("nb6-concepto4-md", """\
---
## 🧠 Concepto 4 -- ¿Por qué importa que un agrupamiento generalice?

k-means no tiene una "respuesta correcta" que pueda fallar -- no hay un
Puntaje real (como en la Misión 3) contra el cual medir un error. Pero eso
no significa que la calidad de tu mapa no se pueda poner a prueba.

Imagina dos usos reales de estos clusters:

- **Recomendación**: cuando termina una canción, Spotify recomienda otra
  del mismo cluster ("canciones parecidas a esta"). Si mañana sube una
  canción nueva -- que tu modelo *nunca vio* -- y la asignas a un cluster
  con `.predict()`, ¿sus compañeras de cluster de verdad se le parecen?
- **Segmentación**: una discográfica quiere usar tus clusters para decidir
  presupuesto de marketing por "tipo de canción". Si vuelves a ajustar el
  modelo con otra muestra de canciones y los grupos se ven completamente
  distintos, esa segmentación no sirve para tomar una decisión real.

En ambos casos la pregunta es la misma que la Misión 3 te enseñó a hacer
con regresión: **¿el patrón que encontraste se sostiene en datos que el
modelo nunca vio, o fue solo un accidente de la muestra que usaste para
ajustar?** La forma de comprobarlo es la misma herramienta de siempre --
train/test -- aplicada a un algoritmo que nunca tuvo una "respuesta
correcta" para empezar.
"""))

s6.append(md("nb6-guiado-generaliza-md", """\
### Repite el ejemplo, esta vez separando entrenamiento y prueba

Vas a repetir el ejemplo guiado de siempre (`Bailabilidad` + `Tempo`,
escalado, k=3) -- pero esta vez ajustas k-means **solo** con el 90% de
entrenamiento, y usas `.predict()` (nunca `.fit()` de nuevo) para asignarle
un cluster a las canciones de prueba, que el modelo nunca vio al ajustar.
"""))
s6.append(code("nb6-guiado-generaliza-code", """\
# 👀 OBSERVA -- separa train/test, escala SOLO con train, ajusta SOLO con train
from sklearn.model_selection import train_test_split

train_demo, test_demo = train_test_split(df_canciones, test_size=0.1, random_state=42)

escalador_demo = StandardScaler().fit(train_demo[['Bailabilidad', 'Tempo']])
X_train_demo = escalador_demo.transform(train_demo[['Bailabilidad', 'Tempo']])
X_test_demo  = escalador_demo.transform(test_demo[['Bailabilidad', 'Tempo']])

modelo_demo_generaliza = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X_train_demo)

train_demo = train_demo.copy()
test_demo  = test_demo.copy()
train_demo['cluster'] = modelo_demo_generaliza.labels_
test_demo['cluster']  = modelo_demo_generaliza.predict(X_test_demo)

print("Perfil por cluster -- ENTRENAMIENTO (90%, lo que el modelo vio al ajustar):")
print(train_demo.groupby('cluster')[['Bailabilidad', 'Tempo']].agg(['mean', 'count']))
print()
print("Perfil por cluster -- PRUEBA (10%, canciones que el modelo NUNCA vio):")
print(test_demo.groupby('cluster')[['Bailabilidad', 'Tempo']].agg(['mean', 'count']))"""))

s6.append(md("nb6-guiado-generaliza-reveal-md", """\
Fíjate: los promedios de `Bailabilidad`/`Tempo` por cluster son casi
idénticos entre entrenamiento y prueba (y las proporciones de tamaño
también se parecen). Eso es lo que significa que un agrupamiento
**generalice**: la estructura que encontraste no es un accidente de qué
canciones cayeron en tu muestra de ajuste -- se sostiene en canciones que
el modelo nunca vio. Si los perfiles fueran muy distintos entre train y
test, cualquier recomendación o segmentación basada en ese mapa sería poco
confiable.
"""))

# ─── Reflexión -- generalización (sin ejercicio propio, el ejemplo guiado
# de arriba ya recorrió el flujo completo train/test) ────────────────────
s6.append(md("nb6-generaliza-reflexiona-md", """\
#### 💭 Reflexiona (respuesta abierta -- calificada por IA, +5 XP)

Piensa en los dos usos reales del Concepto 4: **recomendación** (sugerir
la próxima canción del mismo cluster) y **segmentación** (decidir
presupuesto de marketing por "tipo de canción"). En el ejemplo guiado de
arriba viste que los perfiles de cluster casi no cambian entre
entrenamiento y prueba.
"""))
s6.append(reflexion_check("nb6-generaliza-reflexiona-code", "generalizacion"))

# ─── Knowledge checks ───────────────────────────────────────────────────
s6.append(md("nb6-teoria-md", """\
---
## ❓ Quiz de cierre -- 5 preguntas de teoría (25 pts)

Antes de la reflexión final, confirma que las ideas clave quedaron claras.
"""))
s6.append(teoria_check("nb6-t1-check", 1))
s6.append(teoria_check("nb6-t2-check", 2))
s6.append(teoria_check("nb6-t3-check", 3))
s6.append(teoria_check("nb6-t4-check", 4))
s6.append(teoria_check("nb6-t5-check", 5))

# ─── Reflexión final ────────────────────────────────────────────────────
s6.append(md("nb6-reflexion-final-md", """\
---
## 🪞 Reflexión final (respuesta abierta -- calificada por IA, +5 XP)

Ya usaste k-means para agrupar canciones por variables numéricas, sin
decirle al algoritmo nada sobre el género real de cada canción.
"""))
s6.append(reflexion_check("nb6-reflexion-final-code", "final"))

s6.append(code("nb6-checkpoint-b", """\
# ✅ CHECKPOINT -- necesitas 80% en esta sección para continuar
grader.check_mini_b()"""))

# ─── Reto 1 (bonus) ─────────────────────────────────────────────────────
s6.append(md("nb6-reto1-md", """\
---
#### 🎯 Reto (bonus, +10 XP) -- Cambia el número de regiones

Elige un valor de k **distinto de 3** (por ejemplo, 2, 4 o 5) y vuelve a
ajustar k-means -- reusa los mismos predictores escalados de tu Ejercicio
1. Guarda tu elección en `k_reto1`, el modelo en `modelo_reto1`, y en
una frase describe qué cambió en `comentario_reto1` (¿algún grupo se
dividió? ¿se fusionaron dos?).
"""))
s6.append(code("nb6-reto1-code", """\
# 🔨 CONSTRUYE (bonus)

# ============================
#      Tu código aquí
# ============================


print(f"k_reto1 = {k_reto1}")
print(f"Comentario: {comentario_reto1}")"""))
s6.append(code("nb6-reto1-check", "grader.check_reto1()"))

# ─── Cierre ──────────────────────────────────────────────────────────────
s6.append(md("nb6-cierre", """\
---
## 🏁 Fin de la Misión 4 -- Semana 7

Construiste dos mapas de clusters sobre el mismo dataset de canciones de
Spotify: uno sin escalar (dominado por una sola variable) y otro escalado
(donde todas las variables pesan). Aprendiste que k-means no usa ninguna
etiqueta real -- agrupa por posición, no por significado -- y que
interpretar un cluster es tu trabajo, no algo que el algoritmo hace por
ti.

La próxima vez que alguien te diga "el algoritmo encontró 3 tipos de
clientes/canciones/lo-que-sea", ya sabes qué preguntar: ¿escalaron las
variables antes de agrupar? ¿qué tan estable es ese número de grupos?
¿esos "tipos" describen algo real, o son solo un número que el algoritmo
les puso?
"""))
s6.append(code("nb6-resumen", "grader.resumen()"))


# ═══════════════════════════════════════════════════════════════════════
# ESCRIBIR NOTEBOOK
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


write_notebook(s6, "nb6_clustering.ipynb")

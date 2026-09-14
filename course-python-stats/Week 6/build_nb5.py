# -*- coding: utf-8 -*-
"""
build_nb5.py -- Genera nb5_regresion.ipynb (Semana 6, "Misión 3: El Oráculo
de Datos" -- regresión lineal). Primer notebook de esta misión: sin
predecesor nb-algo que continuar, así que check_ex/check_t/check_reto
empiezan frescos en 1 (WORKFORCE_CONTRACT.md §2 -- la numeración global solo
aplica *dentro* de una misión multi-notebook, como nb1_semana1->nb1_semana2
o nb3->nb4; ésta es la primera y única sesión de Semana 6, "one notebook,
one session" por pedido explícito del usuario).

Sigue el mismo patrón que build_nb3.py/build_nb4.py: helpers `md`/`code`/
`teoria_check`/`reflexion_check`/`LEYENDA_ICONOS` duplicados aquí a propósito
-- cada build_nbN.py es autocontenido, no importa de otro build script
(COURSE_TEMPLATE.md §3).

Dos datasets:
  - 2019_es.csv (World Happiness Report, ya usado en nb3/nb4) -- solo para
    el ejemplo guiado, que sigue el hilo narrativo directo desde nb4
    (PBI↔Puntaje, r≈0.794). No autograded.
  - athlete_events_es.csv (120 Years of Olympic History, ya usado en
    nb1_semana2) -- para los Ejercicios 1-2 y el reto bonus, prediciendo
    Altura.

Decisión de alcance heredada de autograder_nb5.py (ver su docstring para el
detalle completo): el menú de predictores para Altura se recortó de
{Edad, Peso, Sexo, Deporte} a {Edad, Peso, Sexo_num} -- Deporte tiene 66
categorías y codificarlo (one-hot) está fuera del temario comprometido
(WORKFORCE_CONTRACT.md §5). Sexo se convierte a Sexo_num (0/1) en una celda
guiada antes del Ejercicio 1; el notebook explica brevemente por qué
Deporte queda fuera, en vez de omitirlo en silencio.

Todo el código de los ejemplos guiados fue verificado ejecutándolo contra
los CSV reales (ver ATLAS validation en _test_nb5.py, mismo folder) antes
de congelar este build script.
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


s5 = []

# ─── Apertura ─────────────────────────────────────────────────────────
s5.append(md("nb5-titulo", """\
# Misión 3: El Oráculo de Datos
### Semana 6 -- Regresión Lineal

**Dónde quedamos:** en la Misión 2 encontraste que el PBI per cápita de un
país y su Puntaje de felicidad tienen una correlación fuerte (r ≈ 0.794).
Eso te dice que **se mueven juntos**. Pero no te dice **cuánto** -- si te
doy el PBI de un país que nunca viste, ¿puedes decirme su Puntaje
aproximado?

Hoy construyes esa herramienta: un modelo que, a partir de lo que sí sabes,
predice lo que no sabes. En este curso lo vas a llamar tu **oráculo**.
"""))
s5.append(md("nb5-leyenda", LEYENDA_ICONOS))

s5.append(code("nb5-setup", """\
# Carga el autograder y los datasets de esta lección
!wget -q "https://raw.githubusercontent.com/Santa-Maria-de-los-Andes/intro_to_stats/main/course-python-stats/Week%206/autograder_nb5.py"
!wget -q "https://raw.githubusercontent.com/Santa-Maria-de-los-Andes/intro_to_stats/main/course-python-stats/Weeks%203-4/2019_es.csv"
!wget -q "https://raw.githubusercontent.com/Santa-Maria-de-los-Andes/intro_to_stats/main/course-python-stats/Weeks%201-2/athlete_events_es.csv"
from autograder_nb5 import Autograder
grader = Autograder()

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

df_felicidad = pd.read_csv('2019_es.csv')

print("Datasets cargados.")"""))

# ─── Visual concept (no code focus yet) ────────────────────────────────
s5.append(md("nb5-visual-md", """\
## 👀 Antes de cualquier código: ¿qué está haciendo esta línea?

Mira el siguiente gráfico. Es el mismo par de variables que ya conoces: PBI
per cápita (eje X) y Puntaje de felicidad (eje Y). Pero esta vez, además de
los puntos, hay una línea recta atravesándolos.

**No te preocupes por el código todavía** -- solo mira el gráfico y piensa:
¿qué está haciendo esa línea? ¿Para qué te serviría?
"""))
s5.append(code("nb5-visual-code", """\
# 👀 OBSERVA -- no cambies nada, solo mira el resultado
modelo_demo = LinearRegression().fit(df_felicidad[['PBI per cápita']], df_felicidad['Puntaje'])

plt.figure(figsize=(7, 5))
plt.scatter(df_felicidad['PBI per cápita'], df_felicidad['Puntaje'], alpha=0.6, label='Países reales')
x_linea = df_felicidad[['PBI per cápita']].sort_values('PBI per cápita')
plt.plot(x_linea, modelo_demo.predict(x_linea), color='red', linewidth=2, label='¿...?')
plt.xlabel('PBI per cápita')
plt.ylabel('Puntaje de felicidad')
plt.legend()
plt.show()"""))
s5.append(md("nb5-visual-pregunta-md", """\
🔮 En una frase, antes de seguir leyendo: ¿qué crees que hace esa línea
roja? Ejecuta la celda de abajo y escribe tu predicción -- la vas a
confirmar en la siguiente sección.
"""))
s5.append(code("nb5-visual-predice-code", """\
# 🔮 PREDICE -- ejecuta esta celda para escribir tu predicción
grader.check_prediccion_linea()"""))

# ─── Conceptos ──────────────────────────────────────────────────────────
s5.append(md("nb5-concepto-linea-md", """\
---
## 🧠 Concepto 1 -- La línea que "mejor le queda" a los puntos

Esa línea roja es una **línea de mejor ajuste** (best-fit line). No pasa
exactamente por cada punto -- eso sería imposible con datos reales. En
cambio, es la línea que, sumando qué tan lejos queda de *todos* los puntos
a la vez, queda **lo más cerca posible en promedio**.

Eso es literalmente lo que hace `LinearRegression().fit()`: encuentra
(matemáticamente, no por ensayo y error) la línea que minimiza esa
distancia total.
"""))
s5.append(code("nb5-concepto-linea-pausa-code", """\
# 📝 ANOTA -- ejecuta esta celda para escribir tu idea
grader.check_anota_distancia()"""))
s5.append(code("nb5-concepto-r2-visual-code", """\
# 👀 OBSERVA -- tres modelos con distinto R², para "ver" lo que significa el número
import numpy as np
rng = np.random.RandomState(7)
x = np.linspace(0, 10, 40).reshape(-1, 1)
ruido = rng.normal(0, 1, size=len(x))

y_alto  = 2 * x.flatten() + 1 + ruido * 0.4
y_medio = 2 * x.flatten() + 1 + ruido * 5.2
y_bajo  = rng.normal(5, 2, size=len(x))

fig, axes = plt.subplots(1, 3, figsize=(13, 4))
for ax, y in zip(axes, [y_alto, y_medio, y_bajo]):
    modelo_demo_r2 = LinearRegression().fit(x, y)
    r2 = modelo_demo_r2.score(x, y)
    ax.scatter(x, y, alpha=0.6)
    ax.plot(x, modelo_demo_r2.predict(x), color='red', linewidth=2)
    ax.set_title(f'R² = {r2:.2f}')
plt.tight_layout()
plt.show()"""))
s5.append(md("nb5-concepto-r2-md", """\
## 🧠 Concepto 2 -- R²: ¿qué tan bien explica la línea a los puntos?

`r` (Misión 2) te decía qué tan fuerte era una relación, de -1 a 1. **R²**
(así, al cuadrado) es distinto: te dice **qué porcentaje de la variación**
del resultado tu modelo logra explicar.

- R² = 1.0 → el modelo explica el 100% de la variación (predicción
  perfecta -- casi nunca pasa con datos reales)
- R² = 0.72 → el modelo explica el 72% de la variación -- el otro 28%
  depende de cosas que el modelo no ve
- R² = 0.0 → el modelo no explica nada más que "usar siempre el promedio"

En scikit-learn, `.score()` te da el R² directamente.
"""))
s5.append(code("nb5-concepto-r2-barra-code", """\
# 👀 OBSERVA -- el mismo R² de arriba, visto como % explicado vs. % sin explicar
valores_r2 = [1.0, 0.72, 0.0]

fig, ax = plt.subplots(figsize=(7, 3))
for i, r2 in enumerate(valores_r2):
    ax.barh(i, r2 * 100, color='#5dd9ff', label='Explicado' if i == 0 else None)
    ax.barh(i, (1 - r2) * 100, left=r2 * 100, color='#3a3555', label='Sin explicar' if i == 0 else None)
    ax.text(102, i, f'R² = {r2:.2f}', va='center', fontsize=10)

ax.set_yticks(range(len(valores_r2)))
ax.set_yticklabels([])
ax.set_xlim(0, 130)
ax.set_xlabel('% de la variación del resultado')
ax.legend(loc='lower right')
plt.tight_layout()
plt.show()"""))
s5.append(md("nb5-concepto-traintest-md", """\
## 🧠 Concepto 3 -- Por qué separas "entrenamiento" y "prueba"

Si ajustas tu modelo con **todos** los países y luego mides qué tan bien
predice esos **mismos** países, estás haciendo trampa: es como corregir un
examen con las respuestas que el estudiante ya vio.

Por eso separas los datos en dos partes **antes** de entrenar:

- **Train** (entrenamiento, ~90%): el modelo aprende de estos datos
- **Test** (prueba, ~10%): datos que el modelo **nunca vio** -- aquí mides
  si de verdad aprendió un patrón, o si solo memorizó

`train_test_split()` hace esa división por ti. El **R² de prueba** es el
que de verdad importa: te dice si el modelo generaliza a países nuevos, no
solo si memorizó los que ya conocía.
"""))
s5.append(code("nb5-concepto-traintest-visual-code", """\
# 👀 OBSERVA -- así se ve una división train/test real, sobre datos sintéticos
rng3 = np.random.RandomState(3)
n_split = 100
x_split = rng3.uniform(0, 10, n_split)
y_split = 2 * x_split + 1 + rng3.normal(0, 2, n_split)

idx = rng3.permutation(n_split)
test_idx, train_idx = idx[:10], idx[10:]

plt.figure(figsize=(7, 5))
plt.scatter(x_split[train_idx], y_split[train_idx], alpha=0.7, color='#5dd9ff',
            label=f'Train ({len(train_idx)} puntos)')
plt.scatter(x_split[test_idx], y_split[test_idx], alpha=0.9, color='#ffd166', marker='s',
            label=f'Test ({len(test_idx)} puntos)')
plt.title('Mismos datos, divididos una sola vez -- 90% train / 10% test')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.show()"""))

# ─── Guided example (World Happiness) ──────────────────────────────────
s5.append(md("nb5-guiado-md", """\
---
## ✨ Ejemplo guiado -- construye tu primer oráculo (Felicidad)

Vas a repetir, paso a paso, lo que acabas de leer: separar train/test,
ajustar el modelo con **las seis variables** que ya conoces (PBI, Apoyo
social, Esperanza de vida, Libertad, Generosidad, Percepción de
corrupción), y medir qué tan bien predice. Cada paso es su propia celda --
léelo antes de ejecutarlo.
"""))

s5.append(md("nb5-guiado-paso1-md", """\
### Paso 1 -- Elige tus predictores y tu variable objetivo

Usarás las seis variables de siempre como **predictores** (lo que usas para
predecir) y `Puntaje` como tu **variable objetivo** (lo que quieres
predecir).
"""))
s5.append(code("nb5-guiado-paso1-code", """\
# 👀 OBSERVA
predictores_felicidad = ['PBI per cápita', 'Apoyo social', 'Esperanza de vida saludable',
                          'Libertad para tomar decisiones', 'Generosidad', 'Percepción de corrupción']

X_felicidad = df_felicidad[predictores_felicidad]
y_felicidad = df_felicidad['Puntaje']

print(f"Predictores: {X_felicidad.shape[1]} columnas, {X_felicidad.shape[0]} países")"""))

s5.append(md("nb5-guiado-paso2-md", """\
### Paso 2 -- Separa entrenamiento y prueba

Tal como viste en el Concepto 3: separas 90% de los países para entrenar y
10% para probar, **antes** de tocar el modelo. `random_state=42` solo fija
la "semilla" de esa separación aleatoria, para que el resultado sea el
mismo cada vez que ejecutes la celda (y para que tu resultado sea
comparable con el de un compañero).
"""))
s5.append(code("nb5-guiado-paso2-code", """\
# 👀 OBSERVA
X_train_fel, X_test_fel, y_train_fel, y_test_fel = train_test_split(
    X_felicidad, y_felicidad, test_size=0.1, random_state=42)

print(f"Entrenamiento: {len(X_train_fel)} países")
print(f"Prueba:        {len(X_test_fel)} países (el modelo nunca los ve al entrenar)")"""))

s5.append(md("nb5-guiado-paso3-md", """\
### Paso 3 -- Ajusta el modelo

`LinearRegression().fit()` es el paso que de verdad "aprende": encuentra la
línea -- en este caso, con 6 variables, algo como un "plano" de 6
dimensiones, pero la idea es la misma -- que mejor le queda a los datos de
**entrenamiento** únicamente.
"""))
s5.append(code("nb5-guiado-paso3-code", """\
# 👀 OBSERVA
modelo_felicidad = LinearRegression().fit(X_train_fel, y_train_fel)
print("Modelo entrenado con", len(X_train_fel), "países.")"""))

s5.append(md("nb5-guiado-paso4-md", """\
### Paso 4 -- R² en entrenamiento

`.score()` te da el R² directamente. Este es el R² sobre los mismos datos
que el modelo usó para aprender -- todavía no sabes si de verdad
generalizó a países que no vio.
"""))
s5.append(code("nb5-guiado-paso4-code", """\
# 👀 OBSERVA
train_r2_felicidad = modelo_felicidad.score(X_train_fel, y_train_fel)
print(f"R² en entrenamiento: {train_r2_felicidad:.3f}")"""))

s5.append(md("nb5-guiado-paso5-md", """\
### Paso 5 -- R² en prueba (el que de verdad importa)

Ahora mide el R² sobre los países que el modelo **nunca vio**. Si este
número es parecido al de entrenamiento, el modelo generalizó bien. Si es
mucho más bajo, el modelo memorizó en vez de aprender un patrón real.
"""))
s5.append(code("nb5-guiado-paso5-code", """\
# 👀 OBSERVA
test_r2_felicidad = r2_score(y_test_fel, modelo_felicidad.predict(X_test_fel))
print(f"R² en prueba: {test_r2_felicidad:.3f}")"""))

s5.append(md("nb5-guiado-paso6-md", """\
### Paso 6 -- Mira los coeficientes

Cada coeficiente te dice cuánto sube el Puntaje predicho por cada unidad
que sube esa variable, manteniendo las demás fijas.
"""))
s5.append(code("nb5-guiado-paso6-code", """\
# 👀 OBSERVA
for nombre, coef in zip(predictores_felicidad, modelo_felicidad.coef_):
    print(f"  coeficiente de {nombre}: {coef:.3f}")"""))

s5.append(md("nb5-guiado-interpretacion-md", """\
Fíjate en los coeficientes: cada uno te dice cuánto **sube** el Puntaje
predicho por cada unidad que sube esa variable, **manteniendo las demás
fijas**. Un coeficiente más grande no significa automáticamente "más
importante" (las variables tienen escalas distintas) -- pero sí te dice
cómo el modelo está usando esa variable.

#### 💭 Reflexiona (respuesta abierta -- calificada por IA, +5 XP)
"""))
s5.append(reflexion_check("nb5-guiado-interpretacion-code", "interpretacion"))

# ─── Watch me break it ──────────────────────────────────────────────────
s5.append(md("nb5-rompe-md", """\
---
## 💥 Míralo romperse

Tu modelo tiene un R² de prueba decente. Pero, ¿qué pasa si le das un valor
de PBI per cápita **absurdamente** fuera de lo que vio al entrenar?
"""))
s5.append(code("nb5-rompe-rango-code", """\
# 👀 OBSERVA -- primero, recuerda los rangos reales de los datos
print("Rango real de PBI per cápita:", df_felicidad['PBI per cápita'].min(), "a", df_felicidad['PBI per cápita'].max())
print("Rango real de Puntaje:       ", df_felicidad['Puntaje'].min(), "a", df_felicidad['Puntaje'].max())"""))
s5.append(md("nb5-rompe-transicion-md", """\
Ahora dale al modelo un PBI per cápita de **10000** -- muy por fuera de lo
que vio al entrenar (deja las demás variables en su promedio, para que el
único cambio sea ese).
"""))
s5.append(code("nb5-rompe-prediccion-code", """\
# 👀 OBSERVA -- el modelo va a "predecir" igual, aunque el valor no tenga sentido
entrada_absurda = pd.DataFrame([{
    'PBI per cápita': 10000,
    'Apoyo social': df_felicidad['Apoyo social'].mean(),
    'Esperanza de vida saludable': df_felicidad['Esperanza de vida saludable'].mean(),
    'Libertad para tomar decisiones': df_felicidad['Libertad para tomar decisiones'].mean(),
    'Generosidad': df_felicidad['Generosidad'].mean(),
    'Percepción de corrupción': df_felicidad['Percepción de corrupción'].mean(),
}])

prediccion_absurda_demo = modelo_felicidad.predict(entrada_absurda)[0]
print(f"Predicción del modelo con PBI=10000: {prediccion_absurda_demo:.1f}")"""))
s5.append(md("nb5-rompe-caption-md", """\
Un Puntaje de miles, cuando el máximo real del planeta es ≈7.8. **El
modelo solo sabe lo que le enseñaste** -- dentro del rango de PBI que vio
(0 a ≈1.7), su línea es útil. Fuera de ese rango, sigue extendiendo la
misma pendiente sin ningún freno real. Eso se llama **extrapolar**, y es
uno de los errores más comunes al usar un modelo de regresión.
"""))

# ─── Olympics setup (guided preprocessing) ─────────────────────────────
s5.append(md("nb5-atletas-setup-md", """\
---
## 🏟️ Ahora, un dataset distinto: atletas olímpicos

Vas a repetir la misma idea -- separar, ajustar, medir -- pero con un
dataset totalmente distinto: 120 años de atletas olímpicos. Esta vez vas a
predecir la **Altura** de un atleta a partir de otras columnas suyas.

Antes de empezar, dos cosas de preparación:

1. **Filtrar filas sin datos**: varias filas no tienen Edad, Altura o Peso
   registrados -- un modelo no puede aprender de un hueco vacío, así que
   las quitamos.
2. **Convertir texto a número**: `LinearRegression` solo entiende números.
   `Sexo` es texto (`'M'`/`'F'`) -- lo convertimos a 0/1. (`Deporte` tiene
   66 categorías distintas; convertir *eso* a números requiere una técnica
   -- **one-hot encoding** -- que está un paso más allá de esta lección,
   así que por ahora lo dejamos fuera del menú de predictores.)
"""))
s5.append(code("nb5-atletas-setup-code", """\
# 👀 OBSERVA -- preparación del dataset, no necesitas escribir esto
df_atletas = pd.read_csv('athlete_events_es.csv')
df_atletas = df_atletas.dropna(subset=['Edad', 'Altura', 'Peso', 'Sexo']).copy()
df_atletas['Sexo_num'] = (df_atletas['Sexo'] == 'M').astype(int)  # 1 = hombre, 0 = mujer

print(f"Filas después de filtrar: {len(df_atletas)}")
df_atletas[['Edad', 'Altura', 'Peso', 'Sexo', 'Sexo_num']].head()"""))

# ─── Ejercicio 1 ────────────────────────────────────────────────────────
s5.append(md("nb5-ex1-md", """\
#### ✅ Ejercicio 1 -- Construye tu primer oráculo (40 pts)

🔨 Predice `Altura` usando **2 o 3** de estos predictores: `Edad`, `Peso`,
`Sexo_num`.

Pasos (los mismos del ejemplo guiado, con tu propia elección de
predictores):

1. Elige tus predictores y guárdalos en una lista: `predictores_ex1`
2. Separa train/test con `test_size=0.1, random_state=42` (mismo
   `random_state` que el ejemplo -- así tu resultado es comparable y
   verificable)
3. Ajusta un `LinearRegression()` sobre `df_atletas`
4. Calcula `train_r2_ex1` y `test_r2_ex1`
5. Escribe 1-2 oraciones interpretando tus coeficientes en
   `interpretacion_ex1` -- sin palabras causales ("causa", "provoca",
   "hace que")

Variables que espera el autograder: `predictores_ex1` (lista),
`train_r2_ex1`, `test_r2_ex1` (números), `interpretacion_ex1` (string).
"""))
s5.append(code("nb5-ex1-code", """\
# 🔨 CONSTRUYE

# ============================
#      Tu código aquí
# ============================


print(f"R² entrenamiento: {train_r2_ex1:.3f}")
print(f"R² prueba:        {test_r2_ex1:.3f}")"""))
s5.append(code("nb5-ex1-check", "grader.check_ex1()"))

s5.append(code("nb5-checkpoint-a", """\
# ✅ CHECKPOINT -- necesitas 80% en esta sección para continuar
grader.check_mini_a()"""))

# ─── Ejercicio 2 ────────────────────────────────────────────────────────
s5.append(md("nb5-ex2-md", """\
---
#### ✅ Ejercicio 2 -- Optimiza tu oráculo (20 pts)

🔨 Ahora explora: prueba **2 o 3 combinaciones distintas** de predictores
(de nuevo, entre `Edad`, `Peso`, `Sexo_num`) y quédate con la que te dio el
**mejor R² de prueba**. Puedes reejecutar esta celda tantas veces como
quieras, cambiando la combinación, antes de decidir cuál es tu mejor
resultado.

Cuando decidas cuál fue tu mejor combinación, guárdala en `combo_ex2`
(lista) y su R² de prueba en `mejor_test_r2_ex2`.
"""))
s5.append(code("nb5-ex2-code", """\
# 🔨 CONSTRUYE -- prueba varias combinaciones, luego reporta la mejor abajo

# ============================
#      Tu código aquí
# ============================


print(f"Mejor combinación: {combo_ex2}")
print(f"Mejor R² de prueba: {mejor_test_r2_ex2:.3f}")"""))
s5.append(code("nb5-ex2-check", "grader.check_ex2()"))

s5.append(md("nb5-ex2-debrief-md", """\
#### 🔍 Un patrón que quizás ya notaste

Si notaste que agregar `Sexo_num` casi no cambia el resultado una vez que
ya tienes `Peso` (0.643 → 0.644), no es casualidad: `Peso` por sí solo ya
captura casi toda la señal que predice `Altura`. `Edad` y `Sexo_num`
aportan muy poco extra."""))

s5.append(md("nb5-ex2-reflexiona-md", """\
#### 💭 Reflexiona (respuesta abierta -- calificada por IA, +5 XP)

De las combinaciones que probaste, ¿cuál dio el mejor R² de prueba? En 1-2
oraciones: ¿por qué crees que esas variables funcionan mejor para predecir
la estatura de un atleta?
"""))
s5.append(reflexion_check("nb5-ex2-reflexiona-code", "ex2"))

# ─── Reto 1 (bonus) ─────────────────────────────────────────────────────
s5.append(md("nb5-reto1-md", """\
---
#### 🎯 Reto (bonus, +10 XP) -- Rompe tu propio oráculo

Usa tu mejor modelo del Ejercicio 2 para predecir `Altura` con una entrada
**deliberadamente absurda** (por ejemplo, `Edad=200`, `Peso=1000`). Guarda
la predicción en `prediccion_absurda_reto1` y, en una frase, describe qué
entrada usaste y por qué la predicción no tiene sentido en
`descripcion_absurda_reto1`.
"""))
s5.append(code("nb5-reto1-code", """\
# 🔨 CONSTRUYE (bonus)

# ============================
#      Tu código aquí
# ============================


print(f"Predicción absurda de Altura: {prediccion_absurda_reto1:.1f} cm")"""))
s5.append(code("nb5-reto1-check", "grader.check_reto1()"))

# ─── Knowledge checks ───────────────────────────────────────────────────
s5.append(md("nb5-teoria-md", """\
---
## ❓ Quiz de cierre -- 5 preguntas de teoría (25 pts)

Antes de la reflexión final, confirma que las ideas clave quedaron claras.
"""))
s5.append(teoria_check("nb5-t1-check", 1))
s5.append(teoria_check("nb5-t2-check", 2))
s5.append(teoria_check("nb5-t3-check", 3))
s5.append(teoria_check("nb5-t4-check", 4))
s5.append(teoria_check("nb5-t5-check", 5))

# ─── Reflexión final ────────────────────────────────────────────────────
s5.append(md("nb5-reflexion-final-md", """\
---
## 🪞 Reflexión final (respuesta abierta -- calificada por IA, +5 XP)

Ya construiste modelos de regresión en dos datasets totalmente distintos
(puntajes de felicidad, estaturas de atletas). En 2-4 oraciones: ¿cuándo
usarías una herramienta así? ¿qué preguntas podrías responder con un
modelo de predicción como este?
"""))
s5.append(reflexion_check("nb5-reflexion-final-code", "final"))

s5.append(code("nb5-checkpoint-b", """\
# ✅ CHECKPOINT -- necesitas 80% en esta sección para continuar
grader.check_mini_b()"""))

# ─── Cierre ──────────────────────────────────────────────────────────────
s5.append(md("nb5-cierre", """\
---
## 🏁 Fin de la Misión 3 -- Semana 6

Construiste dos oráculos de datos: uno que predice bienestar a partir de
indicadores económicos y sociales, y otro que predice la estatura de un
atleta a partir de datos simples. Aprendiste a medir qué tan bueno es un
modelo (R²), por qué el R² de prueba es el que realmente importa, y qué
pasa cuando le pides a un modelo que adivine fuera de lo que aprendió.

La próxima vez que alguien te diga "el modelo predice X a partir de Y", ya
sabes qué preguntar: ¿con qué datos se entrenó? ¿qué tan bien le fue con
datos que nunca vio? ¿el valor que le estás dando está dentro de lo que
aprendió, o lo estás haciendo adivinar?
"""))
s5.append(code("nb5-resumen", "grader.resumen()"))


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


write_notebook(s5, "nb5_regresion.ipynb")

# -*- coding: utf-8 -*-
"""
build_nb3.py -- Genera nb3_semana3_correlacion.ipynb (Semana 3 / Clase 1 de la
Mision 2: Buscando Patrones -- nombre placeholder, pendiente PIXEL ticket #2).

Nombrado "nb3" por decision explicita del usuario 2026-08-14, que SUPERA la
convencion documentada en WORKFORCE_HANDOFF.md / supabase_schema.sql (nb2 =
Tarea 2 = Correlacion, nb3 reservado para Regresion/Clustering Semanas 6-7).
Ver WORKFORCE_HANDOFF.md Done log 2026-08-14 para el registro de esta decision.

Cubre Apertura + Teoria Desbloqueada + Seccion A + Seccion B, segun el reparto
Semana 3 / Semana 4 propuesto en Teoria_Semanas3-4_Mision2_Correlacion.md SS5.
Seccion C + Integracion (Semana 4) quedan para un notebook separado, no
generado por este script.

Fuente de contenido:
  - Teoria_Semanas3-4_Mision2_Correlacion.md (SS0 Apertura, SS1 Teoria
    Desbloqueada, SS2 Seccion A / Seccion B)
  - 2019_es.csv (World Happiness Report 2019, 156 filas x 10 columnas, SIN
    valores nulos) -- todos los numeros de este notebook se calcularon
    directamente contra el CSV real (ver comentarios inline), ninguno es
    estimado ni inventado, mismo criterio que Semanas 1-2.

Numeracion: reinicia en 1 (check_ex1, check_t1, check_debug1...) igual que
nb1_semana1 -- primera clase de una mision nueva, no continuacion de la
numeracion de Mision 1.

Repeticion (agregada 2026-08-14 por pedido del usuario -- "necesitamos mas
repeticion para solidificar los conceptos, con interpretacion abierta justo
despues"): Seccion A y Seccion B ya no trabajan un solo par por seccion --
cada una repite el patron dos veces (Ronda 1: Percepcion de corrupcion,
Ronda 2: Esperanza de vida saludable, ademas del par guiado Apoyo social),
y cada ronda termina en una celda 💭 REFLEXIONA corta e inmediata -- misma
logica de "ejemplo guiado -> ejercicio -> comparar" que nb1_semana2 usa en
sus Secciones C/D.

Convenciones (identicas a build_nb1.py): check_tN = una celda,
grader.check_tN(); check_exN 🔨 CONSTRUYE = sin solucion escrita; check_exN
🧩 COMPLETA = blancos ___; celdas 🔮 PREDICE = ungraded, contract-exempt
(WORKFORCE_CONTRACT.md SS3).

Reflexion calificada por IA (agregado 2026-08-19, pedido explicito del
usuario -- SUPERA la nota "ungraded, contract-exempt" de abajo SOLO para
este notebook en adelante; nb1_semana1/nb1_semana2 NO se tocan, siguen con
revision manual del profesor per WORKFORCE_CONTRACT.md SS3): las 11 celdas
💭 Reflexiona de este notebook ya NO son `variable = "___"` sin autograder --
usan `reflexion_check()` (mismo patron widget-HTML que `teoria_check()`,
ver autograder_nb3_semana3.py `_ask_reflexion`/`_grade_reflexion`), que
manda el texto a DeepSeek via una funcion Edge de Supabase y devuelve
0-5 pts + comentario. Sube `_CORE_MAX` de 209 a 264 (+55, 5 pts x 11
celdas) -- ver nota de presupuesto actualizada mas abajo.

Expansion 2026-08-18 (usuario, tras revisar el notebook generado): dos pedidos
directos. (1) La celda de la "revelacion" de la Apertura (`nb3-apertura-reveal`)
indexaba `pares_apertura[i][0]/[1]` -- confuso e improductivo como ejemplo a
replicar. Reescrita para calcular cada r con una linea directa y nombrada
(`df_felicidad['col_x'].corr(df_felicidad['col_y'])`), el mismo patron que
Seccion B enseña despues, para que sea el primer lugar donde el patron
completo es visible y copiable. (2) Cuatro rondas nuevas despues del
Ejercicio 4 (ahora `check_ex5`-`check_ex8`), mismo patron scatter+`.corr()`
pero esta vez en un solo ejercicio combinado (antes Seccion A/B lo partian en
dos), y con pares que **no** incluyen `Puntaje` -- PBI per capita vs.
Esperanza de vida (r≈0.835, el mas fuerte de todo el dataset), Apoyo social
vs. Esperanza de vida (r≈0.719), Libertad vs. Percepcion de corrupcion
(r≈0.439), PBI per capita vs. Generosidad (r≈-0.080, practicamente nulo).
Objetivo pedagogico: que el estudiante no generalice "las seis variables
tienen todas r≈0.78 porque asi salieron contra Puntaje" -- la fuerza de una
correlacion es especifica del par, no una propiedad de la variable. Cada
ronda añade una pregunta teorica ❓ ANTES (concepto, no el numero exacto --
p.ej. que la correlacion no es transitiva) y otra DESPUES (interpretar el
resultado real que el estudiante acaba de calcular) -- `check_t7`-`check_t14`,
8 preguntas nuevas. El viejo `check_ex5` (explorar todas las correlaciones)
se renumero a `check_ex9` para dejarle el rango 5-8 a las rondas nuevas.
**Nota de presupuesto**: esto sube el `_CORE_MAX` de Semana 3 de 109 a 209
(y despues a 264 con la reflexion calificada por IA, ver arriba), bastante
por encima del ~180 XP asignado a Semanas 3-4 completas en
`WORKFORCE_CONTRACT.md` SS2 -- no se recorto nada para compensar porque el
pedido fue explicito y aditivo. El usuario decidio explicitamente 2026-08-19
no abrir/actualizar un ticket de presupuesto para esto: el score se
normaliza a 0-100% por notebook, asi que el numero crudo de `_CORE_MAX` no
es un costo real cross-notebook.
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
| 💭 | **REFLEXIONA** | Respuesta abierta -- calificada por IA, feedback instantaneo (+5 XP) |

---
"""

s3 = []

# ═══════════════════════════════════════════════════════════════════════
# TITULO + SETUP
# ═══════════════════════════════════════════════════════════════════════

s3.append(md("nb3s1-titulo", f"""\
# Mision 2: Buscando Patrones
### Semana 3 -- Antes de Calcular, Aprende a Ver

**Hoy vas a trabajar con un dataset real:** el World Happiness Report 2019 --
puntaje de felicidad de 156 paises, junto con seis variables economicas y
sociales que podrian estar relacionadas con ese puntaje. La Mision 1 te enseño
a resumir una sola columna con honestidad. Esta mision te enseña algo nuevo:
**como saber si dos columnas se mueven juntas** -- y que tan peligroso es leer
esa relacion como algo mas de lo que realmente es.

---

{LEYENDA_ICONOS}"""))

s3.append(code("nb3s1-setup", """\
# Autograder (aun no publicado -- ver docstring de build_nb3.py) y dataset
# (repo: Santa-Maria-de-los-Andes/intro_to_stats)
!wget -q "https://raw.githubusercontent.com/Santa-Maria-de-los-Andes/intro_to_stats/main/course-python-stats/Weeks%203-4/autograder_nb3_semana3.py"
!wget -q "https://raw.githubusercontent.com/Santa-Maria-de-los-Andes/intro_to_stats/main/course-python-stats/Weeks%203-4/2019_es.csv"
from autograder_nb3_semana3 import Autograder
grader = Autograder()

import pandas as pd

df_felicidad = pd.read_csv('2019_es.csv')

print("Dataset cargado.")"""))

s3.append(md("nb3-dataset-md", """\
## 🌍 Un vistazo rapido antes de empezar

`df_felicidad` tiene **156 filas** (un pais o region por fila) y **10
columnas**: el puesto en el ranking, el nombre del pais, el continente, el
`Puntaje` de felicidad, y seis variables que el reporte usa para explicar ese
puntaje (`PBI per cápita`, `Apoyo social`, `Esperanza de vida saludable`,
`Libertad para tomar decisiones`, `Generosidad`, `Percepción de corrupción`).

A diferencia del dataset de videojuegos de la Mision 1, **este no tiene
ningun valor faltante** -- las 156 filas estan completas en las 10 columnas.
Eso no significa que el dataset sea perfecto (mas adelante vas a ver que una
de sus columnas es, en realidad, un espejo de otra) -- solo significa que hoy
el problema no es "que falta," sino **"que tan honesto es el patron que
creo ver."**
"""))

# ═══════════════════════════════════════════════════════════════════════
# APERTURA -- 3 diagramas, ningun numero todavia
# ═══════════════════════════════════════════════════════════════════════

s3.append(md("nb3-apertura-md", """\
## 🎬 Apertura -- Tres Diagramas, Ningun Numero Todavia

> *"Antes de que exista un numero para esto, tu ojo ya sabe reconocer un
> patron. La mision de hoy: aprender a ponerle un numero a lo que ya estas
> viendo."*

Abajo hay **tres diagramas de dispersion** reales, calculados con datos reales
de `df_felicidad`. Los ejes dicen solo "Variable X" y "Variable Y" a
proposito -- todavia no sabes que columnas son.

**Tu tarea, en parejas, antes de seguir:** ordena los tres diagramas de **mas
patron** (los puntos forman una linea reconocible) a **menos patron** (una
nube sin forma clara). No hay codigo que calcular todavia -- solo tu ojo.
"""))

s3.append(code("nb3-apertura-oculto", """\
# 👀 OBSERVA: tres diagramas reales, ejes sin identificar a proposito
import matplotlib.pyplot as plt

pares_apertura = [
    ('Libertad para tomar decisiones', 'Puntaje'),   # Diagrama 1
    ('Generosidad', 'Puntaje'),                       # Diagrama 2
    ('PBI per cápita', 'Puntaje'),                    # Diagrama 3
]

fig, axes = plt.subplots(1, 3, figsize=(13, 4))
for i, (ax, (col_x, col_y)) in enumerate(zip(axes, pares_apertura), start=1):
    ax.scatter(df_felicidad[col_x], df_felicidad[col_y], alpha=0.6)
    ax.set_xlabel('Variable X')
    ax.set_ylabel('Variable Y')
    ax.set_title(f'Diagrama {i}')
plt.tight_layout()
plt.show()"""))

s3.append(md("nb3-apertura-orden-md", """\
#### Antes de seguir -- tu orden

Escribe tu orden de "mas patron" a "menos patron" (ej. `"2, 3, 1"`). No se
califica -- es solo para comparar con la revelacion.
"""))
s3.append(code("nb3-apertura-orden-code", """\
# 🔮 PREDICE (no se califica, es solo para ti)
mi_orden_apertura = "___"  # ej: "Diagrama 3 es el mas fuerte, Diagrama 2 el mas debil\""""))

s3.append(code("nb3-apertura-reveal", """\
# 👀 OBSERVA: la revelacion -- mismos tres diagramas, ahora con nombres reales y su r
# El patron que vas a repetir todo el dia es siempre este:
#     df_felicidad['columna_x'].corr(df_felicidad['columna_y'])
# Aqui lo aplicamos tres veces, una por diagrama, con las columnas ya identificadas.

r_diagrama1 = df_felicidad['Libertad para tomar decisiones'].corr(df_felicidad['Puntaje'])
r_diagrama2 = df_felicidad['Generosidad'].corr(df_felicidad['Puntaje'])
r_diagrama3 = df_felicidad['PBI per cápita'].corr(df_felicidad['Puntaje'])

print("Diagrama 1 (Libertad para tomar decisiones vs. Puntaje) -> r =", round(r_diagrama1, 3))
print("Diagrama 2 (Generosidad vs. Puntaje)                    -> r =", round(r_diagrama2, 3))
print("Diagrama 3 (PBI per cápita vs. Puntaje)                 -> r =", round(r_diagrama3, 3))"""))

s3.append(md("nb3-apertura-explicacion", """\
**Diagrama 3 (PBI per cápita) es el patron mas fuerte** (r ≈ 0.79): los
paises con mayor produccion economica por persona tienden a reportar mayor
puntaje de felicidad. **Diagrama 2 (Generosidad) es casi una nube sin forma**
(r ≈ 0.08): saber cuanto dona en promedio la gente de un pais casi no te dice
nada sobre su puntaje de felicidad. Diagrama 1 (Libertad para tomar
decisiones) queda en medio (r ≈ 0.57) -- un patron real, pero mucho menos
limpio que el del PBI.

> ⚠️ Ningun numero de esta apertura dice **por que** pasa esto. "Los paises
> con mayor PBI per capita tienden a reportar mayor felicidad" es una
> **relacion observada** -- no es lo mismo que "tener mas dinero *causa*
> felicidad." Vas a volver a esta frase varias veces hoy.

*Se detecto una señal: dos columnas que parecen moverse juntas. Tu mision de
hoy: aprender a ponerle un numero exacto a "que tan juntas" -- y a reconocer
cuando ese numero se puede malinterpretar.*
"""))

# ═══════════════════════════════════════════════════════════════════════
# TEORIA DESBLOQUEADA
# ═══════════════════════════════════════════════════════════════════════

s3.append(md("nb3-teoria0-md", """\
## 🔓 Teoria Desbloqueada -- El Coeficiente de Correlacion

### ¿Que es el coeficiente de correlacion?

Un numero que resume **que tan fuerte** y **en que direccion** dos variables
numericas se mueven juntas. En este curso se calcula con `.corr()`
(correlacion de Pearson) -- el nombre tecnico se menciona una vez, no se
exige que lo memorices.

### El rango: -1 a 1

| Valor de r | Que significa |
|---|---|
| Cercano a **+1** | Relacion fuerte y positiva -- cuando una sube, la otra tiende a subir |
| Cercano a **-1** | Relacion fuerte y negativa -- cuando una sube, la otra tiende a bajar |
| Cercano a **0** | Relacion lineal debil o inexistente |

### Dos preguntas distintas: fuerza vs. direccion

- **Direccion** (el signo, + o −): ¿suben juntas o una sube mientras la otra
  baja?
- **Fuerza** (que tan lejos de 0): ¿que tan consistente es ese patron? Un r
  de 0.9 es un patron mucho mas consistente que uno de 0.3, aunque ambos sean
  positivos.

> ⚠️ **`.corr()` solo mide relacion *lineal*.** Una relacion real y fuerte
> pero curva puede dar un r cercano a 0. Es una frase de honestidad, no una
> unidad nueva -- este curso no enseña a detectar relaciones no lineales.

> ⚠️ **La regla mas importante de estas dos semanas:** un coeficiente de
> correlacion **nunca, por si solo, te dice si una variable causa la otra.**
> Todavia no explicamos el porque a fondo -- eso es trabajo de la Semana 5 --
> pero la frase queda plantada aqui, la primera vez que calculas un r real.
"""))

s3.append(teoria_check("nb3-t1-check", 1))
s3.append(teoria_check("nb3-t2-check", 2))
s3.append(teoria_check("nb3-t3-check", 3))
s3.append(teoria_check("nb3-t4-check", 4))
s3.append(teoria_check("nb3-t5-check", 5))

# ─── Seccion A -- Antes de Calcular ──────────────────────────────────────
s3.append(md("nb3-a-header", """\
---
## 📈 Seccion A -- Antes de Calcular

Un diagrama de dispersion (*scatter plot*) pone una variable en cada eje y
dibuja un punto por cada fila -- cada pais, en nuestro caso. `matplotlib` es
la libreria de Python para graficar; se importa asi:

```python
import matplotlib.pyplot as plt
```

La funcion que vas a usar hoy es `plt.scatter(x, y)`: dibuja un punto por
cada par `(x[i], y[i])`. El patron completo para un diagrama con ejes
identificados es:

```python
plt.scatter(df['columna_x'], df['columna_y'])
plt.xlabel('columna_x')
plt.ylabel('columna_y')
plt.show()
```
"""))

s3.append(code("nb3-a-guiado", """\
# 👀 OBSERVA: scatter con ejes identificados -- Apoyo social vs. Puntaje
plt.scatter(df_felicidad['Apoyo social'], df_felicidad['Puntaje'], alpha=0.6)
plt.xlabel('Apoyo social')
plt.ylabel('Puntaje')
plt.title('Apoyo social vs. Puntaje de felicidad')
plt.show()"""))

s3.append(md("nb3-a-repeticion-md", """\
### 🔁 Practica repetida: mismo patron, distintas columnas

El ejemplo guiado de arriba usa `Apoyo social`. Ahora repites **exactamente
el mismo patron** dos veces mas, cada vez con una columna distinta -- primero
`Percepción de corrupción`, despues `Esperanza de vida saludable`. Cada ronda
sigue la misma secuencia: predices, construyes, y comparas tu prediccion con
lo que realmente ves.
"""))

s3.append(md("nb3-a-ex1-md", """\
#### Ronda 1 -- Antes de seguir, predice

Mirando el patron guiado de arriba (Apoyo social vs. Puntaje): ¿te parece un
patron fuerte o debil? ¿positivo o negativo? Ahora, **sin graficar
todavia**, predice lo mismo para un par nuevo: `Percepción de corrupción`
vs. `Puntaje`.
"""))
s3.append(code("nb3-a-ex1-predice", """\
# 🔮 PREDICE (no se califica, es solo para ti)
mi_prediccion_corrupcion = "___"  # ej: "creo que es un patron debil y positivo\""""))

s3.append(md("nb3-a-ex1-ej-md", """\
#### ✅ Ejercicio 1 -- Construye tu propio scatter (15 pts)

🔨 Repite el patron del ejemplo guiado, pero con `Percepción de corrupción`
en el eje X y `Puntaje` en el eje Y. Incluye `plt.xlabel()` e `plt.ylabel()`.

Variables que espera el autograder: `x_ex1` (la columna que usaste en el eje
X), `y_ex1` (la columna que usaste en el eje Y).
"""))
s3.append(code("nb3-a-ex1-code", """\
# 🔨 CONSTRUYE

# ============================
#      Tu codigo aqui
# ============================


"""))
s3.append(code("nb3-a-ex1-check", "grader.check_ex1()"))

s3.append(md("nb3-a-ex1-reflexiona-md", """\
#### 💭 Reflexiona -- Ronda 1 (respuesta abierta -- calificada por IA, +5 XP)

En una frase: ¿tu ojo acerto en fuerza y direccion para `Percepción de
corrupción`, o te sorprendio algo del scatter que acabas de construir?
"""))
s3.append(reflexion_check("nb3-a-ex1-reflexiona-code", "a1"))

s3.append(md("nb3-a-ex2-md", """\
#### Ronda 2 -- Antes de seguir, predice

Misma mecanica, tercera columna: **sin graficar todavia**, predice si
`Esperanza de vida saludable` vs. `Puntaje` te parece un patron fuerte o
debil, positivo o negativo.
"""))
s3.append(code("nb3-a-ex2-predice", """\
# 🔮 PREDICE (no se califica, es solo para ti)
mi_prediccion_esperanza = "___"  # ej: "creo que es un patron fuerte y positivo\""""))

s3.append(md("nb3-a-ex2-ej-md", """\
#### ✅ Ejercicio 2 -- Construye tu propio scatter, otra vez (15 pts)

🔨 Mismo patron una vez mas, ahora con `Esperanza de vida saludable` en el
eje X y `Puntaje` en el eje Y.

Variables que espera el autograder: `x_ex2` (la columna que usaste en el eje
X), `y_ex2` (la columna que usaste en el eje Y).
"""))
s3.append(code("nb3-a-ex2-code", """\
# 🔨 CONSTRUYE

# ============================
#      Tu codigo aqui
# ============================


"""))
s3.append(code("nb3-a-ex2-check", "grader.check_ex2()"))

s3.append(md("nb3-a-ex2-reflexiona-md", """\
#### 💭 Reflexiona -- Ronda 2 (respuesta abierta -- calificada por IA, +5 XP)

En una frase: comparando los dos scatter que construiste hoy (`Percepción de
corrupción` y `Esperanza de vida saludable`), ¿en cual de los dos los puntos
siguen un patron mas apretado (menos dispersos)?
"""))
s3.append(reflexion_check("nb3-a-ex2-reflexiona-code", "a2"))

s3.append(code("nb3-a-checkpoint", """\
# ✅ CHECKPOINT -- necesitas 80% en esta seccion para continuar
grader.check_mini_a()"""))

# ─── Seccion B -- Calcúlalo ──────────────────────────────────────────────
s3.append(md("nb3-b-header", """\
---
## 🔢 Seccion B -- Calculalo

Ahora le ponemos el numero formal (`.corr()`) a los mismos pares que
trabajaste en la Seccion A. El patron es siempre el mismo:

```python
df['columna_x'].corr(df['columna_y'])
```

Devuelve un solo numero: el coeficiente de correlacion de Pearson entre esas
dos columnas.
"""))

s3.append(code("nb3-b-guiado", """\
# 👀 OBSERVA: el numero real detras del scatter guiado de la Seccion A
r_apoyo_social = df_felicidad['Apoyo social'].corr(df_felicidad['Puntaje'])
print(f"r (Apoyo social vs. Puntaje) = {r_apoyo_social:.3f}")"""))

s3.append(md("nb3-b-guiado-reflexiona-md", """\
#### 💭 Reflexiona -- interpreta el numero guiado (respuesta abierta -- calificada por IA, +5 XP)

En una frase, sin decir que una "causa" la otra: ¿que te dice un r ≈ 0.78
sobre la relacion entre `Apoyo social` y `Puntaje`?
"""))
s3.append(reflexion_check("nb3-b-guiado-reflexiona-code", "guiado"))

s3.append(teoria_check("nb3-t6-check", 6))

s3.append(md("nb3-b-outlier-md", """\
### 🔍 ¿Por que el ojo a veces se equivoca?

`Catar` tiene el `PBI per cápita` mas alto de las 156 filas (1.684) -- pero
su `Puntaje` (6.374) **no** es el mas alto del dataset (Finlandia lidera con
7.769). Un solo pais asi ya le resta "limpieza" visual a un patron que, en
conjunto, sigue siendo fuerte (r ≈ 0.79). Esto es lo normal, no un error de
datos: **ningun par de variables reales forma una linea perfecta.** Un
outlier real puede hacer que tu ojo dude de un patron que el numero confirma
-- o al reves, que tu ojo "vea" un patron que el numero desmiente.
"""))

s3.append(md("nb3-b-repeticion-md", """\
### 🔁 Practica repetida: mismo patron, tus dos pares de la Seccion A

Igual que en la Seccion A -- ahora le pones el numero real a cada uno de los
dos scatter que ya construiste, y comparas contra tu prediccion visual.
"""))

s3.append(md("nb3-b-ex3-md", """\
#### Ronda 1 -- ✅ Ejercicio 3: Tu prediccion contra la realidad (12 pts)

🧩 Calcula el r real para el par del Ejercicio 1
(`Percepción de corrupción` vs. `Puntaje`). Compara el resultado con tu
`mi_prediccion_corrupcion` de la Seccion A.
"""))
s3.append(code("nb3-b-ex3-code", """\
# 🧩 COMPLETA
r_corrupcion = ___

print(f"r (Percepcion de corrupcion vs. Puntaje) = {r_corrupcion:.3f}")"""))
s3.append(code("nb3-b-ex3-check", "grader.check_ex3()"))

s3.append(md("nb3-b-ex3-reflexiona-md", """\
#### 💭 Reflexiona -- Ronda 1 (respuesta abierta -- calificada por IA, +5 XP)

¿Que tan cerca estuvo tu prediccion del Ejercicio 1 del `r_corrupcion` real?
Y en tus propias palabras: ¿que dice este numero sobre la relacion entre
percepcion de corrupcion y felicidad?
"""))
s3.append(reflexion_check("nb3-b-ex3-reflexiona-code", "corrupcion"))

s3.append(md("nb3-b-ex4-md", """\
#### Ronda 2 -- ✅ Ejercicio 4: Tu prediccion contra la realidad, otra vez (12 pts)

🧩 Mismo patron, ahora con el par del Ejercicio 2
(`Esperanza de vida saludable` vs. `Puntaje`). Compara con tu
`mi_prediccion_esperanza` de la Seccion A.
"""))
s3.append(code("nb3-b-ex4-code", """\
# 🧩 COMPLETA
r_esperanza = ___

print(f"r (Esperanza de vida saludable vs. Puntaje) = {r_esperanza:.3f}")"""))
s3.append(code("nb3-b-ex4-check", "grader.check_ex4()"))

s3.append(md("nb3-b-ex4-reflexiona-md", """\
#### 💭 Reflexiona -- Ronda 2 (respuesta abierta -- calificada por IA, +5 XP)

`r_apoyo_social` y `r_esperanza` resultan casi identicos en fuerza (ambos
cerca de 0.78) aunque son variables completamente distintas. ¿Te parece
casualidad, o tiene sentido que ambas se relacionen con la felicidad de
manera parecida? Explica en 1-2 oraciones.
"""))
s3.append(reflexion_check("nb3-b-ex4-reflexiona-code", "esperanza"))

# ─── Rondas 3-6 -- mas alla de Puntaje ───────────────────────────────────
s3.append(md("nb3-b-mas-alla-md", """\
### 🔁 Practica repetida: pares que NO incluyen Puntaje

Hasta ahora cada par que trabajaste incluia `Puntaje`. Pero las seis
variables economicas y sociales tambien pueden relacionarse **entre si** --
esa es informacion real, y no se puede adivinar solo porque dos variables se
parezcan en como se relacionan con `Puntaje`.

Cuatro rondas mas, mismo patron de siempre (`plt.scatter()` + `.corr()`),
pero esta vez cada ronda junta las dos partes en un solo ejercicio. Cada
ronda tiene una pregunta ❓ **antes** de calcular (para pensar en el concepto,
no para adivinar el numero exacto) y otra ❓ **despues** (para revisar si
interpretaste bien tu propio resultado).
"""))

s3.append(md("nb3-b-ex5-md", """\
#### Ronda 3 -- PBI per cápita vs. Esperanza de vida saludable
"""))
s3.append(teoria_check("nb3-t7-check", 7))
s3.append(md("nb3-b-ex5-ej-md", """\
##### ✅ Ejercicio 5 -- Construye y calcula (15 pts)

🔨 Repite el patron completo: un scatter (`plt.scatter` con `xlabel`/`ylabel`)
**y** el coeficiente de correlacion, ahora para `PBI per cápita` (eje X) vs.
`Esperanza de vida saludable` (eje Y). Ninguna de las dos es `Puntaje`.

Variables que espera el autograder: `x_ex5`, `y_ex5` (columnas del scatter),
`r_ex5` (el coeficiente de correlacion entre ambas).
"""))
s3.append(code("nb3-b-ex5-code", """\
# 🔨 CONSTRUYE

# ============================
#      Tu codigo aqui
# ============================


"""))
s3.append(code("nb3-b-ex5-check", "grader.check_ex5()"))
s3.append(teoria_check("nb3-t8-check", 8))
s3.append(md("nb3-b-ex5-reflexiona-md", """\
##### 💭 Reflexiona -- Ronda 3 (respuesta abierta -- calificada por IA, +5 XP)

`PBI per cápita` y `Esperanza de vida saludable` salio con el r mas alto que
calculaste en toda la clase -- mas alto incluso que cualquiera de los dos con
`Puntaje`. ¿Por que crees que estas dos variables en particular se mueven
tan juntas?
"""))
s3.append(reflexion_check("nb3-b-ex5-reflexiona-code", "ronda3"))

s3.append(md("nb3-b-ex6-md", """\
#### Ronda 4 -- Apoyo social vs. Esperanza de vida saludable
"""))
s3.append(teoria_check("nb3-t9-check", 9))
s3.append(md("nb3-b-ex6-ej-md", """\
##### ✅ Ejercicio 6 -- Construye y calcula, otra vez (15 pts)

🔨 Mismo patron completo, ahora con `Apoyo social` (eje X) vs. `Esperanza de
vida saludable` (eje Y).

Variables que espera el autograder: `x_ex6`, `y_ex6`, `r_ex6`.
"""))
s3.append(code("nb3-b-ex6-code", """\
# 🔨 CONSTRUYE

# ============================
#      Tu codigo aqui
# ============================


"""))
s3.append(code("nb3-b-ex6-check", "grader.check_ex6()"))
s3.append(teoria_check("nb3-t10-check", 10))
s3.append(md("nb3-b-ex6-reflexiona-md", """\
##### 💭 Reflexiona -- Ronda 4 (respuesta abierta -- calificada por IA, +5 XP)

Compara el r de esta ronda con el r de la Ronda 3. Ambos pares comparten
`Esperanza de vida saludable`, pero dan numeros distintos. ¿Que te dice eso
sobre generalizar "esta variable siempre se relaciona igual de fuerte con
todo"?
"""))
s3.append(reflexion_check("nb3-b-ex6-reflexiona-code", "ronda4"))

s3.append(md("nb3-b-ex7-md", """\
#### Ronda 5 -- Libertad para tomar decisiones vs. Percepción de corrupción
"""))
s3.append(teoria_check("nb3-t11-check", 11))
s3.append(md("nb3-b-ex7-ej-md", """\
##### ✅ Ejercicio 7 -- Construye y calcula, una vez mas (15 pts)

🔨 Mismo patron completo, ahora con `Libertad para tomar decisiones` (eje X)
vs. `Percepción de corrupción` (eje Y).

Variables que espera el autograder: `x_ex7`, `y_ex7`, `r_ex7`.
"""))
s3.append(code("nb3-b-ex7-code", """\
# 🔨 CONSTRUYE

# ============================
#      Tu codigo aqui
# ============================


"""))
s3.append(code("nb3-b-ex7-check", "grader.check_ex7()"))
s3.append(teoria_check("nb3-t12-check", 12))
s3.append(md("nb3-b-ex7-reflexiona-md", """\
##### 💭 Reflexiona -- Ronda 5 (respuesta abierta -- calificada por IA, +5 XP)

Este par dio un r notablemente mas chico que las Rondas 3 y 4. En tus propias
palabras: ¿que significa "una relacion real, pero mucho menos consistente"?
"""))
s3.append(reflexion_check("nb3-b-ex7-reflexiona-code", "ronda5"))

s3.append(md("nb3-b-ex8-md", """\
#### Ronda 6 -- PBI per cápita vs. Generosidad
"""))
s3.append(teoria_check("nb3-t13-check", 13))
s3.append(md("nb3-b-ex8-ej-md", """\
##### ✅ Ejercicio 8 -- Construye y calcula, la ultima ronda (15 pts)

🔨 Mismo patron completo, ahora con `PBI per cápita` (eje X) vs.
`Generosidad` (eje Y).

Variables que espera el autograder: `x_ex8`, `y_ex8`, `r_ex8`.
"""))
s3.append(code("nb3-b-ex8-code", """\
# 🔨 CONSTRUYE

# ============================
#      Tu codigo aqui
# ============================


"""))
s3.append(code("nb3-b-ex8-check", "grader.check_ex8()"))
s3.append(teoria_check("nb3-t14-check", 14))
s3.append(md("nb3-b-ex8-reflexiona-md", """\
##### 💭 Reflexiona -- Ronda 6 (respuesta abierta -- calificada por IA, +5 XP)

De las seis variables economicas y sociales del dataset, `PBI per cápita` y
`Generosidad` dieron el r mas cercano a 0 de las cuatro rondas nuevas. ¿Te
parece razonable que el dinero de un pais casi no prediga que tan generosa
es su gente? ¿Por que si o por que no?
"""))
s3.append(reflexion_check("nb3-b-ex8-reflexiona-code", "ronda6"))

s3.append(md("nb3-b-ex9-md", """\
#### ✅ Ejercicio 9 -- Explora todas las correlaciones con Puntaje (15 pts)

🔨 Ya calculaste r para ocho pares distintos, seis de ellos contra `Puntaje`.
Ahora explora **todas** las columnas numericas del dataset a la vez: calcula
la correlacion de cada una con `Puntaje`, y encuentra cual es la mas fuerte y
cual es la mas debil.

Pista: `df_felicidad.corr(numeric_only=True)['Puntaje']` te da un r por cada
columna numerica de una sola vez -- pero **excluye la columna `'Puesto'`
antes de decidir cual es "la mas fuerte."** `Puesto` es el lugar en el
ranking -- se calcula directamente a partir de `Puntaje`, asi que su
correlacion casi perfecta (r ≈ -0.99) no es un hallazgo, es una definicion
circular. Tambien excluye `'Puntaje'` mismo (su correlacion consigo mismo
siempre es 1, tampoco es un hallazgo).

Variables que espera el autograder: `correlaciones_puntaje` (la Serie de r,
sin `Puesto` ni `Puntaje`), `columna_mas_fuerte` (nombre de columna, string),
`columna_mas_debil` (nombre de columna, string).
"""))
s3.append(code("nb3-b-ex9-code", """\
# 🔨 CONSTRUYE

# ============================
#      Tu codigo aqui
# ============================


print(f"Mas fuerte: {columna_mas_fuerte} | Mas debil: {columna_mas_debil}")"""))
s3.append(code("nb3-b-ex9-check", "grader.check_ex9()"))

s3.append(md("nb3-b-ex9-reflexiona-md", """\
#### 💭 Reflexiona (respuesta abierta -- calificada por IA, +5 XP)

De las seis variables que exploraste, ¿cual resultado te sorprendio mas --
una que esperabas fuerte y salio debil, o al reves? ¿Por que crees que pasa
eso?
"""))
s3.append(reflexion_check("nb3-b-ex9-reflexiona-code", "explora"))

s3.append(md("nb3-b-debug1-md", """\
#### ✅ Debug 1 -- Corrige el error (10 pts)

🔧 Este codigo deberia calcular la correlacion entre `PBI per cápita` y
`Puntaje`, pero tiene un error.
"""))
s3.append(code("nb3-b-debug1-code", """\
# 🔧 DEBUG: ejecuta, lee el mensaje completo, e identifica que tipo de error es antes de corregirlo
r_pbi = df_felicidad['PBI per cápita'].corr(df_felicidad['Punaje'])
print(r_pbi)"""))
s3.append(code("nb3-b-debug1-check", "grader.check_debug1()"))

s3.append(md("nb3-b-reflexiona-md", """\
#### 💭 Reflexiona (respuesta abierta -- calificada por IA, +5 XP)

`PBI per cápita` y `Puntaje` tienen r ≈ 0.79 -- una relacion fuerte y
positiva. **¿Significa esto que tener mas dinero produce felicidad?**
Escribe 2-3 oraciones: si no estas seguro de que la respuesta sea "si," ¿que
otra explicacion se te ocurre para esa relacion?
"""))
s3.append(reflexion_check("nb3-b-reflexiona-code", "causacion"))

s3.append(code("nb3-b-checkpoint", "grader.check_mini_b()"))

s3.append(md("nb3s1-cierre", """\
---
## 🏁 Fin de la Clase 1 -- Semana 3

Aprendiste a leer un patron con el ojo, a ponerle un numero exacto, y a
desconfiar de ese numero cuando corresponde. La **Semana 4** continua la
Mision 2: vas a descubrir que el patron general puede esconder -- o hasta
invertir -- lo que pasa dentro de cada grupo (Seccion C), y vas a elegir tu
propio par de variables para un mini-proyecto.
"""))
s3.append(code("nb3s1-resumen", "grader.resumen()"))

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

write_notebook(s3, "nb3_semana3_correlacion.ipynb")

# -*- coding: utf-8 -*-
"""
build_nb3_lite.py -- Genera nb3_lite_correlacion.ipynb, la RUTA DE
INTERPRETACION de la Semana 3 (accesibilidad/inclusion), companion de
build_nb3.py.

Mismo dataset, mismo narrativa, mismos 7 preguntas de teoria y las mismas 3
reflexiones que nb3_correlacion.ipynb -- confirmado que ninguna de ellas
depende de escribir codigo antes de construir esta ruta (ver
autograder_nb3_lite.py). Lo unico que cambia: los cuatro 🔨 CONSTRUYE de
"Grafica y Calcula" (antes check_ex1-ex4) se presentan aqui como celdas 👀
OBSERVA ya resueltas -- mismo codigo de referencia, mismos r reales
(recalculados 2026-08-20 contra 2019_es.csv, ver WORKFORCE_HANDOFF.md), el
estudiante ejecuta y lee en vez de escribir. Nunca se le pide "codigo mas
facil" -- se le quita la escritura, no el dato ni el grafico.

2026-08-23: se agrego el mismo "Quiz de Cierre" de 4 preguntas (t8-t11) que
nb3_correlacion.ipynb recibio el 2026-08-21 -- 1 pregunta de recordar el r
mas fuerte del dia + 3 escenarios nuevos sin relacion con el dataset. Esta
ruta NO recibio las Rondas 5/6 (PBI vs. Apoyo social, Generosidad vs.
Percepcion de corrupcion) que si se agregaron a nb3_correlacion.ipynb ese
dia -- el usuario pidio especificamente las preguntas de cierre para esta
ruta, no rondas nuevas. Por eso t8 (que en la version con codigo pregunta
por "Rondas 1 a 6") esta sobreescrito en autograder_nb3_lite.py para
preguntar por "Rondas 1 a 4" en su lugar -- ver ese archivo para el detalle.

No hereda nada de build_nb3.py en tiempo de ejecucion (cada build_nbN.py es
autocontenido, COURSE_TEMPLATE.md SS3) -- el contenido markdown que se
reusa (Apertura, Teoria Desbloqueada, dataset intro) se copio a mano desde
ese archivo, a proposito, para que este script siga siendo independiente.

Fuente de contenido: identico a build_nb3.py + ATLAS_spec_nb3_nb4.md (para
los r-values de referencia de cada ronda).
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

s3.append(md("nb3l-titulo", f"""\
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

s3.append(code("nb3l-setup", """\
# Carga el autograder y el dataset de esta leccion
!wget -q "https://raw.githubusercontent.com/Santa-Maria-de-los-Andes/intro_to_stats/main/course-python-stats/Weeks%203-4/autograder_nb3.py"
!wget -q "https://raw.githubusercontent.com/Santa-Maria-de-los-Andes/intro_to_stats/main/course-python-stats/Weeks%203-4/autograder_nb3_lite.py"
!wget -q "https://raw.githubusercontent.com/Santa-Maria-de-los-Andes/intro_to_stats/main/course-python-stats/Weeks%203-4/2019_es.csv"
from autograder_nb3_lite import Autograder
grader = Autograder()

import pandas as pd

df_felicidad = pd.read_csv('2019_es.csv')

print("Dataset cargado.")"""))

s3.append(md("nb3l-dataset-md", """\
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

# ─── Apertura (identica a nb3_correlacion.ipynb -- ya es 100% observacional) ──
s3.append(md("nb3l-apertura-md", """\
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

s3.append(code("nb3l-apertura-oculto", """\
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

s3.append(md("nb3l-apertura-orden-md", """\
#### Antes de seguir -- tu orden

Escribe tu orden de "mas patron" a "menos patron" (ej. `"2, 3, 1"`). No se
califica -- es solo para comparar con la revelacion.
"""))
s3.append(code("nb3l-apertura-orden-code", """\
# 🔮 PREDICE (no se califica, es solo para ti)
mi_orden_apertura = "___"  # ej: "Diagrama 3 es el mas fuerte, Diagrama 2 el mas debil\""""))

s3.append(code("nb3l-apertura-reveal", """\
# 👀 OBSERVA: la revelacion -- mismos tres diagramas, ahora con nombres reales y su r
# El patron que vas a ver repetido todo el dia es siempre este:
#     df_felicidad['columna_x'].corr(df_felicidad['columna_y'])
# Aqui lo aplicamos tres veces, una por diagrama, con las columnas ya identificadas.

r_diagrama1 = df_felicidad['Libertad para tomar decisiones'].corr(df_felicidad['Puntaje'])
r_diagrama2 = df_felicidad['Generosidad'].corr(df_felicidad['Puntaje'])
r_diagrama3 = df_felicidad['PBI per cápita'].corr(df_felicidad['Puntaje'])

print("Diagrama 1 (Libertad para tomar decisiones vs. Puntaje) -> r =", round(r_diagrama1, 3))
print("Diagrama 2 (Generosidad vs. Puntaje)                    -> r =", round(r_diagrama2, 3))
print("Diagrama 3 (PBI per cápita vs. Puntaje)                 -> r =", round(r_diagrama3, 3))"""))

s3.append(md("nb3l-apertura-explicacion", """\
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

# ─── Teoria Desbloqueada (identica) ────────────────────────────────────
s3.append(md("nb3l-teoria0-md", """\
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
> pero la frase queda plantada aqui, la primera vez que ves un r real.
"""))

s3.append(teoria_check("nb3l-t1-check", 1))
s3.append(teoria_check("nb3l-t2-check", 2))
s3.append(teoria_check("nb3l-t3-check", 3))
s3.append(teoria_check("nb3l-t4-check", 4))
s3.append(teoria_check("nb3l-t5-check", 5))

# ─── Observa y Calcula (version de interpretacion de Grafica y Calcula) ──
s3.append(md("nb3l-observaycalcula-header", """\
---
## 📈🔢 Observa y Calcula

Hoy vas a ver el mismo patron repetido varias veces -- el grafico y el
numero **ya vienen calculados**, tu trabajo es leerlos con atencion, no
escribir el codigo que los produce. Cada celda de abajo hace exactamente
esto, con columnas distintas cada vez:

```python
plt.scatter(df['columna_x'], df['columna_y'])
plt.xlabel('columna_x')
plt.ylabel('columna_y')
plt.show()

r = df['columna_x'].corr(df['columna_y'])
print(f"r = {r:.3f}")
```
"""))

s3.append(code("nb3l-guiado", """\
# 👀 OBSERVA: el patron completo, de una vez -- Apoyo social vs. Puntaje
plt.scatter(df_felicidad['Apoyo social'], df_felicidad['Puntaje'], alpha=0.6)
plt.xlabel('Apoyo social')
plt.ylabel('Puntaje')
plt.title('Apoyo social vs. Puntaje de felicidad')
plt.show()

r_apoyo_social = df_felicidad['Apoyo social'].corr(df_felicidad['Puntaje'])
print(f"r (Apoyo social vs. Puntaje) = {r_apoyo_social:.3f}")"""))

s3.append(md("nb3l-outlier-md", """\
### 🔍 ¿Por que el ojo a veces se equivoca?

`Catar` tiene el `PBI per cápita` mas alto de las 156 filas (1.684) -- pero
su `Puntaje` (6.374) **no** es el mas alto del dataset (Finlandia lidera con
7.769). Un solo pais asi ya le resta "limpieza" visual al Diagrama 3 de la
Apertura, que en conjunto sigue siendo fuerte (r ≈ 0.79). Esto es lo normal,
no un error de datos: **ningun par de variables reales forma una linea
perfecta.** Un outlier real puede hacer que tu ojo dude de un patron que el
numero confirma -- o al reves, que tu ojo "vea" un patron que el numero
desmiente.
"""))

s3.append(teoria_check("nb3l-t6-check", 6))

s3.append(md("nb3l-repeticion-md", """\
### 🔁 Cuatro rondas mas: mismo patron, distintos pares

Cuatro rondas, mismo patron de siempre (`plt.scatter()` + `.corr()`), ya
ejecutadas -- el codigo y el resultado estan completos en cada celda. Lee el
grafico, lee el numero, y responde lo que se te pide despues.
"""))

# Ronda 1 -- reflexiona
s3.append(md("nb3l-ronda1-predice-md", """\
#### Ronda 1 -- Antes de seguir, predice

Mirando el patron guiado de arriba (Apoyo social vs. Puntaje): ¿te parece un
patron fuerte o debil? ¿positivo o negativo? Ahora, **sin ver el resultado
todavia**, predice lo mismo para un par nuevo: `Percepción de corrupción`
vs. `Puntaje`.
"""))
s3.append(code("nb3l-ronda1-predice-code", """\
# 🔮 PREDICE (no se califica, es solo para ti)
mi_prediccion_ronda1 = "___"  # ej: "creo que es un patron debil y positivo\""""))

s3.append(md("nb3l-ronda1-md", """\
#### 👀 Ronda 1 -- Percepción de corrupción vs. Puntaje

Codigo y resultado ya listos -- ejecuta la celda y compara con tu prediccion.
"""))
s3.append(code("nb3l-ronda1-code", """\
# 👀 OBSERVA
plt.scatter(df_felicidad['Percepción de corrupción'], df_felicidad['Puntaje'], alpha=0.6)
plt.xlabel('Percepción de corrupción')
plt.ylabel('Puntaje')
plt.title('Percepción de corrupción vs. Puntaje de felicidad')
plt.show()

r_ronda1 = df_felicidad['Percepción de corrupción'].corr(df_felicidad['Puntaje'])
print(f"r (Percepción de corrupción vs. Puntaje) = {r_ronda1:.3f}")"""))

s3.append(md("nb3l-ronda1-reflexiona-md", """\
#### 💭 Reflexiona -- Ronda 1 (respuesta abierta -- calificada por IA, +5 XP)

En una frase: ¿tu ojo acerto en fuerza y direccion para `Percepción de
corrupción`, o te sorprendio algo del resultado?
"""))
s3.append(reflexion_check("nb3l-ronda1-reflexiona-code", "ronda1"))

# Ronda 2 -- sin reflexion
s3.append(md("nb3l-ronda2-predice-md", """\
#### Ronda 2 -- Antes de seguir, predice

Misma mecanica, tercera columna: **sin ver el resultado todavia**, predice si
`Esperanza de vida saludable` vs. `Puntaje` te parece un patron fuerte o
debil, positivo o negativo.
"""))
s3.append(code("nb3l-ronda2-predice-code", """\
# 🔮 PREDICE (no se califica, es solo para ti)
mi_prediccion_ronda2 = "___"  # ej: "creo que es un patron fuerte y positivo\""""))

s3.append(md("nb3l-ronda2-md", """\
#### 👀 Ronda 2 -- Esperanza de vida saludable vs. Puntaje
"""))
s3.append(code("nb3l-ronda2-code", """\
# 👀 OBSERVA
plt.scatter(df_felicidad['Esperanza de vida saludable'], df_felicidad['Puntaje'], alpha=0.6)
plt.xlabel('Esperanza de vida saludable')
plt.ylabel('Puntaje')
plt.title('Esperanza de vida saludable vs. Puntaje de felicidad')
plt.show()

r_ronda2 = df_felicidad['Esperanza de vida saludable'].corr(df_felicidad['Puntaje'])
print(f"r (Esperanza de vida saludable vs. Puntaje) = {r_ronda2:.3f}")"""))

s3.append(teoria_check("nb3l-t7-check", 7))

# Ronda 3 -- reflexiona
s3.append(md("nb3l-ronda3-md", """\
#### 👀 Ronda 3 -- PBI per cápita vs. Esperanza de vida saludable

Esta vez ninguna de las dos columnas es `Puntaje` -- las seis variables
economicas y sociales tambien pueden relacionarse **entre si**.
"""))
s3.append(code("nb3l-ronda3-code", """\
# 👀 OBSERVA
plt.scatter(df_felicidad['PBI per cápita'], df_felicidad['Esperanza de vida saludable'], alpha=0.6)
plt.xlabel('PBI per cápita')
plt.ylabel('Esperanza de vida saludable')
plt.title('PBI per cápita vs. Esperanza de vida saludable')
plt.show()

r_ronda3 = df_felicidad['PBI per cápita'].corr(df_felicidad['Esperanza de vida saludable'])
print(f"r (PBI per cápita vs. Esperanza de vida saludable) = {r_ronda3:.3f}")"""))

s3.append(md("nb3l-ronda3-reflexiona-md", """\
#### 💭 Reflexiona -- Ronda 3 (respuesta abierta -- calificada por IA, +5 XP)

`PBI per cápita` y `Esperanza de vida saludable` te deberia haber dado el r
mas alto que has visto hoy (mas alto incluso que cualquiera de los dos contra
`Puntaje`). ¿Por que crees que estas dos variables en particular se mueven
tan juntas?
"""))
s3.append(reflexion_check("nb3l-ronda3-reflexiona-code", "ronda3"))

# Ronda 4 -- sin reflexion
s3.append(md("nb3l-ronda4-md", """\
#### 👀 Ronda 4 -- Apoyo social vs. Esperanza de vida saludable

Mismo patron, otro par sin `Puntaje`.
"""))
s3.append(code("nb3l-ronda4-code", """\
# 👀 OBSERVA
plt.scatter(df_felicidad['Apoyo social'], df_felicidad['Esperanza de vida saludable'], alpha=0.6)
plt.xlabel('Apoyo social')
plt.ylabel('Esperanza de vida saludable')
plt.title('Apoyo social vs. Esperanza de vida saludable')
plt.show()

r_ronda4 = df_felicidad['Apoyo social'].corr(df_felicidad['Esperanza de vida saludable'])
print(f"r (Apoyo social vs. Esperanza de vida saludable) = {r_ronda4:.3f}")"""))

# Chequeo de concepto -- reflexiona
s3.append(md("nb3l-concepto-md", """\
### 🧠 Chequeo de concepto

Ya viste `r` calculado seis veces hoy (Apertura + cuatro Rondas + el ejemplo
guiado). Antes de cerrar la clase, pon el concepto en tus propias palabras
-- sin usar ningun dataset ni numero especifico.
"""))
s3.append(md("nb3l-concepto-reflexiona-md", """\
#### 💭 Reflexiona -- explica el concepto (respuesta abierta -- calificada por IA, +5 XP)

En 2-3 oraciones, sin usar ningun par de columnas como ejemplo: ¿que te dice
el coeficiente de correlacion, y que es lo que **nunca** te dice por si
solo?
"""))
s3.append(reflexion_check("nb3l-concepto-reflexiona-code", "concepto"))

# ─── Quiz de Cierre (2026-08-23, ver autograder_nb3_lite.py docstring) ────
s3.append(md("nb3l-quiz-header", """\
---
## 🧭 Quiz de Cierre

Ya viste cuatro correlaciones reales hoy. Antes de cerrar: una pregunta
para recordar lo que viste en esta clase, y tres preguntas con ejemplos
**nuevos** -- para probar si el concepto de correlacion se te quedo mas
alla del dataset de felicidad.
"""))

s3.append(teoria_check("nb3l-t8-check", 8))
s3.append(teoria_check("nb3l-t9-check", 9))
s3.append(teoria_check("nb3l-t10-check", 10))
s3.append(teoria_check("nb3l-t11-check", 11))

s3.append(code("nb3l-checkpoint", """\
# ✅ CHECKPOINT -- necesitas 80% en esta seccion para continuar
grader.check_mini_a()"""))

s3.append(md("nb3l-cierre", """\
---
## 🏁 Fin de la Clase 1 -- Semana 3

Aprendiste a leer un patron, a reconocer que te dice el numero que lo
acompaña, y a desconfiar de ese numero cuando corresponde. La **Semana 4**
continua la Mision 2: vas a descubrir que el patron general puede esconder --
o hasta invertir -- lo que pasa dentro de cada grupo, y vas a elegir tu propio
par de variables para un mini-proyecto.
"""))
s3.append(code("nb3l-resumen", "grader.resumen()"))


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

write_notebook(s3, "nb3_lite_correlacion.ipynb")

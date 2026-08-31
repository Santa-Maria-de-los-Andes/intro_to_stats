# -*- coding: utf-8 -*-
"""
build_nb4.py -- Genera nb4_correlacion.ipynb (Semana 4 / Clase 2 de la
Mision 2: Buscando Patrones -- continuacion narrativa de nb3_correlacion.ipynb,
ver ese archivo para el porque del split de nombres).

Hermano de `build_nb3.py`: mismos helpers (`md`/`code`/`teoria_check`/
`reflexion_check`/`LEYENDA_ICONOS`), duplicados aqui a proposito -- cada
build_nbN.py es autocontenido, no importa de otro build script
(COURSE_TEMPLATE.md SS3).

check_ex/check_debug/check_tN SIGUEN la numeracion global desde donde nb3
termina (ex7-8, t10, debug1) -- narrativamente esto sigue siendo
"Mision 2, segunda clase", aunque el archivo ya no comparta nb-prefijo con
nb3_correlacion.ipynb (rename explicito del usuario 2026-08-20). Ver
`ATLAS_spec_nb3_nb4.md` para el detalle completo que ATLAS necesita.

Contenido nuevo en este archivo (no existia antes del rebuild 2026-08-20):
Seccion C (correlacion por subgrupo de continente, via filtrado booleano +
`.corr()` -- NO `.groupby().apply(lambda...)`, fuera del temario comprometido,
ver WORKFORCE_CONTRACT.md SS5). Todos los numeros (incluidos los de Seccion C
por continente) se calcularon directamente contra 2019_es.csv 2026-08-20.

RECORTE 2026-08-29 (decision del usuario): las Rondas 5-6 (repeticion pura
del patron grafica+calcula de la Semana 3, ex5/ex6/t8/t9/reflexion_ronda6) y
el Mini-Proyecto de integracion (intex1 + sus dos reflexiones) se eliminaron
de este archivo. Motivo: las Rondas 5-6 no aportaban una habilidad nueva
(bajo valor de supervision en clase), y el Mini-Proyecto se reemplaza por un
proyecto de investigacion mas grande y realmente propio del estudiante
(propio dataset, no solo propio par dentro de 2019_es.csv) --
`build_proyecto_investigacion.py` / `proyecto_investigacion.ipynb`, mismo
folder. Ese notebook nuevo, no `intex1`, es ahora el material de entrada de
la Semana 5 -- ver WORKFORCE_HANDOFF.md Done log 2026-08-29 y la nota de
continuidad actualizada en `ATLAS_spec_nb3_nb4.md`. Seccion C (subgrupos) se
mantiene intacta: es la habilidad distinta y deliberadamente disenada como
puente a la Semana 5, no una repeticion.
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



s4 = []

s4.append(md("nb4-titulo", """\
# Mision 2: Buscando Patrones
### Semana 4 -- Subgrupos

**Donde quedamos:** en la Semana 3 aprendiste a leer un patron con el ojo y a
ponerle un numero exacto (`.corr()`). Hoy: un debug, una exploracion de
**todas** las correlaciones del dataset a la vez, y un vistazo a que pasa
**dentro de cada continente** (el patron general no siempre cuenta toda la
historia).

Tu propio proyecto de investigacion -- con tu propio dataset -- arranca en
clase aparte de este notebook. Ese es el hallazgo que vas a usar la
**Semana 5**, asi que guardalo bien.
"""))

s4.append(code("nb4-setup", """\
# Carga el autograder y el dataset de esta leccion (mismo dataset que Semana 3)
!wget -q "https://raw.githubusercontent.com/Santa-Maria-de-los-Andes/intro_to_stats/main/course-python-stats/Weeks%203-4/autograder_nb4.py"
!wget -q "https://raw.githubusercontent.com/Santa-Maria-de-los-Andes/intro_to_stats/main/course-python-stats/Weeks%203-4/2019_es.csv"
from autograder_nb4 import Autograder
grader = Autograder()

import pandas as pd
import matplotlib.pyplot as plt

df_felicidad = pd.read_csv('2019_es.csv')

print("Dataset cargado.")"""))

# ─── Debug ────────────────────────────────────────────────────────────
s4.append(md("nb4-debug1-md", """\
#### ✅ Debug 1 -- Corrige el error (10 pts)

🔧 Este codigo deberia calcular la correlacion entre `PBI per cápita` y
`Puntaje`, pero tiene un error.
"""))
s4.append(code("nb4-debug1-code", """\
# 🔧 DEBUG: ejecuta, lee el mensaje completo, e identifica que tipo de error es antes de corregirlo
r_pbi = df_felicidad['PBI per cápita'].corr(df_felicidad['Punaje'])
print(r_pbi)"""))
s4.append(code("nb4-debug1-check", "grader.check_debug1()"))

# ─── Explora todo ────────────────────────────────────────────────────
s4.append(md("nb4-ex7-md", """\
#### ✅ Ejercicio 7 -- Explora todas las correlaciones con Puntaje (20 pts)

🔨 Ya calculaste r para varios pares distintos, la mayoria contra `Puntaje`.
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
s4.append(code("nb4-ex7-code", """\
# 🔨 CONSTRUYE

# ============================
#      Tu codigo aqui
# ============================


print(f"Mas fuerte: {columna_mas_fuerte} | Mas debil: {columna_mas_debil}")"""))
s4.append(code("nb4-ex7-check", "grader.check_ex7()"))

s4.append(code("nb4-checkpoint-b", """\
# ✅ CHECKPOINT -- necesitas 80% en esta seccion para continuar
grader.check_mini_b()"""))

# ─── Seccion C -- Por Subgrupos ──────────────────────────────────────
s4.append(md("nb4-seccionc-header", """\
---
## 🌎 Seccion C -- Por Subgrupos

Hasta ahora calculaste `r` sobre las 156 filas juntas. Pero `df_felicidad`
tambien tiene una columna categorica, `Continente` -- y ya sabes filtrar por
categoria (Mision 1). La pregunta de hoy: **¿el patron general se sostiene
dentro de cada continente, o cambia?**

Primero, un vistazo con lo que ya conoces -- `.groupby()` para una estadistica
simple por continente:
"""))
s4.append(code("nb4-seccionc-groupby-demo", """\
# 👀 OBSERVA: promedio de Puntaje por continente
df_felicidad.groupby('Continente')['Puntaje'].mean().sort_values(ascending=False)"""))

s4.append(md("nb4-seccionc-corr-demo-md", """\
Para el `r` **dentro** de un continente, usas exactamente lo que ya sabes:
filtras por categoria, y le calculas `.corr()` al subconjunto filtrado.
"""))
s4.append(code("nb4-seccionc-corr-demo", """\
# 👀 OBSERVA: PBI per cápita vs. Puntaje, dentro de Europa nada mas
df_europa = df_felicidad[df_felicidad['Continente'] == 'Europa']
r_pbi_europa = df_europa['PBI per cápita'].corr(df_europa['Puntaje'])
print(f"r (PBI vs. Puntaje) en Europa = {r_pbi_europa:.3f}")

# Ahora lo mismo, pero en África
df_africa = df_felicidad[df_felicidad['Continente'] == 'África']
r_pbi_africa = df_africa['PBI per cápita'].corr(df_africa['Puntaje'])
print(f"r (PBI vs. Puntaje) en África  = {r_pbi_africa:.3f}")

print(f"\\n(recuerda: el r general de PBI vs. Puntaje, con los 156 países juntos, era ≈0.79)")"""))

s4.append(md("nb4-seccionc-explicacion-md", """\
En Europa el patron es **igual de fuerte** que el general (r ≈ 0.81 vs. 0.79
general) -- pero en África es notablemente **mas debil** (r ≈ 0.49). El mismo
par de variables, la misma pregunta, y la respuesta cambia segun el
continente. **El patron general puede esconder -- o incluso invertir -- lo
que pasa dentro de cada grupo.**
"""))

s4.append(md("nb4-seccionc-oceania-md", """\
### ⚠️ Un aviso antes de seguir

Si filtras por `Oceanía`, vas a obtener un r casi perfecto (≈ ±1.0). No es un
hallazgo -- es una trampa. `Oceanía` tiene **solo 2 paises** en este dataset.
Con 2 puntos, cualquier par de columnas "se correlaciona perfecto" -- una
sola linea siempre pasa exacto por 2 puntos. Esto no tiene nada que ver con
causalidad (eso es la Semana 5); es un problema distinto: **muy pocos datos
no dan una correlacion confiable, sin importar que tan alta salga.**
"""))
s4.append(teoria_check("nb4-t10-check", 10))

s4.append(md("nb4-seccionc-ex8-md", """\
#### ✅ Ejercicio 8 -- Un par que casi no se relaciona, por continente (20 pts)

🔨 En la Semana 3 viste que `Generosidad` vs. `Puntaje` da un r general casi
nulo. Ahora repite el patron de arriba (filtra + `.corr()`) para
`Generosidad` vs. `Puntaje`, pero calculalo **dentro de Europa** y **dentro
de América** por separado.

Variables que espera el autograder: `r_generosidad_europa`,
`r_generosidad_america` (ambos numeros, redondeados a 3 decimales como en
los ejemplos de arriba).
"""))
s4.append(code("nb4-seccionc-ex8-code", """\
# 🔨 CONSTRUYE

# ============================
#      Tu codigo aqui
# ============================


print(f"r (Generosidad vs. Puntaje) en Europa  = {r_generosidad_europa:.3f}")
print(f"r (Generosidad vs. Puntaje) en América = {r_generosidad_america:.3f}")"""))
s4.append(code("nb4-seccionc-ex8-check", "grader.check_ex8()"))

s4.append(md("nb4-seccionc-reflexiona-md", """\
#### 💭 Reflexiona (respuesta abierta -- calificada por IA, +5 XP)

El r general de `Generosidad` vs. `Puntaje` era casi 0. Pero acabas de ver
que dentro de Europa es positivo, y dentro de América es negativo. En 2-3
oraciones: ¿que te dice esto sobre confiar en "el patron general" de todo un
dataset sin mirar los subgrupos?
"""))
s4.append(reflexion_check("nb4-seccionc-reflexiona-code", "subgrupos"))

s4.append(code("nb4-checkpoint-c", """\
# ✅ CHECKPOINT -- necesitas 80% en esta seccion para continuar
grader.check_mini_c()"""))

s4.append(md("nb4-cierre", """\
---
## 🏁 Fin de la Mision 2 -- Semanas 3-4

Aprendiste a leer un patron, a ponerle un numero, a desconfiar de ese numero,
y a desconfiar del patron general cuando no mira los subgrupos. Ahora te toca
a ti: tu proyecto de investigacion, con tu propio dataset, es donde vas a
encontrar (y defender) un patron que nadie te dio ya armado. Guarda tu par de
variables, tu r, y tu hipotesis -- la **Semana 5** va a poner a prueba
exactamente eso.
"""))
s4.append(code("nb4-resumen", "grader.resumen()"))


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

write_notebook(s4, "nb4_correlacion.ipynb")

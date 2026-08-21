# -*- coding: utf-8 -*-
"""
build_nb4_lite.py -- Genera nb4_lite_correlacion.ipynb, la RUTA DE
INTERPRETACION de la Semana 4 (accesibilidad/inclusion), companion de
build_nb4.py y hermano de build_nb3_lite.py.

Mismo dataset, misma narrativa, mismos t8/t9/t10 y las mismas 4 reflexiones
(ronda6, subgrupos, interpretacion, metodologica) que nb4_correlacion.ipynb.
Tres piezas rediseñadas para no requerir escribir codigo (ver
autograder_nb4_lite.py para el detalle de cada rediseño):
  - Rondas 5-6, Ejercicio 7 (explora todo) y Ejercicio 8 (Seccion C) pasan de
    🔨 CONSTRUYE a 👀 OBSERVA -- codigo y resultado ya listos.
  - Debug 1 pasa de "corrige el codigo" a "lee el error ya ejecutado y
    responde una pregunta de opcion multiple" (t11, nueva entrada en el
    _TEORIA de autograder_nb4_lite.py).
  - El Mini-Proyecto pasa de "escribe el codigo para tu propio par" a 🧩
    COMPLETA: el estudiante llena mini_var_x/mini_var_y/mini_hipotesis: el
    calculo de mini_r ya viene escrito en la celda.

No importa nada de build_nb4.py en tiempo de ejecucion (cada build_nbN.py es
autocontenido, COURSE_TEMPLATE.md SS3) -- el contenido reusado se copio a
mano desde ese archivo.
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

s4.append(md("nb4l-titulo", """\
# Mision 2: Buscando Patrones
### Semana 4 -- Subgrupos y tu Propio Hallazgo

**Donde quedamos:** en la Semana 3 viste como leer un patron y como se le
pone un numero exacto (`.corr()`). Hoy: dos rondas mas para terminar de
solidificar el patron, un vistazo a que pasa **dentro de cada continente**
(el patron general no siempre cuenta toda la historia), y para cerrar, tu
propio mini-proyecto -- vas a elegir un par de variables, ver su relacion, y
defender por que crees que estan relacionadas. Ese hallazgo es el material
que vas a usar la **Semana 5**, asi que guardalo bien.
"""))

s4.append(code("nb4l-setup", """\
# Carga el autograder y el dataset de esta leccion (mismo dataset que Semana 3)
!wget -q "https://raw.githubusercontent.com/Santa-Maria-de-los-Andes/intro_to_stats/main/course-python-stats/Weeks%203-4/autograder_nb4.py"
!wget -q "https://raw.githubusercontent.com/Santa-Maria-de-los-Andes/intro_to_stats/main/course-python-stats/Weeks%203-4/autograder_nb4_lite.py"
!wget -q "https://raw.githubusercontent.com/Santa-Maria-de-los-Andes/intro_to_stats/main/course-python-stats/Weeks%203-4/2019_es.csv"
from autograder_nb4_lite import Autograder
grader = Autograder()

import pandas as pd
import matplotlib.pyplot as plt

df_felicidad = pd.read_csv('2019_es.csv')

print("Dataset cargado.")"""))

# ─── Rondas 5-6 (ya resueltas) ────────────────────────────────────
s4.append(md("nb4l-repeticion-md", """\
## 📈🔢 Dos rondas mas para cerrar el patron

Mismo patron que la Semana 3: grafico + `r`, ya calculados -- lee y
responde.
"""))

s4.append(md("nb4l-ronda5-md", """\
#### Ronda 5 -- Libertad para tomar decisiones vs. Percepción de corrupción
"""))
s4.append(teoria_check("nb4l-t8-check", 8))
s4.append(md("nb4l-ronda5-ej-md", """\
##### 👀 Observa el resultado

`Libertad para tomar decisiones` (eje X) vs. `Percepción de corrupción`
(eje Y).
"""))
s4.append(code("nb4l-ronda5-code", """\
# 👀 OBSERVA
plt.scatter(df_felicidad['Libertad para tomar decisiones'], df_felicidad['Percepción de corrupción'], alpha=0.6)
plt.xlabel('Libertad para tomar decisiones')
plt.ylabel('Percepción de corrupción')
plt.title('Libertad para tomar decisiones vs. Percepción de corrupción')
plt.show()

r_ronda5 = df_felicidad['Libertad para tomar decisiones'].corr(df_felicidad['Percepción de corrupción'])
print(f"r (Libertad para tomar decisiones vs. Percepción de corrupción) = {r_ronda5:.3f}")"""))

s4.append(md("nb4l-ronda6-md", """\
#### Ronda 6 -- PBI per cápita vs. Generosidad
"""))
s4.append(md("nb4l-ronda6-ej-md", """\
##### 👀 Observa el resultado, la ultima ronda

`PBI per cápita` (eje X) vs. `Generosidad` (eje Y).
"""))
s4.append(code("nb4l-ronda6-code", """\
# 👀 OBSERVA
plt.scatter(df_felicidad['PBI per cápita'], df_felicidad['Generosidad'], alpha=0.6)
plt.xlabel('PBI per cápita')
plt.ylabel('Generosidad')
plt.title('PBI per cápita vs. Generosidad')
plt.show()

r_ronda6 = df_felicidad['PBI per cápita'].corr(df_felicidad['Generosidad'])
print(f"r (PBI per cápita vs. Generosidad) = {r_ronda6:.3f}")"""))
s4.append(teoria_check("nb4l-t9-check", 9))

s4.append(md("nb4l-ronda6-reflexiona-md", """\
##### 💭 Reflexiona (respuesta abierta -- calificada por IA, +5 XP)

`PBI per cápita` y `Generosidad` dan un r muy cercano a 0. ¿Te parece
razonable que el dinero de un pais casi no prediga que tan generosa es su
gente? ¿Por que si o por que no?
"""))
s4.append(reflexion_check("nb4l-ronda6-reflexiona-code", "ronda6"))

# ─── Debug 1 -- opcion multiple en vez de corregir codigo ─────────────
s4.append(md("nb4l-debug1-md", """\
#### 🔧 Debug 1 -- Lee el error (5 pts)

Este codigo intenta calcular la correlacion entre `PBI per cápita` y
`Puntaje`, pero tiene un error. **No necesitas corregirlo** -- ejecuta la
celda, lee el mensaje de error completo, y despues responde la pregunta de
opcion multiple que sigue.
"""))
s4.append(code("nb4l-debug1-code", """\
# 🔧 DEBUG: ejecuta y lee el mensaje de error completo (no hace falta corregir nada)
r_pbi = df_felicidad['PBI per cápita'].corr(df_felicidad['Punaje'])
print(r_pbi)"""))
s4.append(code("nb4l-debug1-check", "grader.check_debug1()"))

# ─── Explora todo (ya resuelto) ────────────────────────────────────
s4.append(md("nb4l-ex7-md", """\
#### 👀 Explora todas las correlaciones con Puntaje

Ya viste `r` para varios pares distintos, la mayoria contra `Puntaje`. Esta
celda calcula la correlacion de **todas** las columnas numericas con
`Puntaje` a la vez -- ya excluye `Puesto` (su correlacion es circular, no un
hallazgo: se calcula directamente a partir de `Puntaje`) y `Puntaje` mismo
(su correlacion consigo mismo siempre es 1, tampoco es un hallazgo).
"""))
s4.append(code("nb4l-ex7-code", """\
# 👀 OBSERVA
correlaciones_puntaje = df_felicidad.corr(numeric_only=True)['Puntaje'].drop(['Puesto', 'Puntaje'])
columna_mas_fuerte = correlaciones_puntaje.abs().idxmax()
columna_mas_debil  = correlaciones_puntaje.abs().idxmin()

print(correlaciones_puntaje.sort_values(ascending=False))
print(f"\\nMas fuerte: {columna_mas_fuerte} | Mas debil: {columna_mas_debil}")"""))

s4.append(code("nb4l-checkpoint-b", """\
# ✅ CHECKPOINT -- necesitas 80% en esta seccion para continuar
grader.check_mini_b()"""))

# ─── Seccion C -- Por Subgrupos ──────────────────────────────────────
s4.append(md("nb4l-seccionc-header", """\
---
## 🌎 Seccion C -- Por Subgrupos

Hasta ahora viste `r` calculado sobre las 156 filas juntas. Pero
`df_felicidad` tambien tiene una columna categorica, `Continente`. La
pregunta de hoy: **¿el patron general se sostiene dentro de cada continente,
o cambia?**

Primero, un vistazo simple -- promedio de `Puntaje` por continente:
"""))
s4.append(code("nb4l-seccionc-groupby-demo", """\
# 👀 OBSERVA: promedio de Puntaje por continente
df_felicidad.groupby('Continente')['Puntaje'].mean().sort_values(ascending=False)"""))

s4.append(md("nb4l-seccionc-corr-demo-md", """\
Para el `r` **dentro** de un continente, se filtra por categoria y se
calcula `.corr()` sobre el subconjunto filtrado.
"""))
s4.append(code("nb4l-seccionc-corr-demo", """\
# 👀 OBSERVA: PBI per cápita vs. Puntaje, dentro de Europa nada mas
df_europa = df_felicidad[df_felicidad['Continente'] == 'Europa']
r_pbi_europa = df_europa['PBI per cápita'].corr(df_europa['Puntaje'])
print(f"r (PBI vs. Puntaje) en Europa = {r_pbi_europa:.3f}")

# Ahora lo mismo, pero en África
df_africa = df_felicidad[df_felicidad['Continente'] == 'África']
r_pbi_africa = df_africa['PBI per cápita'].corr(df_africa['Puntaje'])
print(f"r (PBI vs. Puntaje) en África  = {r_pbi_africa:.3f}")

print(f"\\n(recuerda: el r general de PBI vs. Puntaje, con los 156 países juntos, era ≈0.79)")"""))

s4.append(md("nb4l-seccionc-explicacion-md", """\
En Europa el patron es **igual de fuerte** que el general (r ≈ 0.81 vs. 0.79
general) -- pero en África es notablemente **mas debil** (r ≈ 0.49). El mismo
par de variables, la misma pregunta, y la respuesta cambia segun el
continente. **El patron general puede esconder -- o incluso invertir -- lo
que pasa dentro de cada grupo.**
"""))

s4.append(md("nb4l-seccionc-oceania-md", """\
### ⚠️ Un aviso antes de seguir

Si filtras por `Oceanía`, se obtiene un r casi perfecto (≈ ±1.0). No es un
hallazgo -- es una trampa. `Oceanía` tiene **solo 2 paises** en este
dataset. Con 2 puntos, cualquier par de columnas "se correlaciona perfecto"
-- una sola linea siempre pasa exacto por 2 puntos. Esto no tiene nada que
ver con causalidad (eso es la Semana 5); es un problema distinto: **muy
pocos datos no dan una correlacion confiable, sin importar que tan alta
salga.**
"""))
s4.append(teoria_check("nb4l-t10-check", 10))

s4.append(md("nb4l-seccionc-ex8-md", """\
#### 👀 Un par que casi no se relaciona, por continente

En la Semana 3 viste que `Generosidad` vs. `Puntaje` da un r general casi
nulo. Esta celda repite el patron de arriba (filtra + `.corr()`) para
`Generosidad` vs. `Puntaje`, calculado por separado **dentro de Europa** y
**dentro de América**.
"""))
s4.append(code("nb4l-seccionc-ex8-code", """\
# 👀 OBSERVA
df_europa = df_felicidad[df_felicidad['Continente'] == 'Europa']
r_generosidad_europa = df_europa['Generosidad'].corr(df_europa['Puntaje'])

df_america = df_felicidad[df_felicidad['Continente'] == 'América']
r_generosidad_america = df_america['Generosidad'].corr(df_america['Puntaje'])

print(f"r (Generosidad vs. Puntaje) en Europa  = {r_generosidad_europa:.3f}")
print(f"r (Generosidad vs. Puntaje) en América = {r_generosidad_america:.3f}")"""))

s4.append(md("nb4l-seccionc-reflexiona-md", """\
#### 💭 Reflexiona (respuesta abierta -- calificada por IA, +5 XP)

El r general de `Generosidad` vs. `Puntaje` era casi 0. Pero acabas de ver
que dentro de Europa es positivo, y dentro de América es negativo. En 2-3
oraciones: ¿que te dice esto sobre confiar en "el patron general" de todo un
dataset sin mirar los subgrupos?
"""))
s4.append(reflexion_check("nb4l-seccionc-reflexiona-code", "subgrupos"))

# ─── Mini-Proyecto (rediseñado: 🧩 COMPLETA, sin escribir el calculo) ──
s4.append(md("nb4l-miniproyecto-header", """\
---
## 🔍 Mini-Proyecto -- Encuentra tu Propio Patron

Ya viste ocho pares distintos hoy y la Semana pasada, todos elegidos por el
curso. Ahora te toca a ti: explora **todas** las combinaciones posibles
entre las 7 columnas numericas del dataset (no solo contra `Puntaje`) y
elige un par que **no hayas usado ya** en ninguna ronda anterior.

**Este hallazgo es tu material de entrada para la Semana 5** -- vas a
defenderlo (o a que te lo cuestionen) la proxima clase, asi que elige algo
que realmente te parezca interesante.
"""))

s4.append(code("nb4l-miniproyecto-matriz", """\
# 👀 OBSERVA: la matriz completa de correlaciones entre TODAS las columnas numericas
df_felicidad.corr(numeric_only=True)"""))

s4.append(md("nb4l-miniproyecto-ej-md", """\
#### 🧩 Integracion 1 -- Tu hallazgo (15 pts)

Elige un par de columnas de la matriz de arriba que **no** hayas usado en
ninguna ronda de Semana 3 o Semana 4 (revisa: ya se usaron
Corrupción-Puntaje, Esperanza-Puntaje, Apoyo social-Puntaje,
Libertad-Puntaje, Generosidad-Puntaje, PBI-Puntaje, PBI-Esperanza, Apoyo
social-Esperanza, Libertad-Corrupción, PBI-Generosidad). Completa
`mini_var_x` y `mini_var_y` copiando el nombre **exacto** de la columna tal
como aparece en la matriz, y escribe una hipotesis: ¿por que crees que esas
dos variables podrian estar relacionadas? No alcanza con reportar el numero
mas alto que encontraste -- necesitas una razon.

El calculo de tu `r` ya viene escrito en la celda -- solo completa los tres
espacios en blanco.
"""))
s4.append(code("nb4l-miniproyecto-code", """\
# 🧩 COMPLETA: reemplaza cada ___ por tu propia eleccion
mini_var_x = "___"       # copia el nombre EXACTO de una columna de la matriz de arriba
mini_var_y = "___"       # copia el nombre EXACTO de otra columna distinta
mini_hipotesis = "___"   # tu hipotesis, en una oracion

mini_r = df_felicidad[mini_var_x].corr(df_felicidad[mini_var_y])
print(f"{mini_var_x} vs. {mini_var_y} -> r = {mini_r:.3f}")
print(f"Hipotesis: {mini_hipotesis}")"""))
s4.append(code("nb4l-miniproyecto-check", "grader.check_intex1()"))

s4.append(md("nb4l-miniproyecto-reflexiona1-md", """\
#### 💭 Reflexiona -- interpreta tu hallazgo (respuesta abierta -- calificada por IA, +5 XP)

Mira el resultado que se imprimio arriba (tus dos variables y tu r). Sin usar
la palabra "causa" ni ninguna variante: ¿que te dice ese r sobre la relacion
entre tus dos variables? ¿Y que es lo que **no** te dice?
"""))
s4.append(reflexion_check("nb4l-miniproyecto-reflexiona1-code", "interpretacion"))

s4.append(md("nb4l-miniproyecto-reflexiona2-md", """\
#### 💭 Reflexiona -- piensa en el metodo (respuesta abierta -- calificada por IA, +5 XP)

Miraste una matriz con muchisimos pares posibles y elegiste uno. Si hubieras
probado 20 pares al azar, es esperable que **alguno** salga con un r alto
solo por casualidad. En 2-3 oraciones: ¿por que no deberias confiar
automaticamente en "el par con el r mas alto que encontre" solo porque salio
alto?
"""))
s4.append(reflexion_check("nb4l-miniproyecto-reflexiona2-code", "metodologica"))

s4.append(code("nb4l-checkpoint-c", """\
# ✅ CHECKPOINT -- necesitas 80% en esta seccion para continuar
grader.check_mini_c()"""))

s4.append(md("nb4l-cierre", """\
---
## 🏁 Fin de la Mision 2 -- Semanas 3-4

Aprendiste a leer un patron, a reconocer el numero que lo acompaña, a
desconfiar de ese numero cuando corresponde, y a encontrar tu propio patron
en datos que nadie te guio. Guarda tu par de variables, tu r, y tu hipotesis
del mini-proyecto -- la **Semana 5** va a poner a prueba exactamente eso.
"""))
s4.append(code("nb4l-resumen", "grader.resumen()"))


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

write_notebook(s4, "nb4_lite_correlacion.ipynb")

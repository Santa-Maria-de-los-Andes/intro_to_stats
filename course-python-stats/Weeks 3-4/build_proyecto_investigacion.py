# -*- coding: utf-8 -*-
"""
build_proyecto_investigacion.py -- Genera proyecto_investigacion.ipynb,
Semana 4 -> Semana 5 de Mision 2: Buscando Patrones.

Creado 2026-08-29 (decision del usuario): reemplaza el Mini-Proyecto de
integracion que se elimino de nb4_correlacion.ipynb (ver build_nb4.py y
autograder_nb4.py, "RECORTE 2026-08-29"). En vez de elegir un par dentro del
dataset del curso (World Happiness 2019), cada pareja/estudiante elige su
propio dataset real y arma un hallazgo de verdad, con supervision en clase
esta semana y presentacion la semana que viene -- esa presentacion abre la
Semana 5 (causalidad).

A diferencia de nb1/nb3/nb4: este notebook NO tiene autograder, NO llama
`grader.check_*()`, NO manda nada a Supabase. Es la excepcion documentada en
WORKFORCE_CONTRACT.md SS4 (el capstone de Semana 8 es "rubric-graded, not
check_*-graded") aplicada en miniatura aca -- calificacion humana por
rubrica al final del notebook, no XP automatico. Mismos helpers (`md`/`code`)
y misma leyenda de iconos que build_nb4.py, duplicados a proposito
(COURSE_TEMPLATE.md SS3: cada build_nbN.py es autocontenido).

Continuidad con la Semana 5 (reemplaza la nota que antes vivia en
check_intex1 / ATLAS_spec_nb3_nb4.md): el par de variables, el r, la
hipotesis y la respuesta al aviso de confusion ("Antes de Presentar") que el
estudiante escribe aca son el material de entrada de la Semana 5 -- quien
diseñe esa semana debe leer esto directamente, no reconstruirlo desde nb4.

PENDIENTE (marcado explicitamente en el notebook, celda "proy-elige-dataset"):
el menu real de datasets/afirmaciones lo define el usuario por separado --
esta celda queda como placeholder TODO. Antes de usarlo en clase, reemplazar
el placeholder y verificar el r real de cada par candidato (no publicar un
numero sin verificar contra el dataset real, misma regla que el resto del
curso).
"""
import json

def md(cell_id, source):
    return {"cell_type": "markdown", "id": cell_id, "metadata": {}, "source": source}

def code(cell_id, source):
    return {"cell_type": "code", "id": cell_id, "metadata": {}, "source": source,
            "outputs": [], "execution_count": None}

LEYENDA_ICONOS = """\
### Leyenda de iconos

| Icono | Accion | Que significa |
|---|---|---|
| 👀 | **OBSERVA** | Ejecuta y observa -- no cambies nada |
| 🔮 | **PREDICE** | Escribe tu prediccion *antes* de ejecutar |
| 🧩 | **COMPLETA** | Reemplaza `___` por el valor correcto |
| 🔨 | **CONSTRUYE** | Escribe codigo desde cero |
| ✍️ | **ESCRIBE** | Respuesta abierta -- edita esta celda de markdown y escribe tu respuesta |

---
"""

p = []

# ─── Apertura ─────────────────────────────────────────────────────────
p.append(md("proy-titulo", """\
# Proyecto de Investigación
### Tu propio dataset, tu propio hallazgo

Ya aprendiste a leer un patrón con el ojo, a ponerle un número exacto
(`.corr()`), a desconfiar de ese número (muestras chicas, correlación no es
causalidad), y a revisar si el patrón general se sostiene por subgrupo.

Ahora te toca aplicar todo eso solo -- vas a elegir un dataset real, una
afirmación que quieras poner a prueba, y vas a construir el hallazgo de
punta a punta. **Esto es lo que vas a presentar y defender la próxima
clase** -- esa presentación abre la Semana 5.
"""))

p.append(md("proy-leyenda", LEYENDA_ICONOS))

p.append(md("proy-instrucciones", """\
## 🗂️ Cómo funciona

- Trabajas en pareja (o solo, si tu grupo así lo decide).
- **Hoy en clase:** eliges dataset y afirmación, cargas los datos, y arrancas
  el análisis con el profesor circulando para ayudarte.
- **De tarea:** terminas el análisis, escribes tu hipótesis y tu reflexión,
  y preparas tu presentación (2-3 minutos).
- **La próxima clase:** presentas. Nada de esto se autocalifica -- tu
  profesor lo revisa con la rúbrica al final de este notebook.
"""))

p.append(code("proy-setup", """\
import pandas as pd
import matplotlib.pyplot as plt

print("Listo -- ahora carga tu dataset en la siguiente celda.")"""))

# ─── Elige tu dataset ───────────────────────────────────────────────────
p.append(md("proy-elige-dataset-md", """\
---
## 1️⃣ Elige tu dataset y tu afirmación

🚧 **TODO (profesor):** reemplaza esta tabla por el menú real de
afirmaciones/datasets antes de usar este notebook en clase. Cada fila debe
traer: la afirmación en una oración, el nombre/forma de cargar el dataset,
el par de columnas numéricas a usar, y (opcional) una columna categórica
para repetir el chequeo por subgrupo de la Sección C de la Semana 4.

| Afirmación | Dataset | Par de columnas | Columna de subgrupo (opcional) |
|---|---|---|---|
| _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ |
| _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ |
| _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ |
| _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ |

¿Tienes una idea propia que no está en la tabla? Puedes proponer tu propio
dataset y afirmación -- pídele el visto bueno a tu profesor antes de
arrancar.
"""))

p.append(code("proy-carga-code", """\
# 🧩 COMPLETA: carga tu dataset en un DataFrame llamado `df`
# (via pd.read_csv(), sns.load_dataset(), o la forma que tu profesor indique)

df = ___

df.head()"""))

# ─── Exploración ────────────────────────────────────────────────────────
p.append(md("proy-exploracion-md", """\
---
## 2️⃣ Explora antes de calcular nada

👀 Igual que en tu primera misión: `.info()` y `.describe()` antes de tocar
`.corr()`. ¿Cuántas filas tiene? ¿Hay columnas con datos faltantes? ¿Qué
rango tienen tus dos columnas de interés?
"""))
p.append(code("proy-exploracion-code", """\
# 👀 OBSERVA / 🔨 CONSTRUYE
df.info()
df.describe()"""))

# ─── Predicción + scatter ───────────────────────────────────────────────
p.append(md("proy-prediccion-md", """\
---
## 3️⃣ Predice antes de graficar

🔮 Antes de ejecutar nada: para tu par de columnas, ¿esperas un patrón
fuerte o débil? ¿Positivo o negativo? Escribe tu predicción en 1 oración
**antes** de correr la celda de abajo.
"""))
p.append(md("proy-prediccion-respuesta", """\
✍️ **Tu predicción:** _(edita esta celda y escribe aquí)_
"""))

p.append(md("proy-scatter-md", """\
🔨 Ahora construye el scatter de tu par de columnas.
"""))
p.append(code("proy-scatter-code", """\
# 🔨 CONSTRUYE
plt.scatter(df[___], df[___])
plt.xlabel(___)
plt.ylabel(___)
plt.show()"""))

# ─── Cálculo ─────────────────────────────────────────────────────────
p.append(md("proy-corr-md", """\
---
## 4️⃣ Ponle un número: `.corr()`

🔨 Calcula el coeficiente de correlación de tu par. ¿Tu ojo (predicción de
arriba) acertó?
"""))
p.append(code("proy-corr-code", """\
# 🔨 CONSTRUYE
r = df[___].corr(df[___])
print(f"r = {r:.3f}")"""))

# ─── Subgrupo (opcional) ────────────────────────────────────────────────
p.append(md("proy-subgrupo-md", """\
---
## 5️⃣ (Opcional) ¿Se sostiene por subgrupo?

Si tu dataset tiene una columna categórica, repite exactamente el patrón de
la Sección C de la Semana 4: filtra por categoría, calcula `.corr()` sobre
el subconjunto. ¿El patrón general se sostiene, se debilita, o cambia de
signo dentro de algún subgrupo? (Recuerda la trampa de Oceanía: si un
subgrupo tiene muy pocas filas, no confíes en su r por más alto que salga.)
"""))
p.append(code("proy-subgrupo-code", """\
# 🔨 CONSTRUYE (opcional -- borra esta celda si tu dataset no tiene columna categórica)
df_subgrupo = df[df[___] == ___]
r_subgrupo = df_subgrupo[___].corr(df_subgrupo[___])
print(f"r dentro de este subgrupo = {r_subgrupo:.3f}  (n={len(df_subgrupo)})")"""))

# ─── Hipótesis ───────────────────────────────────────────────────────
p.append(md("proy-hipotesis-md", """\
---
## 6️⃣ Tu hipótesis

✍️ No alcanza con reportar el r. Escribe **una hipótesis**: ¿por qué crees
que estas dos variables podrían estar relacionadas? Da una razón real, no
solo el número.
"""))
p.append(md("proy-hipotesis-respuesta", """\
✍️ **Tu hipótesis:** _(edita esta celda y escribe aquí, mínimo 2 oraciones)_
"""))

# ─── Reflexión anti-p-hacking ───────────────────────────────────────────
p.append(md("proy-reflexion-metodo-md", """\
---
## 7️⃣ Antes de presentar: dos preguntas incómodas

✍️ **Pregunta 1.** Si hubieras probado varios pares de columnas antes de
quedarte con este, es esperable que alguno diera un r alto solo por
casualidad. ¿Por qué no deberías confiar automáticamente en "el par con el r
más alto que encontré" solo porque salió alto?

✍️ **Pregunta 2.** Nombra **una cosa distinta** a "una variable causa la
otra" que podría explicar el patrón que encontraste (por ejemplo: ambas
variables podrían estar conectadas con una tercera cosa que no mediste).
No hace falta que sea la explicación correcta -- solo que sea plausible.
"""))
p.append(md("proy-reflexion-metodo-respuesta", """\
✍️ **Tus respuestas:** _(edita esta celda y escribe aquí)_

1.
2.
"""))

# ─── Preparación de la presentación ─────────────────────────────────────
p.append(md("proy-presentacion-md", """\
---
## 8️⃣ Prepara tu presentación (2-3 minutos)

Tu presentación debe incluir, en este orden:

1. Tu afirmación y tu dataset (¿de dónde salen los datos?).
2. Tu scatter y tu r.
3. Tu hipótesis (con razón, no solo el número).
4. Tu respuesta a la Pregunta 2 de arriba -- una explicación alternativa a
   "X causa Y".

No hace falta un slide elaborado -- el notebook mismo, o una hoja con estos
cuatro puntos, alcanza.
"""))

# ─── Rúbrica ─────────────────────────────────────────────────────────
p.append(md("proy-rubrica-md", """\
---
## 📋 Rúbrica (la completa tu profesor)

Este proyecto no se autocalifica -- tu profesor lo revisa con esta rúbrica,
la misma que vas a volver a ver en el capstone de fin de bimestre.

| Criterio | Puntos | Nota del profesor |
|---|---|---|
| Calidad del dataset + pregunta de investigación | 15 | |
| Análisis descriptivo con interpretación (`.info()`/`.describe()`) | 20 | |
| Análisis de correlación + hipótesis con crítica de causalidad | 20 | |
| Calidad de la visualización (scatter) | 20 | |
| Claridad de la presentación | 10 | |
| **Total** | **85** | |
"""))

p.append(md("proy-cierre", """\
---
## 🏁 Guarda todo esto

Tu par de variables, tu r, tu hipótesis, y tu respuesta a la Pregunta 2 son
el material que vas a defender (y que te van a cuestionar) la próxima
clase. Eso es la Semana 5.
"""))


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

write_notebook(p, "proyecto_investigacion.ipynb")

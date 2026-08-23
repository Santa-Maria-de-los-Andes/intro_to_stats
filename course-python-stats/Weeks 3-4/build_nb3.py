# -*- coding: utf-8 -*-
"""
build_nb3.py -- Genera nb3_correlacion.ipynb (Semana 3 / Clase 1 de la
Mision 2: Buscando Patrones -- nombre placeholder, pendiente PIXEL ticket #2).

RENOMBRADO 2026-08-20 (decision explicita del usuario, SUPERA la convencion
"un script genera dos notebooks del mismo nb-prefijo" que nb1_semana1/
nb1_semana2 usan): hasta hoy este archivo generaba nb3_semana3_correlacion.ipynb
Y nb3_semana4_correlacion.ipynb desde un solo script. El usuario pidio
renombrar los dos notebooks a "nb3" y "nb4" respectivamente -- cada semana de
esta unidad ahora es su propio nb-prefijo top-level, no una sub-sesion
compartiendo el prefijo "nb3". Este script quedo solo con la Semana 3;
Semana 4 vive en `build_nb4.py`, hermano de este archivo, mismos helpers
duplicados (mismo criterio que cada build_nbN.py es autocontenido, no importa
de otro build script).

⚠️ Nota de numeracion (no cambio con este rename, solo el nombre de archivo):
check_ex/check_debug/check_tN de nb4 SIGUEN la numeracion global desde donde
nb3 termina (ex1-4/t1-7 en nb3, ex5-8/t8-10/debug1/intex1 en nb4) -- las dos
narrativamente siguen siendo "Mision 2" en dos clases, aunque ya no compartan
nb-prefijo de archivo. Ver `ATLAS_spec_nb3_nb4.md` para el detalle completo
que ATLAS necesita.

⚠️ Nota de convencion nb-prefijo (hereda la de la version anterior, sigue
aplicando): "nb3" ya rompia la convencion documentada en
WORKFORCE_HANDOFF.md/supabase_schema.sql (nb2 = Tarea 2 = Correlacion, nb3
reservado para Regresion/Clustering Semanas 6-7) por decision explicita del
usuario 2026-08-14. Ahora que Semana 4 tambien reclama su propio prefijo
("nb4"), lo que sea que Semanas 6-7 (Regresion/Clustering) iba a llamarse
("nb3" en el esquema original) probablemente necesite correrse a "nb5" --
no es bloqueante para este archivo, pero quien diseñe Semanas 6-7 debe
confirmarlo antes de nombrar ese build script.

Cubre Apertura + Teoria Desbloqueada + Grafica y Calcula (fusion de las
Secciones A/B originales), segun la reestructuracion 2026-08-20 documentada
en WORKFORCE_HANDOFF.md (resuelve ticket #13) y WORKFORCE_CONTRACT.md SS2.

2026-08-21: ampliado a pedido del usuario tras revisar la clase ("nb3 es
muy corto") -- Ronda 5 (PBI vs. Apoyo social) y Ronda 6 (Generosidad vs.
Percepcion de corrupcion) se agregaron despues de Ronda 4, cada una con su
propia celda 💭 Reflexiona; y un "Quiz de Cierre" de 4 preguntas de opcion
multiple (t8-t11) se agrego antes del checkpoint -- 1 pregunta de recordar
el r mas fuerte del dia + 3 escenarios nuevos, sin relacion con el dataset
de felicidad, que ponen a prueba si el concepto de correlacion-no-es-
causalidad se transfiere a contextos distintos. Ver autograder_nb3.py
docstring para el detalle de puntaje y ATLAS_spec_nb3_nb4.md para la nota
sobre por que t8-t11/ex5-ex6 son numeracion local a este archivo (no
continuan la convencion "nb4 sigue desde donde nb3 termina").

Fuente de contenido:
  - Teoria_Semanas3-4_Mision2_Correlacion.md (SS0 Apertura, SS1 Teoria
    Desbloqueada, SS2 Seccion A / Seccion B)
  - 2019_es.csv (World Happiness Report 2019, 156 filas x 10 columnas, SIN
    valores nulos) -- todos los numeros de este notebook se recalcularon
    directamente contra el CSV real 2026-08-20 (ver WORKFORCE_HANDOFF.md
    Done log de esa fecha para el detalle de validacion); los pares de la
    Ronda 5/Ronda 6 y los escenarios del Quiz de Cierre se verificaron de
    la misma forma el 2026-08-21.

Convenciones: check_tN = una celda, grader.check_tN(); check_exN 🔨
CONSTRUYE = sin solucion escrita; celdas 🔮 PREDICE = ungraded,
contract-exempt (WORKFORCE_CONTRACT.md SS3); celdas 💭 Reflexiona =
calificadas por IA via `grade-reflexion` (Supabase Edge Function ->
DeepSeek), +5 XP c/u, patron `reflexion_check()` abajo.
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

s3.append(md("nb3-titulo", f"""\
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

s3.append(code("nb3-setup", """\
# Carga el autograder y el dataset de esta leccion
!wget -q "https://raw.githubusercontent.com/Santa-Maria-de-los-Andes/intro_to_stats/main/course-python-stats/Weeks%203-4/autograder_nb3.py"
!wget -q "https://raw.githubusercontent.com/Santa-Maria-de-los-Andes/intro_to_stats/main/course-python-stats/Weeks%203-4/2019_es.csv"
from autograder_nb3 import Autograder
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

# ─── Apertura ─────────────────────────────────────────────────────────────
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

# ─── Teoria Desbloqueada ────────────────────────────────────────────────
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

# ─── Grafica y Calcula (fusion Seccion A + Seccion B) ────────────────────
s3.append(md("nb3-graficaycalcula-header", """\
---
## 📈🔢 Grafica y Calcula

Hoy graficas y calculas en el mismo paso -- ya sabes leer un patron con el
ojo (Apertura) y ya sabes que significa `r` (Teoria Desbloqueada). El patron
completo que vas a repetir toda la clase:

```python
plt.scatter(df['columna_x'], df['columna_y'])
plt.xlabel('columna_x')
plt.ylabel('columna_y')
plt.show()

r = df['columna_x'].corr(df['columna_y'])
print(f"r = {r:.3f}")
```
"""))

s3.append(code("nb3-guiado", """\
# 👀 OBSERVA: el patron completo, de una vez -- Apoyo social vs. Puntaje
plt.scatter(df_felicidad['Apoyo social'], df_felicidad['Puntaje'], alpha=0.6)
plt.xlabel('Apoyo social')
plt.ylabel('Puntaje')
plt.title('Apoyo social vs. Puntaje de felicidad')
plt.show()

r_apoyo_social = df_felicidad['Apoyo social'].corr(df_felicidad['Puntaje'])
print(f"r (Apoyo social vs. Puntaje) = {r_apoyo_social:.3f}")"""))

s3.append(md("nb3-outlier-md", """\
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

s3.append(teoria_check("nb3-t6-check", 6))

s3.append(md("nb3-repeticion-md", """\
### 🔁 Practica repetida: mismo patron, distintos pares

Seis rondas, mismo patron de siempre (`plt.scatter()` + `.corr()`, ahora
en un solo ejercicio). No todas las rondas piden reflexion escrita -- las
que si la piden son las que valen la pena pausar; en las demas, sigue de
largo apenas veas tu numero.
"""))

# Ronda 1 -- reflexiona
s3.append(md("nb3-ronda1-predice-md", """\
#### Ronda 1 -- Antes de seguir, predice

Mirando el patron guiado de arriba (Apoyo social vs. Puntaje): ¿te parece un
patron fuerte o debil? ¿positivo o negativo? Ahora, **sin graficar
todavia**, predice lo mismo para un par nuevo: `Percepción de corrupción`
vs. `Puntaje`.
"""))
s3.append(code("nb3-ronda1-predice-code", """\
# 🔮 PREDICE (no se califica, es solo para ti)
mi_prediccion_ronda1 = "___"  # ej: "creo que es un patron debil y positivo\""""))

s3.append(md("nb3-ronda1-ej-md", """\
#### ✅ Ejercicio 1 -- Grafica y calcula (20 pts)

🔨 Repite el patron completo (scatter + `.corr()`) con `Percepción de
corrupción` en el eje X y `Puntaje` en el eje Y. Incluye `plt.xlabel()` e
`plt.ylabel()`.

Variables que espera el autograder: `x_ex1`, `y_ex1` (columnas del scatter),
`r_ex1` (el coeficiente de correlacion entre ambas).
"""))
s3.append(code("nb3-ronda1-code", """\
# 🔨 CONSTRUYE

# ============================
#      Tu codigo aqui
# ============================


"""))
s3.append(code("nb3-ronda1-check", "grader.check_ex1()"))

s3.append(md("nb3-ronda1-reflexiona-md", """\
#### 💭 Reflexiona -- Ronda 1 (respuesta abierta -- calificada por IA, +5 XP)

En una frase: ¿tu ojo acerto en fuerza y direccion para `Percepción de
corrupción`, o te sorprendio algo del resultado?
"""))
s3.append(reflexion_check("nb3-ronda1-reflexiona-code", "ronda1"))

# Ronda 2 -- sin reflexion
s3.append(md("nb3-ronda2-predice-md", """\
#### Ronda 2 -- Antes de seguir, predice

Misma mecanica, tercera columna: **sin graficar todavia**, predice si
`Esperanza de vida saludable` vs. `Puntaje` te parece un patron fuerte o
debil, positivo o negativo.
"""))
s3.append(code("nb3-ronda2-predice-code", """\
# 🔮 PREDICE (no se califica, es solo para ti)
mi_prediccion_ronda2 = "___"  # ej: "creo que es un patron fuerte y positivo\""""))

s3.append(md("nb3-ronda2-ej-md", """\
#### ✅ Ejercicio 2 -- Grafica y calcula, otra vez (20 pts)

🔨 Mismo patron completo, ahora con `Esperanza de vida saludable` en el eje X
y `Puntaje` en el eje Y.

Variables que espera el autograder: `x_ex2`, `y_ex2`, `r_ex2`.
"""))
s3.append(code("nb3-ronda2-code", """\
# 🔨 CONSTRUYE

# ============================
#      Tu codigo aqui
# ============================


"""))
s3.append(code("nb3-ronda2-check", "grader.check_ex2()"))

s3.append(teoria_check("nb3-t7-check", 7))

# Ronda 3 -- reflexiona
s3.append(md("nb3-ronda3-md", """\
#### Ronda 3 -- PBI per cápita vs. Esperanza de vida saludable

Esta vez ninguna de las dos columnas es `Puntaje` -- las seis variables
economicas y sociales tambien pueden relacionarse **entre si**.
"""))
s3.append(md("nb3-ronda3-ej-md", """\
##### ✅ Ejercicio 3 -- Grafica y calcula (20 pts)

🔨 `PBI per cápita` (eje X) vs. `Esperanza de vida saludable` (eje Y).

Variables que espera el autograder: `x_ex3`, `y_ex3`, `r_ex3`.
"""))
s3.append(code("nb3-ronda3-code", """\
# 🔨 CONSTRUYE

# ============================
#      Tu codigo aqui
# ============================


"""))
s3.append(code("nb3-ronda3-check", "grader.check_ex3()"))

s3.append(md("nb3-ronda3-reflexiona-md", """\
##### 💭 Reflexiona -- Ronda 3 (respuesta abierta -- calificada por IA, +5 XP)

`PBI per cápita` y `Esperanza de vida saludable` te deberia haber dado el r
mas alto que has visto hoy (mas alto incluso que cualquiera de los dos contra
`Puntaje`). ¿Por que crees que estas dos variables en particular se mueven
tan juntas?
"""))
s3.append(reflexion_check("nb3-ronda3-reflexiona-code", "ronda3"))

# Ronda 4 -- sin reflexion
s3.append(md("nb3-ronda4-md", """\
#### Ronda 4 -- Apoyo social vs. Esperanza de vida saludable

Mismo patron, otro par sin `Puntaje`.
"""))
s3.append(md("nb3-ronda4-ej-md", """\
##### ✅ Ejercicio 4 -- Grafica y calcula (20 pts)

🔨 `Apoyo social` (eje X) vs. `Esperanza de vida saludable` (eje Y).

Variables que espera el autograder: `x_ex4`, `y_ex4`, `r_ex4`.
"""))
s3.append(code("nb3-ronda4-code", """\
# 🔨 CONSTRUYE

# ============================
#      Tu codigo aqui
# ============================


"""))
s3.append(code("nb3-ronda4-check", "grader.check_ex4()"))

# Ronda 5 -- reflexiona (2026-08-21: notebook ampliado, ver build_nb3.py
# docstring / autograder_nb3.py docstring / ATLAS_spec_nb3_nb4.md)
s3.append(md("nb3-ronda5-md", """\
#### Ronda 5 -- PBI per cápita vs. Apoyo social

`PBI per cápita` ya te dio el r más alto de la Ronda 3 (con `Esperanza de
vida saludable`). Repite el patron con otra variable distinta -- otra vez,
ninguna de las dos es `Puntaje`.
"""))
s3.append(md("nb3-ronda5-ej-md", """\
##### ✅ Ejercicio 5 -- Grafica y calcula (20 pts)

🔨 `PBI per cápita` (eje X) vs. `Apoyo social` (eje Y).

Variables que espera el autograder: `x_ex5`, `y_ex5`, `r_ex5`.
"""))
s3.append(code("nb3-ronda5-code", """\
# 🔨 CONSTRUYE

# ============================
#      Tu codigo aqui
# ============================


"""))
s3.append(code("nb3-ronda5-check", "grader.check_ex5()"))

s3.append(md("nb3-ronda5-reflexiona-md", """\
##### 💭 Reflexiona -- Ronda 5 (respuesta abierta -- calificada por IA, +5 XP)

`PBI per cápita` te volvio a dar un r fuerte, esta vez con `Apoyo social`.
En 1-2 oraciones: ¿que tienen en comun estas dos relaciones fuertes que
calculaste hoy, y te parece razonable que el PBI se relacione
consistentemente fuerte con variables tan distintas?
"""))
s3.append(reflexion_check("nb3-ronda5-reflexiona-code", "pbi_apoyo"))

# Ronda 6 -- reflexiona
s3.append(md("nb3-ronda6-md", """\
#### Ronda 6 -- Generosidad vs. Percepción de corrupción

Hasta ahora, `Generosidad` casi no se relaciono con nada (r≈0.08 con
`Puntaje` en la Apertura). Prueba si pasa lo mismo con `Percepción de
corrupción`.
"""))
s3.append(md("nb3-ronda6-ej-md", """\
##### ✅ Ejercicio 6 -- Grafica y calcula (20 pts)

🔨 `Generosidad` (eje X) vs. `Percepción de corrupción` (eje Y).

Variables que espera el autograder: `x_ex6`, `y_ex6`, `r_ex6`.
"""))
s3.append(code("nb3-ronda6-code", """\
# 🔨 CONSTRUYE

# ============================
#      Tu codigo aqui
# ============================


"""))
s3.append(code("nb3-ronda6-check", "grader.check_ex6()"))

s3.append(md("nb3-ronda6-reflexiona-md", """\
##### 💭 Reflexiona -- Ronda 6 (respuesta abierta -- calificada por IA, +5 XP)

`Generosidad` te dio un r cercano a 0 con casi todo lo que probaste hoy --
pero aqui ya no es tan chico. En 1-2 oraciones: ¿te parece razonable que
`Generosidad` casi no se relacione con nada mas, excepto con esta variable?
¿Que explicacion se te ocurre?
"""))
s3.append(reflexion_check("nb3-ronda6-reflexiona-code", "generosidad_corrupcion"))

# Chequeo de concepto -- reflexiona
s3.append(md("nb3-concepto-md", """\
### 🧠 Chequeo de concepto

Ya calculaste `r` ocho veces hoy (Apertura + seis Rondas + el ejemplo
guiado). Antes de cerrar la clase, pon el concepto en tus propias palabras
-- sin usar ningun dataset ni numero especifico.
"""))
s3.append(md("nb3-concepto-reflexiona-md", """\
#### 💭 Reflexiona -- explica el concepto (respuesta abierta -- calificada por IA, +5 XP)

En 2-3 oraciones, sin usar ningun par de columnas como ejemplo: ¿que te dice
el coeficiente de correlacion, y que es lo que **nunca** te dice por si
solo?
"""))
s3.append(reflexion_check("nb3-concepto-reflexiona-code", "concepto"))

# ─── Quiz de Cierre ───────────────────────────────────────────────────────
s3.append(md("nb3-quiz-header", """\
---
## 🧭 Quiz de Cierre

Ya calculaste seis correlaciones reales hoy. Antes de cerrar: una pregunta
para recordar lo que viste en esta clase, y tres preguntas con ejemplos
**nuevos** -- para probar si el concepto de correlacion se te quedo mas
alla del dataset de felicidad.
"""))

s3.append(teoria_check("nb3-t8-check", 8))
s3.append(teoria_check("nb3-t9-check", 9))
s3.append(teoria_check("nb3-t10-check", 10))
s3.append(teoria_check("nb3-t11-check", 11))

s3.append(code("nb3-checkpoint", """\
# ✅ CHECKPOINT -- necesitas 80% en esta seccion para continuar
grader.check_mini_a()"""))

s3.append(md("nb3-cierre", """\
---
## 🏁 Fin de la Clase 1 -- Semana 3

Aprendiste a leer un patron con el ojo, a ponerle un numero exacto en el
mismo paso, y a desconfiar de ese numero cuando corresponde. La **Semana 4**
continua la Mision 2: vas a descubrir que el patron general puede esconder --
o hasta invertir -- lo que pasa dentro de cada grupo, y vas a elegir tu propio
par de variables para un mini-proyecto.
"""))
s3.append(code("nb3-resumen", "grader.resumen()"))


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

write_notebook(s3, "nb3_correlacion.ipynb")

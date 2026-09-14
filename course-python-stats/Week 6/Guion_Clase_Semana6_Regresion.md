# Guion de Clase — Semana 6: "El Oráculo de Datos"
## Regresión Lineal (introducción a Machine Learning)

**Autoras:** SOFIA (secuencia pedagógica) + GAUSS (revisión de exactitud estadística)
**Audiencia:** 3°–5° secundaria, 15–17 años
**Duración:** ~45 min de clase magistral, seguida de `nb5_regresion.ipynb` (ya construido) para la práctica
**Requisito previo:** Semana 3–4 (correlación) — esta clase abre citando directamente ese hallazgo

**Objetivo de la sesión:** que el estudiante pueda decir *cuándo* usaría una regresión y *qué significa*
un resultado ya ajustado (línea, R², coeficientes) — **no** que derive la matemática. Esto es
exposición y aplicación, no teoría (`Bimestre3_Statistics_Python_Module_Guide.md`, no-goal explícito).

---

## Antes de empezar

- **No proyectar el notebook todavía.** Esta clase es deliberadamente de pizarra/slides — el
  notebook (`nb5_regresion.ipynb`) repite varios de estos mismos conceptos en texto, así que abrirlo
  antes de tiempo le quita sorpresa a la práctica. Ábrelo recién en el último bloque.
- Ten a mano (proyectado o en tarjetas) la tabla de países del Gancho — está más abajo, con
  valores reales del dataset (`2019_es.csv`) que ya usaron en la Semana 3–4.
- Pizarra libre para dibujar una nube de puntos a mano — el dibujo en vivo importa más que un
  gráfico ya hecho para el Concepto 1.

---

## Línea de tiempo

| Bloque | Min | Contenido |
|---|---|---|
| 1. Gancho — Duelo de Oráculos | 8 | Predicción intuitiva en vivo vs. dato real |
| 2. Concepto 1 — La línea de mejor ajuste | 8 | Qué hace `.fit()`, por qué no pasa por todos los puntos |
| 3. Concepto 2 — R² | 10 | Qué porcentaje de la variación explica el modelo |
| 4. Concepto 3 — Train/test split | 8 | Por qué no calificas con las respuestas que ya viste |
| 5. Concepto 4 — Interpretar coeficientes | 8 | "Por cada unidad extra de X, Y cambia en ___" |
| 6. Cierre y transición al notebook | 3 | Tease de "míralo romperse" (extrapolación) |

Si el tiempo aprieta, el bloque 6 es el más comprimible (es un tráiler, no contenido nuevo) — no
comprimas el bloque 3, es donde más se confunden.

---

## 1. Gancho — "Duelo de Oráculos: Tú vs. la Máquina" (8 min)

**Antes de cualquier fórmula.** Empieza recordando el cliffhanger de Misión 2:

> "En la Misión 2 encontraron que el PBI per cápita de un país y su Puntaje de felicidad tienen
> una correlación fuerte, r ≈ 0.794 — se mueven juntos. Hoy van a construir una herramienta que
> usa eso para predecir. Antes de que lo haga la máquina, lo van a hacer ustedes."

Proyecta o reparte esta tabla (valores reales, `2019_es.csv`):

| País | PBI per cápita | Puntaje de felicidad |
|---|---|---|
| Finlandia | 1.340 | 7.769 |
| Estados Unidos | 1.433 | 6.892 |
| España | 1.286 | 6.354 |
| México | 1.070 | 6.595 |
| Chile | 1.159 | 6.444 |
| Argentina | 1.092 | 6.086 |
| Japón | 1.327 | 5.886 |

**No reveles todavía la fila de Perú.** Solo el dato de PBI:

> **Perú — PBI per cápita: 0.960 — Puntaje: ¿? 🔮**

Dales 60–90 segundos en parejas para escribir su predicción del Puntaje de Perú, usando solo el
patrón de la tabla (nada de buscarlo en el celular). Pide 3–4 voluntarios que digan su número en
voz alta y anótalos en la pizarra.

**Antes de revelar el dato real**, señala el caso de Japón: PBI casi idéntico a Finlandia (1.327
vs. 1.340) pero un Puntaje casi dos puntos más bajo (5.886 vs. 7.769). Pregunta: *"¿esto significa
que el patrón no sirve, o que el patrón no es perfecto?"* — deja la pregunta abierta, no la
respondas todavía; es la semilla del Concepto 2 (R²).

**Revela:** Perú, Puntaje real = **5.697**.

> "Ninguno de ustedes tenía una fórmula — usaron intuición sobre un patrón. Eso es exactamente lo
> que va a hacer el modelo de hoy, con la diferencia de que en vez de intuición usa matemática
> exacta, y en vez de una tabla de 7 países usa los 156 completos. A esa herramienta la van a
> llamar su **oráculo**."

*Por qué esta apertura funciona:* no inventa un ejemplo nuevo — es la misma pregunta cliffhanger
con la que abre `nb5_regresion.ipynb` ("si te doy el PBI de un país que nunca viste, ¿puedes
decirme su Puntaje aproximado?"), pero vivida antes de leerla, así que cuando la vean escrita en el
notebook ya la sintieron.

---

## 2. Concepto 1 — La línea que "mejor le queda" a los puntos (8 min)

Dibuja en la pizarra una nube de puntos parecida a PBI vs. Puntaje (no necesita ser exacta — el
punto es la forma, una tendencia ascendente con dispersión real, no una línea perfecta).

**Idea central, en sus palabras:**
- Esa línea no pasa exactamente por cada punto — con datos reales, eso es imposible.
- Es la línea que, mirando **todos** los puntos a la vez, queda lo más cerca posible **en
  promedio**.
- `LinearRegression().fit()` no prueba líneas al azar ni "adivina por ensayo y error" — encuentra
  matemáticamente la línea que minimiza esa distancia total. (No necesitan saber cómo — solo que
  no es magia ni prueba-y-error.)

**Chequeo rápido (mano alzada):** dibuja dos líneas candidatas sobre la misma nube de puntos —
una que pasa cerca del centro de la nube, otra claramente inclinada hacia una esquina. Pregunta
cuál creen que es la de mejor ajuste y por qué. (Respuesta: la que minimiza la distancia promedio
a *todos* los puntos, no la que toca más puntos individuales.)

---

## 3. Concepto 2 — R²: ¿qué tan bien explica la línea a los puntos? (10 min)

Retoma la pregunta que dejaste abierta en el Gancho (Japón vs. Finlandia): *"el patrón no es
perfecto — ¿cómo le ponemos un número a 'qué tan bueno' es?"*

**Idea central:**
- `r` (que ya conocen de Misión 2) mide qué tan fuerte es una relación, de -1 a 1.
- **R²** es distinto: dice **qué porcentaje de la variación** del resultado logra explicar el
  modelo.
  - R² = 1.0 → el modelo explica el 100% de la variación (predicción perfecta — casi nunca pasa
    con datos reales)
  - R² = 0.72 → el modelo explica el 72% de la variación — el otro 28% depende de cosas que el
    modelo no ve
  - R² = 0.0 → el modelo no aporta nada más que "usar siempre el promedio"

> ⚠️ **Ojo con el lenguaje** (nunca digas esto así): R² **no** es "el porcentaje de predicciones
> correctas" ni "la precisión" del modelo — no hay predicciones correctas/incorrectas en
> regresión, hay números más o menos cerca del real. R² es qué tanto de la *variación* explica el
> modelo, no un puntaje de aciertos.

**Apoyo visual (si tienes cómo proyectar):** el notebook trae un gráfico de tres modelos lado a
lado, mismo tipo de datos, con R² = alto / medio / bajo — muy útil para que "vean" el número antes
de calcularlo. Si no puedes proyectar, dibuja tú tres nubes de puntos a mano: una muy pegada a una
línea recta, una dispersa pero con tendencia visible, y una nube sin ninguna forma — pide que
ordenen las tres de mayor a menor R² a ojo.

---

## 4. Concepto 3 — Por qué separas "entrenamiento" y "prueba" (8 min)

**Analogía de apertura:**

> "Si yo les diera el examen de mañana hoy, con las respuestas, y luego el día del examen les
> hiciera las mismas preguntas... ¿aprendieron algo, o solo memorizaron?"

Deja que respondan. Luego conecta:

- Si ajustas el modelo con **todos** los países y mides qué tan bien predice esos **mismos**
  países, es exactamente ese examen con respuestas regaladas.
- Por eso se separan los datos en dos partes **antes** de entrenar:
  - **Train** (~90%): el modelo aprende de estos datos.
  - **Test** (~10%): datos que el modelo **nunca vio** — aquí se mide si de verdad aprendió un
    patrón, o si solo memorizó.
- El **R² de prueba** es el que de verdad importa: dice si el modelo generaliza a países nuevos,
  no si memorizó los que ya conocía.

**Punto que suele confundir (menciónalo explícitamente):** casi siempre, agregar más variables
sube el R² de **entrenamiento**. Eso *no* significa que el modelo mejoró de verdad — si el R² de
**prueba** no sube igual (o baja), el modelo probablemente memorizó ruido en vez de aprender un
patrón real. Esta es literalmente una de las 5 preguntas del quiz de cierre del notebook, así que
vale la pena que quede clara aquí y no solo leída después.

---

## 5. Concepto 4 — Interpretar los coeficientes (8 min)

Usa el resultado real del ejemplo guiado del notebook (van a verlo calculado en vivo ahí, así que
aquí solo se los adelantas conceptualmente):

> En el modelo de felicidad con las seis variables conocidas, el coeficiente de **PBI per
> cápita** fue ≈0.77 y el de **Apoyo social** ≈1.16.

**Plantilla de interpretación (haz que la repitan, es la que van a usar en sus propias respuestas):**

> "Por cada unidad adicional en \_\_\_ (variable), la predicción de \_\_\_ (resultado) cambia en
> \_\_\_ (coeficiente), **manteniendo las demás variables constantes**."

Aplicada: *"por cada unidad adicional de Apoyo social, la predicción del Puntaje sube en ≈1.16,
manteniendo las demás variables fijas."*

> ⚠️ **Dos reglas no negociables (escríbelas en la pizarra, van a usarlas en la reflexión
> calificada del notebook):**
> 1. **Nunca uses lenguaje causal.** No es "el Apoyo social *causa* que suba el Puntaje" — es
>    "el modelo *usa* el Apoyo social para predecir el Puntaje". La regresión describe una
>    asociación numérica, no prueba una causa (eso lo vieron a fondo en la Semana 5).
> 2. **Un coeficiente más grande no significa automáticamente "más importante".** Las variables
>    tienen escalas distintas — comparar coeficientes en bruto entre variables con rangos
>    distintos puede engañar. Lo que el coeficiente sí te dice con certeza es *cómo* el modelo usa
>    esa variable específica, no un ranking de importancia entre todas.

---

## 6. Cierre y transición al notebook (3 min)

No reveles el resultado del "míralo romperse" (extrapolación) — solo genera la pregunta:

> "Su oráculo va a tener un R² de prueba decente. Pero, ¿qué creen que pasa si le piden predecir
> con un valor **absurdamente** fuera de lo que vio al entrenar — por ejemplo, un PBI diez veces
> más alto que el país más rico del planeta? Ábranlo en el notebook y averígüenlo ustedes mismos."

Con eso, entregas la clase al notebook: van a repetir en código lo que acaban de construir en
palabras (línea de mejor ajuste, R², train/test, coeficientes), con un ejemplo guiado paso a paso
(Felicidad) y luego dos ejercicios calificados con un dataset distinto (Altura de atletas
olímpicos) — `nb5_regresion.ipynb`, ya armado y listo para compartir.

---

## Checklist de precisión estadística (GAUSS)

Para quien dicte la clase — errores fáciles de cometer al explicar esto en vivo, cada uno con su
versión correcta:

| No digas... | Di en su lugar... |
|---|---|
| "R² es la precisión del modelo" | "R² es el porcentaje de la variación que el modelo explica" |
| "El PBI *causa* que suba la felicidad" | "El modelo *usa* el PBI para predecir el Puntaje" |
| "Un coeficiente más grande = variable más importante" | "El coeficiente dice cómo se usa esa variable — no es un ranking, las escalas son distintas" |
| "El modelo funciona bien, así que puede predecir cualquier valor" | "El modelo solo es confiable *dentro* del rango de datos que vio al entrenar" |
| "Si el R² de entrenamiento subió, el modelo mejoró" | "Solo si el R² de **prueba** también sube — si no, probablemente memorizó en vez de aprender" |

---

*Diseñado para acompañar `nb5_regresion.ipynb` ("Misión 3: El Oráculo de Datos") — todos los
valores numéricos citados aquí (r≈0.794, R² de prueba≈0.71, coeficientes ≈0.77/≈1.16, valores de
Perú/Finlandia/Japón) están tomados directamente de `2019_es.csv` y de `autograder_nb5.py`
(calculados y ya validados el 2026-09-13, ver `WORKFORCE_HANDOFF.md`), no inventados para esta
guía.*

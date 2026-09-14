# Guía del Proyecto de Investigación
### Semana 4 → Semana 5 · Misión 2: Buscando Patrones


---

## 1. ¿Qué es esto?

Ya aprendiste a leer un patrón con el ojo, ponerle un número exacto
(`.corr()`), desconfiar de ese número, y revisar si se sostiene por
subgrupo. Ahora lo aplicas solo: eliges un dataset real, una afirmación que
quieras poner a prueba, y construyes el hallazgo de punta a punta.

**Esto es lo que vas a presentar y defender en la próxima clase** — esa
presentación abre la Semana 5 (Causalidad).

---

## 2. Cómo funciona

- Trabajas en pareja (o solo, si prefieres).
- **Hoy en clase:** eliges dataset y afirmación, cargas los datos, y arrancas
  el análisis con el profesor circulando para ayudarte.
- **De tarea:** terminas el análisis, escribes tu hipótesis y tu reflexión,
  y preparas tu presentación (2-3 minutos).
- **La próxima clase:** presentas. Nada de esto se autocalifica — tu
  profesor lo revisa con la rúbrica de la sección 4.

---

## 3. Entregables — checklist

**En el notebook:**

- [ ] Dataset cargado en `df`
- [ ] `.info()` y `.describe()` ejecutados — ¿cuántas filas? ¿faltan datos?
- [ ] Tu predicción escrita **antes** de graficar (¿patrón fuerte o débil? ¿positivo o negativo?)
- [ ] Scatter plot de tu par de columnas
- [ ] `.corr()` calculado — tu valor real de `r`
- [ ] *(Opcional)* `.corr()` repetido dentro de un subgrupo (misma lógica que la Sección C de Semana 4)
- [ ] Tu hipótesis por escrito — mínimo 2 oraciones, con una **razón**, no solo el número
- [ ] Tus respuestas a las dos preguntas incómodas:
  1. Si hubieras probado varios pares antes de quedarte con este, ¿por qué no confiar en "el r más alto que encontré" solo porque salió alto?
  2. Nombra **una cosa distinta** a "una variable causa la otra" que podría explicar tu patrón.

**En tu presentación (2-3 minutos), en este orden:**

1. Tu afirmación y tu dataset (¿de dónde salen los datos?)
2. Tu scatter y tu `r`
3. Tu hipótesis, con razón
4. Tu respuesta a la Pregunta 2 — una explicación alternativa a "X causa Y"

No hace falta un slide elaborado — el notebook mismo, o una hoja con estos
cuatro puntos, alcanza.

---

## 4. Rúbrica (85 puntos, calificación humana — no XP)

Esta es la misma rúbrica (menos la fila de regresión/clustering) que vas a
volver a ver en el proyecto final del bimestre — practicar aquí te sirve dos
veces. Usa los 4 niveles de logro del CNB: **AD** (logro destacado), **A**
(logro esperado), **B** (en proceso), **C** (en inicio).

### Criterio 1 — Calidad del dataset + pregunta de investigación (15 pts)

- **AD (14-15):** Dataset apropiado (del menú o propio con visto bueno), con
  dos columnas numéricas reales y suficientes filas. La afirmación es
  específica y genuinamente pone algo a prueba — no es obvia ni trivial.
- **A (11-13):** Dataset apropiado y afirmación clara, pero podría ser más
  específica (ej. "estas dos variables están relacionadas" en vez de una
  afirmación causal concreta).
- **B (7-10):** El dataset funciona pero la afirmación es vaga o genérica, o
  se eligió del menú sin pensar en por qué esa afirmación importa.
- **C (0-6):** El dataset no es apropiado (menos de 2 columnas numéricas
  usables, demasiados datos faltantes) o no hay una afirmación clara que
  poner a prueba.

### Criterio 2 — Análisis descriptivo con interpretación (20 pts)

- **AD (18-20):** `.info()` y `.describe()` ejecutados correctamente, **y**
  interpretados en palabras propias: cuántas filas hay, si faltan datos, y
  qué rango tienen las dos columnas de interés — no solo repite los
  números, explica qué significan para su pregunta.
- **A (14-17):** Ejecuta correctamente y da una interpretación, pero
  superficial (menciona los números sin conectar con la pregunta de
  investigación).
- **B (9-13):** Ejecuta el código pero no interpreta nada, o la
  interpretación tiene errores menores.
- **C (0-8):** No ejecuta `.info()`/`.describe()`, o los resultados no
  corresponden a su dataset real.

### Criterio 3 — Análisis de correlación + hipótesis con crítica de causalidad (20 pts)

**El criterio más importante — es el puente directo a Semana 5.**

- **AD (18-20):** `r` calculado correctamente e interpretado en palabras
  (fuerza y dirección). La hipótesis da una razón específica y plausible
  (no "porque sí"). La respuesta a la Pregunta 2 nombra una explicación
  alternativa **concreta** — un confusor real, causalidad inversa, o
  coincidencia — no solo repite "correlación no es causalidad" sin explicar
  el mecanismo.
- **A (14-17):** `r` correcto e interpretado. Hipótesis razonable. La
  Pregunta 2 tiene respuesta pero es genérica ("podría haber otra causa"
  sin decir cuál).
- **B (9-13):** `r` calculado pero mal interpretado (confunde signo/fuerza,
  o usa lenguaje causal sin crítica — "esto prueba que X causa Y"). Hipótesis
  débil o ausente.
- **C (0-8):** `r` no calculado o incorrecto; no hay intento real de
  responder la Pregunta 2.

### Criterio 4 — Calidad de la visualización (20 pts)

- **AD (18-20):** Scatter claro, ejes etiquetados con nombre y unidad,
  escala apropiada (sin distorsión), el patrón se lee a simple vista.
- **A (14-17):** Scatter funcional y ejes etiquetados, pero falta unidad o
  la escala podría mejorar.
- **B (9-13):** El scatter se genera pero tiene problemas (ejes sin
  etiqueta, variables invertidas, difícil de leer).
- **C (0-8):** No hay scatter, o no corresponde a las columnas elegidas.

### Criterio 5 — Claridad de la presentación (10 pts)

- **AD (9-10):** Sigue las 4 partes en orden, dentro de 2-3 minutos, explica
  con sus propias palabras (no lee de la pantalla), responde preguntas con
  seguridad.
- **A (7-8):** Sigue las 4 partes en un tiempo razonable, pero lee bastante
  del notebook o de apuntes.
- **B (4-6):** Falta alguna de las 4 partes, se pasa mucho del tiempo, o la
  explicación es confusa.
- **C (0-3):** No presenta, o la presentación está claramente sin preparar.

### Resumen de puntos

| Criterio | Puntos máx. |
|---|---|
| 1. Calidad del dataset + pregunta de investigación | 15 |
| 2. Análisis descriptivo con interpretación | 20 |
| 3. Correlación + hipótesis con crítica de causalidad | 20 |
| 4. Calidad de la visualización | 20 |
| 5. Claridad de la presentación | 10 |
| **Total** | **85** |

---

## 5. Elige tu dataset

Puedes elegir uno del menú de abajo, o proponer el tuyo — si tienes una idea
propia, pídele el visto bueno a tu profesor **antes** de empezar a analizar
(así evitamos que descubras a mitad de camino que tus datos no sirven).

Tu profesor te va a dar el archivo `.csv` de cada opción ya listo para usar,
con los nombres de columna en español. El link de abajo es solo para que
sepas de dónde salen los datos reales — no lo uses para descargar.

### 🩺 A. Salud — Hábitos de sueño y estilo de vida
**Afirmación a poner a prueba:** *"Dormir menos horas causa más estrés."*
**Fuente:** [Sleep Health and Lifestyle Dataset (Kaggle)](https://www.kaggle.com/datasets/uom190346a/sleep-health-and-lifestyle-dataset)
**Columnas a usar:** Duración del sueño ↔ Nivel de estrés
**Columna de subgrupo (opcional):** Ocupación

### ⚽ B. Deportes — Jugadores de fútbol (FIFA)
**Afirmación a poner a prueba:** *"Pagarle más sueldo a un jugador causa que sea mejor jugador."*
**Fuente:** [FIFA 20 Complete Player Dataset (Kaggle)](https://www.kaggle.com/datasets/stefanoleone992/fifa-20-complete-player-dataset)
**Columnas a usar:** Calificación general ↔ Sueldo semanal
**Columna de subgrupo (opcional):** Posición principal

### 🌍 C. Economía y salud global — Países del mundo
**Afirmación a poner a prueba:** *"Un PBI per cápita más alto causa una esperanza de vida más larga."*
**Fuente:** [Gapminder (Software Carpentry / R for Data Science teaching dataset)](https://github.com/resbaz/r-novice-gapminder-files)
**Columnas a usar:** PBI per cápita ↔ Esperanza de vida
**Columna de subgrupo (opcional):** Continente

### 🎬 D. Negocios y entretenimiento — Películas de Hollywood
**Afirmación a poner a prueba:** *"Gastar más en producir una película causa que gane más en taquilla."*
**Fuente:** [Movies dataset (Vega Datasets)](https://github.com/vega/vega-datasets)
**Columnas a usar:** Presupuesto de producción ↔ Recaudación mundial
**Columna de subgrupo (opcional):** Género principal

### 🏀 E. Deportes (alternativa) — Jugadores de la NBA

**Afirmación a poner a prueba:** *"Anotar más puntos causa que un jugador gane más dinero."*
**Fuente:** [NBA 2017 Player Stats + Salary (GitHub — noahgift/socialpowernba)](https://github.com/noahgift/socialpowernba)
**Columnas a usar:** Puntos por temporada ↔ Salario (millones)
**Columna de subgrupo (opcional):** Posición

### 🚗 F. Ingeniería y autos — Consumo de combustible

**Afirmación a poner a prueba:** *"Un motor con más caballos de fuerza causa peor rendimiento de combustible."*
**Fuente:** [MPG dataset (seaborn-data, dataset clásico de autos de EE.UU.)](https://github.com/mwaskom/seaborn-data)
**Columnas a usar:** Caballos de fuerza ↔ Millas por galón
**Columna de subgrupo (opcional):** Origen (EE.UU./Japón/Europa)

### 🌍 G. Economía (alternativa) — Países del mundo (CIA World Factbook)

**Afirmación a poner a prueba:** *"Tener más líneas telefónicas por persona causa un PBI per cápita más alto."*
**Fuente:** [Countries of the World (Kaggle — fernandol/countries-of-the-world)](https://www.kaggle.com/datasets/fernandol/countries-of-the-world)
**Columnas a usar:** PBI per cápita ↔ Teléfonos por cada 1,000 habitantes
**Columna de subgrupo (opcional):** Región (Perú aparece en "Latinoamérica y el Caribe")

---

## 6. ¿Y si tengo mi propio dataset?

Adelante — es una opción real, no solo las de arriba. Para que tu profesor
te dé el visto bueno, tu dataset tiene que cumplir **todos** estos
requisitos:

1. **Fuente identificable.** Viene de un sitio real y citable (Kaggle, un
   organismo oficial, una organización reconocida) — no datos inventados o
   de una página sin origen claro.
2. **Al menos dos columnas numéricas** con datos reales (no todo en cero,
   no todo vacío).
3. **Al menos 30 filas** con datos completos en esas dos columnas —
   con menos, tu `r` no significa nada confiable (mismo problema que la
   trampa de Oceanía con n=2 en Semana 4).
4. **Permite una afirmación tipo "X causa Y"** que alguien podría creer a
   primera vista, pero que se pueda cuestionar.
5. **Apropiado para el colegio** — sin contenido gráfico, violento o fuera
   de lugar.
6. Si está en inglés, trae un **mini-glosario de 5-10 términos clave** (los
   nombres de columna y valores que vas a usar) — parte de mostrar que
   entendiste tus propios datos, no un trámite aparte.
7. **Visto bueno del profesor antes de empezar a analizar** — así evitas
   descubrir a mitad de camino que tus datos no sirven.

**¿Se necesita presentación si uso mi propio dataset? Sí, siempre.** No
importa si tu dataset es del menú o el tuyo — todos presentan, con la misma
estructura de 4 partes (sección 3) y la misma rúbrica (sección 4). No hay
excepción por traer tu propio dataset.

---
---

## ⚠️ Solo para el profesor — no compartir con estudiantes

Valores reales verificados directamente contra los datos (no estimados),
para poder calificar la Pregunta 2 y el criterio de "crítica de
causalidad" con criterio, no a ojo.

| # | Dataset | `r` real | Explicación de confusión esperable | Nota |
|---|---|---|---|---|
| A | Sleep Health | **-0.81** (Duración de sueño ↔ Nivel de estrés) | La ocupación es el confusor plausible — enfermeras/médicos tienen horarios exigentes que probablemente causan tanto menos sueño como más estrés, no una cosa causando la otra directamente. Por subgrupo, el patrón varía fuerte: Enfermería r=-0.99, Docencia r=-0.06 — buen material para "¿se sostiene en todos los grupos?". | 374 filas, 24 KB. Etiqueta inconsistente en `BMI Category` ("Normal" vs "Normal Weight") — no afecta este par. Licencia CC0. |
| B | FIFA 20 | **0.58** (Calificación general ↔ Sueldo, filtrando sueldo>0, n=18,038) | Es sobre todo **causalidad inversa**: los clubes pagan sueldos altos *porque* el jugador ya es bueno, no al revés. La edad es un segundo confusor real (jugadores en edad prime cobran más y rinden más). | Archivo original ~9 MB / 100+ columnas — **recortar a ~10 columnas relevantes + filas sin sueldo antes de entregarlo**, igual que se hizo con `2019_es.csv`. Licencia Kaggle "Other" (datos de EA/sofifa) — uso estándar en proyectos educativos pero no CC0 estricta. |
| C | Gapminder 2007 | **0.68** (PBI per cápita ↔ Esperanza de vida, 142 países) | El confusor es el nivel general de desarrollo — un país rico invierte en salud, nutrición y sistemas sanitarios simultáneamente; el PBI no "causa" longevidad de forma aislada. Por continente: África r=0.39 (débil), Europa r=0.85 (fuerte). | Perú aparece en el dataset (2007: esperanza de vida 71.4 años, PBI per cápita $7,409). Solo 6 columnas — traducción rápida. |
| D | Movies | **0.67** (Presupuesto de producción ↔ Recaudación mundial, n=3,193) | Franquicias y actores reconocidos reciben presupuestos altos *porque* ya se espera que sean éxitos — el dinero sigue al éxito esperado, no solo lo causa. Por género: Thriller/Acción/Aventura r≈0.65-0.69, Drama r≈0.48. | Sin licencia formal estampada (repo académico de uso extendido en cursos de dataviz) — uso educativo está bien, no para redistribución. |
| E | NBA 2017 | **0.64** (Puntos ↔ Salario, n=342) | Misma lógica que FIFA (B): causalidad inversa — un equipo paga más *porque* el jugador ya rinde, no al revés. Por posición: r entre 0.46 (Centro) y 0.80 (Base/PG). | 68 KB, ya viene combinado (stats + salario en un solo archivo, sin necesidad de merge). **Ojo:** cuenta la misma lección que B (causalidad inversa por rendimiento probado) en otro deporte — si usas ambos, aclara que la lección de fondo se repite a propósito. |
| F | MPG | **-0.78** (Caballos de fuerza ↔ Millas por galón, n=398) | El confusor real es el peso del vehículo — caballos de fuerza correlaciona 0.87 con peso, y es plausible que el tamaño/peso del auto explique el consumo, no la potencia por sí sola. Por origen: r entre -0.67 y -0.75, estable. | 9 KB, cero fricción de carga (`sns.load_dataset('mpg')`, sin descarga manual). 6 valores faltantes en caballos de fuerza, triviales de descartar. |
| G | Countries of the World | **0.83** (PBI per cápita ↔ Teléfonos por 1,000 hab., n=227) | Confusor: nivel general de desarrollo — un país próspero invierte en todo tipo de infraestructura a la vez; los teléfonos no "causan" riqueza por sí solos. | **Mismo tipo de historia que C (Gapminder)** — desarrollo nacional como confusor. Si ofreces ambos, son válidos pero parecidos; útil para variedad de dataset, no de lección. Columnas con coma decimal europea (`decimal=','` al leer) y `Region` con espacios al final — arreglar antes de traducir. |



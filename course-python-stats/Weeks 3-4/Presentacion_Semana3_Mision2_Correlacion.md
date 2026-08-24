# Semana 3 — Outline de Presentación: "Misión 2: Buscando Patrones"

**Estado:** Borrador de outline (SOFIA), derivado directamente de `nb3_correlacion.ipynb`
(ya construido, dataset real cargado) y de `Teoria_Semanas3-4_Mision2_Correlacion.md`.
**Propósito:** guion de apoyo para el profesor, proyectado/hablado **antes** de que los
estudiantes abran el notebook — no reemplaza el notebook, lo antecede. Duración estimada:
15–20 min de una clase de ~90 min (`WORKFORCE_CONTRACT.md` §2); el resto es trabajo en el
notebook.

**Regla de lenguaje no negociable (heredada de la Teoría, aplica también aquí):** nunca
"causa," "provoca," "hace que." Solo "relación," "patrón," "asociado con," "tiende a." La
única excepción deliberada es la Sección 2 de abajo (pregunta de apertura), donde se
permite lenguaje causal-cotidiano **porque los estudiantes responden desde su intuición,
antes de ver un solo dato** — el profesor no debe validar ni corregir esas respuestas
todavía, solo recogerlas para contrastarlas más tarde.

Todos los números de este outline son **reales**, tomados directamente de
`nb3_correlacion.ipynb` (celda `nb3-apertura-reveal`) — no son placeholders.

---

## 0. Objetivo pedagógico de esta presentación

Mismo principio que abre el notebook: que el estudiante practique leer un patrón visual y
arriesgar una predicción **antes** de que exista vocabulario formal o un número calculado.
Esta presentación es la versión "en vivo, con el grupo completo" de lo que el notebook
después hace individualmente. Todo lo que se muestre aquí debe **reaparecer** en el
notebook (mismos diagramas, mismos r) para que el estudiante sienta continuidad, no dos
lecciones distintas.

---

## 1. Slide de Título

- **"Misión 2: Buscando Patrones"** (nombre placeholder, pendiente de tematización final
  de PIXEL — ver Notas internas de la Teoría).
- Gancho de una línea: *"La Misión 1 te enseñó a resumir una columna. Hoy vas a aprender
  algo nuevo: cómo saber si dos columnas se mueven juntas."*

---

## 2. Pregunta de Apertura — Brainstorm sin datos (~3–4 min)

**Antes de mostrar el dataset.** Proyectar solo la pregunta, sin ningún gráfico ni número:

> ### "¿Cuál es el origen de la felicidad?"
> *(¿Qué hace que un país, en promedio, reporte más felicidad que otro?)*

- Recoger 3–5 respuestas orales o en el chat, sin juzgar ni corregir — es intuición cruda,
  el mismo espíritu que la apertura de Semanas 1–2.
- **Nota de facilitación:** esta pregunta usa lenguaje causal a propósito ("origen de");
  es la única vez en el bloque de Semanas 3–4 donde eso es aceptable, porque es una
  pregunta de intuición personal, no una conclusión sobre datos. El profesor no debe
  "corregir" hacia lenguaje de correlación todavía — eso vendría en frío y le quitaría
  peso al giro real, que ocurre en la Sección 1 de la Teoría (`nb3-teoria0-md`), donde el
  notebook planta explícitamente: *"un coeficiente de correlación nunca, por sí solo, te
  dice si una variable causa la otra."*

**Segunda pregunta, misma sección — ranking de predicción:**

> Aquí tienes seis variables del reporte de felicidad de este año: **PBI per cápita,
> Apoyo social, Esperanza de vida saludable, Libertad para tomar decisiones, Generosidad,
> Percepción de corrupción.**
>
> Sin ver ningún dato todavía: **ordénalas de "más relacionada con la felicidad de un
> país" a "menos relacionada."**

- Pedir que cada estudiante escriba su orden (papel, chat, o Mentimeter/similar —
  herramienta a elección del profesor, no especificada aquí).
- Guardar las respuestas visibles — se contrastan en la Sección 6.
- Esta dinámica es el equivalente "de aula completa" del ejercicio 🔮 PREDICE que el
  notebook repite individualmente en cada Ronda (`nb3-ronda1-predice-code`, etc.) — mismo
  principio, escala de grupo.

---

## 3. Teoría — ¿Qué es un diagrama de dispersión (*scatter plot*)? (~3 min)

- **Definición simple:** un gráfico donde cada punto representa **una fila del dataset**
  (aquí, un país) y su posición depende de **dos** columnas numéricas a la vez — una en el
  eje X, otra en el eje Y.
- **Cómo leerlo:**
  - Si los puntos forman algo parecido a una línea → hay un patrón.
  - Si los puntos forman una nube sin forma reconocible → no hay un patrón visual claro.
- **Mostrar en vivo** los tres diagramas de la apertura del notebook (`nb3-apertura-oculto`),
  con ejes genéricos "Variable X" / "Variable Y" — **sin revelar todavía** qué columnas son:
  - Diagrama 1, Diagrama 2, Diagrama 3 (los mismos tres que el notebook usa).
- Pedir al grupo que los ordene de "más patrón" a "menos patrón" **solo por percepción
  visual** — mismo ejercicio que la celda `nb3-apertura-orden-code`, ahora hecho en vivo
  antes de que el estudiante lo repita solo en el notebook.

---

## 4. Teoría — ¿Qué es la correlación? (~4–5 min)

- **Definición:** un número (el coeficiente de correlación, `r`) que resume **qué tan
  fuerte** y **en qué dirección** dos variables numéricas se mueven juntas. En este curso
  se calcula con `.corr()` (correlación de Pearson) — el nombre técnico se menciona una
  vez, no se exige que el estudiante lo recuerde.
- **El rango, -1 a 1** (mostrar la tabla, idéntica a la del notebook):

  | Valor de r | Qué significa |
  |---|---|
  | Cercano a **+1** | Relación fuerte y positiva — cuando una sube, la otra tiende a subir |
  | Cercano a **-1** | Relación fuerte y negativa — cuando una sube, la otra tiende a bajar |
  | Cercano a **0** | Relación lineal débil o inexistente |

- **Dos preguntas distintas:**
  - **Dirección** (el signo): ¿suben juntas, o una sube mientras la otra baja?
  - **Fuerza** (qué tan lejos de 0): ¿qué tan consistente es el patrón? (r=0.9 es mucho
    más consistente que r=0.3, aunque ambos sean positivos.)
- **Dos advertencias, dichas en voz alta, no solo leídas** (mismas del notebook,
  `nb3-teoria0-md`):
  1. `.corr()` solo mide relación **lineal** — una relación real pero curva puede dar un
     r cercano a 0.
  2. **La más importante:** un r, por sí solo, **nunca** dice si una variable causa la
     otra. (Plantar la frase aquí; no desarrollarla — eso es trabajo protegido de la
     Semana 5.)

---

## 5. El Dataset de Hoy — World Happiness Report 2019 (~3 min)

- **Qué es:** el ranking mundial de felicidad 2019, con el puntaje de cada país y seis
  variables económicas/sociales que el reporte usa para acompañarlo.
- **Tamaño real:** 156 filas (un país o región por fila) × 10 columnas.
- **Dato de calidad:** a diferencia del dataset de videojuegos de la Misión 1, **este no
  tiene ningún valor faltante** — las 156 filas están completas.
- **Las columnas:**
  - Identificación: `Puesto`, `País o región`, `Continente`
  - Variable objetivo: `Puntaje` (el puntaje de felicidad)
  - Seis variables explicativas: `PBI per cápita`, `Apoyo social`, `Esperanza de vida
    saludable`, `Libertad para tomar decisiones`, `Generosidad`, `Percepción de
    corrupción`
- **Vistazo rápido** (mostrar las primeras filas reales, ya cargadas en el notebook):

  | País | Continente | Puntaje | PBI per cápita |
  |---|---|---|---|
  | Finlandia | Europa | 7.769 | 1.340 |
  | Dinamarca | Europa | 7.600 | 1.383 |
  | Noruega | Europa | 7.554 | 1.488 |
  | Islandia | Europa | 7.494 | 1.380 |

- **Aviso, mismo tono que el notebook:** un dataset sin filas faltantes no es lo mismo
  que un dataset "perfecto" — más adelante en la clase van a ver que una de sus columnas
  es, en la práctica, casi un espejo de otra.

---

## 6. La Revelación — Contrastar la predicción del grupo contra los datos reales (~4–5 min)

Ahora sí, mostrar los mismos tres diagramas de la Sección 3 con sus etiquetas reales y su
`r` real (idéntico a `nb3-apertura-reveal`):

| Diagrama | Par de variables | r real | Lectura |
|---|---|---|---|
| 3 | `PBI per cápita` vs. `Puntaje` | **≈ 0.79** | el patrón más fuerte de los tres |
| 1 | `Libertad para tomar decisiones` vs. `Puntaje` | **≈ 0.57** | patrón real, pero mucho menos limpio |
| 2 | `Generosidad` vs. `Puntaje` | **≈ 0.08** | casi una nube sin forma |

- **Contrastar contra el ranking visual que el grupo hizo en la Sección 3** — ¿el orden
  del grupo coincidió con el orden real de los tres diagramas? Casi siempre sí: ese
  acierto es lo que hace que el coeficiente se sienta como herramienta, no como sintaxis
  arbitraria.
- **Contrastar contra el ranking de las 6 variables que el grupo predijo en la Sección 2**
  (antes de ver cualquier dato). Preguntas de discusión:
  - ¿Quién ubicó `PBI per cápita` cerca del primer lugar? ¿Alguien lo puso último?
  - ¿A cuántos les sorprendió que `Generosidad` casi no se relacione con el puntaje?
  - Volviendo a la pregunta de apertura ("¿cuál es el origen de la felicidad?"): ¿el PBI
    fue una de las respuestas orales de la Sección 2? ¿Cambia esto la respuesta de
    alguien, o la refuerza?
- **Recordatorio explícito, dicho en voz alta antes de pasar al notebook:** *"'Los países
  con mayor PBI per cápita tienden a reportar mayor puntaje' es una relación observada —
  no es lo mismo que decir que el dinero causa la felicidad."* (texto real de
  `nb3-apertura-explicacion`, no parafraseado)

---

## 7. Puente al Notebook (~1–2 min)

- *"Ahora es tu turno: vas a repetir este mismo proceso — predecir, graficar, calcular —
  con seis pares distintos de variables, algunos con `Puntaje` y otros entre sí."*
- Adelanto de lo que viene en el notebook, sin resolverlo:
  - Ronda 3 y 5: `PBI per cápita` también se relaciona fuerte con `Esperanza de vida
    saludable` y con `Apoyo social` — ninguna de las dos veces es con `Puntaje`.
  - Ronda 6: ¿`Generosidad` se relaciona con **algo**, aunque no sea con la felicidad?
  - Semana 4: van a agrupar por continente y descubrir que el patrón general puede
    esconder — o hasta invertir — lo que pasa dentro de cada grupo; y van a elegir su
    propio par de variables para un mini-proyecto.
- **Recordatorio de vocabulario** antes de soltar al grupo al notebook: de aquí en
  adelante, en el trabajo escrito (reflexiones, hipótesis), la palabra es *"relación" /
  "patrón" / "asociado con" / "tiende a"* — no *"causa."*

---

## Notas para quien construya las slides finales (PIXEL / diseño visual)

- Los tres diagramas de las Secciones 3 y 6 deben ser **capturas reales** generadas desde
  `nb3_correlacion.ipynb` (celdas `nb3-apertura-oculto` y `nb3-apertura-reveal`), no
  recreaciones — así el estudiante reconoce literalmente la misma imagen cuando abre el
  notebook minutos después.
- Tema visual y nombre final de "Misión 2" siguen pendientes de PIXEL (ticket #2 en
  `WORKFORCE_HANDOFF.md`) — este outline usa lenguaje neutro a propósito, mismo criterio
  que la Teoría.
- Si el horario real separa Semana 3 en más de una sesión, esta presentación completa
  corresponde solo a la **apertura de la Clase 1** — no repartir sus secciones entre
  distintos días sin revisar la Sección 5 de `Teoria_Semanas3-4_Mision2_Correlacion.md`
  (propuesta de reparto Semana 3 / Semana 4).

---

*Última actualización: 2026-08-23*
*Autor: SOFIA — derivado de `nb3_correlacion.ipynb` (ya construido) y de
`Teoria_Semanas3-4_Mision2_Correlacion.md`*

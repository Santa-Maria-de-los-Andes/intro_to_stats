# Semanas 3–4: Teoría — "Misión 2: Buscando Patrones"

**Estado:** Borrador de contenido (SOFIA) — pendiente de vetting de dataset (GAUSS, ticket #7 en
`WORKFORCE_HANDOFF.md`) y de tematización final (PIXEL). No hay código ni notebook construido
todavía; este documento fija la secuencia pedagógica y el contenido teórico antes de esos pasos,
siguiendo el mismo orden de construcción que Semanas 1–2 (`COURSE_TEMPLATE.md` §2/§12: SOFIA →
GAUSS → PIXEL → ATLAS → build script).

**Estructura de secciones:** propuesta en este documento (sección 2 abajo), pendiente de
confirmar contra `WORKFORCE_CONTRACT.md` §2 una vez GAUSS y el usuario la revisen. Basada
directamente en la secuencia ya fijada en `Bimestre3_Statistics_Python_Module_Guide.md`
("Weeks 3–4: Correlation" — 1) scatter sin código, 2) coeficiente conceptual, 3) calcularlo en
código, 4) explorarlo por subgrupo).

**Dataset propuesto:** World Happiness Report (candidato principal) — ya reservado para
Semanas 3–4 desde la decisión de dataset de Semanas 1–2
(`WORKFORCE_HANDOFF.md`, Done log 2026-08-05: *"World Happiness Report / World Bank indicators
(reserved for Wk 3–4 instead — its strong GDP↔happiness relationship would let students
informally pattern-match a causal read before Week 5's causation guardrails exist to check
it")*. **Ningún valor real de este dataset ha sido descargado ni verificado todavía** — todos los
números de ejemplo abajo son placeholders y deben confirmarse contra el CSV real antes de
fijarse en el notebook, misma regla que Semanas 1–2 (*"no publicar un número sin verificar contra
el dataset real"*).

> Nota de lenguaje: mismo criterio que Semanas 1–2 — texto orientado al estudiante en español,
> código/identificadores en inglés. El nombre "Misión 2: Buscando Patrones" es un placeholder
> funcional (como lo fue "Recuperación de Datos" en Semanas 1–2) hasta que PIXEL cierre el tema
> visual completo del bimestre (ticket #2). El orden pedagógico de este documento no cambia
> cuando eso se defina.

> ⚠️ **Regla de lenguaje no negociable para todo este documento y el notebook que genere:**
> nunca usar "causa," "provoca," "hace que," ni ninguna frase que implique causalidad. Solo
> "relación," "patrón," "asociado con," "tiende a." La Semana 5 es el único lugar del módulo
> donde se trata la causalidad formalmente (`Bimestre3_Statistics_Python_Module_Guide.md`: *"gets
> protected time; don't compress it"*) — Semanas 3–4 construyen intencionalmente la tentación de
> leer causalidad sin nunca cederla, para que la Semana 5 tenga algo real que desarmar.

---

## 0. Apertura — El Gancho (antes de cualquier código)

**Objetivo:** que el estudiante practique "leer" un patrón visual antes de que exista una palabra
formal para nombrarlo — exactamente el mismo principio que abrió Semanas 1–2, aplicado ahora a
relaciones entre dos variables en vez de a un solo número.

**Mecánica propuesta:** se muestran 3–4 diagramas de dispersión (scatter plots) reales del
dataset elegido, **sin ejes etiquetados con las variables reales todavía** (o con etiquetas
genéricas "Variable X" / "Variable Y") y sin ningún coeficiente calculado. Se pide a los
estudiantes ordenarlos de "patrón más fuerte" a "no veo ningún patrón," solo por percepción
visual.

> *"Antes de que exista un número para esto, tu ojo ya sabe reconocer un patrón. La misión de
> hoy: aprender a ponerle un número a lo que ya estás viendo."*

**Revelación:** se destapan las etiquetas reales. Al menos uno de los diagramas debe ser la
relación real y fuerte del dataset (ej. PBI per cápita vs. puntaje de felicidad); al menos otro
debe ser una relación débil o nula real del mismo dataset (no inventada) para que el contraste
sea honesto, no un truco de diseño.

**Nota para GAUSS:** a diferencia de la apertura de Semanas 1–2 (que solo necesitaba dos números
reales), esta apertura necesita **al menos un par fuerte y un par débil/nulo, ambos reales**,
del dataset final. Esto solo puede fijarse en números exactos una vez el CSV esté descargado y
GAUSS confirme qué pares cumplen ese contraste — pendiente, no bloqueante para el resto de este
documento.

**Explícitamente fuera de esta apertura:** el ejemplo clásico de helados y ahogamientos está
**reservado para la apertura de la Semana 5** (`Bimestre3_Statistics_Python_Module_Guide.md`:
*"Classic example (ice cream sales & drownings) → then student-found examples"*) — no reutilizar
aquí aunque encaje temáticamente; usarlo ahora le quitaría impacto a la Semana 5.

---

## 1. Teoría Desbloqueada — Fundamentos (bloque formal, antes de la Sección A)

Mismo patrón que Semanas 1–2 §1: bloque de teoría **formal y nombrada explícitamente**, evaluado
después con `check_tN`. Este es exactamente el tema que el propio documento de Semanas 1–2 ya
anticipó en su tabla de "Patrón para las semanas siguientes": *"Coeficiente de correlación:
definición formal, rango (-1 a 1), fuerza vs. dirección."*

### 1.1 ¿Qué es el coeficiente de correlación?

**Definición:** un número que resume **qué tan fuerte** y **en qué dirección** dos variables
numéricas se mueven juntas. En este curso se calcula con `.corr()` (correlación de Pearson) —
el nombre técnico se menciona una vez, no se exige que el estudiante lo recuerde.

### 1.2 El rango: -1 a 1

| Valor de r | Qué significa |
|---|---|
| Cercano a **+1** | Relación fuerte y positiva — cuando una sube, la otra tiende a subir |
| Cercano a **-1** | Relación fuerte y negativa — cuando una sube, la otra tiende a bajar |
| Cercano a **0** | Relación lineal débil o inexistente |

### 1.3 Dos preguntas distintas: fuerza vs. dirección

- **Dirección** (el signo, + o −): ¿suben juntas o una sube mientras la otra baja?
- **Fuerza** (qué tan lejos de 0): ¿qué tan consistente es ese patrón? Un r de 0.9 es un patrón
  mucho más consistente que uno de 0.3, aunque ambos sean positivos.

**El pago de la apertura:** los diagramas que el estudiante ya ordenó por percepción visual en la
Sección 0 ahora reciben un número — y ese número casi siempre confirma el orden que el ojo ya
había detectado. Eso es lo que hace que el coeficiente se sienta como una herramienta, no como
sintaxis arbitraria.

> ⚠️ Nota de precisión estadística (GAUSS) — importante para no sobre-generalizar: `.corr()`
> mide específicamente relación **lineal**. Una relación real y fuerte pero curva (no lineal)
> puede dar un r cercano a 0. Se menciona como una frase de honestidad, no como una unidad
> nueva — este curso no enseña a detectar no-linealidad formalmente (fuera del alcance técnico,
> `WORKFORCE_CONTRACT.md` §5).

> ⚠️ Nota de precisión estadística (GAUSS) — la más importante de estas dos semanas, y la que
> conecta directo con el riesgo que el propio GAUSS marcó para esta unidad (`04_GAUSS.md`):
> un coeficiente de correlación **nunca, por sí solo, te dice si una variable causa la otra.**
> No se explica todavía el porqué a fondo — eso es trabajo protegido de la Semana 5 — pero la
> frase debe quedar plantada aquí, explícitamente, la primera vez que el estudiante calcula un
> r real.

---

## 2. Teoría por Sección (bloques cortos, cada uno justo antes de su ejercicio)

Mismo principio que Semanas 1–2 §2: teoría → mini-ejercicio inmediato → check → siguiente teoría
(`COURSE_TEMPLATE.md` §4). Los cuatro bloques abajo siguen el orden ya fijado en
`Bimestre3_Statistics_Python_Module_Guide.md` para esta unidad, letra por letra igual que
Semanas 1–2 (A→D), como placeholder de nomenclatura hasta que PIXEL confirme los nombres finales.

### Sección A — Antes de Calcular (`.scatter()`, sin fórmula todavía)

Repite el ejercicio de la apertura pero ahora con código: el estudiante genera sus propios
diagramas de dispersión con `matplotlib` sobre 2–3 pares de columnas del dataset real, y
**predice** (celda 🔮 PREDICE) si espera un patrón fuerte, débil, positivo o negativo — antes de
calcular nada. Practica la lectura visual con datos que él mismo produjo, no solo los que se le
mostraron.

### Sección B — Calcúlalo (`.corr()`)

Aquí se conecta el número formal de la Sección 1 con los mismos pares que el estudiante ya
predijo en la Sección A. El ejercicio central: comparar la predicción visual contra el r real
calculado — cuando coinciden, refuerza la intuición; cuando no, es una oportunidad genuina de
preguntar "¿por qué mi ojo se equivocó aquí?" (ej. un outlier real jalando la impresión visual,
mismo concepto de valor atípico ya sembrado en Semanas 1–2 Sección C).

### Sección C — Por Subgrupos (`.groupby()` + `.corr()`)

Se repite el cálculo de la Sección B pero separado por una columna categórica del dataset (ej.
región/continente, pendiente de confirmar que existe en el CSV real elegido — ver Notas
internas). El hallazgo real que se busca: el r calculado por subgrupo **puede diferir** del r
general — a veces más fuerte, a veces más débil, en dataset reales incluso puede cambiar de
signo.

> ⚠️ Nota de precisión estadística (GAUSS) — misma disciplina de dosis mínima que Semanas 1–2
> Sección D: una sola frase de humildad aquí, sin convertirla en una clase completa (ese es
> presupuesto protegido de la Semana 5): *"el patrón general puede esconder — o incluso
> invertir — lo que pasa dentro de cada grupo."* No se nombra formalmente la paradoja de
> Simpson ni se exige que el estudiante la reconozca por nombre; la frase es la barrera mínima,
> igual que la de Semanas 1–2 Sección D lo fue para lectura causal prematura.

### Sección D / Integración (Semana 4) — Mini-Proyecto: Encuentra un Patrón

**Deliverable del módulo guía:** "Find two strongly correlated variables in a dataset" + scatter
+ coeficiente + escrito corto. El estudiante explora **todas** las columnas numéricas del
dataset (no solo el par ya trabajado en B/C) y elige el par que le parezca más interesante.

> ⚠️ Nota de precisión estadística (GAUSS) — riesgo específico marcado para esta unidad en
> `04_GAUSS.md`: *"'Find two strongly correlated variables' is a built-in spurious-correlation
> trap if the dataset has many columns."* Con suficientes columnas numéricas, algún par va a
> correlacionar fuerte por pura coincidencia. La instrucción del mini-proyecto debe enseñar ese
> riesgo activamente, no caer en él sin querer. Requisitos de diseño para el ejercicio (no
> opcionales):
> 1. El escrito debe incluir, además del r y el scatter, **una hipótesis de por qué esas dos
>    variables podrían estar relacionadas** — no basta con reportar el número más alto.
> 2. Una pregunta de reflexión explícita (probablemente `check_tN` o `check_intexN`, a definir
>    con ATLAS): *"si exploraste 8 columnas y comparaste todos los pares posibles, ¿por qué no
>    deberías confiar automáticamente en el par con el r más alto?"* — convierte el riesgo en
>    parte del aprendizaje evaluado, no en una nota al pie.
> 3. Evitar el marco "ganaste si encontraste el r más alto" en cualquier gamificación (nota para
>    PIXEL) — recompensar la caza del número más alto entrena exactamente el hábito que este
>    punto intenta prevenir.

**Continuidad hacia la Semana 5 (importante, no obvio desde este documento solo):** el par de
variables, el r, y la hipótesis que el estudiante escribe aquí **son el material crudo que la
Semana 5 usa** — el módulo guía especifica que el debunking de la Semana 5 se hace *"using their
own dataset's correlated variables as evidence."* El formato del escrito de este mini-proyecto
debe quedar en una forma reutilizable (variable A, variable B, r, hipótesis) — quien diseñe la
Semana 5 necesita poder leer esto directamente, no re-derivarlo. Marcado también en
`WORKFORCE_HANDOFF.md` (ver entrada de Change Log abajo).

---

## 3. Por qué este orden funciona como Semanas 3–4

La apertura entrena el ojo sin darle nombre al patrón → la Sección 1 le da nombre formal a lo que
el ojo ya reconoció, y planta la advertencia de causalidad antes de que exista la tentación de
usarla → la Sección A deja al estudiante predecir con su propio criterio ya entrenado → la
Sección B mide esa predicción contra la realidad, reforzando o corrigiendo la intuición → la
Sección C descubre que "el patrón general" puede no ser toda la historia → el mini-proyecto de la
Semana 4 suelta al estudiante a explorar solo, con la disciplina de las secciones anteriores ya
internalizada, y su hallazgo se convierte en la materia prima de la Semana 5. Cada bloque
construye la tentación de leer causalidad un poco más — a propósito — sin nunca cederla, para que
la Semana 5 tenga algo genuino que desarmar en vez de un espantapájaros.

---

## 4. Propuesta de reparto de XP (borrador — ATLAS confirma aritmética exacta)

Presupuesto total de la unidad: **~180 XP** (`WORKFORCE_CONTRACT.md` §2). Propuesta inicial,
mismo estilo que el reparto ya usado en Semanas 1–2 (no vinculante hasta que ATLAS fije specs de
ejercicio exactos):

| Bloque | XP propuesto |
|---|---|
| Apertura | 0 (no graduada, mismo patrón que Semanas 1–2) |
| Teoría Desbloqueada (`check_tN` — coeficiente, rango, fuerza/dirección) | ~30 |
| Sección A — Antes de Calcular (predicción + scatter propio) | ~15 |
| Sección B — Calcúlalo (`.corr()`) | ~35 |
| Sección C — Por Subgrupos (`.groupby()` + `.corr()`) | ~40 |
| Integración / Mini-Proyecto (Semana 4) | ~50 |
| **Subtotal (`_CORE_MAX` propuesto)** | **~170** |
| `check_retoN` (bonus, separado de `_CORE_MAX`) | a definir |

Deja ~10 XP de margen frente al presupuesto de 180 antes de sumar `check_debugN` — mismo patrón
de "el presupuesto real se ajusta cuando existen specs de ejercicio concretos" que ya pasó en
Semanas 1–2 (ticket #11).

---

## 5. Propuesta de reparto Semana 3 / Semana 4 (pendiente de confirmar contra horario real)

**No asumir todavía** que esto se divide en dos archivos de notebook — Semanas 1–2 solo se
dividieron en dos archivos después de confirmar que el horario real eran dos sesiones de ~90 min
separadas por una semana (`WORKFORCE_CONTRACT.md` §2, Change Log 2026-08-05). Si el horario de
Semanas 3–4 resulta ser el mismo patrón, la división propuesta (siguiendo el mismo corte "Fin de
la Clase 1" que ya funcionó) sería:

- **Semana 3 (Clase 1):** Apertura + Teoría Desbloqueada + Sección A + Sección B
- **Semana 4 (Clase 2):** Sección C + Integración / Mini-Proyecto

Confirmar con el horario real antes de fijar esto en `WORKFORCE_CONTRACT.md` §2.

---

## Notas internas / pendientes

- **Bloqueante para todo lo demás:** descargar y confirmar el dataset real (World Happiness
  Report, o la alternativa World Bank indicators mencionada en `WORKFORCE_HANDOFF.md`) — ningún
  número de este documento es real todavía. Abre formalmente el trabajo de GAUSS en ticket #7.
- Confirmar que el CSV elegido tiene una columna categórica utilizable para la Sección C
  (región/continente o equivalente) — si la versión del dataset no la trae, hay que buscar una
  versión que sí, o el `.groupby()` de la Sección C no tiene sobre qué agrupar.
- GAUSS debe identificar, dentro del dataset real, un par fuerte y un par débil/nulo genuinos
  para la apertura (Sección 0) — no fabricar un contraste artificial.
- Tema visual y nombre final de "Misión 2" pendientes de PIXEL (ticket #2, arco narrativo del
  bimestre completo) — este documento usa lenguaje neutro a propósito, mismo criterio que
  Semanas 1–2.
- El banco de preguntas `check_tN` (siguiendo el patrón de
  `Preguntas_Teoricas_Semanas1-2.md`) debe esperar a que el dataset esté vetado — las preguntas
  necesitan valores reales, no plantillas abstractas, mismo criterio que Semanas 1–2.
- Recordatorio explícito para quien diseñe la Semana 5: el mini-proyecto de la Semana 4 (Sección
  D/Integración arriba) es su insumo de entrada — no reconstruir el hallazgo del estudiante desde
  cero.
- Recordatorio explícito: no reutilizar el ejemplo de helados/ahogamientos aquí — reservado para
  la apertura de la Semana 5.

---

*Última actualización: 2026-08-14*
*Autor: SOFIA (contenido pedagógico) — vetting de dataset y validación estadística pendiente de GAUSS*

# Semanas 1–2: Teoría — "Misión 1: Recuperación de Datos"

**Estado:** Borrador de contenido (SOFIA) — pendiente de tematización final (PIXEL, ticket abierto
#2 en `WORKFORCE_HANDOFF.md`) y de validación estadística formal (GAUSS).
**Estructura de secciones:** ya fijada en `WORKFORCE_CONTRACT.md` §2 (Sección A Aterrizaje →
B Reconocimiento → C Filtra el Ruido → D Compara Grupos → Integración → Reto bonus).
**Datasets:** INEI (indicadores regionales del Perú, Secciones A–B) y "120 Years of Olympic
History" (Sección C–D). Ya aprobados por GAUSS el 2026-08-02.

> Nota de lenguaje: todo el texto orientado al estudiante va en español; nombres de variables,
> funciones y código permanecen en inglés, según convención del curso (`COURSE_TEMPLATE.md`).
> El wrapper narrativo abajo usa un placeholder genérico ("Comando", "la señal") hasta que PIXEL
> cierre el tema visual — la teoría y el orden pedagógico no cambian cuando eso se defina.

---

## 0. Apertura — El Gancho (antes de cualquier código)

**Objetivo:** que el primer minuto del bimestre incomode productivamente, no que enseñe sintaxis.

> *"Dos titulares. Los dos hablan de lo mismo. Los dos son 'correctos'. ¿Cuál le creerías?"*

Se presentan dos afirmaciones reales y contradictorias en apariencia sobre el mismo indicador
regional (ejemplo: el ingreso o PBI per cápita promedio de una región del Perú), calculadas
ambas correctamente a partir de los mismos datos — una usando la **media**, otra usando la
**mediana**. No se explica todavía por qué difieren. Se pide a los estudiantes votar cuál
creen que es la "verdadera."

**Revelación:** ambas son correctas. Difieren porque "promedio" nunca fue una sola cosa. Esa
es la apertura de la misión:

> *"Se recibió una señal de datos. Está cruda, sin depurar, posiblemente engañosa si la lees
> mal. Tu misión antes de cerrar la Misión 1: recuperarla, estabilizarla, y aprender a leerla
> con honestidad."*

**Nota para GAUSS / ATLAS:** el ejemplo del gancho debe salir de valores reales del dataset
INEI ya aprobado, no ser inventado — de lo efectivo cae si el estudiante luego descubre que fue
un ejemplo de juguete. Pendiente: calcular la media y mediana reales del indicador elegido antes
de fijar los números exactos en el notebook.

---

## 1. Teoría Desbloqueada — Fundamentos (bloque formal, antes de la Sección A)

Este es el bloque de teoría **formal y nombrada explícitamente** — no basta con que el
estudiante "intuya" el concepto; debe poder nombrarlo. Se evalúa luego con preguntas
`check_t1`, `check_t2`, etc. (ver borrador de preguntas en la sección 5).

### 1.1 ¿Qué es la Estadística?

**Definición:** la estadística es la ciencia de recolectar, organizar, analizar e interpretar
datos para tomar decisiones informadas y entender el mundo.

**¿Por qué importa?** No es un ejercicio académico abstracto — es la herramienta que separa
"la opinión de alguien" de "lo que realmente muestra la evidencia." Se usa para:
- **Periodismo:** verificar si un titular sobre "la ciudad más peligrosa" o "el mejor colegio"
  realmente dice lo que parece decir.
- **Medicina:** decidir si un tratamiento funciona mejor que otro.
- **Deporte:** decidir qué jugador fichar según su rendimiento real, no su fama.
- **Gobierno y políticas públicas:** decidir dónde invertir recursos según necesidad real.
- **Negocios:** decidir qué producto funciona, para quién, y por qué.

### 1.2 Las Tres Ramas de la Estadística

| Rama | Pregunta que responde | ¿Dónde aparece en este curso? |
|---|---|---|
| **Descriptiva** | ¿Qué pasó? | Semanas 1–5 — el núcleo de este módulo |
| **Predictiva** | ¿Qué es probable que pase? | Semana 6 (regresión lineal) |
| **Prescriptiva** | ¿Qué deberíamos hacer al respecto? | Se nombra por completitud (ejemplos de medicina/negocios); **este curso no construye una herramienta prescriptiva** |

> ⚠️ Nota de precisión estadística (GAUSS): el agrupamiento (k-means, Semana 7) es
> **descriptivo/exploratorio** — agrupa lo que ya existe — **no es predictivo**. Es un error común
> confundirlo con predicción; el material debe evitarlo explícitamente.

### 1.3 Media, Mediana y Moda — definidas formalmente

- **Media (promedio):** la suma de todos los valores dividida entre la cantidad de valores.
  Sensible a valores extremos — un solo valor muy alto o muy bajo puede "jalar" la media.
- **Mediana:** el valor central de los datos una vez ordenados de menor a mayor. Resistente a
  valores extremos.
- **Moda:** el valor que se repite con más frecuencia. Es la más útil cuando los datos son
  categóricos (no numéricos) — ahí la media y la mediana muchas veces no aplican.

**El pago de la apertura:** cuando media y mediana difieren mucho, **eso es información, no
ruido** — indica que la distribución está sesgada (hay valores extremos jalando la media). No
se enseña "la mediana es más correcta"; se enseña que **cuál usar depende de qué se quiere
describir con honestidad**.

### 1.4 Dispersión (adelanto conceptual para la Sección B)

Además de "dónde está el centro" (media/mediana/moda), una pregunta igual de importante es
"qué tan dispersos están los datos" — introducida formalmente como **desviación estándar** en
la Sección B: en lenguaje simple, "en promedio, qué tan lejos está cada dato del centro."

---

## 2. Teoría por Sección (bloques cortos, cada uno justo antes de su ejercicio)

Regla del curso: teoría → mini-ejercicio inmediato → check → siguiente teoría. Nunca volcar
toda la teoría de una sola vez (`COURSE_TEMPLATE.md` §4). Los bloques de abajo son las
"dosis" que preceden a cada sección ya fijada en el contrato.

### Sección A — Aterrizaje (`.head()`, `.info()`)

Un dataset es una tabla de **observaciones** (filas) y **variables** (columnas) — no es "la
verdad absoluta," es un **registro** de algo, que puede estar incompleto o tener errores.
`.head()` e `.info()` no son sintaxis para memorizar: son **reconocimiento** — antes de
analizar cualquier cosa, hay que revisar qué se tiene realmente entre manos. Plantar la idea de
que valores faltantes, tipos de datos raros, o un número de filas inesperado son cosas que solo
se detectan si se mira primero.

### Sección B — Reconocimiento (`.describe()`, media/mediana/desviación estándar)

Aquí se formaliza con datos reales el conflicto planteado en la apertura. Usar el dataset INEI
directamente: si el PBI per cápita por departamento está sesgado (Lima jalando la media hacia
arriba), ese es el ejemplo real que paga la promesa de la apertura.

### Sección C — Filtra el Ruido (filtrado booleano, valores atípicos,)

Filtrar es **hacerle una pregunta específica a los datos** ("muéstrame solo los atletas mayores
de 30 años"), no un truco de sintaxis.

> ⚠️ Nota de precisión estadística (GAUSS) — la más importante de esta semana: un **valor
> atípico (outlier)** es una observación inusual, **no** es automáticamente un error o "dato
> malo." Confundir ambas cosas es el malentendido más común en estudiantes nuevos a
> estadística. Usar los valores extremos reales del dataset olímpico (edad, altura, peso) —
> son atípicos genuinos, no fabricados, así el concepto se sostiene sobre datos verdaderos.

### Sección D — Compara Grupos (`.groupby()`)

Comparar promedios por subgrupo es donde vive el verdadero hallazgo: "el promedio general
puede esconder lo que realmente pasa dentro de cada grupo."

> ⚠️ Nota de precisión estadística (GAUSS): agregar una sola frase de humildad aquí, sin
> convertirla en una clase completa (eso es trabajo protegido de la Semana 5): *"comparar
> grupos muestra qué es diferente, no por qué es diferente."* Es la barrera mínima contra una
> lectura causal prematura, sin gastar el presupuesto de la Semana 5 antes de tiempo.

---

## 3. Por qué este orden funciona como primera sesión

La apertura crea la necesidad de la Sección A (no se puede resolver el enigma sin mirar datos
reales primero) → el reconocimiento de A crea la necesidad de las estadísticas de B → la
tensión media/mediana de B crea la necesidad del concepto de valor atípico en C (los atípicos
son *la razón* por la que media y mediana no coinciden) → los extremos de C crean la necesidad
de comparar grupos en D. Cada bloque de teoría responde una pregunta que dejó abierta el
anterior — así se siente como una historia, no como un temario, incluso antes de que PIXEL
defina el tema visual completo.

---

## 4. Patrón para las semanas siguientes (para consistencia, no para esta semana)

Cada notebook futuro debe abrir con su propio bloque "Teoría Desbloqueada" — nombrando
formalmente el concepto de esa semana antes de practicar, evaluado con `check_tN`:

| Semana | Teoría formal a introducir |
|---|---|
| 1–2 | Qué es la estadística; ramas descriptiva/predictiva/prescriptiva; media/mediana/moda; dispersión |
| 3–4 | Coeficiente de correlación: definición formal, rango (-1 a 1), fuerza vs. dirección |
| 5 | Causalidad vs. correlación: distinción formal; variable de confusión (confounder), definida |
| 6 | Regresión: variable dependiente/independiente, significado de pendiente e intercepto |
| 7 | Agrupamiento (clustering): aprendizaje no supervisado, centroide — definido, no derivado |

---

## 5. Preguntas `check_tN` (Semana 1–2)

Movidas a su propio documento para no duplicar contenido:
**`Preguntas_Teoricas_Semanas1-2.md`** (mismo folder) — banco de 12 preguntas de opción
múltiple, una por concepto formal de este documento, organizadas por sección A–D más el bloque
de fundamentos, con distractores y tabla de puntaje sugerido para ATLAS.

---

## Notas internas / pendientes

- Confirmar con GAUSS los valores reales (media/mediana) del indicador INEI elegido para la
  apertura antes de fijarlos en el notebook — no publicar un número sin verificar contra el
  dataset real.
- Tema visual (nombres de misión, paleta, flavor text) pendiente de PIXEL — ticket #2 en
  `WORKFORCE_HANDOFF.md`. Este documento usa lenguaje neutro a propósito para no bloquear
  el trabajo de contenido mientras eso se resuelve.
- Preguntas `check_tN` ahora viven en `Preguntas_Teoricas_Semanas1-2.md` — ATLAS debe fijar
  puntaje exacto dentro del presupuesto de ~150 XP de la sección (`WORKFORCE_CONTRACT.md` §2).

---

*Última actualización: 2026-08-03*
*Autor: SOFIA (contenido pedagógico) — validación estadística pendiente de GAUSS*

# Instrucciones de Build — Semana 7 (Sheets): "Caso 2 — El Informe Visual"

**Para:** agente de build (Claude Cowork).
**Estado:** borrador listo para construir la plantilla real de Google Sheets. Contenido
pedagógico propuesto en esta sesión (rol SOFIA) con las convenciones de validación de ATLAS
(`WORKFORCE/03_ATLAS.md`) ya aplicadas a las decisiones de datos/grading de abajo. Validación
estadística final de GAUSS, Theme Brief de PIXEL, y contrato definitivo de Apps Script de ATLAS
siguen pendientes (ver Sección 10) — **no bloquean construir la plantilla**, mismo criterio que
usaron los builds de Semana 1 y Semana 2.
**Fuentes:** `Bimestre3_Statistics_Sheets_Module_Guide.md` (sección "Week 7: El Informe Visual" y
"Pedagogical Guardrails"), `WORKFORCE/03_ATLAS.md`, `COURSE_TEMPLATE.md` §4/§6/§8/§10,
`Instrucciones_Build_Semana1_Sheets.md` / `Instrucciones_Build_Semana2_Sheets.md` (mismo folder
padre, `Weeks 1-2 (Sheets)/`) como precedente estructural.

---

## 0. Alcance de este build — Semana 7, caso nuevo e independiente

### 0.1 Decisión de diseño: no continúa el dataset de la Kermés (Caso 1)

El module guide describe la Semana 7 como "dado el mismo dataset, practica eligiendo entre
gráficos de barra, torta y línea" — en el caso general del módulo, ese dataset ya trae consigo
PROMEDIO/MEDIANA/MODA calculados en Semanas 3–5. Pero **las Semanas 3–6 (Sheets) todavía no están
escritas** (`WORKFORCE_HANDOFF.md`, ticket #7: "Weeks 6, 7... still not drafted"), así que no
existe todavía un Caso 1 extendido con esos tres números ya calculados sobre el dataset de la
Kermés.

**Decisión, documentada en vez de asumida en silencio:** esta semana usa un **dataset nuevo y
autocontenido, "Caso 2"** — no una extensión de `Caso1_Semana1_AbriendoElCaso_v4.xlsx`. Los
estudiantes ya conocen las cuatro fórmulas (asumido: fueron enseñadas en algún momento entre
Semana 3 y Semana 6, aunque esas semanas no estén documentadas aún en este repo); esta plantilla
las **repasa aplicándolas a evidencia nueva**, no las enseña desde cero. Si Semanas 3–6 se
redactan más adelante con el dataset de la Kermés, este documento puede revisarse para continuar
esa línea en vez de usar Caso 2 — marcado explícitamente como decisión abierta a reconsiderar, no
como error.

### 0.2 Qué cubre este build

| Actividad (del module guide) | ¿Incluida? |
|---|---|
| Repaso rápido: organizar evidencia + los 4 números (SUMA/PROMEDIO/MEDIANA/MODA) | ✅ Sí — aplicado a Caso 2, no enseña las fórmulas desde cero |
| Elegir el gráfico correcto (barra/torta/línea) según la pregunta | ✅ Sí — contenido central nuevo de esta semana |
| Armar un informe de una página: gráfico + los 4 números + interpretación | ✅ Sí |

---

## 1. Estructura de pestañas

| Pestaña | Contenido | ¿Se califica? |
|---|---|---|
| 🗂️ **Configuración** | DNI/nombre/grado del estudiante (mismo patrón que `ATLAS_Handoff_Caso1_Semana1_API_DB.md` §2) | No |
| 📋 **Instrucciones** | Teoría corta, leyenda de iconos, narrativa del caso (§2) | No |
| 🔍 **Ejemplo Resuelto** | Mini-caso ya resuelto, los 3 gráficos ya construidos correctamente (§4) | No |
| 📊 **Datos** | El dataset crudo de 26 filas (§3) | No directamente — se recalcula desde aquí |
| 🧩 **Tu Caso** | Todos los ejercicios de esta semana (§5–§8) | **Sí — vía API** |
| 🔒 **Clave** | Respuestas estáticas de las preguntas de teoría (§9) | No (oculta) |

**Leyenda de iconos** — idéntica a Semanas 1–2, sin cambios (`COURSE_TEMPLATE.md` §4):

| Icono | Etiqueta | Acción del estudiante |
|---|---|---|
| 👀 | OBSERVA | Mirar sin modificar nada |
| ✏️ | MODIFICA | Editar una celda o formato existente |
| 🧩 | COMPLETA | Reemplazar `___` por el valor correcto |
| 🔨 | CONSTRUYE | Ejecutar una acción desde cero (aplicar filtro, insertar gráfico) |
| 🔧 | DEBUG | Encontrar el valor correcto pese a un error ya presente |
| ❓ | TEORÍA | Pregunta de opción múltiple |
| ✅ | VERIFICA | Checkpoint que la API valida |

Sigue sin existir Theme Brief final de PIXEL — usar el placeholder neutro **"la Agencia"** en
todo texto narrativo, sin colores de marca hardcodeados, mismo criterio que Semanas 1–2.

---

## 2. Pestaña "Instrucciones" — contenido exacto

1. **Título:** "Caso 2: El Informe Visual — Semana 7"
2. **Gancho de apertura:**

   > *"Ya sabes ordenar evidencia. Ya sabes encontrar el total, el promedio, la mediana y el
   > patrón más común. Pero un detective de verdad no solo calcula — comunica. Tu jefe de agencia
   > tiene 30 segundos para leer tu informe antes de la siguiente reunión. Un gráfico bien
   > elegido dice más, más rápido, que una tabla llena de números."*
   >
   > *"Esta semana te llegó un nuevo caso: los reportes que recibió la Agencia durante una semana
   > completa. Tu trabajo es organizarlos, calcular los cuatro números que ya conoces, elegir el
   > gráfico correcto para cada pregunta, y armar el informe final."*

3. **Los 4 pasos de esta sesión:** 🗂️ Organiza la Evidencia → 🧮 Los Cuatro Números → 📊 Elige el
   Gráfico Correcto → 📝 Arma el Informe → 🎁 Reto bonus.
4. Leyenda de iconos (tabla de §1).
5. Nota corta: "Cuando termines, tu profesor(a) revisará tu hoja con el botón **Enviar para
   calificar** al final de la pestaña Tu Caso."

---

## 3. Pestaña "Datos" — el dataset (26 filas, no modificar)

Colocar exactamente estas 26 filas en una tabla con encabezados `N°`, `Día`, `Tipo de Caso`
(columnas A–C, encabezado en fila 3, datos en filas 4–29):

| N° | Día | Tipo de Caso |
|---|---|---|
| 1 | Lunes | Objeto perdido |
| 2 | Lunes | Objeto perdido |
| 3 | Lunes | Pelea de patio |
| 4 | Martes | Objeto perdido |
| 5 | Martes | Objeto perdido |
| 6 | Martes | Objeto perdido |
| 7 | Martes | Pelea de patio |
| 8 | Martes | Broma pesada |
| 9 | Martes | Rumor falso |
| 10 | Miércoles | Objeto perdido |
| 11 | Miércoles | Objeto perdido |
| 12 | Miércoles | Pelea de patio |
| 13 | Miércoles | Broma pesada |
| 14 | Jueves | Objeto perdido |
| 15 | Jueves | Objeto perdido |
| 16 | Jueves | Pelea de patio |
| 17 | Jueves | Pelea de patio |
| 18 | Jueves | Broma pesada |
| 19 | Jueves | Broma pesada |
| 20 | Jueves | Rumor falso |
| 21 | Jueves | Rumor falso |
| 22 | Jueves | Otro |
| 23 | Viernes | Objeto perdido |
| 24 | Viernes | Pelea de patio |
| 25 | Viernes | Broma pesada |
| 26 | Viernes | Otro |

**Márgenes verificados en esta sesión** (recontar antes de publicar, mismo criterio que Semanas
1–2 — esto no reemplaza el sign-off de GAUSS):

- **Por día:** Lunes = 3, Martes = 6, Miércoles = 4, Jueves = 9, Viernes = 4 → total = **26**.
  Ordenados: 3, 4, 4, 6, 9 → **mediana = 4** (5 valores, sin empate en el punto medio, no hace
  falta promediar dos valores centrales). Promedio = 26 / 5 = **5.2**.
- **Por tipo:** Objeto perdido = 10, Pelea de patio = 6, Broma pesada = 5, Rumor falso = 3,
  Otro = 2 → total = **26**. Moda = **"Objeto perdido"** (10, sin empate con el segundo lugar).
- Ambos márgenes suman 26 de forma independiente — es una verificación cruzada intencional, no
  una coincidencia a resolver (ver nota en §6.1).

---

## 4. Pestaña "Ejemplo Resuelto"

Un mini-caso paralelo, ya resuelto, tema distinto ("El Comedor Escolar" — quejas recibidas en una
semana, 10 filas, 3 categorías) para no filtrar las respuestas del caso real. Debe mostrar:

- La tabla de frecuencia por categoría ya construida.
- Los tres tipos de gráfico ya insertados correctamente, cada uno etiquetado con la pregunta que
  responde (ej. "¿Cuál queja fue más común?" → barras; "¿Qué porcentaje del total representa cada
  queja?" → torta; "¿Cómo cambiaron las quejas día a día?" → líneas).
- Una interpretación modelo de una oración: *"La mayoría de las quejas fueron sobre la fila
  demasiado lenta (6 de 10), y el jueves fue el día con más reportes — probablemente por el menú
  especial."*
- Texto de cierre, adelanto de Semana 8: *"La próxima semana el caso lo eliges tú."*

---

## 5. Sección A — Organiza la Evidencia (~30 XP)

| Clave | Icono | Instrucción | Respuesta esperada | XP |
|---|---|---|---|---|
| `ex1` | 👀🧩 | "Sin editar nada todavía: ¿cuántos casos nuevos reportó la Agencia esta semana? (cuenta las filas de evidencia, sin contar el encabezado)" | `26` | 5 |
| `ex2` | 🔨🧩 | "Construye una tabla de conteo por día: aplica un filtro en la columna Día mostrando solo 'Lunes', selecciona las celdas visibles de esa columna y lee 'Cuenta: ___' en la barra inferior derecha. Anota ese número. Repite para cada día de la semana." | Lunes=`3`, Martes=`6`, Miércoles=`4`, Jueves=`9`, Viernes=`4` | 10 |
| `ex3` | 🔨🧩 | "Construye una tabla de frecuencia por tipo de caso: mismo método que `ex2`, pero filtrando la columna Tipo de Caso, una categoría a la vez." | Objeto perdido=`10`, Pelea de patio=`6`, Broma pesada=`5`, Rumor falso=`3`, Otro=`2` | 10 |
| `t1` | ❓ | MC: *"¿Por qué conviene organizar la evidencia en una tabla de conteo antes de buscar el total o el patrón más común? a) Porque se ve más ordenado, nada más, b) Porque contar celda por celda a simple vista es lento y fácil de equivocarse, c) Porque Google Sheets lo exige, d) Porque así el archivo pesa menos"* | `b` | 5 |
| `check_mini_a` | ✅ | Checkpoint — gate: `ex1`+`ex2`+`ex3`+`t1` correctos antes de desbloquear Sección B | — | 0 (solo gate) |

**Nota de diseño (reutiliza, no inventa, técnica de Semana 1):** ni `ex2` ni `ex3` introducen una
fórmula nueva (nada de `CONTAR.SI`, fuera del alcance técnico declarado en el module guide) —
reusan exactamente la lectura de la barra de estado bajo un filtro activo que ya enseñó la
Sección D de Semana 1, ahora leyendo "Cuenta" en vez de "Suma".

---

## 6. Sección B — Los Cuatro Números (~50 XP)

| Clave | Icono | Instrucción | Respuesta esperada | XP |
|---|---|---|---|---|
| `ex4` | 🧩 | "Usando tu tabla de conteo por día (`ex2`), escribe `=SUMA()` sobre los 5 valores. ¿Cuántos casos en total recibió la Agencia esta semana?" | `26` | 10 |
| `ex5` | 🧩 | "Sobre los mismos 5 valores, escribe `=PROMEDIO()`. ¿Cuál es el promedio de casos por día?" | `5.2` | 10 |
| `debug1` | 🔧 | "Un compañero ficticio escribió `=PROMEDIO(B2:B5)` en vez de `B2:B6` — le faltó el valor del viernes — y obtuvo 5.5. ¿Cuál es el promedio *correcto*, usando los 5 días completos?" | `5.2` | 5 |
| `ex6` | 🧩 | "Sobre los mismos 5 valores, escribe `=MEDIANA()`. ¿Cuál es la mediana de casos por día?" | `4` | 10 |
| `ex7` | 👀🧩 | "`MODA()` de Sheets solo funciona con números — Tipo de Caso es texto. Mira tu tabla de frecuencia (`ex3`) y escribe a mano cuál categoría es la moda (la más frecuente)." | `Objeto perdido` | 10 |
| `t2` | ❓ | MC: *"¿Cuál de los cuatro números responde mejor la pregunta 'qué tipo de caso reportó la Agencia con más frecuencia esta semana'? a) SUMA, b) PROMEDIO, c) MEDIANA, d) MODA"* | `d` | 5 |
| `check_mini_b` | ✅ | Checkpoint — gate: `ex4`+`ex5`+`debug1`+`ex6`+`ex7`+`t2` correctos antes de desbloquear Sección C | — | 0 (solo gate) |

**Nota técnica para quien construya el grader (`ex7`):** el criterio de corrección es el string
de texto `"Objeto perdido"` (case-insensitive, mismo patrón que la teoría), **no** un valor
numérico — es la única clave de esta semana con esa forma. No intentar validar con `MODA()`
sobre la columna de texto; Sheets la rechaza.

---

## 7. Sección C — Elige el Gráfico Correcto (~45 XP)

Tres rondas, cada una: una pregunta de teoría con marco de "compañero que eligió mal" (fuerza
razonar el *por qué*, no solo memorizar la lista barra/torta/línea) + un ejercicio de construir
el gráfico correcto.

### Ronda 1 — Barras (comparar categorías)

| Clave | Icono | Instrucción | Respuesta esperada | XP |
|---|---|---|---|---|
| `t3` | ❓ | MC: *"Un compañero usó un gráfico de LÍNEAS para comparar cuántos casos hay de cada tipo (Objeto perdido vs. Pelea de patio vs. ...). ¿Por qué no es la mejor opción? a) Porque son categorías separadas, no un cambio continuo — un gráfico de barras compara mejor, b) Porque el gráfico de líneas está perfecto así, c) Barras es la única opción que existe, d) No importa, cualquiera sirve"* | `a` | 5 |
| `ex8` | 🔨 | "Usando tu tabla de frecuencia por tipo (`ex3`), inserta un gráfico de **barras** (Insertar → Gráfico) que compare cuántos casos hay de cada categoría." | Gráfico tipo barra/columna, rango = tabla de frecuencia de `ex3` | 10 |

### Ronda 2 — Torta (partes de un todo)

| Clave | Icono | Instrucción | Respuesta esperada | XP |
|---|---|---|---|---|
| `t4` | ❓ | MC: *"Un compañero usó un gráfico de BARRAS para mostrar qué porcentaje del total representa cada tipo de caso. Funciona, pero ¿qué gráfico comunica 'partes de un todo' de forma más directa? a) Torta, porque muestra cada categoría como una porción del 100%, b) Líneas, c) Barras es la única opción, d) Ninguno, mejor una tabla"* | `a` | 5 |
| `ex9` | 🔨 | "Con la misma tabla de frecuencia (`ex3`), inserta un gráfico de **torta** que muestre qué porcentaje del total representa cada tipo de caso." | Gráfico tipo torta (pie), rango = tabla de frecuencia de `ex3` | 10 |

### Ronda 3 — Líneas (cambio en el tiempo)

| Clave | Icono | Instrucción | Respuesta esperada | XP |
|---|---|---|---|---|
| `t5` | ❓ | MC: *"Un compañero graficó los casos por día usando un gráfico de TORTA. ¿Por qué es una mala elección para mostrar cómo cambió el número de casos día a día? a) Una torta no muestra secuencia ni tendencia en el tiempo — un gráfico de líneas sí, b) La torta está bien así, c) Barras es la única opción, d) No importa, cualquiera sirve"* | `a` | 5 |
| `ex10` | 🔨 | "Usando tu tabla de conteo por día (`ex2`), inserta un gráfico de **líneas** que muestre cómo cambió el número de casos a lo largo de la semana." | Gráfico tipo línea, rango = tabla de conteo por día de `ex2` | 10 |

`check_mini_c` (✅, 0 XP, solo gate): `t3`+`ex8`+`t4`+`ex9`+`t5`+`ex10` correctos antes de
desbloquear Sección D.

---

## 8. Sección D — Arma el Informe (~15 XP, Integración)

| Clave | Icono | Instrucción | Respuesta esperada | XP |
|---|---|---|---|---|
| `intex1` | 🧩 | Completar: *"Esta semana la Agencia recibió **___** casos en total (SUMA), con un promedio de **___** casos por día (PROMEDIO) y una mediana de **___** (MEDIANA). El tipo de caso más común fue **___** (MODA)."* — cuatro celdas de respuesta separadas | `26`, `5.2`, `4`, `Objeto perdido` | 10 |
| `intex2` | 📝 | "En una oración, explica cuál de tus tres gráficos elegirías como el centro de tu informe final y por qué." — texto libre, sin respuesta única | Gradeable por esfuerzo, no por valor — ver nota abajo | 5 |

**Nota sobre `intex2` (effort, no correctness):** igual que `ex3` de Semana 1
(`Instrucciones_Build_Semana1_Sheets.md` §3.2) — no existe infraestructura de grading por IA para
el track de Sheets todavía (a diferencia del track de Python, `grade-reflexion`). Criterio:
texto no vacío, longitud mínima razonable (ej. ≥ 15 caracteres), sin validar contenido. No
bloquear el envío final por esto — es el mismo patrón "sí/no se intentó" que `ex3`.

`intex1` es la última clave antes del bloque "Resumen para enviar" / botón **"Enviar para
calificar"** (mismo mecanismo que Semanas 1–2).

---

## `reto1` — Bonus (🎁, 10 XP, separado de `_CORE_MAX`)

"En una pestaña o zona aparte marcada 'Reto', construye a propósito un gráfico que sea una **mala
elección** para estos datos (ejemplo: un gráfico de torta comparando los 5 días en vez de los 5
tipos, o un gráfico de líneas para comparar categorías). Escribe una oración explicando por qué
esa elección sería confusa o engañosa en el informe real."

Callback intencional a la Semana 6 ("Cuidado con las Trampas") sin repetir su contenido — aquí el
estudiante fabrica la mala elección él mismo, en vez de detectarla en un ejemplo ajeno. Gradeable
por esfuerzo (mismo criterio que `intex2`), no por valor exacto.

---

## 9. `🔒 Clave` — respuestas estáticas

```
t1 = "b"
t2 = "d"
t3 = "a"
t4 = "a"
t5 = "a"
```

`ex1`–`ex10`, `debug1`, `intex1` **no van en `🔒 Clave`** — son "numérica/texto vs. fórmula en
vivo", recalculadas siempre contra `📊 Datos`, mismo criterio que Semanas 1–2 (nunca confiar en
el trabajo intermedio del estudiante; recalcular desde el dataset crudo).

---

## 10. XP total y taxonomía de claves

| Sección | XP core |
|---|---|
| A — Organiza la Evidencia | 30 |
| B — Los Cuatro Números | 50 |
| C — Elige el Gráfico Correcto | 45 |
| D — Arma el Informe | 15 |
| **Total `_CORE_MAX`** | **140** |
| `reto1` (bonus) | 10 (`_BONUS_MAX = 10`) |

**Provisional — cercano al ~130 XP que fija el module guide para esta semana, pero no exacto.**
Mismo criterio que Semana 1 (donde el total también quedó "provisional, SOFIA propone, ATLAS
confirma"): ajustar aquí es más barato que forzar una coincidencia exacta con una cifra
aproximada (`~130`) del module guide.

Claves: `ex1`–`ex10` (core), `debug1` (único debug de esta semana), `t1`–`t5` (teoría),
`check_mini_a`/`check_mini_b`/`check_mini_c` (checkpoints, sin XP propio), `intex1`/`intex2`
(integración), `reto1` (bonus). Numeración reinicia en `ex1` — es un caso nuevo, sin
predecesor directo en esta secuencia (mismo criterio que usó Semana 1 al empezar su propia
numeración, y que usó el módulo de Python al abrir Misión 3 en `nb5_regresion.ipynb`).

---

## 11. Contrato de datos para la API (stub — ATLAS confirma el diseño final)

```json
{
  "dni": "<'🗂️ Configuración'!C5>",
  "nombre": "<'🗂️ Configuración'!C4>",
  "grado": "<'🗂️ Configuración'!C6>",
  "notebook": "sheets_caso2_semana7",
  "curso": "STAT_2026",
  "earned": "<suma de puntos obtenidos, sin bonus>",
  "possible": 140,
  "score_breakdown": {
    "ex1": {"e": 5, "p": 5},
    "...": "..."
  }
}
```

- `curso` = `"STAT_2026"`, mismo valor fijo que usan Semanas 1–2.
- `notebook` = `"sheets_caso2_semana7"` es **provisional** — sigue el patrón
  `sheets_caso1_semanaN` que propuso Semana 1, adaptado a `caso2` porque este build usa un
  dataset nuevo (§0.1), no una extensión de Caso 1. ATLAS confirma o reemplaza.
- `intex2` se envía como effort/booleano (`{"e": 5, "p": 5}` si el texto pasa el umbral de
  longitud, `{"e": 0, "p": 5}` si no), igual que `ex3` de Semana 1.

### 11.1 Grading de gráficos — mecanismo nuevo, sin precedente en este repo

Ningún autograder de este proyecto ha calificado un gráfico insertado antes (todos los previos
califican celdas/fórmulas). Propuesta concreta para que ATLAS la confirme o la reemplace:

```js
function _checkChart(sheet, expectedType) {
  return sheet.getCharts().some(c => c.getChartType() === expectedType);
}
// expectedType: Charts.ChartType.COLUMN | Charts.ChartType.PIE | Charts.ChartType.LINE
```

**Recomendación:** validar por **tipo de gráfico presente en la hoja**, no por coincidencia
exacta de rango A1 — igual que el resto del módulo evita confiar en el trabajo intermedio del
estudiante (`ATLAS_Handoff_Caso1_Semana1_API_DB.md` §6), un rango A1 hardcodeado se rompe si el
estudiante inserta una fila antes de construir el gráfico. Si además se quiere validar que el
gráfico usa los datos correctos (no solo el tipo correcto), comparar los valores numéricos que
el gráfico está graficando (`chart.getRanges()` → leer valores) contra los agregados esperados
(ej. la tabla de frecuencia recalculada desde `📊 Datos`), no contra la notación del rango.

---

## 12. Lo que este build deliberadamente NO incluye

- Continuación del dataset de la Kermés (Caso 1) — decisión documentada en §0.1, revisable si
  Semanas 3–6 se redactan más adelante con esa línea narrativa.
- Enseñanza desde cero de PROMEDIO/MEDIANA/MODA — esta semana las repasa aplicadas a datos
  nuevos, no las presenta por primera vez.
- `CONTAR.SI`/`QUERY`/tablas dinámicas — fuera del alcance técnico declarado en el module guide;
  la tabla de frecuencia se construye con filtro + lectura de la barra de estado (§5).
- Tema visual final (nombre de agencia, paleta, achievements) — pendiente de PIXEL.
- El diseño final del Apps Script / endpoint de la API, incluyendo el mecanismo real de
  calificación de gráficos — pendiente de ATLAS (§11 es un contrato provisional).

---

## 13. Pendientes antes de publicar a estudiantes reales

1. **GAUSS:**
   - Confirmar los márgenes de §3 (26 filas, split 3/6/4/9/4 por día, 10/6/5/3/2 por tipo,
     mediana=4, promedio=5.2, moda="Objeto perdido") — verificación aritmética hecha en esta
     sesión, no reemplaza el sign-off formal.
   - Confirmar que el diseño de `intex1` (SUMA de la tabla de conteo diario = mismo número que
     `ex1`, un conteo directo de filas) es pedagógicamente válido y no confunde SUMA con CONTAR
     — es una coincidencia matemática intencional (partición suma al total), documentada en §3,
     no un error a corregir.
   - Confirmar que `ex7`/`intex1` piden la moda de texto por lectura visual (no por fórmula) sin
     introducir un precedente confuso sobre qué hace `MODA()` realmente.
2. **PIXEL:** Theme Brief pendiente — este build usa placeholders neutros en todo texto
   narrativo, igual que Semanas 1–2.
3. **ATLAS:**
   - Confirmar el desglose de XP de §10 (140 vs. el ~130 aproximado del module guide).
   - Confirmar o rediseñar el mecanismo de calificación de gráficos de §11.1 — es ingeniería
     nueva, sin precedente en este repo.
   - Confirmar el contrato de §11 (especialmente `notebook` y el manejo de `intex2` como effort).
   - Diseñar el Apps Script real (`AppsScript_Caso2_Semana7.gs` o extender el patrón de
     `AppsScript_Caso1_Semana1.gs`, decisión de ATLAS).
4. **Decisión abierta para quien secuencie el curso:** si Semanas 3–6 (Sheets) se redactan más
   adelante continuando el dataset de la Kermés, decidir si Caso 2 de esta semana se conserva
   como caso independiente o se retira en favor de continuar Caso 1 — no es necesario resolverlo
   ahora, pero vale la pena que quede visible antes de que ambas versiones convivan sin
   reconciliar (mismo tipo de nota que dejó `Instrucciones_Build_Semana1_Sheets.md` §9.4 para su
   propio caso).

---

*Preparado en sesión de brainstorming/spec (rol SOFIA, con convenciones de validación ATLAS
aplicadas a las decisiones de datos y grading) para build de Claude Cowork. Alcance: Semana 7
completa, caso nuevo e independiente ("Caso 2"). No depende de que Semanas 3–6 existan.*
*Fecha: 2026-09-16*

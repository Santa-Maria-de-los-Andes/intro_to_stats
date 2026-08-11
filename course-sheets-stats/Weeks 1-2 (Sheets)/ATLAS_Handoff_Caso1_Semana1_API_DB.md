# Handoff para ATLAS — API y conexión a DB para calificar "Caso 1: Abriendo el Caso" (Semana 1)

**Origen:** SOFIA (contenido pedagógico) + build ejecutado en esta sesión de Cowork.
**Archivo de referencia:** `Caso1_Semana1_AbriendoElCaso_v4.xlsx` (versión entregada al usuario; conviértela a Google Sheet nativo antes de conectar Apps Script — al subirla a Drive, Google la convierte automáticamente).
**Qué NO incluye este documento:** el diseño final del Apps Script ni el endpoint de la API — eso es tu entregable. Este documento fija el contrato de datos y expone exactamente cómo está construida la hoja para que no tengas que hacer ingeniería inversa.

---

## 1. Resumen de una línea

La hoja ya autocalifica 12 de los 14 ítems **en el cliente**, vía fórmulas que leen directamente la pestaña `📊 Datos` y una pestaña oculta de respuestas (`🔒 Clave`). Tu trabajo es construir el disparador real de "Enviar para calificar": leer el estado actual de la hoja, **re-derivar la corrección de forma independiente** (no confiar ciegamente en las celdas ya calculadas — ver §6, es la parte más importante de este documento), y persistir el resultado en la base de datos con el contrato de §4.

---

## 2. Mapa de pestañas (nombres EXACTOS, con emoji — así se debe llamar `SpreadsheetApp.getSheetByName()`)

| Nombre exacto de la pestaña | Propósito | Visible al alumno |
|---|---|---|
| `🗂️ Configuración` | Identidad del alumno (Nombre, DNI, Grado) | Sí |
| `📁 Instrucciones` | Texto introductorio, sin datos que leer | Sí |
| `🔎 Ejemplo Resuelto` | Demo guiada por el profesor, no se califica | Sí |
| `📊 Datos` | Dataset crudo/editable — 108 filas | Sí |
| `🔒 Clave` | Respuestas correctas de los ítems estáticos | **Oculta** (`sheet_state = "hidden"`, NO protegida — ver §6) |
| `🧩 Tu Caso` | Todos los ejercicios, respuestas y XP | Sí |

---

## 3. `🧩 Tu Caso` — mapa exacto de celdas por ejercicio

Estructura de fila por ejercicio: `A` = clave · `B` = instrucción (incluye el XP posible como sufijo de texto, ej. "(+5 XP)") · `C` = respuesta del alumno (input) · `D` = resultado visible (fórmula) · `E` = XP crudo (número, usado para sumar el total — en los ítems autograded está *visualmente oculto* con el mismo color de fuente que el fondo de su fila, pero el valor sigue ahí y es leíble programáticamente).

| Clave | Fila | Tipo de calificación | Respuesta (C) | Resultado (D) | XP (E) | XP posible |
|---|---|---|---|---|---|---|
| `ex1` | 8 | Estática vs. `🔒 Clave` | número | fórmula | fórmula | 5 |
| `ex2` | 9 | Estática vs. `🔒 Clave` | número | fórmula | fórmula | 5 |
| `t1` | 10 | Estática vs. `🔒 Clave` (MC) | `a\|b\|c\|d` | fórmula | fórmula | 5 |
| `debug1` | 11 | Estática vs. `🔒 Clave` | número | fórmula | fórmula | 5 |
| `ex3` | 21 | **Revisión del profesor** | checkbox TRUE/FALSE | texto fijo | **input manual 0–5** | 5 |
| `ex4` | 22 | Live vs. estado de `📊 Datos` | *(sin input — se autoevalúa)* | fórmula | fórmula | 10 |
| `ex5` | 23 | Live vs. estado de `📊 Datos` | *(sin input)* | fórmula | fórmula | 10 |
| `ex6` | 24 | Live vs. estado de `📊 Datos` | *(sin input)* | fórmula | fórmula | 10 |
| `t2` | 25 | Estática vs. `🔒 Clave` (MC) | `a\|b\|c\|d` | fórmula | fórmula | 5 |
| `check_mini_b` | 26 | Checkpoint informativo | — | — | — | 0 |
| `ex9` | 53 | **Revisión del profesor** | checkbox TRUE/FALSE | texto fijo | **input manual 0–5** | 5 |
| `ex10` | 54 | Numérica vs. `SUMIFS` en vivo sobre `📊 Datos` | número | fórmula | fórmula | 10 |
| `ex11` | 55 | Numérica vs. `SUMIFS` en vivo sobre `📊 Datos` | número | fórmula | fórmula | 10 |
| `t3` | 56 | Estática vs. `🔒 Clave` (MC) | `a\|b\|c\|d` | fórmula | fórmula | 10 |
| `check_mini_d` | 57 | Checkpoint informativo | — | — | — | 0 |
| `reto1` (bonus) | 61 | Dinámica vs. `SUMIFS` en vivo | `Viernes\|Sábado\|Empate` | fórmula | fórmula | 10 (no cuenta al core) |

**`_CORE_MAX` = 95** (suma de todo excepto `reto1`). **`_BONUS_MAX` = 10**.

### Bloque "Resumen para enviar" (filas 63–70 de `🧩 Tu Caso`)

Ya agregado y funcional — puedes leerlo directo o recalcularlo tú mismo (recomendado, ver §6):

- `B64` = Nombre del alumno (espeja `🗂️ Configuración!C4`)
- `E64` = DNI (espeja `🗂️ Configuración!C5`)
- `B65` = Grado (espeja `🗂️ Configuración!C6`)
- `E65` = XP autocalificado = `SUM(E8,E9,E10,E11,E22,E23,E24,E25,E54,E55,E56)`
- `B66` = XP revisión profesor(a) = `SUM(E21,E53)` (ex3 + ex9, manual)
- `E66` = XP Bonus = `E61`
- `B67` = **XP Total (con bonus)** = suma de los tres anteriores

El botón "Enviar para calificar" (fila 69) es hoy **solo un marcador visual** — una celda con fondo de color, sin `onEdit`/`onClick` real. Ese es el gap que tu Apps Script debe llenar.

---

## 4. `📊 Datos` — estructura

- Encabezado en fila 4: `Comprador` (A) · `Boletos` (B) · `Día` (C) · `Estado` (D)
- Datos en filas 5–112 (108 filas al entregar la hoja; **el alumno borra filas durante `ex4`**, así que el rango real de datos se reduce a ~90 filas después de la limpieza — nunca asumas 108 filas fijas, siempre usa `getLastRow()` o `COUNTA` sobre la columna A).
- Rango con nombre implícito usado en las fórmulas: `'📊 Datos'!A5:A112`, `B5:B112`, `C5:C112`, `D5:D112` (rango FIJO de 108 filas, aunque el alumno borre filas — las fórmulas de calificación ya están diseñadas para tolerar filas vacías al final del rango; ver la nota de `ex6` en §6).

---

## 5. Contrato de payload — ya establecido en la especificación original del módulo, replicado aquí para no perder consistencia

```json
{
  "dni": "<'🗂️ Configuración'!C5>",
  "nombre": "<'🗂️ Configuración'!C4>",
  "grado": "<'🗂️ Configuración'!C6>",
  "notebook": "sheets_caso1_semana1",
  "curso": "EST1_2026",
  "earned": "<suma total, incluye bonus si corresponde — decide si earned separa bonus o no>",
  "possible": 95,
  "bonus_possible": 10,
  "score_breakdown": {
    "ex1": {"e": 5, "p": 5},
    "ex2": {"e": 5, "p": 5},
    "t1": {"e": 5, "p": 5},
    "debug1": {"e": 5, "p": 5},
    "ex3": {"e": "0-5, manual", "p": 5, "kind": "teacher_review"},
    "ex4": {"e": 10, "p": 10},
    "ex5": {"e": 10, "p": 10},
    "ex6": {"e": 10, "p": 10},
    "t2": {"e": 5, "p": 5},
    "ex9": {"e": "0-5, manual", "p": 5, "kind": "teacher_review"},
    "ex10": {"e": 10, "p": 10},
    "ex11": {"e": 10, "p": 10},
    "t3": {"e": 10, "p": 10},
    "reto1": {"e": 10, "p": 10, "kind": "bonus"}
  },
  "submitted_at": "<timestamp>"
}
```

- `curso` = **`"STAT_2026"`** exacto (fijado en `WORKFORCE_HANDOFF.md`, Done log 2026-08-07 — no uses el placeholder `"bimestre3_estadistica"` de una entrada anterior, quedó superado).
- `notebook` = `"sheets_caso1_semana1"` es **provisional** — sigue el patrón `nb1_semana1`/`nb1_semana2` de Python, pero como este es el primer entregable de Sheets no existe todavía una convención de nombres propia. Decide/confirma tú la convención definitiva.
- Los campos `dni`/`nombre`/`grado` vienen de `🗂️ Configuración` (C5/C4/C6) — la hoja ya bloquea visualmente el inicio si están vacíos (banner en `🧩 Tu Caso!A4`), pero eso es solo una advertencia en pantalla, no una validación real. Tu backend debe rechazar envíos con estos campos vacíos.

---

## 6. LO MÁS IMPORTANTE: no confíes en los valores ya calculados por la hoja

El diseño actual es "autocalificación en el cliente" pensado para dar feedback instantáneo al alumno mientras trabaja — **no fue diseñado como un sistema a prueba de manipulación**. Antes de construir el endpoint de calificación final, ten en cuenta:

1. **Nada está protegido.** Cualquier alumno puede sobrescribir una celda de fórmula (`D` o `E`) con un valor fijo, o desocultar la pestaña `🔒 Clave` (clic derecho → Mostrar hoja) y leer las respuestas directamente. Google Sheets permite esto a cualquier editor salvo que se apliquen *protected ranges* explícitos.
2. **Recomendación:** cuando Apps Script dispare el envío real, **no leas `E65`/`B67` y confíes en ellos**. En su lugar, tu script debe:
   - Leer los valores crudos: las respuestas del alumno (columna `C` en cada fila de ejercicio) y el estado completo de `📊 Datos!A5:D112`.
   - Re-derivar la corrección de cada ítem con la MISMA lógica que ya está en las fórmulas (documentada exercise-by-exercise abajo), pero ejecutada en tu propio código, no leyendo el resultado de Sheets.
   - Solo entonces calcular `earned` y escribirlo en la DB.
   - Esto también resuelve el problema de que un alumno haya "congelado" un ✓ editando la celda directamente — tu recálculo lo ignora.
3. **Aplica `Range.protect()`** al menos sobre `🔒 Clave` (protegida + oculta, no solo oculta) y sobre las columnas `D`/`E` de `🧩 Tu Caso`, para que la UI deje de invitar a hacer trampa aunque tu backend ya no dependa de esos valores.

### Lógica exacta de cada tipo de calificación (para reimplementar en Apps Script/servidor)

**a) Estática vs. clave oculta** (`ex1`, `ex2`, `t1`, `debug1`, `t2`, `t3`):
Comparar la respuesta del alumno contra un valor fijo. Los valores están en `🔒 Clave!B2:B9`:
```
ex1 = 108   (N_RAW — cantidad de filas crudas entregadas; SIEMPRE recalcula esto al construir
             una hoja nueva, no lo hardcodees — depende de cuántas filas tenga el dataset de
             ESE build en particular)
ex2 = 4
debug1 = 108   (mismo valor que ex1)
t1 = "b"    (case-insensitive)
t2 = "c"    (case-insensitive)
t3 = "b"    (case-insensitive)
```
⚠️ Estos números son correctos **para el archivo `_v4.xlsx` actual**. Si regeneras la hoja (dataset nuevo, otro seed), estos valores cambian — la clave de verdad siempre es `🔒 Clave` de la hoja específica que el alumno está usando, no una constante en tu backend.

**b) Live-check contra el estado de `📊 Datos`** (`ex4`, `ex5`, `ex6` — sin input del alumno, se autoevalúan):
- `ex4` correcto ⟺ `COUNTIF(Datos!D:D, "Cancelado") = 0` Y `COUNTA(Datos!A5:A112) = 90` (90 = `N_VALID`, también recalculable, no constante universal).
- `ex5` correcto ⟺ `COUNTA(Datos!A5:A112) = 90` Y `COUNTIF(Datos!C:C,"Viernes") + COUNTIF(Datos!C:C,"Sábado") = 90` (todo el texto de Día ya es exactamente uno de los dos valores canónicos).
- `ex6` correcto ⟺ ninguna fila con Comprador no-vacío tiene Boletos vacío (`SUMPRODUCT((A<>"")*(B=""))=0`) Y `SUM(Datos!B5:B112) = 324` (`SUM_TOTAL_90`, la suma de los 90 boletos ya completos — también recalculable).
  - **Nota de diseño ya resuelta, no la reintroduzcas:** la primera versión de este check usaba `COUNTBLANK` sobre todo el rango fijo de 108 filas, lo cual siempre fallaba porque después de `ex4` quedan ~18 filas vacías al final del rango (por las filas borradas) que `COUNTBLANK` contaba como "boletos faltantes" aunque no lo fueran. El fix fue contar blancos solo donde también hay un Comprador no-vacío en esa fila. Si reimplementas esto en Apps Script, replica el fix, no el bug.

**c) Numérica vs. fórmula en vivo (`SUMIFS`)** (`ex10`, `ex11`, y el bonus `reto1`):
- `ex10` correcto ⟺ `VALUE(respuesta) = SUMIFS(Datos!B5:B112, Datos!C5:C112, "Sábado")`
- `ex11` correcto ⟺ `VALUE(respuesta) = SUMIFS(Datos!B5:B112, Datos!C5:C112, "Viernes")`
- `reto1` correcto ⟺ la respuesta coincide (case-sensitive vía `EXACT`) con: `"Empate"` si ambos SUMIFS son iguales, si no `"Viernes"` o `"Sábado"` según cuál sea mayor.

**d) Revisión del profesor** (`ex3`, `ex9`): no autograded. El alumno marca un checkbox de autorreporte; el puntaje real (0 al máximo, hoy 5 y 5) lo escribe el profesor directamente en la celda `E` correspondiente (`E21` para `ex3`, `E53` para `ex9`). **Decisión de producto pendiente para ti:** ¿el envío a la DB ocurre una sola vez después de que el profesor ya calificó estos dos ítems manualmente, o el alumno envía primero (con 0 en estos dos) y hay un segundo evento de "recalificación" cuando el profesor los completa? La hoja no impone ningún orden — hoy es posible enviar con `E21`/`E53` en blanco.

---

## 7. Checkbox: nota técnica, no bloqueante

Los checkboxes de `ex3`/`ex9` (celda `C`) están guardados en el `.xlsx` como celdas booleanas con validación de datos tipo lista `"TRUE,FALSE"` — un truco para que se comporten como checkbox al importarlas. **Al subir el archivo a Drive, Google Sheets NO los convierte automáticamente a su widget nativo de casilla** — hay que seleccionar esas celdas una vez y usar Insertar → Casilla de verificación (autodetecta los valores TRUE/FALSE existentes y los preserva). Esto es cosmético/UX, no afecta ninguna fórmula ni tu lógica de backend — igual léelos como booleano.

---

## 8. Decisiones de producto que te tocan a ti (no resueltas por este build)

1. **Reenvíos:** ¿la DB guarda cada intento de "Enviar" o solo el último? ¿se puede reenviar después de que el profesor calificó `ex3`/`ex9`?
2. **Datasets por alumno:** hoy TODOS los alumnos que reciban este mismo archivo comparten exactamente el mismo dataset de `📊 Datos` y por lo tanto las mismas respuestas correctas en `🔒 Clave`. Si quieres evitar copia entre compañeros, necesitas un pipeline que genere/clone un dataset distinto por alumno (el script Python que generó este dataset —semilla fija, patrón de duplicados/cancelados/vacíos proporcional— se puede parametrizar con una semilla por alumno; pídemelo si lo necesitas). Si el trabajo es supervisado en clase, puede que no te importe.
3. **Trigger real del botón "Enviar":** hoy es una celda pintada, sin comportamiento. Decide si usas un dibujo asignado a una función de Apps Script (`Insertar → Dibujo`, clásico), un menú personalizado (`onOpen` + custom menu item), o un trigger `onEdit` que detecta cuando se marca cierto checkpoint.
4. **Gate de Configuración:** hoy es solo un mensaje visual (`🧩 Tu Caso!A4`) — no bloquea nada de verdad. Si quieres bloqueo real, necesitas `Protection` a nivel de rango condicionado por script, no es nativo de Sheets con fórmulas.

---

## 9. Dataset ground-truth de este build específico (para pruebas / semilla de tu backend de verificación)

Archivo: `_dataset_ground_truth.json` (adjunto en este mensaje). Contiene, para el dataset exacto embebido en `Caso1_Semana1_AbriendoElCaso_v4.xlsx`:
- las 108 filas crudas tal como aparecen en `📊 Datos` (comprador, boletos o `null` si empieza vacía, día con el casing "sucio" original, estado),
- `n_raw` = 108, `n_valid` = 90, `n_viernes` = 48, `n_sabado` = 42,
- `sum_viernes` = 162, `sum_sabado` = 162, `sum_total_90` = 324,
- `revealed` = los 12 pares (Comprador, Boletos) de la "nueva pista" para `ex6`.

Úsalo para escribir tests automatizados de tu Apps Script/backend sin tener que recalcular todo a mano — pero recuerda: si regeneras la hoja con otra semilla, estos números ya no aplican y hay que regenerar este JSON también.

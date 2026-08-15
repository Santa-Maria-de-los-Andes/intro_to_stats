# Instrucciones de Build — Semana 2 (Sheets): "Caso 1 — Cerrando el Caso"

**Para:** agente de build (Claude Cowork).
**Estado:** listo para construir sobre la plantilla YA ENTREGADA de Semana 1
(`Caso1_Semana1_AbriendoElCaso_v4.xlsx`). Contenido pedagógico de SOFIA, redactado a partir de
la especificación original y reconciliado con los números reales del dataset que Semana 1
efectivamente usó (no los del ejemplo de 18 filas del documento original — ver §0.2). Validación
estadística de GAUSS y confirmación de contrato/Apps Script de ATLAS siguen pendientes (§10),
pero no bloquean construir la plantilla — mismo criterio que se usó para autorizar el build de
Semana 1.
**Fuentes:** `Ejercicios_Practica_Semanas1-2_Sheets.md`, `Teoria_Semanas1-2_Caso1_AbriendoElCaso.md`,
`Instrucciones_Build_Semana1_Sheets.md` y `ATLAS_Handoff_Caso1_Semana1_API_DB.md` (mismo folder —
esta última es la fuente de verdad de cómo quedó *realmente* construida la Semana 1, no el
borrador), `Bimestre3_Statistics_Sheets_Module_Guide.md`, `WORKFORCE/03_ATLAS.md` (convenciones de
tolerancia numérica, grading source, effort vs. skill), `COURSE_TEMPLATE.md` §4/§6/§8/§10.

---

## 0. Alcance de este build — SOLO Semana 2

### 0.1 Qué cubre

Este documento cierra la mitad que `Instrucciones_Build_Semana1_Sheets.md` (§0, §8) dejó
explícitamente pendiente:

| Sección | ¿Incluida en este build? |
|---|---|
| A — Recepción del Caso | Ya construida en Semana 1. No se toca. |
| B — Limpieza | Ya construida en Semana 1 (ampliada). No se toca. |
| C — El Total (`=SUMA()`) | ✅ **Sí — el contenido central de este build** |
| D — Filtrado Básico | Ya construida en Semana 1 (adaptada, sin `SUMA()`). No se toca. |
| Integración (`intex1`) | ✅ **Sí** — ahora sí es resoluble, porque depende del total de C |

**No se crea un archivo nuevo.** Este build **extiende el mismo Google Sheet** que Semana 1 ya
entregó — mismas pestañas, mismo dataset ya limpio en `📊 Datos`, mismo tab `🧩 Tu Caso`. La
numeración de claves (`ex7`, `ex8`, `debug3`) se dejó reservada a propósito en Semana 1
precisamente para este momento (`Instrucciones_Build_Semana1_Sheets.md` §6): "no tener que
renumerar nada cuando se construya" Semana 2. Si terminas este build y necesitas renumerar algo
de Semana 1, para y revisa — probablemente significa que este documento tiene un error, no que
haga falta romper el contrato ya entregado a ATLAS.

### 0.2 Por qué los números de este documento NO son los del documento original

`Ejercicios_Practica_Semanas1-2_Sheets.md` §2 usa un dataset de ejemplo de **18 filas** (56
boletos, S/280) para ilustrar la lógica. Pero el build real de Semana 1 —documentado en
`ATLAS_Handoff_Caso1_Semana1_API_DB.md` §9— usó un dataset **escalado**: 108 filas crudas, 90
válidas tras la limpieza, 48 viernes / 42 sábado, con **suma de boletos = 324** (viernes = 162,
sábado = 162 — el empate que motiva `reto1` está en la *suma*, no en el conteo de filas). Este
build de Semana 2 tiene que continuar sobre esos números reales, no sobre los del ejemplo de 18
filas — usar 56/280 aquí produciría una plantilla que no cuadra con lo que el estudiante ya tiene
en su hoja de Semana 1.

**Precio por boleto:** el dato original (`Ejercicios_Practica_Semanas1-2_Sheets.md` §2, "dato
fijo, se da en la narrativa, no es columna") es **S/5**. Nada en el build de Semana 1 lo contradice
ni lo usa todavía (Sección C es la primera vez que aparece), así que este documento lo hereda sin
cambios. **Recaudación total = 324 × 5 = S/1620.** Confirmar con GAUSS junto con el resto de §10.

⚠️ **Nota importante para quien construya:** los números `108/90/48/42/162/162/324` vienen de la
documentación post-build de Semana 1, no de haber inspeccionado el archivo `.xlsx` fila por fila
(el JSON `_dataset_ground_truth.json` que los generó se adjuntó como mensaje de chat, no quedó
guardado en el repo). **Antes de escribir cualquier clave/valor esperado, abre
`Caso1_Semana1_AbriendoElCaso_v4.xlsx` y confirma estos agregados contra la pestaña `📊 Datos`
real** (`COUNTA`, `SUM`, `COUNTIF` sobre el rango ya poblado). Si algo no cuadra con lo que este
documento asume, el archivo real manda, no este documento.

---

## 1. Estructura de pestañas (sin cambios de nombres/orden)

| Pestaña | Qué se toca en este build |
|---|---|
| 📋 **Instrucciones** | Se agrega un bloque corto de apertura de Semana 2 (§2) — no se borra nada de Semana 1 |
| 🔍 **Ejemplo Resuelto** | Se resuelve el callback pendiente de la demo `debug2` (§2) — no se agregan datasets nuevos |
| 📊 **Datos** | Se agrega **una columna nueva, `E` = "Total"** (§3.2) — las columnas `A`–`D` que ya usa el contrato de Semana 1 **no se tocan** |
| 🕵️ **Tu Caso** | Se agrega el bloque de Sección C + Integración + Resumen/Enviar de Semana 2, **después** del bloque de `reto1` que Semana 1 ya dejó (§3–§5) |
| 🔒 **Clave** | Se agregan las respuestas estáticas nuevas (`t4`, valor recalculado de `debug3`) — ver §6 |

Mismo léxico de iconos que Semana 1, sin cambios (`COURSE_TEMPLATE.md` §4, ya replicado en
`Instrucciones_Build_Semana1_Sheets.md` §1). Sigue sin existir Theme Brief final de PIXEL — seguir
usando el placeholder neutro "la Agencia".

---

## 2. Actualizaciones a pestañas ya existentes

### 2.1 `📋 Instrucciones` — bloque nuevo, agregado al final

Agregar, sin borrar el contenido de Semana 1:

1. **Subtítulo:** "Caso 1: Cerrando el Caso — Semana 2"
2. **Callback breve** (mismo patrón que el módulo de Python usa para conectar semanas —
   `WORKFORCE_HANDOFF.md`, entrada 2026-08-05 sobre `nb1-c-header"): *"La sesión pasada dejamos
   la evidencia limpia y organizada — sabíamos que Viernes y Sábado vendieron la misma cantidad
   de boletos (28... o mejor dicho, en tu caso, un número que viste con tus propios ojos en la
   barra de estado). Pero nunca escribiste una fórmula para confirmarlo. Hoy sí."*
3. Los 3 pasos de esta sesión: 🧮 El Total formal (`SUMA` de verdad) → 💰 La Recaudación (columna
   Total) → 📝 Cierre del Caso (resumen final).
4. Nota corta, mismo texto que Semana 1: "Cuando termines, tu profesor(a) revisará tu hoja con el
   botón **Enviar para calificar (Semana 2)** al final de la pestaña Tu Caso." — **el "(Semana 2)"
   en el nombre del botón es intencional, ver §5**, para que quede claro que es un envío
   independiente del de Semana 1.

### 2.2 `🔍 Ejemplo Resuelto` — resolver el callback de `debug2`

El demo `debug2` de Semana 1 (`Instrucciones_Build_Semana1_Sheets.md` §4-B) terminaba con el texto
*"La próxima sesión vas a usar esta fórmula tú mismo."* Agregar, junto a ese mismo demo (no
borrarlo — dejarlo como referencia), una línea corta que cierre el círculo: *"Esa fórmula era
`=SUMA()`. Ya la viste fallar en silencio con texto mal escrito — hoy la vas a escribir tú, sobre
evidencia que TÚ ya limpiaste."*

No se agrega un mini-caso nuevo en esta pestaña — el mini-caso de "El Bazar Escolar" de Semana 1
ya mostró el patrón completo; reutilizarlo basta.

---

## 3. Pestaña `🧩 Tu Caso` — Sección C (nuevo bloque, ~40 XP)

**Dónde insertar:** inmediatamente después del bloque de `reto1` (fila 61 según
`ATLAS_Handoff_Caso1_Semana1_API_DB.md` §3) y **antes** del bloque "Resumen para enviar" de
Semana 1 (filas 63–70 de ese mismo documento). Insertar filas nuevas ahí — no sobrescribir ni
mover el bloque de resumen de Semana 1; solo empujarlo hacia abajo si Sheets no lo hace solo al
insertar filas.

Mismo layout de columnas que ya usa toda la pestaña (`ATLAS_Handoff...` §3): `A` = clave · `B` =
instrucción (XP como sufijo de texto) · `C` = respuesta del alumno · `D` = resultado visible
(fórmula) · `E` = XP crudo (oculto visualmente, legible programáticamente).

Antes del primer ejercicio, insertar un separador visual: **"— Sección C: El Total —"** (mismo
patrón que el separador "Fin de la Recepción y Limpieza" que ya existe entre B y D).

### 3.1 `ex7` — SUMA formal sobre Boletos ya limpio

| Campo | Valor |
|---|---|
| Icono | 🧩 COMPLETA |
| Instrucción | "Escribe `=SUMA(` seguido del rango de la columna Boletos en `📊 Datos` (el mismo rango que la barra de estado te mostraba la sesión pasada), y ciérralo. ¿Cuántos boletos se vendieron en total, según la fórmula?" |
| Rango esperado | `Datos!B5:B112` — el mismo rango fijo de 108 filas que ya usan las fórmulas de Semana 1 (`ATLAS_Handoff...` §4); las ~18 filas vacías al final (por las eliminaciones de `ex4`) no afectan el resultado — `SUMA` las trata como 0, mismo comportamiento que el estudiante ya vio en `debug2` |
| Respuesta esperada | `324` (recalcular contra el archivo real — ver §0.2) |
| Grading source | Numérica vs. fórmula en vivo — mismo patrón que `ex10`/`ex11` de Semana 1: `VALUE(respuesta) = SUMA(Datos!B5:B112)` |
| XP | 15 |

**Nota pedagógica (de `Teoria_Semanas1-2_Caso1_AbriendoElCaso.md` §2, Sección C):** el texto de
acompañamiento debe remarcar que el número ahora es confiable **porque los datos están limpios**,
no porque `SUMA` sea una fórmula distinta a la que ya usaron en `debug2` — es literalmente la
misma fórmula, aplicada a mejor evidencia.

### 3.2 `ex8` — Columna Total y recaudación

| Campo | Valor |
|---|---|
| Icono | 🔨 CONSTRUYE |
| Instrucción | "En `📊 Datos`, agrega el encabezado `Total` en la columna E. En cada fila con evidencia, escribe una fórmula que multiplique Boletos por el precio (S/5) y arrástrala hasta el final de los datos. Luego, en tu hoja de Tu Caso, escribe `=SUMA()` sobre esa columna nueva. ¿Cuánto se recaudó en total?" |
| Fórmula por fila esperada | `=B5*5` (o equivalente), arrastrada por el rango poblado de `📊 Datos` |
| Respuesta esperada | `1620` (= 324 × 5; recalcular contra el archivo real) |
| Grading source | Numérica vs. fórmula en vivo: `VALUE(respuesta) = SUMA(Datos!B5:B112)*5` (no depende de que la columna E del alumno esté bien construida fila por fila — igual que el resto del módulo, ver §7, no confíes en el trabajo intermedio del alumno, recalcula desde `Boletos` directamente) |
| XP | 15 |

**Nota para ATLAS:** esta es la primera vez que el build escribe en `📊 Datos` fuera de las
columnas `A`–`D` que ya documentó `ATLAS_Handoff_Caso1_Semana1_API_DB.md` §4. La columna `E` es
nueva y exclusiva de Semana 2 — no colisiona con nada que el contrato de Semana 1 lea, pero
vale la pena que lo confirmes antes de fijar el Apps Script de Semana 2 (§8).

### 3.3 `debug3` — el rango corrido (rediseñado, ver nota)

⚠️ **Este ejercicio NO es el `debug3` del documento original.** La especificación original
(`Ejercicios_Practica_Semanas1-2_Sheets.md` §3, Sección C) decía: *"una fórmula SUMA ya escrita
que por error sigue incluyendo la fila cancelada en el rango."* Esa fila ya no existe — Semana 1
la eliminó físicamente en `ex4`. Reutilizar ese diseño tal cual generaría un ejercicio irresoluble
contra el dataset real de este build, así que se rediseñó manteniendo la misma lección (**"SUMA
no avisa cuando algo está mal"**) con un error que sí puede ocurrir sobre los datos ya limpios.
Mismo criterio que `Instrucciones_Build_Semana1_Sheets.md` §0 usó para adaptar la Sección D —
documentar la decisión, no ocultarla.

| Campo | Valor |
|---|---|
| Icono | 🔧 DEBUG |
| Narrativa | Un compañero ficticio ya escribió `=SUMA(Datos!B6:B112)` para calcular el total (un error de un solo renglón — empezó en la fila 6, no en la 5, típico de arrastrar el rango después de que `ex4` borró filas la sesión pasada) y obtuvo un número que **parece razonable pero no es el correcto** — la fórmula no avisó del error. |
| Instrucción | "¿Cuál es el total *correcto* de boletos vendidos?" (no se pide corregir la fórmula del compañero, solo dar el valor correcto — mismo mecanismo que `debug1` de Semana 1) |
| Respuesta esperada | `324` (la misma respuesta que `ex7` — refuerza el número, no introduce uno nuevo) |
| Grading source | Numérica vs. fórmula en vivo, idéntica a `ex7`: `VALUE(respuesta) = SUMA(Datos!B5:B112)` |
| XP | 5 |

**Nota técnica para el build:** el "número que parece razonable" que muestra el compañero ficticio
(`=SUMA(Datos!B6:B112)`) depende del valor real de Boletos en la fila 5 del dataset final —
**calcúlalo abriendo el archivo real** (324 menos ese valor) en vez de inventar un número; no lo
hardcodees en este documento porque puede no coincidir con el archivo real.

### 3.4 `t4` — Teoría: por qué confiamos en el número ahora

| Campo | Valor |
|---|---|
| Icono | ❓ TEORÍA |
| Pregunta (MC) | *"Ahora confías en el resultado de `SUMA`. ¿Por qué? a) Porque `SUMA` es una fórmula distinta a la que viste la sesión pasada, b) Porque la evidencia ya está limpia y organizada, c) Porque escribiste la fórmula tú mismo esta vez, d) Porque Google Sheets corrige los errores automáticamente"* |
| Respuesta esperada | `b` |
| Grading source | Estática vs. `🔒 Clave` (case-insensitive), mismo patrón que `t1`–`t3` |
| XP | 5 |

**Nota de precisión (heredada de `Teoria_Semanas1-2_Caso1_AbriendoElCaso.md` §2, marcada
explícitamente para que GAUSS la confirme):** esta pregunta es el punto pedagógico central de
Sección C — el texto de las opciones incorrectas no debe sugerir que `SUMA` "se arregló" o que es
distinta a la que ya usaron; la fórmula siempre fue correcta, lo que cambió fue la calidad de los
datos que recibió.

### 3.5 `check_mini_c` — Checkpoint

Gate: `ex7` + `ex8` + `debug3` + `t4` correctos antes de desbloquear Integración. Sin XP propio
(0 pts, solo gate) — mismo patrón que `check_mini_b`/`check_mini_d` de Semana 1.

---

## 4. Pestaña `🧩 Tu Caso` — Integración (~15 XP)

Insertar después de `check_mini_c`, con separador **"— Cierre del Caso —"**.

### 4.1 `intex1`

| Campo | Valor |
|---|---|
| Icono | 🧩 COMPLETA (fill-in-the-blank de varias partes) |
| Instrucción | Completar el resumen del caso: *"El caso cerró con **___** boletos vendidos (**S/___** recaudados), sobre **___** registros de evidencia ya limpia, tras eliminar los duplicados y la venta cancelada en la sesión anterior."* — tres celdas de respuesta separadas |
| Respuestas esperadas | boletos = `324` · recaudación = `1620` · registros = `90` (recalcular los tres contra el archivo real) |
| Grading source | Numérica vs. fórmula en vivo, las tres celdas: `SUMA(Datos!B5:B112)`, `SUMA(Datos!B5:B112)*5`, `COUNTA(Datos!A5:A112)` respectivamente — mismo criterio que `ex4` de Semana 1 para no depender de que el alumno haya escrito bien `ex7`/`ex8`, sino de recalcular todo desde `📊 Datos` |
| XP | 15 |

**Por qué esta pregunta obliga a integrar, no solo a repetir `ex7`/`ex8`:** el tercer blanco
(`90` registros) no se calculó en ningún ejercicio anterior de Semana 2 — obliga al estudiante a
volver a `📊 Datos` y contar, conectando la limpieza de Semana 1 con el total de Semana 2 en una
sola conclusión, que es exactamente el propósito de un ejercicio de Integración
(`COURSE_TEMPLATE.md` §4, taxonomía `intex*`).

---

## 5. Botón "Enviar para calificar (Semana 2)" — envío independiente

**Decisión de diseño: Semana 2 es un segundo evento de envío independiente, no una actualización
del envío de Semana 1.** Razones:

1. Semana 1 ya se entregó a ATLAS con un contrato cerrado (`possible: 95`, `notebook:
   "sheets_caso1_semana1"`, bloque "Resumen para enviar" en filas 63–70). Reabrir ese contrato
   para inyectarle las claves de Semana 2 arriesga romper algo que ATLAS ya puede haber
   implementado.
2. Mismo patrón que el módulo de Python: `nb1_semana1` y `nb1_semana2` son envíos con
   `notebook` distinto aunque la misión narrativa continúe (`WORKFORCE_HANDOFF.md`, múltiples
   entradas sobre `autograder_nb1_semana2.py`).

Insertar, después de `intex1`, un bloque "Resumen Semana 2" independiente (mismo mecanismo que el
de Semana 1 — celdas espejo + suma de XP crudo) y su propio botón/dibujo "Enviar para calificar
(Semana 2)", asignado a una función de Apps Script separada de la de Semana 1. El botón de Semana
1 (fila 69 original) **no se toca, no se renombra, sigue funcionando igual**.

- `E_semana2` (XP autocalificado Semana 2) = `SUMA(E<ex7>, E<ex8>, E<debug3>, E<t4>, E<intex1>)`
  (referenciar las filas reales una vez insertadas, no las de Semana 1).
- No hay ítems de revisión del profesor en Semana 2 (a diferencia de `ex3`/`ex9` en Semana 1) —
  todo es autograded, así que no hace falta un bloque separado de "XP revisión profesor(a)".
- No hay bonus nuevo en Semana 2 (`reto2` no existe en la especificación original ni se agrega
  aquí) — mantener el alcance ceñido a lo que pide `Ejercicios_Practica_Semanas1-2_Sheets.md`.

---

## 6. `🔒 Clave` — valores nuevos a agregar

Agregar, sin tocar las filas que ya usa Semana 1 (`ex1=108`, `ex2=4`, `debug1=108`, `t1="b"`,
`t2="c"`, `t3="b"`):

```
t4 = "b"
```

`ex7`, `ex8`, `debug3` e `intex1` **no van en `🔒 Clave`** — son "numérica vs. fórmula en vivo"
(§3.1–§3.3, §4.1), igual que `ex10`/`ex11`/`reto1` de Semana 1, así que se recalculan siempre
contra `📊 Datos`, nunca contra un valor fijo guardado de antemano (mismo razonamiento que
`ATLAS_Handoff...` §6 ya documentó para esos tres: un valor fijo se desactualizaría si el dataset
cambia de semilla).

---

## 7. Recordatorio de seguridad — mismo problema que Semana 1, no reintroducirlo

`ATLAS_Handoff_Caso1_Semana1_API_DB.md` §6 ya documentó que nada en la hoja está protegido —
cualquier alumno puede sobrescribir una celda de fórmula o desocultar `🔒 Clave`. Todo lo nuevo de
este build hereda el mismo riesgo, especialmente la columna `Total` nueva en `📊 Datos` (§3.2), que
un alumno podría escribir a mano con valores inventados. **El mismo principio aplica sin
excepción: cuando el Apps Script de Semana 2 dispare el envío real, no leas los valores ya
calculados en la hoja — re-derive `ex7`/`ex8`/`debug3`/`intex1` directamente desde `Boletos` en
`📊 Datos`**, exactamente como ya se documentó para Semana 1. No es necesario repetir aquí toda la
lógica de recálculo — es la misma de §3.1–§4.1, ya escrita en formato "fórmula en vivo" para que
se traduzca directo a Apps Script/servidor sin ambigüedad.

---

## 8. Contrato de datos para la API — Semana 2 (stub, ATLAS confirma diseño final)

```json
{
  "dni": "<'🗂️ Configuración'!C5>",
  "nombre": "<'🗂️ Configuración'!C4>",
  "grado": "<'🗂️ Configuración'!C6>",
  "notebook": "sheets_caso1_semana2",
  "curso": "STAT_2026",
  "earned": "<suma de puntos obtenidos, sin bonus — no hay bonus en Semana 2>",
  "possible": 55,
  "score_breakdown": {
    "ex7": {"e": 15, "p": 15},
    "ex8": {"e": 15, "p": 15},
    "debug3": {"e": 5, "p": 5},
    "t4": {"e": 5, "p": 5},
    "intex1": {"e": 15, "p": 15}
  },
  "submitted_at": "<timestamp>"
}
```

- `curso` = **`"STAT_2026"`** — el mismo valor exacto que fijó Semana 1 (`ATLAS_Handoff...` §5,
  citando `WORKFORCE_HANDOFF.md` Done log 2026-08-07). No inventar un valor nuevo para Semana 2.
- `notebook` = `"sheets_caso1_semana2"` es **provisional**, propuesto aquí por el mismo criterio
  que usó Semana 1 (`ATLAS_Handoff...` §3, "sigue el patrón `nb1_semana1`/`nb1_semana2` de
  Python") — ATLAS confirma o reemplaza.
- `possible: 55` = suma de XP core de este build únicamente (15+15+5+5+15). **`possible` de
  Semana 1 (95) no cambia** — son dos envíos independientes, no un total acumulado (§5). Si el
  reporting/dashboard necesita mostrar un "total del Caso 1" combinado (95+55=150, que además
  coincide con el presupuesto de ~150 XP que fija `Bimestre3_Statistics_Sheets_Module_Guide.md`
  para Semanas 1–2), eso es una agregación del lado del backend sobre dos filas de `submissions`,
  no un cambio al payload de ninguna de las dos semanas — decisión de ATLAS, no de este documento.
- Ningún campo usa `kind: "teacher_review"` en Semana 2 (a diferencia de Semana 1) — todo el
  bloque es autograded.

---

## 9. Lo que este build deliberadamente NO incluye

- Un dataset nuevo o distinto — reutiliza exactamente el `📊 Datos` que Semana 1 ya limpió.
- Cambios a las claves, respuestas o XP ya fijados de Semana 1 (`ex1`–`ex6`, `ex9`–`ex11`,
  `t1`–`t3`, `debug1`, `check_mini_b`, `check_mini_d`, `reto1`).
- Un segundo reto bonus (`reto2`) — no está en la especificación original.
- Tema visual final (nombre de agencia, paleta, achievements) — sigue pendiente de PIXEL, igual
  que Semana 1.
- El diseño final del Apps Script del botón de Semana 2 — pendiente de ATLAS (§8 es un contrato
  provisional, no la implementación; puede reusar/extender `AppsScript_Caso1_Semana1.gs` con una
  segunda función de envío, no necesariamente un archivo nuevo).

---

## 10. Pendientes antes de publicar a estudiantes reales

1. **Quien construya (Claude Cowork):** antes de fijar cualquier valor esperado, **abrir
   `Caso1_Semana1_AbriendoElCaso_v4.xlsx` y recalcular los agregados reales** de `📊 Datos`
   (`n_valid`, suma de Boletos, valor de la fila 5) — este documento hereda `108/90/48/42/162/
   162/324` de la documentación post-build de Semana 1 (`ATLAS_Handoff...` §9), no de una
   inspección directa del archivo (§0.2). Si algo no cuadra, el archivo manda.
2. **GAUSS:** confirmar (a) los agregados heredados de §0.2, (b) que S/5 sigue siendo el precio
   correcto por boleto para este dataset escalado (heredado del ejemplo de 18 filas, nunca
   re-confirmado contra el dataset de 108), (c) que la reformulación de `debug3` (§3.3) preserva
   la lección original sin introducir un error nuevo, (d) el paralelismo "SUMA no es especial,
   los datos están limpios" de `t4` (mismo pendiente que ya tenía la Sección C original en
   `Teoria_Semanas1-2_Caso1_AbriendoElCaso.md` §2).
3. **PIXEL:** Theme Brief sigue pendiente — este build sigue usando placeholders neutros.
4. **ATLAS:** confirmar el contrato de §8 (especialmente `notebook`, y si `possible` de las dos
   semanas se agrega o se reporta por separado), diseñar el Apps Script real del botón de Semana
   2, y decidir el orden de reenvío/recalificación si un alumno reenvía Semana 2 antes de que
   Semana 1 haya sido revisada por el profesor (`ex3`/`ex9` son manuales — ver
   `ATLAS_Handoff...` §6d, pregunta ya abierta ahí, que Semana 2 hereda sin resolver).
5. **Sincronización de documentación:** una vez este build exista de verdad, actualizar
   `Ejercicios_Practica_Semanas1-2_Sheets.md` para que dejar de listar `ex6`/`ex7`/`ex8` con la
   numeración/contenido original (superada por la partición real en `Instrucciones_Build_
   Semana1_Sheets.md` + este documento) — hoy el documento original y los dos de build ya
   divergieron en qué clave hace qué, y vale la pena que quien lea el repo en el futuro no tenga
   que reconciliar tres fuentes a mano.

---

*Preparado por SOFIA (contenido pedagógico), con las convenciones de ATLAS (`03_ATLAS.md`) para
tolerancia de grading, effort vs. skill, y estructura de contrato, para build de Claude Cowork.
Alcance: solo Semana 2 (Sección C + Integración). Depende de que Semana 1 ya esté construida
(`Caso1_Semana1_AbriendoElCaso_v4.xlsx`) — este documento no es independiente.*
*Fecha: 2026-08-14*

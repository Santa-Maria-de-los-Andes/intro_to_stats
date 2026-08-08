# Instrucciones de Build — Semana 1 (Sheets): "Caso 1 — Abriendo el Caso"

**Para:** agente de build (Claude Cowork).
**Estado:** listo para construir la plantilla real de Google Sheets. Contenido pedagógico de
SOFIA. Validación estadística final de GAUSS y contrato definitivo de Apps Script/API de ATLAS
siguen pendientes (ver Sección 9), pero **no bloquean construir la plantilla** — los números ya
están verificados a mano (heredados de `Ejercicios_Practica_Semanas1-2_Sheets.md` §6) y la capa
de envío/API puede quedar como stub hasta que ATLAS cierre su diseño.
**Fuentes:** `Ejercicios_Practica_Semanas1-2_Sheets.md`, `Teoria_Semanas1-2_Caso1_AbriendoElCaso.md`
(mismo folder), `Bimestre3_Statistics_Sheets_Module_Guide.md`, `COURSE_TEMPLATE.md` §4/§6/§8/§10
(convenciones de icono, taxonomía de claves, payload, effort-grading).

---

## 0. Alcance de este build — SOLO Semana 1

Este documento parte el caso "Semanas 1–2" original en dos mitades, igual que ya se hizo con el
módulo de Python (`nb1_semana1` / `nb1_semana2`, ver `WORKFORCE_HANDOFF.md`). Esta plantilla
cubre, de la especificación original:

| Sección | ¿Incluida en este build? |
|---|---|
| A — Recepción del Caso | ✅ Sí, sin cambios de contenido |
| B — Limpieza | ✅ Sí, **ampliada** (absorbe el llenado de vacíos que antes vivía en C — ver §3.2) |
| C — El Total (`=SUMA()`) | ❌ No. Va en el build de Semana 2, junto con `SUMA()` enseñado formalmente |
| D — Filtrado Básico | ✅ Sí, **adaptada** para no depender de un total general que todavía no existe (ver §3.4) |
| Integración (`intex1`) | ❌ No. Depende de C (recaudación total) — va en Semana 2 |

**Por qué D se adapta y no simplemente se salta:** en el documento original, Sección D asume que
el estudiante ya calculó y confía en un total general (56 boletos) antes de filtrar un
subconjunto — la pregunta que abre D es literalmente "¿y si solo quiero el total de una parte?"
de un total que ya existe. Como esta plantilla no enseña `SUMA()` todavía, D se reescribió para
apoyarse solo en lo que Sección B ya dejó limpio, y para funcionar sin fórmulas nuevas (ver
§3.4 para el mecanismo exacto). Esto es una decisión real de secuencia pedagógica, no solo un
recorte de alcance — si este documento se retoma en una revisión formal de SOFIA/GAUSS, vale la
pena que lo revisen explícitamente.

---

## 1. Estructura de pestañas (sin cambios respecto al original)

| Pestaña | Contenido | ¿Se califica? |
|---|---|---|
| 📋 **Instrucciones** | Teoría corta, leyenda de iconos, narrativa del caso (ver §2) | No |
| 🔍 **Ejemplo Resuelto** | Mini-caso ya resuelto + demo `debug2` (ver §4) | No |
| 🕵️ **Tu Caso** | El dataset de 18 filas + todos los ejercicios de esta semana | **Sí — vía API** |

**Leyenda de iconos** — reutilizar exactamente (mismos emoji/etiquetas, `COURSE_TEMPLATE.md` §4):

| Icono | Etiqueta | Acción del estudiante |
|---|---|---|
| 👀 | OBSERVA | Mirar sin modificar nada |
| ✏️ | MODIFICA | Editar una celda o formato existente |
| 🧩 | COMPLETA | Reemplazar `___` por el valor correcto |
| 🔨 | CONSTRUYE | Ejecutar una acción desde cero (borrar filas, aplicar filtro) |
| 🔧 | DEBUG | Encontrar y corregir un error ya presente |
| ❓ | TEORÍA | Pregunta de opción múltiple |
| ✅ | VERIFICA | Checkpoint que la API valida |

No usar el tema visual final (nombre de la agencia, paleta) todavía — PIXEL no ha cerrado su
Theme Brief para este módulo. Usar el placeholder neutro **"la Agencia"** en todo texto
narrativo, igual que hace `Teoria_Semanas1-2_Caso1_AbriendoElCaso.md`. No hardcodear colores de
marca; dejar el formato en la paleta por defecto de Sheets salvo lo que pida un ejercicio
específico (negrita, bordes).

---

## 2. Pestaña "Instrucciones" — contenido exacto

Incluir, en este orden:

1. **Título:** "Caso 1: Abriendo el Caso — Semana 1"
2. **Gancho de apertura** (adaptar el texto de `Teoria_Semanas1-2_Caso1_AbriendoElCaso.md` §0,
   reemplazando el placeholder "45 vs. 52" por la progresión real de este dataset — resuelve el
   pendiente marcado en la §7 de `Ejercicios_Practica_Semanas1-2_Sheets.md`):

   > *"Dos tesoreros de la Kermés cuentan el mismo montón de boletos vendidos. Uno dice que se
   > vendieron 68. El otro dice 60. Ninguno mintió, ninguno se equivocó al sumar.
   > ¿Cómo es posible?"*
   >
   > *"Te acaba de llegar el primer caso de la Agencia. La evidencia está desordenada, con
   > duplicados, una venta cancelada y espacios vacíos — antes de poder calcular nada con
   > confianza, tu primer trabajo como detective es poner la evidencia en orden."*

   **Nota para el build:** esta pestaña NO revela todavía el número final (56) — ese es el
   pago de la Semana 2, cuando se enseñe `SUMA()` formalmente. Esta semana el caso cierra
   confiando en el desglose por día (28 + 28), no en el total general. Dejar el gancho abierto
   con algo como: *"Al final de hoy vas a confiar en cuántos boletos se vendieron cada día. El
   total general te lo confirma la próxima sesión con una fórmula nueva."*

3. **Los 4 pasos de esta sesión**, en lenguaje simple: 🕵️ Recepción (mirar la evidencia cruda) →
   🧹 Limpieza (arreglar duplicados, texto inconsistente, datos faltantes) → 🔎 Filtrado (aislar
   solo la evidencia de un día) → 🎁 Reto bonus.
4. **Leyenda de iconos** (tabla de §1).
5. Nota corta: "Cuando termines, tu profesor(a) revisará tu hoja con el botón **Enviar para
   calificar** al final de la pestaña Tu Caso."

---

## 3. Pestaña "Tu Caso" — dataset y ejercicios

### 3.0 El dataset (idéntico al original — no modificar)

Colocar exactamente estas 18 filas, **sin limpiar**, en una tabla con encabezados `Comprador`,
`Boletos`, `Día`, `Estado` (columnas A–D, fila de encabezado en fila 3 sugerida, datos en filas
4–21):

| Fila | Comprador | Boletos | Día | Estado |
|---|---|---|---|---|
| 1 | María López | 5 | viernes | Válido |
| 2 | Jorge Quispe | 3 | Sábado | Válido |
| 3 | Ana Ccahuana | 4 | VIERNES | Válido |
| 4 | Luis Mamani | 6 | sábado | Válido |
| 5 | Rosa Huamán | 2 | Viernes | Válido |
| 6 | Pedro Flores | 5 | SÁBADO | Válido |
| 7 | Diego Torres | *(vacío)* | viernes | Válido |
| 8 | Karla Rojas | 3 | Sábado | Válido |
| 9 | Fernando Paz | 4 | viernes | Válido |
| 10 | Gabriela Ríos | 6 | Sábado | Válido |
| 11 | Andrés Cusi | 2 | viernes | Válido |
| 12 | Valeria Ponce | *(vacío)* | sábado | Válido |
| 13 | Sofía Vargas | 5 | Viernes | Válido |
| 14 | Renzo Salas | 3 | SABADO | Válido |
| 15 | Camila Yupanqui | 2 | viernes | Válido |
| 16 | María López | 5 | viernes | Válido *(duplicado exacto de fila 1)* |
| 17 | Karla Rojas | 3 | Sábado | Válido *(duplicado exacto de fila 8)* |
| 18 | Ana Torres | 10 | Sábado | **Cancelado** |

No incluir la columna "Total" ni el dato "Precio por boleto S/5" en esta plantilla — no se usan
hasta Sección C (Semana 2). Si aparecen en el material de referencia, ignorarlos por ahora.

**Números verificados que este build usa** (heredados de `Ejercicios_Practica_Semanas1-2_Sheets.md`
§6, re-derivados para esta secuencia sin Sección C — confirmar con GAUSS antes de publicar,
igual que el original):

- Tras quitar los 2 duplicados exactos y la fila cancelada: **15 filas válidas únicas**.
- De esas 15, **8 son viernes** (filas 1,3,5,7,9,11,13,15) y **7 son sábado** (filas
  2,4,6,8,10,12,14).
- 2 celdas de Boletos llegan vacías (filas 7 y 12 — Diego Torres y Valeria Ponce). La "nueva
  pista" revela que fueron **4** y **2** respectivamente.
- Subtotal de boletos, ya limpio: **Viernes = 28**, **Sábado = 28** (empate intencional — mismo
  gancho hacia "promedio" de Semana 3 que en el original).
- El total general (Viernes + Sábado = **56**) se **menciona pero no se calcula con fórmula**
  esta semana — se confirma formalmente en Semana 2 con `SUMA()`.

### 3.1 Sección A — Recepción del Caso (~20 XP)

Colocar el dataset crudo (§3.0) y, antes de tocar nada, estos ejercicios:

| Clave | Icono | Instrucción (texto para el estudiante) | Respuesta esperada | XP |
|---|---|---|---|---|
| `ex1` | 👀🧩 | "Sin editar nada todavía: ¿cuántas filas de evidencia llegaron? (no cuentes el encabezado)" | `18` | 5 |
| `ex2` | 👀🧩 | "¿Cuántas columnas/pistas tiene el caso?" | `4` | 5 |
| `t1` | ❓ | MC: *"En esta hoja, cada FILA representa: a) una columna de datos, b) un boleto vendido (una pieza de evidencia), c) el nombre de la Agencia, d) el precio total"* | `b` | 5 |
| `debug1` | 🔧 | "Un compañero ficticio ya contó 'hay 20 filas de evidencia' — contó el encabezado dos veces. ¿Cuántas filas hay en realidad?" | `18` | 5 |

### 3.2 Sección B — Limpieza (~40 XP)

**Ampliada respecto al original:** absorbe el llenado de las celdas vacías (antes vivía en
Sección C, ver §0) porque el llenado de datos faltantes ya está descrito como parte de
"Limpieza" en `Teoria_Semanas1-2_Caso1_AbriendoElCaso.md` §2 ("rellenar/marcar vacíos"), así que
no es un contenido nuevo, solo se reubica.

| Clave | Icono | Instrucción | Respuesta esperada / criterio | XP |
|---|---|---|---|---|
| `ex3` | ✏️ | "Pon en negrita la fila de encabezados y agrégale bordes." | **Gradeable por esfuerzo, no por valor** — ver nota abajo | 5 |
| `ex4` | 🔨 | "Elimina las filas duplicadas exactas Y la fila cancelada (Ana Torres)." | 15 filas restantes (8 viernes + 7 sábado); "María López" y "Karla Rojas" aparecen una sola vez cada una; "Ana Torres" ya no aparece | 10 |
| `ex5` | 🧩 | "Estandariza la columna Día a exactamente `Viernes` o `Sábado` (sin mayúsculas irregulares tipo VIERNES, sábado, SABADO)." | Cada celda de Día ∈ {`Viernes`, `Sábado`} exacto | 10 |
| `ex6` | 🧩 | *(Tras la narrativa "nueva pista": "La Agencia encontró los boletos que faltaban.")* "Completa las 2 celdas vacías de Boletos: Diego Torres vendió 4, Valeria Ponce vendió 2." | Boletos(Diego Torres) = `4`; Boletos(Valeria Ponce) = `2` | 10 |
| `t2` | ❓ | MC: *"Una celda de Boletos está vacía. ¿Qué deberías hacer? a) Borrar la fila, b) Asumir que es 0, c) Investigar antes de asumir, d) Poner el promedio del resto"* | `c` | 5 |
| `check_mini_b` | ✅ | Checkpoint — gate: `ex4`+`ex5`+`ex6`+`t2` correctos antes de desbloquear Sección D | — | 0 (solo gate) |

**Nota sobre `ex3` (effort, no correctness):** igual que `grade_report.py` §10 de
`COURSE_TEMPLATE.md` (`kind='effort'`), no es verificable por valor de celda de forma confiable.
Agregar una casilla de verificación (Insertar → Casilla de verificación) junto al ejercicio que
el estudiante marca cuando termina; la API lee esa casilla como el criterio de "sí/no se
intentó", no si el formato quedó pixel-perfecto.

**Nota técnica para quien construya el Apps Script de validación:** `ex4` borra filas, así que
las posiciones de fila de todo lo que viene después (`ex5`, `ex6`) se recorren hacia arriba.
Validar `ex5`/`ex6` **por contenido** (buscar la fila donde `Comprador = "Diego Torres"`, etc.),
no por número de fila fijo. Esto es válido porque tras `ex4` los nombres ya son únicos (los
únicos duplicados del dataset eran los que se eliminaron).

### 3.3 Pestaña "Tu Caso" — marcador de fin de trabajo en clase (opcional, recomendado)

Insertar un separador visual tipo "— Fin de la Recepción y Limpieza —" antes de Sección D, mismo
patrón usado en el módulo de Python (`WORKFORCE_HANDOFF.md`, marcador "Fin de la Clase 1") si
esta plantilla se reparte en más de una sesión.

### 3.4 Sección D — Filtrado Básico (~35 XP, adaptada — ver §0)

**Cómo se resuelve la dependencia de Sección C sin usar `SUMA()`:** Google Sheets ya muestra un
resumen (Suma/Promedio/Cuenta) en la **barra de estado inferior derecha** cuando seleccionas un
rango de celdas — y ese resumen respeta las filas ocultas por un filtro activo. Esto le permite
al estudiante leer un subtotal real sin escribir ninguna fórmula todavía, dejando `=SUMA()` como
la revelación formal de la próxima sesión (visualización antes de formalización, mismo principio
que ya rige todo el módulo — ver `Bimestre3_Statistics_Sheets_Module_Guide.md`,
"Pedagogical Guardrails").

| Clave | Icono | Instrucción | Respuesta esperada | XP |
|---|---|---|---|---|
| `ex9` | 🔨 | "Aplica un filtro (Datos → Crear un filtro) mostrando solo Día = 'Sábado'." | 7 filas visibles | 5 |
| `ex10` | 🧩 | "Con el filtro de Sábado activo, selecciona toda la columna Boletos (solo las celdas visibles) y mira la barra inferior donde dice 'Suma: ___'. Escribe ese número." | `28` | 10 |
| `ex11` | 🧩 | "Repite el filtro para Viernes y anota el subtotal de la misma forma." | `28` | 10 |
| `t3` | ❓ | MC: *"Si sumas los dos subtotales que acabas de calcular (Viernes + Sábado), ¿qué deberías obtener? a) Un número distinto cada vez que lo intentes, b) El total general de boletos vendidos, c) El precio por boleto, d) La cantidad de días de venta"* | `b` | 10 |
| `check_mini_d` | ✅ | Checkpoint — gate: `ex9`+`ex10`+`ex11`+`t3` correctos antes de habilitar "Enviar para calificar" | — | 0 (solo gate) |

**`reto1` (🎁 BONUS, separado — no cuenta a `_CORE_MAX`):** "Sin usar `SUMA()` ni ninguna fórmula
nueva: comparando los subtotales que ya calculaste, ¿qué día vendió más boletos?" — desplegable
con opciones `Viernes` / `Sábado` / `Empate`. Respuesta esperada: `Empate` (28 boletos cada
día). Mismo gancho intencional hacia "promedio" de Semana 3 que en el original, sin necesitar el
dato de recaudación en soles (eso vive en Sección C). XP bonus sugerido: 10.

### 3.5 Botón "Enviar para calificar"

Al final de la pestaña, un botón (dibujo insertado, asignado a una función de Apps Script) que
dispara el envío — mismo mecanismo que describe `Ejercicios_Practica_Semanas1-2_Sheets.md` §5.
El diseño exacto del script queda para ATLAS (ver §9); este documento solo fija qué claves debe
leer y en qué shape debe empaquetarlas (§7).

---

## 4. Pestaña "Ejemplo Resuelto"

Dos piezas, ninguna calificada:

**A. Mini-caso ya resuelto** — un dataset paralelo, distinto al de "Tu Caso" (para no filtrar
respuestas), pequeño (6 filas) y ya limpio, mostrando el resultado final de aplicar los mismos
pasos que Secciones A/B/D: cero duplicados, texto de Día estandarizado, sin celdas vacías, un
filtro ya aplicado con su subtotal visible en la barra inferior. Sugerencia de tema: "El Bazar
Escolar" (evita reusar "Kermés" para no confundir con el caso real del estudiante).

**B. Demo `debug2` — adelanto de la próxima sesión (marcar explícitamente como "Adelanto",
mismo patrón usado en el módulo de Python para prever contenido de la semana siguiente sin
enseñarlo del todo):**

> Tres celdas de muestra con Boletos = `4`, `"tres"` (texto), `5`. La celda de al lado ya tiene
> escrito `=SUMA(rango)` y muestra el resultado: **9**, no 12 — porque Sheets ignora
> silenciosamente el valor de texto, sin marcar error.
>
> Texto de acompañamiento: *"La próxima sesión vas a usar esta fórmula tú mismo. Por ahora, solo
> observa: la fórmula no avisa cuando algo está mal escrito — por eso esta semana revisamos la
> evidencia ANTES de confiar en cualquier número."*

**Cuidado con el lenguaje (nota heredada de GAUSS en el documento original, sigue aplicando
aquí):** no dar a entender que `SUMA` "se rompe" con texto o con vacíos — la fórmula funciona
correctamente, el punto pedagógico es que **no avisa** cuando la evidencia está incompleta o mal
escrita.

---

## 5. Checkpoints y XP — resumen para este build

| Sección | XP core | Notas |
|---|---|---|
| A — Recepción del Caso | 20 | Sin cambios respecto al original |
| B — Limpieza (ampliada) | 40 | +1 ejercicio nuevo (`ex6`, llenado de vacíos, reubicado desde C) |
| D — Filtrado Básico (adaptada) | 35 | Sin fórmula `SUMA()`; usa la barra de estado de Sheets |
| **Total `_CORE_MAX` (Semana 1)** | **95** | Provisional — SOFIA propone, **ATLAS debe confirmar** antes de fijar el autograder, mismo criterio que el documento original |
| `reto1` (bonus) | 10 | Separado, no cuenta al `_CORE_MAX` (`_BONUS_MAX = 10`) |

Semana 2 (fuera de este build) retomará con Sección C (~40 XP) + Integración (~15 XP), para
llegar al presupuesto total de ~150 XP que fija `WORKFORCE_CONTRACT.md`/el module guide para
todo el caso.

---

## 6. Taxonomía de claves usadas en este build

Mismo patrón que `COURSE_TEMPLATE.md` §4, aplicado a Sheets:

- `ex1`, `ex2`, `ex3`, `ex4`, `ex5`, `ex6`, `ex9`, `ex10`, `ex11` — ejercicios core (numeración
  no consecutiva a propósito: `ex7`/`ex8` quedan reservados para Sección C en Semana 2, para no
  tener que renumerar nada cuando se construya).
- `debug1` — único debug de esta semana (`debug2` y `debug3` del original son demo/Sección C,
  fuera de este build; `debug2` sobrevive solo como demo no calificada en Ejemplo Resuelto, ver
  §4).
- `t1`, `t2`, `t3` — teoría, opción múltiple.
- `check_mini_b`, `check_mini_d` — checkpoints, sin XP propio.
- `reto1` — bonus, `_BONUS_MAX` separado.

---

## 7. Contrato de datos para la API (stub — ATLAS confirma el diseño final)

No es el diseño final del Apps Script (eso es ingeniería nueva marcada explícitamente como
pendiente en `Bimestre3_Statistics_Sheets_Module_Guide.md`, Coordination Notes). Lo que este
build sí puede fijar, para que el trabajo de ATLAS tenga un contrato estable desde el día uno:

- **Claves a leer:** exactamente las 13 de §6 (`ex1,ex2,ex3,ex4,ex5,ex6,ex9,ex10,ex11,t1,t2,t3,
  reto1`) más los dos checkpoints (`check_mini_b`, `check_mini_d`, informativos, sin puntaje).
- **Shape del payload**, calcado del patrón `self._scores`/`score_breakdown` de
  `COURSE_TEMPLATE.md` §6/§8:

  ```json
  {
    "dni": "<DNI del estudiante>",
    "nombre": "<nombre real>",
    "grado": "<grado>",
    "notebook": "sheets_caso1_semana1",
    "curso": "STAT_2026",
    "earned": "<suma de puntos obtenidos, sin bonus>",
    "possible": 95,
    "score_breakdown": {
      "ex1": {"e": 5, "p": 5},
      "...": "..."
    }
  }
  ```

  El campo `curso` usa exactamente el valor `"STAT_2026"` ya fijado para Bimestre 3 -
  Estadística en `WORKFORCE_HANDOFF.md` (Done log, 2026-08-07) — **no** el placeholder
  `"bimestre3_estadistica"` de una entrada anterior de ese mismo log, que quedó superado. El
  valor `"sheets_caso1_semana1"` de `notebook` es **provisional**, propuesto aquí por
  consistencia con el patrón `nb1_semana1`/`nb1_semana2` de Python — ATLAS debe confirmarlo o
  reemplazarlo si define una convención de nombres propia para el módulo de Sheets (todavía no
  existe una, ya que este es el primer entregable de Sheets).
- **`ex3` se envía con un valor booleano/effort** (`{"e": 5, "p": 5}` si la casilla está
  marcada, `{"e": 0, "p": 5}` si no), no una verificación de formato real — ver nota en §3.2.
- **Row-identity:** cualquier validación que dependa del estado de las filas del dataset después
  de `ex4` (es decir, `ex5` y `ex6`) debe hacerse por contenido (columna `Comprador`), no por
  número de fila fijo — ver nota técnica en §3.2.

---

## 8. Lo que este build deliberadamente NO incluye

- Cualquier fórmula `=SUMA()` que el estudiante escriba (queda para Semana 2, Sección C).
- La columna "Total" (`Boletos × S/5`) y cualquier cifra de recaudación en soles.
- `intex1` (Integración) — depende del total recaudado de Sección C.
- Tema visual final (nombre de agencia, paleta, achievements) — pendiente de PIXEL.
- El diseño final del Apps Script / endpoint de la API — pendiente de ATLAS (§7 es un contrato
  provisional, no la implementación).

---

## 9. Pendientes antes de publicar a estudiantes reales

1. **GAUSS:** confirmar los números heredados de §3.0 (15 filas válidas, split 8 viernes/7
   sábado, 28/28 boletos, 4 y 2 en las celdas reveladas) — son los mismos del documento
   original, re-verificar que la reestructuración de qué-va-en-B-vs-D en este documento no
   introdujo un error de conteo.
   ⚠️ **Verificación aritmética ya hecha en esta sesión (no reemplaza el sign-off formal de
   GAUSS, pero deja constancia):** sumando Boletos por fila para Viernes (filas 1,3,5,7,9,11,13,15
   con vacíos ya rellenados: 5+4+2+4+4+2+5+2) = 28; para Sábado (filas 2,4,6,8,10,12,14:
   3+6+5+3+6+2+3) = 28. Conteo de filas por día tras `ex4`: 8 viernes + 7 sábado = 15. Consistente
   con lo que ya reportaba `Ejercicios_Practica_Semanas1-2_Sheets.md` §2 y §6.
2. **PIXEL:** Theme Brief pendiente (nombre de agencia, paleta, achievements) — este build usa
   placeholders neutros en todo texto narrativo para no bloquear.
3. **ATLAS:** confirmar el desglose de XP de §5, el contrato de §7 (especialmente el valor de
   `notebook` y el manejo de row-identity), y diseñar el Apps Script real.
4. **Sincronización con `Teoria_Semanas1-2_Caso1_AbriendoElCaso.md` §0:** ese documento todavía
   usa el placeholder "45 vs. 52" para el gancho de apertura. Este build ya usa la progresión
   real (68 → 60, ver §2) para la pestaña Instrucciones — recomendable actualizar el documento de
   teoría con el mismo texto una vez GAUSS confirme los números, para que ambos documentos no
   diverjan.

---

*Preparado por SOFIA (contenido pedagógico) para build de Claude Cowork. Alcance: solo Semana 1
(Secciones A, B ampliada, D adaptada, `reto1`). Semana 2 (Sección C + Integración) queda como
build separado.*
*Fecha: 2026-08-07*

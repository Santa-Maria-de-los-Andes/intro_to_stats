# Semanas 1–2 (Sheets): Especificación de Ejercicios de Práctica — "Caso 1: Abriendo el Caso"

**Estado:** Borrador de contenido (SOFIA) — especificación de ejercicios lista para que un
agente de build (ej. Claude Cowork) construya la plantilla real de Google Sheets. Pendiente:
validación estadística de GAUSS sobre los números exactos (sección 6) y diseño final del
contrato Apps Script → API por ATLAS (sección 5, marcado como *new engineering* en
`Bimestre3_Statistics_Sheets_Module_Guide.md`, Coordination Notes).
**Contenido teórico que estos ejercicios practican:**
`Teoria_Semanas1-2_Caso1_AbriendoElCaso.md` (mismo folder).
**Resuelve un pendiente de ese documento:** el "dataset real pendiente" de la sección de Notas
internas ahora tiene números concretos y verificados (sección 2 abajo) — ver nota al final
sobre sincronizar el gancho de apertura con estos valores.

---

## 1. Estructura de pestañas de la Hoja (una copia por estudiante)

| Pestaña | Contenido | ¿Se califica? |
|---|---|---|
| 📋 **Instrucciones** | Teoría corta (del documento de teoría), leyenda de iconos, narrativa del caso | No |
| 🔍 **Ejemplo Resuelto** | Muestra pequeña ya resuelta, incluyendo el demo de `debug2` (ver sección 3) | No |
| 🕵️ **Tu Caso** | El dataset de 18 filas (sección 2), todas las celdas de respuesta editables | **Sí — vía API** |

Leyenda de iconos: reutilizar exactamente la de `COURSE_TEMPLATE.md` §4 (OBSERVA/MODIFICA/
PREDICE/COMPLETA/CONSTRUYE/DEBUG/VERIFICA/TEORÍA) — es la misma convención visual que ya
conocen los estudiantes que toman ambos módulos, y no cuesta nada mantenerla en Sheets.

---

## 2. El dataset sintético — "La Kermés" (evidencia cruda tal como llega)

18 filas exactamente como las recibe el estudiante, **sin limpiar**. Este dataset ya resuelve
el pendiente de números reales que el gancho de apertura necesitaba.

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

**Precio por boleto (dato fijo, se da en la narrativa, no es columna):** S/5.

**Números verdaderos (verificados a mano, para que GAUSS confirme antes de publicar):**
- Filas de evidencia únicas y válidas: **15** (filas 1–15; 16–17 son duplicados, 18 está
  cancelado).
- De esas 15, **2 tienen el dato de boletos vacío** (filas 7 y 12) — una "nueva pista" en la
  Sección C revela que fueron **4** y **2** respectivamente.
- **Total de boletos vendidos (correcto, final): 56**
- **Total recaudado (correcto, final): S/280** (56 × S/5)
- Split por día: **Viernes = 28 boletos (filas 1,3,5,7,9,11,13,15)**, **Sábado = 28 boletos
  (filas 2,4,6,8,10,12,14)** — suman 56. El empate exacto es intencional: sirve de
  auto-verificación ("¿los subtotales suman el total?") y de gancho para el reto bonus.
- Si un estudiante suma la columna cruda tal cual llega (sin limpiar nada), `SUMA` da **68**
  (incluye los 2 duplicados +8 y la fila cancelada +10, ignora los vacíos como 0). Si solo
  quita los duplicados a ojo pero olvida excluir la fila cancelada, da **60**. El correcto es
  **56**. Esa progresión 68 → 60 → 56 es la versión con números reales de la disputa de los
  "dos tesoreros" del gancho de apertura.

---

## 3. Progresión de ejercicios por sección

### Sección A — Recepción del Caso (~20 XP)

| Clave | Icono | Ejercicio | Respuesta esperada |
|---|---|---|---|
| `ex1` | 👀 OBSERVA + 🧩 COMPLETA | Contar cuántas filas de evidencia llegaron (sin contar encabezado) | 18 |
| `ex2` | 👀 OBSERVA + 🧩 COMPLETA | Contar cuántas columnas/pistas tiene el caso | 4 (Comprador, Boletos, Día, Estado) |
| `t1` | ❓ TEORÍA | Opción múltiple: "¿qué representa cada fila? ¿qué representa cada columna?" | (ver banco de preguntas, a redactar junto con las de la sección 5) |
| `debug1` | 🔧 DEBUG | Un compañero ficticio ya contó "20 filas" (contó el encabezado dos veces). Identificar el error. | 18, no 20 |

### Sección B — Limpieza (~40 XP)

| Clave | Icono | Ejercicio | Respuesta esperada |
|---|---|---|---|
| `ex3` | ✏️ MODIFICA | Encabezados en negrita + bordes | *(gradeable por completitud, no por valor — ver nota ATLAS abajo)* |
| `ex4` | 🔨 CONSTRUYE | Identificar y eliminar las filas duplicadas exactas | Filas restantes tras eliminar duplicados: 16 (15 únicas válidas + 1 cancelada) |
| `ex5` | 🧩 COMPLETA | Estandarizar la columna Día a exactamente "Viernes" / "Sábado" (sin mayúsculas irregulares) | Todas las celdas de Día deben ser una de esas dos cadenas exactas |
| `t2` | ❓ TEORÍA | "Una celda de Boletos está vacía. ¿Qué deberías hacer?" a) Borrar la fila b) Asumir que es 0 c) Investigar antes de asumir d) Poner el promedio del resto | c) |
| `check_mini_b` | ✅ Checkpoint | Gate: duplicados eliminados + Día estandarizado antes de desbloquear Sección C | — |

> **Ejemplo demo (`debug2`, en la pestaña Ejemplo Resuelto, no en el dataset principal):**
> tres filas de muestra donde Boletos = 4, "tres" (texto), 5. `=SUMA()` sobre esas tres da **9**,
> no 12 — porque Sheets ignora silenciosamente el texto, sin marcar error. Es un ejemplo real
> y verificable del comportamiento de `SUMA`, y refuerza la idea central de la Sección A:
> la fórmula no avisa cuando algo está mal escrito; hay que mirar primero.

### Sección C — El Total (`=SUMA()`) (~40 XP)

| Clave | Icono | Ejercicio | Respuesta esperada |
|---|---|---|---|
| `ex6` | 🧩 COMPLETA | `=SUMA()` sobre Boletos ya sin duplicados/cancelados, pero con las 2 celdas aún vacías | 50 (SUMA trata los vacíos como 0 — pregunta de reflexión: "¿confías en este número?") |
| *(narrativa)* | — | "Nueva pista": se encuentran los boletos que faltaban — fueron 4 y 2 | — |
| `ex7` | ✏️ MODIFICA | Completar las 2 celdas vacías y volver a correr `SUMA()` | **56** (total oficial de boletos) |
| `ex8` | 🔨 CONSTRUYE | Crear columna "Total" (`=Boletos*5`) por fila, luego `SUMA()` de esa columna | **280** (recaudación total) |
| `debug3` | 🔧 DEBUG | Una fórmula `SUMA` ya escrita que por error sigue incluyendo la fila cancelada en el rango | Corregir para excluir esa fila; resultado correcto = 56, no 66 |
| `check_mini_c` | ✅ Checkpoint | Gate: total boletos = 56 y total recaudado = 280 confirmados antes de Sección D | — |

### Sección D — Filtrado Básico (~35 XP)

| Clave | Icono | Ejercicio | Respuesta esperada |
|---|---|---|---|
| `ex9` | ✏️ MODIFICA | Aplicar filtro (Datos → Crear un filtro) mostrando solo Día = "Sábado" | 7 filas visibles |
| `ex10` | 🧩 COMPLETA | Subtotal de boletos con el filtro de Sábado activo | 28 |
| `ex11` | 🧩 COMPLETA | Repetir el filtro para Viernes y su subtotal | 28 |
| `t3` | ❓ TEORÍA | "Los subtotales de Sábado y Viernes suman ___. Si no coincidiera con el total general, ¿qué revisarías primero?" | 56 — revisar si algún filtro excluyó/duplicó filas por error |
| `reto1` | 🎁 BONUS (separado, `_BONUS_MAX`) | Sin usar promedio: ¿qué día recaudó más? | Empate — S/140 cada día (28 boletos × S/5). Gancho intencional hacia la Semana 3 sin nombrar "promedio" todavía |

### Integración (~15 XP)

| Clave | Ejercicio |
|---|---|
| `intex1` | Completar el resumen del caso: *"El caso cerró con **56** boletos vendidos (**S/280** recaudados), tras eliminar **2** registros duplicados, excluir **1** boleto cancelado, y completar **2** dato(s) faltante(s)."* — obliga a integrar los resultados de las 4 secciones en una sola conclusión. |

---

## 4. Resumen de XP (dentro del presupuesto de ~150 ya fijado en el module guide)

| Sección | XP |
|---|---|
| A — Recepción del Caso | 20 |
| B — Limpieza | 40 |
| C — El Total | 40 |
| D — Filtrado Básico | 35 |
| Integración | 15 |
| **Total core** | **150** |
| Bonus (`reto1`) | separado, no cuenta al `_CORE_MAX` |

ATLAS debe confirmar el desglose exacto por ejercicio dentro de cada sección (mismo criterio
que `WORKFORCE_CONTRACT.md` §2/§5 aplicado al módulo Python).

---

## 5. Contrato de datos sugerido para la API (para ATLAS / Claude Cowork)

No especificado en detalle aquí — es trabajo de ingeniería nueva marcado explícitamente en
`Bimestre3_Statistics_Sheets_Module_Guide.md` (Coordination Notes). Lo que sí se puede fijar
desde esta especificación, para que el build tenga un contrato consistente:

- Cada ejercicio tiene una **clave única** (`ex1`...`ex11`, `debug1`...`debug3`, `t1`...`t3`,
  `check_mini_b`, `check_mini_c`, `intex1`, `reto1`) — mismo patrón de taxonomía que
  `COURSE_TEMPLATE.md` §4, adaptado de código Python a celdas de Sheets.
- Un botón ("Enviar para calificar") dispara un Apps Script que lee el valor de cada celda de
  respuesta y hace `POST` a la API con un payload `{clave_ejercicio: valor}` — mismo *shape*
  que `self._scores` en el autograder de Python (`COURSE_TEMPLATE.md` §6), no un formato nuevo.
- `ex3` (formato/negrita) es difícil de verificar por valor de celda — sugerido: tratarlo como
  criterio de **esfuerzo** (¿se intentó? sí/no), igual al patrón `kind='effort'` de
  `grade_report.py` §10 del `COURSE_TEMPLATE.md`, no como criterio de corrección exacta.
- El payload debe incluir el discriminador `course` (ej. `"sheets_deteccion"` o el slug que
  PIXEL/ATLAS decidan) y un `notebook`/unidad interno (ej. `"caso1"`), siguiendo el mismo
  patrón de columnas ya usado en Supabase (`COURSE_TEMPLATE.md` §8).

---

## 6. Notas para GAUSS (antes de publicar)

- **Confirmar los números exactos** de la sección 2 (56 boletos, S/280, split 28/28,
  progresión 68→60→56) — verificados a mano en este borrador, pero necesitan una segunda
  verificación independiente antes de que un estudiante los vea como "la respuesta correcta."
- **Cuidado con el lenguaje sobre celdas vacías:** `SUMA` no falla ni da error con celdas
  vacías — las trata como 0 silenciosamente. El punto pedagógico es sobre **confiar en que la
  evidencia esté completa**, no sobre una limitación técnica de la fórmula. Ningún texto del
  ejercicio debe sugerir que "SUMA se rompe" con vacíos — sí que un total puede *parecer*
  confiable sin estarlo.
- **`debug2` (SUMA ignora texto) es el mismo tipo de precisión** — confirmar que el ejemplo
  ilustrativo (4, "tres", 5 → SUMA da 9) es representativo del comportamiento real de Google
  Sheets antes de fijarlo como demo.

---

## 7. Pendiente: sincronizar con el documento de teoría

`Teoria_Semanas1-2_Caso1_AbriendoElCaso.md`, Sección 0, todavía usa el placeholder ilustrativo
"45 vs. 52" para el gancho de apertura, con una nota explícita de que debía reemplazarse por
números reales del dataset final. Ahora que este documento fija esos números (68 → 60 → 56),
sugiero actualizar esa sección para usar la progresión real. Puedo hacer ese cambio ahora si
quieres, o dejarlo pendiente hasta que GAUSS confirme los números de la sección 6 de este
documento.

---

*Última actualización: 2026-08-05*
*Autor: SOFIA (contenido pedagógico) — listo para build de Claude Cowork; validación
estadística pendiente de GAUSS, contrato API pendiente de ATLAS*

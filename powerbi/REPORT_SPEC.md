# SMA_Tareas_Master — Especificación del rediseño (narrativa + visuales por página)

**Para:** el agente que implemente el rediseño del reporte Power BI.
**Fecha del análisis:** 2026-10-03. Datos: `public.submissions` (Supabase), curso `STAT_2026`, ruta Python, 3ro–5to.
**Estado:** especificación lista. Las decisiones abiertas (§8) traen un valor por defecto: si nadie responde, implementa ese.

Reglas del repo que siguen vigentes:
- Las páginas se generan con [build_report.py](build_report.py). **No edites a mano** los `visual.json`, porque se regeneran.
- El modelo vive en `SMA_Tareas_Master.SemanticModel/definition/` (TMDL). La metadata de cada notebook está en la tabla `Meta`, dentro de `tables/Tareas.tmdl`.

---

## 0. Por qué se rediseña

El reporte actual responde "¿cuánto se envió y cuándo?". El docente necesita saber **"¿a quién buscar esta semana y por qué?"**.

**Titular de todo el reporte:**
> Nadie termina el notebook en clase. Aprueba quien vuelve a trabajarlo después, y el reporte tiene que mostrar cada semana quién no volvió.

**Lectores:** el autor del curso y los docentes de cada grado. Usan el reporte cada semana, antes del cierre de cada notebook. Conocen bien los datos y **pueden ver nombres**. Dirección no abre este archivo (ver §8, D1).

### Hallazgos que sostienen el diseño
Se verificaron en Python sobre 4,347 envíos limpios, 54 alumnos y los 5 notebooks ya vencidos (nb1_semana1, nb1_semana2, nb3, nb4, nb5).

1. **Nadie termina el notebook en clase.** Al salir de clase está aprobado solo el 15–26% de los pares alumno × tarea. Entre los que no aprobaron en clase, 0 de 66 aprobaron sin trabajar fuera de clase; los que sí trabajaron fuera aprobaron el 88%.
2. **La brecha de 3ro está en el seguimiento, no en lo que pasa en clase.** 3ro trabaja fuera de clase en el 36% de sus tareas; 4to en el 65% y 5to en el 63%. En clase, los tres grados rinden igual.
3. **Si un alumno falla o no entrega una tarea, probablemente tampoco apruebe la siguiente.** Quien desaprobó el nb1 s1 aprobó después solo el 28%; quien lo aprobó, el 66%.
4. **El bache del nb4 empezó en la clase del 31 de agosto.** Ese día solo 3 de 13 alumnos de 3ro y 6 de 19 de 5to empezaron el notebook.
5. **"Mal → bien rápido" no detecta IA.** El autograder muestra el valor esperado en nb1 s1, nb1 s2, nb4 y nb5. En el nb3, que no lo muestra, la corrección mediana tarda unos 11 minutos; en los otros, 1 a 2.

### Medidas actuales que se eliminan o reemplazan
- **`Entregas a tiempo %`:** siempre da 100%, porque el autograder no acepta envíos tardíos.
- **Envíos por hora y por día de la semana:** solo dibujan el horario de clase.
- **`Nota promedio` como titular:** mezcla entregados con no entregados. Usa `Aprobado s/ esperado %`.
- **Logros y rachas:** no ayudan a ninguna decisión del docente. Se quedan en los leaderboards de los alumnos.

---

## 1. Correcciones de datos (FASE 1 — hacer primero)

| # | Cambio | Dónde | Detalle |
|---|---|---|---|
| D-1 | Excluir la cuenta de prueba | `expressions.tmdl` → `SubmissionsRaw`, `TestIds` | Agregar `"SCRATCH"` ("Estudiante de Prueba", 40 envíos, 3ro). Hoy aparece como el único alumno del nb6 |
| D-2 | Fusionar DNI con error de tipeo | Nueva tabla `AliasDNI` (DNIOrigen → DNICanonico), aplicada en `SubmissionsRaw` antes de `WithAlumno` | `7725963 → 77257963` (3ro) y `74114477 → 74771144` (5to) |
| D-3 | Calcular la nota sobre el puntaje máximo del notebook | Envios: nueva columna `NotaReal = MIN(100, Puntos / Tareas[PuntajeMaximo] * 100)` (si `PuntajeMaximo` está vacío, usar `Nota`) | `pct` se calcula solo con las secciones ya intentadas: el 37% de los mejores intentos se calificó sobre un notebook incompleto. No cambia el aprobado (coincide en 213 de 213 pares), pero sí infla los promedios. Las medidas de nota nuevas usan `NotaReal` |
| D-4 | Corregir el naranja del tema | `build_report.py`: `ORANGE = "#DB6C14"` (antes `#E8761A`) | El actual no pasa la prueba de luminosidad sobre el fondo oscuro `#17171D`. El par morado `#8B5CF6` + `#DB6C14` pasa todos los chequeos de daltonismo |

---

## 2. Cambios al modelo (FASE 2)

### 2.1 Tabla `Horario` (nueva, importada)
| Grado | DiaSemana | HoraInicio | HoraFin |
|---|---|---|---|
| 3ro | Lunes | 12:00 | 13:59 |
| 4to | Lunes | 10:00 | 11:59 |
| 5to | Lunes | 14:00 | 15:59 |

Estos horarios **se dedujeron de las horas de los primeros envíos**: 3ro siempre a las 12, 4to a las 10, 5to a las 14. Hay que confirmarlos (§8, D2). Usa una tabla editable como esta, igual que `Meta`, en lugar de escribir las horas dentro del código.

### 2.2 Columnas nuevas en `Envios`
- `EnClase` (lógico): el envío cae dentro de la ventana de `Horario` para el grado del alumno, en hora de Perú (la columna `FechaHora` ya está en esa hora).
- `DiasDesdeClase` (entero): días entre la fecha del envío y la fecha del primer envío `EnClase` de ese alumno en esa tarea. Si nunca envió en clase, se cuenta desde su primer envío.

### 2.3 Tabla `AlumnoTarea` (nueva; Power Query sobre `Envios`, agrupada por StudentKey × TareaKey)
| Columna | Definición |
|---|---|
| `StudentKey`, `TareaKey` | Claves; se relacionan con Alumnos y Tareas |
| `MejorNotaReal` | Máximo de `NotaReal` |
| `NotaAlSalirDeClase` | Máximo de `NotaReal` entre los envíos `EnClase`. Vacío si no tiene envíos en clase |
| `TrabajoFueraDeClase` | Tiene al menos un envío que no es `EnClase` |
| `DiasTrabajados` | Cantidad de fechas distintas (hora de Perú) |
| `DiasTrabajadosBanda` | "1", "2" o "3+" |
| `Intentos`, `MinutosTotales` | Cantidad de envíos; minutos entre el primer y el último envío |
| `Estado` | "Aprobó" si `MejorNotaReal >= 55`, si no "Desaprobó" |

Los pares **esperados pero sin entregar** no existen como filas. Las medidas los cuentan comparando contra la medida que ya existe, `Entregas esperadas` (alumnos de la banda × tareas con `CuentaParaEntrega = TRUE` y fecha límite vencida). La medida `Estado` del §3 devuelve "No entregó" cuando la fila no existe.

### 2.4 Tabla `ItemIntentos` (nueva; Power Query; necesaria solo para la página 4)
La tabla `Items` actual guarda una foto de las notas por envío, sin orden de intentos. Esta tabla reconstruye la secuencia de intentos de cada pregunta.

**Algoritmo** (igual al que se usó en el análisis en Python):
1. Ordenar los envíos de cada StudentKey × TareaKey por fecha y hora.
2. Comparar el `score_breakdown` de cada envío con el anterior. Un ítem tuvo un intento si aparece por primera vez o si cambió su `e` (o su `text`).
3. **Envíos que no cambian nada** (1,160 en el análisis): son reintentos que dieron el mismo puntaje. Asignarlos al último ítem cambiado de ese par, si ese ítem todavía no tiene el puntaje máximo. Si no, descartarlos.
4. Excluir los tipos `Teoria` (solo admiten una respuesta y quedan bloqueadas) y `Registro` (dan 1 punto solo por participar).

**Columnas:** StudentKey, TareaKey, Item, Tipo, NumIntento, FechaHoraUTC, Puntos, PuntosPosibles.

**Columnas derivadas, una fila por StudentKey × TareaKey × Item, en la tabla `ItemResumen`:**
- `PrimerIntentoOK`
- `ResueltoFinal`
- `SegundosCorreccion`: tiempo entre el último intento fallido y el primer intento con puntaje máximo. Vacío si acertó al primer intento o nunca llegó al máximo.

Si hacer esto en Power Query resulta demasiado lento (unos 4,700 envíos en STAT), es aceptable calcularlo con un script de Python versionado en `powerbi/` que escriba un CSV, siempre que se documente cómo se actualiza. En ese caso, avisa al usuario.

### 2.5 Cambios en `Meta` (Tareas.tmdl)
- Nueva columna `MuestraEsperado` (lógico): indica si los mensajes de error del autograder muestran el valor correcto. `nb1_semana1`, `nb1_semana2`, `nb4` y `nb5` = TRUE; `nb3` = FALSE. Para `nb6`, revisar en `course-python-stats/Week 7/autograder_nb6.py` si los mensajes de `checks.append((False, …))` incluyen `{exp…}` o `{EXP…}`.
- La fila del nb6 ya existe (vence el 2026-10-06 a las 04:59 UTC). No cambia.

### 2.6 Tabla desconectada `Etapas`
Para el embudo: Orden 1 Esperados, 2 Empezó en clase, 3 Volvió después de clase, 4 Aprobó.

---

## 3. Medidas DAX (FASE 2, en `_Medidas`)

Lo que importa es la definición; la sintaxis exacta queda a criterio de quien implemente. Todas responden a los segmentadores de Curso, Tarea y Grado.

| Medida | Definición |
|---|---|
| `Aprobado s/ esperado %` | Pares con `Estado = "Aprobó"` ÷ `[Entregas esperadas]` |
| `Aprobado al salir de clase %` | Pares con `NotaAlSalirDeClase >= 55` ÷ `[Entregas esperadas]` |
| `Trabajó fuera de clase %` | Pares con `TrabajoFueraDeClase` ÷ pares entregados |
| `Volvieron` / `No volvieron` | Para la tarea actual: alumnos esperados con / sin envíos fuera de clase. Los que no entregaron cuentan como "No volvieron" |
| `Estado` (contexto alumno × tarea) | "Aprobó", "Desaprobó" o "No entregó" (cuando no hay fila en AlumnoTarea) |
| `Estado icono` | ✓ / ✗ / – , para que el estado se lea sin depender del color |
| `Dias desde ultimo envio` | `TODAY()` − último `Fecha` del alumno |
| `Mediana del grado` | Mediana de `MejorNotaReal` de los alumnos del mismo grado, en la misma tarea, quitando el filtro del alumno |
| `Puntos perdidos` | Suma de (PuntosPosibles − Puntos) del mejor envío, por ítem |
| `% al primer intento` | Promedio de `ItemResumen[PrimerIntentoOK]` |
| `% resuelto final` | Promedio de `ItemResumen[ResueltoFinal]` |
| `Minutos para corregir (mediana)` | Mediana de `SegundosCorreccion` / 60 |
| `Dias para cierre` | Días entre hoy y `FechaLimite` de la próxima tarea que aún no vence |
| `Titulo resumen` | Texto: "‹tarea›: X de N aprobaron (P%). M no volvieron después de clase." |
| `Titulo countdown` | Texto: "‹tarea› cierra en D días · M sin volver" |
| `Etapa valor` | `SWITCH` sobre `Etapas[Orden]`: esperados / empezó en clase / volvió / aprobó |

Las medidas que ya existen y siguen en uso no se tocan: `Entregas esperadas`, `Tasa de entrega`, `Alumnos en riesgo` y `Entregas faltantes`. `Alumnos en riesgo` debe pasar a usar `NotaReal`.

---

## 4. Reglas visuales (aplican a todas las páginas)

- **Colores:**
  - Morado `#8B5CF6` para el dato principal.
  - Gris `#6B6B76` (TEXT_3) para el contexto. Es intencional que sea gris: indica lo que no hay que mirar primero.
  - Naranja `#DB6C14` solo como el extremo "bajo" de la escala divergente y para el estado "Desaprobó".
- **Escala divergente** para notas y tasas: naranja · neutro `#2A2A33` en 55 · morado. Es la función `gradient()` que ya existe; se justifica porque 55 es un umbral real.
- **Estados** (Aprobó / Desaprobó / No entregó): siempre con ícono y texto, nunca solo con color.
- **Títulos que dicen el hallazgo**, no el tema. Cuando dependen de los filtros, el título del visual toma su texto de una medida.
- **Prohibido:** gráficos con dos ejes, tortas, donas y etiquetas en cada punto. Etiquetas solo en la serie principal o en gráficos de 3 barras o menos.
- **Segmentadores:** una sola fila arriba (Curso, Tarea, Grado), sincronizados en todas las páginas.
- **Cada visual** tiene habilitado *Mostrar como tabla*. Así ningún valor depende solo de la información sobre herramientas.
- **Grupos chicos:** donde un grupo tenga menos de 15 alumnos (hoy 3ro tiene 13), mostrar el n en la información sobre herramientas o en una nota.

---

## 5. Páginas

Para cada página: **narrativa** (qué tiene que entender el lector) y **visuales** (cómo se construye). Coordenadas sobre un lienzo de 1280×720, como en `build_report.py`; son orientativas.

### Página 1 — Vista general (`page_resumen`, se reescribe)

**Narrativa**
- **Lector:** docente o autor, al inicio de la semana. La lee en 30 segundos.
- **Titular (dinámico):** "‹tarea›: X de N aprobaron (P%). M no volvieron después de clase."
- **Qué hacer:** si "no volvieron" es alto, ir a la página Seguimiento.
- **Orden:** titular → 4 KPI → en clase contra final (la prueba) → brecha por grado (el alcance) → embudo (en qué paso se pierden).
- **Advertencia visible:** "3ro: n=13" junto a la matriz.

**Visuales**

| # | Visual (tipo PBIR) | Campos | Detalle |
|---|---|---|---|
| 1.1 | Cuadro de texto o tarjeta ancha | `[Titulo resumen]` | Fila superior, debajo de los segmentadores |
| 1.2 | 4 × `card` (o `cardVisual` con valor de referencia) | `Aprobado s/ esperado %`, `Tasa de entrega`, `Trabajó fuera de clase %`, `Alumnos en riesgo` | Etiqueta de referencia: "vs tarea anterior" si se puede, si no se omite |
| 1.3 | `clusteredColumnChart`, X = `Tareas[NombreTarea]` (por `Orden`) | Y: `Aprobado al salir de clase %` (gris), `Aprobado s/ esperado %` (morado) | Etiquetas solo en la serie morada. Título: "Lo que se aprueba se aprueba después de clase" |
| 1.4 | `pivotTable`: filas = Tarea, columnas = Grado | `Aprobado s/ esperado %` con fondo `gradient()` | Información sobre herramientas: n de alumnos esperados. Nota "3ro: n=13" |
| 1.5 | `funnel`, categoría = `Etapas[Etapa]` (por Orden) | `Etapa valor` | Un solo color morado. Reacciona al filtro de Tarea |

**Se elimina de esta página:** "Envíos por día", "Nota promedio por tarea" y "Nota por grado". La matriz 1.4 reemplaza a "Nota por grado".

### Página 2 — Estudiante (`page_estudiante`, nueva, drill-through)

**Narrativa**
- **Lector:** el docente, justo antes de hablar con el alumno.
- **Tiene que responder en 10 segundos:** ¿cómo va, desde cuándo, y qué le falta?
- **Titular:** "‹Nombre›: aprobó A de N · última actividad hace D días".
- **Qué no va:** posición en un ranking, nivel ni logros. No ayudan a decidir nada y ponen al alumno a la defensiva si ve la pantalla.

**Visuales**

| # | Visual | Campos | Detalle |
|---|---|---|---|
| 2.0 | Configuración de drill-through | Campo: `Alumnos[StudentKey]` (o Nombre) | Se llega desde Alumnos, Libro, Seguimiento y Actividad. Botón "Atrás" |
| 2.1 | `multiRowCard` | Nombre, Grado, DNI, `Dias desde ultimo envio` | — |
| 2.2 | `pivotTable` de 1 fila, columnas = Tarea | `Estado icono` + `Estado` | Fondo: morado (Aprobó), naranja (Desaprobó), gris (No entregó), siempre con el ícono |
| 2.3 | `lineChart` solo con marcadores (línea de 0 px, marcador de 8 px), X = Tarea | `MejorNotaReal` (morado), `Mediana del grado` (gris) | Línea constante en 55. Funciona como gráfico de puntos, que Power BI no tiene nativo |
| 2.4 | `tableEx` | Tarea, `DiasTrabajados`, `TrabajoFueraDeClase` (ícono), `Intentos`, `MinutosTotales` | — |
| 2.5 | `barChart` horizontal, orden descendente | Item × `Puntos perdidos` | Responde a la tarea elegida. Un solo color |
| 2.6 | "Para conversar" | — | **Fase 3, no se implementa ahora.** Ver §8, D3 |

### Página 3 — Seguimiento después de clase (`page_seguimiento`, nueva; reemplaza la parte de puntualidad de `page_actividad`)

**Narrativa**
- **Lector:** el docente o el autor, a mitad de semana. Lo que hace con esta página es escribirle a cada alumno de la lista.
- **Titular (dinámico):** "‹tarea› cierra en D días · M sin volver".
- **Qué hacer:** contactar a los de la lista 3.2 empezando por los de nota más baja en clase.
- **Advertencia junto al 3.4:** "Asociación, no causa: los más motivados trabajan más días y también aprueban más."

**Visuales**

| # | Visual | Campos | Detalle |
|---|---|---|---|
| 3.1 | `card` | `[Titulo countdown]` | — |
| 3.2 | `tableEx` | Alumno, Grado, `NotaAlSalirDeClase` (barra de datos), `Dias desde ultimo envio` | Filtro: no volvieron (incluye a quienes no entregaron). Orden ascendente por nota en clase |
| 3.3 | `clusteredColumnChart`, X = `DiasDesdeClase` (0…6) | Cantidad de pares; series por `Estado`: Aprobó (morado) y Desaprobó (gris) | Título: "¿Cuándo vuelven los que aprueban?" |
| 3.4 | `columnChart`, X = `DiasTrabajadosBanda` (1 / 2 / 3+) | `Aprobado %` entre los entregados | Etiqueta en cada barra con % y n |
| 3.5 | `barChart` horizontal, X = `Trabajó fuera de clase %`, Y = Grado | Un solo color; línea constante con el promedio del curso | **No resaltar 3ro**: la distancia a la línea ya lo muestra |

### Página 4 — Actividad y calidad de los ítems (`page_actividad`, se reescribe; absorbe parte de `page_ejercicios`)

**Narrativa**
- **Lector:** sobre todo el autor del curso, para mejorar los notebooks. Los docentes la usan además por la tabla de inactivos.
- **Titular:** "Los ítems donde los alumnos se quedan atascados, y quién lleva más de una semana sin actividad".
- **Advertencia obligatoria junto al 4.2:** "En las tareas que muestran el valor esperado, este tiempo mide copiar el número, no entender el error."
- **No usar la palabra "IA"** en ninguna parte de esta página.

**Visuales**

| # | Visual | Campos | Detalle |
|---|---|---|---|
| 4.1 | `scatterChart`: X = `% al primer intento`, Y = `% resuelto final`, detalle = Tarea + Item | Información sobre herramientas: Tarea, Item, Tipo, n | Líneas constantes en X = 50% e Y = 80%. Sin etiquetas en los puntos; los nombres van en la información sobre herramientas y en la tabla. Ocultar los ítems con n < 10 |
| 4.2 | `barChart` horizontal, Y = Tarea | `Minutos para corregir (mediana)`; color por `Tareas[MuestraEsperado]` (gris = sí, morado = no) | Leyenda: "Muestra el valor esperado" |
| 4.3 | `clusteredColumnChart`, X = Tarea | `% al primer intento` (gris) y `% resuelto final` (morado), filtrado a Tipo = "Reflexion IA" | Título: "Las reflexiones casi no se reintentan" |
| 4.4 | `tableEx` | Alumno, Grado, `Dias desde ultimo envio`, última tarea | Ícono de alerta si pasan 7 días. Orden descendente |

**Se elimina:** envíos por hora, envíos por día de la semana, "Entregas a tiempo por tarea" y "Logros desbloqueados".

### Páginas que se mantienen
- **`page_libro`:** sin cambios, salvo que la nota pasa a `NotaReal`.
- **`page_alumnos`:** sin cambios. Habilitar drill-through hacia Estudiante.
- **`page_ejercicios`:** se mantiene la tabla de detalle. El gráfico "Éxito por tipo de ítem" pasa a usar `% al primer intento` y `% resuelto final` (columnas agrupadas, gris y morado).

**Orden final de páginas:** Vista general · Seguimiento · Libro · Alumnos · Estudiante (oculta, solo drill-through) · Actividad · Ejercicios.

---

## 6. Números de referencia para verificar

Se calcularon en Python con los datos al 2026-10-03, ya aplicadas las correcciones D-1 a D-3, para STAT_2026 de 3ro a 5to y los 5 notebooks vencidos. En el análisis, "en clase" se definió como día hábil entre las 07:00 y las 15:59 de Perú; con la tabla `Horario`, las diferencias deberían ser de ±2 puntos porcentuales. Si un número difiere más que eso, la definición está mal implementada.

| Comprobación | Valor esperado |
|---|---|
| Alumnos en el padrón (con al menos un envío) | 54 (3ro 13, 4to 22, 5to 19) |
| Pares esperados / entregados | 270 / 213 |
| Pares aprobados (≥55) | 137 |
| Aprobado s/ esperado, por grado (promedio por alumno) | 3ro 28%, 4to 56%, 5to 60% |
| Entregó, por grado | 3ro 68%, 4to y 5to en conjunto 82% |
| Aprobado al salir de clase (sobre lo entregado) | 3ro 20%, 4to 15%, 5to 26% |
| Trabajó fuera de clase (sobre lo entregado) | 3ro 36%, 4to 65%, 5to 63% |
| Aprobación por días trabajados | 1 día: 56 de 127 (44%) · 2 días: 70 de 75 (93%) · 3+: 11 de 11 (100%) |
| Tasa de entrega del nb4 por grado | 3ro 31%, 4to 86%, 5to 68% |
| Envíos del nb6 de alumnos reales | 0 (al 2026-10-03) |
| % al primer intento por tipo | Debug 82%, Ejercicio 53%, Integración 65%, Reto 59%, Reflexión 36% |
| Mediana de minutos para corregir | nb3 ≈ 11; nb1_semana1 ≈ 0.9; nb4 ≈ 1.2; nb1_semana2 ≈ 1.3; nb5 ≈ 2 |

---

## 7. Plan de trabajo y criterios de aceptación

**Fase 1 (datos):** D-1 a D-4.
*Se acepta cuando:* refrescar el modelo da 54 alumnos y ningún envío de `SCRATCH`.

**Fase 2 (modelo y medidas):** del §2.1 al §2.6 y el §3.
*Se acepta cuando:* los números del §6 coinciden dentro de la tolerancia, y `Estado` devuelve "No entregó" para los pares esperados sin envío.

**Fase 3 (páginas):** las del §5, en este orden: Vista general → Seguimiento → Estudiante → Actividad.
*Se acepta cuando:*
- Correr `python build_report.py` no da errores.
- Abrir el `.pbip` en Power BI Desktop no da errores de visual.
- Cada visual cumple el §4: sin dos ejes, sin tortas, estados con ícono y *Mostrar como tabla* habilitado.
- El drill-through funciona desde Alumnos y desde Seguimiento.

**Después de terminar:**
- Actualizar la sección `powerbi/` del [README](../README.md): tablas nuevas y cómo editar `Horario`.
- Si el usuario quiere, agregar una entrada al Done log de `WORKFORCE/WORKFORCE_HANDOFF.md`.

---

## 8. Decisiones abiertas (con valor por defecto)

| # | Pregunta | Valor por defecto si nadie responde |
|---|---|---|
| D1 | ¿Dirección va a abrir este archivo? | **No.** Un solo archivo, solo para docentes. Si la respuesta es sí: armar un `.pbip` aparte con solo la Vista general y sin la matriz por grado. Power BI no oculta páginas de forma segura dentro del mismo archivo |
| D2 | ¿El horario es fijo (lunes: 4to a las 10, 3ro a las 12, 5to a las 14, bloques de 2 h)? | Sí, usar la tabla del §2.1, editable |
| D3 | ¿La página de Estudiante incluye "Para conversar" (textos pegados, respuestas casi idénticas entre alumnos)? | **No por ahora.** Requiere que los widgets de texto registren cuándo el alumno pega texto y el tiempo de escritura, y que `Items` conserve el campo `text`. Es una fase posterior. Si se implementa, el rótulo debe decir "patrones para conversar con el alumno", nunca "uso de IA" |
| D4 | ¿Quién usa la página de Seguimiento? | Los docentes y el autor |

## 9. Fuera de alcance
- **Cambios al autograder:** dejar de mostrar el valor esperado, registrar la pregunta de cada envío, registrar cuándo se pega texto. Están recomendados, pero son otro ticket.
- **Rediseño para CS_2026 y Sheets:** siguen accesibles con el filtro de Curso, pero el diseño piensa en STAT_2026.
- **Ranking de alumnos:** ya existe en los leaderboards.

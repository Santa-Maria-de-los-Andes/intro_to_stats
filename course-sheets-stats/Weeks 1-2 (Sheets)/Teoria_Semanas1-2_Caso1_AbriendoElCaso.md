# Semanas 1–2: Teoría — "Caso 1: Abriendo el Caso"

**Estado:** Borrador de contenido (SOFIA) — pendiente de tematización final (PIXEL: paleta,
nombre exacto de la agencia, flavor text — ver Coordination Notes en
`Bimestre3_Statistics_Sheets_Module_Guide.md`) y de validación estadística formal (GAUSS).
**Estructura de secciones:** Sección A Recepción del Caso → B Limpieza → C El Total (SUMA) →
D Filtrado Básico, siguiendo la progresión ya fijada en el guide (`Core Activity`, Semanas 1-2).
**Dataset:** placeholder narrativo — "la Kermés" (venta de entradas de un festival escolar) —
ver nota de pendientes al final; falta reemplazar por un dataset real de números concretos
antes de construir la plantilla de Sheets.

> Nota de lenguaje: todo el texto orientado al estudiante va en español; los nombres de fórmulas
> siguen la convención de Sheets en español (`SUMA`, no `SUM`), según se fijó en el module guide.
> El nombre de la agencia detectivesca abajo usa el placeholder "la Agencia" hasta que PIXEL
> cierre el tema visual — la teoría y el orden pedagógico no cambian cuando eso se defina.

---

## 0. Apertura — El Gancho (antes de cualquier fórmula)

**Objetivo:** que el primer minuto de la Misión incomode productivamente — no enseñar SUMA
todavía, sino hacer sentir *por qué* hace falta.

> *"Dos tesoreros de la Kermés cuentan el mismo montón de boletos vendidos. Uno dice que se
> vendieron 45 boletos. El otro dice 52. Ninguno mintió. Ninguno se equivocó al sumar.
> ¿Cómo es posible?"*

Se presenta la misma "pila de evidencia" (una lista desordenada de boletos vendidos, con
algunas filas duplicadas, una fila de un boleto cancelado que uno de los dos sí contó, y un
par de espacios en blanco) a dos personajes que llegan a sumas distintas — ambos sumando
correctamente, sobre datos distintos porque nadie limpió la lista primero. Se pide a los
estudiantes votar quién tiene razón.

**Revelación:** los dos hicieron bien la suma. El problema nunca fue el cálculo — fue que
nadie organizó la evidencia antes de calcular. Esa es la apertura del Caso 1:

> *"Te acaba de llegar el primer caso de la Agencia. La evidencia está desordenada, con
> duplicados y espacios vacíos — antes de poder calcular nada con confianza, tu primer trabajo
> como detective es poner la evidencia en orden."*

**Nota para GAUSS/ATLAS:** los números exactos del gancho (45 vs. 52, cuántas filas duplicadas,
etc.) son ilustrativos — deben fijarse contra el dataset real elegido para la plantilla antes
de publicarse, no quedarse como números inventados de este borrador (mismo criterio que el
borrador equivalente de la Semana 1-2 en Python).

---

## 1. Teoría Desbloqueada — Fundamentos (bloque formal, antes de la Sección A)

Bloque de teoría **formal y nombrada explícitamente** — el estudiante debe poder nombrar el
concepto, no solo intuirlo. Se evalúa después con preguntas `check_tN` (pendiente: banco de
preguntas en documento separado, mismo patrón que `Preguntas_Teoricas_Semanas1-2.md` del
módulo de Python).

### 1.1 ¿Qué es la Estadística? (versión para 1°-2° secundaria)

**Definición simple:** la estadística es organizar y resumir información para responder una
pregunta con evidencia, en lugar de con opinión.

**¿Por qué importa a esta edad?** Ejemplos deliberadamente cercanos a su vida diaria, no
ejemplos abstractos de adultos:
- **Entre amigos:** decidir objetivamente cuál es el snack favorito del salón, no solo el que
  grita más fuerte.
- **En el deporte:** saber si de verdad un jugador anota más que otro, o solo lo recordamos
  porque tuvo un partido bueno.
- **En una tienda o kermés escolar:** saber cuánto se vendió realmente, no solo "sentir" que
  fue mucho o poco.
- **En redes sociales:** reconocer cuándo un número que alguien publica ("todos compran esto")
  en realidad no está bien contado.

> No se introduce todavía la división descriptiva/predictiva/prescriptiva del módulo de
> Python — es innecesaria en esta etapa y no aporta a las Semanas 1-2. Este módulo se queda
> enteramente en el territorio descriptivo; no hace falta nombrar las otras ramas.

### 1.2 Datos: observaciones y variables (metáfora del expediente)

Un conjunto de datos es una tabla de **evidencia** (filas — cada boleto vendido, cada
encuestado, cada partido) y **pistas** (columnas — cada dato que se registró sobre esa
evidencia: cantidad, fecha, nombre, precio). No es "la verdad absoluta" — es un **registro**,
y los registros pueden tener errores: filas repetidas, espacios vacíos, información mal
escrita.

### 1.3 Por qué organizar antes de calcular

Antes de calcular cualquier cosa — incluso algo tan simple como un total — hay que revisar:
- **¿Hay evidencia duplicada?** (la misma fila copiada dos veces)
- **¿Hay espacios en blanco?** (evidencia incompleta)
- **¿Está todo escrito de forma consistente?** (mayúsculas/minúsculas, texto vs. número)

Esta es la idea central que paga la apertura: **la fórmula nunca fue el problema — la evidencia
desordenada sí lo era.**

### 1.4 SUMA — definida formalmente

**Definición:** `=SUMA()` calcula el total de un grupo de valores numéricos.

**Cuándo sirve:** cuando la pregunta es "¿cuánto en total?" sobre algo que tiene sentido sumar
— dinero recaudado, boletos vendidos, horas jugadas.

**Cuándo NO sirve (plantar la semilla para semanas futuras):** sumar no responde "¿cuál es lo
típico?" (eso vendrá en la Semana 3 con `PROMEDIO`) ni "¿qué fue lo más común?" (Semana 5 con
`MODA`) — ni tiene sentido sobre datos que no son cantidades (sumar "colores favoritos" no
significa nada). No resolver esta tensión todavía; solo nombrarla, para que la pregunta quede
abierta de forma natural hacia la Semana 3.

---

## 2. Teoría por Sección (bloques cortos, cada uno justo antes de su ejercicio)

Regla del curso: teoría → mini-ejercicio inmediato → check → siguiente teoría — igual que el
módulo de Python (`COURSE_TEMPLATE.md` §4). Los bloques de abajo son las "dosis" que preceden
a cada sección de la plantilla de Sheets de esta Misión.

### Sección A — Recepción del Caso (mirar los datos crudos)

Antes de tocar una sola fórmula: mirar la hoja tal como llegó. Identificar en voz alta —
¿cuántas filas hay?, ¿qué columnas tiene?, ¿algo se ve raro (vacío, repetido, mal escrito)?
Esto es **reconocimiento**, no cálculo — el mismo principio que `.head()`/`.info()` en el
módulo de Python, adaptado a "mirar antes de tocar" en una hoja de cálculo.

### Sección B — Limpieza (formato, quitar duplicados, rellenar/marcar vacíos)

Organizar la evidencia: encabezados en negrita, formato de número consistente, identificar y
eliminar filas duplicadas, decidir qué hacer con espacios vacíos (no siempre se borran — a
veces significan "no aplica," y eso también es información). Esta sección es la que
**resuelve** el misterio de la apertura: al limpiar la lista de boletos, ambos tesoreros
llegarían al mismo número.

### Sección C — El Total (`=SUMA()`)

Ahora que la evidencia está limpia, calcular el total tiene sentido y produce un número en el
que se puede confiar. Aplicar `SUMA` para responder la pregunta original del caso ("¿cuánto se
recaudó en total?").

> ⚠️ Nota de precisión estadística (GAUSS, a confirmar): remarcar explícitamente que "ahora
> confiamos en el número" es **porque los datos están limpios, no porque `SUMA` sea una fórmula
> especial** — la fórmula fue correcta desde el inicio; lo que cambió fueron los datos que
> recibió. Este es el mismo tipo de distinción que el módulo de Python hace entre "valor
> atípico" y "dato malo" — conceptualmente relacionado, vale la pena que GAUSS confirme que el
> paralelismo es válido antes de fijarlo en la plantilla final.

### Sección D — Filtrado Básico (Datos → Crear un filtro)

Aplicar un filtro para aislar un subconjunto de la evidencia (por ejemplo, "solo boletos
vendidos el sábado") y volver a calcular el total sobre ese subconjunto. La idea clave:
filtrar es **hacerle una pregunta más específica a los datos**, no un truco de la interfaz.

---

## 3. Por qué este orden funciona como primera sesión

La apertura crea la necesidad de la Sección A (no se puede resolver el enigma de los dos
tesoreros sin mirar la evidencia real primero) → mirar la evidencia en A revela los problemas
que la Sección B resuelve → una vez limpia, B habilita que el total de la Sección C sea
confiable → confiar en el total general en C abre la pregunta natural de la Sección D ("¿y si
solo quiero el total de una parte?"). Cada bloque responde una pregunta que dejó abierta el
anterior, igual que en el módulo de Python — se siente como una historia, no como un temario.

---

## 4. Patrón para las semanas siguientes (para consistencia, no para esta semana)

Mismo propósito que la tabla equivalente del módulo de Python — cada Caso futuro abre con su
propio bloque "Teoría Desbloqueada," evaluado con `check_tN`:

| Semana | Teoría formal a introducir |
|---|---|
| 1–2 | Qué es un dato/observación/variable; por qué organizar antes de calcular; `SUMA` |
| 3 | `PROMEDIO`: definición formal, "valor típico," sensibilidad a valores extremos |
| 4 | `MEDIANA`: definición formal, resistencia a valores extremos, cuándo diverge de `PROMEDIO` |
| 5 | `MODA`: definición formal, dato categórico vs. numérico |
| 6 | Qué hace confiable o engañoso un número o gráfico (eje truncado, muestra sesgada, promedio fuera de contexto) |
| 7 | Cuándo usar cada tipo de gráfico (barra, circular, línea) según la pregunta que se quiere responder |

---

## 5. Preguntas `check_tN` (Semanas 1–2)

**Pendiente:** banco de preguntas de opción múltiple para esta Misión, mismo patrón que
`Preguntas_Teoricas_Semanas1-2.md` del módulo de Python (una pregunta por concepto formal de
la sección 1, distractores, tabla de puntaje sugerido para ATLAS). No incluido en este
documento para no bloquear la teoría en un solo entregable — crear como archivo separado
cuando se retome este ticket.

---

## Notas internas / pendientes

- **Dataset real pendiente:** este documento usa "la Kermés" como placeholder narrativo con
  números inventados para el gancho. Antes de construir la plantilla de Sheets, reemplazar por
  un dataset concreto (real o realista, aprobado por GAUSS) con duplicados/vacíos genuinos, no
  fabricados de forma que se note.
- **Tema visual pendiente de PIXEL** — nombre de la agencia, paleta, flavor text (ticket en
  `Bimestre3_Statistics_Sheets_Module_Guide.md` → Coordination Notes). Este documento usa
  lenguaje neutro ("la Agencia") a propósito para no bloquear el contenido mientras eso se
  resuelve.
- **Preguntas `check_tN`** aún no escritas — ver sección 5.
- **Mecánica de puntaje/XP exacta** (cuántos puntos por sub-sección dentro del presupuesto de
  ~150 XP ya fijado en el module guide) queda para el pase de ATLAS, no se fija aquí.

---

*Última actualización: 2026-08-05*
*Autor: SOFIA (contenido pedagógico) — validación estadística pendiente de GAUSS*

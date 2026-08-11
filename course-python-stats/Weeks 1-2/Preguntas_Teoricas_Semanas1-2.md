# Semanas 1–2: Banco de Preguntas Teóricas (`check_tN`)

**Estado:** Borrador de contenido (SOFIA) — pendiente de: (1) revisión de GAUSS (que ningún
enunciado ni distractor induzca una idea estadísticamente incorrecta), (2) asignación de
puntaje exacto por ATLAS dentro del presupuesto de la sección correspondiente
(`WORKFORCE_CONTRACT.md` §2).
**Fuente del contenido evaluado:** `Teoria_Semanas1-2_Mision1_RecuperacionDeDatos.md` (mismo
folder) — cada pregunta aquí reemplaza y expande el borrador de la sección 5 de ese documento;
esa sección ahora apunta aquí en vez de duplicar contenido.
**Formato:** opción múltiple, patrón `respuesta_tN = "?"` (`COURSE_TEMPLATE.md` §4, ícono ❓
TEORÍA). Una pregunta por concepto nombrado en el bloque "Teoría Desbloqueada."

---

## Bloque 1 — ¿Qué es la estadística? / Las tres ramas

### check_t1 — Definición e importancia
**Pregunta:** Un periodista afirma "el colegio X es el mejor de la ciudad" citando solo el
promedio de notas de sus 5 mejores alumnos. ¿Qué le falta a esa afirmación para ser un uso
correcto de la estadística?
a) Nada, un promedio siempre es suficiente para comparar
b) Considerar a todos los estudiantes, no solo una muestra elegida a conveniencia
c) Usar una gráfica en vez de un número
d) Cambiar el promedio por la moda
**Respuesta correcta:** b)
**Por qué:** la estadística exige mirar el conjunto de datos completo (o una muestra
representativa), no una selección que ya favorece la conclusión deseada.
**Distractor clave:** a) — apunta directamente al malentendido "un número correcto = una
conclusión correcta," que es justo lo que el gancho de apertura de la semana busca desmontar.

### check_t2 — Clasificar la rama de la estadística
**Pregunta:** Un hospital usa el historial de pacientes de los últimos 5 años para **estimar**
cuántas camas necesitará el próximo mes. ¿Qué rama de la estadística está usando principalmente?
a) Descriptiva
b) Predictiva
c) Prescriptiva
d) Ninguna, esto no es estadística
**Respuesta correcta:** b) Predictiva
**Por qué:** está proyectando un valor futuro a partir de patrones existentes — la definición
exacta de predictiva.

### check_t3 — Descriptiva vs. predictiva (el error común de esta semana)
**Pregunta:** Un programa agrupa a 500 clientes en 4 grupos según sus hábitos de compra
similares. ¿Qué rama de la estadística describe
mejor esto?
a) Predictiva, porque usa un algoritmo
b) Descriptiva, porque organiza y resume lo que ya existe en los datos
c) Prescriptiva, porque recomienda una acción
d) No es estadística, es solo programación
**Respuesta correcta:** b)
**Por qué:** agrupar (clustering) organiza patrones existentes; no proyecta un valor futuro.
**Nota GAUSS:** esta pregunta existe específicamente para prevenir el error de archivar
k-means (Semana 7) como "predictivo" — se siembra la distinción desde la Semana 1.

---

## Bloque 2 — Media, Mediana, Moda

### check_t4 — Sensibilidad de la media
**Pregunta:** En un salón de 20 estudiantes, 19 ganan S/10 de propina por una encuesta y uno
gana S/500 por un error de registro. ¿Qué le pasa a la media del grupo?
a) No cambia, la media ignora valores extremos
b) Sube mucho, porque la media se ve arrastrada por valores extremos
c) Baja mucho
d) Se vuelve imposible de calcular
**Respuesta correcta:** b)
**Por qué:** la media es la suma dividida entre la cantidad — un solo valor extremo la desplaza
notablemente cuando el grupo es pequeño.

### check_t5 — Cuál medida usar
**Pregunta:** Usando el mismo salón del ejercicio anterior, ¿qué medida describe mejor "lo
típico" de la propina que recibió la mayoría?
a) La media  b) La mediana  c) Ambas son igual de buenas aquí  d) Ninguna aplica
**Respuesta correcta:** b) La mediana
**Por qué:** la mediana no se mueve por el valor extremo — sigue reflejando el centro real de
la mayoría de los datos (S/10).

### check_t6 — Cuándo usar la moda
**Pregunta:** Se tiene una lista con el deporte favorito de 200 estudiantes (fútbol, vóley,
básquet, natación...). ¿Qué medida de tendencia central tiene sentido calcular aquí?
a) La media  b) La mediana  c) La moda  d) La desviación estándar
**Respuesta correcta:** c) La moda
**Por qué:** son datos categóricos (no numéricos) — no se puede "sumar" fútbol + vóley, así que
media y mediana no aplican. La moda (el valor más frecuente) sí.

### check_t7 — Media y mediana muy distintas: ¿qué significa?
**Pregunta:** En un dataset de ingresos, la media es S/3,200 y la mediana es S/1,800. ¿Qué es
lo más razonable de concluir?
a) Uno de los dos cálculos está mal
b) La distribución probablemente está sesgada — hay valores altos poco frecuentes que suben
   la media
c) Los datos no sirven y hay que descartarlos
d) Hay que usar solo la moda en vez de ambas
**Respuesta correcta:** b)
**Por qué:** es exactamente el patrón del gancho de apertura de la semana — ambos cálculos son
correctos; la brecha entre ellos es información sobre la forma de la distribución, no un error.

---

## Bloque 3 — Dispersión, Datasets, Valores Atípicos

### check_t8 — Qué mide la desviación estándar
**Pregunta:** Si un dataset tiene una desviación estándar muy baja, ¿qué indica eso?
a) Los datos están muy cerca del promedio, poco dispersos
b) Los datos tienen muchos errores
c) La media está mal calculada
d) El dataset es muy grande
**Respuesta correcta:** a)
**Por qué:** desviación estándar = "en promedio, qué tan lejos está cada dato del centro" —
baja desviación significa poca dispersión, no un juicio sobre calidad de los datos.

### check_t9 — Observaciones vs. variables
**Pregunta:** En una tabla de datos de atletas olímpicos, cada **fila** representa un atleta y
cada **columna** representa un dato sobre ese atleta (edad, altura, deporte...). ¿Cómo se llama
correctamente cada fila y cada columna?
a) Fila = variable, columna = observación
b) Fila = observación, columna = variable
c) Ambas son observaciones
d) Ambas son variables
**Respuesta correcta:** b)
**Por qué:** definición estándar usada durante todo el curso — fila = un caso/observación,
columna = una característica/variable medida sobre cada caso.

### check_t10 — Qué es (y qué no es) un valor atípico
**Pregunta:** En el dataset olímpico aparece un atleta con una altura muy por encima del resto.
¿Qué es lo correcto de asumir sobre ese dato antes de investigarlo?
a) Es un error de registro y debe eliminarse de inmediato
b) Es un valor atípico — una observación inusual que puede ser real y válida
c) Significa que todo el dataset no es confiable
d) Hay que reemplazarlo automáticamente por la media
**Respuesta correcta:** b)
**Por qué:** es el malentendido más común en estudiantes nuevos a estadística — un atípico es
"inusual," no automáticamente "erróneo." Puede ser un caso real (ej. un atleta de básquet
excepcionalmente alto).

---

## Bloque 4 — Filtrado y Comparación de Grupos

### check_t11 — Qué hace un filtro
**Pregunta:** Cuando se escribe `df[df['edad'] > 30]`, ¿qué se está haciendo conceptualmente?
a) Borrando permanentemente a los atletas menores de 30 del archivo original
b) Haciéndole una pregunta específica a los datos: "muéstrame solo los casos que cumplen esta
   condición"
c) Calculando el promedio de edad
d) Ordenando el dataset de mayor a menor
**Respuesta correcta:** b)
**Por qué:** el filtrado crea una vista/subconjunto para responder una pregunta puntual; no
modifica el dataset original.

### check_t12 — El límite de comparar grupos
**Pregunta:** Al comparar con `.groupby()` el promedio de medallas entre dos países, se
encuentra que el País A tiene un promedio más alto que el País B. ¿Qué se puede concluir
correctamente?
a) El País A es "mejor" en todo, y esa es la causa de la diferencia
b) Existe una diferencia entre los grupos en este dataset — pero esto no explica por qué existe
   esa diferencia
c) No se puede concluir nada de una comparación de grupos
d) El País B debería copiar exactamente lo que hace el País A
**Respuesta correcta:** b)
**Por qué:** comparar grupos muestra *qué* es diferente, no *por qué* — la explicación causal
es tema protegido de la Semana 5; esta pregunta siembra la barrera sin adelantar esa clase.

---

## Bloque 5 — Semana 2 independiente (numeración propia, reiniciada en 0)

**Contexto (2026-08-11):** por decisión del usuario, Semana 2 dejó de continuar la
numeración global de Semana 1 — ahora tiene su propia secuencia `check_t0`–`check_t4`
dentro de `autograder_nb1_semana2.py` (ticket #10, no escrito todavía). Las tres
primeras reutilizan preguntas ya existentes de este banco bajo su nuevo número local;
las dos últimas son **nuevas**, escritas para esta reestructuración y documentadas
aquí por primera vez.

| Nº local (Semana 2) | Contenido | Fuente |
|---|---|---|
| `check_t0` | Valores atípicos | = `check_t10` de este banco, verbatim |
| `check_t1` | Filtrado booleano | = `check_t11` de este banco, verbatim |
| `check_t2` | Equivalencia de un filtro combinado | **Nueva**, ver abajo |
| `check_t3` | Qué devuelve `groupby()` antes de agregar | **Nueva**, ver abajo |
| `check_t4` | Límite de comparar grupos | = `check_t12` de este banco, verbatim |

### check_t2 (Semana 2) — Equivalencia de un filtro combinado
**Pregunta:** Quieres los atletas mayores de 20 años que juegan Vóleibol. ¿Cuál de estas
opciones te da EXACTAMENTE el mismo resultado que
`df_atletas[(df_atletas['Edad'] > 20) & (df_atletas['Deporte'] == 'Voleibol')]`?
a) `df_atletas[df_atletas['Edad'] > 20 and df_atletas['Deporte'] == 'Voleibol']`
b) `df_atletas[df_atletas['Edad'] > 20][df_atletas['Deporte'] == 'Voleibol']` — filtrar
   dos veces seguidas, primero por edad y después por deporte sobre el resultado
c) `df_atletas[df_atletas['Edad'] > 20 | df_atletas['Deporte'] == 'Voleibol']`
d) `df_atletas['Edad'] > 20 & df_atletas['Deporte'] == 'Voleibol']` (sin el corchete
   externo `df_atletas[...]`)
**Respuesta correcta:** b)
**Por qué:** filtrar dos veces seguidas (primero por Edad, después por Deporte sobre lo
que quedó) equivale exactamente a combinar ambas condiciones con `&`, porque en los dos
casos una fila sobrevive solo si cumple las dos condiciones a la vez. a) usa `and` de
Python, que falla sobre columnas de pandas (el mismo error de Debug 1). c) usa `|` (O)
en vez de `&` (Y), lo que cambia el significado por completo — se queda con filas que
cumplen cualquiera de las dos, no ambas. d) tiene un error de sintaxis (falta el
corchete externo y los paréntesis).
**Distractor clave:** c) — apunta al error conceptual de confundir "Y" con "O" al
combinar condiciones, no solo al error de sintaxis de `and`/`or`.

### check_t3 (Semana 2) — Qué devuelve `groupby()` antes de agregar
**Pregunta:** Después de escribir `grupos = df_atletas.groupby('Deporte')['Altura']`
(sin agregar `.mean()` ni ningún otro método todavía), ¿qué tiene guardado la variable
`grupos`?
a) Un DataFrame con la altura promedio de cada deporte, ya calculada
b) Un solo número: la altura promedio de todos los deportes juntos
c) Los datos ya separados por deporte, pero SIN ningún resumen calculado todavía —
   falta aplicar `.mean()`, `.median()`, `.std()`, etc.
d) Una lista con los nombres de los deportes, sin ningún dato numérico
**Respuesta correcta:** c)
**Por qué:** `.groupby()` por sí solo solo organiza las filas en grupos — es el paso de
"agrupar." El resumen (media, mediana, conteo...) es un paso aparte que se aplica
después, sobre cada grupo. Previene el error común de tratar `.groupby()` como si ya
calculara algo por sí mismo.

### check_intex3 (Semana 2) — Interpretación del propio hallazgo de Integración 1
**Pregunta:** En Integración 1 calculaste que la edad promedio en Baloncesto y en
Gimnasia es diferente. ¿Qué se puede concluir correctamente de ese resultado?
a) Que jugar Baloncesto hace que un atleta envejezca más rápido que la Gimnasia
b) Que existe una diferencia observada entre los dos grupos en este dataset — pero el
   dataset por sí solo no explica POR QUÉ existe esa diferencia
c) Que el cálculo debe estar mal, porque todos los deportes deberían tener la misma
   edad promedio
d) Que hay que eliminar uno de los dos deportes del dataset porque no son comparables
**Respuesta correcta:** b)
**Por qué:** mismo principio que `check_t12`/`check_t4` (Semana 2), aplicado ahora al
hallazgo propio del estudiante en vez de a un ejemplo genérico — comparar grupos
muestra *qué* es diferente, no *por qué*.
**Nota:** vive en `check_intex3`, no en la secuencia `check_tN`, porque está anclada al
resultado que el propio estudiante calculó en Integración 1, no a un ejemplo fijo del
banco.

---

## Resumen para ATLAS (puntaje)

| # | Tema | Sección que evalúa |
|---|---|---|
| t1–t3 | Qué es la estadística / tres ramas | Teoría Desbloqueada (previa a Sección A) |
| t4–t7 | Media, mediana, moda | Sección B — Reconocimiento |
| t8 | Dispersión / desviación estándar | Sección B — Reconocimiento |
| t9 | Observaciones vs. variables | Sección A — Aterrizaje |
| t10 | Valores atípicos | Sección C — Filtra el Ruido |
| t11 | Filtrado booleano | Sección C — Filtra el Ruido |
| t12 | Límite de comparar grupos | Sección D — Compara Grupos |

12 preguntas totales para Semana 1 (numeración global `check_t1`–`check_t12`, sin
cambios). **Semana 2 usa su propia numeración independiente, `check_t0`–`check_t4`
(Bloque 5 arriba) + `check_intex3`** — no continúa esta tabla; ver Bloque 5 para el
mapeo completo. Sugerido: repartir dentro del presupuesto de ~150 XP ya fijado por
sección en `WORKFORCE_CONTRACT.md` §2, sin que el total de `check_tN` desplace el peso de los
`check_exN` de código — ATLAS confirma el desglose exacto antes de fijar `_CORE_MAX`
(ver también ticket #10 y #11 en `WORKFORCE_HANDOFF.md` para el estado de Semana 2).

---

## Notas internas / pendientes

- GAUSS debe revisar cada distractor (opción incorrecta), no solo la respuesta correcta — un
  distractor mal diseñado puede enseñar una idea falsa aunque el estudiante elija bien.
- t3 y t12 son las dos preguntas de mayor prioridad de revisión: previenen los dos errores
  conceptuales que `04_GAUSS.md` marca explícitamente como riesgo para este módulo
  (clustering mal clasificado como predictivo; lectura causal prematura de `.groupby()`).
- Pendiente decidir si estas preguntas van intercaladas por sección (según la tabla de arriba,
  siguiendo el patrón teoría→ejercicio→check) o agrupadas al final de cada sección como
  checkpoint — la Sección 5 de `Teoria_Semanas1-2_Mision1_RecuperacionDeDatos.md` ya prevé la
  primera opción.

---

*Última actualización: 2026-08-03*
*Autor: SOFIA (contenido pedagógico) — validación estadística pendiente de GAUSS, puntaje
pendiente de ATLAS*

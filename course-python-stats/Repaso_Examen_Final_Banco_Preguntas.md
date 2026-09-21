# Banco de Preguntas — 3 Knowledge Checks de Repaso (rumbo al examen final)

**Estado:** borrador de contenido (markdown), no wireado a ningún notebook/autograder todavía.
**Cobertura:** todo lo enseñado hasta la fecha de este draft (2026-09-14) — Semanas 1-2
(estadística descriptiva, pandas), Semanas 3-4 (correlación), Semana 5 (causalidad), Semana 6
(regresión lineal, `nb5`). **Deliberadamente NO incluye k-means (Semana 7)** — todavía no se
enseña, por pedido explícito del usuario de no evaluar contenido no dictado.
**No cubre:** notebooks Sheets (`course-sheets-stats/`) — este banco es solo para la ruta Python.

---

## 0. Cómo está armado este banco

Tres Knowledge Checks (**KC1, KC2, KC3**), pensados como tarea de una semana cada uno, a
repartirse en las próximas 3 semanas de clase. **Cada uno es acumulativo** — no son un quiz por
tema nuevo, son repaso espaciado de todo el curso hasta ahora, con el énfasis rotando:

| | Énfasis principal | Repasa también |
|---|---|---|
| **KC1** — Fundamentos + Correlación | Semanas 1-2 (descriptiva, pandas) + Semanas 3-4 (correlación básica) | seed conceptual de causalidad |
| **KC2** — Correlación en profundidad + Causalidad | Semanas 3-4 (subgrupos, no-transitividad) + Semana 5 (confusión, correlación espuria) | fundamentos de Semanas 1-2 |
| **KC3** — Regresión + Síntesis final | Semana 6 (R², train/test, coeficientes) + integración de las 4 unidades | el más cercano a un simulacro del examen |

Cada KC tiene **24 preguntas = 8 + 8 + 8**, todas valen **5 pts** → **120 pts por KC**, mismo
orden de magnitud que el `_CORE_MAX` de los notebooks existentes:

- **A. Opción múltiple (8)** — reutiliza verbatim o casi verbatim las preguntas canónicas ya
  validadas de `Preguntas_Teoricas_Semanas1-2.md` y de `_TEORIA` en `autograder_nb3.py`/
  `autograder_nb4.py`/`autograder_nb5.py` (cada pregunta cita su fuente), más un par de
  escenarios nuevos en la misma clase de pregunta (lectura de signo/fuerza de r, variable
  confusora o causalidad inversa) para sumar variedad sin inventar un concepto nuevo. Corregidas
  localmente, sin red.
- **B. Interpretación — calificada por IA (8)** — mismo formato que `ReflexionSpec` en
  `supabase/functions/grade-reflexion/index.ts` (`question`, `grounding`, `grading_notes`,
  `max_pts`). Preguntas abiertas, 1-3 oraciones.
- **C. Código / matemática directa (8)** — un enunciado con respuesta verificable: código pandas
  de una línea limitado a `.describe()` y a filtrado booleano (`df[condición]`) — sin
  `groupby`/`.corr()`/`.corrwith()`/`sklearn`, fuera de alcance para esta sección — un cálculo
  numérico con respuesta exacta o tolerancia, o despejar una ecuación de recta `y = mx + b`
  (dado `m`, `b` y una de `x`/`y`, hallar la otra; o hallar `m`/`b` a partir de dos puntos).

### Disciplina de grounding

Ningún número en este documento fue inventado. Cada r, R², coeficiente o tamaño de dataset
citado ya está verificado en otro archivo de este repo (autograders, `grade-reflexion/index.ts`,
`build_correlaciones_espurias.py`) — se marca la fuente entre paréntesis la primera vez que
aparece un valor. Donde una pregunta necesita un número nuevo (ej. un mini-dataset para calcular
media/mediana), se usa un conjunto pequeño e inventado *a propósito* como ejercicio de cálculo
autocontenido (no una estadística real del curso) — nunca se inventa un dato que se presente
como real.

### Calibración de estrictez por grado

Reutiliza el mismo criterio que `GRADO_STRICTNESS` en `grade-reflexion/index.ts`: 3ro
(leniente, premia intento genuino aunque el razonamiento sea simple), 4to (nivel medio, espera
conectar el número/hallazgo con el concepto), 5to (estricto, exige razonamiento preciso y
evitar activamente lenguaje causal donde corresponda). Si esto se conecta a la función real,
cada pregunta de interpretación hereda ese mismo parámetro `grado` sin cambios.

### Nota de implementación futura (no hecho en este draft)

Si esto pasa a ser un notebook/autograder real: las preguntas de la sección B ya están en la
forma exacta que espera `GRADING_NOTES` en `grade-reflexion/index.ts` (agregar con ids nuevos,
namespaced por KC igual que se hizo con `nb5_*` para evitar colisión de ids genéricos — ver el
comentario 2026-09-13 en ese archivo); las de la sección A calzan tal cual en un diccionario
`_TEORIA`. La sección C no tiene equivalente todavía — necesitaría su propio `check_*` con
validación estructural (regex/AST para código) o de valor numérico con tolerancia, al estilo
`_R2_LOOKUP`/`_approx()` de `autograder_nb5.py`.

---

## KC1 — Fundamentos + Correlación

### A. Opción múltiple (8 × 5 = 40 pts)

**A1.** *(idéntica a `check_t1`, `Preguntas_Teoricas_Semanas1-2.md`)* Un periodista afirma "el
colegio X es el mejor de la ciudad" citando solo el promedio de notas de sus 5 mejores alumnos.
¿Qué le falta a esa afirmación para ser un uso correcto de la estadística?
a) Nada, un promedio siempre es suficiente para comparar
b) Considerar a todos los estudiantes, no solo una muestra elegida a conveniencia
c) Usar una gráfica en vez de un número
d) Cambiar el promedio por la moda
**Correcta: b)** — la estadística exige mirar el conjunto completo (o una muestra
representativa), no una selección que ya favorece la conclusión deseada.

**A2.** *(idéntica a `check_t3`, `Preguntas_Teoricas_Semanas1-2.md` — prioridad GAUSS)* Un
programa agrupa a 500 clientes en 4 grupos según sus hábitos de compra similares. ¿Qué rama de
la estadística describe mejor esto?
a) Predictiva, porque usa un algoritmo
b) Descriptiva, porque organiza y resume lo que ya existe en los datos
c) Prescriptiva, porque recomienda una acción
d) No es estadística, es solo programación
**Correcta: b)** — agrupar (clustering) organiza patrones existentes, no proyecta un valor
futuro. Pregunta diseñada para prevenir archivar k-means (Semana 7) como "predictivo."

**A3.** *(idéntica a `check_t4`, `Preguntas_Teoricas_Semanas1-2.md`)* En un salón de 20
estudiantes, 19 ganan S/10 de propina por una encuesta y uno gana S/500 por un error de
registro. ¿Qué le pasa a la media del grupo?
a) No cambia, la media ignora valores extremos
b) Sube mucho, porque la media se ve arrastrada por valores extremos
c) Baja mucho
d) Se vuelve imposible de calcular
**Correcta: b)**

**A4.** *(idéntica a `check_t6`, `Preguntas_Teoricas_Semanas1-2.md`)* Se tiene una lista con el
deporte favorito de 200 estudiantes (fútbol, vóley, básquet, natación...). ¿Qué medida de
tendencia central tiene sentido calcular aquí?
a) La media
b) La mediana
c) La moda
d) La desviación estándar
**Correcta: c)** — son datos categóricos, no se pueden sumar ni ordenar de forma numérica.

**A5.** *(idéntica a `check_t9`, `Preguntas_Teoricas_Semanas1-2.md`)* En una tabla de datos de
atletas olímpicos, cada fila representa un atleta y cada columna representa un dato sobre ese
atleta (edad, altura, deporte...). ¿Cómo se llama correctamente cada fila y cada columna?
a) Fila = variable, columna = observación
b) Fila = observación, columna = variable
c) Ambas son observaciones
d) Ambas son variables
**Correcta: b)**

**A6.** *(idéntica a `check_t11`, `Preguntas_Teoricas_Semanas1-2.md`)* Cuando se escribe
`df[df['edad'] > 30]`, ¿qué se está haciendo conceptualmente?
a) Borrando permanentemente a los atletas menores de 30 del archivo original
b) Haciéndole una pregunta específica a los datos: "muéstrame solo los casos que cumplen esta condición"
c) Calculando el promedio de edad
d) Ordenando el dataset de mayor a menor
**Correcta: b)**

**A7.** *(idéntica a T1, `autograder_nb3.py`)* ¿Qué resume el coeficiente de correlación (r)
entre dos variables numéricas?
a) Solo qué tan grande es el promedio de una de las variables
b) Qué tan fuerte y en qué dirección se mueven juntas dos variables
c) Cuántos valores nulos tiene el dataset
d) La forma exacta (curva) de una relación
**Correcta: b)**

**A8.** Una tienda encuentra que "temperatura promedio del día" y "ventas de abrigos" tienen
r ≈ -0.88. ¿Qué significa?
a) Relación fuerte y positiva — a más calor, más abrigos se venden
b) Relación fuerte y negativa — a más calor, tienden a venderse menos abrigos
c) Es imposible, r no puede ser negativo
d) No hay ninguna relación entre esas variables
**Correcta: b)**

### B. Interpretación — calificada por IA (8 × 5 = 40 pts)

**B1.** *Pregunta:* "El Puntaje de felicidad real de Perú es 5.697. Sin hacer ningún cálculo
todavía: en 1-2 oraciones, ¿por qué adivinar ese valor 'a ojo' usando solo el PBI de un país
puede fallar, incluso si el PBI y la felicidad están relacionados?"
*Grounding:* Puntaje real de Perú = 5.697 (usado como gancho en `Guion_Clase_Semana6_Regresion.md`).
r(PBI, Puntaje) = 0.794 (`autograder_nb3.py`, ronda "causación") — fuerte pero no perfecto.
*Qué evaluar:* crédito si reconoce que una relación fuerte-pero-imperfecta (r≠1) deja variación
sin explicar, así que adivinar a ojo ignora esa parte; sin crédito si trata al PBI como
determinante exacto de la felicidad, o si la respuesta es vacía/genérica.

**B2.** *Pregunta:* "El r entre 'PBI per cápita' y 'Apoyo social' es 0.755, y el r entre 'PBI
per cápita' y 'Generosidad' es -0.080. En 2 oraciones: ¿qué te dicen estos dos números juntos
sobre si el dinero de un país 'explica' cualquier cosa que le pase a su gente?"
*Grounding:* ambos valores reales, verificados en `grade-reflexion/index.ts` (`pbi_apoyo`=0.755,
`ronda6`=-0.080).
*Qué evaluar:* crédito si concluye que el PBI se relaciona fuerte con algunas variables pero no
con todas — el dinero no es una explicación universal; sin crédito si generaliza que el PBI
siempre se relaciona fuerte con todo.

**B3.** *Pregunta:* "Un reporte dice 'el ingreso promedio del barrio es S/4,500', pero la
mayoría de vecinos gana menos de S/2,000. En 2 oraciones, ¿cómo puede pasar esto y por qué la
mediana sería un dato más honesto aquí?"
*Grounding:* mismo patrón que el ejemplo real de ingresos en `autograder_nb1_semana1.py` (T7:
media S/3,200 vs. mediana S/1,800).
*Qué evaluar:* crédito si explica que pocos ingresos muy altos arrastran la media hacia arriba
mientras la mayoría gana menos, y que la mediana refleja mejor el caso típico; sin crédito si
concluye que uno de los dos números "está mal".

**B4.** *Pregunta:* "Dentro de Europa, 'Generosidad' y 'Puntaje' dan r=0.530. Dentro de América,
dan r=-0.211. El r general (todos los países juntos) es apenas 0.076. En 2-3 oraciones: si solo
hubieras mirado el r general, ¿qué te habrías perdido?"
*Grounding:* los tres valores son reales, Sección C de `autograder_nb4.py` (subgrupos).
*Qué evaluar:* crédito si explica que el r general esconde signos opuestos dentro de cada
subgrupo; sin crédito si concluye que el r general ya era suficiente.

**B5.** *Pregunta:* "En el dataset olímpico hay un atleta con una altura muy por encima del
resto de su equipo. Antes de decidir qué hacer con ese dato, en 1-2 oraciones: ¿por qué no
deberías simplemente borrarlo del dataset?"
*Grounding:* mismo concepto que T0 de `autograder_nb1_semana2.py` (atípico ≠ error, ej. un
atleta excepcionalmente alto real en el dataset).
*Qué evaluar:* crédito si explica que un atípico puede ser un caso real y válido que merece
investigarse antes de eliminarlo; sin crédito si afirma que los atípicos siempre deben borrarse.

**B6.** *Pregunta:* "Un artículo dice: 'Los países con más Percepción de corrupción positiva
(menos corrupción) tienen más felicidad (r=0.386), así que reducir la corrupción garantiza más
felicidad.' En 1-2 oraciones, ¿qué parte de esa frase no está respaldada por el número r=0.386
por sí solo?"
*Grounding:* r real = 0.386, descrito en `grade-reflexion/index.ts` como "débil a moderada", no
fuerte.
*Qué evaluar:* crédito completo si señala tanto el salto causal (garantiza) como que 0.386 ni
siquiera es una relación fuerte; crédito parcial si solo señala una de las dos cosas; sin
crédito si acepta la afirmación como probada.

**B7.** *Pregunta:* "Una escuela calcula el promedio de notas de este semestre, que ya terminó,
para un reporte. ¿Es esto estadística descriptiva o predictiva? Explica en 1 oración por qué."
*Qué evaluar:* crédito si identifica descriptiva (resume algo que ya ocurrió) con una razón; sin
crédito si dice predictiva sin justificar, o deja la respuesta vacía.

**B8.** *Pregunta:* "Antes de calcular ningún r, con solo mirar un scatter plot, ¿qué dos cosas
puedes empezar a estimar a simple vista? Explica brevemente por qué esas dos y no otra cosa."
*Grounding:* secuencia pedagógica del curso — visualizar antes de formalizar (`Teoria_Semanas3-4_Mision2_Correlacion.md` §1.3).
*Qué evaluar:* crédito si nombra fuerza (dispersión) y dirección (signo) como las dos cosas
visualmente estimables; sin crédito si nombra algo que r nunca muestra (ej. causalidad) como
visualmente obvio.

### C. Código / matemática directa (8 × 5 = 40 pts)

**C1.** Escribe (en una línea) el código pandas para quedarte solo con las filas de `df` donde
la columna `Peso` sea mayor a 80.
*Respuesta esperada:* `df[df['Peso'] > 80]`

**C2.** Dado este mini-dataset de propinas de 10 personas: `[10,10,10,10,10,10,10,10,10,100]`.
Calcula la media y la mediana.
*Respuesta esperada:* media = 19.0 (190/10); mediana = 10 (promedio del 5to y 6to valor
ordenado, ambos 10).

**C3.** Dado este conjunto: `[4,4,4,4,4,4]`. ¿Cuál es su desviación estándar?
*Respuesta esperada:* 0 — todos los valores son iguales, no hay dispersión.

**C4.** El dataset real de felicidad tiene 156 filas. Si ejecutas `df['Puntaje'].describe()` y
la columna no tiene valores faltantes, ¿qué número esperas ver en la fila `count`? Escribe
también el código que ejecutarías.
*Respuesta esperada:* `df['Puntaje'].describe()`; `count` = 156 (una fila por país, sin nulos).

**C5.** Con esta tabla real de Semana 3 — PBI vs Esperanza=0.835, Apoyo social vs
Esperanza=0.719, Libertad vs Corrupción=0.439 (todos verificados en `autograder_nb3.py`/
`autograder_nb4.py`) — ¿cuál par tiene la relación MÁS fuerte y cuál la MÁS débil de los tres?
*Respuesta esperada:* más fuerte = PBI vs Esperanza (0.835); más débil = Libertad vs Corrupción
(0.439).

**C6.** Si r(A,B) = 0.6 y r(B,C) = 0.6, ¿puedes concluir el valor de r(A,C) sin calcularlo?
Responde sí/no y en una frase por qué.
*Respuesta esperada:* No — la correlación no es transitiva, hay que calcularla directamente
(mismo argumento que T7 de `autograder_nb3.py`).

**C7.** Escribe el código pandas para filtrar `df` quedándote solo con los países donde
`Puntaje` sea menor a 4 (los países menos felices del dataset).
*Respuesta esperada:* `df[df['Puntaje'] < 4]`

**C8.** Una recta es y = 2x + 1. ¿Cuál es el valor de y cuando x = 4?
*Respuesta esperada:* y = 9 (2×4 + 1).

---

## KC2 — Correlación en profundidad + Causalidad

### A. Opción múltiple (8 × 5 = 40 pts)

**A1.** *(idéntica a T7, `autograder_nb3.py`)* Ya viste que tanto "PBI per cápita" como
"Esperanza de vida saludable" tienen cada una r ≈ 0.78-0.79 con "Puntaje". ¿Qué puedes concluir
sobre la correlación ENTRE esas dos variables, sin Puntaje de por medio?
a) Tiene que ser también ≈0.78, porque ambas se relacionan igual con Puntaje
b) No se puede saber su valor exacto sin calcularlo directamente — que ambas se relacionen con una tercera variable no fija su relación mutua
c) Tiene que ser 0, porque ya "usaron" su relación con Puntaje
d) Tiene que ser negativa, porque son variables distintas
**Correcta: b)**

**A3.** *(idéntica al Quiz de Cierre 2 / T9, `autograder_nb3.py`)* En una ciudad, las ventas de
helado y el número de personas que se ahogan en la playa tienen un r muy alto, cercano a 0.9,
medido mes a mes durante todo el año. ¿Cuál es la mejor explicación?
a) Comer helado le da a la gente ganas de nadar en aguas peligrosas
b) Ahogarse hace que la gente compre más helado después
c) Una tercera variable — el calor del verano — hace subir tanto las ventas de helado como la cantidad de gente que va a nadar, sin que una cause la otra directamente
d) El r no significa nada aquí porque son dos actividades sin relación
**Correcta: c)**

**A4.** *(idéntica al Quiz de Cierre 3 / T10, `autograder_nb3.py`)* En un grupo de niños de
primaria de distintas edades, el tamaño de zapato y la habilidad de lectura tienen un r ≈ 0.65 —
niños con zapatos más grandes tienden a leer mejor. ¿Qué explica mejor esta relación?
a) Tener pies más grandes ayuda al cerebro a leer mejor
b) Leer bien hace que crezcan más los pies
c) La edad es la variable de fondo: los niños mayores tienen pies más grandes Y llevan más años aprendiendo a leer — ninguna de las dos causa la otra directamente
d) Un r de 0.65 es demasiado bajo para significar algo
**Correcta: c)**

**A5.** *(idéntica al Quiz de Cierre 4 / T11, `autograder_nb3.py`)* Un estudiante prueba la
correlación entre 30 pares de variables al azar en una encuesta enorme (número de zapato
preferido, día de la semana en que nació, color favorito...) y encuentra que uno de esos 30
pares da r ≈ 0.61. ¿Qué es lo más razonable pensar?
a) Como el r es alto, encontró una relación real e importante
b) Probar muchos pares al azar aumenta la probabilidad de que al menos uno salga con un r alto solo por casualidad — conviene desconfiar de este resultado hasta confirmarlo con datos nuevos
c) r nunca puede salir alto por casualidad, siempre significa algo real
d) Hay que usar ese par sin dudar porque el número es alto
**Correcta: b)**

**A8.** El número de bomberos enviados a un incendio y el daño causado tienen correlación
positiva fuerte. ¿Significa que enviar más bomberos empeora el incendio?
a) Sí, mandar más bomberos empeora el incendio
b) No, el tamaño del incendio determina cuántos bomberos se envían
c) No hay ninguna relación real entre esas variables
d) Es imposible que estas dos variables tengan correlación
**Correcta: b)** — causalidad inversa: es el daño/tamaño del incendio el que determina cuántos
bomberos se mandan, no al revés — distinto del caso de variable confusora (helado/ahogamientos).

### B. Interpretación — (8 × 5 = 40 pts)

**B1.** *Pregunta:* "La tasa de divorcio en Maine y el consumo de margarina per cápita en EE.UU.
dieron r=0.992 entre 2000 y 2009 (dato real). ¿qué tan convincente te parece este r como evidencia de una relación real, y qué le
falta?"
*Grounding:* r real = 0.992, `build_correlaciones_espurias.py`.
*Qué evaluar:* crédito si reconoce que el número por sí solo no es evidencia de una relación
real pese a ser numéricamente muy alto, y lo atribuye a coincidencia sobre una serie corta; sin
crédito si trata 0.992 como prueba de una relación real.

**B2.** *Pregunta:* "'Asesinatos por vapor y objetos calientes' subió y bajó casi igual que la
'edad de Miss America' entre 1999 y 2009 (r=0.870, dato real). Propón una explicación de por qué
dos series sin ninguna relación lógica pueden terminar con un r tan alto."
*Grounding:* r real = 0.870, `build_correlaciones_espurias.py`.
*Qué evaluar:* crédito si propone coincidencia sobre una serie temporal corta o fluctuaciones
año a año sin relación real (aquí no hace falta nombrar un confusor específico, a diferencia de
otros ejemplos); sin crédito si inventa un mecanismo causal entre las dos.

**B3.** *Pregunta:* "Dentro de Oceanía, con solo 2 países en el dataset, cualquier r que
calcules sale cercano a ±1. ¿Es este el mismo problema que ver una correlación espuria como la
del queso y las sábanas, o es un problema distinto? Explica en 2-3 oraciones."
*Grounding:* nota explícita de T10 en `autograder_nb4.py`: "esto no tiene nada que ver con
causalidad... es un problema distinto de tamaño de muestra."
*Qué evaluar:* crédito completo si distingue explícitamente los dos (artefacto geométrico de
n=2 vs. coincidencia real sobre muchos datos reales, no un problema de tamaño de muestra);
crédito parcial si dice "distinto" sin explicar por qué; sin crédito si los trata como el mismo
problema.

**B4.** *Pregunta:* "PBI per cápita y Generosidad dieron r=-0.080 — prácticamente nulo. En 1-2
oraciones: ¿este resultado hace más o menos creíble que Generosidad y Percepción de corrupción
(r=0.327) tengan una relación real? Explica tu razonamiento."
*Grounding:* ambos valores reales, `grade-reflexion/index.ts` (`ronda6`=-0.080,
`generosidad_corrupcion`=0.327).
*Qué evaluar:* crédito si razona sobre el contraste (Generosidad casi no se relaciona con nada
más, así que una relación no trivial específicamente con corrupción resulta más notable/digna de
investigar — o alternativamente, una respuesta cautelosa de que 0.327 tampoco alcanza para
confirmar nada por sí solo, siempre que esté justificada); sin crédito si trata -0.080 y 0.327
como básicamente lo mismo.

**B5.** *Pregunta:* "Piensa en un ejemplo propio (no puede ser helado/ahogamientos,
zapato/lectura, ni ningún par de este curso) de dos variables que probablemente estén
correlacionadas sin que una cause la otra. Nombra las dos variables y la variable de fondo
(confusora) que las conecta."
*Grounding:* aplicación conceptual, sin respuesta fija — evalúa transferencia genuina del
concepto de variable confusora a un ejemplo nuevo.
*Qué evaluar:* crédito completo si el par es genuinamente nuevo, plausible, y nombra un
confusor específico y plausible; crédito parcial si el confusor es vago ("hay otro factor"); sin
crédito si reutiliza un ejemplo del curso o propone causalidad directa.

**B6.** *Pregunta:* "En el 'Duelo de Oráculos' de la clase de Semana 6, Japón tenía un PBI per
cápita cercano al de Finlandia, pero un Puntaje de felicidad más bajo. En 2 oraciones,
¿contradice esto que r(PBI, Puntaje)=0.794 sea una relación fuerte?"
*Grounding:* hecho real de `Guion_Clase_Semana6_Regresion.md` (Japón usado deliberadamente para
sembrar la pregunta "el patrón no es perfecto").
*Qué evaluar:* crédito si explica que r=0.794 describe un patrón general fuerte, no perfecto —
las excepciones individuales son esperables y no invalidan la relación; sin crédito si concluye
que la excepción refuta la correlación, o si la ignora por completo.

**B7.** *Pregunta:* "Un compañero dice: 'si r es alto, ya no hace falta pensar en si tiene
sentido la relación.' En 2-3 oraciones, usando cualquiera de los ejemplos reales de
correlaciones espurias de esta semana, explica por qué esa frase es un error."
*Grounding:* los 5 ejemplos reales de `build_correlaciones_espurias.py` (Nicolas Cage/ahogamientos
r=0.666, Miss America/asesinatos r=0.870, queso/sábanas r=0.947, ciencia/suicidios r=0.992,
margarina/divorcio r=0.992).
*Qué evaluar:* crédito si usa un ejemplo real específico (cualquiera de los 5) para argumentar
que un r alto nunca sustituye un mecanismo plausible/evidencia adicional; sin crédito si es
genérico sin referenciar un caso concreto.

**B8.** *Pregunta:* "De los 6 pares de variables del dataset de felicidad que se calcularon en
Semana 3-4, ¿cuál resultado te pareció más contraintuitivo y por qué?"
*Grounding:* los 6 r reales de las Rondas 1-6 (0.386, 0.794, 0.777, 0.780, 0.835, 0.719, 0.439,
-0.080, 0.076, 0.327 — el estudiante elige un subconjunto real de estos, según qué rondas hizo).
*Qué evaluar:* crédito si nombra un par y un valor real específicos y da una razón genuina para
la sorpresa; sin crédito si es genérico o no nombra ningún par específico.

### C. Código / matemática directa (8 × 5 = 40 pts)

**C1.** Escribe el código pandas para quedarte solo con los países de `Continente == 'Asia'` y
luego obtener el resumen estadístico (`.describe()`) de su columna `Percepción de corrupción`.
*Respuesta esperada:* `df[df['Continente']=='Asia']['Percepción de corrupción'].describe()`

**C2.** Si el r general de una relación es 0.08, pero dentro de un subgrupo es 0.53 y dentro de
otro es -0.21, ¿cuál de los tres números NO deberías usar solo para describir "la" relación
entre las dos variables? Justifica en una frase.
*Respuesta esperada:* ninguno de los tres por sí solo — el r general esconde que los subgrupos
van en direcciones distintas; hay que reportar los tres o al menos aclarar que existen.

**C3.** Con los 5 r reales de correlaciones espurias — `[0.666, 0.870, 0.947, 0.992, 0.992]` —
calcula su media.
*Respuesta esperada:* ≈0.893 (4.467 / 5).

**C4.** Una recta es y = -3x + 10. ¿Para qué valor de x es y = 1?
*Respuesta esperada:* x = 3 (1 = -3x + 10 → -3x = -9 → x = 3).

**C5.** Con r(A,B)=0.6 y r(B,C)=0.6 dados, ¿es matemáticamente posible que r(A,C) sea negativo?
Responde sí/no.
*Respuesta esperada:* Sí — la correlación no es transitiva; A y C pueden no tener relación o
tenerla negativa.

**C6.** Un dataset real tiene 156 países. Un estudiante filtra por continente y le quedan 2
filas para Oceanía. ¿Qué fracción del dataset total representa ese subgrupo?
*Respuesta esperada:* ≈1.3% (2/156 ≈ 0.0128).

**C7.** Escribe el código pandas para quedarte con las filas donde `Puntaje` sea mayor a 6 Y
`Percepción de corrupción` sea menor a 0.1 (usa `&` con paréntesis).
*Respuesta esperada:* `df[(df['Puntaje'] > 6) & (df['Percepción de corrupción'] < 0.1)]`

**C8.** De estos 3 r reales — Ronda1 (Percepción corrupción)=0.386, Ronda3
(PBI-Esperanza)=0.835, Ronda6 (PBI-Generosidad)=-0.080 — ordénalos de MÁS fuerte a MENOS fuerte
(por fuerza, sin importar el signo).
*Respuesta esperada:* 0.835 (Ronda3) > 0.386 (Ronda1) > |-0.080| (Ronda6).

---

## KC3 — Regresión + Síntesis final

### A. Opción múltiple (8 × 5 = 40 pts)

**A1.** *(idéntica a T1, `autograder_nb5.py`)* Tu modelo de regresión da R² = 0.72 en el set de
prueba. ¿Qué significa exactamente ese número?
a) El 72% de las predicciones individuales fueron exactamente correctas
b) El modelo explica (predice) alrededor del 72% de la variación real del resultado — el otro 28% queda sin explicar por estas variables
c) Hay un 72% de probabilidad de que la relación sea real y no producto del azar
d) El modelo acierta el 72% de las veces si el resultado fuera categórico (sí/no)
**Correcta: b)**

**A2.** *(idéntica a T2, `autograder_nb5.py`)* ¿Por qué el R² calculado sobre el set de prueba
(test) importa más que el R² calculado sobre el set de entrenamiento (train)?
a) El R² de prueba siempre da más alto, así que se ve mejor en el reporte
b) El de entrenamiento mide qué tan bien el modelo memorizó datos que ya vio; el de prueba mide si el modelo funciona con datos nuevos que nunca vio — eso es lo que importa en la práctica
c) El R² de prueba es más fácil de calcular en código
d) El R² de entrenamiento solo aplica a clasificación, no a regresión
**Correcta: b)**

**A3.** *(idéntica a T3, `autograder_nb5.py`)* Agregas al modelo una variable que en realidad no
tiene ninguna relación con lo que estás prediciendo. El R² de entrenamiento sube. El R² de
prueba baja. ¿Qué te dice esto?
a) La variable inútil en realidad sí ayuda a predecir, solo que no lo sabías
b) El modelo empezó a memorizar ruido específico del set de entrenamiento en vez de aprender un patrón real que se generalice — esto se llama sobreajuste (overfitting)
c) Hubo un error de cálculo
d) Hay que agregar todavía más variables para corregirlo
**Correcta: b)**

**A4.** *(idéntica a T4, `autograder_nb5.py`)* El modelo de felicidad del ejemplo guiado tenía
un R² de prueba decente (≈0.71). Pero al predecir con PBI per cápita = 10000 (el dato real más
alto es ≈1.7) dio un Puntaje de miles de puntos, sin sentido. ¿Por qué pasó esto?
a) El modelo está mal entrenado — con más datos, esa predicción sería razonable
b) El modelo solo aprendió el patrón dentro del rango de datos que vio; fuera de ese rango, la línea recta simplemente se sigue extendiendo sin ningún control real — eso es extrapolar
c) PBI per cápita nunca debería usarse como predictor
d) Un R² alto garantiza predicciones razonables para cualquier valor, incluso fuera del rango de entrenamiento
**Correcta: b)**

**A5.** *(idéntica a T5, `autograder_nb5.py`)* En el ejemplo guiado, el coeficiente de "Apoyo
social" (≈1.16) fue mayor que el de "PBI per cápita" (≈0.77). ¿Significa esto que "Apoyo social"
es la variable más importante para predecir el Puntaje?
a) Sí, siempre — el coeficiente más grande siempre indica la variable más importante
b) No necesariamente — las variables tienen escalas distintas, así que sus coeficientes no son directamente comparables sin más contexto
c) No, los coeficientes nunca sirven para comparar variables, bajo ninguna circunstancia
d) Sí, pero solo porque ambos coeficientes son positivos
**Correcta: b)**

**A6.** *(idéntica a T6, `autograder_nb3.py`)* Una relación real y fuerte, pero en forma de
curva (no una línea recta), puede dar un valor de r cercano a...
a) 1, porque `.corr()` siempre detecta cualquier patrón
b) -1, siempre
c) 0, porque `.corr()` solo mide relación lineal
d) Es imposible calcular r en ese caso
**Correcta: c)**

**A7.** *(idéntica a `check_t2`, `Preguntas_Teoricas_Semanas1-2.md`)* Un hospital usa el
historial de pacientes de los últimos 5 años para estimar cuántas camas necesitará el próximo
mes. ¿Qué rama de la estadística está usando principalmente?
a) Descriptiva
b) Predictiva
c) Prescriptiva
d) Ninguna, esto no es estadística
**Correcta: b)**

**A8.** *(idéntica a `check_intex3`, `Preguntas_Teoricas_Semanas1-2.md`)* Un estudiante calculó
que la edad promedio de los atletas de Baloncesto y la de Gimnasia son distintas. ¿Qué se puede
concluir correctamente de ese resultado?
a) Que jugar Baloncesto hace que un atleta envejezca más rápido que la Gimnasia
b) Que existe una diferencia observada entre los dos grupos en este dataset — pero el dataset por sí solo no explica POR QUÉ existe esa diferencia
c) Que el cálculo debe estar mal, porque todos los deportes deberían tener la misma edad promedio
d) Que hay que eliminar uno de los dos deportes del dataset porque no son comparables
**Correcta: b)**

### B. Interpretación — calificada por IA (8 × 5 = 40 pts)

**B1.** *Pregunta:* "En el ejemplo guiado, el coeficiente de 'PBI per cápita' fue ≈0.77 y el de
'Apoyo social' ≈1.16. En 2-3 oraciones, en lenguaje simple y sin usar 'causa' ni 'provoca': ¿qué
te dicen estos dos números sobre cómo el modelo usa cada variable para predecir el Puntaje?"
*Grounding:* valores reales del modelo guiado, `autograder_nb5.py` / `grade-reflexion/index.ts`
(`nb5_interpretacion`).
*Qué evaluar:* crédito si explica que un coeficiente positivo significa que el Puntaje predicho
sube cuando esa variable sube (manteniendo las demás fijas), sin lenguaje causal; crédito extra
si nota que el coeficiente mayor de Apoyo social no lo hace automáticamente "más importante" por
la diferencia de escalas; sin crédito si usa lenguaje causal o la respuesta es vacía/genérica.

**B2.** *Pregunta:* "Con estos test R² reales para predecir Altura — {Edad,Peso}=0.635,
{Edad,Sexo_num}=0.247, {Peso,Sexo_num}=0.643, {Edad,Peso,Sexo_num}=0.644 — en 2 oraciones: ¿qué
te dice el salto tan grande entre 0.247 y los otros tres sobre cuál variable realmente importa
para predecir la altura?"
*Grounding:* `_R2_LOOKUP` real de `autograder_nb5.py`.
*Qué evaluar:* crédito si identifica que Peso hace casi todo el trabajo (cualquier combinación
sin Peso rinde muy por debajo) y que Edad/Sexo_num agregan poco una vez que Peso está incluido;
sin crédito si no menciona a Peso específicamente o es genérico.

**B3.** *Pregunta:* "El PBI per cápita real más alto del dataset de felicidad es ≈1.7. Si le
pides al modelo predecir con PBI=10000, da un Puntaje de miles de puntos, sin sentido. En 2
oraciones: ¿este resultado absurdo significa que el modelo está mal construido? ¿Por qué sí o
por qué no?"
*Grounding:* hecho real (PBI máximo ≈1.7, demo de extrapolación de `nb5_regresion.ipynb`).
*Qué evaluar:* crédito si explica que el modelo no está necesariamente "mal" — nunca fue
entrenado en ese rango, así que extrapolar tan lejos no es una prueba justa; sin crédito si
concluye que el modelo está roto, o si ignora el problema del rango.

**B4.** *Pregunta:* "Tu modelo de regresión predice el Puntaje de felicidad a partir del PBI
per cápita con un R² de prueba decente. Un compañero concluye: 'entonces subir el PBI de un país
sube su felicidad.' En 2-3 oraciones, sin negar que el modelo funcione razonablemente bien para
predecir, ¿qué está mal en esa conclusión?"
*Grounding:* integra la advertencia de causalidad (Semana 5) con regresión (Semana 6) — mismo
encuadre no negociable documentado en `04_GAUSS.md` para Semana 6.
*Qué evaluar:* crédito si separa explícitamente "el modelo predice bien" de "esto prueba
causalidad" — un buen modelo predictivo no es prueba de un mecanismo causal; sin crédito si
acepta la conclusión causal porque el modelo "funciona".

**B5.** *Pregunta:* "Un par de variables tuyo (de tu mini-proyecto o de cualquier ronda real de
este curso) dio un r de cierta fuerza. Si construyeras un modelo de regresión con esa variable
sola, ¿esperarías un R² alto o bajo? Explica la conexión entre el r que ya calculaste y el R²
que obtendrías."
*Grounding:* conexión conceptual entre r bivariado y ajuste de un modelo de un solo predictor —
no requiere la fórmula exacta R²=r² (no enseñada explícitamente en el curso), solo el
razonamiento cualitativo.
*Qué evaluar:* crédito si razona que un r más fuerte sugiere que esa variable sola ya captura
una parte importante de la variación, así que el R² de un modelo con solo esa variable no
debería sorprender si sale también relativamente alto; sin crédito si trata r y R² como
conceptos sin ninguna relación.

**B6.** *Pregunta:* "Imagina que analizas un dataset nuevo desde cero: primero calculas
promedios y medianas, después una matriz de correlación, y finalmente un modelo de regresión. En
3-4 oraciones: ¿qué pregunta distinta responde cada uno de esos tres pasos, y por qué ninguno de
los tres, por sí solo, te permite afirmar que una variable 'causa' otra?"
*Grounding:* síntesis del arco pedagógico completo del curso (descriptiva → correlación →
regresión; la advertencia de causalidad aplica a los tres).
*Qué evaluar:* crédito completo si asigna correctamente una pregunta distinta a cada paso
(qué es típico / qué tan fuerte se mueven juntas dos variables / puedo predecir Y a partir de X)
Y menciona explícitamente que ninguno prueba causalidad; crédito parcial si los tres roles son
correctos pero falta o es vaga la advertencia de causalidad; sin crédito si confunde los pasos o
contradice la regla enseñada.

**B7.** *Pregunta:* "El R² de prueba de tu modelo bajó comparado con el de entrenamiento, pero
no de forma dramática (0.68 vs. 0.71). ¿Es esto una señal de sobreajuste grave, un
comportamiento normal y esperable, o no se puede saber? Explica en 1-2 oraciones."
*Grounding:* concepto de `autograder_nb5.py` T3 — la señal de sobreajuste es una brecha grande y
dramática, no cualquier diferencia.
*Qué evaluar:* crédito si identifica esto como una brecha pequeña y saludable, no una alarma,
contrastándolo con el caso de sobreajuste severo; sin crédito si lo llama sobreajuste grave o
afirma que train/test siempre deberían coincidir exactamente.

**B8.** *Pregunta:* "De todo lo que viste en este curso (estadística descriptiva, correlación,
causalidad, regresión), ¿cuál concepto te costó más entender y qué ejemplo específico (de
cualquier semana) finalmente te ayudó a entenderlo?"
*Grounding:* pregunta reflexiva/metacognitiva, sin un contenido único correcto — funciona como
autodiagnóstico de repaso para el examen.
*Qué evaluar:* crédito si nombra un concepto específico Y un ejemplo/momento concreto del curso
(no "todo fue difícil" genérico); sin crédito si está vacía o sin ningún ejemplo específico.

### C. Código / matemática directa (8 × 5 = 40 pts)

**C1.** Un modelo de regresión simple tiene la ecuación: `Puntaje_predicho = 0.77 × PBI_per_cápita + 3.2`.
Si un país tiene PBI_per_cápita=1.2, ¿cuál es el Puntaje predicho?
*Respuesta esperada:* ≈4.12 (0.77×1.2 + 3.2 = 0.924 + 3.2).

**C2.** Con la tabla real de R² de prueba para predecir Altura — {Edad,Peso}=0.635,
{Edad,Sexo_num}=0.247, {Peso,Sexo_num}=0.643, {Edad,Peso,Sexo_num}=0.644 — ¿qué combinación
elegirías si solo puedes usar 2 variables, y por qué es casi tan buena como usar las 3?
*Respuesta esperada:* {Peso, Sexo_num} (0.643) — casi idéntico al de las 3 variables juntas
(0.644); agregar Edad casi no mejora nada.

**C3.** Dos puntos de una recta de regresión: cuando x=0, y=3; cuando x=10, y=8. ¿Cuál es la
pendiente (coeficiente) de esa recta?
*Respuesta esperada:* 0.5 ((8-3)/(10-0)).

**C4.** Usando la recta del ejercicio anterior (pendiente 0.5, y=3 cuando x=0), ¿qué y predice
el modelo para x=20?
*Respuesta esperada:* y=13 (0.5×20+3), pero notando que x=20 está fuera del rango de
entrenamiento (0-10) — es una extrapolación.

**C5.** Escribe el código pandas para obtener el resumen estadístico (`.describe()`) de la
columna `Peso` del dataset olímpico.
*Respuesta esperada:* `df['Peso'].describe()`

**C6.** Una recta de regresión es y = -2x + 15. ¿Para qué valor de x predice el modelo y = 5?
*Respuesta esperada:* x = 5 (5 = -2x + 15 → -2x = -10 → x = 5).

**C7.** Si r(X,Y)=0.9 en una muestra, y luego calculas una regresión lineal simple de Y sobre X,
¿esperarías un R² más cercano a 0.1 o a 0.8? Justifica en una frase.
*Respuesta esperada:* más cercano a 0.8 — un r alto en valor absoluto indica un patrón lineal
fuerte, lo que se traduce en un R² alto también.

**C8.** De los R² reales de Altura — 0.247 (Edad+Sexo_num) y 0.644 (Edad+Peso+Sexo_num) —
calcula cuánto mejora el R² al agregar Peso a la combinación.
*Respuesta esperada:* mejora en 0.397 (0.644 − 0.247), ≈40 puntos porcentuales — confirma que
Peso es el predictor que realmente carga casi toda la señal.

---

## Resumen de puntajes

| | A. Opción múltiple | B. Interpretación IA | C. Código/matemática | Total |
|---|---|---|---|---|
| KC1 | 40 | 40 | 40 | 120 |
| KC2 | 40 | 40 | 40 | 120 |
| KC3 | 40 | 40 | 40 | 120 |
| **Total 3 semanas** | | | | **360** |

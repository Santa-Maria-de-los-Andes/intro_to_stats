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

- **A. Opción múltiple (8)** — corregidas localmente, sin red. Mismo formato que `_TEORIA` en
  los autograders (`q`, 4 opciones, `correct`, `why`).
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

**A1.** Una tienda usa las ventas de los últimos 3 años para estimar cuántas unidades pedirá el
próximo mes. ¿Qué rama de la estadística está usando principalmente?
a) Descriptiva
b) Predictiva
c) Prescriptiva
d) Ninguna, esto no es estadística
**Correcta: b)** — está proyectando un valor futuro a partir de patrones existentes.

**A2.** En un equipo de 15 vendedores, 14 vendieron S/200 cada uno esta semana y uno vendió
S/3,200 por una venta excepcional. ¿Qué le pasa a la media del equipo comparada con la mediana?
a) Ambas se mantienen en S/200
b) La media sube notablemente (a S/400) mientras la mediana se mantiene en S/200, reflejando mejor lo típico
c) La mediana sube más que la media
d) Es imposible calcular la media con un valor tan distinto
**Correcta: b)** — (14×200 + 3200) / 15 = 400; la mediana de 15 valores donde 14 son 200 sigue en 200.

**A3.** 200 estudiantes reportan su color favorito. ¿Qué medida de tendencia central tiene
sentido calcular?
a) La media
b) La mediana
c) La moda
d) La desviación estándar
**Correcta: c)** — son datos categóricos, no se pueden sumar ni ordenar de forma numérica.

**A4.** Dos variables dan r ≈ -0.91. ¿Qué significa?
a) Relación fuerte y positiva
b) Relación fuerte y negativa — cuando una sube, la otra tiende a bajar
c) No hay relación entre las dos variables
d) El cálculo está mal, r no puede ser tan cercano a -1
**Correcta: b)**

**A5.** "Número de mascotas" y "Puntaje de felicidad" dan r ≈ 0.02 en un dataset. ¿Qué te dice
ese número?
a) Es una relación perfecta
b) Es una relación fuerte y negativa
c) Hay poca o ninguna relación lineal entre ellas
d) Se necesitan más datos para poder calcular r
**Correcta: c)**

**A6.** La variable X tiene r=-0.85 con el resultado, y la variable Y tiene r=0.20. ¿Cuál de las
dos tiene una relación más fuerte?
a) Y, porque es positiva
b) X, porque su distancia a 0 es mayor, sin importar el signo
c) Ambas son igual de fuertes
d) No se puede comparar r de distinto signo
**Correcta: b)** — fuerza = distancia a 0; |−0.85| > |0.20|.

**A7.** Al escribir `df[df['Edad'] < 18]`, ¿qué pasa con el DataFrame original `df`?
a) Se borran permanentemente las filas que no cumplen la condición
b) No cambia — se crea una vista/subconjunto nuevo
c) Se ordena de menor a mayor
d) Se calcula el promedio de Edad
**Correcta: b)**

**A8.** En un dataset de videojuegos donde cada fila es un juego y cada columna es un dato del
juego (año, plataforma, ventas...), ¿cómo se llama correctamente cada fila y cada columna?
a) Fila = variable, columna = observación
b) Fila = observación, columna = variable
c) Ambas son observaciones
d) Ambas son variables
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

**A1.** Filtras un dataset y te quedan solo 2 países. Cualquier par de columnas que pruebes da
r≈±1.0 casi seguro. ¿Por qué no deberías confiar en ese número?
a) Porque esos países nunca deberían estar en el dataset
b) Con solo 2 puntos, una línea recta siempre pasa exactamente por ambos — el r perfecto es un artefacto del tamaño de muestra, no evidencia de una relación fuerte
c) Porque el signo de r está mal calculado con muestras chicas
d) Porque `.corr()` no acepta menos de 3 filas
**Correcta: b)** — mismo caso que la trampa de Oceanía (T10, `autograder_nb4.py`).

**A2.** Un estudiante prueba 25 pares de variables sin ninguna razón teórica y uno de ellos da
r=0.58. ¿Qué es lo más razonable pensar?
a) Como el r es alto, encontró una relación real e importante
b) Probar muchos pares al azar aumenta la probabilidad de que alguno salga alto por pura casualidad — conviene desconfiar sin confirmación adicional
c) r nunca puede salir alto por casualidad
d) Hay que usar ese par sin dudar
**Correcta: b)**

**A3.** El consumo de queso per cápita en EE.UU. y las muertes por enredarse en sábanas tienen
r=0.947 (dato real, 2000-2009, `build_correlaciones_espurias.py`). ¿Qué explica mejor esto?
a) El queso causa que la gente se enrede
b) Coincidencia estadística sin relación causal real — ninguna variable causa la otra
c) Enredarse en sábanas hace que la gente coma más queso
d) El cálculo debe estar mal porque 0.947 es demasiado alto para ser casualidad
**Correcta: b)**

**A4.** Los pueblos con más heladerías por habitante tienen más ahogamientos en playas, r alto.
¿Cuál es la variable de fondo más probable?
a) Las heladerías causan directamente los ahogamientos
b) El calor / la temporada de verano sube ambas cosas a la vez, sin que una cause la otra
c) Los ahogamientos hacen que abran más heladerías
d) No existe ninguna explicación posible
**Correcta: b)** — misma lógica que el clásico helado/ahogamientos (T9, `autograder_nb3.py`).

**A5.** Comparando con `.groupby()`, el País A tiene un promedio de esperanza de vida más alto
que el País B. ¿Qué se puede concluir correctamente?
a) El País A es "mejor" en todo, y esa es la causa de la diferencia
b) Existe una diferencia entre los grupos en este dataset — pero esto no explica por qué existe
c) No se puede concluir nada de una comparación de grupos
d) El País B debería copiar exactamente lo que hace el País A
**Correcta: b)**

**A6.** Una relación real y fuerte pero en forma de U (no una línea recta) puede dar un r
cercano a...
a) 1, porque `.corr()` siempre detecta cualquier patrón
b) -1, siempre
c) 0, porque `.corr()` solo mide relación lineal
d) Es imposible calcular r en ese caso
**Correcta: c)**

**A7.** r(Percepción de corrupción, Puntaje) = 0.386. Comparado con r(PBI, Esperanza de
vida)=0.835, ¿cómo la describirías?
a) Igual de fuerte, ambas cercanas a 1
b) Positiva, pero notablemente más débil que 0.835 — no fuerte
c) Negativa
d) Prácticamente nula, igual que r≈0
**Correcta: b)**

**A8.** Una relación con r=0.99 entre dos variables sin ninguna conexión lógica evidente (ej.
gasto en ciencia y suicidios por ahorcamiento, r=0.992 real) es...
a) Prueba suficiente de que existe una conexión real, dado lo alto del número
b) Matemáticamente una correlación muy fuerte, pero un r alto no prueba ni requiere una explicación causal real entre ellas
c) Imposible — un r tan alto no puede ser casualidad
d) Evidencia de que el dataset está mal construido
**Correcta: b)**

### B. Interpretación — calificada por IA (8 × 5 = 40 pts)

**B1.** *Pregunta:* "La tasa de divorcio en Maine y el consumo de margarina per cápita en EE.UU.
dieron r=0.992 entre 2000 y 2009 (dato real). En 2-3 oraciones, sin decir que una 'causa' la
otra: ¿qué tan convincente te parece este r como evidencia de una relación real, y qué le
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

**A1.** Un modelo da R²=0.60 en el set de prueba. ¿Qué significa?
a) El 60% de las predicciones individuales fueron exactamente correctas
b) El modelo explica ~60% de la variación real del resultado; el otro 40% queda sin explicar
c) Hay 60% de probabilidad de que la relación sea real
d) El modelo acierta el 60% de las veces si el resultado fuera categórico
**Correcta: b)**

**A2.** Un modelo tiene R² de entrenamiento = 0.95 y R² de prueba = 0.40. ¿Qué es lo más
probable que esté pasando?
a) El modelo es excelente, ambos números son buenos
b) Sobreajuste (overfitting): memorizó el set de entrenamiento pero no generaliza a datos nuevos
c) El R² de prueba está mal calculado
d) Hace falta más entrenamiento con las mismas variables
**Correcta: b)**

**A3.** Un modelo entrenado con casas de 50 a 200 m² se usa para predecir el precio de una casa
de 5,000 m². ¿Por qué es arriesgado confiar en esa predicción?
a) El modelo nunca aprendió el patrón fuera del rango que vio — está extrapolando sin ningún control real
b) 5,000 m² es un número redondo y eso confunde al modelo
c) No es arriesgado, un buen R² garantiza cualquier predicción
d) Los modelos de regresión no pueden predecir casas grandes
**Correcta: a)**

**A4.** En un modelo, el coeficiente de "Edad" (que va de 0 a 90) es 0.05, y el de "Ingresos
mensuales en miles" (que va de 0 a 20) es 0.8. ¿Significa que Ingresos es la variable "más
importante"?
a) Sí, siempre — el coeficiente más grande siempre gana
b) No necesariamente — están en escalas distintas, no son directamente comparables sin más contexto
c) No, los coeficientes nunca sirven para nada
d) Sí, pero solo porque ambos son positivos
**Correcta: b)**

**A5.** Calcular el precio promedio de las casas vendidas el año pasado es estadística ___.
Usar el tamaño de una casa nueva para predecir su precio es estadística ___.
a) predictiva / descriptiva
b) descriptiva / predictiva
c) descriptiva / descriptiva
d) prescriptiva / predictiva
**Correcta: b)**

**A6.** Agregas "signo zodiacal" como predictor de un resultado sin ninguna relación real. El
R² de entrenamiento sube ligeramente, el de prueba baja. ¿Qué pasó?
a) El signo zodiacal en realidad sí ayuda a predecir
b) Sobreajuste — el modelo memorizó ruido específico del set de entrenamiento
c) Hubo un error de cálculo
d) Hay que agregar aún más variables para corregirlo
**Correcta: b)**

**A7.** "R²=0.85 significa que el modelo acertó exactamente el 85% de sus predicciones."
¿Verdadero o falso?
a) Verdadero
b) Falso — R² mide variación explicada, no un porcentaje de aciertos exactos
**Correcta: b)**

**A8.** Quieres describir qué tan fuerte se mueven juntas dos variables SIN construir ningún
modelo de predicción. ¿Qué herramienta de las que viste en el curso usarías?
a) Un modelo de regresión lineal completo
b) El coeficiente de correlación (`.corr()`)
c) K-means
d) `train_test_split`
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

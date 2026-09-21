# Guion de Clase — Semana 7: "El Cartógrafo de Patrones"
## K-Means Clustering (introducción a Machine Learning no supervisado)

**Autoras:** SOFIA (secuencia pedagógica) + GAUSS (revisión de exactitud estadística)
**Audiencia:** 3°–5° secundaria, 15–17 años
**Duración:** ~45 min de clase magistral, seguida de `nb6_clustering.ipynb` (ya construido) para la práctica
**Requisito previo:** Semana 6 (regresión lineal) — esta clase abre contrastando directamente con ese aprendizaje

**Objetivo de la sesión:** que el estudiante pueda decir *cuándo* usaría k-means y *cómo* interpretar un
agrupamiento ya hecho (centroides, tamaños, estabilidad) — **no** que derive el algoritmo de optimización.
Esto es exposición y aplicación, no teoría (`Bimestre3_Statistics_Python_Module_Guide.md`, no-goal explícito).

---

## Antes de empezar

- **No proyectar el notebook todavía** — mismo criterio que Semana 6: el notebook repite varios de estos
  conceptos en texto, abrirlo antes le quita sorpresa a la práctica.
- Prepara el scatter plot sin colorear de Bailabilidad vs. Tempo (113,842 canciones, `alpha` bajo para que
  se vea la densidad) para proyectar en el Bloque 1 — es literalmente la misma imagen que genera
  `nb6-scatter-code`, así que puede exportarse de una corrida previa del notebook.
- Deja espacio libre al frente del salón — el Concepto 1 usa una dinámica corporal con 3 voluntarios.
- Ten lista la tabla de rangos (Bailabilidad 0–1, Tempo 30–243 BPM) para el Concepto 2, en pizarra o slide.

---

## Línea de tiempo

| Bloque | Min | Contenido |
|---|---|---|
| 1. Gancho — De "cuánto" a "qué tipo" | 8 | Contraste con Semana 6 + "¿cuántos grupos ven?" |
| 2. Concepto 1 — Cómo agrupa k-means | 8 | Centroides, asignación, recálculo — dinámica en vivo |
| 3. Concepto 2 — Por qué escalar es un no-negociable | 10 | Reveal sin escalar vs. escalado, números reales |
| 4. Concepto 3 — Las etiquetas son arbitrarias | 8 | Índice de cluster ≠ significado; clusters ≠ géneros reales |
| 5. Concepto 4 — ¿Este mapa generaliza? | 8 | train/test para un modelo sin respuesta correcta |
| 6. Cierre y transición al notebook | 3 | Tease del Reto (cambiar k) |

Si el tiempo aprieta, el Bloque 6 es el más comprimible (es tráiler, no contenido nuevo). **No comprimas
el Bloque 3** — es, según GAUSS, el error más común al usar k-means y el corazón estadístico de la clase.

---

## 1. Gancho — "De 'cuánto' a 'qué tipo'" (8 min)

Abre contrastando explícitamente con la semana anterior:

> "La semana pasada construyeron un oráculo que predice un número — cuánto vale el Puntaje de felicidad
> de un país. Ese oráculo tenía una respuesta correcta contra la cual medirse: el Puntaje real. Hoy van a
> construir algo distinto: una herramienta que agrupa cosas parecidas... sin que nadie, ni siquiera el
> algoritmo, sepa de antemano cuáles son los grupos. No hay una 'respuesta correcta' esperándolos al final."

Proyecta el scatter plot sin colorear (Bailabilidad en X, Tempo en Y — 113,842 canciones reales de
Spotify):

> "Cada punto es una canción real. Si tuvieran que separarlas en grupos de canciones 'parecidas entre
> sí', ¿cuántos grupos usarían? ¿En qué se fijarían para decidir?"

Dales 60–90 segundos en parejas o por chat — sin corregir, sin revelar un número "correcto" (no lo hay).
Pide 3–4 respuestas en voz alta y anota los números que dijeron (2, 3, 4, 5...) en la pizarra; se
retoman implícitamente en el Bloque 4 cuando vean cuántos grupos "reales" (géneros) hay de verdad.

**Actividad opcional — dibujar los grupos a mano (si el tiempo alcanza):** reparte una copia impresa
del mismo scatter plot (o deja que señalen sobre la proyección) y pide que, en parejas, tracen con
lápiz los límites de los grupos que ven — literalmente dibujar círculos u óvalos sobre la nube de
puntos, sin ningún cálculo. Guarda esos dibujos: en el Bloque 2 van a ver cómo el algoritmo traza sus
propios límites (a partir de centroides, no a ojo), y en el Bloque 3 van a descubrir que esos límites
cambian radicalmente si no escalas las variables. Es el puente visual entre "agrupar a ojo" (lo que
acaban de hacer) y "agrupar con matemática" (lo que viene) — mismo principio de "visualización antes
que formalización" que ya vivieron con el scatter plot de Semana 3.

*Por qué esta apertura funciona:* es exactamente la misma pregunta con la que abre
`nb6_clustering.ipynb` (celda `nb6-cuantos-grupos-code`) — vivida en grupo antes de que la respondan
solos, mismo patrón que ya usaron en Semana 3 y Semana 6. También conecta con usos reales que van a
reconocer sin que se los expliques todavía: esto es lo mismo que hace Spotify para armar un Discover
Weekly, lo que hace un supermercado para segmentar clientes en campañas de marketing sin que nadie les
diga de antemano "tipos de cliente", o lo que usa una app de fotos para comprimir una imagen a menos
colores agrupando píxeles parecidos — el Bloque 2 cierra retomando esto explícitamente.

---

## 2. Concepto 1 — Cómo agrupa k-means (8 min)

**Dinámica en vivo (recomendada):** pide a 3 estudiantes que se paren en puntos distintos del salón —
son los **centroides**. El resto de la clase son los **datos**: cada uno camina hacia el centroide más
cercano. Luego cada grupo de estudiantes-datos "recalcula" la posición de su centroide moviéndose hacia
el promedio de dónde están parados. Repite una vez. Esto es, literalmente, el algoritmo — sin fórmulas.

**Traduce la dinámica a los 4 pasos formales (escríbelos en la pizarra):**
1. Coloca **k** centroides al azar.
2. Cada punto se asigna al centroide **más cercano**.
3. Cada centroide se recalcula como el **promedio** de los puntos que le tocaron.
4. Repite 2–3 hasta que las asignaciones casi no cambian.

**El detalle que más importa, dilo explícitamente:** k-means **nunca** usa una etiqueta real (como el
género de la canción) para decidir los grupos — solo usa la posición de los puntos. Tú eliges **k**
(cuántos grupos quieres); el algoritmo decide **cuáles son**.

**Chequeo rápido (mano alzada):** si cambias k de 3 a 5, ¿el algoritmo encuentra "más categorías
verdaderas escondidas", o simplemente parte el espacio en más pedazos? (Respuesta: lo segundo — no hay
categorías verdaderas que "descubrir", solo una partición geométrica que tú controlas con k. Es la
semilla del Reto 1 del notebook.)

**¿Por qué k-means y no otro algoritmo de clustering?** (una frase, no lo compares en profundidad —
existen otros como clustering jerárquico o DBSCAN, pero quedan fuera del alcance de este curso):
k-means es el punto de entrada estándar a clustering porque su mecanismo se explica sin fórmulas
(como acaban de vivirlo con la dinámica de centroides), corre rápido incluso con más de cien mil
canciones, y su resultado es fácil de interpretar — cada grupo tiene un centroide que es, literalmente,
el promedio de sus miembros, no una "caja negra".

**¿Y dónde se usa esto fuera de Spotify?** Cierra el concepto retomando la promesa del Gancho —
misma técnica, contextos distintos, ninguno con etiquetas dadas de antemano:
- **Marketing:** segmentar clientes por comportamiento de compra en grupos que nadie definió de
  antemano ("compradores frecuentes de bajo ticket" vs. "compradores ocasionales de alto ticket").
- **Compresión de imágenes:** reducir una foto a k colores, agrupando píxeles de color parecido y
  reemplazando cada grupo por su centroide.
- **Documentos y noticias:** agrupar artículos o reseñas por tema sin que existan etiquetas de tema
  previas.
- **Detección de anomalías:** un punto que queda lejos de todos los centroides puede ser un caso
  atípico — una transacción rara, un sensor con lectura extraña.

---

## 3. Concepto 2 — Por qué escalar es un no-negociable (10 min)

Plantea la trampa antes de revelarla:

> "Vamos a agrupar canciones reales por Bailabilidad (0 a 1) y Tempo (30 a 243 BPM) en 3 grupos. ¿Alguien
> ve un problema con juntar estas dos columnas antes de siquiera correr el algoritmo?"

Deja la pregunta abierta ~30 segundos. Luego muestra la tabla de rangos reales:

| Variable | Rango real |
|---|---|
| Bailabilidad | 0.05 – 0.99 |
| Tempo | 30.2 – 243.4 BPM |

**Revela el resultado SIN escalar** (k=3, mismos datos que corre el notebook, `random_state=42`):

| Cluster | Bailabilidad (media) | Tempo (media) | n |
|---|---|---|---|
| 0 | 0.498 | 167.0 BPM | 22,413 |
| 1 | 0.558 | 91.2 BPM | 40,398 |
| 2 | 0.606 | 127.3 BPM | 51,031 |

> "Miren el Tempo: va de 91 a 167 entre los tres grupos — varía muchísimo. La Bailabilidad va de 0.50 a
> 0.61 — casi no se mueve. ¿Qué separó realmente a estos tres grupos?"

Deja que lo digan ellos: básicamente solo el Tempo. **Por qué pasa esto:** k-means mide distancia, y una
diferencia de 50 BPM ya vale 50, mientras que la diferencia *máxima posible* de Bailabilidad es 1. Sin
hacer nada especial, la variable de rango más grande domina casi por completo.

**Revela el resultado escalado** (`StandardScaler`, mismos datos, k=3):

| Cluster | Bailabilidad (media) | Tempo (media) | n |
|---|---|---|---|
| 0 | 0.707 (bailable) | 115.0 BPM (medio) | 51,867 |
| 1 | 0.477 (poco bailable) | 155.8 BPM (rápida) | 34,782 |
| 2 | 0.417 (poco bailable) | 93.4 BPM (lenta) | 27,193 |

> "Ahora sí: Bailabilidad y Tempo influyen las dos. Este es el error más común al usar k-means — y la
> solución es una línea de código: escalar antes de ajustar."

⚠️ **No lo llames "opcional" ni "buena práctica"** — dilo como lo que es: sin escalar, casi cualquier
resultado de k-means sobre variables de escalas distintas está dominado por la variable de mayor rango,
no por una combinación real de todas.

---

## 4. Concepto 3 — Las etiquetas de cluster son arbitrarias (8 min)

> "Al cluster 0 de arriba lo llamé 'cluster 0' porque así lo numeró scikit-learn — no porque el 0
> signifique algo. Si vuelven a correr el mismo código en otra computadora, esos mismos grupos de
> canciones pueden salir numerados distinto. Lo único con significado real es **quién quedó agrupado con
> quién**, nunca el número del índice."

**Pregunta trampa, con datos reales (misma que trae el notebook):**

> "Agrupamos por Bailabilidad y Tempo. Este dataset tiene 114 géneros reales distintos (Pop, Rock,
> Reggaetón, K-Pop, Jazz...). ¿Creen que los 3 clusters terminaron siendo, básicamente, 3 géneros
> musicales?"

Deja que voten (sí/no). Revela:

| Cluster | Género más común dentro del cluster |
|---|---|
| 0 (n=51,867) | House de Chicago — 1.9% del cluster |
| 1 (n=34,782) | Hardstyle — 2.3% del cluster |
| 2 (n=27,193) | Grindcore — 2.6% del cluster |

> "Si el género no tuviera ninguna relación con Bailabilidad/Tempo, cada género representaría al azar
> ≈1/114 ≈ 0.9% de cualquier cluster. Lo que ven aquí (2–3%) es apenas un poco más que el azar — no un
> género dominando un cluster. k-means agrupó por posición numérica, no reconstruyó géneros musicales
> reales."

**Conclusión con la que deben quedarse:** interpretar un cluster es describir qué tienen en común sus
puntos, con tus propias palabras y números — nunca inventarle un nombre "oficial" como si fuera una
categoría preexistente.

---

## 5. Concepto 4 — ¿Este mapa generaliza? (8 min)

Retoma el hilo de Semana 6 (train/test), pero adaptado: aquí no hay una respuesta correcta que calificar,
así que "generalizar" significa otra cosa.

> "En regresión, train/test les decía si el modelo memorizó o de verdad aprendió un patrón, porque había
> una respuesta correcta que comparar. Acá no hay respuesta correcta — entonces, ¿qué significaría que un
> agrupamiento 'generalice'?"

Plantea los dos usos reales (mismos que trae el notebook):
- **Recomendación:** Spotify sugiere la próxima canción del mismo cluster. Si mañana sube una canción
  nueva que el modelo nunca vio, y la asignas a un cluster con `.predict()`, ¿sus compañeras de cluster
  de verdad se le parecen?
- **Segmentación:** una discográfica decide presupuesto de marketing por "tipo de canción" usando tus
  clusters. Si vuelves a ajustar con otra muestra y los grupos se ven totalmente distintos, esa decisión
  no sirve.

**Revela el resultado real** (ajustado SOLO con el 90% de los datos — "train" — y usando `.predict()`,
nunca `.fit()` de nuevo, sobre el 10% que el modelo nunca vio — "test"):

| Cluster | Bailabilidad train | Bailabilidad test | Tempo train | Tempo test |
|---|---|---|---|---|
| 0 | 0.417 | 0.416 | 93.5 BPM | 93.2 BPM |
| 1 | 0.708 | 0.707 | 115.0 BPM | 114.7 BPM |
| 2 | 0.478 | 0.476 | 155.7 BPM | 156.0 BPM |

> "Prácticamente idénticos entre train y test. Eso es lo que significa que un agrupamiento generalice: la
> estructura no es un accidente de qué canciones cayeron en la muestra de ajuste — se sostiene en
> canciones que el modelo nunca vio."

⚠️ **Aclara explícitamente:** esto NO es "accuracy" ni "% de aciertos" — eso no existe en clustering. Es
comparar **perfiles** (promedios por cluster), no calificar predicciones individuales contra una
respuesta correcta.

---

## 6. Cierre y transición al notebook (3 min)

> "Hoy construyeron dos mapas del mismo dataset: uno sin escalar (dominado por una sola variable) y otro
> escalado (donde todo pesa). Ahora es su turno: van a repetir el proceso con sus propios predictores, van
> a probar si su mapa generaliza a canciones que el modelo nunca vio, y al final hay un reto — ¿qué pasa
> si cambian k?"

Con eso, entregas la clase al notebook (`nb6_clustering.ipynb`, "Misión 4: El Cartógrafo de Patrones"):
ejemplo guiado paso a paso, tres ejercicios calificados y un reto bonus, ya armado y listo para
compartir.

---

## Checklist de precisión estadística (GAUSS)

Para quien dicte la clase — errores fáciles de cometer al explicar esto en vivo, cada uno con su
versión correcta:

| No digas... | Di en su lugar... |
|---|---|
| "El algoritmo encontró 3 tipos de canciones" | "El algoritmo agrupó canciones parecidas — el número de grupos (k) lo elegiste tú, no lo 'descubrió' el modelo" |
| "El cluster 0 es el grupo de las bailables" (tratando el índice como fijo) | "El índice de cada cluster es arbitrario — solo el centroide y quiénes lo componen tienen significado" |
| "Como agrupamos por Bailabilidad/Tempo, los clusters son los géneros reales" | "El género más común en cualquier cluster ronda apenas 2–3%, con 114 géneros posibles — eso es casi el azar (≈0.9%), no una reconstrucción de géneros" |
| "Escalar es una buena práctica opcional" | "Sin escalar, la variable de mayor rango (aquí, Tempo) domina casi toda la distancia — es el error más común al usar k-means, no un detalle de estilo" |
| "El modelo tuvo X% de accuracy en el test" | "No hay accuracy en clustering sin etiquetas reales — lo que se compara es si los *perfiles* de cada cluster se parecen entre train y test" |
| "Subimos k hasta que los grupos de train y test coincidieran" | "Si los perfiles no coinciden, el agrupamiento no generaliza — no es algo que se arregle subiendo k a la fuerza" |

---

*Diseñado para acompañar `nb6_clustering.ipynb` ("Misión 4: El Cartógrafo de Patrones") — todos los
valores numéricos citados aquí (n=113,842 canciones tras limpieza, rangos y promedios de
Bailabilidad/Tempo, centroides sin escalar y escalados, pureza de género por cluster, perfiles
train/test) fueron recalculados directamente sobre `spotify_es.csv` con el mismo pipeline que usa el
notebook (`KMeans(n_clusters=3, random_state=42, n_init=10)`, `StandardScaler`,
`train_test_split(test_size=0.1, random_state=42)`) — no inventados para esta guía. Calculado el
2026-09-21.*

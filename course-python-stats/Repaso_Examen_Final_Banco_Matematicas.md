# Banco de Preguntas — Matemática de Base (cohorte de repaso, Semanas 7-8)

**Estado:** borrador de contenido (markdown), no wireado a ningún notebook/autograder todavía.
**Para quién:** cohorte específica de 3°-5° que reemplaza k-means (Semana 7) y el capstone
(Semana 8) por dos sesiones de repaso matemático + un examen final — ver decisión en
`WORKFORCE_HANDOFF.md`. **No aplica al resto del curso**, que sigue el plan original de
`Bimestre3_Statistics_Python_Module_Guide.md`.
**Cobertura:** solo matemática de base — decimales, media/mediana a mano, plano cartesiano,
regla de tres simple, porcentajes, y = mx + b. La revisión de conceptos estadísticos (correlación,
causalidad, regresión) sigue viviendo en `Repaso_Examen_Final_Banco_Preguntas.md` (KC1/KC2,
trabajados en clase, no como tarea — ver decisión de la sesión). Este banco es el complemento
matemático de ese banco conceptual, no un reemplazo.

---

## 0. Cómo está armado este banco

Dos bloques, uno por sesión, más una nota sobre el examen:

| Bloque | Sesión | Bloques de habilidad | Preguntas | Puntos |
|---|---|---|---|---|
| **Bloque 1 — "Los Números"** | Semana 7 (única sesión) | A. Decimales · B. Media y mediana a mano | 20 | 100 |
| **Bloque 2 — "Las Relaciones"** | Semana 8 (única sesión) | C. Plano cartesiano · D. Regla de tres · E. Porcentajes · F. y = mx + b | 40 | 200 |
| **Total** | | | **60** | **300** |

Cada pregunta vale **5 pts**, mismo valor unitario que `Repaso_Examen_Final_Banco_Preguntas.md`,
para que ambos bancos se puedan mezclar en el examen final sin normalizar puntajes.

**Dificultad:** cada pregunta está etiquetada Fácil / Medio / Difícil / Aplicado, en progresión
dentro de cada bloque de habilidad — mismo principio de "fácil → medio → difícil → bonus" que ya
usa el resto del curso.

**Problemas de enunciado (nuevo, al final de cada bloque de habilidad):** además de las preguntas
originales, cada bloque de habilidad A-F cierra con 3-4 preguntas etiquetadas **(problema de
enunciado)**. A diferencia del resto del banco, estas no dan los números ya aislados ni dicen qué
operación usar — describen relaciones en palabras ("es un tercio de", "es la mitad del promedio
de", "sube en la misma proporción que baja el otro") y el estudiante tiene que traducir esa
relación a una expresión matemática antes de poder calcular. Buscan practicar exactamente la
habilidad que falta cuando un ejercicio ya viene "pre-armado": leer un enunciado y decidir solo/a
qué cuenta corresponde.

**Uso recomendado:** no todas las preguntas de un bloque tienen que usarse en la sesión en vivo —
este banco es una reserva de la que se sacan los ejemplos guiados, la práctica en clase, y
después una selección para la Sección D ("matemática directa") del examen final, evitando que el
examen repita ítem por ítem lo ya practicado en clase.

### Disciplina de grounding (misma regla que el banco conceptual)

Todo número marcado **(real)** ya está verificado en otro archivo del repo y se cita la fuente.
Todo número marcado **(práctica)** es un conjunto pequeño inventado a propósito como ejercicio de
cálculo autocontenido — nunca se presenta como un dato real del curso. Donde un ejercicio adapta
un valor real de forma simplificada (ej. tratar un coeficiente de regresión como si la relación
fuera perfectamente proporcional), se marca explícitamente para no enseñar una idea estadística
incorrecta.

### Nota sobre negativos

Por decisión de diseño, los números negativos **no tienen bloque propio** — están distribuidos
dentro de los otros seis bloques. Cada pregunta que incluye un valor negativo lleva la etiqueta
**(negativo)** junto a su dificultad, para poder auditar la cobertura sin releer todo el banco.

---

## BLOQUE 1 — Semana 7: "Los Números"

### A. Decimales — suma y multiplicación (10 × 5 = 50 pts)

**A1.** *(Fácil, real)* Perú tiene un Puntaje de felicidad real de **5.697**
(`Guion_Clase_Semana6_Regresion.md`). Si a ese puntaje le sumas 0.303, ¿qué número obtienes?
*Respuesta:* 5.697 + 0.303 = **6.000**

**A2.** *(Fácil, real, negativo)* El r real entre PBI per cápita y Generosidad es **-0.080**
(`grade-reflexion/index.ts`). El r real entre Libertad y Percepción de corrupción es **0.439**.
Súmalos.
*Respuesta:* -0.080 + 0.439 = **0.359**

**A3.** *(Medio, real)* Tres r reales del curso: 0.386 (Percepción de corrupción), 0.794
(PBI-Puntaje), 0.439 (Libertad-Corrupción). Súmalos.
*Respuesta:* 0.386 + 0.794 + 0.439 = **1.619**

**A4.** *(Medio, real)* El coeficiente real de "Apoyo social" en el modelo de la Semana 6 es
**1.16** (`autograder_nb5.py`). Multiplícalo × 4.
*Respuesta:* 1.16 × 4 = **4.64**

**A5.** *(Difícil, real, negativo)* El r real entre PBI y Generosidad es **-0.080**.
Multiplícalo por -5
*Respuesta:* -0.080 × -5 = **0.400** — positivo (negativo × negativo = positivo).

**A6.** *(Aplicado, real)* El coeficiente de PBI en el modelo real de la Semana 6 es 0.77 y el
intercepto es 3.2 (`autograder_nb5.py`). Multiplica 0.77 × 1.5 y luego suma 3.2.
*Respuesta:* 0.77 × 1.5 = 1.155; 1.155 + 3.2 = **4.355** *(este ejercicio anticipa y = mx + b del
Bloque 2 — mismo cálculo, sin nombrarlo todavía).*

**A7.** *(Medio, práctica, problema de enunciado)* Un estudiante mide tres coeficientes en tres
modelos distintos. El segundo coeficiente es el triple del primero. El tercer coeficiente es la
suma de los dos anteriores. Si el primer coeficiente es 0.15, ¿cuál es el tercer coeficiente?
*Respuesta:* segundo = 0.15 × 3 = 0.45; tercero = 0.15 + 0.45 = **0.60**

**A8.** *(Medio, práctica, negativo, problema de enunciado)* La diferencia entre dos temperaturas
es de 4.5 grados. La temperatura más baja registrada es -3.2. ¿Cuál es la temperatura más alta?
*Respuesta:* más alta = -3.2 + 4.5 = **1.3**

**A9.** *(Difícil, real, problema de enunciado — la relación es inventada para practicar)* El r
real entre Libertad y Percepción de corrupción es 0.439 (`grade-reflexion/index.ts`). Otro
coeficiente hipotético es el doble de ese r, menos 0.128. ¿Cuál es el valor de ese coeficiente?
*Respuesta:* 0.439 × 2 = 0.878; 0.878 − 0.128 = **0.750**

**A10.** *(Aplicado, real, problema de enunciado — hipotético, no es el intercepto real del
modelo)* Un intercepto hipotético es la mitad de la suma de dos coeficientes reales de la Semana
6: 0.77 y 1.16 (`autograder_nb5.py`). ¿Cuánto vale ese intercepto?
*Respuesta:* (0.77 + 1.16) / 2 = 1.93 / 2 = **0.965**

---

### B. Media y mediana a mano (10 × 5 = 50 pts)

**B1.** *(Fácil, práctica, inspirado en un caso real)* El curso ya vio un caso real donde el
ingreso promedio de un barrio era S/3,200 pero la mediana era S/1,800
(`autograder_nb1_semana1.py`, T7). Con este conjunto de práctica que sigue el mismo patrón (no es
el dato real, solo se inspira en él): `[1700, 1800, 1900, 1750, 8000]` — calcula la media.
*Respuesta:* (1700+1800+1900+1750+8000) / 5 = 15150 / 5 = **3030**

**B2.** *(Fácil, práctica, mismo conjunto)* Con el mismo conjunto `[1700, 1800, 1900, 1750,
8000]`, ordénalo y halla la mediana.
*Respuesta:* ordenado: 1700, 1750, **1800**, 1900, 8000 → mediana = **1800**

**B3.** *(Medio, práctica, negativo)* Temperaturas registradas en 5 días (conjunto inventado
para practicar): `[-2, 3, 5, -1, 0]`. Calcula la media.
*Respuesta:* (-2+3+5-1+0) / 5 = 5 / 5 = **1.0**

**B4.** *(Medio, práctica, negativo, mismo conjunto)* Con el mismo conjunto `[-2, 3, 5, -1, 0]`,
ordénalo y halla la mediana.
*Respuesta:* ordenado: **-2, -1, 0, 3, 5** → mediana = **0**

**B5.** *(Difícil, real, reutiliza KC2-C3)* Los 5 r reales de correlaciones espurias:
`[0.666, 0.870, 0.947, 0.992, 0.992]` (`build_correlaciones_espurias.py`,
`Repaso_Examen_Final_Banco_Preguntas.md` KC2-C3). Calcula su media.
*Respuesta:* suma = 4.467; media = 4.467 / 5 = **≈0.893** *(mismo resultado que KC2-C3 — este
ítem es la versión "muéstrame el procedimiento a mano" de esa pregunta)*

**B6.** *(Aplicado, real, reutiliza KC3-C2/C8)* 4 R² reales para predecir Altura
(`autograder_nb5.py`): {Edad,Peso}=0.635, {Edad,Sexo_num}=0.247, {Peso,Sexo_num}=0.643,
{Edad,Peso,Sexo_num}=0.644. Calcula la media y la mediana de estos 4 valores. ¿Cuál es mayor?
*Respuesta:* media = (0.635+0.247+0.643+0.644)/4 = 2.169/4 = **≈0.542**; ordenado
0.247,0.635,0.643,0.644 → mediana = (0.635+0.643)/2 = **0.639**. La mediana es mayor — el valor
bajo (0.247) arrastra la media hacia abajo, la mediana no.

**B7.** *(Medio, práctica, problema de enunciado)* Un profesor registra las calificaciones de 5
estudiantes. El primero sacó 12. El segundo sacó 3 puntos más que el primero. El tercero sacó la
mitad del segundo. El cuarto sacó lo mismo que el primero. El quinto sacó 2 puntos menos que el
tercero. ¿Cuál es el promedio de los cinco estudiantes?
*Respuesta:* 12, 15, 7.5, 12, 5.5 → suma = 52; media = 52 / 5 = **10.4**

**B8.** *(Difícil, práctica, negativo, problema de enunciado)* Se registran 5 variaciones diarias
de temperatura respecto al promedio anual. La primera es -3. La segunda es el doble de la
primera. La tercera es 0. La cuarta es la mitad del valor absoluto de la segunda. La quinta es 1
más que la primera. Ordena los cinco valores y halla la mediana.
*Respuesta:* -3, -6, 0, 3, -2 → ordenado: -6, -3, **-2**, 0, 3 → mediana = **-2**

**B9.** *(Difícil, real, problema de enunciado — el segundo y tercer valor son inventados para
practicar, no son R² reales de otros modelos)* El R² real del modelo {Edad, Peso} para predecir
Altura es 0.635 (`autograder_nb5.py`). Un segundo modelo tiene un R² que es un tercio del
anterior. Un tercer modelo tiene un R² que es la mitad del promedio de los dos anteriores. ¿Cuál
es el promedio de los tres R²?
*Respuesta:* segundo = 0.635/3 ≈ 0.2117; promedio(1,2) = (0.635+0.2117)/2 ≈ 0.4233; tercero =
0.4233/2 ≈ 0.2117; promedio de los tres = (0.635+0.2117+0.2117)/3 ≈ **0.353**

**B10.** *(Aplicado, práctica, problema de enunciado)* Cuatro estudiantes tienen 20, 21, 22 y 23
años. Un quinto estudiante tiene una edad que es el triple del promedio de los otros cuatro.
Calcula la media y la mediana de las cinco edades. ¿Cuál es mayor, y por qué?
*Respuesta:* promedio de los 4 = 21.5; quinto = 3 × 21.5 = 64.5. Conjunto: 20, 21, 22, 23, 64.5 →
media = 150.5/5 = **30.1**; ordenado → mediana = **22**. La media es mucho mayor — el valor atípico
(64.5) la arrastra hacia arriba; la mediana no se ve afectada.

---

## BLOQUE 2 — Semana 8: "Las Relaciones"

### C. Plano cartesiano — ubicar y leer puntos (9 × 5 = 45 pts)

**C1.** *(Fácil)* ¿En qué cuadrante está el punto (3, 5)? ¿Y el punto (-3, 5)?
*Respuesta:* (3, 5) → Cuadrante I; (-3, 5) → Cuadrante II

**C2.** *(Fácil, negativo)* Ubica el punto (-4, -2). ¿En qué cuadrante cae?
*Respuesta:* Cuadrante III

**C3.** *(Medio, negativo)* Un punto tiene x=2 y y=-6. Escríbelo como par ordenado y di en qué
cuadrante cae.
*Respuesta:* (2, -6) → Cuadrante IV

**C4.** *(Medio, aplicado, real)* En el gráfico de dispersión real de la Semana 3-4 (PBI vs.
Puntaje de felicidad), cada punto es un país. Si un punto está en la esquina superior derecha del
gráfico, ¿qué significa sobre ese país en las dos variables?
*Respuesta:* tiene PBI alto **y** Puntaje alto — ambos valores altos para ese país.

**C5.** *(Aplicado, sin respuesta fija — usar el artefacto real del estudiante)* Abre tu propio
gráfico de dispersión de la Semana 3-4. Elige un país/punto y escribe sus coordenadas
aproximadas (x, y). ¿Qué representa cada coordenada?
*Nota para el profesor:* esta pregunta no tiene un valor "correcto" único — se revisa contra el
gráfico real que cada estudiante ya construyó. No se puede resolver solo con este banco; es
deliberadamente experiencial.

**C6.** *(Medio, práctica, problema de enunciado)* Un punto tiene una coordenada x que es 3
menos que su coordenada y. Si la coordenada y es 5, ¿cuáles son las coordenadas del punto y en
qué cuadrante está?
*Respuesta:* x = 5 − 3 = 2 → punto (2, 5) → **Cuadrante I**

**C7.** *(Medio, práctica, negativo, problema de enunciado)* Un punto está ubicado de manera que
su coordenada x es el doble de su coordenada y, y su coordenada y es -3. ¿Cuáles son sus
coordenadas? ¿En qué cuadrante cae?
*Respuesta:* x = 2 × (-3) = -6 → punto (-6, -3) → **Cuadrante III**

**C8.** *(Aplicado, real, problema de enunciado)* En el gráfico de dispersión real de la Semana
3-4 (PBI vs. Puntaje de felicidad), el país A tiene un PBI que es el doble del de un país B, y
ambos países tienen el mismo Puntaje de felicidad. Comparando sus posiciones en el gráfico, ¿cómo
se ven una respecto a la otra?
*Respuesta:* el país A está el doble de lejos del eje y (más a la derecha, mayor x = PBI), pero a
la **misma altura** que B (mismo y = Puntaje), porque comparten la coordenada vertical.

**C9.** *(Difícil, práctica, negativo, problema de enunciado)* Un punto está tres unidades a la
izquierda del origen en el eje x, y cinco unidades hacia abajo en el eje y. Escribe sus
coordenadas y di en qué cuadrante está.
*Respuesta:* (-3, -5) → **Cuadrante III**

---

### D. Regla de tres simple — directa e inversa (10 × 5 = 50 pts)

**D1.** *(Fácil, práctica, directa)* Si 4 kg de papas cuestan S/12, ¿cuánto cuestan 7 kg?
*Respuesta:* 12/4 = 3 por kg; 7 × 3 = **S/21**

**D2.** *(Fácil, práctica, directa)* Un carro recorre 180 km con 15 litros de gasolina. ¿Cuántos
km recorre con 20 litros, a la misma proporción?
*Respuesta:* 180/15 = 12 km/litro; 20 × 12 = **240 km**

**D3.** *(Medio, real, simplificado — marcado)* El coeficiente real de "Apoyo social" en el
modelo de la Semana 6 es 1.16 (`autograder_nb5.py`) — es decir, por cada punto que sube el Apoyo
social, el Puntaje sube 1.16. *(Simplificación para practicar: en el modelo real hay más
variables de por medio, pero el coeficiente ya es una tasa que se puede escalar con regla de
tres.)* Si el Apoyo social sube 3 puntos, ¿cuánto sube el Puntaje según esta proporción?
*Respuesta:* 1.16 × 3 = **3.48**

**D4.** *(Medio, práctica, inversa)* Si 3 obreros terminan un trabajo en 8 días, ¿cuántos días
tardarían 6 obreros trabajando al mismo ritmo?
*Respuesta:* 3 × 8 = 24 obrero-días; 24 / 6 = **4 días** *(más obreros, menos días — proporción
inversa)*

**D5.** *(Medio, práctica, inversa, tie-in conceptual)* Dos variables se relacionan de forma
inversa — mientras más sube X, más baja Y, en la misma proporción (como una correlación negativa
fuerte). Si 2 unidades de X producen 30 unidades de Y, ¿cuántas unidades de Y produce X=5, con la
misma relación inversa?
*Respuesta:* 2 × 30 = 60; 60 / 5 = **12**

**D6.** *(Difícil, real)* El modelo real de la Semana 6 predice que por cada 1 unidad que sube el
PBI per cápita, el Puntaje sube 0.77 (`autograder_nb5.py`). Con regla de tres, ¿cuánto sube el
Puntaje si el PBI sube 2.5 unidades?
*Respuesta:* 0.77 × 2.5 = **1.925**

**D7.** *(Medio, práctica, problema de enunciado)* Una impresora imprime páginas a un ritmo
constante: 45 páginas en 5 minutos. ¿Cuántas páginas imprime en 12 minutos?
*Respuesta:* 45/5 = 9 páginas/min; 12 × 9 = **108 páginas** *(proporción directa — a más tiempo,
más páginas)*

**D8.** *(Medio, práctica, problema de enunciado)* Si 8 pintores pintan una casa en 6 días,
trabajando todos al mismo ritmo, ¿cuántos días tardarían 4 pintores?
*Respuesta:* 8 × 6 = 48 obrero-días; 48 / 4 = **12 días** *(proporción inversa — menos pintores,
más días)*

**D9.** *(Difícil, real, problema de enunciado)* El coeficiente real de PBI per cápita en el
modelo de la Semana 6 es 0.77 (`autograder_nb5.py`): a mayor PBI, mayor Puntaje predicho, en
proporción constante. Si el PBI de un país es 1.8 unidades mayor que el de otro con el que se
compara, ¿cuánto mayor es su Puntaje predicho, según esta proporción?
*Respuesta:* 0.77 × 1.8 = **1.386**

**D10.** *(Difícil, práctica, negativo, problema de enunciado)* Dos variables se relacionan de
forma inversa: mientras una sube, la otra baja en la misma proporción. Cuando la primera vale 4,
la segunda vale -18. ¿Cuánto vale la segunda cuando la primera vale -6?
*Respuesta:* producto constante = 4 × (-18) = -72; segunda = -72 / (-6) = **12**

---

### E. Porcentajes — aumento y disminución (9 × 5 = 45 pts)

**E1.** *(Fácil, real)* El dataset real de felicidad tiene 156 países
(`Repaso_Examen_Final_Banco_Preguntas.md`, KC1-C4). Si el 10% de ellos tiene un Puntaje mayor a
7, ¿aproximadamente cuántos países son?
*Respuesta:* 10% de 156 = **≈16 países**

**E2.** *(Fácil, real, reutiliza KC2-C6)* El subgrupo real de Oceanía tiene 2 de los 156 países
del dataset (KC2-C6, donde ya calculaste esto como fracción ≈1.3%). Exprésalo ahora como
porcentaje, mostrando el cálculo.
*Respuesta:* 2/156 = 0.0128... → **≈1.3%** (mismo resultado que KC2-C6)

**E3.** *(Medio, práctica, aumento)* Un país tenía un Puntaje de 5.0 el año pasado y subió 8%
este año. ¿Cuál es el nuevo puntaje?
*Respuesta:* 5.0 × 1.08 = **5.4**

**E4.** *(Medio, práctica, disminución)* El mismo país, en otro escenario, bajó su Puntaje en 8%
desde 5.0. ¿Cuál sería el nuevo puntaje, y cuánto bajó en valor absoluto?
*Respuesta:* 5.0 × 0.92 = **4.6**; bajó **0.4 puntos**

**E5.** *(Difícil, real, aplicado)* El R² de prueba real de un modelo bajó de 0.71 a 0.68
(`Repaso_Examen_Final_Banco_Preguntas.md`, KC3-B7). ¿Qué porcentaje de disminución representa
este cambio, respecto al valor original de 0.71?
*Respuesta:* (0.71 − 0.68) / 0.71 = 0.03 / 0.71 ≈ **4.2% de disminución**

**E6.** *(Medio, práctica, problema de enunciado)* En una encuesta, cierto porcentaje de los
participantes contestó "sí" y el resto contestó "no". 51 personas contestaron "sí", y eso
representa el 15% del total de participantes. ¿Cuántas personas participaron en total?
*Respuesta:* 51 = 0.15 × total → total = 51 / 0.15 = **340 personas**

**E7.** *(Medio, real, problema de enunciado)* El dataset real de felicidad tiene 156 países
(`Repaso_Examen_Final_Banco_Preguntas.md`, KC1-C4). Un subconjunto de esos países tiene 39
países. ¿Qué porcentaje del total representa ese subconjunto?
*Respuesta:* 39 / 156 = 0.25 → **25%**

**E8.** *(Difícil, práctica, problema de enunciado)* El precio de un producto subió cierto
porcentaje y pasó de S/50 a S/56.50. ¿Cuál fue el porcentaje de aumento?
*Respuesta:* (56.50 − 50) / 50 = 6.5 / 50 = 0.13 → **13% de aumento**

**E9.** *(Aplicado, real, problema de enunciado)* El R² de prueba de un modelo bajó un 15%
respecto a su valor original. Si el nuevo valor es 0.578, ¿cuál era el valor original?
*Respuesta:* nuevo = original × (1 − 0.15) → 0.578 = original × 0.85 → original = 0.578 / 0.85 =
**0.68**

---

### F. y = mx + b (12 × 5 = 60 pts)

**F1.** *(Fácil, reutiliza KC1-C8)* En la recta y = 2x + 1, ¿cuál es el valor de y cuando x = 4?
*Respuesta:* y = 2(4) + 1 = **9**

**F2.** *(Fácil, real, negativo, reutiliza la recta de KC2-C4)* En la recta y = -3x + 10, ¿cuál
es el valor de y cuando x = 2?
*Respuesta:* y = -3(2) + 10 = -6 + 10 = **4**

**F3.** *(Medio, negativo, reutiliza KC2-C4)* Usando la misma recta y = -3x + 10, ¿para qué valor
de x es y = 1?
*Respuesta:* 1 = -3x + 10 → -3x = -9 → x = **3**

**F4.** *(Medio, real)* El modelo real de la Semana 6 es Puntaje_predicho = 0.77 × PBI + 3.2
(`autograder_nb5.py`, idéntico a KC1-C1/KC3-C1). Si un país tiene PBI = 0.9, ¿cuál es el Puntaje
predicho?
*Respuesta:* 0.77 × 0.9 = 0.693; 0.693 + 3.2 = **≈3.893**

**F5.** *(Medio, reutiliza KC3-C3)* Dos puntos de una recta: cuando x=0, y=3; cuando x=10, y=8.
Halla la pendiente.
*Respuesta:* (8−3) / (10−0) = 5/10 = **0.5**

**F6.** *(Difícil, negativo)* Dos puntos de una recta: cuando x=0, y=12; cuando x=4, y=4. Halla
la pendiente. ¿Qué significa que sea negativa?
*Respuesta:* (4−12) / (4−0) = -8/4 = **-2**. Significa que y disminuye cuando x aumenta —
relación inversa.

**F7.** *(Difícil, negativo, reutiliza KC3-C6)* Una recta es y = -2x + 15. ¿Para qué valor de x
predice el modelo y = 5?
*Respuesta:* 5 = -2x + 15 → -2x = -10 → x = **5**

**F8.** *(Aplicado, real, simplificado — marcado)* El coeficiente real de "Apoyo social" es 1.16.
*(Simplificación para practicar: se usa un intercepto de 2.0, no el intercepto real de múltiples
variables, que no es un solo número limpio.)* Escribe la ecuación y = mx + b con estos valores, y
calcula y cuando Apoyo social (x) = 1.5.
*Respuesta:* y = 1.16x + 2.0; y = 1.16(1.5) + 2.0 = 1.74 + 2.0 = **3.74**

**F9.** *(Medio, práctica, problema de enunciado)* En una recta, cuando x vale 0, y vale 4.
Cuando x aumenta en 5 unidades, y aumenta en 15 unidades. Escribe la ecuación de la recta y
calcula y cuando x = 8.
*Respuesta:* pendiente = 15/5 = 3; b = 4 (valor de y cuando x=0) → y = 3x + 4; y = 3(8) + 4 =
**28**

**F10.** *(Medio, práctica, negativo, problema de enunciado)* En una recta, el intercepto es el
triple de la pendiente. Si la pendiente es -2, escribe la ecuación de la recta y calcula y cuando
x = 3.
*Respuesta:* b = 3 × (-2) = -6 → y = -2x - 6; y = -2(3) - 6 = **-12**

**F11.** *(Difícil, real, problema de enunciado — hipotético, no es un modelo real)* El
coeficiente real de "Apoyo social" es 1.16 y el intercepto real es 3.2 (Semana 6,
`autograder_nb5.py`). Un modelo hipotético tiene una pendiente que es la mitad de esa, y el mismo
intercepto. Escribe su ecuación y calcula y cuando Apoyo social (x) = 4.
*Respuesta:* pendiente = 1.16/2 = 0.58 → y = 0.58x + 3.2; y = 0.58(4) + 3.2 = 2.32 + 3.2 =
**5.52**

**F12.** *(Aplicado, práctica, problema de enunciado)* Una recta pasa por el punto (2, 7) y su
pendiente es el doble de 1.5. Halla su ecuación y calcula y cuando x = 10.
*Respuesta:* pendiente = 1.5 × 2 = 3; usando el punto: 7 = 3(2) + b → b = 1 → y = 3x + 1;
y = 3(10) + 1 = **31**

---

## Resumen de puntajes

| Bloque | Habilidad | Preguntas | Puntos |
|---|---|---|---|
| 1 | A. Decimales | 10 | 50 |
| 1 | B. Media y mediana a mano | 10 | 50 |
| 2 | C. Plano cartesiano | 9 | 45 |
| 2 | D. Regla de tres simple | 10 | 50 |
| 2 | E. Porcentajes | 9 | 45 |
| 2 | F. y = mx + b | 12 | 60 |
| **Total** | | **60** | **300** |

**Cobertura de negativos (auditable):** A2, A5, A8, B3, B4, B8, C2, C3, C7, C9, D10, F2, F3, F6,
F7, F10 — 16 de 60 preguntas, repartidas en 5 de los 6 bloques de habilidad (todas menos E, donde
el aumento/disminución ya transmite la idea de dirección sin necesitar un valor negativo
explícito).

**Cobertura de "problemas de enunciado" (auditable):** A7-A10, B7-B10, C6-C9, D7-D10, E6-E9,
F9-F12 — 24 de 60 preguntas, 4 en cada uno de los seis bloques de habilidad.

---

## Próximo paso sugerido (no hecho en este draft)

Seleccionar de aquí la Sección D del examen final (matemática directa) sin repetir ítem por ítem
lo ya usado en clase — por ejemplo, usar A1/A4/B1/B2 en la Sesión 1 en vivo y reservar A3/A6/B5/
B6 para el examen; mismo criterio para el Bloque 2. Pendiente de validación por ATLAS (aritmética/
puntaje) y GAUSS (que ninguna simplificación —D3, F8— se lea como un hecho estadístico real en
vez de un ejercicio de práctica).

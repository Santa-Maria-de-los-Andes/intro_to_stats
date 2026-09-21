"""
Autograder — Bimestre 3, Misión 4: El Cartógrafo de Patrones — SEMANA 7
K-MEANS CLUSTERING — Spotify Tracks Dataset (spotify_es.csv), 114,000
pistas x 114 géneros reales.

ATLAS build 2026-09-19, a partir del beat sheet detallado provisto
directamente por el usuario para "nb6" (Semana 7, k-means). Continúa la
numeración global de check_ex/check_t/check_reto de Misión 3 (nb5) — no,
espera: WORKFORCE_CONTRACT.md §2 solo exige numeración global *dentro* de
una misión multi-notebook (ej. nb1_semana1->nb1_semana2, nb3->nb4). La
Misión 4 (Semana 7) es una sola sesión, igual que la Misión 3 (Semana 6)
lo fue — así que check_ex/check_t/check_reto empiezan frescos en 1, mismo
patrón que nb5 frente a nb3/nb4.

Cubre: check_cuantos_grupos, check_como_agrupa (registro, sin IA),
check_cluster_es_genero (🧩 completa, estructural), check_t1-t5,
check_ex1, check_mini_a, check_reflexion_ex2,
check_reflexion_generalizacion, check_reto1 (bonus), check_reflexion_final,
check_mini_b, resumen()

**Revisión 2026-09-19 (mismo día, el usuario proveyó el dataset real)**:
la primera versión de este notebook usaba `vgsales_es.csv` (ventas de
videojuegos) como sustituto, porque el beat sheet original pedía
danceability/tempo (un dataset de audio estilo Spotify) y no existía
ningún CSV de ese tipo en el repo todavía. El usuario agregó
`course-python-stats/Week 7/spotify.csv` (el "Spotify Tracks Dataset" de
Kaggle, 114,000 filas x 21 columnas, 114 géneros x 1000 pistas c/u) — este
archivo se reconstruyó alrededor de ese dataset real. `translate_to_spanish.py`
(mismo folder) traduce encabezados y los 114 géneros al español,
produciendo `spotify_es.csv` (la razón completa de nombre-por-nombre para
cada género está en el docstring de ese script). Ver `WORKFORCE_HANDOFF.md`
para la entrada de Done log que documenta esta sustitución explícitamente
(no una edición silenciosa del historial).

Dataset: `spotify_es.csv`. Limpieza guiada (no escrita por el estudiante):
1 fila sin `Artistas`/`Nombre_Cancion` + 157 filas con `Tempo` = 0 (fallo
de detección de tempo, no una canción real de 0 BPM) se descartan antes de
cualquier ejercicio — quedan 113,842 filas. `Bailabilidad` (0 a 1) y
`Tempo` (≈30-243 BPM, promedio ≈122) para el ejemplo guiado, el 🧩 de
géneros y el Ejercicio 1; `Energia` (0 a 1) se muestra en una celda de
demostración (`nb6-demo-energia-*`, sin calificar) y puede opcionalmente
incluirse entre los predictores propios del Ejercicio 1. `Genero` (114
valores reales, nunca usado como predictor) alimenta el
cruce cluster×género que sostiene `check_cluster_es_genero` — evita por
completo el problema de one-hot-encoding que recortó el menú de nb5 (114
categorías, ni se intenta codificar, solo se usa para comparar después de
agrupar).

**Decisión de alcance real, documentada aquí y en `WORKFORCE_CONTRACT.md`
§5 (no una desviación silenciosa)**: el temario técnico committeado
listaba solo `sklearn.cluster.KMeans (.fit_predict())`, sin
`sklearn.preprocessing.StandardScaler`. Escalar antes de ajustar es un
no-negociable estadístico para k-means (04_GAUSS.md, fila Semana 7: "needs
feature scaling before .fit_predict()") — sin él, el ejemplo guiado ni
siquiera puede *mostrar* el problema que Concepto 2 explica. Se agregó
`StandardScaler` al temario técnico (§5) como una ampliación de alcance
reconocida, aprobada por el pedido explícito del usuario de que el
escalado fuera un "GAUSS-flagged non-negotiable" del beat sheet.

**Validación empírica del dataset, ATLAS (2026-09-19)**, antes de fijar
ningún valor en este archivo — igual disciplina que nb5's R²:
  - K-means SIN escalar sobre {Bailabilidad, Tempo} (k=3, random_state=42,
    n_init=10, sobre las 113,842 filas limpias): los 3 centros quedan en
    Tempo≈91/127/167 BPM (una diferencia enorme) pero Bailabilidad≈0.50/
    0.56/0.61 (una diferencia mínima frente a su rango real 0.05-0.985) —
    Tempo domina casi por completo la distancia euclidiana, exactamente el
    efecto que Concepto 2 necesita mostrar.
  - K-means CON `StandardScaler` sobre las mismas dos columnas: los 3
    clusters quedan con tamaños comparables (51,867 / 34,782 / 27,193) y
    ahora sí se distinguen por Bailabilidad (0.42 / 0.48 / 0.71) además de
    por Tempo (93 / 156 / 115 BPM) — silhouette_score ≈ 0.392.
  - Cruce cluster×Genero (mismo modelo, k=3 escalado, 114 géneros reales):
    el género más común dentro de cada cluster nunca supera ~2.6% de ese
    cluster (House de Chicago 1.9%, Hardstyle 2.3%, Grindcore/Ópera 2.6%)
    — muy cerca del ≈0.9% que tocaría por puro azar (1/114), y lejísimos
    de que un cluster "sea" un género. Esto respalda la respuesta correcta
    ("no") de `check_cluster_es_genero`.
  - Agregar `Energia` a {Bailabilidad, Tempo} y re-ajustar (mismo k, mismo
    random_state): Adjusted Rand Index ≈ 0.528 frente al modelo de 2
    features — un cambio moderado, ni total ni trivial, porque
    corr(Bailabilidad, Energia) ≈ 0.13 y corr(Tempo, Energia) ≈ 0.24 (débil
    en ambos casos): `Energia` aporta información genuinamente nueva.
    Distinto del patrón "casi no cambia" de nb5 (`Peso` ya capturaba casi
    toda la señal) — la celda de muestra `nb6-demo-energia-*` refleja el
    hallazgo real de este dataset, no copia el de nb5.

Notas de scoring:
  reg_cuantos_grupos / reg_como_agrupa (registro de participación --
  texto corto, sin IA, sin respuesta incorrecta) valen 1 c/u = 2.
  cluster_es_genero (🧩 completa -- ¿los clusters son géneros reales?,
  respuesta objetiva "no", estructural) vale 5.
  t1-t5 (teoría: qué hace k-means, por qué escalar, por qué las etiquetas
  de cluster son arbitrarias, sensibilidad a k/inicialización, qué es un
  centroide) valen 5 c/u = 25.
  ex1 (Ejercicio 1 -- ajustar k-means escalado con 2 o 3 predictores
  propios + interpretar un centroide) vale 40.
  refl_ex2 (compara tu propio resultado con la muestra de agregar Energia)
  vale 5, IA. (id interno "nb6_ex2" conservado desde antes de la
  simplificación 2026-09-21 -- ver esa entrada más abajo -- para no
  requerir un redeploy de `grade-reflexion/index.ts`.)
  refl_generalizacion (riesgo de una recomendación/segmentación que no
  generaliza a datos nuevos, sobre el ejemplo guiado de train/test) vale
  5, IA.
  refl_final (riesgo de tratar un cluster como género oficial) vale 5, IA.
  _CORE_MAX = 2 (registro) + 5 (cluster_es_genero) + 25 (t1-5) + 40 (ex1)
            + 5 (refl_ex2) + 5 (refl_generalizacion) + 5 (refl_final) = 87.
  reto1 (bonus -- reejecutar con otro k y describir qué cambió) vale 10,
  fuera de _CORE_MAX, en _BONUS_MAX.

**Simplificación 2026-09-21 (mismo día, revisión — no una desviación
silenciosa)**: tras una lectura completa del notebook, el usuario decidió
que la Semana 7 es "extra credit para quienes ya avanzaron bien" y por lo
tanto debe ser mayoritariamente muestra + interpretación, con ejercicios
de construcción simples — no tres builds separados (ex1 40 + ex2 20 + ex3
20 = 80 pts de código desde cero). Se revierte la adición del mismo día
descrita justo abajo ("ex3 / refl_generalizacion agregados"), conservando
solo lo que sí encaja con ese objetivo:
  - `check_ex2` se elimina. Agregar `Energia` pasa de ser un
    `🔨 CONSTRUYE` calificado (20 pts) a una celda `👀 OBSERVA` de muestra
    sin calificar (`nb6-demo-energia-*` en `build_nb6.py`), mostrada ANTES
    del Ejercicio 1 para informar la elección de predictores del
    estudiante.
  - `check_ex1` se amplía para aceptar 2 O 3 predictores (antes exactamente
    2) — un solo build cubre lo que antes eran dos ejercicios separados,
    mismos 40 pts.
  - `check_ex3` se elimina por completo. El concepto de generalización ya
    lo enseña el ejemplo guiado `nb6-guiado-generaliza-*` (sin cambios) y
    ya lo evalúa `check_reflexion_generalizacion` (conservada, reescrita
    para referirse "al ejemplo guiado de arriba" en vez de "tu Ejercicio
    3" — ver ese método más abajo).
  - `check_reflexion_ex2` se conserva con el mismo id interno ("nb6_ex2",
    ver Notas de scoring arriba) pero su pregunta cambia: compara el
    resultado propio del estudiante con la muestra de Energia, no "tu
    Ejercicio 1 vs. tu Ejercicio 2".
  `_CORE_MAX` baja de 127 a 87 (-20 ex2, -20 ex3). `mini_a`/`mini_b`
  (checkpoints) y `explorador_completo` (achievement, antes exigía
  ex1+ex2+ex3 perfectos) actualizados para no referenciar ex2/ex3.
  `supabase/functions/grade-reflexion/index.ts`: `nb6_ex2`/
  `nb6_generalizacion`'s `question`/`grounding`/`grading_notes` reescritos
  para que coincidan (mismos ids, no requiere tocar `EXPECTED_NOTEBOOKS`,
  pero SÍ requiere redeploy de esa función para que el texto nuevo llegue
  a producción). Ver `WORKFORCE_HANDOFF.md`, Done log 2026-09-21 (segunda
  entrada), para el registro completo.

**Adición 2026-09-21, mismo día, anterior a la simplificación de arriba
(ex3 / refl_generalizacion agregados -- contexto histórico, la mayor parte
de esta sección ya no aplica tras la simplificación)**: la Semana 6 (nb5)
enseñó train/test para regresión -- generalización medida con un R² de
prueba. k-means no tiene una "respuesta correcta" que un R² de prueba
pueda medir como error (no hay etiqueta real), así que "test accuracy" no
aplica aquí -- intentarlo además contradiría al Concepto 3 (las etiquetas
de cluster no son categorías reales que se puedan acertar o fallar). El
equivalente correcto para un algoritmo no supervisado es la
generalización/estabilidad del agrupamiento en sí: ajustar SOLO con train,
usar `.predict()` (nunca re-ajustar) sobre un test held-out, y comparar si
los perfiles de cluster se sostienen. Motivado con dos casos de uso reales
-- recomendación de la próxima canción por cluster, y segmentación de
canciones para una decisión de marketing -- en vez de una prueba abstracta
de "qué tan bueno es el modelo". El ejemplo guiado que nació de esta
adición (`nb6-guiado-generaliza-*`) y la reflexión `refl_generalizacion`
sobreviven a la simplificación; solo el build `check_ex3` fue revertido.

El check de ex1 es deliberadamente ESTRUCTURAL, no un lookup de valores
exactos (a diferencia de nb3/4/5's R²/r): a diferencia de
`LinearRegression` (solución cerrada, determinística sin importar la
versión de sklearn), el número de cluster que k-means asigna a cada grupo
NO es portable entre corridas/versiones de sklearn — es literalmente el
mismo hecho que Concepto 3 enseña ("las etiquetas de cluster son
arbitrarias"). Hardcodear "el cluster bailable es el índice 0" sería a la
vez frágil (rompe con otra versión de sklearn/`n_init`) y pedagógicamente
contradictorio. En su lugar, check_ex1 verifica propiedades
independientes del índice: ¿se ajustó un `KMeans` real con `n_clusters`
correcto?, ¿los datos SÍ se escalaron antes de ajustar (los centros de
cluster deben quedar en un rango típico de datos estandarizados, no en el
rango crudo de `Tempo` en BPM)?, ¿la interpretación menciona la variable/
número propio del estudiante sin tratar el cluster como un género fijo?

Nota Supabase: mismo proyecto/tabla `submissions` que el resto del curso,
campo "curso"="STAT_2026", "notebook"="nb6". Deadline: 5 de octubre 2026,
11:59 PM Perú -- dos semanas después del cierre de nb5 (21 sept), mismo
cadencia de "dos semanas por notebook" que nb5 usó frente a nb4.
"""

import sys
import unicodedata
import datetime as _dt
from IPython.display import HTML, display

try:
    import pandas as pd
except ImportError:
    pd = None

# ─── Supabase Config (mismo proyecto que nb1/nb3) ─────────────
SUPABASE_URL      = "https://uwykikwutjtkpffwmdiq.supabase.co"
SUPABASE_ANON_KEY = "sb_publishable_aBG6GD4wn9CgpSE-47fagQ_sNhnzznu"
LOGO_URL          = "https://raw.githubusercontent.com/Santa-Maria-de-los-Andes/CS1---Grader/main/icono%20SMA.png"
CURSO_ID          = "STAT_2026"
NOTEBOOK_ID       = "nb6"

# ─── Deadline: 5 octubre 2026, 11:59 PM Peru (UTC-5) = 6 oct 04:59 UTC ─
_DEADLINE_UTC   = _dt.datetime(2026, 10, 6, 4, 59, 0, tzinfo=_dt.timezone.utc)
DEADLINE_PASSED = _dt.datetime.now(_dt.timezone.utc) >= _DEADLINE_UTC

# ─── Scoring ─────────────────────────────────────────────────
_CORE_MAX   = 87   # 2 (registro) + 5 (cluster_es_genero) + 25 (t1-5)
                   # + 40 (ex1) + 5 (refl_ex2) + 5 (refl_generalizacion)
                   # + 5 (refl_final)
_BONUS_KEYS = {"reto1"}
_BONUS_MAX  = 10   # reto1 — "reejecuta con otro k", fuera del core

# ─── Reflexion (calificada por IA vía Supabase Edge Function) ─
_REFLEXION_PTS       = 5
GRADE_REFLEXION_URL  = f"{SUPABASE_URL}/functions/v1/grade-reflexion"

# ─── Niveles "El Cartógrafo de Patrones" (por % del score core) ───
# Paleta verde bosque / ámbar de mapa -- distinta a proposito del violeta/
# cian mistico de nb5 y del sol calido de nb3/nb4 (COURSE_TEMPLATE.md §5,
# theming distinto por notebook).
_LEVELS = [
    (96, 6, "🏆 Cartógrafo Supremo"),
    (81, 5, "🏔️ Cartógrafo Experto"),
    (61, 4, "📍 Trazador de Fronteras"),
    (41, 3, "🗺️ Lector de Regiones"),
    (21, 2, "🧭 Primer Trazo"),
    (0,  1, "🌱 Aprendiz de Cartógrafo"),
]

_XP_GRAD = {
    1: "linear-gradient(90deg,#1b4332,#52b788)",
    2: "linear-gradient(90deg,#2d6a4f,#e9c46a)",
    3: "linear-gradient(90deg,#40916c,#95d5b2)",
    4: "linear-gradient(90deg,#023047,#74c69d)",
    5: "linear-gradient(90deg,#1b4332,#f4a261)",
    6: "linear-gradient(90deg,#f4a261,#e9c46a,#52b788)",
}
_LV_CSS_COLOR = {1: "#52b788", 2: "#e9c46a", 3: "#95d5b2", 4: "#74c69d", 5: "#f4a261", 6: "#e9c46a"}


def _level_info(pct):
    for thresh, num, name in _LEVELS:
        if pct >= thresh:
            return num, name
    return 1, "🌱 Primer Boceto"


def _lv_color(n):
    return _LV_CSS_COLOR.get(n, "#3a5a40")


def _is_nontrivial_text(v, min_len=15):
    """Guarda de placeholder/vacio -- corre ANTES de cualquier llamada de
    red a la funcion de calificacion IA."""
    if not isinstance(v, str):
        return False
    t = v.strip().strip('"').strip("'").strip()
    if t in ("", "___", "?", "..."):
        return False
    return len(t) >= min_len


# ─── Helpers ─────────────────────────────────────────────────

def _get(name):
    try:
        import __main__
        return getattr(__main__, name, None)
    except Exception:
        return None


def _approx(a, b, tol=1e-6):
    try:
        return abs(float(a) - float(b)) < tol
    except (TypeError, ValueError):
        return False


def _norm(s):
    """Minusculas + sin tildes, para comparar strings de forma tolerante."""
    if not isinstance(s, str):
        return ""
    s = s.strip().lower()
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c))


def _is_number(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _is_dataframe(v):
    return pd is not None and isinstance(v, pd.DataFrame)


def _is_series(v):
    return pd is not None and isinstance(v, pd.Series)


# Nombres reales de columna usadas por spotify_es.csv para las
# clusterizaciones de esta semana -- ver docstring del modulo para la
# validacion empirica de por que esta terna (escala muy distinta entre
# Bailabilidad y Tempo, sin one-hot encoding de por medio pese a que
# Genero tiene 114 categorias -- Genero nunca se usa como predictor).
_COL_BAILABILIDAD = "Bailabilidad"
_COL_TEMPO        = "Tempo"
_COL_ENERGIA      = "Energia"
_COL_GENERO       = "Genero"

_PREDICTORES_VALIDOS = [_COL_BAILABILIDAD, _COL_TEMPO, _COL_ENERGIA]
_PREDICTORES_NORM    = {_norm(c) for c in _PREDICTORES_VALIDOS}

# Los 114 generos reales de spotify_es.csv (traducidos por
# translate_to_spanish.py) -- usados solo para detectar si una
# interpretacion trata un cluster como si FUERA uno de estos generos de
# verdad, en vez de un grupo numerico que hay que interpretar. Este es el
# riesgo exacto que 04_GAUSS.md marca para la Semana 7: "interpretation
# text must not treat cluster labels as fixed/meaningful IDs". Normalizados
# con _norm() al comparar, asi que el case/acentos del texto del estudiante
# no importan.
_GENEROS_REALES = [
    "acustico", "afrobeat", "rock alternativo", "alternativa", "ambiental",
    "anime", "black metal", "bluegrass", "blues", "brasil", "breakbeat",
    "britanica", "cantopop", "house de chicago", "infantil", "relajante",
    "clasica", "club", "comedia", "country", "baile", "dancehall",
    "death metal", "deep house", "techno de detroit", "disco", "disney",
    "drum and bass", "dub", "dubstep", "edm", "electro", "electronica",
    "emo", "folk", "forro", "francesa", "funk", "garage", "alemana",
    "gospel", "gotica", "grindcore", "groove", "grunge", "guitarra",
    "feliz", "rock duro", "hardcore", "hardstyle", "heavy metal", "hip-hop",
    "honky-tonk", "house", "idm", "india", "indie", "indie pop",
    "industrial", "irani", "j-dance", "j-idol", "j-pop", "j-rock", "jazz",
    "k-pop", "para ninos", "latina", "latino", "malaya", "mandopop",
    "metal", "metalcore", "techno minimal", "mpb", "new age", "opera",
    "pagode", "fiesta", "piano", "pop", "pop de peliculas", "power pop",
    "progressive house", "rock psicodelico", "punk", "punk rock", "r&b",
    "reggae", "reggaeton", "rock", "rock and roll", "rockabilly",
    "romantica", "triste", "salsa", "samba", "sertanejo",
    "musical de teatro", "cantautor", "ska", "para dormir", "compositor",
    "soul", "en espanol", "para estudiar", "sueca", "synth-pop", "tango",
    "techno", "trance", "trip-hop", "turca", "musica del mundo",
]

# Palabras que matizan una afirmacion -- si el texto nombra un genero real
# Y usa una de estas, esta reconociendo la incertidumbre (ej. "se parece
# más a...", "no significa que sea..."), no afirmando que el cluster ES
# ese genero.
_PALABRAS_MATIZADORAS = [
    "parece", "parecen", "parecido", "podria", "podrian", "posiblemente",
    "probablemente", "tal vez", "talvez", "no necesariamente", "no siempre",
    "aunque", "no es", "no son", "no significa", "no quiere decir",
    "mezcla", "mezclados", "de varios generos", "distintos generos",
]


def _col_match(val, expected_colname, df=None):
    """Tolerante: acepta un string con el nombre de columna (con o sin
    tildes/mayusculas), o una Serie/columna que corresponda a esa columna."""
    expected_norm = _norm(expected_colname)
    if isinstance(val, str):
        return _norm(val) == expected_norm
    if _is_series(val) and df is not None and expected_colname in df.columns:
        try:
            return val.reset_index(drop=True).equals(df[expected_colname].reset_index(drop=True))
        except Exception:
            return False
    return False


def _predictores_normalizados(lst, min_n=2, max_n=3):
    """Valida una lista/tupla de min_n-max_n nombres de columna contra el
    menu permitido {Bailabilidad, Tempo, Energia}. Devuelve el frozenset
    normalizado (sin duplicados) si es valida, o None si no lo es."""
    if not isinstance(lst, (list, tuple)) or not all(isinstance(x, str) for x in lst):
        return None
    norm = {_norm(x) for x in lst}
    if len(norm) != len(lst):
        return None  # duplicados
    if not (min_n <= len(norm) <= max_n):
        return None
    if not norm.issubset(_PREDICTORES_NORM):
        return None
    return frozenset(norm)


def _trata_cluster_como_genero_fijo(text):
    """Detecta si una interpretacion afirma, sin matiz, que un cluster ES
    un genero real (ej. "el cluster 2 es de canciones de Reggaetón") en vez
    de describirlo con sus propias variables/numeros. Nombrar un genero
    real NO es un problema por si solo (puede ser parte de una comparacion
    honesta, ej. "el genero más común en este cluster es Pop, pero
    representa apenas 2%") -- el problema es afirmarlo sin ningun matiz."""
    t = _norm(text)
    menciona_genero = any(g in t for g in _GENEROS_REALES)
    if not menciona_genero:
        return False
    matiza = any(_norm(p) in t for p in _PALABRAS_MATIZADORAS)
    return not matiza


def _menciona_predictor_o_numero(text, predictores):
    """Rechaza relleno generico-pero-valido (pasa el largo minimo y aun asi
    no dice nada especifico -- ej. "el cluster que elegí agrupa canciones
    parecidas"). Exige que la interpretacion nombre al menos uno de los
    predictores que el propio estudiante eligio (tolerante a tildes/
    mayusculas via _norm) o incluya al menos un digito (un valor de
    centroide, un tamaño de cluster, cualquier numero de su propio
    resultado)."""
    t = _norm(text)
    if any(_norm(p) in t for p in predictores):
        return True
    return any(ch.isdigit() for ch in text)


def _menciona_train_test_o_numero(text):
    """Version de _menciona_predictor_o_numero() para el Ejercicio 3 --
    exige que la interpretacion nombre train/test (tolerante a 'entrena'/
    'prueba', castellano comun para esos terminos) o incluya al menos un
    numero de su propio resultado, en vez de una frase generica que
    serviria para cualquier comparacion."""
    t = _norm(text)
    if any(p in t for p in ("train", "entrena", "test", "prueba")):
        return True
    return any(ch.isdigit() for ch in text)


def _es_kmeans_fit(modelo, n_clusters_esperado, n_features_esperado=None):
    """Verifica estructuralmente que `modelo` sea un KMeans ya ajustado con
    el n_clusters esperado (y, si se pasa, el numero de features esperado)
    -- sin importar la version de sklearn ni que indice de cluster le tocó
    a cada grupo (ver docstring del modulo: por que este check es
    estructural y no un lookup de valores exactos)."""
    try:
        from sklearn.cluster import KMeans
    except ImportError:
        return False
    if not isinstance(modelo, KMeans):
        return False
    centers = getattr(modelo, "cluster_centers_", None)
    if centers is None:
        return False
    if centers.shape[0] != n_clusters_esperado:
        return False
    if n_features_esperado is not None and centers.shape[1] != n_features_esperado:
        return False
    return True


def _parece_escalado(modelo, tol=50.0):
    """Verifica que los centros de cluster queden en un rango plausible
    para datos ESTANDARIZADOS -- no exactamente ±3, porque un cluster chico
    de outliers extremos puede promediar z-scores de 10-17 sin que eso sea
    un error (verificado empíricamente contra `vgsales_es.csv`, con un
    cluster chico de "éxitos de taquilla", antes de fijar `tol`; re-
    confirmado contra `spotify_es.csv` -- ahí los centros escalados nunca
    superan ≈1.3 con k=3 ni k=4, así que `tol=50` deja margen amplio de
    sobra en ambos datasets). Sigue estando muy por debajo del rango crudo
    de una columna típicamente sin escalar en este curso (`Año` ~1980-2020,
    `Tempo` en BPM hasta ~243) -- sin escalar, cualquier centro que
    involucre esas columnas cae muy por fuera de `tol`. Version estructural
    e independiente de indice de cluster del chequeo que 04_GAUSS.md exige
    ("confirms features are scaled before fitting")."""
    try:
        import numpy as _np
    except ImportError:
        return False
    centers = getattr(modelo, "cluster_centers_", None)
    if centers is None:
        return False
    return bool(_np.all(_np.abs(centers) < tol))


# ─── Main Class ──────────────────────────────────────────────

class Autograder:

    def __init__(self):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass
        self._scores       = {}
        self._text_answers = {}
        self._achievements = set()
        self._streak       = 0
        self._prev_level   = 0
        self._nombre_real  = None
        self._grado        = None
        self._dni          = None
        self._checkpoints  = set()
        self._show_registration_form()

    # ── Registration form ────────────────────────────────────

    def _show_registration_form(self):
        logo_tag = (f'<img src="{LOGO_URL}" style="height:48px;object-fit:contain;" '
                    f'onerror="this.style.display=\'none\'">'
                    if LOGO_URL else
                    '<span style="font-family:\'Press Start 2P\',monospace;font-size:13px;'
                    'color:#e9c46a;letter-spacing:2px;">SMA</span>')

        try:
            from google.colab import output as _out

            def _on_register(nombre, grado, dni):
                nombre = (nombre or "").strip()
                grado  = (grado  or "").strip()
                dni    = (dni    or "").strip()
                if not nombre or not grado or not dni:
                    return
                self._nombre_real = nombre
                self._grado       = grado
                self._dni         = dni

                _best = None
                try:
                    import urllib.request as _ur2, json as _json2, urllib.parse as _up2
                    # 2026-08-24 (mismo bug reportado en vivo por el usuario
                    # para autograder_nb3.py, corregido aca en espejo): esta
                    # query filtraba por dni+notebook pero NO por curso, y
                    # ademas restauraba progreso con solo un match de dni --
                    # sin comparar `nombre` como si hace nb3. `notebook` no es
                    # unico entre cursos (el modulo de Programacion tambien
                    # usa ids simples como 'nb2'/'nb3'), y el DNI es texto
                    # libre sin validacion de formato/unicidad, asi que
                    # cualquiera de las dos colisiones heredaba en silencio
                    # score_breakdown/achievements/streak/nivel de otro
                    # curso u otro alumno -- se mostraba "ya hecho" con un
                    # score que nunca tuvo las claves refl_* de esta materia,
                    # y esa fila ajena se resometia despues bajo
                    # curso=STAT_2026 (ver _submit_to_supabase), contaminando
                    # la tabla real.
                    _qurl = (
                        f"{SUPABASE_URL}/rest/v1/submissions"
                        f"?select=nombre,earned,possible,pct,level_name,level_num,streak,achievements,score_breakdown"
                        f"&dni=eq.{_up2.quote(str(dni), safe='')}"
                        f"&curso=eq.{CURSO_ID}"
                        f"&notebook=eq.{NOTEBOOK_ID}"
                        f"&order=pct.desc,submitted_at.desc&limit=1"
                    )
                    _req2 = _ur2.Request(_qurl, headers={
                        "apikey": SUPABASE_ANON_KEY,
                        "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
                    })
                    with _ur2.urlopen(_req2, timeout=8) as _resp2:
                        _rows = _json2.loads(_resp2.read())
                    if _rows and _norm(_rows[0].get("nombre")) == _norm(nombre):
                        _best = _rows[0]
                        self._scores = {
                            k: (int(v.get("e", 0)), int(v.get("p", 0)))
                            for k, v in (_best.get("score_breakdown") or {}).items()
                        }
                        # Restaura tambien el texto crudo de las celdas de
                        # registro (reg_*) -- si no se restaura aca, el
                        # proximo _submit_to_supabase() (ej. al final en
                        # resumen()) reconstruye score_breakdown solo desde
                        # self._text_answers, que arrancaria vacio en esta
                        # sesion nueva, y pisaria el texto ya guardado de una
                        # sesion anterior con un score_breakdown sin "text".
                        self._text_answers = {
                            k: v["text"]
                            for k, v in (_best.get("score_breakdown") or {}).items()
                            if isinstance(v, dict) and "text" in v
                        }
                        self._achievements = set(_best.get("achievements") or [])
                        self._streak       = int(_best.get("streak") or 0)
                        self._prev_level   = int(_best.get("level_num") or 0)
                except Exception:
                    pass

                if _best:
                    _score_html = f'''
  <div style="background:#0c0a16;border:1px solid #52b788;border-radius:3px;
    padding:12px 20px;margin-top:6px;
    font-family:'Press Start 2P',monospace;animation:ag-fadein .4s ease .1s both;">
    <div style="font-size:6px;color:#52b788;letter-spacing:2px;margin-bottom:10px;">
      🧭 TU MEJOR MARCA — SEMANA 7</div>
    <div style="display:flex;align-items:center;gap:20px;">
      <div style="font-size:28px;color:#e9c46a;
        text-shadow:0 0 16px rgba(255,209,102,.8),2px 2px 0 #2d6a4f;">
        {_best['pct']}%</div>
      <div>
        <div style="font-size:8px;color:#f4a261;letter-spacing:1px;">{_best['level_name']}</div>
        <div style="font-size:6px;color:#b0a8d0;margin-top:6px;letter-spacing:1px;">
          {_best['earned']} / {_best['possible']} XP</div>
      </div>
    </div>
  </div>'''
                else:
                    _score_html = (
                        '<div style="background:#0c0a16;border:1px solid #241f3d;border-radius:3px;'
                        'padding:10px 20px;margin-top:6px;'
                        'font-family:\'Press Start 2P\',monospace;font-size:6px;color:#7a72a0;'
                        'letter-spacing:1px;animation:ag-fadein .4s ease .1s both;">'
                        '🧭 El mapa todavía está en blanco — ¡aun no tienes marca registrada!</div>'
                    )

                display(HTML(f'''
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
  @keyframes ag-fadein {{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:translateY(0)}}}}
  @keyframes ag-start  {{0%{{opacity:0;transform:scale(.7)}}60%{{transform:scale(1.12)}}100%{{opacity:1;transform:scale(1)}}}}
  @keyframes ag-dot    {{0%,80%,100%{{transform:scale(.6);opacity:.3}}40%{{transform:scale(1);opacity:1}}}}
  @keyframes ag-spin   {{to{{transform:rotate(360deg)}}}}
</style>
<div style="max-width:840px;margin:10px 0;box-sizing:border-box;">
  <div style="background:#140c04;border:1px solid #f4a261;border-radius:3px;padding:12px 18px;
    font-family:'Press Start 2P',monospace;font-size:8px;
    color:#f4a261;letter-spacing:1px;animation:ag-fadein .4s ease;">
    🧭 &nbsp;¡BIENVENIDO DE VUELTA, CARTÓGRAFO {nombre.upper()}! &nbsp;·&nbsp; {grado}
  </div>
  {_score_html}
  <div id="ag-loading" style="background:#0c0a16;border:1px solid #241f3d;border-radius:3px;
    padding:22px 18px;margin-top:6px;text-align:center;animation:ag-fadein .5s ease .2s both;">
    <div style="display:flex;justify-content:center;gap:6px;margin-bottom:12px;">
      <div style="width:8px;height:8px;border-radius:50%;background:#f4a261;
        animation:ag-dot 1.2s ease-in-out 0s infinite;"></div>
      <div style="width:8px;height:8px;border-radius:50%;background:#f4a261;
        animation:ag-dot 1.2s ease-in-out .2s infinite;"></div>
      <div style="width:8px;height:8px;border-radius:50%;background:#f4a261;
        animation:ag-dot 1.2s ease-in-out .4s infinite;"></div>
    </div>
    <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#7a72a0;letter-spacing:2px;">
      TRAZANDO EL MAPA…
    </div>
  </div>
  <div id="ag-start" style="display:none;background:linear-gradient(160deg,#0c0a16,#1a1436);
    border:2px solid #f4a261;border-radius:4px;padding:36px 24px;margin-top:6px;text-align:center;
    box-shadow:0 0 40px rgba(255,158,44,.25),0 0 80px rgba(255,209,102,.06),0 6px 24px rgba(0,0,0,.9);">
    <div style="font-size:44px;margin-bottom:14px;animation:ag-start .55s cubic-bezier(.34,1.56,.64,1);">🧭</div>
    <div style="font-family:'Press Start 2P',monospace;font-size:clamp(15px,3.6vw,26px);color:#e9c46a;
      letter-spacing:4px;text-shadow:0 0 24px rgba(255,209,102,.95),0 0 50px rgba(255,158,44,.35),
      2px 2px 0 #2d6a4f;animation:ag-start .6s ease;margin-bottom:14px;">¡CONTINÚA TU MISIÓN!</div>
    <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#52b788;
      letter-spacing:2px;opacity:.85;margin-bottom:16px;">EJECUTA LA PRIMERA CELDA PARA COMENZAR</div>
    <div style="font-size:15px;color:#f4a261;opacity:.4;letter-spacing:8px;">🧭 🗺️ 🧭 🗺️ 🧭 🗺️ 🧭</div>
  </div>
</div>
<script>
setTimeout(function(){{
  var l = document.getElementById('ag-loading');
  var s = document.getElementById('ag-start');
  if(l) l.style.display = 'none';
  if(s){{ s.style.display = 'block'; }}
}}, 1600);
</script>
'''))

            _out.register_callback('_ag_register', _on_register)
            _out.register_callback('_ag_teoria_answer', self._grade_teoria)
            _out.register_callback('_ag_reflexion_answer', self._grade_reflexion)
            _out.register_callback('_ag_registro_answer', self._grade_registro)

            display(HTML(f'''
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
  .ag-input,.ag-select {{
    width:100%;box-sizing:border-box;background:#0c0a16;border:1px solid #241f3d;
    border-radius:3px;padding:0 12px;color:#ece8f8;font-size:13px;height:42px;
    font-family:'Segoe UI',Roboto,sans-serif;outline:none;transition:border .2s;
  }}
  .ag-input:focus,.ag-select:focus {{ border-color:#52b788; }}
  .ag-select option {{ background:#0c0a16; }}
  .ag-btn {{
    width:100%;padding:13px;background:linear-gradient(90deg,#6a3fc0,#f4a261);
    border:none;border-radius:3px;color:#0c0a16;font-family:'Press Start 2P',monospace;
    font-size:9px;letter-spacing:2px;cursor:pointer;transition:opacity .2s;margin-top:6px;
  }}
  .ag-btn:hover {{ opacity:.85; }}
  .ag-err {{ color:#ff5d5d;font-size:11px;margin-top:6px;display:none; }}
  .ag-label {{ font-family:'Press Start 2P',monospace;font-size:7px;letter-spacing:1px;
    margin-bottom:8px;display:flex;align-items:center;gap:5px; }}
  .ag-field {{ display:flex;flex-direction:column; }}
</style>
<div style="background:#0c0a16;border:2px solid #52b788;border-radius:4px;max-width:840px;
  margin:10px 0;overflow:hidden;box-shadow:0 0 40px rgba(74,168,216,.2),0 10px 30px rgba(0,0,0,.8);">

  <div style="background:linear-gradient(90deg,#0c0a16,#1a1436,#0c0a16);border-bottom:2px solid #e9c46a;
    padding:18px 24px;position:relative;display:flex;align-items:center;justify-content:center;min-height:80px;">
    <div style="position:absolute;left:20px;top:50%;transform:translateY(-50%);">{logo_tag}</div>
    <div style="text-align:center;">
      <div style="font-family:'Press Start 2P',monospace;font-size:clamp(13px,3vw,18px);color:#e9c46a;letter-spacing:3px;
        text-shadow:0 0 14px rgba(255,209,102,.7),2px 2px 0 #2d6a4f;">🧭 MISIÓN 4: EL CARTÓGRAFO DE PATRONES 🗺️</div>
      <div style="font-family:'Press Start 2P',monospace;font-size:8px;color:#f4a261;
        letter-spacing:2px;margin-top:8px;">SEMANA 7 — EL CARTÓGRAFO DE PATRONES</div>
    </div>
    <div style="position:absolute;right:20px;top:50%;transform:translateY(-50%);">{logo_tag}</div>
  </div>

  <div style="padding:24px;">
    <div style="display:grid;grid-template-columns:2fr 1fr;gap:14px;margin-bottom:14px;align-items:end;">
      <div class="ag-field">
        <div class="ag-label" style="color:#f4a261;">🧭 NOMBRE COMPLETO</div>
        <input id="ag-nombre" class="ag-input" placeholder="Tu nombre y apellido" />
      </div>
      <div class="ag-field">
        <div class="ag-label" style="color:#f4a261;">🏫 GRADO</div>
        <select id="ag-grado" class="ag-select">
          <option value="">— Selecciona —</option>
          <option value="3ro">3ro</option>
          <option value="4to">4to</option>
          <option value="5to">5to</option>
        </select>
      </div>
    </div>
    <div class="ag-field" style="margin-bottom:14px;">
      <div class="ag-label" style="color:#e9c46a;">🪪 CÓDIGO DE ESTUDIANTE (DNI, Pasaporte, Carnet)</div>
      <input id="ag-dni" class="ag-input" placeholder="Ingresa tu código" />
    </div>
    <div id="ag-err" class="ag-err">⚠ Por favor completa todos los campos.</div>
    <button class="ag-btn" onclick="agRegister()">🧭 &nbsp; ¡CONTINUAR LA EXPEDICIÓN! &nbsp; 🗺️</button>
  </div>
</div>
<script>
async function agRegister() {{
  const nombre = document.getElementById('ag-nombre').value.trim();
  const grado  = document.getElementById('ag-grado').value.trim();
  const dni    = document.getElementById('ag-dni').value.trim();
  const err    = document.getElementById('ag-err');
  if (!nombre || !grado || !dni) {{ err.style.display = 'block'; return; }}
  err.style.display = 'none';
  await google.colab.kernel.invokeFunction('_ag_register', [nombre, grado, dni], {{}});
}}
</script>
'''))

        except ImportError:
            try:
                display(HTML('<div style="font-family:monospace;padding:10px;background:#0c0a16;'
                             'color:#f4a261;border:1px solid #52b788;border-radius:3px;max-width:840px;">'
                             '🧭 MISIÓN 4 — SEMANA 7 — Registro</div>'))
                self._nombre_real = input("Nombre completo: ").strip()
                grado_opts = {"1": "3ro", "2": "4to", "3": "5to"}
                print("Grado: 1) 3ro  2) 4to  3) 5to")
                self._grado = grado_opts.get(input("Elige (1/2/3): ").strip(), "3ro")
                self._dni   = input("Código de estudiante (DNI/Pasaporte/Carnet): ").strip()
            except Exception:
                pass

    # ── Internal helpers ─────────────────────────────────────

    @property
    def _logo_tag(self):
        if LOGO_URL:
            return (f'<img src="{LOGO_URL}" style="height:40px;object-fit:contain;" '
                    f'onerror="this.style.display=\'none\'">')
        return '<span style="font-family:\'Press Start 2P\',monospace;font-size:11px;color:#e9c46a;">SMA</span>'

    @property
    def _logo_tag_sm(self):
        if LOGO_URL:
            return (f'<img src="{LOGO_URL}" style="height:24px;object-fit:contain;" '
                    f'onerror="this.style.display=\'none\'">')
        return '<span style="font-family:\'Press Start 2P\',monospace;font-size:8px;color:#e9c46a;">SMA</span>'

    def _nombre(self):
        if self._nombre_real:
            return self._nombre_real
        return "cartógrafo"

    def _totals(self):
        earned   = sum(e for k, (e, _) in self._scores.items() if k not in _BONUS_KEYS)
        possible = sum(p for k, (_, p) in self._scores.items() if k not in _BONUS_KEYS)
        pct      = min(round(earned / _CORE_MAX * 100), 100)
        return earned, possible, pct

    def _bonus_earned(self):
        return sum(e for k, (e, _) in self._scores.items() if k in _BONUS_KEYS)

    def _unlock(self, key):
        if key not in self._achievements:
            self._achievements.add(key)
            return True
        return False

    def _header(self, title, icon="🧭", pts=None):
        self._curr_title = title
        self._curr_icon  = icon
        self._curr_pts   = pts

    def _check_achievements(self, key):
        unlocked = []
        earned, possible, pct = self._totals()

        # Primer Trazo — primer XP ganado
        if any(e > 0 for e, _ in self._scores.values()) and self._unlock("primer_trazo"):
            unlocked.append(("🧭 Primer Trazo — ¡Tu primera marca en el mapa!", "#f4a261", "Boceto"))

        # Cartógrafo Novato — ex1 perfecto (predictores + modelo escalado + interpretacion)
        if (self._scores.get("ex1", (0, 1))[0] == self._scores.get("ex1", (0, 1))[1]
                and "ex1" in self._scores and self._unlock("cartografo_novato")):
            unlocked.append(("🗺️ Cartógrafo Novato — Tu primer mapa de clusters, escalado y bien interpretado", "#52b788", "Trazo"))

        # Explorador Completo — ex1 perfecto + las 3 reflexiones enviadas
        # (comparaste tu mapa con la muestra de Energia, con el ejemplo de
        # generalización, y con el riesgo de tratar un cluster como
        # género real). Redefinida 2026-09-21 junto con la simplificación
        # que eliminó ex2/ex3 como builds calificados -- antes exigía
        # ex1+ex2+ex3 perfectos.
        refl_keys = ["refl_nb6_ex2", "refl_nb6_generalizacion", "refl_nb6_final"]
        if (self._scores.get("ex1", (0, 1))[0] == self._scores.get("ex1", (0, 1))[1]
                and "ex1" in self._scores
                and all(k in self._scores for k in refl_keys)
                and self._unlock("explorador_completo")):
            unlocked.append(("🏔️ Explorador Completo — Tu mapa quedó bien trazado y reflexionaste sobre los tres conceptos clave", "#95d5b2", "Hallazgo"))

        # Cazador de K — completaste el reto de reejecutar con otro k
        if (self._scores.get("reto1", (0, 1))[0] > 0
                and "reto1" in self._scores and self._unlock("cazador_de_k")):
            unlocked.append(("🎯 Cazador de K — Reejecutaste con otro k y viste cómo cambia el mapa", "#95d5b2", "Hallazgo"))

        # Medalla del Cartógrafo — ambos checkpoints de Semana 7 alcanzados
        if len(self._checkpoints) >= 2 and self._unlock("medalla_cartografo"):
            unlocked.append(("🎖️ Medalla del Cartógrafo — Ambos checkpoints de Semana 7 superados", "#95d5b2", "Hallazgo"))

        # Racha de Trazos — racha >= 5
        if self._streak >= 5 and self._unlock("racha_de_trazos"):
            unlocked.append(("🔥 Racha de Trazos — Combo x5", "#52b788", "Trazo"))

        # Mapa Completo — 100% del core
        if pct >= 100 and self._unlock("mapa_completo"):
            unlocked.append(("🏆 Mapa Completo — 100% de la Semana 7", "#f4a261", "Mapa Maestro"))

        # Level-up
        lvl_num, lvl_name = _level_info(pct)
        if lvl_num > self._prev_level and self._prev_level > 0:
            unlocked.append((f"⬆️ ¡SUBISTE DE NIVEL! — {lvl_name}", "#52b788", "Nivel"))
        if lvl_num > self._prev_level:
            self._prev_level = lvl_num

        return unlocked

    def _award(self, key, checks, max_pts):
        passed = sum(1 for ok, _, _ in checks if ok)
        pts    = round(max_pts * passed / len(checks)) if checks else 0
        self._scores[key] = (pts, max_pts)

        if pts == max_pts:
            self._streak += 1
        else:
            self._streak = 0

        earned, possible, pct = self._totals()
        lvl_num, lvl_name     = _level_info(pct)

        import threading as _thr
        _thr.Thread(
            target=self._submit_to_supabase,
            args=(earned, possible, pct, lvl_num, lvl_name, True),
            daemon=True,
        ).start()

        rows_html = ""
        for ok, label, msg in checks:
            if ok:
                rows_html += (
                    f'<div style="display:flex;align-items:flex-start;gap:10px;padding:7px 10px;'
                    f'margin-bottom:3px;background:rgba(76,175,80,.05);'
                    f'border-left:3px solid #4caf50;border-radius:0 3px 3px 0;">'
                    f'<span style="color:#4caf50;font-size:13px;flex-shrink:0;line-height:1.5;">✔</span>'
                    f'<div style="font-size:11px;line-height:1.5;">'
                    f'<span style="color:#4caf50;font-weight:bold;">{label}:</span> '
                    f'<span style="color:#b0a8d0;">{msg}</span></div></div>'
                )
            else:
                rows_html += (
                    f'<div style="display:flex;align-items:flex-start;gap:10px;padding:7px 10px;'
                    f'margin-bottom:3px;background:rgba(255,93,93,.06);'
                    f'border-left:3px solid #ff5d5d;border-radius:0 3px 3px 0;">'
                    f'<span style="color:#ff5d5d;font-size:13px;flex-shrink:0;line-height:1.5;">✖</span>'
                    f'<div style="font-size:11px;line-height:1.5;">'
                    f'<span style="color:#ff5d5d;font-weight:bold;">{label}:</span> '
                    f'<span style="color:#c9a8d8;">{msg}</span></div></div>'
                )

        star_r = pts / max_pts if max_pts > 0 else 0
        gold, dark = "#e9c46a", "#2a2200"
        if star_r == 1.0:
            stars_html = f'<span style="color:{gold};font-size:15px;letter-spacing:3px;">★★★</span>'
        elif star_r >= 0.67:
            stars_html = (f'<span style="color:{gold};font-size:15px;letter-spacing:3px;">★★</span>'
                          f'<span style="color:{dark};font-size:15px;">★</span>')
        elif star_r > 0:
            stars_html = (f'<span style="color:{gold};font-size:15px;">★</span>'
                          f'<span style="color:{dark};font-size:15px;letter-spacing:3px;">★★</span>')
        else:
            stars_html = f'<span style="color:{dark};font-size:15px;letter-spacing:3px;">★★★</span>'

        combo_html = ""
        if self._streak >= 2:
            c_color = "#f4a261" if self._streak >= 5 else "#e9c46a"
            combo_html = (
                f'<div style="display:inline-flex;align-items:center;gap:5px;padding:3px 10px;'
                f'background:rgba(255,158,44,.12);border:1px solid {c_color};border-radius:2px;'
                f'margin-left:8px;">'
                f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;'
                f'color:{c_color};">🧭 RACHA x{self._streak}</span></div>'
            )

        if pts == max_pts:
            s_icon, s_text, s_color = "🗺️", f"¡ZONA DEL MAPA COMPLETA! +{pts} XP", "#4caf50"
            border_color, glow = "#4caf50", "0 0 22px rgba(76,175,80,.15)"
        elif pts > 0:
            s_icon, s_text, s_color = "🧭", f"+{pts} XP  ·  {max_pts - pts} por trazar", "#e9c46a"
            border_color, glow = "#95d5b2", "0 0 22px rgba(255,183,3,.12)"
        else:
            s_icon, s_text, s_color = "🌫️", "NIEBLA EN EL MAPA — Corrige los ✖ e intenta de nuevo", "#ff5d5d"
            border_color, glow = "#ff5d5d", "0 0 22px rgba(255,93,93,.15)"

        xp_grad = _XP_GRAD.get(lvl_num, _XP_GRAD[1])

        dots = "".join(
            f'<span style="display:inline-block;width:7px;height:7px;border-radius:50%;'
            f'background:{"#4caf50" if ok else "#ff5d5d"};margin:0 2px;'
            f'box-shadow:0 0 4px {"#4caf50" if ok else "#ff5d5d"};"></span>'
            for ok, _, _ in checks
        )

        new_ach     = self._check_achievements(key)
        reg_ach     = [(n, c, r) for n, c, r in new_ach if r != "Nivel"]
        levelup_ach = [(n, c, r) for n, c, r in new_ach if r == "Nivel"]

        _RC = {
            "Boceto":      ("#3a5a40", "rgba(58,90,64,.14)",   "🌱"),
            "Trazo":       ("#52b788", "rgba(82,183,136,.12)", "🧭"),
            "Hallazgo":    ("#95d5b2", "rgba(149,213,178,.12)", "🗺️"),
            "Mapa Maestro": ("#f4a261", "rgba(244,162,97,.15)", "🏆"),
        }
        ach_html = ""
        for ach_name, _, ach_rarity in reg_ach:
            bc, bg, ach_icon = _RC.get(ach_rarity, _RC["Boceto"])
            ach_html += (
                f'<div style="display:flex;align-items:center;gap:10px;margin-top:8px;'
                f'padding:10px 12px;background:{bg};border:1px solid {bc};border-radius:3px;">'
                f'<span style="font-size:18px;">{ach_icon}</span>'
                f'<div style="flex:1;">'
                f'<div style="margin-bottom:3px;">'
                f'<span style="background:{bc};color:#0c0a16;font-size:7px;font-weight:bold;'
                f'padding:1px 5px;border-radius:2px;font-family:\'Press Start 2P\',monospace;">'
                f'{ach_rarity.upper()}</span>'
                f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;'
                f'color:{bc};margin-left:6px;">LOGRO DESBLOQUEADO</span>'
                f'</div>'
                f'<div style="color:#ece8f8;font-size:12px;font-weight:bold;">{ach_name}</div>'
                f'</div></div>'
            )

        curr_icon  = getattr(self, '_curr_icon', '🧭')
        curr_title = getattr(self, '_curr_title', 'EJERCICIO').upper()
        _logo_sm   = self._logo_tag_sm

        _core_pct_bar = min(round(earned / _CORE_MAX * 100), 100)
        xp_bar_html = (
            f'<div style="display:flex;justify-content:space-between;margin-bottom:4px;">'
            f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;color:#7a72a0;">'
            f'XP: {earned}/{_CORE_MAX}</span>'
            f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;'
            f'color:{_lv_color(lvl_num)};">{lvl_name}</span></div>'
            f'<div style="width:100%;height:10px;background:#191430;border:1px solid #241f3d;'
            f'border-radius:2px;overflow:hidden;">'
            f'<div style="width:{_core_pct_bar}%;height:100%;background:{xp_grad};'
            f'border-radius:2px;transform-origin:left;'
            f'animation:pg-xpscale 1.1s cubic-bezier(.4,0,.2,1) forwards;'
            f'box-shadow:0 0 6px rgba(255,209,102,.25);"></div></div>'
        )

        deadline_html = ""
        if DEADLINE_PASSED:
            deadline_html = '''<div style="margin-top:10px;padding:12px 16px;background:#1a0000;
  border:2px solid #ff0000;border-radius:3px;text-align:center;">
  <div style="font-family:'Press Start 2P',monospace;font-size:10px;color:#ff0000;
    letter-spacing:2px;text-shadow:0 0 10px rgba(255,0,0,.6);">🚫 PLAZO VENCIDO</div>
  <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#ff8888;
    margin-top:6px;letter-spacing:1px;">TU NOTA NO SERÁ ACTUALIZADA</div>
  <div style="font-size:11px;color:#cc6666;margin-top:6px;">
    Puedes revisar tus respuestas, pero la entrega ya cerró.</div></div>'''
        elif self._dni:
            deadline_html = ('<div style="margin-top:8px;font-family:\'Press Start 2P\',monospace;'
                             'font-size:6px;color:#52b788;letter-spacing:1px;opacity:.85;">'
                             '📊 Calificación actualizada en la base de datos</div>')

        card_html = f'''<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
  @keyframes pg-xpscale{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
</style>
<div style="background:#0c0a16;border:2px solid {border_color};border-radius:4px;max-width:840px;
  margin-bottom:14px;overflow:hidden;box-shadow:{glow},0 6px 24px rgba(0,0,0,.7);
  font-family:'Segoe UI',Roboto,sans-serif;">
  <div style="background:{border_color}18;border-bottom:1px solid {border_color}40;
    padding:9px 16px;display:flex;justify-content:space-between;align-items:center;">
    <div style="display:flex;align-items:center;gap:8px;">
      {_logo_sm}
      <span style="font-family:'Press Start 2P',monospace;font-size:9px;
        color:{border_color};letter-spacing:1px;">{curr_icon} {curr_title}</span>
    </div>
    <div style="display:flex;align-items:center;gap:10px;">
      {stars_html}
      <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#f4a261;
        background:rgba(255,158,44,.1);border:1px solid rgba(255,158,44,.4);
        padding:3px 8px;border-radius:2px;">MAX {max_pts} XP</div>
    </div>
  </div>
  <div style="padding:10px 14px 6px;">{rows_html}</div>
  <div style="background:#0f0c1e;border-top:1px solid #1a1710;padding:11px 14px;">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:9px;">
      <div style="display:flex;align-items:center;gap:8px;">
        <span style="font-size:16px;">{s_icon}</span>
        <span style="font-family:'Press Start 2P',monospace;font-size:8px;
          color:{s_color};">{s_text}</span>
        {combo_html}
      </div>
      <div style="display:flex;align-items:center;gap:4px;color:#7a72a0;font-size:10px;">
        {dots}<span style="margin-left:3px;">{passed}/{len(checks)}</span>
      </div>
    </div>
    {xp_bar_html}
    {ach_html}
    {deadline_html}
  </div>
</div>'''
        display(HTML(card_html))

        for _ in levelup_ach:
            display(HTML(self._render_levelup(lvl_num, lvl_name)))

        return pts

    # ── Level-up banner ───────────────────────────────────────

    def _render_levelup(self, lvl_num, lvl_name):
        import random as _r
        _r.seed(lvl_num * 97 + 31)
        uid = f"lu{_r.randint(10000, 99999)}"

        _cfg = {
            2: dict(bg="linear-gradient(160deg,#0c0a16,#12271e)",
                    c="#e9c46a", sc="#ffe6a3", rc="#e9c46a",
                    sub="PRIMER TRAZO — EL MAPA EMPIEZA A TOMAR FORMA", icon="🧭"),
            3: dict(bg="linear-gradient(160deg,#0f1f14,#1a1030)",
                    c="#95d5b2", sc="#c7f0d8", rc="#95d5b2",
                    sub="LECTOR DE REGIONES — LOS GRUPOS EMPIEZAN A HABLAR", icon="🗺️"),
            4: dict(bg="linear-gradient(160deg,#0d0c22,#14203d)",
                    c="#52b788", sc="#9fe8c9", rc="#52b788",
                    sub="TRAZADOR DE FRONTERAS — TU MAPA YA AGRUPA DE VERDAD", icon="📍"),
            5: dict(bg="linear-gradient(160deg,#180d02,#2a1400)",
                    c="#f4a261", sc="#ffc27a", rc="#f4a261",
                    sub="CARTÓGRAFO EXPERTO — SABES CUÁNDO CONFIAR EN UN CLUSTER", icon="🏔️"),
            6: dict(bg="linear-gradient(160deg,#0c0a16,#1a0f02,#0d260f)",
                    c="#e9c46a", sc="#52b788", rc="#f4a261",
                    sub="CARTÓGRAFO SUPREMO — SALÓN DE LA FAMA", icon="🏆"),
        }
        cfg = _cfg.get(lvl_num, _cfg[2])
        c, sc, rc = cfg["c"], cfg["sc"], cfg["rc"]

        _sd = [(-50,-88),(0,-100),(50,-88),(92,-35),(78,55),(0,92),(-78,55),(-92,-35)]
        _bd = [(-4,-115),(115,0),(4,115),(-115,0)]
        spark_css, spark_html = "", ""
        for i, (dx, dy) in enumerate(_sd):
            d = 0.12 + i * 0.035
            sz = 4 if i % 2 == 0 else 3
            spark_css  += (f"@keyframes {uid}-s{i}{{0%{{transform:translate(0,0);opacity:1}}"
                           f"100%{{transform:translate({dx}px,{dy}px);opacity:0}}}}")
            spark_html += (f'<div style="position:absolute;top:50%;left:50%;width:{sz}px;height:{sz}px;'
                           f'border-radius:50%;background:{sc};margin:-{sz//2}px;opacity:0;'
                           f'animation:{uid}-s{i} .85s ease-out {d:.2f}s forwards;'
                           f'pointer-events:none;z-index:6;"></div>')
        for i, (dx, dy) in enumerate(_bd):
            d = 0.08 + i * 0.08
            spark_css  += (f"@keyframes {uid}-b{i}{{0%{{transform:translate(0,0);opacity:.9}}"
                           f"100%{{transform:translate({dx}px,{dy}px);opacity:0}}}}")
            spark_html += (f'<div style="position:absolute;top:50%;left:50%;width:6px;height:6px;'
                           f'border-radius:50%;background:{c};margin:-3px;opacity:0;'
                           f'animation:{uid}-b{i} 1.1s ease-out {d:.2f}s forwards;'
                           f'pointer-events:none;z-index:6;"></div>')

        extra_ring = ""
        if lvl_num == 6:
            extra_ring = (f'<div style="position:absolute;top:50%;left:50%;width:100px;height:100px;'
                          f'margin:-50px;border-radius:50%;border:2px solid #52b788;opacity:0;'
                          f'animation:{uid}-ring 1.6s ease-out .5s forwards;'
                          f'pointer-events:none;z-index:5;"></div>')

        return f'''<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
  @keyframes {uid}-flash{{0%{{opacity:.6}}35%{{opacity:.15}}100%{{opacity:0}}}}
  @keyframes {uid}-ring {{0%{{transform:scale(.08);opacity:.95}}100%{{transform:scale(4.5);opacity:0}}}}
  @keyframes {uid}-icon {{
    0%  {{transform:scale(0) rotate(-25deg);opacity:0}}
    55% {{transform:scale(1.22) rotate(6deg);opacity:1}}
    72% {{transform:scale(0.91) rotate(-3deg)}}
    86% {{transform:scale(1.06) rotate(2deg)}}
    100%{{transform:scale(1) rotate(0deg)}}}}
  @keyframes {uid}-slam {{
    0%  {{transform:scaleX(3) scaleY(0.05);opacity:0;letter-spacing:16px}}
    55% {{transform:scaleX(1.04) scaleY(1.04);opacity:1}}
    100%{{transform:scale(1);letter-spacing:4px}}}}
  @keyframes {uid}-rise {{
    0%  {{transform:translateY(32px);opacity:0;filter:blur(6px)}}
    100%{{transform:translateY(0);opacity:1;filter:blur(0)}}}}
  @keyframes {uid}-sub  {{from{{opacity:0;letter-spacing:6px}}to{{opacity:1;letter-spacing:2px}}}}
  @keyframes {uid}-cl   {{from{{transform:translateX(-115%);opacity:0}}to{{transform:translateX(0);opacity:1}}}}
  @keyframes {uid}-cr   {{from{{transform:translateX(115%);opacity:0}}to{{transform:translateX(0);opacity:1}}}}
  @keyframes {uid}-rl   {{from{{opacity:0;transform:translateY(-50%) translateX(-36px)}}
                          to{{opacity:.18;transform:translateY(-50%) translateX(0)}}}}
  @keyframes {uid}-rr   {{from{{opacity:0;transform:translateY(-50%) translateX(36px)}}
                          to{{opacity:.18;transform:translateY(-50%) translateX(0)}}}}
  @keyframes {uid}-pulse{{0%,100%{{text-shadow:0 0 10px {c}88,2px 2px 0 #000}}
                          50%{{text-shadow:0 0 32px {c},0 0 64px {c}55,2px 2px 0 #000}}}}
  {spark_css}
</style>
<div style="position:relative;overflow:hidden;background:{cfg['bg']};
  border:2px solid {c};border-radius:6px;max-width:840px;margin:14px 0;
  box-shadow:0 0 55px {c}44,0 0 110px {c}11,0 12px 50px rgba(0,0,0,.97);">

  <div style="position:absolute;top:14px;left:14px;z-index:16;">{self._logo_tag_sm}</div>

  <div style="position:absolute;inset:0;background:{c};border-radius:4px;
    animation:{uid}-flash .55s ease-out forwards;pointer-events:none;z-index:20;"></div>

  <div style="position:absolute;top:50%;left:50%;width:90px;height:90px;margin:-45px;
    border-radius:50%;border:3px solid {rc};opacity:0;
    animation:{uid}-ring 1.05s ease-out .04s forwards;pointer-events:none;z-index:8;"></div>
  <div style="position:absolute;top:50%;left:50%;width:90px;height:90px;margin:-45px;
    border-radius:50%;border:2px solid {sc}cc;opacity:0;
    animation:{uid}-ring 1.35s ease-out .26s forwards;pointer-events:none;z-index:8;"></div>
  <div style="position:absolute;top:50%;left:50%;width:90px;height:90px;margin:-45px;
    border-radius:50%;border:1px solid {c}55;opacity:0;
    animation:{uid}-ring 1.65s ease-out .48s forwards;pointer-events:none;z-index:8;"></div>
  {extra_ring}

  {spark_html}

  <div style="position:absolute;left:14px;top:50%;
    font-size:15px;letter-spacing:5px;
    animation:{uid}-rl .9s ease-out .6s both;pointer-events:none;z-index:7;">
    🧭 🗺️ 🧭 🗺️ 🧭</div>
  <div style="position:absolute;right:14px;top:50%;
    font-size:15px;letter-spacing:5px;
    animation:{uid}-rr .9s ease-out .6s both;pointer-events:none;z-index:7;">
    🧭 🗺️ 🧭 🗺️ 🧭</div>

  <div style="position:relative;z-index:15;padding:42px 60px 32px;text-align:center;">

    <div style="font-size:54px;margin-bottom:16px;display:block;
      animation:{uid}-icon .68s cubic-bezier(.34,1.56,.64,1) .15s both;">
      {cfg['icon']}</div>

    <div style="font-family:'Press Start 2P',monospace;font-size:9px;color:{c};
      letter-spacing:4px;margin-bottom:20px;
      animation:{uid}-slam .52s cubic-bezier(.22,.61,.36,1) .38s both;">
      ¡SUBISTE DE NIVEL!</div>

    <div style="font-family:'Press Start 2P',monospace;
      font-size:clamp(12px,2.6vw,20px);color:{c};letter-spacing:3px;margin-bottom:18px;
      text-shadow:0 0 20px {c}88,2px 2px 0 #000;
      animation:{uid}-rise .55s ease-out .72s both,
                {uid}-pulse 2.8s ease-in-out 1.3s infinite;">
      {lvl_name}</div>

    <div style="font-family:'Press Start 2P',monospace;font-size:7px;
      color:#7a72a0;letter-spacing:2px;
      animation:{uid}-sub .5s ease-out 1.0s both;">{cfg['sub']}</div>

    <div style="display:flex;align-items:center;margin-top:26px;overflow:hidden;">
      <div style="font-size:13px;color:{c};opacity:.4;letter-spacing:-3px;flex-shrink:0;
        animation:{uid}-cl .6s ease-out .92s both;">◆◆◆◆◆</div>
      <div style="flex:1;height:1px;background:linear-gradient(90deg,{c}60,{c}10);margin:0 8px;"></div>
      <div style="font-family:'Press Start 2P',monospace;font-size:8px;color:{c};opacity:.65;
        animation:{uid}-rise .4s ease-out 1.1s both;">LV {lvl_num}</div>
      <div style="flex:1;height:1px;background:linear-gradient(90deg,{c}10,{c}60);margin:0 8px;"></div>
      <div style="font-size:13px;color:{c};opacity:.4;letter-spacing:-3px;flex-shrink:0;
        animation:{uid}-cr .6s ease-out .92s both;">◆◆◆◆◆</div>
    </div>
  </div>
</div>'''

    # ── Checkpoint summary ───────────────────────────────────

    def _render_checkpoint(self, title, seccion, color):
        rows = ""
        total_e = total_p = 0
        for key, (label, max_p) in seccion.items():
            e, p = self._scores.get(key, (0, max_p))
            total_e += e; total_p += p
            ok = e == p
            bar_w = round(60 * e / p) if p else 0
            rows += (
                f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">'
                f'<span style="font-size:12px;">{"✅" if ok else "⬜"}</span>'
                f'<div style="flex:1;">'
                f'<div style="font-size:11px;color:#ece8f8;margin-bottom:3px;">{label}</div>'
                f'<div style="height:5px;background:#1a1710;border-radius:2px;overflow:hidden;">'
                f'<div style="width:{bar_w * 100 // 60}%;height:100%;'
                f'background:{color};opacity:.85;border-radius:2px;"></div></div>'
                f'</div>'
                f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;'
                f'color:{color if ok else "#7a72a0"};">{e}/{p}</span>'
                f'</div>'
            )
        pct_sec = round(total_e / total_p * 100) if total_p else 0
        display(HTML(
            f'<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">'
            f'<div style="background:#0c0a16;border:2px solid {color};border-radius:4px;'
            f'max-width:840px;margin:10px 0;padding:18px 20px;'
            f'box-shadow:0 0 20px {color}22,0 4px 16px rgba(0,0,0,.6);">'
            f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:16px;">'
            f'{self._logo_tag_sm}'
            f'<span style="font-family:\'Press Start 2P\',monospace;font-size:9px;'
            f'color:{color};letter-spacing:2px;">✨ {title}</span></div>'
            f'{rows}'
            f'<div style="margin-top:14px;padding-top:10px;border-top:1px solid {color}30;'
            f'display:flex;justify-content:space-between;align-items:center;">'
            f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;color:#948cc0;">'
            f'SECCIÓN: {total_e}/{total_p} XP</span>'
            f'<span style="font-family:\'Press Start 2P\',monospace;font-size:9px;color:{color};">'
            f'{pct_sec}%</span>'
            f'</div></div>'
        ))

    # ── Supabase submit ───────────────────────────────────────

    def _submit_to_supabase(self, earned, possible, pct, lvl_num, lvl_name, silent=False):
        if DEADLINE_PASSED:
            return
        if not self._dni:
            return
        try:
            import json as _json, urllib.request as _ur
            payload = _json.dumps({
                "email":           self._dni,
                "dni":             self._dni,
                "nombre":          self._nombre_real or "cartógrafo",
                "grado":           self._grado or "",
                "curso":           CURSO_ID,
                "notebook":        NOTEBOOK_ID,
                "earned":          earned,
                "possible":        possible,
                "pct":             pct,
                "level_num":       lvl_num,
                "level_name":      lvl_name,
                "achievements":    list(self._achievements),
                "streak":          self._streak,
                # 2026-09-14: las celdas de registro (reg_*, ver esa seccion
                # mas abajo) meten el texto crudo del alumno aca -- columna
                # JSON, no requiere migracion -- para poder revisarlo por SQL
                # sin abrir cada notebook individualmente.
                "score_breakdown": {
                    k: ({"e": e, "p": p, "text": self._text_answers[k]}
                        if k in self._text_answers else {"e": e, "p": p})
                    for k, (e, p) in self._scores.items()
                },
            }).encode("utf-8")
            req = _ur.Request(
                f"{SUPABASE_URL}/rest/v1/submissions",
                data=payload,
                headers={
                    "apikey":        SUPABASE_ANON_KEY,
                    "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
                    "Content-Type":  "application/json",
                    "Prefer":        "return=minimal",
                },
                method="POST",
            )
            with _ur.urlopen(req, timeout=12):
                pass
            if not silent:
                display(HTML(
                    f'<div style="display:flex;align-items:center;gap:8px;'
                    f'font-family:\'Press Start 2P\',monospace;font-size:8px;'
                    f'color:#4caf50;background:#020d02;border:1px solid #4caf50;'
                    f'border-radius:3px;padding:10px 16px;max-width:840px;margin-top:6px;">'
                    f'{self._logo_tag_sm}'
                    f'<span>✅ SCORE ENVIADO — {self._nombre_real} · DNI {self._dni}'
                    f'<br><span style="color:#52b788;font-size:7px;">'
                    f'📊 Calificación actualizada en la base de datos</span></span></div>'
                ))
        except Exception as _ex:
            if not silent:
                display(HTML(
                    f'<div style="display:flex;align-items:center;gap:8px;'
                    f'font-family:\'Press Start 2P\',monospace;font-size:7px;'
                    f'color:#ff5d5d;background:#1a0005;border:1px solid #ff5d5d;'
                    f'border-radius:3px;padding:10px 16px;max-width:840px;margin-top:6px;">'
                    f'{self._logo_tag_sm}'
                    f'<span>⚠️ Leaderboard no disponible: {_ex}</span></div>'
                ))

    # ═══════════════════════════════════════════════════════════
    # REGISTRO — 🔮 PREDICE / 📝 ANOTA: texto corto de participación
    # (+1 XP c/u, sin IA, sin respuesta incorrecta) — mismo widget que nb5
    # (autograder_nb5.py, sección REGISTRO), reusado verbatim: el texto
    # crudo viaja dentro de `score_breakdown` en `submissions` (columna
    # JSON, no requiere migración) para poder revisarlo por SQL sin entrar
    # a cada Colab.
    # ═══════════════════════════════════════════════════════════

    def _show_registro_locked(self, id):
        """Registro ya enviado -- no se permite un segundo intento."""
        key = f"reg_{id}"
        pts, max_pts = self._scores[key]
        color = "#4caf50" if pts == max_pts else "#ff5d5d"
        display(HTML(
            f'<div style="max-width:840px;margin:10px 0;background:#0c0a16;'
            f'border:2px solid {color};border-radius:4px;padding:14px 18px;'
            f'font-family:\'Segoe UI\',Roboto,sans-serif;">'
            f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">'
            f'{self._logo_tag_sm}'
            f'<span style="font-family:\'Press Start 2P\',monospace;font-size:9px;'
            f'color:#b0a8d0;letter-spacing:1px;">'
            f'🔒 YA REGISTRADO</span></div>'
            f'<div style="color:{color};font-size:13px;">'
            f'Ya enviaste tu respuesta ({pts}/{max_pts} XP)</div>'
            f'<div style="color:#b0a8d0;font-size:12px;margin-top:6px;">'
            f'Esta celda admite un solo envío. Volver a ejecutarla no '
            f'genera un nuevo intento.</div></div>'
        ))

    def _grade_registro(self, id, text):
        key = f"reg_{id}"
        if key in self._scores:
            self._show_registro_locked(id)
            return
        ok = _is_nontrivial_text(text, min_len=3)
        self._text_answers[key] = text if isinstance(text, str) else ""
        self._award_registro(key, 1 if ok else 0, 1, ok)

    def _ask_registro(self, id, question, icon="🔮", label="PREDICE"):
        key = f"reg_{id}"
        if key in self._scores:
            self._show_registro_locked(id)
            return
        try:
            from google.colab import output as _out  # noqa: F401  (solo para confirmar entorno Colab)
            import random as _r
            uid = f"rg_{id}_{_r.randint(10000, 99999)}"

            display(HTML(f'''
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<div id="{uid}-wrap" style="background:#0c0a16;border:2px solid #52b788;border-radius:4px;
  max-width:840px;margin:10px 0;overflow:hidden;box-shadow:0 6px 24px rgba(0,0,0,.7);">
  <div style="background:#52b78818;border-bottom:1px solid #52b78840;padding:10px 16px;
    display:flex;align-items:center;gap:8px;">
    {self._logo_tag_sm}
    <span style="font-family:'Press Start 2P',monospace;font-size:9px;color:#52b788;
      letter-spacing:1px;">{icon} {label}</span>
  </div>
  <div style="padding:16px 18px;">
    <div style="color:#ece8f8;font-size:13px;line-height:1.6;margin-bottom:14px;">{question}</div>
    <textarea id="{uid}-text" rows="2" placeholder="Escribe aquí -- no hay respuesta incorrecta..."
      style="width:100%;box-sizing:border-box;background:#171130;border:2px solid #52b788;
      border-radius:4px;color:#ece8f8;font-family:'Segoe UI',Roboto,sans-serif;
      font-size:13px;padding:10px 12px;resize:vertical;"></textarea>
    <button id="{uid}-btn" onclick="{uid}_submit()"
      style="margin-top:10px;padding:10px 20px;background:#52b788;border:none;
      border-radius:4px;color:#0f0c1e;font-family:'Press Start 2P',monospace;
      font-size:9px;cursor:pointer;">ENVIAR ✉️</button>
    <div id="{uid}-status" style="margin-top:10px;font-size:12px;color:#b0a8d0;"></div>
  </div>
</div>
<script>
async function {uid}_submit() {{
  var ta = document.getElementById('{uid}-text');
  var btn = document.getElementById('{uid}-btn');
  var status = document.getElementById('{uid}-status');
  var text = ta.value;
  ta.disabled = true;
  btn.disabled = true;
  btn.style.opacity = '0.5';
  btn.style.cursor = 'not-allowed';
  status.innerHTML = '⏳ Registrando...';
  await google.colab.kernel.invokeFunction('_ag_registro_answer', ['{id}', text], {{}});
  status.innerHTML = '';
}}
</script>
'''))
        except ImportError:
            print(f"{icon} {label}\n{question}\n")
            text = input("Tu respuesta: ").strip()
            self._grade_registro(id, text)

    def _award_registro(self, key, pts, max_pts, ok):
        """Hermano liviano de _award_reflexion() -- sin comentario de IA,
        solo confirma el envío y otorga el XP de participación."""
        self._scores[key] = (pts, max_pts)

        earned, possible, pct = self._totals()
        lvl_num, lvl_name     = _level_info(pct)

        import threading as _thr
        _thr.Thread(
            target=self._submit_to_supabase,
            args=(earned, possible, pct, lvl_num, lvl_name, True),
            daemon=True,
        ).start()

        if ok:
            color, icon2, msg = "#4caf50", "✅", f"¡Registrado! +{pts} XP"
        else:
            color, icon2, msg = ("#ff5d5d", "🌥️",
                                  "Escribe una respuesta real antes de enviar -- no dejes el cuadro vacío ni un placeholder")

        display(HTML(
            f'<div style="max-width:840px;margin:10px 0 14px;background:#0c0a16;'
            f'border:2px solid {color};border-radius:4px;padding:12px 16px;'
            f'font-family:\'Segoe UI\',Roboto,sans-serif;display:flex;align-items:center;gap:10px;">'
            f'<span style="font-size:16px;">{icon2}</span>'
            f'<span style="color:{color};font-size:13px;">{msg}</span></div>'
        ))

    def check_cuantos_grupos(self):
        """Predicción rápida sobre el scatter sin etiquetar del inicio -- participación (+1 XP), sin IA"""
        return self._ask_registro(
            "cuantos_grupos",
            '¿Cuántos grupos crees que hay en este scatter? Escribe tu predicción en una frase '
            '-- no hay respuesta incorrecta, todavía nadie lo sabe con certeza.',
            icon="🔮", label="PREDICE")

    def check_como_agrupa(self):
        """En tus propias palabras -- cómo decide k-means a qué grupo pertenece un punto (+1 XP), sin IA"""
        return self._ask_registro(
            "como_agrupa",
            'En tus propias palabras: ¿cómo crees que k-means decide a qué grupo pertenece cada punto?',
            icon="📝", label="ANOTA")

    # ═══════════════════════════════════════════════════════════
    # TEORÍA — check_t1..check_t5 (formulario interactivo HTML)
    # ═══════════════════════════════════════════════════════════

    _TEORIA = {
        1: dict(
            title="T1 — ¿Qué hace k-means, en el fondo?",
            q=("Le pides a k-means que agrupe tus datos en k=3 grupos. En términos simples, "
               "¿qué hace el algoritmo para decidir a qué grupo pertenece cada punto?"),
            opts={"a": "Ordena los puntos por su primera columna y los corta en 3 partes iguales",
                  "b": "Coloca 3 centroides (puntos promedio), asigna cada punto al centroide más cercano, recalcula los centroides como el promedio de sus puntos, y repite hasta que las asignaciones casi no cambian",
                  "c": "Usa una columna de categorías reales (como el género de la canción) para separar los puntos en 3 grupos conocidos",
                  "d": "Calcula la correlación entre todas las columnas y agrupa las que correlacionan más entre sí"},
            correct="b",
            why=("k-means no usa ninguna etiqueta real -- solo la posición de los puntos. "
                 "Coloca k centroides, asigna cada punto al más cercano, recalcula cada "
                 "centroide como el promedio de sus puntos asignados, y repite hasta que las "
                 "asignaciones dejan de cambiar."),
            pts=5,
        ),
        2: dict(
            title="T2 — Por qué escalar antes de ajustar",
            q=("Ajustas k-means SIN escalar sobre `Bailabilidad` (rango 0 a 1) y `Tempo` "
               "(rango ≈30-243 BPM). Los 3 clusters resultantes terminan separados casi solo "
               "por `Tempo`, con `Bailabilidad` influyendo muy poco. ¿Por qué?"),
            opts={"a": "Bailabilidad no tiene ninguna relación real con Tempo, así que el algoritmo la descarta a propósito",
                  "b": "k-means mide distancia entre puntos -- una diferencia de 50 BPM ya vale 50, mientras que la diferencia máxima posible de Bailabilidad es 1, así que la distancia total queda dominada casi por completo por la escala de Tempo",
                  "c": "El dataset tiene un error y Bailabilidad quedó con puros ceros",
                  "d": "k-means siempre prioriza la primera columna que se le pasa, sin importar su escala"},
            correct="b",
            why=("k-means no sabe qué unidad tiene cada columna -- solo ve números y calcula "
                 "distancias. Si una columna vive en el rango de las decenas/cientos (Tempo) y "
                 "otra en el rango 0-1 (Bailabilidad), la de escala más grande domina la "
                 "distancia casi por completo. Escalar (ej. StandardScaler) pone a todas las "
                 "variables en la misma escala antes de calcular esa distancia."),
            pts=5,
        ),
        3: dict(
            title="T3 — Por qué las etiquetas de cluster son arbitrarias",
            q=("Ajustas k-means dos veces sobre los mismos datos y la misma k, en dos "
               "computadoras distintas. Los grupos de canciones que quedan juntos son "
               "básicamente los mismos -- pero el grupo de canciones \"muy bailables\" se "
               "llama cluster 2 la primera vez y cluster 0 la segunda. ¿Qué te dice esto?"),
            opts={"a": "Uno de los dos ajustes está mal hecho -- el número de cluster debería ser siempre el mismo",
                  "b": "El número que k-means le pone a cada grupo (0, 1, 2...) es solo una etiqueta interna sin significado propio -- lo que importa es qué puntos quedaron juntos y sus centroides, no el índice que les tocó",
                  "c": "Los datos cambiaron entre una corrida y otra",
                  "d": "Esto solo pasa si k está mal elegido"},
            correct="b",
            why=("k-means no sabe qué \"significa\" cada grupo -- simplemente les asigna un "
                 "número en el orden en que los encuentra, y ese número puede cambiar entre "
                 "corridas, versiones de la librería o inicializaciones distintas. Lo único con "
                 "significado real son los puntos agrupados y sus centroides -- nunca el índice."),
            pts=5,
        ),
        4: dict(
            title="T4 — Sensibilidad a k y a la inicialización",
            q=("Ajustas k-means con k=3 y luego con k=5 sobre el mismo dataset. Los grupos "
               "resultantes son distintos -- no es que k=5 simplemente \"subdivida\" los "
               "mismos 3 grupos de antes. ¿Qué explica mejor esto?"),
            opts={"a": "k-means recalcula la agrupación completa para cada valor de k -- no hay garantía de que los grupos de k=3 estén \"contenidos\" dentro de los de k=5",
                  "b": "Es un error -- k=5 siempre debería ser un refinamiento exacto de k=3",
                  "c": "k no afecta el resultado, solo cuántos colores se usan al graficar",
                  "d": "Esto solo pasa si el dataset tiene outliers"},
            correct="a",
            why=("k-means es sensible tanto al valor de k como a dónde arrancan los centroides "
                 "iniciales -- cambiar k cambia el problema de optimización completo, no solo "
                 "\"subdivide\" el resultado anterior. Por eso probar más de un k es parte "
                 "normal de usar k-means, no un síntoma de que algo salió mal."),
            pts=5,
        ),
        5: dict(
            title="T5 — ¿Qué es un centroide?",
            q=("Tu modelo de k-means (features `Bailabilidad` y `Tempo`, ya escalados) te da "
               "un centroide para uno de sus clusters. ¿Qué representa ese centroide?"),
            opts={"a": "La canción real más cercana al centro de ese grupo",
                  "b": "El punto promedio (uno por cada feature) de todas las canciones asignadas a ese cluster -- no corresponde necesariamente a ninguna canción real",
                  "c": "La canción más popular dentro de ese cluster",
                  "d": "La primera canción que k-means asignó a ese cluster"},
            correct="b",
            why=("El centroide es un promedio matemático de las coordenadas de todos los "
                 "puntos del cluster, en la escala en que se ajustó el modelo. Es un resumen "
                 "del grupo, no necesariamente un punto de datos real -- para interpretarlo en "
                 "unidades reales hay que compararlo contra los rangos originales de esas "
                 "columnas."),
            pts=5,
        ),
    }

    def _show_teoria_locked(self, n):
        """Pregunta ya respondida -- no se permite una segunda respuesta."""
        spec = self._TEORIA[int(n)]
        pts, max_pts = self._scores[f"t{int(n)}"]
        ok = pts == max_pts
        color = "#4caf50" if ok else "#ff5d5d"
        estado = (f"✅ Ya respondiste correctamente ({pts}/{max_pts} pts)" if ok
                  else f"❌ Ya respondiste esta pregunta ({pts}/{max_pts} pts)")
        display(HTML(
            f'<div style="max-width:840px;margin:10px 0;background:#0c0a16;'
            f'border:2px solid {color};border-radius:4px;padding:14px 18px;'
            f'font-family:\'Segoe UI\',Roboto,sans-serif;">'
            f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">'
            f'{self._logo_tag_sm}'
            f'<span style="font-family:\'Press Start 2P\',monospace;font-size:9px;'
            f'color:#b0a8d0;letter-spacing:1px;">'
            f'🔒 {spec["title"]} — YA RESPONDIDA</span></div>'
            f'<div style="color:{color};font-size:13px;">{estado}</div>'
            f'<div style="color:#b0a8d0;font-size:12px;margin-top:6px;">'
            f'Esta pregunta admite una sola respuesta. Volver a ejecutar la celda no '
            f'genera un nuevo intento.</div></div>'
        ))

    def _grade_teoria(self, n, letter):
        spec = self._TEORIA[int(n)]
        key = f"t{int(n)}"
        if key in self._scores:
            self._show_teoria_locked(n)
            return
        letter = (letter or "").strip().lower()
        ok = letter == spec["correct"]
        self._header(f"❓ {spec['title']}", icon="❓", pts=spec["pts"])
        if ok:
            checks = [(True, f"Respuesta: {letter.upper()})", f"¡Correcto! {spec['why']}")]
        else:
            correct_txt = spec["opts"][spec["correct"]]
            given = letter.upper() if letter in ("a", "b", "c", "d") else "(sin responder)"
            checks = [(False, f"Respuesta: {given}",
                       f"La correcta era {spec['correct'].upper()}) {correct_txt} — {spec['why']}")]
        return self._award(f"t{n}", checks, spec["pts"])

    def _ask_teoria(self, n):
        spec = self._TEORIA[n]
        if f"t{n}" in self._scores:
            self._show_teoria_locked(n)
            return
        try:
            from google.colab import output as _out  # noqa: F401  (solo para confirmar entorno Colab)
            import random as _r
            uid = f"tq{n}_{_r.randint(10000, 99999)}"

            opts_html = ""
            for L in ("a", "b", "c", "d"):
                opts_html += (
                    f'<button id="{uid}-{L}" class="{uid}-opt" onclick="{uid}_pick(\'{L}\')" '
                    f'style="display:block;width:100%;text-align:left;padding:12px 16px;'
                    f'margin-bottom:8px;background:#171130;border:2px solid #52b788;'
                    f'border-radius:4px;color:#ece8f8;font-family:\'Segoe UI\',Roboto,sans-serif;'
                    f'font-size:13px;cursor:pointer;transition:all .15s;">'
                    f'<span style="font-family:\'Press Start 2P\',monospace;font-size:9px;'
                    f'color:#e9c46a;margin-right:10px;">{L.upper()}</span>{spec["opts"][L]}</button>'
                )

            display(HTML(f'''
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
  .{uid}-opt:hover {{ border-color:#e9c46a !important; background:#1e1a0c !important; }}
</style>
<div id="{uid}-wrap" style="background:#0c0a16;border:2px solid #52b788;border-radius:4px;
  max-width:840px;margin:10px 0;overflow:hidden;box-shadow:0 6px 24px rgba(0,0,0,.7);">
  <div style="background:#52b78818;border-bottom:1px solid #52b78840;padding:10px 16px;
    display:flex;align-items:center;gap:8px;">
    {self._logo_tag_sm}
    <span style="font-family:'Press Start 2P',monospace;font-size:9px;color:#52b788;
      letter-spacing:1px;">❓ {spec['title']}</span>
  </div>
  <div style="padding:16px 18px;">
    <div style="color:#ece8f8;font-size:13px;line-height:1.6;margin-bottom:16px;">{spec['q']}</div>
    {opts_html}
  </div>
</div>
<script>
async function {uid}_pick(letter) {{
  var opts = document.querySelectorAll('.{uid}-opt');
  opts.forEach(function(b) {{ b.style.pointerEvents = 'none'; b.style.opacity = '0.55'; }});
  var chosen = document.getElementById('{uid}-' + letter);
  if (chosen) {{
    chosen.style.opacity = '1';
    chosen.style.borderColor = '#e9c46a';
    chosen.style.background = '#1e1a0c';
  }}
  await google.colab.kernel.invokeFunction('_ag_teoria_answer', [{n}, letter], {{}});
}}
</script>
'''))
        except ImportError:
            print(f"❓ {spec['title']}\n{spec['q']}\n")
            for L in ("a", "b", "c", "d"):
                print(f"  {L}) {spec['opts'][L]}")
            ans = input("Tu respuesta (a/b/c/d): ").strip().lower()
            self._grade_teoria(n, ans)

    def check_t1(self): return self._ask_teoria(1)
    def check_t2(self): return self._ask_teoria(2)
    def check_t3(self): return self._ask_teoria(3)
    def check_t4(self): return self._ask_teoria(4)
    def check_t5(self): return self._ask_teoria(5)

    # ═══════════════════════════════════════════════════════════
    # REFLEXIÓN — 💭 calificada por IA (DeepSeek vía Supabase Edge Function)
    # ═══════════════════════════════════════════════════════════

    def _call_grade_reflexion(self, reflexion_id, text):
        """POST a la funcion Edge grade-reflexion. Devuelve (score, comment)
        en exito, None en CUALQUIER fallo (red, timeout, respuesta con forma
        invalida) -- el caller nunca debe interpretar None como "el alumno
        saco 0", solo como "no se pudo calificar, que reintente".

        2026-08-24: timeout subido de 15s a 55s tras diagnosticar 502s en
        vivo durante clase (ver WORKFORCE_HANDOFF.md) -- la funcion Edge
        ahora reintenta una vez contra DeepSeek con timeout de 20s por
        intento + 1.5s de pausa (peor caso ~41.5s), asi que un timeout
        cliente de 15s la cortaba antes de que su propio reintento pudiera
        terminar. 55s deja margen sobre ese peor caso.

        2026-08-24 (mismo diagnostico): la causa raiz de esos 502 no era la
        funcion en si, sino que toda la clase hace clic en "Enviar" casi al
        mismo segundo (mismo ritmo de leccion, misma DEEPSEEK_API_KEY
        compartida) -- una ráfaga sincronizada, no trafico parejo. Un jitter
        aleatorio de 0-3s antes de disparar el POST desincroniza esa ráfaga
        sin coordinacion entre kernels (cada notebook es un proceso
        independiente): mismo alumno, misma espera percibida (~3s extra
        sobre una llamada que igual toma varios segundos), pero la ventana
        de solicitudes simultaneas contra DeepSeek se reparte en vez de
        llegar toda junta."""
        try:
            import json as _json, random as _rnd, time as _time, urllib.request as _ur
            _time.sleep(_rnd.uniform(0, 3))
            payload = _json.dumps({
                "dni":          self._dni,
                "notebook":     NOTEBOOK_ID,
                "curso":        CURSO_ID,
                "reflexion_id": reflexion_id,
                "student_text": text,
                "grado":        self._grado or "",
            }).encode("utf-8")
            req = _ur.Request(
                GRADE_REFLEXION_URL,
                data=payload,
                headers={
                    "apikey":        SUPABASE_ANON_KEY,
                    "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
                    "Content-Type":  "application/json",
                },
                method="POST",
            )
            with _ur.urlopen(req, timeout=55) as resp:
                data = _json.loads(resp.read().decode("utf-8"))
            score, comment = data.get("score"), data.get("comment")
            if not isinstance(score, int) or not isinstance(comment, str) or not comment.strip():
                return None
            return score, comment
        except Exception:
            return None

    def _show_reflexion_locked(self, id):
        """Reflexion ya respondida -- no se permite un segundo intento."""
        key = f"refl_{id}"
        pts, max_pts = self._scores[key]
        color = "#4caf50" if pts == max_pts else ("#e9c46a" if pts > 0 else "#ff5d5d")
        display(HTML(
            f'<div style="max-width:840px;margin:10px 0;background:#0c0a16;'
            f'border:2px solid {color};border-radius:4px;padding:14px 18px;'
            f'font-family:\'Segoe UI\',Roboto,sans-serif;">'
            f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">'
            f'{self._logo_tag_sm}'
            f'<span style="font-family:\'Press Start 2P\',monospace;font-size:9px;'
            f'color:#b0a8d0;letter-spacing:1px;">'
            f'🔒 💭 REFLEXIONA — YA RESPONDIDA</span></div>'
            f'<div style="color:{color};font-size:13px;">'
            f'Ya enviaste tu reflexión ({pts}/{max_pts} pts)</div>'
            f'<div style="color:#b0a8d0;font-size:12px;margin-top:6px;">'
            f'Esta celda admite una sola respuesta. Volver a ejecutar la celda no '
            f'genera un nuevo intento.</div></div>'
        ))

    def _grade_reflexion(self, id, text):
        key = f"refl_{id}"
        if key in self._scores:
            self._show_reflexion_locked(id)
            return

        if not _is_nontrivial_text(text):
            self._award_reflexion(
                key, 0, _REFLEXION_PTS,
                "Escribe una reflexión real de 1-2 oraciones -- no dejes el "
                "placeholder \"___\" ni una respuesta de una sola palabra."
            )
            return

        result = self._call_grade_reflexion(id, text)
        if result is None:
            display(HTML(
                '<div style="max-width:840px;margin:10px 0;background:#0c0a16;'
                'border:2px solid #95d5b2;border-radius:4px;padding:14px 18px;'
                'font-family:\'Segoe UI\',Roboto,sans-serif;">'
                '<div style="font-family:\'Press Start 2P\',monospace;font-size:9px;'
                'color:#95d5b2;letter-spacing:1px;margin-bottom:8px;">'
                '⏳ NO SE PUDO CALIFICAR</div>'
                '<div style="color:#ece8f8;font-size:13px;">'
                'No pudimos calificar tu reflexión ahora mismo (problema de conexión). '
                'Vuelve a ejecutar esta celda para intentar de nuevo -- tu respuesta no '
                'se perdió ni se calificó con 0.</div></div>'
            ))
            return

        score, comment = result
        score = max(0, min(_REFLEXION_PTS, int(round(score))))
        self._award_reflexion(key, score, _REFLEXION_PTS, comment)

    def _ask_reflexion(self, id, question):
        key = f"refl_{id}"
        if key in self._scores:
            self._show_reflexion_locked(id)
            return
        try:
            from google.colab import output as _out  # noqa: F401  (solo para confirmar entorno Colab)
            import random as _r
            uid = f"rq_{id}_{_r.randint(10000, 99999)}"

            display(HTML(f'''
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<div id="{uid}-wrap" style="background:#0c0a16;border:2px solid #52b788;border-radius:4px;
  max-width:840px;margin:10px 0;overflow:hidden;box-shadow:0 6px 24px rgba(0,0,0,.7);">
  <div style="background:#52b78818;border-bottom:1px solid #52b78840;padding:10px 16px;
    display:flex;align-items:center;gap:8px;">
    {self._logo_tag_sm}
    <span style="font-family:'Press Start 2P',monospace;font-size:9px;color:#52b788;
      letter-spacing:1px;">💭 REFLEXIONA</span>
  </div>
  <div style="padding:16px 18px;">
    <div style="color:#ece8f8;font-size:13px;line-height:1.6;margin-bottom:14px;">{question}</div>
    <textarea id="{uid}-text" rows="3" placeholder="Escribe tu reflexión aquí..."
      style="width:100%;box-sizing:border-box;background:#171130;border:2px solid #52b788;
      border-radius:4px;color:#ece8f8;font-family:'Segoe UI',Roboto,sans-serif;
      font-size:13px;padding:10px 12px;resize:vertical;"></textarea>
    <button id="{uid}-btn" onclick="{uid}_submit()"
      style="margin-top:10px;padding:10px 20px;background:#52b788;border:none;
      border-radius:4px;color:#0f0c1e;font-family:'Press Start 2P',monospace;
      font-size:9px;cursor:pointer;">ENVIAR ✉️</button>
    <div id="{uid}-status" style="margin-top:10px;font-size:12px;color:#b0a8d0;"></div>
  </div>
</div>
<script>
async function {uid}_submit() {{
  var ta = document.getElementById('{uid}-text');
  var btn = document.getElementById('{uid}-btn');
  var status = document.getElementById('{uid}-status');
  var text = ta.value;
  ta.disabled = true;
  btn.disabled = true;
  btn.style.opacity = '0.5';
  btn.style.cursor = 'not-allowed';
  status.innerHTML = '⏳ Calificando...';
  await google.colab.kernel.invokeFunction('_ag_reflexion_answer', ['{id}', text], {{}});
  status.innerHTML = '';
}}
</script>
'''))
        except ImportError:
            print(f"💭 REFLEXIONA\n{question}\n")
            text = input("Tu reflexión: ").strip()
            self._grade_reflexion(id, text)

    def _award_reflexion(self, key, pts, max_pts, comment):
        """Hermano de _award() para calificacion IA -- no reusa _award()
        directamente porque su motor de pts = round(max_pts * passed/len(checks))
        promedia sub-checks booleanos, y aca ya tenemos un puntaje numerico
        directo del LLM."""
        self._scores[key] = (pts, max_pts)

        earned, possible, pct = self._totals()
        lvl_num, lvl_name     = _level_info(pct)

        import threading as _thr
        _thr.Thread(
            target=self._submit_to_supabase,
            args=(earned, possible, pct, lvl_num, lvl_name, True),
            daemon=True,
        ).start()

        new_ach = self._check_achievements(key)
        reg_ach = [(n, c, r) for n, c, r in new_ach if r != "Nivel"]

        _RC = {
            "Boceto":      ("#3a5a40", "rgba(58,90,64,.14)",   "🌱"),
            "Trazo":       ("#52b788", "rgba(82,183,136,.12)", "🧭"),
            "Hallazgo":    ("#95d5b2", "rgba(149,213,178,.12)", "🗺️"),
            "Mapa Maestro": ("#f4a261", "rgba(244,162,97,.15)", "🏆"),
        }
        ach_html = ""
        for ach_name, _, ach_rarity in reg_ach:
            bc, bg, ach_icon = _RC.get(ach_rarity, _RC["Boceto"])
            ach_html += (
                f'<div style="display:flex;align-items:center;gap:10px;margin-top:8px;'
                f'padding:10px 12px;background:{bg};border:1px solid {bc};border-radius:3px;">'
                f'<span style="font-size:18px;">{ach_icon}</span>'
                f'<div style="flex:1;">'
                f'<div style="margin-bottom:3px;">'
                f'<span style="background:{bc};color:#0c0a16;font-size:7px;font-weight:bold;'
                f'padding:1px 5px;border-radius:2px;font-family:\'Press Start 2P\',monospace;">'
                f'{ach_rarity.upper()}</span>'
                f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;'
                f'color:{bc};margin-left:6px;">LOGRO DESBLOQUEADO</span>'
                f'</div>'
                f'<div style="color:#ece8f8;font-size:12px;font-weight:bold;">{ach_name}</div>'
                f'</div></div>'
            )

        if pts == max_pts:
            s_icon, s_text, s_color = "💭", f"¡REFLEXIÓN COMPLETA! +{pts} XP", "#4caf50"
            border_color, glow = "#4caf50", "0 0 22px rgba(76,175,80,.15)"
        elif pts > 0:
            s_icon, s_text, s_color = "💭", f"+{pts} XP  ·  {max_pts - pts} por profundizar", "#e9c46a"
            border_color, glow = "#95d5b2", "0 0 22px rgba(255,183,3,.12)"
        else:
            s_icon, s_text, s_color = "💭", "Sin XP esta vez — lee el comentario abajo", "#ff5d5d"
            border_color, glow = "#ff5d5d", "0 0 22px rgba(255,93,93,.15)"

        xp_grad = _XP_GRAD.get(lvl_num, _XP_GRAD[1])
        _core_pct_bar = min(round(earned / _CORE_MAX * 100), 100)
        xp_bar_html = (
            f'<div style="display:flex;justify-content:space-between;margin-bottom:4px;">'
            f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;color:#7a72a0;">'
            f'XP: {earned}/{_CORE_MAX}</span>'
            f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;'
            f'color:{_lv_color(lvl_num)};">{lvl_name}</span></div>'
            f'<div style="width:100%;height:10px;background:#191430;border:1px solid #241f3d;'
            f'border-radius:2px;overflow:hidden;">'
            f'<div style="width:{_core_pct_bar}%;height:100%;background:{xp_grad};'
            f'border-radius:2px;transform-origin:left;'
            f'animation:pg-xpscale 1.1s cubic-bezier(.4,0,.2,1) forwards;'
            f'box-shadow:0 0 6px rgba(255,209,102,.25);"></div></div>'
        )

        comment_html = (
            f'<div style="padding:10px 12px;margin:2px 0 8px;background:rgba(74,168,216,.06);'
            f'border-left:3px solid #52b788;border-radius:0 3px 3px 0;">'
            f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;color:#52b788;">'
            f'🤖 FEEDBACK</span>'
            f'<div style="color:#ece8f8;font-size:12px;line-height:1.6;margin-top:5px;">{comment}</div>'
            f'</div>'
        )

        deadline_html = ""
        if DEADLINE_PASSED:
            deadline_html = '''<div style="margin-top:10px;padding:12px 16px;background:#1a0000;
  border:2px solid #ff0000;border-radius:3px;text-align:center;">
  <div style="font-family:'Press Start 2P',monospace;font-size:10px;color:#ff0000;
    letter-spacing:2px;text-shadow:0 0 10px rgba(255,0,0,.6);">🚫 PLAZO VENCIDO</div>
  <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#ff8888;
    margin-top:6px;letter-spacing:1px;">TU NOTA NO SERÁ ACTUALIZADA</div>
  <div style="font-size:11px;color:#cc6666;margin-top:6px;">
    Puedes revisar tus respuestas, pero la entrega ya cerró.</div></div>'''
        elif self._dni:
            deadline_html = ('<div style="margin-top:8px;font-family:\'Press Start 2P\',monospace;'
                             'font-size:6px;color:#52b788;letter-spacing:1px;opacity:.85;">'
                             '📊 Calificación actualizada en la base de datos</div>')

        card_html = f'''<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
  @keyframes pg-xpscale{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
</style>
<div style="background:#0c0a16;border:2px solid {border_color};border-radius:4px;max-width:840px;
  margin-bottom:14px;overflow:hidden;box-shadow:{glow},0 6px 24px rgba(0,0,0,.7);
  font-family:'Segoe UI',Roboto,sans-serif;">
  <div style="background:{border_color}18;border-bottom:1px solid {border_color}40;
    padding:9px 16px;display:flex;justify-content:space-between;align-items:center;">
    <div style="display:flex;align-items:center;gap:8px;">
      {self._logo_tag_sm}
      <span style="font-family:'Press Start 2P',monospace;font-size:9px;
        color:{border_color};letter-spacing:1px;">💭 REFLEXIÓN CALIFICADA</span>
    </div>
    <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#f4a261;
      background:rgba(255,158,44,.1);border:1px solid rgba(255,158,44,.4);
      padding:3px 8px;border-radius:2px;">MAX {max_pts} XP</div>
  </div>
  <div style="padding:10px 14px 6px;">{comment_html}</div>
  <div style="background:#0f0c1e;border-top:1px solid #1a1710;padding:11px 14px;">
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:9px;">
      <span style="font-size:16px;">{s_icon}</span>
      <span style="font-family:'Press Start 2P',monospace;font-size:8px;
        color:{s_color};">{s_text}</span>
    </div>
    {xp_bar_html}
    {ach_html}
    {deadline_html}
  </div>
</div>'''
        display(HTML(card_html))

    # ═══════════════════════════════════════════════════════════
    # 🧩 COMPLETA — ¿los clusters corresponden a géneros reales?
    # (5 pts, ESTRUCTURAL, sin IA -- operacionaliza directamente el riesgo
    # de 04_GAUSS.md para la Semana 7: "interpretation text must not treat
    # cluster labels as fixed/meaningful IDs". La celda guiada anterior en
    # el notebook ya imprimió la tabla cluster×Género (ver docstring del
    # módulo: con 114 géneros reales, ningún género pasa de ~2.6% dentro de
    # un cluster -- apenas por encima del ≈0.9% que tocaría al azar), así
    # que la respuesta correcta es objetiva y verificable, no de opinión.
    # ═══════════════════════════════════════════════════════════

    def check_cluster_es_genero(self):
        """🧩 COMPLETA — ¿los clusters de k-means son géneros reales? (5 pts, estructural)"""
        self._header("🧩 ¿LOS CLUSTERS SON GÉNEROS?", icon="🧩", pts=5)
        checks = []
        respuesta    = _get("respuesta_cluster_es_genero")
        explicacion  = _get("explicacion_cluster_es_genero")

        r = _norm(respuesta) if isinstance(respuesta, str) else ""
        if respuesta is None or r == "":
            checks.append((False, "respuesta_cluster_es_genero",
                           "No definida — completa con 'si' o 'no' según la tabla cluster×Género de arriba"))
        elif r.startswith("no"):
            checks.append((True, "respuesta_cluster_es_genero = 'no'",
                           "✓  Correcto -- ningún cluster corresponde a un género real"))
        elif r.startswith("si"):
            checks.append((False, "respuesta_cluster_es_genero",
                           "Revisa la tabla cluster×Género que imprimiste arriba: con 114 géneros reales, ninguno pasa de ~2.6% dentro de un cluster -- la respuesta correcta es 'no'"))
        else:
            checks.append((False, "respuesta_cluster_es_genero",
                           f"'{respuesta}' no es una respuesta reconocida -- completa con 'si' o 'no'"))

        if not _is_nontrivial_text(explicacion, min_len=10):
            checks.append((False, "explicacion_cluster_es_genero",
                           "Escribe 1 frase citando un número de la tabla que imprimiste arriba (ej. el % del género más común dentro de un cluster)"))
        elif not any(ch.isdigit() for ch in explicacion):
            checks.append((False, "explicacion_cluster_es_genero",
                           "Cita al menos un número de la tabla cluster×Género (ej. un porcentaje) -- no una afirmación genérica"))
        else:
            checks.append((True, "explicacion_cluster_es_genero", "✓  Explicación con un número real de la tabla"))

        return self._award("cluster_es_genero", checks, 5)

    # ═══════════════════════════════════════════════════════════
    # EJERCICIO 1 — Traza tu primer mapa (2 predictores, k=3, escalado)
    # ═══════════════════════════════════════════════════════════

    def check_ex1(self):
        """Ex1 — k-means propio: agrupar canciones con 2 o 3 predictores + interpretar un centroide (40 pts)"""
        self._header("EJERCICIO 1 — Traza tu Mapa 🗺️", icon="🗺️", pts=40)
        checks = []
        predictores_ex1     = _get("predictores_ex1")
        modelo_ex1          = _get("modelo_ex1")
        cluster_interes_ex1 = _get("cluster_interes_ex1")
        interpretacion_ex1  = _get("interpretacion_ex1")

        combo = _predictores_normalizados(predictores_ex1, min_n=2, max_n=3) if predictores_ex1 is not None else None

        if predictores_ex1 is None:
            checks.append((False, "predictores_ex1",
                           "No definida — usa una lista con 2 o 3 nombres de 'Bailabilidad', 'Tempo', 'Energia'"))
        elif combo is None:
            checks.append((False, "predictores_ex1",
                           f"'{predictores_ex1}' no es válida — elige 2 o 3 columnas distintas de 'Bailabilidad', 'Tempo', 'Energia'"))
        else:
            checks.append((True, f"predictores_ex1 = {list(predictores_ex1)}", "✓  Combinación válida"))

        n_pred = len(combo) if combo is not None else 0

        if combo is None:
            checks.append((False, "modelo_ex1", "No se puede verificar sin predictores_ex1 válidos"))
            checks.append((False, "modelo_ex1 (escalado)", "No se puede verificar sin predictores_ex1 válidos"))
        elif not _es_kmeans_fit(modelo_ex1, 3, n_pred):
            checks.append((False, "modelo_ex1",
                           f"Debe ser un KMeans ya AJUSTADO (.fit()) con n_clusters=3 sobre tus {n_pred} predictores"))
            checks.append((False, "modelo_ex1 (escalado)", "No se puede verificar sin un modelo_ex1 válido"))
        else:
            checks.append((True, "modelo_ex1", "✓  KMeans ajustado con n_clusters=3"))
            if _parece_escalado(modelo_ex1):
                checks.append((True, "modelo_ex1 (escalado)",
                               "✓  Los centros de cluster están en un rango típico de datos estandarizados"))
            else:
                checks.append((False, "modelo_ex1 (escalado)",
                               "Los centros de cluster están muy fuera del rango típico de datos escalados -- ¿ajustaste sobre los datos SIN pasar por StandardScaler?"))

        modelo_valido = _es_kmeans_fit(modelo_ex1, 3, n_pred) if combo is not None else False

        if cluster_interes_ex1 is None:
            checks.append((False, "cluster_interes_ex1",
                           "No definida — el número de cluster (0, 1 o 2) cuyo centroide vas a interpretar"))
        elif not isinstance(cluster_interes_ex1, int) or isinstance(cluster_interes_ex1, bool):
            checks.append((False, "cluster_interes_ex1", f"Debe ser un entero (0, 1 o 2), recibí {type(cluster_interes_ex1).__name__}"))
        elif modelo_valido and not (0 <= cluster_interes_ex1 < modelo_ex1.n_clusters):
            checks.append((False, "cluster_interes_ex1", f"Debe ser un índice válido de tu modelo (0 a {modelo_ex1.n_clusters - 1})"))
        else:
            checks.append((True, f"cluster_interes_ex1 = {cluster_interes_ex1}", "✓  Índice de cluster válido"))

        predictor_names = predictores_ex1 if isinstance(predictores_ex1, (list, tuple)) else []

        if not _is_nontrivial_text(interpretacion_ex1, min_len=15):
            checks.append((False, "interpretacion_ex1",
                           "Escribe 1-2 oraciones interpretando el centroide de tu cluster -- no dejes '___' ni una frase de una palabra"))
        elif _trata_cluster_como_genero_fijo(interpretacion_ex1):
            checks.append((False, "interpretacion_ex1",
                           "Evita afirmar que el cluster ES un género real sin matiz (ej. 'es de canciones de Reggaetón') -- describe el grupo con tus propias variables/números, como hiciste en el 🧩 de arriba"))
        elif predictor_names and not _menciona_predictor_o_numero(interpretacion_ex1, predictor_names):
            checks.append((False, "interpretacion_ex1",
                           "Menciona al menos uno de tus predictores (ej. 'Bailabilidad', 'Tempo') o un número de tu propio resultado -- no una frase genérica que serviría para cualquier cluster"))
        else:
            checks.append((True, "interpretacion_ex1", "✓  Interpretación presente, sin tratar el cluster como un género fijo"))

        return self._award("ex1", checks, 40)

    # ═══════════════════════════════════════════════════════════
    # CHECKPOINT — mitad de Semana 7
    # ═══════════════════════════════════════════════════════════

    def check_mini_a(self):
        """Checkpoint — mitad de Semana 7, justo tras el Ejercicio 1"""
        self._checkpoints.add("mini_a")
        seccion = {
            "ex1": ("Ejercicio 1 – Tu primer mapa de clusters (canciones de Spotify)", 40),
        }
        self._render_checkpoint("CHECKPOINT — MITAD DE SEMANA 7", seccion, "#52b788")

    # ═══════════════════════════════════════════════════════════
    # REFLEXIONES — Ex1 (muestra de Energia) y generalización
    # (2026-09-21, simplificación: check_ex2/check_ex3 eliminados como
    # builds calificados -- ver docstring del módulo. Los ids internos
    # "nb6_ex2"/"nb6_generalizacion" se conservan para no requerir un
    # redeploy de grade-reflexion/index.ts.)
    # ═══════════════════════════════════════════════════════════

    def check_reflexion_ex2(self):
        """Reflexión — compara tu propio Ejercicio 1 con la muestra de agregar Energia (5 pts, IA)"""
        return self._ask_reflexion("nb6_ex2",
            'Arriba viste qué pasó al agregar Energia a Bailabilidad+Tempo (un cambio '
            'moderado, ni total ni trivial). En 1-2 oraciones: ¿usaste Energia entre tus '
            'predictores del Ejercicio 1? Si no la usaste, ¿crees que agregarla cambiaría tu '
            'agrupamiento? Si sí la usaste, ¿tu resultado se parece a ese cambio moderado?')

    def check_reflexion_generalizacion(self):
        """Reflexión — riesgo de una recomendación/segmentación que no generaliza, sobre el
        ejemplo guiado de train/test (5 pts, IA)"""
        return self._ask_reflexion("nb6_generalizacion",
            'En el ejemplo guiado de arriba, comparaste el perfil de cada cluster entre '
            'entrenamiento y prueba. Si esos perfiles se hubieran visto muy distintos entre '
            'train y test, ¿qué problema causaría eso para (a) recomendar la próxima canción '
            'por cluster, o (b) segmentar canciones para una decisión de marketing? En 2-4 '
            'oraciones, explica el problema para al menos uno de los dos usos.')

    # ═══════════════════════════════════════════════════════════
    # RETO 1 (bonus) — Cambia el número de regiones (otro k)
    # ═══════════════════════════════════════════════════════════

    def check_reto1(self):
        """Reto 1 (bonus) — reejecuta con otro k y describe qué cambió (10 pts, fuera del core)"""
        self._header("🎯 RETO — Cambia el Número de Regiones", icon="🧭", pts=10)
        checks = []
        k_reto1          = _get("k_reto1")
        modelo_reto1     = _get("modelo_reto1")
        comentario_reto1 = _get("comentario_reto1")

        k_valido = isinstance(k_reto1, int) and not isinstance(k_reto1, bool) and k_reto1 >= 2 and k_reto1 != 3

        if k_reto1 is None:
            checks.append((False, "k_reto1", "No definida — elige un valor de k distinto de 3 (ej. 2, 4 o 5)"))
        elif not isinstance(k_reto1, int) or isinstance(k_reto1, bool):
            checks.append((False, "k_reto1", f"Debe ser un entero, recibí {type(k_reto1).__name__}"))
        elif k_reto1 == 3:
            checks.append((False, "k_reto1", "Debe ser distinto de 3 -- ese ya lo usaste en el Ejercicio 1"))
        elif k_reto1 < 2:
            checks.append((False, "k_reto1", "Debe ser al menos 2 -- un solo cluster no agrupa nada"))
        else:
            checks.append((True, f"k_reto1 = {k_reto1}", "✓  k distinto de 3"))

        if not k_valido:
            checks.append((False, "modelo_reto1", "No se puede verificar sin k_reto1 válido"))
        elif not _es_kmeans_fit(modelo_reto1, k_reto1):
            checks.append((False, "modelo_reto1", f"Debe ser un KMeans ya AJUSTADO (.fit()) con n_clusters={k_reto1}"))
        elif not _parece_escalado(modelo_reto1):
            checks.append((False, "modelo_reto1",
                           "Los centros de cluster sugieren que no ajustaste sobre datos escalados -- reusa el mismo StandardScaler de antes"))
        else:
            checks.append((True, "modelo_reto1", f"✓  KMeans ajustado con n_clusters={k_reto1}, sobre datos escalados"))

        if not _is_nontrivial_text(comentario_reto1, min_len=10):
            checks.append((False, "comentario_reto1",
                           "Escribe en 1 frase qué cambió al usar otro k (ej. cuántos grupos quedaron, si alguno se dividió o se fusionó)"))
        else:
            checks.append((True, "comentario_reto1", "✓  Comentario presente"))

        return self._award("reto1", checks, 10)

    def check_reflexion_final(self):
        """Reflexión de cierre — riesgo de tratar un cluster como género oficial (5 pts, IA)"""
        return self._ask_reflexion("nb6_final",
            'Ya usaste k-means para agrupar canciones por variables numéricas, sin '
            'decirle al algoritmo nada sobre el género real de cada canción. En 2-4 '
            'oraciones: ¿cuál es el riesgo de tratar un cluster de k-means como si fuera '
            'un género "oficial"? ¿en qué otro contexto (que no sean canciones) podría '
            'pasar algo parecido?')

    # ═══════════════════════════════════════════════════════════
    # CHECKPOINT — fin de la Semana 7 / Misión 4
    # ═══════════════════════════════════════════════════════════

    def check_mini_b(self):
        """Checkpoint — fin de la Semana 7 y de la Misión 4"""
        self._checkpoints.add("mini_b")
        if len(self._checkpoints) >= 2 and self._unlock("medalla_cartografo"):
            display(HTML(
                f'<div style="display:flex;align-items:center;gap:8px;'
                f'font-family:\'Press Start 2P\',monospace;font-size:8px;'
                f'color:#95d5b2;background:#1a1030;border:1px solid #95d5b2;'
                f'border-radius:3px;padding:12px 16px;max-width:840px;margin:6px 0;">'
                f'{self._logo_tag_sm}'
                f'<span>🎖️ LOGRO: Medalla del Cartógrafo — Ambos checkpoints de Semana 7 superados</span></div>'
            ))
        seccion = {
            "cluster_es_genero": ("🧩 ¿Los clusters son géneros reales?", 5),
            "t1": ("T1 – Qué hace k-means", 5),
            "t2": ("T2 – Por qué escalar", 5),
            "t3": ("T3 – Etiquetas de cluster arbitrarias", 5),
            "t4": ("T4 – Sensibilidad a k e inicialización", 5),
            "t5": ("T5 – Qué es un centroide", 5),
        }
        self._render_checkpoint("CHECKPOINT — FIN DE LA MISIÓN 4", seccion, "#f4a261")

    # ═══════════════════════════════════════════════════════════
    # RESUMEN FINAL
    # ═══════════════════════════════════════════════════════════

    def resumen(self):
        _, _, pct         = self._totals()
        n                 = self._nombre()
        lvl_num, lvl_name = _level_info(pct)
        core_earned       = sum(e for k, (e, _) in self._scores.items() if k not in _BONUS_KEYS)
        bonus_earned      = self._bonus_earned()

        if pct >= 96:
            final_msg = f"🏆 CARTÓGRAFO SUPREMO. {n.upper()}, tu nombre entra al Salón de la Fama de la Misión 4."
        elif pct >= 81:
            final_msg = f"🏔️ CARTÓGRAFO EXPERTO. {n}, ya sabes trazar un mapa de clusters y leer sus límites. Sigue así."
        elif pct >= 61:
            final_msg = f"📍 TRAZADOR DE FRONTERAS. {n}, tu mapa ya agrupa de verdad. ¡Sigue así!"
        elif pct >= 41:
            final_msg = f"🗺️ LECTOR DE REGIONES. {n}, los grupos empiezan a tener sentido. Revisa los ✖ para avanzar."
        elif pct >= 21:
            final_msg = f"🧭 PRIMER TRAZO. {n}, todo mapa empieza así. Relee la teoría y vuelve a intentar."
        else:
            final_msg = f"🌱 {n}, tu camino como cartógrafo de datos sigue. Cada celda ejecutada es un paso hacia adelante."

        ach_display = {
            "primer_trazo":          "🧭 Primer Trazo",
            "cartografo_novato":     "🗺️ Cartógrafo Novato",
            "explorador_completo":   "🏔️ Explorador Completo",
            "cazador_de_k":          "🎯 Cazador de K",
            "medalla_cartografo":    "🎖️ Medalla del Cartógrafo",
            "racha_de_trazos":       "🔥 Racha de Trazos",
            "mapa_completo":         "🏆 Mapa Completo",
        }

        ach_html = ""
        if self._achievements:
            for ak, alabel in ach_display.items():
                if ak in self._achievements:
                    ach_html += (
                        f'<div style="display:inline-flex;align-items:center;gap:5px;'
                        f'padding:3px 8px;background:rgba(255,209,102,.08);'
                        f'border:1px solid #e9c46a40;border-radius:2px;margin:2px;">'
                        f'<span style="font-family:\'Press Start 2P\',monospace;font-size:6px;'
                        f'color:#e9c46a;">{alabel}</span></div>'
                    )

        lv_color = _lv_color(lvl_num)
        xp_grad  = _XP_GRAD.get(lvl_num, _XP_GRAD[1])

        self._submit_to_supabase(core_earned, _CORE_MAX, pct, lvl_num, lvl_name)

        display(HTML(f'''
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
  @keyframes pk-glow{{0%,100%{{text-shadow:0 0 14px rgba(255,209,102,.8),2px 2px 0 #2d6a4f}}
    50%{{text-shadow:0 0 32px rgba(255,209,102,1),0 0 60px rgba(255,158,44,.5),2px 2px 0 #2d6a4f}}}}
  @keyframes pk-xp{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
</style>
<div style="background:#0c0a16;border:2px solid #e9c46a;border-radius:6px;max-width:840px;
  margin:12px 0;overflow:hidden;
  box-shadow:0 0 40px rgba(255,209,102,.15),0 0 80px rgba(255,158,44,.08),0 10px 40px rgba(0,0,0,.8);">

  <div style="background:linear-gradient(135deg,#0c0a16,#1a1436,#0c0a16);
    border-bottom:2px solid #e9c46a;padding:22px 28px;text-align:center;position:relative;">
    <div style="position:absolute;left:20px;top:50%;transform:translateY(-50%);">{self._logo_tag}</div>
    <div style="font-family:'Press Start 2P',monospace;font-size:clamp(13px,2.8vw,20px);
      color:#e9c46a;animation:pk-glow 2.5s ease-in-out infinite;letter-spacing:3px;
      margin-bottom:8px;">🧭 MISIÓN 4: EL CARTÓGRAFO DE PATRONES 🗺️</div>
    <div style="font-family:'Press Start 2P',monospace;font-size:8px;color:#f4a261;
      letter-spacing:2px;">SEMANA 7 — RESUMEN FINAL</div>
    <div style="position:absolute;right:20px;top:50%;transform:translateY(-50%);">{self._logo_tag}</div>
  </div>

  <div style="padding:24px 28px;">
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:20px;">
      <div style="background:#0f0c1e;border:1px solid #241f3d;border-radius:3px;
        padding:16px;text-align:center;">
        <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#7a72a0;
          letter-spacing:1px;margin-bottom:10px;">XP TOTAL</div>
        <div style="font-family:'Press Start 2P',monospace;font-size:clamp(14px,3vw,22px);
          color:#e9c46a;">{core_earned}/{_CORE_MAX}</div>
      </div>
      <div style="background:#0f0c1e;border:1px solid #241f3d;border-radius:3px;
        padding:16px;text-align:center;">
        <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#7a72a0;
          letter-spacing:1px;margin-bottom:10px;">NIVEL</div>
        <div style="font-family:'Press Start 2P',monospace;font-size:clamp(8px,1.5vw,12px);
          color:{lv_color};">{lvl_name}</div>
      </div>
      <div style="background:#0f0c1e;border:1px solid #241f3d;border-radius:3px;
        padding:16px;text-align:center;">
        <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#7a72a0;
          letter-spacing:1px;margin-bottom:10px;">SCORE</div>
        <div style="font-family:'Press Start 2P',monospace;font-size:clamp(14px,3vw,22px);
          color:#4caf50;">{pct}%</div>
      </div>
    </div>

    <div style="margin-bottom:20px;">
      <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
        <span style="font-family:'Press Start 2P',monospace;font-size:7px;color:#7a72a0;">
          PROGRESO</span>
        <span style="font-family:'Press Start 2P',monospace;font-size:7px;color:{lv_color};">
          {pct}%</span>
      </div>
      <div style="width:100%;height:14px;background:#191430;border:1px solid #241f3d;
        border-radius:3px;overflow:hidden;">
        <div style="width:{pct}%;height:100%;background:{xp_grad};
          border-radius:3px;transform-origin:left;
          animation:pk-xp 1.4s cubic-bezier(.4,0,.2,1) forwards;
          box-shadow:0 0 8px rgba(255,209,102,.4);"></div>
      </div>
    </div>

    <div style="background:#0f0c1e;border:1px solid #52b788;border-radius:3px;
      padding:14px 18px;margin-bottom:20px;text-align:center;">
      <div style="font-size:13px;color:#ece8f8;line-height:1.7;">{final_msg}</div>
    </div>

    {f'''
    <div style="text-align:center;margin-bottom:20px;font-family:'Press Start 2P',monospace;
      font-size:7px;color:#e9c46a;letter-spacing:1px;">
      🎯 BONUS — Cambia el Número de Regiones: {bonus_earned}/{_BONUS_MAX} XP (no cuenta para el nivel)
    </div>''' if "reto1" in self._scores else ""}

    {f"""
    <div style="margin-bottom:16px;">
      <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#7a72a0;
        letter-spacing:1px;margin-bottom:10px;">🧭 LOGROS DESBLOQUEADOS</div>
      <div style="display:flex;flex-wrap:wrap;gap:4px;">{ach_html}</div>
    </div>""" if ach_html else ""}

    {"""
    <div style="padding:12px 16px;background:#1a0000;border:2px solid #ff0000;
      border-radius:3px;text-align:center;">
      <div style="font-family:'Press Start 2P',monospace;font-size:10px;color:#ff0000;
        letter-spacing:2px;">🚫 PLAZO VENCIDO</div>
      <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#ff8888;
        margin-top:6px;">La nota no será actualizada en la base de datos</div>
    </div>""" if DEADLINE_PASSED else f"""
    <div style="text-align:center;font-family:'Press Start 2P',monospace;font-size:7px;
      color:#52b788;letter-spacing:1px;opacity:.9;">
      📊 Calificación final enviada al leaderboard · {n} · {lvl_name}
    </div>"""}
  </div>
</div>'''))

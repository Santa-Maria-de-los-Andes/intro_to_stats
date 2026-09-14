"""
Autograder — Bimestre 3, Misión 3: El Oráculo de Datos — SEMANA 6
REGRESIÓN LINEAL — World Happiness Report 2019 (ejemplo guiado) +
120 Years of Olympic History (ejercicios)

ATLAS build 2026-09-13, a partir del pedido directo del usuario para "nb5"
(Semana 6, regresión lineal). Primer notebook de esta misión -- sin
predecesor nb3/nb4 que continuar, así que check_ex/check_t/check_reto
empiezan frescos en 1, no continúan la numeración de Misión 2
(WORKFORCE_CONTRACT.md §2). SOFIA/PIXEL/ATLAS se hicieron en una sola
pasada dado el pedido explícito de estructura del usuario: estructura,
tema y grader se diseñaron juntos siguiendo WORKFORCE_CONTRACT.md §2
(Semana 6 -- "interpretar un modelo ajustado, no derivarlo") y §5 (temario
técnico: solo `LinearRegression().fit()/.predict()`, nada de encoding
avanzado).

Cubre: check_prediccion_linea, check_anota_distancia, check_t1-t5,
check_reflexion_interpretacion, check_ex1, check_ex2, check_reflexion_ex2,
check_reflexion_final, check_mini_a, check_mini_b, check_reto1 (bonus),
resumen()

2026-09-13 (mismo día, pase de revisión pre-lanzamiento): se agregó check_t5
(coeficientes y escala) a pedido explícito del usuario -- t1-t4 explican R²/
overfitting/extrapolación, pero la advertencia de Paso 6 del ejemplo guiado
("un coeficiente más grande no significa automáticamente más importante")
se quedaba sin evaluar. _CORE_MAX sube de 95 a 100 -- cambio de alcance
reconocido, no una desviación silenciosa (ver WORKFORCE_CONTRACT.md §2,
entrada 2026-09-13).

2026-09-14 (mismo pedido de usuario, pase de UX/scoring): `check_prediccion_linea`
y `check_anota_distancia` reemplazan lo que antes eran celdas de código con
una variable suelta (`mi_prediccion_x = "___"`, sin calificar y sin registro
en ningún lado). Ahora son el mismo widget HTML/JS que las reflexiones IA
(sección "REGISTRO" en este archivo), sin llamada a DeepSeek: 1 XP de
participación c/u si el texto no es un placeholder vacío, texto crudo
guardado en `score_breakdown` de `submissions` para revisión por SQL sin
abrir cada notebook. _CORE_MAX sube de 100 a 102.

Datasets:
  - 2019_es.csv (156 filas × 10 columnas, World Happiness Report) -- mismo
    archivo que nb3/nb4, reutilizado solo para el ejemplo guiado (no
    autograded, es demostración con el hallazgo de nb4: PBI↔Puntaje
    r≈0.794). Se vuelve a descargar en esta sesión de Colab.
  - athlete_events_es.csv (271,116 filas, 120 Years of Olympic History) --
    mismo archivo que nb1_semana2, reutilizado para los Ejercicios 1-2 y el
    reto. Tras `dropna` en Edad/Altura/Peso/Sexo quedan 206,165 filas.

Decisión de alcance (ATLAS, documentada también en build_nb5.py): el pedido
original listaba {Edad, Peso, Sexo, Deporte} como menú de predictores para
predecir Altura. `Deporte` tiene 66 categorías -- codificarlo (one-hot)
está fuera del temario comprometido (WORKFORCE_CONTRACT.md §5 no incluye
`pd.get_dummies`/`OneHotEncoder`). Se recortó el menú a
{Edad, Peso, Sexo_num} -- `Sexo` se convierte a número binario (0/1) en una
celda guiada antes del Ejercicio 1 (una sola línea, defendible a este
nivel); `Deporte` queda explícitamente fuera, con una nota en el notebook
de por qué. Esto reduce el menú de "2-4 predictores" a "2-3 predictores" --
ajuste menor, documentado aquí y en build_nb5.py, no una desviación
silenciosa.

Todos los R² de este archivo se calcularon directamente contra los CSV
reales el 2026-09-13 con `train_test_split(..., test_size=0.1,
random_state=42)` -- mismo `random_state` exigido a los estudiantes en el
enunciado de cada ejercicio, para que los valores sean reproducibles y
verificables, no solo "aproximadamente parecidos". Tolerancia ±0.02 en el
lookup de R² (más ancha que el ±0.01 de nb3/nb4 porque aquí hay 206K filas
en vez de 156 -- deja margen para que una versión de sklearn ligeramente
distinta en el Colab de un estudiante no reviente el check).

Notas de scoring:
  reg_linea_roja / reg_minimiza_distancia (registro de participación --
  texto corto, sin IA, sin respuesta incorrecta) valen 1 c/u = 2.
  t1-t4 (teoría: qué significa R², por qué importa el R² de prueba, qué es
  overfitting, por qué la extrapolación da resultados absurdos) valen 5
  c/u = 20.
  t5 (teoría: un coeficiente más grande no implica automáticamente más
  importante, por diferencia de escala entre variables) vale 5.
  refl_interpretacion (interpretar los coeficientes del ejemplo guiado,
  sin lenguaje causal) vale 5, calificada por IA.
  ex1 (Ejercicio 1 -- predictores + train/test R² + interpretación no
  causal, sobre Altura de atletas) vale 40 (4 sub-checks × 10 c/u).
  ex2 (Ejercicio 2 -- explorar combos, reportar el mejor R² de prueba) vale
  20 (2 sub-checks × 10 c/u).
  refl_ex2 (por qué esa combinación funcionó mejor) vale 5, IA.
  refl_final (reflexión de cierre, cuándo usarías esto) vale 5, IA.
  _CORE_MAX = 2 (registro) + 25 (t1-5) + 5 (refl_interpretacion) + 40 (ex1)
            + 20 (ex2) + 5 (refl_ex2) + 5 (refl_final) = 102.
  reto1 (bonus -- "rompe el modelo" con una entrada absurda) vale 10,
  fuera de _CORE_MAX, en _BONUS_MAX.

Nota Supabase: mismo proyecto/tabla `submissions` que el resto del curso,
campo "curso"="STAT_2026", "notebook"="nb5". Deadline: 21 de septiembre
2026, 11:59 PM Perú -- dos semanas después del cierre de nb4 (7 sept),
dejando la semana intermedia para el debunking de causalidad (Semana 5,
sin autograder propio, ver Week 5/build_correlaciones_espurias.py).
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
NOTEBOOK_ID       = "nb5"

# ─── Deadline: 21 septiembre 2026, 11:59 PM Peru (UTC-5) = 22 sept 04:59 UTC ─
_DEADLINE_UTC   = _dt.datetime(2026, 9, 22, 4, 59, 0, tzinfo=_dt.timezone.utc)
DEADLINE_PASSED = _dt.datetime.now(_dt.timezone.utc) >= _DEADLINE_UTC

# ─── Scoring ─────────────────────────────────────────────────
_CORE_MAX   = 102  # 2 (registro) + 25 (t1-5) + 5 (refl_interpretacion)
                   # + 40 (ex1) + 20 (ex2) + 5 (refl_ex2) + 5 (refl_final)
_BONUS_KEYS = {"reto1"}
_BONUS_MAX  = 10   # reto1 — "rompe el modelo", fuera del core

# ─── Reflexion (calificada por IA vía Supabase Edge Function) ─
_REFLEXION_PTS       = 5
GRADE_REFLEXION_URL  = f"{SUPABASE_URL}/functions/v1/grade-reflexion"

# ─── Niveles "El Oráculo de Datos" (por % del score core) ───
_LEVELS = [
    (96, 6, "🏆 Oráculo Supremo"),
    (81, 5, "🔮 Vidente de Datos"),
    (61, 4, "📈 Trazador de Líneas"),
    (41, 3, "✨ Lector de Patrones"),
    (21, 2, "🌙 Primera Visión"),
    (0,  1, "🌱 Aprendiz de Oráculo"),
]

_XP_GRAD = {
    1: "linear-gradient(90deg,#33402c,#6f8f57)",
    2: "linear-gradient(90deg,#5a3d99,#ffd166)",
    3: "linear-gradient(90deg,#3d2270,#b185f0)",
    4: "linear-gradient(90deg,#0d3a52,#5dd9ff)",
    5: "linear-gradient(90deg,#4a2680,#9b5de5)",
    6: "linear-gradient(90deg,#9b5de5,#ffd166,#5dd9ff)",
}
_LV_CSS_COLOR = {1: "#6a5ea8", 2: "#ffd166", 3: "#b185f0", 4: "#5dd9ff", 5: "#9b5de5", 6: "#ffd166"}


def _level_info(pct):
    for thresh, num, name in _LEVELS:
        if pct >= thresh:
            return num, name
    return 1, "🌱 Semilla de Curiosidad"


def _lv_color(n):
    return _LV_CSS_COLOR.get(n, "#6a5ea8")


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


# Nombres reales de columna usados por athlete_events_es.csv (tras el
# preprocesamiento guiado que agrega Sexo_num -- ver build_nb5.py).
_COL_EDAD      = "Edad"
_COL_PESO      = "Peso"
_COL_SEXO_NUM  = "Sexo_num"
_COL_ALTURA    = "Altura"

_PREDICTORES_VALIDOS = [_COL_EDAD, _COL_PESO, _COL_SEXO_NUM]
_PREDICTORES_NORM    = {_norm(c) for c in _PREDICTORES_VALIDOS}

# R² real por combinacion de predictores (train_test_split test_size=0.1,
# random_state=42, sobre las 206,165 filas sin nulos en Edad/Altura/Peso/
# Sexo) -- calculado 2026-09-13, ver docstring del modulo. clave = frozenset
# normalizado de nombres de columna -> (train_r2, test_r2).
_R2_LOOKUP = {
    frozenset([_norm(_COL_EDAD), _norm(_COL_PESO)]):                       (0.635, 0.635),
    frozenset([_norm(_COL_EDAD), _norm(_COL_SEXO_NUM)]):                   (0.247, 0.247),
    frozenset([_norm(_COL_PESO), _norm(_COL_SEXO_NUM)]):                   (0.644, 0.643),
    frozenset([_norm(_COL_EDAD), _norm(_COL_PESO), _norm(_COL_SEXO_NUM)]): (0.645, 0.644),
}
_MEJOR_COMBO_TEST_R2 = max(v[1] for v in _R2_LOOKUP.values())  # 0.644, combo completo

# Palabras/frases causales -- ver Teoria_Semanas3-4_Mision2_Correlacion.md,
# la misma regla de lenguaje no-causal que rige nb3/nb4 aplica aqui a la
# interpretacion de coeficientes de regresion.
_PALABRAS_CAUSALES = [
    "causa", "causan", "provoca", "provocan", "hace que", "hacen que",
    "genera que", "generan que", "produce que", "producen que",
    "es la razon de", "por culpa de", "debido a que causa",
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


def _predictores_normalizados(lst):
    """Valida una lista/tupla de 2-3 nombres de columna contra el menu
    permitido {Edad, Peso, Sexo_num}. Devuelve el frozenset normalizado (sin
    duplicados) si es valida, o None si no lo es -- para usar como llave en
    _R2_LOOKUP."""
    if not isinstance(lst, (list, tuple)) or not all(isinstance(x, str) for x in lst):
        return None
    norm = {_norm(x) for x in lst}
    if len(norm) != len(lst):
        return None  # duplicados
    if not (2 <= len(norm) <= 3):
        return None
    if not norm.issubset(_PREDICTORES_NORM):
        return None
    return frozenset(norm)


def _contiene_lenguaje_causal(text):
    t = _norm(text)
    return any(_norm(p) in t for p in _PALABRAS_CAUSALES)


def _menciona_predictor_o_numero(text, predictores):
    """Rechaza relleno generico-pero-valido (pasa el largo minimo, evita
    palabras causales, y aun asi no dice nada especifico -- ej. "la variable
    que elegi influye en el resultado"). Exige que la interpretacion nombre
    al menos uno de los predictores que el propio estudiante eligio
    (tolerante a tildes/mayusculas via _norm) o incluya al menos un digito
    (un coeficiente, un R², cualquier numero de su propio resultado)."""
    t = _norm(text)
    if any(_norm(p) in t for p in predictores):
        return True
    return any(ch.isdigit() for ch in text)


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
                    'color:#ffd166;letter-spacing:2px;">SMA</span>')

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
  <div style="background:#0c0a16;border:1px solid #5dd9ff;border-radius:3px;
    padding:12px 20px;margin-top:6px;
    font-family:'Press Start 2P',monospace;animation:ag-fadein .4s ease .1s both;">
    <div style="font-size:6px;color:#5dd9ff;letter-spacing:2px;margin-bottom:10px;">
      🔮 TU MEJOR MARCA — SEMANA 6</div>
    <div style="display:flex;align-items:center;gap:20px;">
      <div style="font-size:28px;color:#ffd166;
        text-shadow:0 0 16px rgba(255,209,102,.8),2px 2px 0 #5a3d99;">
        {_best['pct']}%</div>
      <div>
        <div style="font-size:8px;color:#9b5de5;letter-spacing:1px;">{_best['level_name']}</div>
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
                        '🔮 La bola de cristal está en blanco — ¡aun no tienes marca registrada!</div>'
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
  <div style="background:#140c04;border:1px solid #9b5de5;border-radius:3px;padding:12px 18px;
    font-family:'Press Start 2P',monospace;font-size:8px;
    color:#9b5de5;letter-spacing:1px;animation:ag-fadein .4s ease;">
    🔮 &nbsp;¡BIENVENIDO DE VUELTA, VIDENTE {nombre.upper()}! &nbsp;·&nbsp; {grado}
  </div>
  {_score_html}
  <div id="ag-loading" style="background:#0c0a16;border:1px solid #241f3d;border-radius:3px;
    padding:22px 18px;margin-top:6px;text-align:center;animation:ag-fadein .5s ease .2s both;">
    <div style="display:flex;justify-content:center;gap:6px;margin-bottom:12px;">
      <div style="width:8px;height:8px;border-radius:50%;background:#9b5de5;
        animation:ag-dot 1.2s ease-in-out 0s infinite;"></div>
      <div style="width:8px;height:8px;border-radius:50%;background:#9b5de5;
        animation:ag-dot 1.2s ease-in-out .2s infinite;"></div>
      <div style="width:8px;height:8px;border-radius:50%;background:#9b5de5;
        animation:ag-dot 1.2s ease-in-out .4s infinite;"></div>
    </div>
    <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#7a72a0;letter-spacing:2px;">
      CONSULTANDO EL ORÁCULO…
    </div>
  </div>
  <div id="ag-start" style="display:none;background:linear-gradient(160deg,#0c0a16,#1a1436);
    border:2px solid #9b5de5;border-radius:4px;padding:36px 24px;margin-top:6px;text-align:center;
    box-shadow:0 0 40px rgba(255,158,44,.25),0 0 80px rgba(255,209,102,.06),0 6px 24px rgba(0,0,0,.9);">
    <div style="font-size:44px;margin-bottom:14px;animation:ag-start .55s cubic-bezier(.34,1.56,.64,1);">🔮</div>
    <div style="font-family:'Press Start 2P',monospace;font-size:clamp(15px,3.6vw,26px);color:#ffd166;
      letter-spacing:4px;text-shadow:0 0 24px rgba(255,209,102,.95),0 0 50px rgba(255,158,44,.35),
      2px 2px 0 #5a3d99;animation:ag-start .6s ease;margin-bottom:14px;">¡CONTINÚA TU MISIÓN!</div>
    <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#5dd9ff;
      letter-spacing:2px;opacity:.85;margin-bottom:16px;">EJECUTA LA PRIMERA CELDA PARA COMENZAR</div>
    <div style="font-size:15px;color:#9b5de5;opacity:.4;letter-spacing:8px;">🔮 ✨ 🔮 ✨ 🔮 ✨ 🔮</div>
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
  .ag-input:focus,.ag-select:focus {{ border-color:#5dd9ff; }}
  .ag-select option {{ background:#0c0a16; }}
  .ag-btn {{
    width:100%;padding:13px;background:linear-gradient(90deg,#6a3fc0,#9b5de5);
    border:none;border-radius:3px;color:#0c0a16;font-family:'Press Start 2P',monospace;
    font-size:9px;letter-spacing:2px;cursor:pointer;transition:opacity .2s;margin-top:6px;
  }}
  .ag-btn:hover {{ opacity:.85; }}
  .ag-err {{ color:#ff5d5d;font-size:11px;margin-top:6px;display:none; }}
  .ag-label {{ font-family:'Press Start 2P',monospace;font-size:7px;letter-spacing:1px;
    margin-bottom:8px;display:flex;align-items:center;gap:5px; }}
  .ag-field {{ display:flex;flex-direction:column; }}
</style>
<div style="background:#0c0a16;border:2px solid #5dd9ff;border-radius:4px;max-width:840px;
  margin:10px 0;overflow:hidden;box-shadow:0 0 40px rgba(74,168,216,.2),0 10px 30px rgba(0,0,0,.8);">

  <div style="background:linear-gradient(90deg,#0c0a16,#1a1436,#0c0a16);border-bottom:2px solid #ffd166;
    padding:18px 24px;position:relative;display:flex;align-items:center;justify-content:center;min-height:80px;">
    <div style="position:absolute;left:20px;top:50%;transform:translateY(-50%);">{logo_tag}</div>
    <div style="text-align:center;">
      <div style="font-family:'Press Start 2P',monospace;font-size:clamp(13px,3vw,18px);color:#ffd166;letter-spacing:3px;
        text-shadow:0 0 14px rgba(255,209,102,.7),2px 2px 0 #5a3d99;">🔮 MISIÓN 3: EL ORÁCULO DE DATOS 📈</div>
      <div style="font-family:'Press Start 2P',monospace;font-size:8px;color:#9b5de5;
        letter-spacing:2px;margin-top:8px;">SEMANA 6 — EL ORÁCULO DE DATOS</div>
    </div>
    <div style="position:absolute;right:20px;top:50%;transform:translateY(-50%);">{logo_tag}</div>
  </div>

  <div style="padding:24px;">
    <div style="display:grid;grid-template-columns:2fr 1fr;gap:14px;margin-bottom:14px;align-items:end;">
      <div class="ag-field">
        <div class="ag-label" style="color:#9b5de5;">🔮 NOMBRE COMPLETO</div>
        <input id="ag-nombre" class="ag-input" placeholder="Tu nombre y apellido" />
      </div>
      <div class="ag-field">
        <div class="ag-label" style="color:#9b5de5;">🏫 GRADO</div>
        <select id="ag-grado" class="ag-select">
          <option value="">— Selecciona —</option>
          <option value="3ro">3ro</option>
          <option value="4to">4to</option>
          <option value="5to">5to</option>
        </select>
      </div>
    </div>
    <div class="ag-field" style="margin-bottom:14px;">
      <div class="ag-label" style="color:#ffd166;">🪪 CÓDIGO DE ESTUDIANTE (DNI, Pasaporte, Carnet)</div>
      <input id="ag-dni" class="ag-input" placeholder="Ingresa tu código" />
    </div>
    <div id="ag-err" class="ag-err">⚠ Por favor completa todos los campos.</div>
    <button class="ag-btn" onclick="agRegister()">🔮 &nbsp; ¡CONTINUAR LA BÚSQUEDA! &nbsp; 📈</button>
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
                             'color:#9b5de5;border:1px solid #5dd9ff;border-radius:3px;max-width:840px;">'
                             '🔮 MISIÓN 3 — SEMANA 6 — Registro</div>'))
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
        return '<span style="font-family:\'Press Start 2P\',monospace;font-size:11px;color:#ffd166;">SMA</span>'

    @property
    def _logo_tag_sm(self):
        if LOGO_URL:
            return (f'<img src="{LOGO_URL}" style="height:24px;object-fit:contain;" '
                    f'onerror="this.style.display=\'none\'">')
        return '<span style="font-family:\'Press Start 2P\',monospace;font-size:8px;color:#ffd166;">SMA</span>'

    def _nombre(self):
        if self._nombre_real:
            return self._nombre_real
        return "vidente"

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

    def _header(self, title, icon="🔮", pts=None):
        self._curr_title = title
        self._curr_icon  = icon
        self._curr_pts   = pts

    def _check_achievements(self, key):
        unlocked = []
        earned, possible, pct = self._totals()

        # Primera Visión — primer XP ganado
        if any(e > 0 for e, _ in self._scores.values()) and self._unlock("primera_vision"):
            unlocked.append(("🔮 Primera Visión — ¡Tu primer punto de predicción conquistado!", "#9b5de5", "Destello"))

        # Constructor de Modelos — ex1 perfecto (predictores + R² + interpretacion)
        if (self._scores.get("ex1", (0, 1))[0] == self._scores.get("ex1", (0, 1))[1]
                and "ex1" in self._scores and self._unlock("constructor_de_modelos")):
            unlocked.append(("🏗️ Constructor de Modelos — Tu primer modelo de regresión, completo y bien interpretado", "#5dd9ff", "Fulgor"))

        # Optimizador — ex1 y ex2 perfectos (encontraste y mejoraste el mejor R²)
        ex_todos = ["ex1", "ex2"]
        if (all(k in self._scores and self._scores[k][0] == self._scores[k][1] for k in ex_todos)
                and self._unlock("optimizador")):
            unlocked.append(("📈 Optimizador — Probaste varias combinaciones y encontraste la mejor", "#b185f0", "Revelación"))

        # Rompe-Modelos — completaste el reto de extrapolación absurda
        if (self._scores.get("reto1", (0, 1))[0] > 0
                and "reto1" in self._scores and self._unlock("rompe_modelos")):
            unlocked.append(("💥 Rompe-Modelos — Le diste al oráculo una entrada imposible y viste el resultado", "#b185f0", "Revelación"))

        # Medalla del Oráculo — ambos checkpoints de Semana 6 alcanzados
        if len(self._checkpoints) >= 2 and self._unlock("medalla_oraculo"):
            unlocked.append(("✨ Medalla del Oráculo — Ambos checkpoints de Semana 6 superados", "#b185f0", "Revelación"))

        # Racha Predictiva — racha >= 5
        if self._streak >= 5 and self._unlock("racha_predictiva"):
            unlocked.append(("🔥 Racha Predictiva — Combo x5", "#5dd9ff", "Fulgor"))

        # Visión Completa — 100% del core
        if pct >= 100 and self._unlock("vision_completa"):
            unlocked.append(("🏆 Visión Completa — 100% de la Semana 6", "#9b5de5", "Visión Suprema"))

        # Level-up
        lvl_num, lvl_name = _level_info(pct)
        if lvl_num > self._prev_level and self._prev_level > 0:
            unlocked.append((f"⬆️ ¡SUBISTE DE NIVEL! — {lvl_name}", "#5dd9ff", "Nivel"))
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
        gold, dark = "#ffd166", "#2a2200"
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
            c_color = "#9b5de5" if self._streak >= 5 else "#ffd166"
            combo_html = (
                f'<div style="display:inline-flex;align-items:center;gap:5px;padding:3px 10px;'
                f'background:rgba(255,158,44,.12);border:1px solid {c_color};border-radius:2px;'
                f'margin-left:8px;">'
                f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;'
                f'color:{c_color};">🔮 RACHA x{self._streak}</span></div>'
            )

        if pts == max_pts:
            s_icon, s_text, s_color = "🔮", f"¡RAYO DE SOL COMPLETO! +{pts} XP", "#4caf50"
            border_color, glow = "#4caf50", "0 0 22px rgba(76,175,80,.15)"
        elif pts > 0:
            s_icon, s_text, s_color = "🌙", f"+{pts} XP  ·  {max_pts - pts} por brillar", "#ffd166"
            border_color, glow = "#b185f0", "0 0 22px rgba(255,183,3,.12)"
        else:
            s_icon, s_text, s_color = "🌥️", "NUBE PASAJERA — Corrige los ✖ e intenta de nuevo", "#ff5d5d"
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
            "Destello":       ("#6a5ea8", "rgba(106,94,168,.12)", "🌱"),
            "Fulgor":         ("#5dd9ff", "rgba(93,217,255,.12)", "🌙"),
            "Revelación":     ("#b185f0", "rgba(177,133,240,.10)", "✨"),
            "Visión Suprema": ("#9b5de5", "rgba(155,93,229,.15)",  "🔮"),
        }
        ach_html = ""
        for ach_name, _, ach_rarity in reg_ach:
            bc, bg, ach_icon = _RC.get(ach_rarity, _RC["Destello"])
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

        curr_icon  = getattr(self, '_curr_icon', '🔮')
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
                             'font-size:6px;color:#5dd9ff;letter-spacing:1px;opacity:.85;">'
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
      <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#9b5de5;
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
            2: dict(bg="linear-gradient(160deg,#0c0a16,#1a1030)",
                    c="#ffd166", sc="#ffe6a3", rc="#ffd166",
                    sub="PRIMERA VISIÓN — LA BOLA DE CRISTAL EMPIEZA A ACLARAR", icon="🌙"),
            3: dict(bg="linear-gradient(160deg,#141005,#1a1030)",
                    c="#b185f0", sc="#ffd27f", rc="#b185f0",
                    sub="LECTOR DE PATRONES — LOS NÚMEROS EMPIEZAN A HABLAR", icon="✨"),
            4: dict(bg="linear-gradient(160deg,#0d0c22,#14203d)",
                    c="#5dd9ff", sc="#9fe8ff", rc="#5dd9ff",
                    sub="TRAZADOR DE LÍNEAS — TU MODELO YA PREDICE DE VERDAD", icon="📈"),
            5: dict(bg="linear-gradient(160deg,#180d02,#2a1400)",
                    c="#9b5de5", sc="#ffc27a", rc="#9b5de5",
                    sub="VIDENTE DE DATOS — SABES CUÁNDO CONFIAR EN EL MODELO", icon="🔮"),
            6: dict(bg="linear-gradient(160deg,#0c0a16,#1a0f02,#0d1a26)",
                    c="#ffd166", sc="#5dd9ff", rc="#9b5de5",
                    sub="ORÁCULO SUPREMO — SALÓN DE LA FAMA", icon="🏆"),
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
                          f'margin:-50px;border-radius:50%;border:2px solid #5dd9ff;opacity:0;'
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
    🔮 ✨ 🔮 ✨ 🔮</div>
  <div style="position:absolute;right:14px;top:50%;
    font-size:15px;letter-spacing:5px;
    animation:{uid}-rr .9s ease-out .6s both;pointer-events:none;z-index:7;">
    🔮 ✨ 🔮 ✨ 🔮</div>

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
                "nombre":          self._nombre_real or "vidente",
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
                    f'<br><span style="color:#5dd9ff;font-size:7px;">'
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
    # (+1 XP c/u, sin IA, sin respuesta incorrecta)
    # ═══════════════════════════════════════════════════════════
    #
    # 2026-09-14: antes estas eran celdas de código con una variable suelta
    # (`mi_prediccion_x = "___"`) que nadie calificaba ni quedaba registrada
    # en ningun lado -- revisar lo que escribió cada alumno exigía abrir su
    # notebook individual. Ahora es el mismo widget HTML/JS que las
    # reflexiones (`_ask_reflexion`), sin la llamada a DeepSeek: se otorga
    # 1 XP de participación si el texto no es un placeholder vacío, y el
    # texto crudo viaja dentro de `score_breakdown` en `submissions`
    # (columna JSON, no requiere migración) para poder revisarlo por SQL
    # sin entrar a cada Colab.

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
<div id="{uid}-wrap" style="background:#0c0a16;border:2px solid #5dd9ff;border-radius:4px;
  max-width:840px;margin:10px 0;overflow:hidden;box-shadow:0 6px 24px rgba(0,0,0,.7);">
  <div style="background:#5dd9ff18;border-bottom:1px solid #5dd9ff40;padding:10px 16px;
    display:flex;align-items:center;gap:8px;">
    {self._logo_tag_sm}
    <span style="font-family:'Press Start 2P',monospace;font-size:9px;color:#5dd9ff;
      letter-spacing:1px;">{icon} {label}</span>
  </div>
  <div style="padding:16px 18px;">
    <div style="color:#ece8f8;font-size:13px;line-height:1.6;margin-bottom:14px;">{question}</div>
    <textarea id="{uid}-text" rows="2" placeholder="Escribe aquí -- no hay respuesta incorrecta..."
      style="width:100%;box-sizing:border-box;background:#171130;border:2px solid #5dd9ff;
      border-radius:4px;color:#ece8f8;font-family:'Segoe UI',Roboto,sans-serif;
      font-size:13px;padding:10px 12px;resize:vertical;"></textarea>
    <button id="{uid}-btn" onclick="{uid}_submit()"
      style="margin-top:10px;padding:10px 20px;background:#5dd9ff;border:none;
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

    def check_prediccion_linea(self):
        """Predicción rápida sobre la línea roja del demo inicial -- participación (+1 XP), sin IA"""
        return self._ask_registro(
            "linea_roja",
            '¿Qué crees que hace esa línea roja? Escribe tu predicción en una frase.',
            icon="🔮", label="PREDICE")

    def check_anota_distancia(self):
        """En tus propias palabras -- qué significa minimizar la distancia (+1 XP), sin IA"""
        return self._ask_registro(
            "minimiza_distancia",
            'En tus propias palabras: ¿qué significa que la línea "minimice la distancia" a los puntos?',
            icon="📝", label="ANOTA")

    # ═══════════════════════════════════════════════════════════
    # TEORÍA — check_t1..check_t5 (formulario interactivo HTML)
    # ═══════════════════════════════════════════════════════════

    _TEORIA = {
        1: dict(
            title="T1 — ¿Qué significa R²?",
            q=("Tu modelo de regresión da R² = 0.72 en el set de prueba. ¿Qué significa "
               "exactamente ese número?"),
            opts={"a": "El 72% de las predicciones individuales fueron exactamente correctas",
                  "b": "El modelo explica (predice) alrededor del 72% de la variación real del resultado -- el otro 28% queda sin explicar por estas variables",
                  "c": "Hay un 72% de probabilidad de que la relación sea real y no producto del azar",
                  "d": "El modelo acierta el 72% de las veces si el resultado fuera categórico (sí/no)"},
            correct="b",
            why=("R² mide cuánta variación del resultado el modelo logra explicar con las "
                 "variables que le diste -- no es un porcentaje de aciertos exactos ni una "
                 "probabilidad de que la relación 'sea real'."),
            pts=5,
        ),
        2: dict(
            title="T2 — Train R² vs. Test R²",
            q=("¿Por qué el R² calculado sobre el set de **prueba** (test) importa más que el "
               "R² calculado sobre el set de **entrenamiento** (train)?"),
            opts={"a": "El R² de prueba siempre da más alto, así que se ve mejor en el reporte",
                  "b": "El de entrenamiento mide qué tan bien el modelo memorizó datos que ya vio; el de prueba mide si el modelo funciona con datos nuevos que nunca vio -- eso es lo que importa en la práctica",
                  "c": "El R² de prueba es más fácil de calcular en código",
                  "d": "El R² de entrenamiento solo aplica a clasificación, no a regresión"},
            correct="b",
            why=("Un modelo que solo funciona bien con datos que ya vio (memoriza) no sirve "
                 "para predecir nada nuevo -- el test R² es la prueba real de si aprendió un "
                 "patrón generalizable."),
            pts=5,
        ),
        3: dict(
            title="T3 — Agregas una variable inútil",
            q=("Agregas al modelo una variable que en realidad no tiene ninguna relación con "
               "lo que estás prediciendo. El R² de entrenamiento **sube**. El R² de prueba "
               "**baja**. ¿Qué te dice esto?"),
            opts={"a": "La variable inútil en realidad sí ayuda a predecir, solo que no lo sabías",
                  "b": "El modelo empezó a memorizar ruido específico del set de entrenamiento en vez de aprender un patrón real que se generalice -- esto se llama sobreajuste (overfitting)",
                  "c": "Hubo un error de cálculo -- si una variable no tiene relación real, ambos R² deberían quedar exactamente iguales",
                  "d": "Hay que agregar todavía más variables para corregirlo"},
            correct="b",
            why=("Más variables casi siempre suben el R² de entrenamiento (el modelo tiene más "
                 "formas de ajustarse a esos puntos exactos) -- pero si esas variables no "
                 "cargan información real, el modelo empeora prediciendo datos nuevos. Esa "
                 "brecha train-sube/test-baja es la señal clásica de sobreajuste."),
            pts=5,
        ),
        4: dict(
            title="T4 — Por qué la predicción absurda salió absurda",
            q=("El modelo de felicidad del ejemplo guiado tenía un R² de prueba decente "
               "(≈0.71). Pero al predecir con PBI per cápita = 10000 (el dato real más alto "
               "es ≈1.7) dio un Puntaje de miles de puntos, sin sentido. ¿Por qué pasó esto?"),
            opts={"a": "El modelo está mal entrenado -- si tuviera más datos, esa predicción sería razonable",
                  "b": "El modelo solo aprendió el patrón dentro del rango de datos que vio (0 a ≈1.7); fuera de ese rango, la línea recta simplemente se sigue extendiendo sin ningún control real -- eso es extrapolar",
                  "c": "PBI per cápita nunca debería usarse como predictor en ningún modelo",
                  "d": "Un R² alto garantiza predicciones razonables para cualquier valor de entrada, incluso fuera del rango de entrenamiento"},
            correct="b",
            why=("Un buen R² solo certifica que el modelo funciona bien *dentro* del rango de "
                 "datos con el que se entrenó. Extrapolar muy lejos de ese rango es pedirle al "
                 "modelo que adivine algo que nunca aprendió -- la línea sigue la misma "
                 "pendiente hasta el infinito, sin ningún freno real."),
            pts=5,
        ),
        5: dict(
            title="T5 — ¿Coeficiente más grande = más importante?",
            q=("En el ejemplo guiado, el coeficiente de \"Apoyo social\" (≈1.16) fue mayor que "
               "el de \"PBI per cápita\" (≈0.77). ¿Significa esto que \"Apoyo social\" es la "
               "variable más importante para predecir el Puntaje?"),
            opts={"a": "Sí, siempre -- el coeficiente más grande siempre indica la variable más importante",
                  "b": "No necesariamente -- las variables tienen escalas distintas (PBI per cápita va de 0 a ≈2, Apoyo social de 0 a ≈1), así que sus coeficientes no son directamente comparables sin más contexto",
                  "c": "No, los coeficientes nunca sirven para comparar variables entre sí, bajo ninguna circunstancia",
                  "d": "Sí, pero solo porque ambos coeficientes son positivos"},
            correct="b",
            why=("Comparar coeficientes crudos solo tiene sentido si las variables comparten "
                 "escala. PBI per cápita y Apoyo social se mueven en rangos distintos, así que "
                 "un coeficiente mayor puede simplemente reflejar que esa variable cambia en "
                 "pasos más chicos -- no que \"importe más\" para el modelo."),
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
                    f'margin-bottom:8px;background:#171130;border:2px solid #5dd9ff;'
                    f'border-radius:4px;color:#ece8f8;font-family:\'Segoe UI\',Roboto,sans-serif;'
                    f'font-size:13px;cursor:pointer;transition:all .15s;">'
                    f'<span style="font-family:\'Press Start 2P\',monospace;font-size:9px;'
                    f'color:#ffd166;margin-right:10px;">{L.upper()}</span>{spec["opts"][L]}</button>'
                )

            display(HTML(f'''
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
  .{uid}-opt:hover {{ border-color:#ffd166 !important; background:#1e1a0c !important; }}
</style>
<div id="{uid}-wrap" style="background:#0c0a16;border:2px solid #5dd9ff;border-radius:4px;
  max-width:840px;margin:10px 0;overflow:hidden;box-shadow:0 6px 24px rgba(0,0,0,.7);">
  <div style="background:#5dd9ff18;border-bottom:1px solid #5dd9ff40;padding:10px 16px;
    display:flex;align-items:center;gap:8px;">
    {self._logo_tag_sm}
    <span style="font-family:'Press Start 2P',monospace;font-size:9px;color:#5dd9ff;
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
    chosen.style.borderColor = '#ffd166';
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
        color = "#4caf50" if pts == max_pts else ("#ffd166" if pts > 0 else "#ff5d5d")
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
                'border:2px solid #b185f0;border-radius:4px;padding:14px 18px;'
                'font-family:\'Segoe UI\',Roboto,sans-serif;">'
                '<div style="font-family:\'Press Start 2P\',monospace;font-size:9px;'
                'color:#b185f0;letter-spacing:1px;margin-bottom:8px;">'
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
<div id="{uid}-wrap" style="background:#0c0a16;border:2px solid #5dd9ff;border-radius:4px;
  max-width:840px;margin:10px 0;overflow:hidden;box-shadow:0 6px 24px rgba(0,0,0,.7);">
  <div style="background:#5dd9ff18;border-bottom:1px solid #5dd9ff40;padding:10px 16px;
    display:flex;align-items:center;gap:8px;">
    {self._logo_tag_sm}
    <span style="font-family:'Press Start 2P',monospace;font-size:9px;color:#5dd9ff;
      letter-spacing:1px;">💭 REFLEXIONA</span>
  </div>
  <div style="padding:16px 18px;">
    <div style="color:#ece8f8;font-size:13px;line-height:1.6;margin-bottom:14px;">{question}</div>
    <textarea id="{uid}-text" rows="3" placeholder="Escribe tu reflexión aquí..."
      style="width:100%;box-sizing:border-box;background:#171130;border:2px solid #5dd9ff;
      border-radius:4px;color:#ece8f8;font-family:'Segoe UI',Roboto,sans-serif;
      font-size:13px;padding:10px 12px;resize:vertical;"></textarea>
    <button id="{uid}-btn" onclick="{uid}_submit()"
      style="margin-top:10px;padding:10px 20px;background:#5dd9ff;border:none;
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
            "Destello":       ("#6a5ea8", "rgba(106,94,168,.12)", "🌱"),
            "Fulgor":         ("#5dd9ff", "rgba(93,217,255,.12)", "🌙"),
            "Revelación":     ("#b185f0", "rgba(177,133,240,.10)", "✨"),
            "Visión Suprema": ("#9b5de5", "rgba(155,93,229,.15)",  "🔮"),
        }
        ach_html = ""
        for ach_name, _, ach_rarity in reg_ach:
            bc, bg, ach_icon = _RC.get(ach_rarity, _RC["Destello"])
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
            s_icon, s_text, s_color = "💭", f"+{pts} XP  ·  {max_pts - pts} por profundizar", "#ffd166"
            border_color, glow = "#b185f0", "0 0 22px rgba(255,183,3,.12)"
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
            f'border-left:3px solid #5dd9ff;border-radius:0 3px 3px 0;">'
            f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;color:#5dd9ff;">'
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
                             'font-size:6px;color:#5dd9ff;letter-spacing:1px;opacity:.85;">'
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
    <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#9b5de5;
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

    def check_reflexion_interpretacion(self):
        """Reflexión del ejemplo guiado (Felicidad) — interpretar coeficientes, sin causalidad (5 pts, IA)"""
        return self._ask_reflexion("nb5_interpretacion",
            'En el ejemplo guiado, el coeficiente de "PBI per cápita" fue ≈0.77 y el de '
            '"Apoyo social" ≈1.16. En 2-3 oraciones, en lenguaje simple: ¿qué significan '
            'estos números sobre cómo el modelo usa cada variable para predecir el '
            'Puntaje? Evita palabras como "causa" o "provoca".')

    # ═══════════════════════════════════════════════════════════
    # EJERCICIO 1 — Construye tu primer oráculo (Altura de atletas)
    # ═══════════════════════════════════════════════════════════

    def check_ex1(self):
        """Ex1 — Regresión propia: predecir Altura con 2-3 predictores (40 pts)"""
        self._header("EJERCICIO 1 — Construye tu Primer Oráculo 🔮", icon="🔮", pts=40)
        checks = []
        predictores_ex1     = _get("predictores_ex1")
        train_r2_ex1        = _get("train_r2_ex1")
        test_r2_ex1         = _get("test_r2_ex1")
        interpretacion_ex1  = _get("interpretacion_ex1")

        combo = _predictores_normalizados(predictores_ex1) if predictores_ex1 is not None else None

        if predictores_ex1 is None:
            checks.append((False, "predictores_ex1",
                           "No definida — usa una lista con 2 o 3 nombres de 'Edad', 'Peso', 'Sexo_num'"))
        elif combo is None:
            checks.append((False, "predictores_ex1",
                           f"'{predictores_ex1}' no es válida — elige 2 o 3 columnas distintas de 'Edad', 'Peso', 'Sexo_num'"))
        else:
            checks.append((True, f"predictores_ex1 = {list(predictores_ex1)}", "✓  Combinación válida"))

        if combo is None:
            checks.append((False, "train_r2_ex1", "No se puede verificar sin predictores_ex1 válidos"))
            checks.append((False, "test_r2_ex1", "No se puede verificar sin predictores_ex1 válidos"))
        else:
            exp_train, exp_test = _R2_LOOKUP[combo]

            if train_r2_ex1 is None:
                checks.append((False, "train_r2_ex1", "No definida"))
            elif not _is_number(train_r2_ex1):
                checks.append((False, "train_r2_ex1", f"Debe ser número, recibí {type(train_r2_ex1).__name__}"))
            elif _approx(train_r2_ex1, exp_train, tol=0.02):
                checks.append((True, f"train_r2_ex1 ≈ {exp_train:.3f}", "✓  Coincide con random_state=42"))
            else:
                checks.append((False, "train_r2_ex1",
                               f"Debe ser ≈{exp_train:.3f} para esa combinación (test_size=0.1, random_state=42), obtuve {train_r2_ex1}"))

            if test_r2_ex1 is None:
                checks.append((False, "test_r2_ex1", "No definida"))
            elif not _is_number(test_r2_ex1):
                checks.append((False, "test_r2_ex1", f"Debe ser número, recibí {type(test_r2_ex1).__name__}"))
            elif _approx(test_r2_ex1, exp_test, tol=0.02):
                checks.append((True, f"test_r2_ex1 ≈ {exp_test:.3f}", "✓  Coincide con random_state=42"))
            else:
                checks.append((False, "test_r2_ex1",
                               f"Debe ser ≈{exp_test:.3f} para esa combinación (test_size=0.1, random_state=42), obtuve {test_r2_ex1}"))

        predictor_names = predictores_ex1 if isinstance(predictores_ex1, (list, tuple)) else []

        if not _is_nontrivial_text(interpretacion_ex1, min_len=15):
            checks.append((False, "interpretacion_ex1",
                           "Escribe 1-2 oraciones interpretando tus coeficientes -- no dejes '___' ni una frase de una palabra"))
        elif _contiene_lenguaje_causal(interpretacion_ex1):
            checks.append((False, "interpretacion_ex1",
                           "Evita palabras causales ('causa', 'provoca', 'hace que') -- describe la relación, no una causa"))
        elif predictor_names and not _menciona_predictor_o_numero(interpretacion_ex1, predictor_names):
            checks.append((False, "interpretacion_ex1",
                           "Menciona al menos uno de tus predictores (ej. 'Peso', 'Edad') o un número de tu propio resultado -- no una frase genérica que serviría para cualquier modelo"))
        else:
            checks.append((True, "interpretacion_ex1", "✓  Interpretación presente, sin lenguaje causal"))

        return self._award("ex1", checks, 40)

    # ═══════════════════════════════════════════════════════════
    # CHECKPOINT — mitad de Semana 6
    # ═══════════════════════════════════════════════════════════

    def check_mini_a(self):
        """Checkpoint — mitad de Semana 6, justo tras el Ejercicio 1"""
        self._checkpoints.add("mini_a")
        seccion = {
            "ex1": ("Ejercicio 1 – Tu primer oráculo (Altura de atletas)", 40),
        }
        self._render_checkpoint("CHECKPOINT — MITAD DE SEMANA 6", seccion, "#5dd9ff")

    # ═══════════════════════════════════════════════════════════
    # EJERCICIO 2 — Optimiza: explora combinaciones, quédate con la mejor
    # ═══════════════════════════════════════════════════════════

    def check_ex2(self):
        """Ex2 — Explora 2-3 combinaciones, reporta tu mejor R² de prueba (20 pts)"""
        self._header("EJERCICIO 2 — Optimiza tu Oráculo 📈", icon="📈", pts=20)
        checks = []
        combo_ex2          = _get("combo_ex2")
        mejor_test_r2_ex2  = _get("mejor_test_r2_ex2")

        combo = _predictores_normalizados(combo_ex2) if combo_ex2 is not None else None

        if combo_ex2 is None:
            checks.append((False, "combo_ex2",
                           "No definida — la combinación de predictores que te dio el mejor R² de prueba"))
        elif combo is None:
            checks.append((False, "combo_ex2",
                           f"'{combo_ex2}' no es válida — 2 o 3 columnas distintas de 'Edad', 'Peso', 'Sexo_num'"))
        else:
            checks.append((True, f"combo_ex2 = {list(combo_ex2)}", "✓  Combinación válida"))

        if combo is None:
            checks.append((False, "mejor_test_r2_ex2", "No se puede verificar sin combo_ex2 válida"))
        else:
            exp_train, exp_test = _R2_LOOKUP[combo]
            if mejor_test_r2_ex2 is None:
                checks.append((False, "mejor_test_r2_ex2", "No definida"))
            elif not _is_number(mejor_test_r2_ex2):
                checks.append((False, "mejor_test_r2_ex2", f"Debe ser número, recibí {type(mejor_test_r2_ex2).__name__}"))
            elif _approx(mejor_test_r2_ex2, exp_test, tol=0.02):
                checks.append((True, f"mejor_test_r2_ex2 ≈ {exp_test:.3f}", "✓  Coincide con esa combinación"))
            else:
                checks.append((False, "mejor_test_r2_ex2",
                               f"Debe ser ≈{exp_test:.3f} para esa combinación, obtuve {mejor_test_r2_ex2}"))

        return self._award("ex2", checks, 20)

    def check_reflexion_ex2(self):
        """Reflexión Ex2 — por qué esa combinación funcionó mejor (5 pts, IA)"""
        return self._ask_reflexion("nb5_ex2",
            'De las combinaciones que probaste para predecir Altura, ¿cuál dio el mejor '
            'R² de prueba? En 1-2 oraciones: ¿por qué crees que esas variables funcionan '
            'mejor para predecir la estatura de un atleta?')

    # ═══════════════════════════════════════════════════════════
    # RETO 1 (bonus) — Rompe tu propio oráculo
    # ═══════════════════════════════════════════════════════════

    def check_reto1(self):
        """Reto 1 (bonus) — extrapolar con una entrada absurda (10 pts, fuera del core)"""
        self._header("🎯 RETO — Rompe el Oráculo", icon="💥", pts=10)
        checks = []
        prediccion_absurda_reto1   = _get("prediccion_absurda_reto1")
        descripcion_absurda_reto1  = _get("descripcion_absurda_reto1")

        if prediccion_absurda_reto1 is None:
            checks.append((False, "prediccion_absurda_reto1",
                           "No definida — usa tu modelo para predecir Altura con una entrada muy fuera de rango (ej. Edad=200, Peso=1000)"))
        elif not _is_number(prediccion_absurda_reto1):
            checks.append((False, "prediccion_absurda_reto1", f"Debe ser número, recibí {type(prediccion_absurda_reto1).__name__}"))
        else:
            checks.append((True, f"prediccion_absurda_reto1 = {prediccion_absurda_reto1:.1f}", "✓  Predicción calculada"))

        if not _is_nontrivial_text(descripcion_absurda_reto1, min_len=10):
            checks.append((False, "descripcion_absurda_reto1",
                           "Escribe en 1 frase qué entrada absurda usaste y por qué esa predicción no tiene sentido"))
        else:
            checks.append((True, "descripcion_absurda_reto1", "✓  Descripción presente"))

        return self._award("reto1", checks, 10)

    def check_reflexion_final(self):
        """Reflexión de cierre — cuándo usarías esto (5 pts, IA)"""
        return self._ask_reflexion("nb5_final",
            'Ya construiste modelos de regresión en dos datasets totalmente distintos '
            '(puntajes de felicidad, estaturas de atletas). En 2-4 oraciones: ¿cuándo '
            'usarías una herramienta así? ¿qué preguntas podrías responder con un '
            'modelo de predicción como este?')

    # ═══════════════════════════════════════════════════════════
    # CHECKPOINT — fin de la Semana 6 / Misión 3
    # ═══════════════════════════════════════════════════════════

    def check_mini_b(self):
        """Checkpoint — fin de la Semana 6 y de la Misión 3"""
        self._checkpoints.add("mini_b")
        if len(self._checkpoints) >= 2 and self._unlock("medalla_oraculo"):
            display(HTML(
                f'<div style="display:flex;align-items:center;gap:8px;'
                f'font-family:\'Press Start 2P\',monospace;font-size:8px;'
                f'color:#b185f0;background:#1a1030;border:1px solid #b185f0;'
                f'border-radius:3px;padding:12px 16px;max-width:840px;margin:6px 0;">'
                f'{self._logo_tag_sm}'
                f'<span>✨ LOGRO: Medalla del Oráculo — Ambos checkpoints de Semana 6 superados</span></div>'
            ))
        seccion = {
            "t1": ("T1 – Qué significa R²", 5),
            "t2": ("T2 – Train R² vs. test R²", 5),
            "t3": ("T3 – Variable inútil y sobreajuste", 5),
            "t4": ("T4 – Por qué la extrapolación falla", 5),
            "t5": ("T5 – Coeficiente más grande ≠ más importante", 5),
            "ex2": ("Ejercicio 2 – Optimiza tu oráculo", 20),
        }
        self._render_checkpoint("CHECKPOINT — FIN DE LA MISIÓN 3", seccion, "#9b5de5")

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
            final_msg = f"🏆 ORÁCULO SUPREMO. {n.upper()}, tu nombre entra al Salón de la Fama de la Misión 3."
        elif pct >= 81:
            final_msg = f"🔮 VIDENTE DE DATOS. {n}, ya sabes construir un modelo y leer sus límites. Sigue así."
        elif pct >= 61:
            final_msg = f"📈 TRAZADOR DE LÍNEAS. {n}, tu modelo ya predice de verdad. ¡Sigue así!"
        elif pct >= 41:
            final_msg = f"✨ LECTOR DE PATRONES. {n}, los coeficientes empiezan a tener sentido. Revisa los ✖ para avanzar."
        elif pct >= 21:
            final_msg = f"🌙 PRIMERA VISIÓN. {n}, toda predicción empieza así. Relee la teoría y vuelve a intentar."
        else:
            final_msg = f"🌱 {n}, tu camino como oráculo de datos sigue. Cada celda ejecutada es un paso hacia adelante."

        ach_display = {
            "primera_vision":        "🔮 Primera Visión",
            "constructor_de_modelos": "🏗️ Constructor de Modelos",
            "optimizador":            "📈 Optimizador",
            "rompe_modelos":          "💥 Rompe-Modelos",
            "medalla_oraculo":        "✨ Medalla del Oráculo",
            "racha_predictiva":       "🔥 Racha Predictiva",
            "vision_completa":        "🏆 Visión Completa",
        }

        ach_html = ""
        if self._achievements:
            for ak, alabel in ach_display.items():
                if ak in self._achievements:
                    ach_html += (
                        f'<div style="display:inline-flex;align-items:center;gap:5px;'
                        f'padding:3px 8px;background:rgba(255,209,102,.08);'
                        f'border:1px solid #ffd16640;border-radius:2px;margin:2px;">'
                        f'<span style="font-family:\'Press Start 2P\',monospace;font-size:6px;'
                        f'color:#ffd166;">{alabel}</span></div>'
                    )

        lv_color = _lv_color(lvl_num)
        xp_grad  = _XP_GRAD.get(lvl_num, _XP_GRAD[1])

        self._submit_to_supabase(core_earned, _CORE_MAX, pct, lvl_num, lvl_name)

        display(HTML(f'''
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
  @keyframes pk-glow{{0%,100%{{text-shadow:0 0 14px rgba(255,209,102,.8),2px 2px 0 #5a3d99}}
    50%{{text-shadow:0 0 32px rgba(255,209,102,1),0 0 60px rgba(255,158,44,.5),2px 2px 0 #5a3d99}}}}
  @keyframes pk-xp{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
</style>
<div style="background:#0c0a16;border:2px solid #ffd166;border-radius:6px;max-width:840px;
  margin:12px 0;overflow:hidden;
  box-shadow:0 0 40px rgba(255,209,102,.15),0 0 80px rgba(255,158,44,.08),0 10px 40px rgba(0,0,0,.8);">

  <div style="background:linear-gradient(135deg,#0c0a16,#1a1436,#0c0a16);
    border-bottom:2px solid #ffd166;padding:22px 28px;text-align:center;position:relative;">
    <div style="position:absolute;left:20px;top:50%;transform:translateY(-50%);">{self._logo_tag}</div>
    <div style="font-family:'Press Start 2P',monospace;font-size:clamp(13px,2.8vw,20px);
      color:#ffd166;animation:pk-glow 2.5s ease-in-out infinite;letter-spacing:3px;
      margin-bottom:8px;">🔮 MISIÓN 3: EL ORÁCULO DE DATOS 📈</div>
    <div style="font-family:'Press Start 2P',monospace;font-size:8px;color:#9b5de5;
      letter-spacing:2px;">SEMANA 6 — RESUMEN FINAL</div>
    <div style="position:absolute;right:20px;top:50%;transform:translateY(-50%);">{self._logo_tag}</div>
  </div>

  <div style="padding:24px 28px;">
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:20px;">
      <div style="background:#0f0c1e;border:1px solid #241f3d;border-radius:3px;
        padding:16px;text-align:center;">
        <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#7a72a0;
          letter-spacing:1px;margin-bottom:10px;">XP TOTAL</div>
        <div style="font-family:'Press Start 2P',monospace;font-size:clamp(14px,3vw,22px);
          color:#ffd166;">{core_earned}/{_CORE_MAX}</div>
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

    <div style="background:#0f0c1e;border:1px solid #5dd9ff;border-radius:3px;
      padding:14px 18px;margin-bottom:20px;text-align:center;">
      <div style="font-size:13px;color:#ece8f8;line-height:1.7;">{final_msg}</div>
    </div>

    {f'''
    <div style="text-align:center;margin-bottom:20px;font-family:'Press Start 2P',monospace;
      font-size:7px;color:#ffd166;letter-spacing:1px;">
      💥 BONUS — Rompe el Oráculo: {bonus_earned}/{_BONUS_MAX} XP (no cuenta para el nivel)
    </div>''' if "reto1" in self._scores else ""}

    {f"""
    <div style="margin-bottom:16px;">
      <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#7a72a0;
        letter-spacing:1px;margin-bottom:10px;">🔮 LOGROS DESBLOQUEADOS</div>
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
      color:#5dd9ff;letter-spacing:1px;opacity:.9;">
      📊 Calificación final enviada al leaderboard · {n} · {lvl_name}
    </div>"""}
  </div>
</div>'''))

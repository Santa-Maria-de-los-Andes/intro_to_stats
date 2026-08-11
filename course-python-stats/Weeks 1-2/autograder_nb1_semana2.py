"""
Autograder — Bimestre 3, Mision 1: Recuperacion de Datos — SEMANA 2
JUEGOS OLIMPICOS EDITION — Del Podio de Entrenamiento al Record Olimpico

Cubre: check_ex0-ex6, check_debug0-3, check_t0-t4, check_intex0-4, check_reto1,
check_mini_c, check_mini_d, resumen()
Dataset: athlete_events_es.csv (271116 filas x 15 columnas)

Companion file: autograder_nb1_semana1.py (ex1-5, debug1, t1-9, mini_a/mini_b) —
mismo tema-hermano (Pokemon la semana pasada, Juegos Olimpicos esta semana), pero
Semana 2 es una tarea independiente con numeracion propia reiniciada en 0
(decision del usuario, 2026-08-11 — ver WORKFORCE_HANDOFF.md). Comparten el mismo
motor visual (tarjetas HTML, niveles, logros, checkpoints, Supabase) descrito en
autograder_nb1_semana1.py; aqui solo cambia el skin (colores/iconos/copy) y, claro,
toda la logica de grading (dataset y ejercicios distintos).

Notas de scoring (ATLAS, ticket #10/#11 — WORKFORCE_HANDOFF.md, 2026-08-11):
  Los puntos de cada check_exN/check_debugN/check_intexN son los que YA aparecen
  impresos en el markdown del notebook — no son negociables aqui (ex0=10, ex1=10,
  ex2=10, ex3=12, ex4=12, ex5=11, ex6=12 => 77; debug0-3=10 c/u => 40; intex0=8,
  intex1=8, intex2=7, intex3=5, intex4=7 => 35). Los 5 check_tN (t0-t4) NO tienen
  puntaje fijado en el notebook ni en Preguntas_Teoricas_Semanas1-2.md Bloque 5 —
  siguiendo el mismo criterio que Semana 1 (5 pts/pregunta, ver ese archivo), se
  fijan en 5 pts c/u => 25. Total _CORE_MAX = 77+40+35+25 = 177. Esto excede la
  estimacion original de "~135-160" que el ticket #11 dejo anotada antes de que
  Integracion creciera de 2 a 5 items el 2026-08-11 — se resuelve subiendo el techo
  (mismo criterio que Semana 1), no recortando contenido ya escrito y verificado.
  `reto1` es bonus, fuera de _CORE_MAX: al ser un hallazgo completamente abierto
  (el estudiante elige su propio filtro+groupby), no tiene un valor numerico unico
  que verificar — se califica por evidencia de esfuerzo genuino (variable no vacia,
  no el placeholder "___", longitud minima), igual que un criterio "effort-derivable"
  de una rubrica humana. _BONUS_MAX = 10.

  Ambiguedad de spec resuelta (ATLAS): el enunciado de Integracion 1 dice "Resta
  ambos promedios" sin fijar el orden — el nombre de variable
  (`diferencia_edad_basket_gimnasia`) sugiere basket - gimnasia, pero exigir ese
  signo exacto rechazaria una resta en el otro orden que es igual de correcta
  aritmeticamente. `check_intex1` acepta ambos signos (valor absoluto) para no
  generar un falso rechazo por una eleccion de orden que el enunciado no fuerza.

  Valores esperados para cada check numerico fueron calculados directamente contra
  `athlete_events_es.csv` real (271116 filas), no estimados — ver el bloque de
  constantes `_EXP_*` mas abajo para cada uno.

Nota Supabase: mismo proyecto/tabla `submissions` que Semana 1 (y NB2/NB3), pero
`notebook="nb1_semana2"` (distinto de `"nb1_semana1"`) para que el lookup de
"tu mejor marca" del formulario de registro no mezcle ambas sesiones — cada semana
es su propia fila en el leaderboard. Mismo campo `"curso": "STAT_2026"`.

Nota de fecha limite: se asume cadencia semanal (una semana despues del deadline de
Semana 1, 2026-08-17 04:59 UTC) => 2026-08-24 04:59 UTC. Es un valor por defecto
razonable dado el patron de la Semana 1, no una fecha confirmada por el usuario —
quien tenga la fecha real de la Clase 2 debe ajustar `_DEADLINE_UTC` antes de
publicar este archivo.
"""

import sys
import re
import unicodedata
import datetime as _dt
from IPython.display import HTML, display

try:
    import pandas as pd
except ImportError:
    pd = None

# ─── Supabase Config (mismo proyecto que Semana 1/NB2/NB3) ────
SUPABASE_URL      = "https://uwykikwutjtkpffwmdiq.supabase.co"
SUPABASE_ANON_KEY = "sb_publishable_aBG6GD4wn9CgpSE-47fagQ_sNhnzznu"
LOGO_URL          = "https://raw.githubusercontent.com/Santa-Maria-de-los-Andes/CS1---Grader/main/icono%20SMA.png"
CURSO_ID          = "STAT_2026"
NOTEBOOK_ID       = "nb1_semana2"

# ─── Deadline: 23 agosto 2026, 11:59 PM Peru (UTC-5) = 24 agosto 04:59 UTC ────
# (asumido por cadencia semanal — ver nota en el docstring del modulo)
_DEADLINE_UTC   = _dt.datetime(2026, 8, 24, 4, 59, 0, tzinfo=_dt.timezone.utc)
DEADLINE_PASSED = _dt.datetime.now(_dt.timezone.utc) >= _DEADLINE_UTC

# ─── Scoring ─────────────────────────────────────────────────
_CORE_MAX  = 177   # 77 (ex0-6) + 40 (debug0-3) + 35 (intex0-4) + 25 (5 teoria x 5)
_BONUS_MAX = 10    # reto1 (unico item bonus, hallazgo abierto)

# ─── Niveles Olimpicos (por % del score core) ──────────────────
_LEVELS = [
    (96, 6, "🏆 Récord Olímpico"),
    (81, 5, "🥇 Medalla de Oro"),
    (61, 4, "🥈 Medalla de Plata"),
    (41, 3, "🥉 Medalla de Bronce"),
    (21, 2, "🏃 Atleta en Entrenamiento"),
    (0,  1, "🌱 Novato en la Villa Olímpica"),
]

_XP_GRAD = {
    1: "linear-gradient(90deg,#333344,#666688)",
    2: "linear-gradient(90deg,#7a4a10,#ff8c42)",
    3: "linear-gradient(90deg,#6a3d1a,#cd7f32)",
    4: "linear-gradient(90deg,#5a5a66,#d8d8e6)",
    5: "linear-gradient(90deg,#7a5c00,#ffd700)",
    6: "linear-gradient(90deg,#df0024,#ffd700,#0081C8)",
}
_LV_CSS_COLOR = {1: "#8899aa", 2: "#ff8c42", 3: "#cd7f32", 4: "#d8d8e6", 5: "#ffd700", 6: "#0081C8"}


def _level_info(pct):
    for thresh, num, name in _LEVELS:
        if pct >= thresh:
            return num, name
    return 1, "🌱 Novato en la Villa Olímpica"


def _lv_color(n):
    return _LV_CSS_COLOR.get(n, "#8899aa")


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


def _is_int_like(v):
    if isinstance(v, bool):
        return False
    try:
        return float(v) == int(v)
    except (TypeError, ValueError):
        return False


def _is_dataframe(v):
    return pd is not None and isinstance(v, pd.DataFrame)


def _is_series(v):
    return pd is not None and isinstance(v, pd.Series)


def _is_nontrivial_text(v, min_len=15):
    if not isinstance(v, str):
        return False
    t = v.strip().strip('"').strip("'").strip()
    if t in ("", "___", "?", "..."):
        return False
    return len(t) >= min_len


def _series_check(val, expected, tol=0.06):
    """Compara una Serie/dict de resultado de groupby contra valores esperados
    para un subconjunto de categorias (no exige que sean las UNICAS categorias)."""
    if val is None:
        return False, "No definida"
    if _is_series(val):
        data = val.to_dict()
    elif isinstance(val, dict):
        data = val
    else:
        return False, f"Debe ser una Series (resultado de .groupby()...), recibí {type(val).__name__}"

    missing = [k for k in expected if k not in data]
    if missing:
        return False, f"Faltan categorías esperadas: {', '.join(missing)}"

    bad = []
    for k, exp in expected.items():
        v = data[k]
        if not _is_number(v) or not _approx(v, exp, tol=tol):
            bad.append(f"{k}≈{exp:.2f} (obtuve {v})")
    if bad:
        return False, "Valores incorrectos — " + "; ".join(bad)
    return True, "✓"


# ─── Main Class ──────────────────────────────────────────────

class Autograder:

    def __init__(self):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass
        self._scores       = {}
        self._achievements = set()
        self._streak       = 0
        self._prev_level   = 0
        self._email        = None
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
                    'color:#ffd700;letter-spacing:2px;">SMA</span>')

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
                    _qurl = (
                        f"{SUPABASE_URL}/rest/v1/submissions"
                        f"?select=earned,possible,pct,level_name,streak"
                        f"&dni=eq.{_up2.quote(str(dni), safe='')}"
                        f"&notebook=eq.{NOTEBOOK_ID}"
                        f"&order=pct.desc,submitted_at.desc&limit=1"
                    )
                    _req2 = _ur2.Request(_qurl, headers={
                        "apikey": SUPABASE_ANON_KEY,
                        "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
                    })
                    with _ur2.urlopen(_req2, timeout=8) as _resp2:
                        _rows = _json2.loads(_resp2.read())
                    if _rows:
                        _best = _rows[0]
                except Exception:
                    pass

                if _best:
                    _score_html = f'''
  <div style="background:#0a0e14;border:1px solid #0081C8;border-radius:3px;
    padding:12px 20px;margin-top:6px;
    font-family:'Press Start 2P',monospace;animation:ag-fadein .4s ease .1s both;">
    <div style="font-size:6px;color:#0081C8;letter-spacing:2px;margin-bottom:10px;">
      🏅 TU MEJOR MARCA — SEMANA 2</div>
    <div style="display:flex;align-items:center;gap:20px;">
      <div style="font-size:28px;color:#ffd700;
        text-shadow:0 0 16px rgba(255,215,0,.8),2px 2px 0 #7a5c00;">
        {_best['pct']}%</div>
      <div>
        <div style="font-size:8px;color:#df0024;letter-spacing:1px;">{_best['level_name']}</div>
        <div style="font-size:6px;color:#8899bb;margin-top:6px;letter-spacing:1px;">
          {_best['earned']} / {_best['possible']} XP</div>
      </div>
    </div>
  </div>'''
                else:
                    _score_html = (
                        '<div style="background:#0a0e14;border:1px solid #1a2233;border-radius:3px;'
                        'padding:10px 20px;margin-top:6px;'
                        'font-family:\'Press Start 2P\',monospace;font-size:6px;color:#555566;'
                        'letter-spacing:1px;animation:ag-fadein .4s ease .1s both;">'
                        '🏅 Primera vuelta a la pista — ¡aun no tienes marca registrada!</div>'
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
  <div style="background:#12100a;border:1px solid #ffd700;border-radius:3px;padding:12px 18px;
    font-family:'Press Start 2P',monospace;font-size:8px;
    color:#ffd700;letter-spacing:1px;animation:ag-fadein .4s ease;">
    🏅 &nbsp;¡BIENVENIDO, ATLETA {nombre.upper()}! &nbsp;·&nbsp; {grado}
  </div>
  {_score_html}
  <div id="ag-loading" style="background:#0a0e14;border:1px solid #1a2233;border-radius:3px;
    padding:22px 18px;margin-top:6px;text-align:center;animation:ag-fadein .5s ease .2s both;">
    <div style="display:flex;justify-content:center;gap:6px;margin-bottom:12px;">
      <div style="width:8px;height:8px;border-radius:50%;background:#df0024;
        animation:ag-dot 1.2s ease-in-out 0s infinite;"></div>
      <div style="width:8px;height:8px;border-radius:50%;background:#ffd700;
        animation:ag-dot 1.2s ease-in-out .2s infinite;"></div>
      <div style="width:8px;height:8px;border-radius:50%;background:#0081C8;
        animation:ag-dot 1.2s ease-in-out .4s infinite;"></div>
    </div>
    <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#555566;letter-spacing:2px;">
      CARGANDO MARCADOR OLÍMPICO…
    </div>
  </div>
  <div id="ag-start" style="display:none;background:linear-gradient(160deg,#0a0e14,#12060a);
    border:2px solid #ffd700;border-radius:4px;padding:36px 24px;margin-top:6px;text-align:center;
    box-shadow:0 0 40px rgba(255,215,0,.25),0 0 80px rgba(0,129,200,.08),0 6px 24px rgba(0,0,0,.9);">
    <div style="font-size:44px;margin-bottom:14px;animation:ag-start .55s cubic-bezier(.34,1.56,.64,1);">🏅</div>
    <div style="font-family:'Press Start 2P',monospace;font-size:clamp(15px,3.6vw,26px);color:#ffd700;
      letter-spacing:4px;text-shadow:0 0 24px rgba(255,215,0,.95),0 0 50px rgba(223,0,36,.35),
      2px 2px 0 #7a5c00;animation:ag-start .6s ease;margin-bottom:14px;">¡LOS JUEGOS COMIENZAN!</div>
    <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#0081C8;
      letter-spacing:2px;opacity:.85;margin-bottom:16px;">EJECUTA LA PRIMERA CELDA PARA COMENZAR</div>
    <div style="font-size:15px;opacity:.55;letter-spacing:8px;">🔵 🟡 ⚫ 🟢 🔴</div>
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
            _out.register_callback('_ag_intex3_answer', self._grade_intex3)

            display(HTML(f'''
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
  .ag-input,.ag-select {{
    width:100%;box-sizing:border-box;background:#0a0e14;border:1px solid #1a2233;
    border-radius:3px;padding:0 12px;color:#f0ece0;font-size:13px;height:42px;
    font-family:'Segoe UI',Roboto,sans-serif;outline:none;transition:border .2s;
  }}
  .ag-input:focus,.ag-select:focus {{ border-color:#0081C8; }}
  .ag-select option {{ background:#0a0e14; }}
  .ag-btn {{
    width:100%;padding:13px;background:linear-gradient(90deg,#0060a0,#0081C8);
    border:none;border-radius:3px;color:#ffd700;font-family:'Press Start 2P',monospace;
    font-size:9px;letter-spacing:2px;cursor:pointer;transition:opacity .2s;margin-top:6px;
  }}
  .ag-btn:hover {{ opacity:.85; }}
  .ag-err {{ color:#ff5555;font-size:11px;margin-top:6px;display:none; }}
  .ag-label {{ font-family:'Press Start 2P',monospace;font-size:7px;letter-spacing:1px;
    margin-bottom:8px;display:flex;align-items:center;gap:5px; }}
  .ag-field {{ display:flex;flex-direction:column; }}
</style>
<div style="background:#0a0e14;border:2px solid #0081C8;border-radius:4px;max-width:840px;
  margin:10px 0;overflow:hidden;box-shadow:0 0 40px rgba(0,129,200,.2),0 10px 30px rgba(0,0,0,.8);">

  <div style="background:linear-gradient(90deg,#0a0e14,#12060a,#0a0e14);border-bottom:2px solid #ffd700;
    padding:18px 24px;position:relative;display:flex;align-items:center;justify-content:center;min-height:80px;">
    <div style="position:absolute;left:20px;top:50%;transform:translateY(-50%);">{logo_tag}</div>
    <div style="text-align:center;">
      <div style="font-family:'Press Start 2P',monospace;font-size:clamp(13px,3vw,18px);color:#ffd700;letter-spacing:3px;
        text-shadow:0 0 14px rgba(255,215,0,.7),2px 2px 0 #7a5c00;">🏅 MISIÓN 1: DATOS 🏅</div>
      <div style="font-family:'Press Start 2P',monospace;font-size:8px;color:#df0024;
        letter-spacing:2px;margin-top:8px;">SEMANA 2 — MODO ATLETA</div>
    </div>
    <div style="position:absolute;right:20px;top:50%;transform:translateY(-50%);">{logo_tag}</div>
  </div>

  <div style="padding:24px;">
    <div style="display:grid;grid-template-columns:2fr 1fr;gap:14px;margin-bottom:14px;align-items:end;">
      <div class="ag-field">
        <div class="ag-label" style="color:#df0024;">🏅 NOMBRE COMPLETO</div>
        <input id="ag-nombre" class="ag-input" placeholder="Tu nombre y apellido" />
      </div>
      <div class="ag-field">
        <div class="ag-label" style="color:#df0024;">🏫 GRADO</div>
        <select id="ag-grado" class="ag-select">
          <option value="">— Selecciona —</option>
          <option value="3ro">3ro</option>
          <option value="4to">4to</option>
          <option value="5to">5to</option>
        </select>
      </div>
    </div>
    <div class="ag-field" style="margin-bottom:14px;">
      <div class="ag-label" style="color:#ffd700;">🪪 CÓDIGO DE ESTUDIANTE (DNI, Pasaporte, Carnet)</div>
      <input id="ag-dni" class="ag-input" placeholder="Ingresa tu código" />
    </div>
    <div id="ag-err" class="ag-err">⚠ Por favor completa todos los campos.</div>
    <button class="ag-btn" onclick="agRegister()">🏅 &nbsp; ¡ENTRAR AL ESTADIO! &nbsp; 🏅</button>
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
                display(HTML('<div style="font-family:monospace;padding:10px;background:#0a0e14;'
                             'color:#ffd700;border:1px solid #0081C8;border-radius:3px;max-width:840px;">'
                             '🏅 MISIÓN 1 — SEMANA 2 — Registro</div>'))
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
        return '<span style="font-family:\'Press Start 2P\',monospace;font-size:11px;color:#ffd700;">SMA</span>'

    @property
    def _logo_tag_sm(self):
        if LOGO_URL:
            return (f'<img src="{LOGO_URL}" style="height:24px;object-fit:contain;" '
                    f'onerror="this.style.display=\'none\'">')
        return '<span style="font-family:\'Press Start 2P\',monospace;font-size:8px;color:#ffd700;">SMA</span>'

    def _nombre(self):
        if self._nombre_real:
            return self._nombre_real
        n = _get("nombre")
        if isinstance(n, str) and n.strip() and n.strip() not in ("?", ""):
            return n.strip()
        return "atleta"

    def _totals(self):
        earned   = sum(e for e, _ in self._scores.values())
        possible = sum(p for _, p in self._scores.values())
        pct      = min(round(earned / _CORE_MAX * 100), 100)
        return earned, possible, pct

    def _unlock(self, key):
        if key not in self._achievements:
            self._achievements.add(key)
            return True
        return False

    def _header(self, title, icon="🏅", pts=None):
        self._curr_title = title
        self._curr_icon  = icon
        self._curr_pts   = pts

    def _check_achievements(self, key):
        unlocked = []
        earned, possible, pct = self._totals()

        # Primera Medalla — primer XP ganado
        if any(e > 0 for e, _ in self._scores.values()) and self._unlock("primera_medalla"):
            unlocked.append(("🥉 Primera Medalla — ¡Tu primer punto en el podio!", "#cd7f32", "Bronce"))

        # Relevo Perfecto — ex0-ex3 (recap + Seccion C) todos perfectos
        ex_keys = ["ex0", "ex1", "ex2", "ex3"]
        if (all(k in self._scores and self._scores[k][0] == self._scores[k][1] for k in ex_keys)
                and self._unlock("relevo_perfecto")):
            unlocked.append(("🥇 Relevo Perfecto — Los 4 primeros ejercicios sin fallos", "#4caf50", "Oro"))

        # Muralla Defensiva — los 4 debugs perfectos
        debug_keys = ["debug0", "debug1", "debug2", "debug3"]
        if (all(k in self._scores and self._scores[k][0] == self._scores[k][1] for k in debug_keys)
                and self._unlock("muralla_defensiva")):
            unlocked.append(("🛡️ Muralla Defensiva — Los 4 debugs corregidos sin errores", "#d8d8e6", "Plata"))

        # Doble Podio — ambos checkpoints alcanzados
        if len(self._checkpoints) >= 2 and self._unlock("doble_podio"):
            unlocked.append(("🎖️ Doble Podio — Ambos checkpoints superados", "#ffd700", "Oro"))

        # Racha de Relevos — racha >= 5
        if self._streak >= 5 and self._unlock("racha_de_relevos"):
            unlocked.append(("🔥 Racha de Relevos — Combo x5", "#df0024", "Plata"))

        # Juegos Completos — 100% del core
        if pct >= 100 and self._unlock("juegos_completos"):
            unlocked.append(("🏆 Juegos Completos — 100% de la Semana 2", "#0081C8", "Récord"))

        # Level-up
        lvl_num, lvl_name = _level_info(pct)
        if lvl_num > self._prev_level and self._prev_level > 0:
            unlocked.append((f"⬆️ ¡SUBISTE DE NIVEL! — {lvl_name}", "#0081C8", "Nivel"))
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
                    f'<span style="color:#a0a0bb;">{msg}</span></div></div>'
                )
            else:
                rows_html += (
                    f'<div style="display:flex;align-items:flex-start;gap:10px;padding:7px 10px;'
                    f'margin-bottom:3px;background:rgba(223,0,36,.06);'
                    f'border-left:3px solid #df0024;border-radius:0 3px 3px 0;">'
                    f'<span style="color:#df0024;font-size:13px;flex-shrink:0;line-height:1.5;">✖</span>'
                    f'<div style="font-size:11px;line-height:1.5;">'
                    f'<span style="color:#df0024;font-weight:bold;">{label}:</span> '
                    f'<span style="color:#cc8888;">{msg}</span></div></div>'
                )

        star_r = pts / max_pts if max_pts > 0 else 0
        gold, dark = "#ffd700", "#2a2200"
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
            c_color = "#df0024" if self._streak >= 5 else "#ffd700"
            combo_html = (
                f'<div style="display:inline-flex;align-items:center;gap:5px;padding:3px 10px;'
                f'background:rgba(223,0,36,.12);border:1px solid {c_color};border-radius:2px;'
                f'margin-left:8px;">'
                f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;'
                f'color:{c_color};">🔥 COMBO x{self._streak}</span></div>'
            )

        if pts == max_pts:
            s_icon, s_text, s_color = "🥇", f"¡PODIO! +{pts} XP", "#4caf50"
            border_color, glow = "#4caf50", "0 0 22px rgba(76,175,80,.15)"
        elif pts > 0:
            s_icon, s_text, s_color = "🎯", f"+{pts} XP  ·  {max_pts - pts} por ganar", "#ffd700"
            border_color, glow = "#ffd700", "0 0 22px rgba(255,215,0,.12)"
        else:
            s_icon, s_text, s_color = "🚫", "¡FUERA DE PISTA! — Corrige los ✖ e intenta de nuevo", "#df0024"
            border_color, glow = "#df0024", "0 0 22px rgba(223,0,36,.15)"

        xp_grad = _XP_GRAD.get(lvl_num, _XP_GRAD[1])

        dots = "".join(
            f'<span style="display:inline-block;width:7px;height:7px;border-radius:50%;'
            f'background:{"#4caf50" if ok else "#df0024"};margin:0 2px;'
            f'box-shadow:0 0 4px {"#4caf50" if ok else "#df0024"};"></span>'
            for ok, _, _ in checks
        )

        new_ach     = self._check_achievements(key)
        reg_ach     = [(n, c, r) for n, c, r in new_ach if r != "Nivel"]
        levelup_ach = [(n, c, r) for n, c, r in new_ach if r == "Nivel"]

        _RC = {
            "Bronce": ("#cd7f32", "rgba(205,127,50,.12)", "🥉"),
            "Plata":  ("#d8d8e6", "rgba(216,216,230,.12)", "🥈"),
            "Oro":    ("#ffd700", "rgba(255,215,0,.10)",  "🥇"),
            "Récord": ("#0081C8", "rgba(0,129,200,.15)",  "🏆"),
        }
        ach_html = ""
        for ach_name, _, ach_rarity in reg_ach:
            bc, bg, ach_icon = _RC.get(ach_rarity, _RC["Bronce"])
            ach_html += (
                f'<div style="display:flex;align-items:center;gap:10px;margin-top:8px;'
                f'padding:10px 12px;background:{bg};border:1px solid {bc};border-radius:3px;">'
                f'<span style="font-size:18px;">{ach_icon}</span>'
                f'<div style="flex:1;">'
                f'<div style="margin-bottom:3px;">'
                f'<span style="background:{bc};color:#0a0e14;font-size:7px;font-weight:bold;'
                f'padding:1px 5px;border-radius:2px;font-family:\'Press Start 2P\',monospace;">'
                f'{ach_rarity.upper()}</span>'
                f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;'
                f'color:{bc};margin-left:6px;">LOGRO DESBLOQUEADO</span>'
                f'</div>'
                f'<div style="color:#f0ece0;font-size:12px;font-weight:bold;">{ach_name}</div>'
                f'</div></div>'
            )

        curr_icon  = getattr(self, '_curr_icon', '🏅')
        curr_title = getattr(self, '_curr_title', 'EJERCICIO').upper()
        _logo_sm   = self._logo_tag_sm

        _core_pct_bar = min(round(earned / _CORE_MAX * 100), 100)
        xp_bar_html = (
            f'<div style="display:flex;justify-content:space-between;margin-bottom:4px;">'
            f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;color:#555566;">'
            f'XP: {earned}/{_CORE_MAX}</span>'
            f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;'
            f'color:{_lv_color(lvl_num)};">{lvl_name}</span></div>'
            f'<div style="width:100%;height:10px;background:#12141f;border:1px solid #1a2233;'
            f'border-radius:2px;overflow:hidden;">'
            f'<div style="width:{_core_pct_bar}%;height:100%;background:{xp_grad};'
            f'border-radius:2px;transform-origin:left;'
            f'animation:pg-xpscale 1.1s cubic-bezier(.4,0,.2,1) forwards;'
            f'box-shadow:0 0 6px rgba(255,215,0,.25);"></div></div>'
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
                             'font-size:6px;color:#0081C8;letter-spacing:1px;opacity:.85;">'
                             '📊 Calificación actualizada en la base de datos</div>')

        card_html = f'''<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
  @keyframes pg-xpscale{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
</style>
<div style="background:#0a0e14;border:2px solid {border_color};border-radius:4px;max-width:840px;
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
      <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#df0024;
        background:rgba(223,0,36,.1);border:1px solid rgba(223,0,36,.4);
        padding:3px 8px;border-radius:2px;">MAX {max_pts} XP</div>
    </div>
  </div>
  <div style="padding:10px 14px 6px;">{rows_html}</div>
  <div style="background:#07090e;border-top:1px solid #161a26;padding:11px 14px;">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:9px;">
      <div style="display:flex;align-items:center;gap:8px;">
        <span style="font-size:16px;">{s_icon}</span>
        <span style="font-family:'Press Start 2P',monospace;font-size:8px;
          color:{s_color};">{s_text}</span>
        {combo_html}
      </div>
      <div style="display:flex;align-items:center;gap:4px;color:#555566;font-size:10px;">
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

    # ── Level-up banner (Olimpico style) ──────────────────────

    def _render_levelup(self, lvl_num, lvl_name):
        import random as _r
        _r.seed(lvl_num * 97 + 31)
        uid = f"lu{_r.randint(10000, 99999)}"

        _cfg = {
            2: dict(bg="linear-gradient(160deg,#0a0e14,#1a1000)",
                    c="#ff8c42", sc="#ffb066", rc="#ff8c42",
                    sub="ATLETA EN ENTRENAMIENTO — TU RITMO EMPIEZA A SUBIR", icon="🏃"),
            3: dict(bg="linear-gradient(160deg,#1a0f05,#2a1608)",
                    c="#cd7f32", sc="#e0a066", rc="#cd7f32",
                    sub="MEDALLA DE BRONCE — TU PRIMER PODIO", icon="🥉"),
            4: dict(bg="linear-gradient(160deg,#12141c,#1e2130)",
                    c="#d8d8e6", sc="#eeeef6", rc="#d8d8e6",
                    sub="MEDALLA DE PLATA — CASI EN LO MÁS ALTO", icon="🥈"),
            5: dict(bg="linear-gradient(160deg,#1a1400,#2a2200)",
                    c="#ffd700", sc="#ffe680", rc="#ffd700",
                    sub="MEDALLA DE ORO — LOS JUECES YA TE RECONOCEN", icon="🥇"),
            6: dict(bg="linear-gradient(160deg,#0a0e14,#12060a,#0a0e14)",
                    c="#ffd700", sc="#0081C8", rc="#df0024",
                    sub="RÉCORD OLÍMPICO — SALÓN DE LA FAMA DE LA SEMANA 2", icon="🏆"),
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
                          f'margin:-50px;border-radius:50%;border:2px solid #0081C8;opacity:0;'
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
    🔵 🟡 ⚫ 🟢 🔴</div>
  <div style="position:absolute;right:14px;top:50%;
    font-size:15px;letter-spacing:5px;
    animation:{uid}-rr .9s ease-out .6s both;pointer-events:none;z-index:7;">
    🔵 🟡 ⚫ 🟢 🔴</div>

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
      color:#555566;letter-spacing:2px;
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
                f'<div style="font-size:11px;color:#f0ece0;margin-bottom:3px;">{label}</div>'
                f'<div style="height:5px;background:#161a26;border-radius:2px;overflow:hidden;">'
                f'<div style="width:{bar_w * 100 // 60}%;height:100%;'
                f'background:{color};opacity:.85;border-radius:2px;"></div></div>'
                f'</div>'
                f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;'
                f'color:{color if ok else "#555566"};">{e}/{p}</span>'
                f'</div>'
            )
        pct_sec = round(total_e / total_p * 100) if total_p else 0
        display(HTML(
            f'<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">'
            f'<div style="background:#0a0e14;border:2px solid {color};border-radius:4px;'
            f'max-width:840px;margin:10px 0;padding:18px 20px;'
            f'box-shadow:0 0 20px {color}22,0 4px 16px rgba(0,0,0,.6);">'
            f'<div style="font-family:\'Press Start 2P\',monospace;font-size:9px;'
            f'color:{color};letter-spacing:2px;margin-bottom:16px;">🎖️ {title}</div>'
            f'{rows}'
            f'<div style="margin-top:14px;padding-top:10px;border-top:1px solid {color}30;'
            f'display:flex;justify-content:space-between;align-items:center;">'
            f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;color:#666677;">'
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
                "nombre":          self._nombre_real or "atleta",
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
                "score_breakdown": {k: {"e": e, "p": p}
                                    for k, (e, p) in self._scores.items()},
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
                    f'<div style="font-family:\'Press Start 2P\',monospace;font-size:8px;'
                    f'color:#4caf50;background:#020d02;border:1px solid #4caf50;'
                    f'border-radius:3px;padding:10px 16px;max-width:840px;margin-top:6px;">'
                    f'✅ SCORE ENVIADO — {self._nombre_real} · DNI {self._dni}'
                    f'<br><span style="color:#0081C8;font-size:7px;">'
                    f'📊 Calificación actualizada en la base de datos</span></div>'
                ))
        except Exception as _ex:
            if not silent:
                display(HTML(
                    f'<div style="font-family:\'Press Start 2P\',monospace;font-size:7px;'
                    f'color:#df0024;background:#1a0005;border:1px solid #df0024;'
                    f'border-radius:3px;padding:10px 16px;max-width:840px;margin-top:6px;">'
                    f'⚠️ Leaderboard no disponible: {_ex}</div>'
                ))

    # ═══════════════════════════════════════════════════════════
    # ANTES DE FILTRAR — Repaso
    # ═══════════════════════════════════════════════════════════

    def check_ex0(self):
        """Ex0 — Repite el patron: mean/median/std sobre Altura (10 pts)"""
        self._header("EJERCICIO 0 — Calentamiento 🏃", icon="🏅", pts=10)
        checks = []
        media  = _get("media_altura")
        mediana = _get("mediana_altura")
        desv    = _get("desviacion_altura")
        EXP_MEDIA, EXP_MEDIANA, EXP_DESV = 175.33896987366376, 175.0, 10.518462222679224

        for vname, val, exp, tol in [
            ("media_altura", media, EXP_MEDIA, 0.06),
            ("mediana_altura", mediana, EXP_MEDIANA, 0.06),
            ("desviacion_altura", desv, EXP_DESV, 0.06),
        ]:
            if val is None:
                checks.append((False, vname, "No definida"))
            elif not _is_number(val):
                checks.append((False, vname, f"Debe ser número, recibí {type(val).__name__}"))
            elif _approx(val, exp, tol=tol):
                checks.append((True, f"{vname} ≈ {exp:.1f}", "✓"))
            else:
                checks.append((False, vname, f"Debe ser ≈{exp:.1f}, obtuve {val}"))

        return self._award("ex0", checks, 10)

    # ═══════════════════════════════════════════════════════════
    # SECCIÓN C — Filtra el Ruido
    # ═══════════════════════════════════════════════════════════

    def check_ex1(self):
        """Ex1 — Filtro numerico: Edad > 25 (10 pts)"""
        self._header("EJERCICIO 1 — Carril de Edad 🏃‍♀️", icon="🏅", pts=10)
        checks = []
        df_m25  = _get("df_mayores25")
        media   = _get("media_c1")
        mediana = _get("mediana_c1")
        EXP_N = 110801
        EXP_MEDIA, EXP_MEDIANA = 31.004900677791717, 29.0

        if df_m25 is None:
            checks.append((False, "df_mayores25", "No definida — usa df_atletas[df_atletas['Edad'] > 25]"))
        elif not _is_dataframe(df_m25):
            checks.append((False, "df_mayores25", f"Debe ser un DataFrame filtrado, recibí {type(df_m25).__name__}"))
        elif len(df_m25) == EXP_N:
            checks.append((True, f"len(df_mayores25) == {EXP_N}", "✓"))
        else:
            checks.append((False, "df_mayores25", f"Debe tener {EXP_N} filas, tiene {len(df_m25)}. ¿Usaste '>' con Edad?"))

        for vname, val, exp, tol in [("media_c1", media, EXP_MEDIA, 0.06), ("mediana_c1", mediana, EXP_MEDIANA, 0.06)]:
            if val is None:
                checks.append((False, vname, "No definida"))
            elif not _is_number(val):
                checks.append((False, vname, f"Debe ser número, recibí {type(val).__name__}"))
            elif _approx(val, exp, tol=tol):
                checks.append((True, f"{vname} ≈ {exp:.1f}", "✓"))
            else:
                checks.append((False, vname, f"Debe ser ≈{exp:.1f}, obtuve {val}"))

        return self._award("ex1", checks, 10)

    def check_ex2(self):
        """Ex2 — Filtro categorico: Deporte == 'Natacion' (10 pts)"""
        self._header("EJERCICIO 2 — Carril de Natación 🏊", icon="🏅", pts=10)
        checks = []
        df_nat = _get("df_natacion")
        edad_p = _get("edad_promedio_natacion")
        peso_p = _get("peso_promedio_natacion")
        EXP_N = 23195
        EXP_EDAD, EXP_PESO = 20.566803405231354, 70.58849181025313

        if df_nat is None:
            checks.append((False, "df_natacion", "No definida — usa df_atletas[df_atletas['Deporte'] == 'Natacion']"))
        elif not _is_dataframe(df_nat):
            checks.append((False, "df_natacion", f"Debe ser un DataFrame filtrado, recibí {type(df_nat).__name__}"))
        elif len(df_nat) == EXP_N:
            checks.append((True, f"len(df_natacion) == {EXP_N}", "✓"))
        else:
            checks.append((False, "df_natacion", f"Debe tener {EXP_N} filas, tiene {len(df_nat)}. Revisa el nombre exacto: 'Natacion'"))

        for vname, val, exp, tol in [("edad_promedio_natacion", edad_p, EXP_EDAD, 0.06),
                                      ("peso_promedio_natacion", peso_p, EXP_PESO, 0.06)]:
            if val is None:
                checks.append((False, vname, "No definida"))
            elif not _is_number(val):
                checks.append((False, vname, f"Debe ser número, recibí {type(val).__name__}"))
            elif _approx(val, exp, tol=tol):
                checks.append((True, f"{vname} ≈ {exp:.1f}", "✓"))
            else:
                checks.append((False, vname, f"Debe ser ≈{exp:.1f}, obtuve {val}"))

        return self._award("ex2", checks, 10)

    def check_debug0(self):
        """Debug0 — '=' en vez de '==' dentro del filtro (SyntaxError) (10 pts)"""
        self._header("🔧 DEBUG 0 — Falso Arranque", icon="🔧", pts=10)
        checks = []
        df_muj = _get("df_mujeres")
        EXP_N = 74522

        if df_muj is None:
            checks.append((False, "df_mujeres", "No definida — dentro de un filtro se compara con '==', no se asigna con '='"))
        elif not _is_dataframe(df_muj):
            checks.append((False, "df_mujeres", f"Debe ser un DataFrame filtrado, recibí {type(df_muj).__name__}"))
        elif len(df_muj) == EXP_N:
            checks.append((True, f"len(df_mujeres) == {EXP_N}", "✓  SyntaxError corregido — '==' compara, '=' asigna"))
        else:
            checks.append((False, "df_mujeres", f"Debe tener {EXP_N} filas, tiene {len(df_muj)}"))

        return self._award("debug0", checks, 10)

    def check_t0(self): return self._ask_teoria(0)
    def check_t1(self): return self._ask_teoria(1)
    def check_t2(self): return self._ask_teoria(2)

    def check_ex3(self):
        """Ex3 — Filtro combinado: Edad > 25 & Deporte == 'Baloncesto' (12 pts)"""
        self._header("EJERCICIO 3 — Doble Carril: Edad + Baloncesto 🏀", icon="🏅", pts=12)
        checks = []
        df_bb   = _get("df_basket_mayores25")
        cant    = _get("cantidad_c3")
        altura  = _get("altura_promedio_c3")
        EXP_N = 1938
        EXP_ALTURA = 190.97715591090804

        if df_bb is None:
            checks.append((False, "df_basket_mayores25",
                           "No definida — combina (Edad > 25) & (Deporte == 'Baloncesto')"))
        elif not _is_dataframe(df_bb):
            checks.append((False, "df_basket_mayores25", f"Debe ser un DataFrame filtrado, recibí {type(df_bb).__name__}"))
        elif len(df_bb) == EXP_N:
            checks.append((True, f"len(df_basket_mayores25) == {EXP_N}", "✓"))
        else:
            checks.append((False, "df_basket_mayores25",
                           f"Debe tener {EXP_N} filas, tiene {len(df_bb)}. ¿Pusiste cada condición entre paréntesis y usaste '&'?"))

        if cant is None:
            checks.append((False, "cantidad_c3", "No definida — usa len(df_basket_mayores25)"))
        elif not _is_int_like(cant):
            checks.append((False, "cantidad_c3", f"Debe ser un entero, recibí {type(cant).__name__}"))
        elif int(cant) == EXP_N:
            checks.append((True, f"cantidad_c3 == {EXP_N}", "✓"))
        else:
            checks.append((False, "cantidad_c3", f"Debe ser {EXP_N}, obtuve {cant}"))

        if altura is None:
            checks.append((False, "altura_promedio_c3", "No definida"))
        elif not _is_number(altura):
            checks.append((False, "altura_promedio_c3", f"Debe ser número, recibí {type(altura).__name__}"))
        elif _approx(altura, EXP_ALTURA, tol=0.06):
            checks.append((True, f"altura_promedio_c3 ≈ {EXP_ALTURA:.1f}", "✓"))
        else:
            checks.append((False, "altura_promedio_c3", f"Debe ser ≈{EXP_ALTURA:.1f}, obtuve {altura}"))

        return self._award("ex3", checks, 12)

    def check_debug1(self):
        """Debug1 — 'and' de Python en vez de '&' de pandas (ValueError) (10 pts)"""
        self._header("🔧 DEBUG 1 — Choque en la Pista", icon="🔧", pts=10)
        checks = []
        df_res = _get("df_resultado")
        EXP_N = 3015

        if df_res is None:
            checks.append((False, "df_resultado",
                           "No definida — usa '&' con cada condición entre paréntesis, no 'and'"))
        elif not _is_dataframe(df_res):
            checks.append((False, "df_resultado", f"Debe ser un DataFrame filtrado, recibí {type(df_res).__name__}"))
        elif len(df_res) == EXP_N:
            checks.append((True, f"len(df_resultado) == {EXP_N}", "✓  ValueError corregido — 'and' no funciona sobre Series de pandas"))
        else:
            checks.append((False, "df_resultado", f"Debe tener {EXP_N} filas, tiene {len(df_res)}"))

        return self._award("debug1", checks, 10)

    def check_mini_c(self):
        """Checkpoint — Sección C (Filtra el Ruido)"""
        self._checkpoints.add("mini_c")
        seccion = {
            "ex0": ("Ejercicio 0 – Calentamiento (mean/median/std)", 10),
            "ex1": ("Ejercicio 1 – Carril de Edad", 10),
            "ex2": ("Ejercicio 2 – Carril de Natación", 10),
            "t0": ("T0 — Valores atípicos", 5),
            "t1": ("T1 — Qué hace un filtro", 5),
            "debug0": ("Debug 0 – Falso Arranque", 10),
            "t2": ("T2 — Equivalencia de filtro combinado", 5),
            "ex3": ("Ejercicio 3 – Doble Carril", 12),
            "debug1": ("Debug 1 – Choque en la Pista", 10),
        }
        self._render_checkpoint("CHECKPOINT — PODIO SECCIÓN C", seccion, "#0081C8")

    # ═══════════════════════════════════════════════════════════
    # SECCIÓN D — Compara Grupos
    # ═══════════════════════════════════════════════════════════

    def check_t3(self): return self._ask_teoria(3)

    def check_ex4(self):
        """Ex4 — groupby: peso promedio por deporte (top5) (12 pts)"""
        self._header("EJERCICIO 4 — Ranking de Peso por Disciplina 🏋️", icon="🏅", pts=12)
        checks = []
        val = _get("peso_por_deporte")
        EXPECTED = {
            "Atletismo": 69.2492868317, "Ciclismo": 70.0679438059,
            "Gimnasia": 56.9165530406, "Natacion": 70.5884918103, "Tiro": 74.0278767123,
        }
        ok, msg = _series_check(val, EXPECTED, tol=0.06)
        checks.append((ok, "peso_por_deporte", msg if ok else msg + " — usa .groupby('Deporte')['Peso'].mean() sobre deportes_top"))
        return self._award("ex4", checks, 12)

    def check_debug2(self):
        """Debug2 — 'Edd' en vez de 'Edad' (KeyError) (10 pts)"""
        self._header("🔧 DEBUG 2 — Nombre Mal Escrito", icon="🔧", pts=10)
        checks = []
        val = _get("edad_por_deporte")
        EXP_N = 66

        if val is None:
            checks.append((False, "edad_por_deporte", "No definida — corrige el nombre de columna a 'Edad'"))
        elif not _is_series(val):
            checks.append((False, "edad_por_deporte", f"Debe ser una Series (resultado de groupby), recibí {type(val).__name__}"))
        else:
            data = val.to_dict()
            n_ok = len(data) == EXP_N
            bb_ok = "Baloncesto" in data and _approx(data["Baloncesto"], 25.324597701149425, tol=0.06)
            at_ok = "Atletismo" in data and _approx(data["Atletismo"], 25.161223238328844, tol=0.06)
            if n_ok and bb_ok and at_ok:
                checks.append((True, "edad_por_deporte", "✓  KeyError corregido — 'Edad' es el nombre real de la columna"))
            else:
                checks.append((False, "edad_por_deporte",
                               f"Se esperaban {EXP_N} deportes con Baloncesto≈25.3 y Atletismo≈25.2, obtuve {len(data)} categorías"))

        return self._award("debug2", checks, 10)

    def check_ex5(self):
        """Ex5 — groupby: edad promedio por Temporada (11 pts)"""
        self._header("EJERCICIO 5 — Verano vs. Invierno ❄️☀️", icon="🏅", pts=11)
        checks = []
        val = _get("edad_por_temporada")
        EXPECTED = {"Invierno": 25.0391474554, "Verano": 25.6740531395}
        ok, msg = _series_check(val, EXPECTED, tol=0.06)
        checks.append((ok, "edad_por_temporada", msg if ok else msg + " — usa .groupby('Temporada')['Edad'].mean()"))
        return self._award("ex5", checks, 11)

    def check_t4(self): return self._ask_teoria(4)

    def check_ex6(self):
        """Ex6 — filtrar + groupby: mujeres, altura por deporte (top5) (12 pts)"""
        self._header("EJERCICIO 6 — Altura Femenina por Disciplina 🤸‍♀️", icon="🏅", pts=12)
        checks = []
        df_muj = _get("df_mujeres")
        val    = _get("altura_por_deporte_mujeres")
        EXP_N = 74522
        EXPECTED = {
            "Atletismo": 169.2857142857, "Ciclismo": 168.0186289121,
            "Gimnasia": 156.1433246073, "Natacion": 171.4687354176, "Tiro": 164.9329341317,
        }

        if df_muj is None:
            checks.append((False, "df_mujeres", "No definida — usa df_atletas[df_atletas['Sexo'] == 'F']"))
        elif not _is_dataframe(df_muj):
            checks.append((False, "df_mujeres", f"Debe ser un DataFrame filtrado, recibí {type(df_muj).__name__}"))
        elif len(df_muj) == EXP_N:
            checks.append((True, f"len(df_mujeres) == {EXP_N}", "✓"))
        else:
            checks.append((False, "df_mujeres", f"Debe tener {EXP_N} filas, tiene {len(df_muj)}"))

        ok, msg = _series_check(val, EXPECTED, tol=0.06)
        checks.append((ok, "altura_por_deporte_mujeres",
                        msg if ok else msg + " — filtra a mujeres primero, luego agrupa por Deporte sobre deportes_top"))

        return self._award("ex6", checks, 12)

    def check_debug3(self):
        """Debug3 — '.means()' en vez de '.mean()' (AttributeError) (10 pts)"""
        self._header("🔧 DEBUG 3 — Método que no Existe", icon="🔧", pts=10)
        checks = []
        val = _get("edad_por_pais")
        EXP_N = 230

        if val is None:
            checks.append((False, "edad_por_pais", "No definida — el método correcto es '.mean()', no '.means()'"))
        elif not _is_series(val):
            checks.append((False, "edad_por_pais", f"Debe ser una Series (resultado de groupby), recibí {type(val).__name__}"))
        else:
            data = val.to_dict()
            n_ok = len(data) == EXP_N
            afg_ok = "AFG" in data and _approx(data["AFG"], 23.53846153846154, tol=0.06)
            if n_ok and afg_ok:
                checks.append((True, "edad_por_pais", "✓  AttributeError corregido — 'SeriesGroupBy' no tiene '.means()', el método es '.mean()'"))
            else:
                checks.append((False, "edad_por_pais",
                               f"Se esperaban {EXP_N} países con AFG≈23.5, obtuve {len(data)} categorías"))

        return self._award("debug3", checks, 10)

    def check_mini_d(self):
        """Checkpoint — Sección D (Compara Grupos, fin de la Semana 2 en clase)"""
        self._checkpoints.add("mini_d")
        if len(self._checkpoints) >= 2 and self._unlock("doble_podio"):
            display(HTML(
                '<div style="font-family:\'Press Start 2P\',monospace;font-size:8px;'
                'color:#ffd700;background:#1a1400;border:1px solid #ffd700;'
                'border-radius:3px;padding:12px 16px;max-width:840px;margin:6px 0;">'
                '🎖️ LOGRO: Doble Podio — Ambos checkpoints superados</div>'
            ))
        seccion = {
            "t3": ("T3 — Qué devuelve groupby() antes de agregar", 5),
            "ex4": ("Ejercicio 4 – Ranking de Peso por Disciplina", 12),
            "debug2": ("Debug 2 – Nombre Mal Escrito", 10),
            "ex5": ("Ejercicio 5 – Verano vs. Invierno", 11),
            "t4": ("T4 — Límite de comparar grupos", 5),
            "ex6": ("Ejercicio 6 – Altura Femenina por Disciplina", 12),
            "debug3": ("Debug 3 – Método que no Existe", 10),
        }
        self._render_checkpoint("CHECKPOINT — PODIO SECCIÓN D", seccion, "#df0024")

    # ═══════════════════════════════════════════════════════════
    # TEORÍA — check_t0 .. check_t4 (formulario interactivo HTML)
    # ═══════════════════════════════════════════════════════════

    _TEORIA = {
        0: dict(
            title="T0 — Qué es (y qué no es) un valor atípico",
            q=('En el dataset olímpico aparece un atleta con una altura muy por encima del resto. '
               '¿Qué es lo correcto de asumir sobre ese dato antes de investigarlo?'),
            opts={"a": "Es un error de registro y debe eliminarse de inmediato",
                  "b": "Es un valor atípico — una observación inusual que puede ser real y válida",
                  "c": "Significa que todo el dataset no es confiable",
                  "d": "Hay que reemplazarlo automáticamente por la media"},
            correct="b",
            why=("Es el malentendido más común en estudiantes nuevos a estadística — un atípico es "
                 "\"inusual,\" no automáticamente \"erróneo.\" Puede ser un caso real (ej. un atleta "
                 "de básquet excepcionalmente alto, como Yao Ming en este mismo dataset)."),
            pts=5,
        ),
        1: dict(
            title="T1 — Qué hace un filtro",
            q=("Cuando se escribe <code>df[df['edad'] > 30]</code>, ¿qué se está haciendo conceptualmente?"),
            opts={"a": "Borrando permanentemente a los atletas menores de 30 del archivo original",
                  "b": "Haciéndole una pregunta específica a los datos: \"muéstrame solo los casos que cumplen esta condición\"",
                  "c": "Calculando el promedio de edad",
                  "d": "Ordenando el dataset de mayor a menor"},
            correct="b",
            why="El filtrado crea una vista/subconjunto para responder una pregunta puntual; no modifica el dataset original.",
            pts=5,
        ),
        2: dict(
            title="T2 — Equivalencia de un filtro combinado",
            q=("Quieres los atletas mayores de 20 años que juegan Vóleibol. ¿Cuál de estas opciones te da "
               "EXACTAMENTE el mismo resultado que "
               "<code>df_atletas[(df_atletas['Edad'] &gt; 20) &amp; (df_atletas['Deporte'] == 'Voleibol')]</code>?"),
            opts={"a": "df_atletas[df_atletas['Edad'] > 20 and df_atletas['Deporte'] == 'Voleibol']",
                  "b": "df_atletas[df_atletas['Edad'] > 20][df_atletas['Deporte'] == 'Voleibol']  (filtrar dos veces seguidas)",
                  "c": "df_atletas[df_atletas['Edad'] > 20 | df_atletas['Deporte'] == 'Voleibol']",
                  "d": "df_atletas['Edad'] > 20 & df_atletas['Deporte'] == 'Voleibol']  (sin el corchete externo)"},
            correct="b",
            why=("Filtrar dos veces seguidas (primero por Edad, después por Deporte sobre lo que quedó) equivale "
                 "exactamente a combinar ambas condiciones con '&', porque en los dos casos una fila sobrevive "
                 "solo si cumple las dos condiciones a la vez. a) usa 'and' de Python, que falla sobre columnas "
                 "de pandas (el mismo error de Debug 1). c) usa '|' (O) en vez de '&' (Y), lo que cambia el "
                 "significado por completo. d) tiene un error de sintaxis."),
            pts=5,
        ),
        3: dict(
            title="T3 — Qué devuelve groupby() antes de agregar",
            q=("Después de escribir <code>grupos = df_atletas.groupby('Deporte')['Altura']</code> "
               "(sin agregar <code>.mean()</code> ni ningún otro método todavía), ¿qué tiene guardado la "
               "variable <code>grupos</code>?"),
            opts={"a": "Un DataFrame con la altura promedio de cada deporte, ya calculada",
                  "b": "Un solo número: la altura promedio de todos los deportes juntos",
                  "c": "Los datos ya separados por deporte, pero SIN ningún resumen calculado todavía — falta aplicar .mean(), .median(), .std(), etc.",
                  "d": "Una lista con los nombres de los deportes, sin ningún dato numérico"},
            correct="c",
            why=("'.groupby()' por sí solo únicamente organiza las filas en grupos — es el paso de 'agrupar'. "
                 "El resumen (media, mediana, conteo...) es un paso aparte que se aplica después, sobre cada grupo."),
            pts=5,
        ),
        4: dict(
            title="T4 — El límite de comparar grupos",
            q=("Al comparar con .groupby() el promedio de medallas entre dos países, se encuentra que el "
               "País A tiene un promedio más alto que el País B. ¿Qué se puede concluir correctamente?"),
            opts={"a": "El País A es \"mejor\" en todo, y esa es la causa de la diferencia",
                  "b": "Existe una diferencia entre los grupos en este dataset — pero esto no explica por qué existe esa diferencia",
                  "c": "No se puede concluir nada de una comparación de grupos",
                  "d": "El País B debería copiar exactamente lo que hace el País A"},
            correct="b",
            why=("Comparar grupos muestra qué es diferente, no por qué — la explicación causal es tema "
                 "protegido de la Semana 5; esta pregunta siembra la barrera sin adelantar esa clase."),
            pts=5,
        ),
    }

    def _show_teoria_locked(self, n):
        """Pregunta ya respondida -- no se permite una segunda respuesta."""
        spec = self._TEORIA[int(n)]
        pts, max_pts = self._scores[f"t{int(n)}"]
        ok = pts == max_pts
        color = "#4caf50" if ok else "#df0024"
        estado = (f"✅ Ya respondiste correctamente ({pts}/{max_pts} pts)" if ok
                  else f"❌ Ya respondiste esta pregunta ({pts}/{max_pts} pts)")
        display(HTML(
            f'<div style="max-width:840px;margin:10px 0;background:#0a0e14;'
            f'border:2px solid {color};border-radius:4px;padding:14px 18px;'
            f'font-family:\'Segoe UI\',Roboto,sans-serif;">'
            f'<div style="font-family:\'Press Start 2P\',monospace;font-size:9px;'
            f'color:#8899bb;letter-spacing:1px;margin-bottom:8px;">'
            f'🔒 {spec["title"]} — YA RESPONDIDA</div>'
            f'<div style="color:{color};font-size:13px;">{estado}</div>'
            f'<div style="color:#8899bb;font-size:12px;margin-top:6px;">'
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
                    f'margin-bottom:8px;background:#0e1119;border:2px solid #0081C8;'
                    f'border-radius:4px;color:#f0ece0;font-family:\'Segoe UI\',Roboto,sans-serif;'
                    f'font-size:13px;cursor:pointer;transition:all .15s;">'
                    f'<span style="font-family:\'Press Start 2P\',monospace;font-size:9px;'
                    f'color:#ffd700;margin-right:10px;">{L.upper()}</span>{spec["opts"][L]}</button>'
                )

            display(HTML(f'''
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
  .{uid}-opt:hover {{ border-color:#ffd700 !important; background:#161a26 !important; }}
</style>
<div id="{uid}-wrap" style="background:#0a0e14;border:2px solid #0081C8;border-radius:4px;
  max-width:840px;margin:10px 0;overflow:hidden;box-shadow:0 6px 24px rgba(0,0,0,.7);">
  <div style="background:#0081C818;border-bottom:1px solid #0081C840;padding:10px 16px;">
    <span style="font-family:'Press Start 2P',monospace;font-size:9px;color:#0081C8;
      letter-spacing:1px;">❓ {spec['title']}</span>
  </div>
  <div style="padding:16px 18px;">
    <div style="color:#f0ece0;font-size:13px;line-height:1.6;margin-bottom:16px;">{spec['q']}</div>
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
    chosen.style.borderColor = '#ffd700';
    chosen.style.background = '#161a26';
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

    # ═══════════════════════════════════════════════════════════
    # INTEGRACIÓN — check_intex0 .. check_intex4 (Tarea)
    # ═══════════════════════════════════════════════════════════

    def check_intex0(self):
        """Integracion 0 — Altura promedio y dispersion en Baloncesto (8 pts)"""
        self._header("INTEGRACIÓN 0 — Gigantes de la Cancha 🏀", icon="🧬", pts=8)
        checks = []
        df_bb  = _get("df_basket")
        altura = _get("altura_promedio_basket")
        desv   = _get("desviacion_altura_basket")
        interp = _get("interpretacion_intex0")
        EXP_N = 4536
        EXP_ALTURA, EXP_DESV = 190.86987889719146, 11.459242981184454

        if df_bb is None:
            checks.append((False, "df_basket", "No definida — filtra Deporte == 'Baloncesto'"))
        elif not _is_dataframe(df_bb):
            checks.append((False, "df_basket", f"Debe ser un DataFrame filtrado, recibí {type(df_bb).__name__}"))
        elif len(df_bb) == EXP_N:
            checks.append((True, f"len(df_basket) == {EXP_N}", "✓"))
        else:
            checks.append((False, "df_basket", f"Debe tener {EXP_N} filas, tiene {len(df_bb)}"))

        for vname, val, exp in [("altura_promedio_basket", altura, EXP_ALTURA),
                                 ("desviacion_altura_basket", desv, EXP_DESV)]:
            if val is None:
                checks.append((False, vname, "No definida"))
            elif not _is_number(val):
                checks.append((False, vname, f"Debe ser número, recibí {type(val).__name__}"))
            elif _approx(val, exp, tol=0.06):
                checks.append((True, f"{vname} ≈ {exp:.1f}", "✓"))
            else:
                checks.append((False, vname, f"Debe ser ≈{exp:.1f}, obtuve {val}"))

        if _is_nontrivial_text(interp):
            checks.append((True, "interpretacion_intex0", "✓  Escribiste una frase con tu hallazgo"))
        else:
            checks.append((False, "interpretacion_intex0", "Falta una frase real con tu hallazgo (mínimo ~15 caracteres, no el placeholder)"))

        return self._award("intex0", checks, 8)

    def check_intex1(self):
        """Integracion 1 — Diferencia de edad Baloncesto vs Gimnasia (8 pts)"""
        self._header("INTEGRACIÓN 1 — ¿Quiénes son más jóvenes? 🤸", icon="🧬", pts=8)
        checks = []
        eb = _get("edad_promedio_basket")
        eg = _get("edad_promedio_gimnasia")
        dif = _get("diferencia_edad_basket_gimnasia")
        interp = _get("interpretacion_intex1")
        EXP_BB, EXP_GYM = 25.324597701149425, 22.733038232528987
        EXP_DIF = EXP_BB - EXP_GYM  # ≈ 2.5916

        for vname, val, exp in [("edad_promedio_basket", eb, EXP_BB), ("edad_promedio_gimnasia", eg, EXP_GYM)]:
            if val is None:
                checks.append((False, vname, "No definida"))
            elif not _is_number(val):
                checks.append((False, vname, f"Debe ser número, recibí {type(val).__name__}"))
            elif _approx(val, exp, tol=0.06):
                checks.append((True, f"{vname} ≈ {exp:.1f}", "✓"))
            else:
                checks.append((False, vname, f"Debe ser ≈{exp:.1f}, obtuve {val}"))

        # El enunciado no fija el orden de la resta -- se acepta cualquiera de los
        # dos signos (basket-gimnasia o gimnasia-basket) para no rechazar una
        # resta aritmeticamente correcta solo por el orden elegido.
        if dif is None:
            checks.append((False, "diferencia_edad_basket_gimnasia", "No definida"))
        elif not _is_number(dif):
            checks.append((False, "diferencia_edad_basket_gimnasia", f"Debe ser número, recibí {type(dif).__name__}"))
        elif _approx(abs(dif), EXP_DIF, tol=0.06):
            checks.append((True, f"|diferencia_edad_basket_gimnasia| ≈ {EXP_DIF:.2f}", "✓"))
        else:
            checks.append((False, "diferencia_edad_basket_gimnasia", f"Debe ser ≈±{EXP_DIF:.2f}, obtuve {dif}"))

        if _is_nontrivial_text(interp):
            checks.append((True, "interpretacion_intex1", "✓  Escribiste una frase con tu hallazgo"))
        else:
            checks.append((False, "interpretacion_intex1", "Falta una frase real con tu hallazgo (mínimo ~15 caracteres, no el placeholder)"))

        return self._award("intex1", checks, 8)

    def check_intex2(self):
        """Integracion 2 — Peru en los Juegos Olimpicos (7 pts)"""
        self._header("INTEGRACIÓN 2 — 🇵🇪 Perú en los Juegos", icon="🧬", pts=7)
        checks = []
        df_peru = _get("df_peru")
        deportes = _get("deportes_peru")
        interp = _get("interpretacion_intex2")
        EXP_N = 532
        EXP_N_DEPORTES = 26

        if df_peru is None:
            checks.append((False, "df_peru", "No definida — filtra CON == 'PER'"))
        elif not _is_dataframe(df_peru):
            checks.append((False, "df_peru", f"Debe ser un DataFrame filtrado, recibí {type(df_peru).__name__}"))
        elif len(df_peru) == EXP_N:
            checks.append((True, f"len(df_peru) == {EXP_N}", "✓"))
        else:
            checks.append((False, "df_peru", f"Debe tener {EXP_N} filas, tiene {len(df_peru)}"))

        if deportes is None:
            checks.append((False, "deportes_peru", "No definida — usa df_peru['Deporte'].value_counts()"))
        elif not (_is_series(deportes) or isinstance(deportes, dict)):
            checks.append((False, "deportes_peru", f"Debe ser una Series (value_counts), recibí {type(deportes).__name__}"))
        else:
            data = deportes.to_dict() if _is_series(deportes) else deportes
            if len(data) == EXP_N_DEPORTES and data.get("Tiro") == 88:
                checks.append((True, "deportes_peru", "✓  26 deportes registrados, Tiro es el más frecuente (88)"))
            else:
                checks.append((False, "deportes_peru",
                               f"Se esperaban {EXP_N_DEPORTES} deportes con Tiro=88, obtuve {len(data)} categorías"))

        if _is_nontrivial_text(interp):
            checks.append((True, "interpretacion_intex2", "✓  Escribiste una frase con tu hallazgo"))
        else:
            checks.append((False, "interpretacion_intex2", "Falta una frase real con tu hallazgo (mínimo ~15 caracteres, no el placeholder)"))

        return self._award("intex2", checks, 7)

    # ── Integracion 3 — pregunta de opcion multiple sobre el propio hallazgo ──

    _INTEX3 = dict(
        title="Integración 3 — Interpreta tu propio hallazgo",
        q=("En Integración 1 calculaste que la edad promedio en Baloncesto y en Gimnasia es "
           "diferente. ¿Qué se puede concluir correctamente de ese resultado?"),
        opts={"a": "Que jugar Baloncesto hace que un atleta envejezca más rápido que la Gimnasia",
              "b": "Que existe una diferencia observada entre los dos grupos en este dataset — pero el dataset por sí solo no explica POR QUÉ existe esa diferencia",
              "c": "Que el cálculo debe estar mal, porque todos los deportes deberían tener la misma edad promedio",
              "d": "Que hay que eliminar uno de los dos deportes del dataset porque no son comparables"},
        correct="b",
        why=("Mismo principio que T4 (límite de comparar grupos), aplicado ahora a tu propio hallazgo: "
             "comparar grupos muestra qué es diferente, no por qué."),
        pts=5,
    )

    def _show_intex3_locked(self):
        pts, max_pts = self._scores["intex3"]
        ok = pts == max_pts
        color = "#4caf50" if ok else "#df0024"
        estado = (f"✅ Ya respondiste correctamente ({pts}/{max_pts} pts)" if ok
                  else f"❌ Ya respondiste esta pregunta ({pts}/{max_pts} pts)")
        display(HTML(
            f'<div style="max-width:840px;margin:10px 0;background:#0a0e14;'
            f'border:2px solid {color};border-radius:4px;padding:14px 18px;'
            f'font-family:\'Segoe UI\',Roboto,sans-serif;">'
            f'<div style="font-family:\'Press Start 2P\',monospace;font-size:9px;'
            f'color:#8899bb;letter-spacing:1px;margin-bottom:8px;">'
            f'🔒 {self._INTEX3["title"]} — YA RESPONDIDA</div>'
            f'<div style="color:{color};font-size:13px;">{estado}</div></div>'
        ))

    def _grade_intex3(self, letter):
        spec = self._INTEX3
        if "intex3" in self._scores:
            self._show_intex3_locked()
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
        return self._award("intex3", checks, spec["pts"])

    def check_intex3(self):
        spec = self._INTEX3
        if "intex3" in self._scores:
            self._show_intex3_locked()
            return
        try:
            from google.colab import output as _out  # noqa: F401
            import random as _r
            uid = f"ix3_{_r.randint(10000, 99999)}"

            opts_html = ""
            for L in ("a", "b", "c", "d"):
                opts_html += (
                    f'<button id="{uid}-{L}" class="{uid}-opt" onclick="{uid}_pick(\'{L}\')" '
                    f'style="display:block;width:100%;text-align:left;padding:12px 16px;'
                    f'margin-bottom:8px;background:#0e1119;border:2px solid #0081C8;'
                    f'border-radius:4px;color:#f0ece0;font-family:\'Segoe UI\',Roboto,sans-serif;'
                    f'font-size:13px;cursor:pointer;transition:all .15s;">'
                    f'<span style="font-family:\'Press Start 2P\',monospace;font-size:9px;'
                    f'color:#ffd700;margin-right:10px;">{L.upper()}</span>{spec["opts"][L]}</button>'
                )

            display(HTML(f'''
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
  .{uid}-opt:hover {{ border-color:#ffd700 !important; background:#161a26 !important; }}
</style>
<div id="{uid}-wrap" style="background:#0a0e14;border:2px solid #0081C8;border-radius:4px;
  max-width:840px;margin:10px 0;overflow:hidden;box-shadow:0 6px 24px rgba(0,0,0,.7);">
  <div style="background:#0081C818;border-bottom:1px solid #0081C840;padding:10px 16px;">
    <span style="font-family:'Press Start 2P',monospace;font-size:9px;color:#0081C8;
      letter-spacing:1px;">❓ {spec['title']}</span>
  </div>
  <div style="padding:16px 18px;">
    <div style="color:#f0ece0;font-size:13px;line-height:1.6;margin-bottom:16px;">{spec['q']}</div>
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
    chosen.style.borderColor = '#ffd700';
    chosen.style.background = '#161a26';
  }}
  await google.colab.kernel.invokeFunction('_ag_intex3_answer', [letter], {{}});
}}
</script>
'''))
        except ImportError:
            print(f"❓ {spec['title']}\n{spec['q']}\n")
            for L in ("a", "b", "c", "d"):
                print(f"  {L}) {spec['opts'][L]}")
            ans = input("Tu respuesta (a/b/c/d): ").strip().lower()
            self._grade_intex3(ans)

    def check_intex4(self):
        """Integracion 4 — Deporte con la altura mas variable (7 pts)"""
        self._header("INTEGRACIÓN 4 — El Deporte Más Impredecible 📏", icon="🧬", pts=7)
        checks = []
        val = _get("desviacion_altura_por_deporte")
        interp = _get("interpretacion_intex4")
        EXPECTED = {
            "Atletismo": 9.3144874195, "Ciclismo": 7.7200998793,
            "Gimnasia": 8.2897258432, "Natacion": 9.8966638591, "Tiro": 8.1671640954,
        }
        ok, msg = _series_check(val, EXPECTED, tol=0.06)
        checks.append((ok, "desviacion_altura_por_deporte",
                        msg if ok else msg + " — usa .groupby('Deporte')['Altura'].std() sobre deportes_top"))

        if _is_nontrivial_text(interp):
            checks.append((True, "interpretacion_intex4", "✓  Escribiste una frase con tu hallazgo"))
        else:
            checks.append((False, "interpretacion_intex4", "Falta una frase real con tu hallazgo (mínimo ~15 caracteres, no el placeholder)"))

        return self._award("intex4", checks, 7)

    # ═══════════════════════════════════════════════════════════
    # RETO BONUS — hallazgo abierto (fuera de _CORE_MAX)
    # ═══════════════════════════════════════════════════════════

    def check_reto1(self):
        """Reto Bonus — filtro + groupby libres sobre df_atletas (10 pts, bonus)"""
        self._header("🏆 RETO BONUS — Tu Propio Hallazgo", icon="🏆", pts=_BONUS_MAX)
        checks = []
        hallazgo = _get("hallazgo_reto1")

        if _is_nontrivial_text(hallazgo, min_len=20):
            checks.append((True, "hallazgo_reto1", "✓  Encontraste y describiste algo propio en los datos"))
        else:
            checks.append((False, "hallazgo_reto1",
                           "Falta una frase real (mínimo ~20 caracteres) describiendo tu propio hallazgo — no el placeholder \"___\""))

        passed = sum(1 for ok, _, _ in checks if ok)
        pts = round(_BONUS_MAX * passed / len(checks)) if checks else 0
        self._scores["reto1"] = (pts, _BONUS_MAX)
        # El bonus no cuenta para el streak del core, pero sí se muestra con la
        # misma tarjeta/engine que el resto de ejercicios para mantener el look
        # consistente -- se re-usa _award() y luego se corrige el streak si hace
        # falta (reto1 es opcional, no debe romper una racha del core).
        prev_streak = self._streak
        result = self._award("reto1", checks, _BONUS_MAX)
        if pts == _BONUS_MAX:
            self._streak = max(self._streak, prev_streak)
        else:
            self._streak = prev_streak
        return result

    # ═══════════════════════════════════════════════════════════
    # RESUMEN FINAL
    # ═══════════════════════════════════════════════════════════

    def resumen(self):
        _, _, pct         = self._totals()
        n                 = self._nombre()
        lvl_num, lvl_name = _level_info(pct)
        core_earned       = sum(e for k, (e, _) in self._scores.items() if k != "reto1")
        bonus_earned      = self._scores.get("reto1", (0, _BONUS_MAX))[0]

        if pct >= 96:
            final_msg = f"🏆 RÉCORD OLÍMPICO. {n.upper()}, tu nombre entra al Salón de la Fama de la Semana 2."
        elif pct >= 81:
            final_msg = f"🥇 MEDALLA DE ORO. {n}, subiste al podio más alto. La Semana 3 te espera."
        elif pct >= 61:
            final_msg = f"🥈 MEDALLA DE PLATA. {n}, tu segunda semana de datos ya tiene podio. ¡Sigue así!"
        elif pct >= 41:
            final_msg = f"🥉 MEDALLA DE BRONCE. {n}, ya filtras y agrupas datos reales. Revisa los ✖ para subir de podio."
        elif pct >= 21:
            final_msg = f"🏃 ATLETA EN ENTRENAMIENTO. {n}, cada atleta empieza en la pista de entrenamiento. Relee la teoría y vuelve a intentar."
        else:
            final_msg = f"🌱 {n}, tu ficha de atleta acaba de nacer. Cada celda ejecutada es una vuelta más a la pista."

        ach_display = {
            "primera_medalla":    "🥉 Primera Medalla",
            "relevo_perfecto":    "🥇 Relevo Perfecto",
            "muralla_defensiva":  "🛡️ Muralla Defensiva",
            "doble_podio":        "🎖️ Doble Podio",
            "racha_de_relevos":   "🔥 Racha de Relevos",
            "juegos_completos":   "🏆 Juegos Completos",
        }

        ach_html = ""
        if self._achievements:
            for ak, alabel in ach_display.items():
                if ak in self._achievements:
                    ach_html += (
                        f'<div style="display:inline-flex;align-items:center;gap:5px;'
                        f'padding:3px 8px;background:rgba(255,215,0,.08);'
                        f'border:1px solid #ffd70040;border-radius:2px;margin:2px;">'
                        f'<span style="font-family:\'Press Start 2P\',monospace;font-size:6px;'
                        f'color:#ffd700;">{alabel}</span></div>'
                    )

        lv_color = _lv_color(lvl_num)
        xp_grad  = _XP_GRAD.get(lvl_num, _XP_GRAD[1])

        self._submit_to_supabase(core_earned, _CORE_MAX, pct, lvl_num, lvl_name)

        bonus_html = ""
        if "reto1" in self._scores:
            bonus_html = (
                f'<div style="text-align:center;margin-bottom:16px;font-family:\'Press Start 2P\',monospace;'
                f'font-size:7px;color:#0081C8;letter-spacing:1px;">'
                f'🏆 RETO BONUS: +{bonus_earned}/{_BONUS_MAX} XP extra</div>'
            )

        display(HTML(f'''
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
  @keyframes ok-glow{{0%,100%{{text-shadow:0 0 14px rgba(255,215,0,.8),2px 2px 0 #7a5c00}}
    50%{{text-shadow:0 0 32px rgba(255,215,0,1),0 0 60px rgba(0,129,200,.5),2px 2px 0 #7a5c00}}}}
  @keyframes ok-xp{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
</style>
<div style="background:#0a0e14;border:2px solid #ffd700;border-radius:6px;max-width:840px;
  margin:12px 0;overflow:hidden;
  box-shadow:0 0 40px rgba(255,215,0,.15),0 0 80px rgba(0,129,200,.08),0 10px 40px rgba(0,0,0,.8);">

  <div style="background:linear-gradient(135deg,#0a0e14,#12060a,#0a0e14);
    border-bottom:2px solid #ffd700;padding:22px 28px;text-align:center;position:relative;">
    <div style="position:absolute;left:20px;top:50%;transform:translateY(-50%);">{self._logo_tag}</div>
    <div style="font-family:'Press Start 2P',monospace;font-size:clamp(13px,2.8vw,20px);
      color:#ffd700;animation:ok-glow 2.5s ease-in-out infinite;letter-spacing:3px;
      margin-bottom:8px;">🏅 MISIÓN 1: DATOS 🏅</div>
    <div style="font-family:'Press Start 2P',monospace;font-size:8px;color:#df0024;
      letter-spacing:2px;">SEMANA 2 — RESUMEN FINAL</div>
    <div style="position:absolute;right:20px;top:50%;transform:translateY(-50%);">{self._logo_tag}</div>
  </div>

  <div style="padding:24px 28px;">
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:20px;">
      <div style="background:#080a10;border:1px solid #1a2233;border-radius:3px;
        padding:16px;text-align:center;">
        <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#555566;
          letter-spacing:1px;margin-bottom:10px;">XP TOTAL</div>
        <div style="font-family:'Press Start 2P',monospace;font-size:clamp(14px,3vw,22px);
          color:#ffd700;">{core_earned}/{_CORE_MAX}</div>
      </div>
      <div style="background:#080a10;border:1px solid #1a2233;border-radius:3px;
        padding:16px;text-align:center;">
        <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#555566;
          letter-spacing:1px;margin-bottom:10px;">NIVEL</div>
        <div style="font-family:'Press Start 2P',monospace;font-size:clamp(8px,1.5vw,12px);
          color:{lv_color};">{lvl_name}</div>
      </div>
      <div style="background:#080a10;border:1px solid #1a2233;border-radius:3px;
        padding:16px;text-align:center;">
        <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#555566;
          letter-spacing:1px;margin-bottom:10px;">SCORE</div>
        <div style="font-family:'Press Start 2P',monospace;font-size:clamp(14px,3vw,22px);
          color:#4caf50;">{pct}%</div>
      </div>
    </div>

    <div style="margin-bottom:20px;">
      <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
        <span style="font-family:'Press Start 2P',monospace;font-size:7px;color:#555566;">
          PROGRESO</span>
        <span style="font-family:'Press Start 2P',monospace;font-size:7px;color:{lv_color};">
          {pct}%</span>
      </div>
      <div style="width:100%;height:14px;background:#12141f;border:1px solid #1a2233;
        border-radius:3px;overflow:hidden;">
        <div style="width:{pct}%;height:100%;background:{xp_grad};
          border-radius:3px;transform-origin:left;
          animation:ok-xp 1.4s cubic-bezier(.4,0,.2,1) forwards;
          box-shadow:0 0 8px rgba(255,215,0,.4);"></div>
      </div>
    </div>

    {bonus_html}

    <div style="background:#080a10;border:1px solid #0081C8;border-radius:3px;
      padding:14px 18px;margin-bottom:20px;text-align:center;">
      <div style="font-size:13px;color:#f0ece0;line-height:1.7;">{final_msg}</div>
    </div>

    {f"""
    <div style="margin-bottom:16px;">
      <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#555566;
        letter-spacing:1px;margin-bottom:10px;">🏅 LOGROS DESBLOQUEADOS</div>
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
      color:#0081C8;letter-spacing:1px;opacity:.9;">
      📊 Calificación final enviada al leaderboard · {n} · {lvl_name}
    </div>"""}
  </div>
</div>'''))

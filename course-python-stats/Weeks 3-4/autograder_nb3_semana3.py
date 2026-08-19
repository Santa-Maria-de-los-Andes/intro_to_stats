"""
Autograder — Bimestre 3, Mision 2: Buscando Patrones — SEMANA 3 (Clase 1)
EN BUSCA DE LA FELICIDAD EDITION — World Happiness Report 2019

Cubre: check_t1-t14, check_ex1-ex9, check_debug1, check_mini_a, check_mini_b, resumen()
Dataset: 2019_es.csv (156 filas x 10 columnas, World Happiness Report)

Companion file (Semana 4, Clase 2 -- Seccion C + Mini-Proyecto): pendiente,
mismo patron que autograder_nb1_semana2.py (WORKFORCE_HANDOFF.md).

Notas de scoring (ATLAS):
  t1-t5 (Teoria Desbloqueada, antes de la Seccion A) valen 5 pts c/u = 25.
  ex1/ex2 (Seccion A -- scatter propio) valen 15 pts c/u, tal como aparece
  impreso en el markdown del notebook -- no son negociables aqui, cambiar el
  numero rompería la consistencia notebook<->autograder.
  t6 (justo antes de la explicacion del outlier de Catar, Seccion B) vale 5.
  ex3/ex4 (Seccion B -- prediccion vs. realidad) valen 12 pts c/u.
  t7-t14 (Rondas 3-6, un par pre/post por ronda, ninguna incluye Puntaje)
  valen 5 pts c/u = 40. ex5-ex8 (esas mismas cuatro rondas, scatter+.corr()
  combinados en un solo ejercicio) valen 15 pts c/u = 60.
  ex9 (explorar las 6 correlaciones -- antes ex5, renumerado 2026-08-18 para
  dejarle el rango 5-8 a las rondas nuevas) vale 15. debug1 vale 10.
  _CORE_MAX = 25 (t1-5) + 15 (ex1) + 15 (ex2) + 5 (t6) + 12 (ex3) + 12 (ex4)
            + 40 (t7-14) + 15*4 (ex5-8) + 15 (ex9) + 10 (debug1) = 209.
  Sin bonus/reto en esta Clase 1 -- Semana 3 no declara check_retoN.
  **Nota de presupuesto**: 209 pts supera bastante el ~180 XP asignado a
  Semanas 3-4 juntas en WORKFORCE_CONTRACT.md SS2 (que ademas todavia debe
  cubrir Seccion C + Integracion de Semana 4) -- expansion 2026-08-18 pedida
  explicitamente por el usuario (4 rondas nuevas + preguntas pre/post cada
  una), no una desviacion accidental. Ver WORKFORCE_HANDOFF.md para el
  ticket de seguimiento del presupuesto.

Nota Supabase: mismo proyecto/tabla `submissions` que nb1 (Bimestre 3 --
Estadistica en Python), campo "curso"="STAT_2026", "notebook"="nb3_semana3".
Deadline calculado con el mismo intervalo semanal que nb1_semana1 ->
nb1_semana2 (una semana de diferencia): nb1_semana2 cierra 2026-08-24, esta
Semana 3 (nb3_semana3) cierra una semana despues, 2026-08-31 11:59 PM Peru.
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

# ─── Supabase Config (mismo proyecto que nb1) ─────────────────
SUPABASE_URL      = "https://uwykikwutjtkpffwmdiq.supabase.co"
SUPABASE_ANON_KEY = "sb_publishable_aBG6GD4wn9CgpSE-47fagQ_sNhnzznu"
LOGO_URL          = "https://raw.githubusercontent.com/Santa-Maria-de-los-Andes/CS1---Grader/main/icono%20SMA.png"
CURSO_ID          = "STAT_2026"
NOTEBOOK_ID       = "nb3_semana3"

# ─── Deadline: 31 agosto 2026, 11:59 PM Peru (UTC-5) = 1 sept 04:59 UTC ───
_DEADLINE_UTC   = _dt.datetime(2026, 8, 31, 4, 59, 0, tzinfo=_dt.timezone.utc)
DEADLINE_PASSED = _dt.datetime.now(_dt.timezone.utc) >= _DEADLINE_UTC

# ─── Scoring ─────────────────────────────────────────────────
_CORE_MAX = 209   # 25 (t1-5) + 15+15 (ex1,ex2) + 5 (t6) + 12+12 (ex3,ex4)
                  # + 40 (t7-14) + 15*4 (ex5-8) + 15 (ex9) + 10 (debug1)

# ─── Niveles "En Busca de la Felicidad" (por % del score core) ───
_LEVELS = [
    (96, 6, "🏆 En la Cima del Bienestar"),
    (81, 5, "☀️ Casi Amanece"),
    (61, 4, "🧭 Explorador de Patrones"),
    (41, 3, "🌻 Floreciendo con los Datos"),
    (21, 2, "🌤️ Primeros Rayos de Sol"),
    (0,  1, "🌱 Semilla de Curiosidad"),
]

_XP_GRAD = {
    1: "linear-gradient(90deg,#33402c,#6f8f57)",
    2: "linear-gradient(90deg,#7a5c00,#ffd166)",
    3: "linear-gradient(90deg,#7a4400,#ffb703)",
    4: "linear-gradient(90deg,#0d3a52,#4aa8d8)",
    5: "linear-gradient(90deg,#803d00,#ff9e2c)",
    6: "linear-gradient(90deg,#ff9e2c,#ffd166,#4aa8d8)",
}
_LV_CSS_COLOR = {1: "#8fae7a", 2: "#ffd166", 3: "#ffb703", 4: "#4aa8d8", 5: "#ff9e2c", 6: "#ffd166"}


def _level_info(pct):
    for thresh, num, name in _LEVELS:
        if pct >= thresh:
            return num, name
    return 1, "🌱 Semilla de Curiosidad"


def _lv_color(n):
    return _LV_CSS_COLOR.get(n, "#8fae7a")


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


# Nombres reales de columna (con tildes) usados por el dataset.
_COL_PUNTAJE      = "Puntaje"
_COL_PUESTO       = "Puesto"
_COL_PBI          = "PBI per cápita"
_COL_APOYO        = "Apoyo social"
_COL_ESPERANZA    = "Esperanza de vida saludable"
_COL_LIBERTAD     = "Libertad para tomar decisiones"
_COL_GENEROSIDAD  = "Generosidad"
_COL_CORRUPCION   = "Percepción de corrupción"

_SEIS_COLUMNAS = [_COL_PBI, _COL_APOYO, _COL_ESPERANZA, _COL_LIBERTAD, _COL_GENEROSIDAD, _COL_CORRUPCION]


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
  <div style="background:#12100a;border:1px solid #4aa8d8;border-radius:3px;
    padding:12px 20px;margin-top:6px;
    font-family:'Press Start 2P',monospace;animation:ag-fadein .4s ease .1s both;">
    <div style="font-size:6px;color:#4aa8d8;letter-spacing:2px;margin-bottom:10px;">
      ☀️ TU MEJOR MARCA — SEMANA 3</div>
    <div style="display:flex;align-items:center;gap:20px;">
      <div style="font-size:28px;color:#ffd166;
        text-shadow:0 0 16px rgba(255,209,102,.8),2px 2px 0 #7a5c00;">
        {_best['pct']}%</div>
      <div>
        <div style="font-size:8px;color:#ff9e2c;letter-spacing:1px;">{_best['level_name']}</div>
        <div style="font-size:6px;color:#a8a08a;margin-top:6px;letter-spacing:1px;">
          {_best['earned']} / {_best['possible']} XP</div>
      </div>
    </div>
  </div>'''
                else:
                    _score_html = (
                        '<div style="background:#12100a;border:1px solid #26241a;border-radius:3px;'
                        'padding:10px 20px;margin-top:6px;'
                        'font-family:\'Press Start 2P\',monospace;font-size:6px;color:#6a6656;'
                        'letter-spacing:1px;animation:ag-fadein .4s ease .1s both;">'
                        '☀️ Primer amanecer — ¡aun no tienes marca registrada!</div>'
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
  <div style="background:#140c04;border:1px solid #ff9e2c;border-radius:3px;padding:12px 18px;
    font-family:'Press Start 2P',monospace;font-size:8px;
    color:#ff9e2c;letter-spacing:1px;animation:ag-fadein .4s ease;">
    ☀️ &nbsp;¡BIENVENIDO, BUSCADOR {nombre.upper()}! &nbsp;·&nbsp; {grado}
  </div>
  {_score_html}
  <div id="ag-loading" style="background:#12100a;border:1px solid #26241a;border-radius:3px;
    padding:22px 18px;margin-top:6px;text-align:center;animation:ag-fadein .5s ease .2s both;">
    <div style="display:flex;justify-content:center;gap:6px;margin-bottom:12px;">
      <div style="width:8px;height:8px;border-radius:50%;background:#ff9e2c;
        animation:ag-dot 1.2s ease-in-out 0s infinite;"></div>
      <div style="width:8px;height:8px;border-radius:50%;background:#ff9e2c;
        animation:ag-dot 1.2s ease-in-out .2s infinite;"></div>
      <div style="width:8px;height:8px;border-radius:50%;background:#ff9e2c;
        animation:ag-dot 1.2s ease-in-out .4s infinite;"></div>
    </div>
    <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#6a6656;letter-spacing:2px;">
      BUSCANDO PATRONES…
    </div>
  </div>
  <div id="ag-start" style="display:none;background:linear-gradient(160deg,#12100a,#1e1406);
    border:2px solid #ff9e2c;border-radius:4px;padding:36px 24px;margin-top:6px;text-align:center;
    box-shadow:0 0 40px rgba(255,158,44,.25),0 0 80px rgba(255,209,102,.06),0 6px 24px rgba(0,0,0,.9);">
    <div style="font-size:44px;margin-bottom:14px;animation:ag-start .55s cubic-bezier(.34,1.56,.64,1);">☀️</div>
    <div style="font-family:'Press Start 2P',monospace;font-size:clamp(15px,3.6vw,26px);color:#ffd166;
      letter-spacing:4px;text-shadow:0 0 24px rgba(255,209,102,.95),0 0 50px rgba(255,158,44,.35),
      2px 2px 0 #7a5c00;animation:ag-start .6s ease;margin-bottom:14px;">¡TU MISIÓN COMIENZA!</div>
    <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#4aa8d8;
      letter-spacing:2px;opacity:.85;margin-bottom:16px;">EJECUTA LA PRIMERA CELDA PARA COMENZAR</div>
    <div style="font-size:15px;color:#ff9e2c;opacity:.4;letter-spacing:8px;">☀️ 🌻 ☀️ 🌻 ☀️ 🌻 ☀️</div>
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

            display(HTML(f'''
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
  .ag-input,.ag-select {{
    width:100%;box-sizing:border-box;background:#12100a;border:1px solid #26241a;
    border-radius:3px;padding:0 12px;color:#f0ece0;font-size:13px;height:42px;
    font-family:'Segoe UI',Roboto,sans-serif;outline:none;transition:border .2s;
  }}
  .ag-input:focus,.ag-select:focus {{ border-color:#4aa8d8; }}
  .ag-select option {{ background:#12100a; }}
  .ag-btn {{
    width:100%;padding:13px;background:linear-gradient(90deg,#b56a00,#ff9e2c);
    border:none;border-radius:3px;color:#12100a;font-family:'Press Start 2P',monospace;
    font-size:9px;letter-spacing:2px;cursor:pointer;transition:opacity .2s;margin-top:6px;
  }}
  .ag-btn:hover {{ opacity:.85; }}
  .ag-err {{ color:#ff5d5d;font-size:11px;margin-top:6px;display:none; }}
  .ag-label {{ font-family:'Press Start 2P',monospace;font-size:7px;letter-spacing:1px;
    margin-bottom:8px;display:flex;align-items:center;gap:5px; }}
  .ag-field {{ display:flex;flex-direction:column; }}
</style>
<div style="background:#12100a;border:2px solid #4aa8d8;border-radius:4px;max-width:840px;
  margin:10px 0;overflow:hidden;box-shadow:0 0 40px rgba(74,168,216,.2),0 10px 30px rgba(0,0,0,.8);">

  <div style="background:linear-gradient(90deg,#12100a,#1e1406,#12100a);border-bottom:2px solid #ffd166;
    padding:18px 24px;position:relative;display:flex;align-items:center;justify-content:center;min-height:80px;">
    <div style="position:absolute;left:20px;top:50%;transform:translateY(-50%);">{logo_tag}</div>
    <div style="text-align:center;">
      <div style="font-family:'Press Start 2P',monospace;font-size:clamp(13px,3vw,18px);color:#ffd166;letter-spacing:3px;
        text-shadow:0 0 14px rgba(255,209,102,.7),2px 2px 0 #7a5c00;">☀️ MISIÓN 2: BUSCANDO PATRONES 🧭</div>
      <div style="font-family:'Press Start 2P',monospace;font-size:8px;color:#ff9e2c;
        letter-spacing:2px;margin-top:8px;">SEMANA 3 — EN BUSCA DE LA FELICIDAD</div>
    </div>
    <div style="position:absolute;right:20px;top:50%;transform:translateY(-50%);">{logo_tag}</div>
  </div>

  <div style="padding:24px;">
    <div style="display:grid;grid-template-columns:2fr 1fr;gap:14px;margin-bottom:14px;align-items:end;">
      <div class="ag-field">
        <div class="ag-label" style="color:#ff9e2c;">☀️ NOMBRE COMPLETO</div>
        <input id="ag-nombre" class="ag-input" placeholder="Tu nombre y apellido" />
      </div>
      <div class="ag-field">
        <div class="ag-label" style="color:#ff9e2c;">🏫 GRADO</div>
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
    <button class="ag-btn" onclick="agRegister()">☀️ &nbsp; ¡COMENZAR LA BÚSQUEDA! &nbsp; 🧭</button>
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
                display(HTML('<div style="font-family:monospace;padding:10px;background:#12100a;'
                             'color:#ff9e2c;border:1px solid #4aa8d8;border-radius:3px;max-width:840px;">'
                             '☀️ MISIÓN 2 — SEMANA 3 — Registro</div>'))
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
        n = _get("nombre")
        if isinstance(n, str) and n.strip() and n.strip() not in ("?", ""):
            return n.strip()
        return "buscador"

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

    def _header(self, title, icon="☀️", pts=None):
        self._curr_title = title
        self._curr_icon  = icon
        self._curr_pts   = pts

    def _check_achievements(self, key):
        unlocked = []
        earned, possible, pct = self._totals()

        # Primer Rayo de Sol — primer XP ganado
        if any(e > 0 for e, _ in self._scores.values()) and self._unlock("primer_rayo"):
            unlocked.append(("☀️ Primer Rayo de Sol — ¡Tu primer punto de felicidad conquistado!", "#ff9e2c", "Chispa"))

        # Ojo Entrenado — ex1+ex2 perfectos (Seccion A completa)
        ex_ab = ["ex1", "ex2"]
        if (all(k in self._scores and self._scores[k][0] == self._scores[k][1] for k in ex_ab)
                and self._unlock("ojo_entrenado")):
            unlocked.append(("👁️ Ojo Entrenado — Tus dos scatters de la Sección A, perfectos", "#4aa8d8", "Rayo"))

        # Numero Exacto — ex3+ex4 perfectos (prediccion vs. realidad)
        ex_pred = ["ex3", "ex4"]
        if (all(k in self._scores and self._scores[k][0] == self._scores[k][1] for k in ex_pred)
                and self._unlock("numero_exacto")):
            unlocked.append(("🔢 Número Exacto — Tu predicción, confirmada con datos reales", "#4aa8d8", "Rayo"))

        # Cartografo de Patrones — ex5,ex6,ex7,ex8 perfectos (las 4 rondas sin Puntaje)
        ex_extra = ["ex5", "ex6", "ex7", "ex8"]
        if (all(k in self._scores and self._scores[k][0] == self._scores[k][1] for k in ex_extra)
                and self._unlock("cartografo_patrones")):
            unlocked.append(("🗺️ Cartógrafo de Patrones — Cuatro pares nuevos, cuatro relaciones distintas", "#4aa8d8", "Rayo"))

        # Explorador Completo — ex9 perfecto
        if (self._scores.get("ex9", (0, 1))[0] == self._scores.get("ex9", (0, 1))[1]
                and "ex9" in self._scores and self._unlock("explorador_completo")):
            unlocked.append(("🧭 Explorador Completo — Recorriste las seis variables del bienestar", "#ffb703", "Amanecer"))

        # Depurador Feliz — debug1 perfecto
        if (self._scores.get("debug1", (0, 1))[0] == self._scores.get("debug1", (0, 1))[1]
                and "debug1" in self._scores and self._unlock("depurador_feliz")):
            unlocked.append(("🔧 Depurador Feliz — Encontraste el error sin perder la calma", "#ffb703", "Amanecer"))

        # Medalla del Camino — ambos checkpoints alcanzados
        if len(self._checkpoints) >= 2 and self._unlock("medalla_camino"):
            unlocked.append(("🌻 Medalla del Camino — Ambos checkpoints superados", "#ffb703", "Amanecer"))

        # Racha de Bienestar — racha >= 5
        if self._streak >= 5 and self._unlock("racha_bienestar"):
            unlocked.append(("🔥 Racha de Bienestar — Combo x5", "#4aa8d8", "Rayo"))

        # Felicidad Plena — 100% del core
        if pct >= 100 and self._unlock("felicidad_plena"):
            unlocked.append(("🏆 Felicidad Plena — 100% de la Semana 3", "#ff9e2c", "Sol Pleno"))

        # Level-up
        lvl_num, lvl_name = _level_info(pct)
        if lvl_num > self._prev_level and self._prev_level > 0:
            unlocked.append((f"⬆️ ¡SUBISTE DE NIVEL! — {lvl_name}", "#4aa8d8", "Nivel"))
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
                    f'<span style="color:#a8a08a;">{msg}</span></div></div>'
                )
            else:
                rows_html += (
                    f'<div style="display:flex;align-items:flex-start;gap:10px;padding:7px 10px;'
                    f'margin-bottom:3px;background:rgba(255,93,93,.06);'
                    f'border-left:3px solid #ff5d5d;border-radius:0 3px 3px 0;">'
                    f'<span style="color:#ff5d5d;font-size:13px;flex-shrink:0;line-height:1.5;">✖</span>'
                    f'<div style="font-size:11px;line-height:1.5;">'
                    f'<span style="color:#ff5d5d;font-weight:bold;">{label}:</span> '
                    f'<span style="color:#cc9988;">{msg}</span></div></div>'
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
            c_color = "#ff9e2c" if self._streak >= 5 else "#ffd166"
            combo_html = (
                f'<div style="display:inline-flex;align-items:center;gap:5px;padding:3px 10px;'
                f'background:rgba(255,158,44,.12);border:1px solid {c_color};border-radius:2px;'
                f'margin-left:8px;">'
                f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;'
                f'color:{c_color};">☀️ RACHA x{self._streak}</span></div>'
            )

        if pts == max_pts:
            s_icon, s_text, s_color = "☀️", f"¡RAYO DE SOL COMPLETO! +{pts} XP", "#4caf50"
            border_color, glow = "#4caf50", "0 0 22px rgba(76,175,80,.15)"
        elif pts > 0:
            s_icon, s_text, s_color = "🌤️", f"+{pts} XP  ·  {max_pts - pts} por brillar", "#ffd166"
            border_color, glow = "#ffb703", "0 0 22px rgba(255,183,3,.12)"
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
            "Chispa":    ("#8fae7a", "rgba(143,174,122,.12)", "🌱"),
            "Rayo":      ("#4aa8d8", "rgba(74,168,216,.12)",  "🌤️"),
            "Amanecer":  ("#ffb703", "rgba(255,183,3,.10)",   "🌻"),
            "Sol Pleno": ("#ff9e2c", "rgba(255,158,44,.15)",  "☀️"),
        }
        ach_html = ""
        for ach_name, _, ach_rarity in reg_ach:
            bc, bg, ach_icon = _RC.get(ach_rarity, _RC["Chispa"])
            ach_html += (
                f'<div style="display:flex;align-items:center;gap:10px;margin-top:8px;'
                f'padding:10px 12px;background:{bg};border:1px solid {bc};border-radius:3px;">'
                f'<span style="font-size:18px;">{ach_icon}</span>'
                f'<div style="flex:1;">'
                f'<div style="margin-bottom:3px;">'
                f'<span style="background:{bc};color:#12100a;font-size:7px;font-weight:bold;'
                f'padding:1px 5px;border-radius:2px;font-family:\'Press Start 2P\',monospace;">'
                f'{ach_rarity.upper()}</span>'
                f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;'
                f'color:{bc};margin-left:6px;">LOGRO DESBLOQUEADO</span>'
                f'</div>'
                f'<div style="color:#f0ece0;font-size:12px;font-weight:bold;">{ach_name}</div>'
                f'</div></div>'
            )

        curr_icon  = getattr(self, '_curr_icon', '☀️')
        curr_title = getattr(self, '_curr_title', 'EJERCICIO').upper()
        _logo_sm   = self._logo_tag_sm

        _core_pct_bar = min(round(earned / _CORE_MAX * 100), 100)
        xp_bar_html = (
            f'<div style="display:flex;justify-content:space-between;margin-bottom:4px;">'
            f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;color:#6a6656;">'
            f'XP: {earned}/{_CORE_MAX}</span>'
            f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;'
            f'color:{_lv_color(lvl_num)};">{lvl_name}</span></div>'
            f'<div style="width:100%;height:10px;background:#1c1810;border:1px solid #26241a;'
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
                             'font-size:6px;color:#4aa8d8;letter-spacing:1px;opacity:.85;">'
                             '📊 Calificación actualizada en la base de datos</div>')

        card_html = f'''<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
  @keyframes pg-xpscale{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
</style>
<div style="background:#12100a;border:2px solid {border_color};border-radius:4px;max-width:840px;
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
      <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#ff9e2c;
        background:rgba(255,158,44,.1);border:1px solid rgba(255,158,44,.4);
        padding:3px 8px;border-radius:2px;">MAX {max_pts} XP</div>
    </div>
  </div>
  <div style="padding:10px 14px 6px;">{rows_html}</div>
  <div style="background:#0d0b06;border-top:1px solid #1a1710;padding:11px 14px;">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:9px;">
      <div style="display:flex;align-items:center;gap:8px;">
        <span style="font-size:16px;">{s_icon}</span>
        <span style="font-family:'Press Start 2P',monospace;font-size:8px;
          color:{s_color};">{s_text}</span>
        {combo_html}
      </div>
      <div style="display:flex;align-items:center;gap:4px;color:#6a6656;font-size:10px;">
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
            2: dict(bg="linear-gradient(160deg,#12100a,#1a1400)",
                    c="#ffd166", sc="#ffe6a3", rc="#ffd166",
                    sub="PRIMEROS RAYOS DE SOL — TU MISIÓN COMIENZA", icon="🌤️"),
            3: dict(bg="linear-gradient(160deg,#141005,#1a1400)",
                    c="#ffb703", sc="#ffd27f", rc="#ffb703",
                    sub="FLORECIENDO CON LOS DATOS — LOS PATRONES APARECEN", icon="🌻"),
            4: dict(bg="linear-gradient(160deg,#0a1420,#0d2436)",
                    c="#4aa8d8", sc="#8fcbee", rc="#4aa8d8",
                    sub="EXPLORADOR DE PATRONES — TU OJO YA CONFÍA EN EL NÚMERO", icon="🧭"),
            5: dict(bg="linear-gradient(160deg,#180d02,#2a1400)",
                    c="#ff9e2c", sc="#ffc27a", rc="#ff9e2c",
                    sub="CASI AMANECE — EL BIENESTAR SE VE CLARO", icon="☀️"),
            6: dict(bg="linear-gradient(160deg,#12100a,#1a0f02,#0d1a26)",
                    c="#ffd166", sc="#4aa8d8", rc="#ff9e2c",
                    sub="EN LA CIMA DEL BIENESTAR — SALÓN DE LA FAMA", icon="🏆"),
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
                          f'margin:-50px;border-radius:50%;border:2px solid #4aa8d8;opacity:0;'
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
    ☀️ 🌻 ☀️ 🌻 ☀️</div>
  <div style="position:absolute;right:14px;top:50%;
    font-size:15px;letter-spacing:5px;
    animation:{uid}-rr .9s ease-out .6s both;pointer-events:none;z-index:7;">
    ☀️ 🌻 ☀️ 🌻 ☀️</div>

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
      color:#6a6656;letter-spacing:2px;
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
                f'<div style="height:5px;background:#1a1710;border-radius:2px;overflow:hidden;">'
                f'<div style="width:{bar_w * 100 // 60}%;height:100%;'
                f'background:{color};opacity:.85;border-radius:2px;"></div></div>'
                f'</div>'
                f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;'
                f'color:{color if ok else "#6a6656"};">{e}/{p}</span>'
                f'</div>'
            )
        pct_sec = round(total_e / total_p * 100) if total_p else 0
        display(HTML(
            f'<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">'
            f'<div style="background:#12100a;border:2px solid {color};border-radius:4px;'
            f'max-width:840px;margin:10px 0;padding:18px 20px;'
            f'box-shadow:0 0 20px {color}22,0 4px 16px rgba(0,0,0,.6);">'
            f'<div style="font-family:\'Press Start 2P\',monospace;font-size:9px;'
            f'color:{color};letter-spacing:2px;margin-bottom:16px;">🌻 {title}</div>'
            f'{rows}'
            f'<div style="margin-top:14px;padding-top:10px;border-top:1px solid {color}30;'
            f'display:flex;justify-content:space-between;align-items:center;">'
            f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;color:#8a8570;">'
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
                "nombre":          self._nombre_real or "buscador",
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
                    f'<br><span style="color:#4aa8d8;font-size:7px;">'
                    f'📊 Calificación actualizada en la base de datos</span></div>'
                ))
        except Exception as _ex:
            if not silent:
                display(HTML(
                    f'<div style="font-family:\'Press Start 2P\',monospace;font-size:7px;'
                    f'color:#ff5d5d;background:#1a0005;border:1px solid #ff5d5d;'
                    f'border-radius:3px;padding:10px 16px;max-width:840px;margin-top:6px;">'
                    f'⚠️ Leaderboard no disponible: {_ex}</div>'
                ))

    # ═══════════════════════════════════════════════════════════
    # TEORÍA — check_t1 .. check_t6 (formulario interactivo HTML)
    # ═══════════════════════════════════════════════════════════

    _TEORIA = {
        1: dict(
            title="T1 — ¿Qué mide el coeficiente de correlación?",
            q=("¿Qué resume el coeficiente de correlación (r) entre dos variables numéricas?"),
            opts={"a": "Solo qué tan grande es el promedio de una de las variables",
                  "b": "Qué tan fuerte y en qué dirección se mueven juntas dos variables",
                  "c": "Cuántos valores nulos tiene el dataset",
                  "d": "La forma exacta (curva) de una relación"},
            correct="b",
            why=("El coeficiente de correlación resume dos cosas a la vez: fuerza (qué tan "
                 "consistente es el patrón) y dirección (si suben juntas o al revés)."),
            pts=5,
        ),
        2: dict(
            title="T2 — El rango de -1 a 1",
            q=('Un estudio encuentra que "horas de sueño" y "nivel de estrés reportado" tienen '
               'r ≈ -0.82. ¿Qué significa ese valor?'),
            opts={"a": "Relación fuerte y positiva — más sueño se asocia con más estrés",
                  "b": "Relación fuerte y negativa — más sueño tiende a asociarse con menos estrés",
                  "c": "No hay relación entre las dos variables",
                  "d": "El cálculo está mal, r no puede ser negativo"},
            correct="b",
            why="Un r cercano a -1 es una relación fuerte pero inversa: cuando una variable sube, la otra tiende a bajar.",
            pts=5,
        ),
        3: dict(
            title="T3 — ¿Qué significa un r cercano a 0?",
            q="Dos variables tienen r ≈ 0.03. ¿Qué te dice ese número sobre la relación lineal entre ellas?",
            opts={"a": "Es una relación perfecta",
                  "b": "Es una relación fuerte y negativa",
                  "c": "Hay poca o ninguna relación lineal entre ellas",
                  "d": "Se necesitan más datos para poder calcular r"},
            correct="c",
            why="r cercano a 0 significa que, en línea recta, las dos variables casi no se mueven juntas.",
            pts=5,
        ),
        4: dict(
            title="T4 — Fuerza vs. dirección",
            q=("La variable A tiene r = 0.9 con el puntaje de felicidad, y la variable B tiene "
               "r = 0.3, ambas positivas. ¿Qué diferencia real hay entre esos dos valores?"),
            opts={"a": "Ninguna, ambas son igual de fuertes porque las dos son positivas",
                  "b": "A tiene una relación mucho más fuerte y consistente que B, aunque ambas sean positivas",
                  "c": "B es más fuerte porque su número es más chico",
                  "d": "El signo positivo no importa aquí"},
            correct="b",
            why="El signo (dirección) es el mismo en ambas, pero la distancia a 0 (fuerza) es muy distinta -- 0.9 es un patrón mucho más consistente que 0.3.",
            pts=5,
        ),
        5: dict(
            title="T5 — La regla más importante: correlación no es causalidad",
            q=('Un r ≈ 0.85 entre "horas de ejercicio semanal" y "satisfacción con la vida" '
               'significa que...'),
            opts={"a": "Hacer ejercicio garantiza que una persona sea más feliz",
                  "b": "Las dos variables se mueven juntas de forma consistente, pero el número por sí solo no prueba que una cause la otra",
                  "c": "El ejercicio no tiene relación real con la felicidad",
                  "d": "El r está mal calculado porque involucra personas"},
            correct="b",
            why="Un r alto describe qué tan juntas se mueven dos variables -- nunca prueba, por sí solo, que una sea la causa de la otra.",
            pts=5,
        ),
        6: dict(
            title="T6 — El límite de .corr()",
            q=("Una relación real y fuerte, pero en forma de curva (no una línea recta), "
               "puede dar un valor de r cercano a..."),
            opts={"a": "1, porque .corr() siempre detecta cualquier patrón",
                  "b": "-1, siempre",
                  "c": "0, porque .corr() solo mide relación lineal",
                  "d": "Es imposible calcular r en ese caso"},
            correct="c",
            why="`.corr()` mide específicamente relación lineal -- un patrón real pero curvo puede pasar casi invisible para ese número.",
            pts=5,
        ),
        7: dict(
            title="T7 — Ronda 3, antes de calcular",
            q=("Ya viste que tanto `PBI per cápita` como `Esperanza de vida saludable` "
               "tienen cada una r ≈ 0.78-0.79 con `Puntaje`. ¿Qué puedes concluir sobre "
               "la correlación ENTRE esas dos variables, sin Puntaje de por medio?"),
            opts={"a": "Tiene que ser también ≈0.78, porque ambas se relacionan igual con Puntaje",
                  "b": "No se puede saber su valor exacto sin calcularlo directamente -- que ambas se relacionen con una tercera variable no fija su relación mutua",
                  "c": "Tiene que ser 0, porque ya \"usaron\" su relación con Puntaje",
                  "d": "Tiene que ser negativa, porque son variables distintas"},
            correct="b",
            why=("La correlación no es transitiva: que A y B se relacionen con C no dice "
                 "cuánto se relacionan A y B entre sí. Hay que calcularlo directamente, "
                 "como vas a hacer ahora."),
            pts=5,
        ),
        8: dict(
            title="T8 — Ronda 3, interpreta tu resultado",
            q=("Acabas de calcular que `PBI per cápita` y `Esperanza de vida saludable` "
               "tienen r ≈ 0.84 -- más fuerte incluso que la relación de cualquiera de las "
               "dos con `Puntaje`. ¿Cuál es la lectura correcta de ese número?"),
            opts={"a": "Los países ricos causan que su población viva más años",
                  "b": "Es un error de cálculo -- dos variables que no son Puntaje no pueden tener una relación tan fuerte",
                  "c": "Los países con mayor producción económica por persona tienden a reportar también mayor esperanza de vida saludable -- una relación observada muy fuerte, no una prueba de causa",
                  "d": "r ≈ 0.84 significa que el 84% de los países tienen ambos valores altos"},
            correct="c",
            why=("Un r alto describe qué tan consistentemente se mueven juntas dos "
                 "variables -- nunca prueba causa, y no es un porcentaje de países."),
            pts=5,
        ),
        9: dict(
            title="T9 — Ronda 4, antes de calcular",
            q=("¿Por qué tiene sentido calcular r entre dos variables explicativas "
               "(ninguna de las dos es Puntaje), como vas a hacer ahora?"),
            opts={"a": "Porque el curso lo exige, no tiene una razón estadística",
                  "b": "Porque dos variables explicativas pueden estar relacionadas entre sí, y eso es información real más allá de su relación con Puntaje",
                  "c": "Porque Puntaje deja de importar una vez que lo calculaste una vez",
                  "d": "No tiene ningún uso real, es solo práctica repetida"},
            correct="b",
            why=("Las variables que usas para explicar algo (aquí, el bienestar) pueden "
                 "estar relacionadas entre sí -- entender eso es parte de leer un dataset "
                 "con honestidad, no solo mirar cada una contra el objetivo final."),
            pts=5,
        ),
        10: dict(
            title="T10 — Ronda 4, interpreta tu resultado",
            q=("Calculaste r ≈ 0.72 entre `Apoyo social` y `Esperanza de vida saludable`. "
               "¿Cuál es la lectura correcta?"),
            opts={"a": "Todos los países con Apoyo social alto tienen la Esperanza de vida más alta del dataset",
                  "b": "Los países con mayor apoyo social percibido tienden a reportar también mayor esperanza de vida saludable -- una relación observada fuerte, no una regla sin excepciones",
                  "c": "r ≈ 0.72 significa que no hay relación real entre las dos variables",
                  "d": "El signo debería ser negativo porque son conceptos completamente distintos"},
            correct="b",
            why=("Fuerte y positivo no significa \"sin excepciones\" -- significa que la "
                 "tendencia general es consistente, no que cada fila individual la cumpla."),
            pts=5,
        ),
        11: dict(
            title="T11 — Ronda 5, antes de calcular",
            q=("Hasta ahora, en las rondas sin Puntaje viste r ≈ 0.72 y r ≈ 0.84 (fuertes). "
               "Si un nuevo par te da r ≈ 0.44, ¿qué tan fuerte es esa relación, comparada "
               "con las anteriores?"),
            opts={"a": "Sigue siendo igual de fuerte que las anteriores",
                  "b": "Es una relación real y positiva, pero notablemente menos consistente que las que viste antes",
                  "c": "No es una relación real -- hay que ignorarla por completo",
                  "d": "Es imposible que dos pares del mismo dataset tengan r tan distinto"},
            correct="b",
            why=("r ≈ 0.44 sigue siendo un patrón real y positivo -- solo que mucho menos "
                 "consistente que uno de 0.72 u 0.84. Distintos pares, distinta fuerza, "
                 "mismo dataset."),
            pts=5,
        ),
        12: dict(
            title="T12 — Ronda 5, interpreta tu resultado",
            q=("`Libertad para tomar decisiones` y `Percepción de corrupción` te dieron "
               "r ≈ 0.44. ¿Cuál interpretación es correcta?"),
            opts={"a": "Sentirse libre para tomar decisiones causa que un país perciba menos corrupción",
                  "b": "Los países con mayor libertad percibida tienden, de forma moderada, a percibir también algo menos de corrupción -- una relación real pero bastante menos consistente que las de las rondas anteriores",
                  "c": "r ≈ 0.44 es prácticamente 0, no vale la pena mencionarlo",
                  "d": "El resultado no se puede interpretar porque las dos variables son percepciones subjetivas"},
            correct="b",
            why=("Un r moderado (ni cerca de 0 ni cerca de ±1) sigue siendo una lectura "
                 "real -- solo hay que describirlo con la fuerza que realmente tiene, sin "
                 "inflarlo a \"fuerte\" ni descartarlo como \"nada\"."),
            pts=5,
        ),
        13: dict(
            title="T13 — Ronda 6, antes de calcular",
            q=("Vas a calcular la correlación entre `PBI per cápita` y `Generosidad`. Si el "
               "resultado te da un número negativo pero muy cercano a 0 (por ejemplo, "
               "-0.08), ¿qué deberías concluir?"),
            opts={"a": "Que hay una relación negativa fuerte entre las dos variables",
                  "b": "Que casi no hay relación lineal entre las dos variables -- el signo negativo no es informativo cuando el número está tan cerca de 0",
                  "c": "Que el cálculo está mal, porque r no puede ser negativo",
                  "d": "Que los países ricos son menos generosos, sin excepción"},
            correct="b",
            why=("Cerca de 0, el signo deja de ser el dato importante -- lo que importa es "
                 "que el valor está pegado a 0, es decir, casi sin relación lineal."),
            pts=5,
        ),
        14: dict(
            title="T14 — Ronda 6, interpreta tu resultado",
            q=("Confirmaste que `PBI per cápita` y `Generosidad` tienen r ≈ -0.08. ¿Qué te "
               "dice esto sobre estas dos variables en el dataset?"),
            opts={"a": "El dinero de un país destruye la generosidad de su gente",
                  "b": "Es el par más fuerte de toda la clase de hoy",
                  "c": "Casi no hay relación lineal -- saber el PBI per cápita de un país casi no ayuda a predecir qué tan generosa es su gente",
                  "d": "El resultado es un error porque Generosidad debería depender del PBI"},
            correct="c",
            why=("r ≈ -0.08 está pegado a 0: prácticamente no hay relación lineal detectable "
                 "entre estas dos variables en este dataset, ni fuerte ni débil-pero-real."),
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
            f'<div style="max-width:840px;margin:10px 0;background:#12100a;'
            f'border:2px solid {color};border-radius:4px;padding:14px 18px;'
            f'font-family:\'Segoe UI\',Roboto,sans-serif;">'
            f'<div style="font-family:\'Press Start 2P\',monospace;font-size:9px;'
            f'color:#a8a08a;letter-spacing:1px;margin-bottom:8px;">'
            f'🔒 {spec["title"]} — YA RESPONDIDA</div>'
            f'<div style="color:{color};font-size:13px;">{estado}</div>'
            f'<div style="color:#a8a08a;font-size:12px;margin-top:6px;">'
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
                    f'margin-bottom:8px;background:#171307;border:2px solid #4aa8d8;'
                    f'border-radius:4px;color:#f0ece0;font-family:\'Segoe UI\',Roboto,sans-serif;'
                    f'font-size:13px;cursor:pointer;transition:all .15s;">'
                    f'<span style="font-family:\'Press Start 2P\',monospace;font-size:9px;'
                    f'color:#ffd166;margin-right:10px;">{L.upper()}</span>{spec["opts"][L]}</button>'
                )

            display(HTML(f'''
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
  .{uid}-opt:hover {{ border-color:#ffd166 !important; background:#1e1a0c !important; }}
</style>
<div id="{uid}-wrap" style="background:#12100a;border:2px solid #4aa8d8;border-radius:4px;
  max-width:840px;margin:10px 0;overflow:hidden;box-shadow:0 6px 24px rgba(0,0,0,.7);">
  <div style="background:#4aa8d818;border-bottom:1px solid #4aa8d840;padding:10px 16px;">
    <span style="font-family:'Press Start 2P',monospace;font-size:9px;color:#4aa8d8;
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
    def check_t6(self): return self._ask_teoria(6)
    def check_t7(self): return self._ask_teoria(7)
    def check_t8(self): return self._ask_teoria(8)
    def check_t9(self): return self._ask_teoria(9)
    def check_t10(self): return self._ask_teoria(10)
    def check_t11(self): return self._ask_teoria(11)
    def check_t12(self): return self._ask_teoria(12)
    def check_t13(self): return self._ask_teoria(13)
    def check_t14(self): return self._ask_teoria(14)

    # ═══════════════════════════════════════════════════════════
    # SECCIÓN A — Antes de Calcular (scatter propio)
    # ═══════════════════════════════════════════════════════════

    def check_ex1(self):
        """Ex1 — Scatter propio: Percepción de corrupción vs. Puntaje (15 pts)"""
        self._header("EJERCICIO 1 — Tu Propio Scatter 📊", icon="📊", pts=15)
        checks = []
        df = _get("df_felicidad")
        x_ex1 = _get("x_ex1")
        y_ex1 = _get("y_ex1")

        if x_ex1 is None:
            checks.append((False, "x_ex1", "No definida — usa 'Percepción de corrupción' en el eje X"))
        elif _col_match(x_ex1, _COL_CORRUPCION, df):
            checks.append((True, "x_ex1 == 'Percepción de corrupción'", "✓"))
        else:
            checks.append((False, "x_ex1", f"Debe ser 'Percepción de corrupción', obtuve '{x_ex1}'"))

        if y_ex1 is None:
            checks.append((False, "y_ex1", "No definida — usa 'Puntaje' en el eje Y"))
        elif _col_match(y_ex1, _COL_PUNTAJE, df):
            checks.append((True, "y_ex1 == 'Puntaje'", "✓"))
        else:
            checks.append((False, "y_ex1", f"Debe ser 'Puntaje', obtuve '{y_ex1}'"))

        return self._award("ex1", checks, 15)

    def check_ex2(self):
        """Ex2 — Scatter propio: Esperanza de vida saludable vs. Puntaje (15 pts)"""
        self._header("EJERCICIO 2 — Tu Propio Scatter, Otra Vez 📊", icon="📊", pts=15)
        checks = []
        df = _get("df_felicidad")
        x_ex2 = _get("x_ex2")
        y_ex2 = _get("y_ex2")

        if x_ex2 is None:
            checks.append((False, "x_ex2", "No definida — usa 'Esperanza de vida saludable' en el eje X"))
        elif _col_match(x_ex2, _COL_ESPERANZA, df):
            checks.append((True, "x_ex2 == 'Esperanza de vida saludable'", "✓"))
        else:
            checks.append((False, "x_ex2", f"Debe ser 'Esperanza de vida saludable', obtuve '{x_ex2}'"))

        if y_ex2 is None:
            checks.append((False, "y_ex2", "No definida — usa 'Puntaje' en el eje Y"))
        elif _col_match(y_ex2, _COL_PUNTAJE, df):
            checks.append((True, "y_ex2 == 'Puntaje'", "✓"))
        else:
            checks.append((False, "y_ex2", f"Debe ser 'Puntaje', obtuve '{y_ex2}'"))

        return self._award("ex2", checks, 15)

    # ═══════════════════════════════════════════════════════════
    # CHECKPOINT — Teoría Desbloqueada + Sección A
    # ═══════════════════════════════════════════════════════════

    def check_mini_a(self):
        """Checkpoint — Teoría Desbloqueada + Sección A"""
        self._checkpoints.add("mini_a")
        seccion = {
            "t1": ("T1 — Qué mide el coeficiente de correlación", 5),
            "t2": ("T2 — El rango de -1 a 1", 5),
            "t3": ("T3 — r cercano a 0", 5),
            "t4": ("T4 — Fuerza vs. dirección", 5),
            "t5": ("T5 — Correlación no es causalidad", 5),
            "ex1": ("Ejercicio 1 – Scatter de corrupción", 15),
            "ex2": ("Ejercicio 2 – Scatter de esperanza de vida", 15),
        }
        self._render_checkpoint("CHECKPOINT — PRIMEROS RAYOS DE SOL", seccion, "#4aa8d8")

    # ═══════════════════════════════════════════════════════════
    # SECCIÓN B — Calcúlalo (.corr())
    # ═══════════════════════════════════════════════════════════

    def check_ex3(self):
        """Ex3 — r real: Percepción de corrupción vs. Puntaje (12 pts)"""
        self._header("EJERCICIO 3 — Predicción Contra la Realidad 🔢", icon="🔢", pts=12)
        checks = []
        r_corrupcion = _get("r_corrupcion")
        EXP = 0.3856130708664784

        if r_corrupcion is None:
            checks.append((False, "r_corrupcion",
                           "No definida — usa df_felicidad['Percepción de corrupción'].corr(df_felicidad['Puntaje'])"))
        elif not _is_number(r_corrupcion):
            checks.append((False, "r_corrupcion", f"Debe ser número, recibí {type(r_corrupcion).__name__}"))
        elif _approx(r_corrupcion, EXP, tol=0.01):
            checks.append((True, f"r_corrupcion ≈ {EXP:.3f}", "✓"))
        else:
            checks.append((False, "r_corrupcion", f"Debe ser ≈{EXP:.3f}, obtuve {r_corrupcion}"))

        return self._award("ex3", checks, 12)

    def check_ex4(self):
        """Ex4 — r real: Esperanza de vida saludable vs. Puntaje (12 pts)"""
        self._header("EJERCICIO 4 — Predicción Contra la Realidad, Otra Vez 🔢", icon="🔢", pts=12)
        checks = []
        r_esperanza = _get("r_esperanza")
        EXP = 0.7798831492425831

        if r_esperanza is None:
            checks.append((False, "r_esperanza",
                           "No definida — usa df_felicidad['Esperanza de vida saludable'].corr(df_felicidad['Puntaje'])"))
        elif not _is_number(r_esperanza):
            checks.append((False, "r_esperanza", f"Debe ser número, recibí {type(r_esperanza).__name__}"))
        elif _approx(r_esperanza, EXP, tol=0.01):
            checks.append((True, f"r_esperanza ≈ {EXP:.3f}", "✓"))
        else:
            checks.append((False, "r_esperanza", f"Debe ser ≈{EXP:.3f}, obtuve {r_esperanza}"))

        return self._award("ex4", checks, 12)

    # ═══════════════════════════════════════════════════════════
    # RONDAS 3-6 — scatter + .corr() combinados, sin Puntaje
    # ═══════════════════════════════════════════════════════════

    def _check_ronda(self, key, header_n, x_col, y_col, r_exp, pts=15):
        self._header(f"EJERCICIO {header_n} — Construye y Calcula 🗺️", icon="🗺️", pts=pts)
        checks = []
        df = _get("df_felicidad")
        x_val = _get(f"x_{key}")
        y_val = _get(f"y_{key}")
        r_val = _get(f"r_{key}")

        if x_val is None:
            checks.append((False, f"x_{key}", f"No definida — usa '{x_col}' en el eje X"))
        elif _col_match(x_val, x_col, df):
            checks.append((True, f"x_{key} == '{x_col}'", "✓"))
        else:
            checks.append((False, f"x_{key}", f"Debe ser '{x_col}', obtuve '{x_val}'"))

        if y_val is None:
            checks.append((False, f"y_{key}", f"No definida — usa '{y_col}' en el eje Y"))
        elif _col_match(y_val, y_col, df):
            checks.append((True, f"y_{key} == '{y_col}'", "✓"))
        else:
            checks.append((False, f"y_{key}", f"Debe ser '{y_col}', obtuve '{y_val}'"))

        if r_val is None:
            checks.append((False, f"r_{key}",
                           f"No definida — usa df_felicidad['{x_col}'].corr(df_felicidad['{y_col}'])"))
        elif not _is_number(r_val):
            checks.append((False, f"r_{key}", f"Debe ser número, recibí {type(r_val).__name__}"))
        elif _approx(r_val, r_exp, tol=0.01):
            checks.append((True, f"r_{key} ≈ {r_exp:.3f}", "✓"))
        else:
            checks.append((False, f"r_{key}", f"Debe ser ≈{r_exp:.3f}, obtuve {r_val}"))

        return self._award(key, checks, pts)

    def check_ex5(self):
        """Ex5 — Ronda 3: PBI per cápita vs. Esperanza de vida saludable (15 pts)"""
        return self._check_ronda("ex5", 5, _COL_PBI, _COL_ESPERANZA, 0.8354621150416076)

    def check_ex6(self):
        """Ex6 — Ronda 4: Apoyo social vs. Esperanza de vida saludable (15 pts)"""
        return self._check_ronda("ex6", 6, _COL_APOYO, _COL_ESPERANZA, 0.7190094590308561)

    def check_ex7(self):
        """Ex7 — Ronda 5: Libertad para tomar decisiones vs. Percepción de corrupción (15 pts)"""
        return self._check_ronda("ex7", 7, _COL_LIBERTAD, _COL_CORRUPCION, 0.4388433064150672)

    def check_ex8(self):
        """Ex8 — Ronda 6: PBI per cápita vs. Generosidad (15 pts)"""
        return self._check_ronda("ex8", 8, _COL_PBI, _COL_GENEROSIDAD, -0.07966231348976406)

    def check_ex9(self):
        """Ex9 — Explora todas las correlaciones con Puntaje (15 pts) — antes ex5"""
        self._header("EJERCICIO 9 — Explora Todas las Correlaciones 🧭", icon="🧭", pts=15)
        checks = []
        df = _get("df_felicidad")
        correlaciones_puntaje = _get("correlaciones_puntaje")
        columna_mas_fuerte = _get("columna_mas_fuerte")
        columna_mas_debil = _get("columna_mas_debil")

        expected_norm = {_norm(c) for c in _SEIS_COLUMNAS}

        if correlaciones_puntaje is None:
            checks.append((False, "correlaciones_puntaje",
                           "No definida — usa df_felicidad.corr(numeric_only=True)['Puntaje'], sin 'Puesto' ni 'Puntaje'"))
        else:
            try:
                if _is_series(correlaciones_puntaje):
                    idx_norm = {_norm(str(i)) for i in correlaciones_puntaje.index}
                elif isinstance(correlaciones_puntaje, dict):
                    idx_norm = {_norm(str(i)) for i in correlaciones_puntaje.keys()}
                else:
                    idx_norm = None
            except Exception:
                idx_norm = None

            if idx_norm is None:
                checks.append((False, "correlaciones_puntaje",
                               f"Debe ser una Serie o dict de r por columna, recibí {type(correlaciones_puntaje).__name__}"))
            elif _norm(_COL_PUESTO) in idx_norm:
                checks.append((False, "correlaciones_puntaje",
                               "Incluye 'Puesto' -- excluyelo, su correlación es circular (se calcula a partir de Puntaje)"))
            elif _norm(_COL_PUNTAJE) in idx_norm:
                checks.append((False, "correlaciones_puntaje",
                               "Incluye 'Puntaje' -- excluyelo, su correlación consigo mismo siempre es 1"))
            elif idx_norm == expected_norm:
                checks.append((True, "correlaciones_puntaje — 6 columnas correctas",
                               "✓  Sin 'Puesto' ni 'Puntaje'"))
            else:
                checks.append((False, "correlaciones_puntaje",
                               "Debe tener exactamente las 6 variables económicas/sociales, sin 'Puesto' ni 'Puntaje'"))

        if columna_mas_fuerte is None:
            checks.append((False, "columna_mas_fuerte", "No definida"))
        elif _col_match(columna_mas_fuerte, _COL_PBI, df):
            checks.append((True, "columna_mas_fuerte == 'PBI per cápita'", "✓  r ≈ 0.79, la más fuerte"))
        else:
            checks.append((False, "columna_mas_fuerte",
                           f"Debe ser 'PBI per cápita' (r ≈ 0.79), obtuve '{columna_mas_fuerte}'"))

        if columna_mas_debil is None:
            checks.append((False, "columna_mas_debil", "No definida"))
        elif _col_match(columna_mas_debil, _COL_GENEROSIDAD, df):
            checks.append((True, "columna_mas_debil == 'Generosidad'", "✓  r ≈ 0.08, la más débil"))
        else:
            checks.append((False, "columna_mas_debil",
                           f"Debe ser 'Generosidad' (r ≈ 0.08), obtuve '{columna_mas_debil}'"))

        return self._award("ex9", checks, 15)

    def check_debug1(self):
        """Debug1 — nombre de columna mal escrito: Punaje -> Puntaje (10 pts)"""
        self._header("🔧 DEBUG 1 — Corrige el Error de Columna", icon="🔧", pts=10)
        checks = []
        r_pbi = _get("r_pbi")
        EXP = 0.7938828678781273

        if r_pbi is None:
            checks.append((False, "r_pbi", "No definida — corrige el nombre de columna a 'Puntaje'"))
        elif not _is_number(r_pbi):
            checks.append((False, "r_pbi", f"Debe ser número, recibí {type(r_pbi).__name__}"))
        elif _approx(r_pbi, EXP, tol=0.01):
            checks.append((True, f"r_pbi ≈ {EXP:.3f}",
                           "✓  KeyError corregido — 'Puntaje' es el nombre real de la columna"))
        else:
            checks.append((False, "r_pbi",
                           f"Debe ser ≈{EXP:.3f}, obtuve {r_pbi}. Revisa el nombre exacto de la columna"))

        return self._award("debug1", checks, 10)

    # ═══════════════════════════════════════════════════════════
    # CHECKPOINT — Sección B (fin de la Semana 3, Clase 1)
    # ═══════════════════════════════════════════════════════════

    def check_mini_b(self):
        """Checkpoint — Sección B (fin de la Semana 3, Clase 1)"""
        self._checkpoints.add("mini_b")
        if len(self._checkpoints) >= 2 and self._unlock("medalla_camino"):
            display(HTML(
                '<div style="font-family:\'Press Start 2P\',monospace;font-size:8px;'
                'color:#ffb703;background:#1a1400;border:1px solid #ffb703;'
                'border-radius:3px;padding:12px 16px;max-width:840px;margin:6px 0;">'
                '🌻 LOGRO: Medalla del Camino — Ambos checkpoints superados</div>'
            ))
        seccion = {
            "t6": ("T6 — El límite de .corr()", 5),
            "ex3": ("Ejercicio 3 – r real de corrupción", 12),
            "ex4": ("Ejercicio 4 – r real de esperanza de vida", 12),
            "t7": ("T7 — Ronda 3, antes de calcular", 5),
            "ex5": ("Ejercicio 5 – PBI per cápita vs. Esperanza de vida", 15),
            "t8": ("T8 — Ronda 3, interpreta tu resultado", 5),
            "t9": ("T9 — Ronda 4, antes de calcular", 5),
            "ex6": ("Ejercicio 6 – Apoyo social vs. Esperanza de vida", 15),
            "t10": ("T10 — Ronda 4, interpreta tu resultado", 5),
            "t11": ("T11 — Ronda 5, antes de calcular", 5),
            "ex7": ("Ejercicio 7 – Libertad vs. Percepción de corrupción", 15),
            "t12": ("T12 — Ronda 5, interpreta tu resultado", 5),
            "t13": ("T13 — Ronda 6, antes de calcular", 5),
            "ex8": ("Ejercicio 8 – PBI per cápita vs. Generosidad", 15),
            "t14": ("T14 — Ronda 6, interpreta tu resultado", 5),
            "ex9": ("Ejercicio 9 – Explora todas las correlaciones", 15),
            "debug1": ("Debug 1 – Corrige el error de columna", 10),
        }
        self._render_checkpoint("CHECKPOINT — CASI AMANECE", seccion, "#ff9e2c")

    # ═══════════════════════════════════════════════════════════
    # RESUMEN FINAL
    # ═══════════════════════════════════════════════════════════

    def resumen(self):
        _, _, pct         = self._totals()
        n                 = self._nombre()
        lvl_num, lvl_name = _level_info(pct)
        core_earned       = sum(e for e, _ in self._scores.values())

        if pct >= 96:
            final_msg = f"🏆 EN LA CIMA DEL BIENESTAR. {n.upper()}, tu nombre entra al Salón de la Fama de la Semana 3."
        elif pct >= 81:
            final_msg = f"☀️ CASI AMANECE. {n}, el bienestar ya se ve claro. La Semana 4 te espera."
        elif pct >= 61:
            final_msg = f"🧭 EXPLORADOR DE PATRONES. {n}, tu ojo ya confía en el número. ¡Sigue así!"
        elif pct >= 41:
            final_msg = f"🌻 FLORECIENDO CON LOS DATOS. {n}, los patrones empiezan a aparecer. Revisa los ✖ para avanzar."
        elif pct >= 21:
            final_msg = f"🌤️ PRIMEROS RAYOS DE SOL. {n}, toda búsqueda empieza así. Relee la teoría y vuelve a intentar."
        else:
            final_msg = f"🌱 {n}, tu búsqueda de patrones acaba de empezar. Cada celda ejecutada es un paso hacia adelante."

        ach_display = {
            "primer_rayo":          "☀️ Primer Rayo de Sol",
            "ojo_entrenado":        "👁️ Ojo Entrenado",
            "numero_exacto":        "🔢 Número Exacto",
            "cartografo_patrones":  "🗺️ Cartógrafo de Patrones",
            "explorador_completo":  "🧭 Explorador Completo",
            "depurador_feliz":      "🔧 Depurador Feliz",
            "medalla_camino":       "🌻 Medalla del Camino",
            "racha_bienestar":      "🔥 Racha de Bienestar",
            "felicidad_plena":      "🏆 Felicidad Plena",
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
  @keyframes pk-glow{{0%,100%{{text-shadow:0 0 14px rgba(255,209,102,.8),2px 2px 0 #7a5c00}}
    50%{{text-shadow:0 0 32px rgba(255,209,102,1),0 0 60px rgba(255,158,44,.5),2px 2px 0 #7a5c00}}}}
  @keyframes pk-xp{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
</style>
<div style="background:#12100a;border:2px solid #ffd166;border-radius:6px;max-width:840px;
  margin:12px 0;overflow:hidden;
  box-shadow:0 0 40px rgba(255,209,102,.15),0 0 80px rgba(255,158,44,.08),0 10px 40px rgba(0,0,0,.8);">

  <div style="background:linear-gradient(135deg,#12100a,#1e1406,#12100a);
    border-bottom:2px solid #ffd166;padding:22px 28px;text-align:center;position:relative;">
    <div style="position:absolute;left:20px;top:50%;transform:translateY(-50%);">{self._logo_tag}</div>
    <div style="font-family:'Press Start 2P',monospace;font-size:clamp(13px,2.8vw,20px);
      color:#ffd166;animation:pk-glow 2.5s ease-in-out infinite;letter-spacing:3px;
      margin-bottom:8px;">☀️ MISIÓN 2: BUSCANDO PATRONES 🧭</div>
    <div style="font-family:'Press Start 2P',monospace;font-size:8px;color:#ff9e2c;
      letter-spacing:2px;">SEMANA 3 — RESUMEN FINAL</div>
    <div style="position:absolute;right:20px;top:50%;transform:translateY(-50%);">{self._logo_tag}</div>
  </div>

  <div style="padding:24px 28px;">
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:20px;">
      <div style="background:#0d0b06;border:1px solid #26241a;border-radius:3px;
        padding:16px;text-align:center;">
        <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#6a6656;
          letter-spacing:1px;margin-bottom:10px;">XP TOTAL</div>
        <div style="font-family:'Press Start 2P',monospace;font-size:clamp(14px,3vw,22px);
          color:#ffd166;">{core_earned}/{_CORE_MAX}</div>
      </div>
      <div style="background:#0d0b06;border:1px solid #26241a;border-radius:3px;
        padding:16px;text-align:center;">
        <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#6a6656;
          letter-spacing:1px;margin-bottom:10px;">NIVEL</div>
        <div style="font-family:'Press Start 2P',monospace;font-size:clamp(8px,1.5vw,12px);
          color:{lv_color};">{lvl_name}</div>
      </div>
      <div style="background:#0d0b06;border:1px solid #26241a;border-radius:3px;
        padding:16px;text-align:center;">
        <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#6a6656;
          letter-spacing:1px;margin-bottom:10px;">SCORE</div>
        <div style="font-family:'Press Start 2P',monospace;font-size:clamp(14px,3vw,22px);
          color:#4caf50;">{pct}%</div>
      </div>
    </div>

    <div style="margin-bottom:20px;">
      <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
        <span style="font-family:'Press Start 2P',monospace;font-size:7px;color:#6a6656;">
          PROGRESO</span>
        <span style="font-family:'Press Start 2P',monospace;font-size:7px;color:{lv_color};">
          {pct}%</span>
      </div>
      <div style="width:100%;height:14px;background:#1c1810;border:1px solid #26241a;
        border-radius:3px;overflow:hidden;">
        <div style="width:{pct}%;height:100%;background:{xp_grad};
          border-radius:3px;transform-origin:left;
          animation:pk-xp 1.4s cubic-bezier(.4,0,.2,1) forwards;
          box-shadow:0 0 8px rgba(255,209,102,.4);"></div>
      </div>
    </div>

    <div style="background:#0d0b06;border:1px solid #4aa8d8;border-radius:3px;
      padding:14px 18px;margin-bottom:20px;text-align:center;">
      <div style="font-size:13px;color:#f0ece0;line-height:1.7;">{final_msg}</div>
    </div>

    {f"""
    <div style="margin-bottom:16px;">
      <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#6a6656;
        letter-spacing:1px;margin-bottom:10px;">☀️ LOGROS DESBLOQUEADOS</div>
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
      color:#4aa8d8;letter-spacing:1px;opacity:.9;">
      📊 Calificación final enviada al leaderboard · {n} · {lvl_name}
    </div>"""}
  </div>
</div>'''))

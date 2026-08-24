"""
Autograder — Bimestre 3, Mision 2: Buscando Patrones — SEMANA 4
EN BUSCA DE LA FELICIDAD EDITION — World Happiness Report 2019

ATLAS build 2026-08-20/21, contra ATLAS_spec_nb3_nb4.md (SOFIA). Companion de
autograder_nb3.py -- continua su numeracion global (ex5-8, t8-10, debug1,
intex1) porque narrativamente sigue siendo Mision 2, aunque el archivo ya no
comparta nb-prefijo con nb3_correlacion.ipynb (rename explicito del usuario
2026-08-20). Este archivo no tiene predecesor -- Seccion C y el
Mini-Proyecto nunca habian sido construidos antes de esta reestructuracion
(ver WORKFORCE_HANDOFF.md Done log 2026-08-20).

Cubre: check_t8-t10, check_ex5-ex8, check_debug1, check_intex1,
check_mini_b, check_mini_c, check_reflexion_ronda6/subgrupos/
interpretacion/metodologica, resumen()
Dataset: 2019_es.csv (156 filas x 10 columnas, World Happiness Report) --
mismo archivo que nb3, vuelto a descargar en esta sesion de Colab (el estado
de nb3 no persiste entre notebooks).

Notas de scoring:
  t8-t10 (Ronda 5 antes de calcular, Ronda 6 interpreta, trampa de Oceanía
  n=2 en Sección C) valen 5 pts c/u = 15.
  ex5/ex6 (Rondas 5-6, grafica+calcula fusionados, 20 pts c/u tal como
  aparece impreso en el markdown -- no negociable aqui) = 40.
  debug1 vale 10. ex7 (explora todas las correlaciones con Puntaje) vale 20.
  ex8 (Sección C -- Generosidad vs. Puntaje, filtrado por continente) vale 20.
  intex1 (Mini-Proyecto de integración -- el estudiante elige su propio par,
  con hipótesis obligatoria) vale 25, más que un ex1-8 normal porque combina
  scatter + `.corr()` + elección propia + hipótesis en un solo ejercicio.
  4 celdas 💭 Reflexiona (ronda6, subgrupos, interpretacion, metodologica)
  valen 5 pts c/u = 20, calificadas por IA (ver autograder_nb3.py para el
  mecanismo completo -- idéntico aquí).
  _CORE_MAX = 15 (t8-10) + 40 (ex5-6) + 10 (debug1) + 20 (ex7) + 20 (ex8)
            + 20 (reflexion x4) + 25 (intex1) = 150.
  Sin bonus/reto -- este notebook no declara check_retoN.

Nota tecnica -- Sección C sin `.groupby().apply(lambda...)`: ver
build_nb4.py y WORKFORCE_HANDOFF.md para el razonamiento completo. El
ejercicio pide filtrado booleano (`df[df['Continente']=='Europa']`) +
`.corr()` sobre el subconjunto, no `.groupby().apply()` -- fuera del
temario comprometido (WORKFORCE_CONTRACT.md §5).

Nota Supabase: mismo proyecto/tabla `submissions` que nb1/nb3, campo
"curso"="STAT_2026", "notebook"="nb4". Deadline: 7 septiembre 2026, 11:59 PM
Peru -- una semana después del cierre de nb3, mismo intervalo semanal que
nb1_semana1 -> nb1_semana2 -> nb3 -> nb4.
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
NOTEBOOK_ID       = "nb4"

# ─── Deadline: 7 septiembre 2026, 11:59 PM Peru (UTC-5) = 8 sept 04:59 UTC ───
_DEADLINE_UTC   = _dt.datetime(2026, 9, 7, 4, 59, 0, tzinfo=_dt.timezone.utc)
DEADLINE_PASSED = _dt.datetime.now(_dt.timezone.utc) >= _DEADLINE_UTC

# ─── Scoring ─────────────────────────────────────────────────
_CORE_MAX = 150   # 15 (t8-10) + 40 (ex5-6) + 10 (debug1) + 20 (ex7) + 20 (ex8)
                  # + 20 (reflexion x4) + 25 (intex1)

# ─── Reflexion (calificada por IA vía Supabase Edge Function) ─
_REFLEXION_PTS       = 5
GRADE_REFLEXION_URL  = f"{SUPABASE_URL}/functions/v1/grade-reflexion"

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


# Nombres reales de columna (con tildes) usados por el dataset.
_COL_PUNTAJE      = "Puntaje"
_COL_PUESTO       = "Puesto"
_COL_PBI          = "PBI per cápita"
_COL_APOYO        = "Apoyo social"
_COL_ESPERANZA    = "Esperanza de vida saludable"
_COL_LIBERTAD     = "Libertad para tomar decisiones"
_COL_GENEROSIDAD  = "Generosidad"
_COL_CORRUPCION   = "Percepción de corrupción"

_SEIS_COLUMNAS      = [_COL_PBI, _COL_APOYO, _COL_ESPERANZA, _COL_LIBERTAD, _COL_GENEROSIDAD, _COL_CORRUPCION]
_TODAS_COLUMNAS_MINI = _SEIS_COLUMNAS + [_COL_PUNTAJE]

# Pares ya trabajados en Semana 3 / Semana 4 antes del Mini-Proyecto -- el
# estudiante debe elegir un par NUEVO (ver Teoria_Semanas3-4_Mision2_Correlacion.md
# §2 Sección D, requisito de GAUSS contra el riesgo de correlación espuria).
_USED_PAIRS = [
    frozenset([_norm(_COL_CORRUPCION), _norm(_COL_PUNTAJE)]),
    frozenset([_norm(_COL_ESPERANZA), _norm(_COL_PUNTAJE)]),
    frozenset([_norm(_COL_APOYO), _norm(_COL_PUNTAJE)]),
    frozenset([_norm(_COL_LIBERTAD), _norm(_COL_PUNTAJE)]),
    frozenset([_norm(_COL_GENEROSIDAD), _norm(_COL_PUNTAJE)]),
    frozenset([_norm(_COL_PBI), _norm(_COL_PUNTAJE)]),
    frozenset([_norm(_COL_PBI), _norm(_COL_ESPERANZA)]),
    frozenset([_norm(_COL_APOYO), _norm(_COL_ESPERANZA)]),
    frozenset([_norm(_COL_LIBERTAD), _norm(_COL_CORRUPCION)]),
    frozenset([_norm(_COL_PBI), _norm(_COL_GENEROSIDAD)]),
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
                        self._achievements = set(_best.get("achievements") or [])
                        self._streak       = int(_best.get("streak") or 0)
                        self._prev_level   = int(_best.get("level_num") or 0)
                except Exception:
                    pass

                if _best:
                    _score_html = f'''
  <div style="background:#12100a;border:1px solid #4aa8d8;border-radius:3px;
    padding:12px 20px;margin-top:6px;
    font-family:'Press Start 2P',monospace;animation:ag-fadein .4s ease .1s both;">
    <div style="font-size:6px;color:#4aa8d8;letter-spacing:2px;margin-bottom:10px;">
      ☀️ TU MEJOR MARCA — SEMANA 4</div>
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
    ☀️ &nbsp;¡BIENVENIDO DE VUELTA, BUSCADOR {nombre.upper()}! &nbsp;·&nbsp; {grado}
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
      2px 2px 0 #7a5c00;animation:ag-start .6s ease;margin-bottom:14px;">¡CONTINÚA TU MISIÓN!</div>
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
            _out.register_callback('_ag_reflexion_answer', self._grade_reflexion)

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
        letter-spacing:2px;margin-top:8px;">SEMANA 4 — EN BUSCA DE LA FELICIDAD</div>
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
    <button class="ag-btn" onclick="agRegister()">☀️ &nbsp; ¡CONTINUAR LA BÚSQUEDA! &nbsp; 🧭</button>
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
                             '☀️ MISIÓN 2 — SEMANA 4 — Registro</div>'))
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

        # Primer Rayo de Sol — primer XP ganado (por si el estudiante entra
        # directo a nb4 sin haber pasado por nb3 en esta sesion de Colab)
        if any(e > 0 for e, _ in self._scores.values()) and self._unlock("primer_rayo"):
            unlocked.append(("☀️ Primer Rayo de Sol — ¡Tu primer punto de felicidad conquistado!", "#ff9e2c", "Chispa"))

        # Cartografo de Patrones — ex5,ex6,ex7,ex8 perfectos
        ex_todos = ["ex5", "ex6", "ex7", "ex8"]
        if (all(k in self._scores and self._scores[k][0] == self._scores[k][1] for k in ex_todos)
                and self._unlock("cartografo_patrones")):
            unlocked.append(("🗺️ Cartógrafo de Patrones — Todas tus rondas de Semana 4, perfectas", "#4aa8d8", "Rayo"))

        # Explorador Completo — ex7 (explora todo) perfecto
        if (self._scores.get("ex7", (0, 1))[0] == self._scores.get("ex7", (0, 1))[1]
                and "ex7" in self._scores and self._unlock("explorador_completo")):
            unlocked.append(("🧭 Explorador Completo — Recorriste las seis variables del bienestar", "#ffb703", "Amanecer"))

        # Depurador Feliz — debug1 perfecto
        if (self._scores.get("debug1", (0, 1))[0] == self._scores.get("debug1", (0, 1))[1]
                and "debug1" in self._scores and self._unlock("depurador_feliz")):
            unlocked.append(("🔧 Depurador Feliz — Encontraste el error sin perder la calma", "#ffb703", "Amanecer"))

        # Descubridor — intex1 (mini-proyecto) perfecto
        if (self._scores.get("intex1", (0, 1))[0] == self._scores.get("intex1", (0, 1))[1]
                and "intex1" in self._scores and self._unlock("descubridor")):
            unlocked.append(("🔍 Descubridor — Encontraste tu propio patrón, con hipótesis y todo", "#ff9e2c", "Sol Pleno"))

        # Medalla del Camino — ambos checkpoints de Semana 4 alcanzados
        if len(self._checkpoints) >= 2 and self._unlock("medalla_camino"):
            unlocked.append(("🌻 Medalla del Camino — Ambos checkpoints de Semana 4 superados", "#ffb703", "Amanecer"))

        # Racha de Bienestar — racha >= 5
        if self._streak >= 5 and self._unlock("racha_bienestar"):
            unlocked.append(("🔥 Racha de Bienestar — Combo x5", "#4aa8d8", "Rayo"))

        # Felicidad Plena — 100% del core
        if pct >= 100 and self._unlock("felicidad_plena"):
            unlocked.append(("🏆 Felicidad Plena — 100% de la Semana 4", "#ff9e2c", "Sol Pleno"))

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
            f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:16px;">'
            f'{self._logo_tag_sm}'
            f'<span style="font-family:\'Press Start 2P\',monospace;font-size:9px;'
            f'color:{color};letter-spacing:2px;">🌻 {title}</span></div>'
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
                    f'<div style="display:flex;align-items:center;gap:8px;'
                    f'font-family:\'Press Start 2P\',monospace;font-size:8px;'
                    f'color:#4caf50;background:#020d02;border:1px solid #4caf50;'
                    f'border-radius:3px;padding:10px 16px;max-width:840px;margin-top:6px;">'
                    f'{self._logo_tag_sm}'
                    f'<span>✅ SCORE ENVIADO — {self._nombre_real} · DNI {self._dni}'
                    f'<br><span style="color:#4aa8d8;font-size:7px;">'
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
    # TEORÍA — check_t8 .. check_t10 (formulario interactivo HTML)
    # ═══════════════════════════════════════════════════════════

    _TEORIA = {
        8: dict(
            title="T8 — Ronda 5, antes de calcular",
            q=("`Libertad para tomar decisiones` y `Percepción de corrupción` son dos "
               "variables distintas, aunque ambas describen algo sobre las instituciones "
               "de un país. Antes de calcular su r: ¿por qué NO deberías asumir que van a "
               "tener una relación tan fuerte como la de `PBI per cápita` vs. `Esperanza de "
               "vida saludable` (r≈0.84) que calculaste la clase pasada?"),
            opts={"a": "Porque medir instituciones nunca produce correlaciones fuertes",
                  "b": "Porque cada par de variables tiene su propia relación real -- que dos variables 'suenen' relacionadas con lo mismo no fija qué tan fuerte es su r, hay que calcularlo",
                  "c": "Porque Libertad y Corrupción son en realidad la misma variable con otro nombre",
                  "d": "Porque .corr() no funciona bien con variables de percepción"},
            correct="b",
            why=("Cada par de columnas tiene su propia relación real, calculada directamente "
                 "-- que dos variables compartan un tema (aquí, instituciones) no predice qué "
                 "tan fuerte va a ser su r."),
            pts=5,
        ),
        9: dict(
            title="T9 — Ronda 6, interpreta tu resultado",
            q=("Calculaste r ≈ -0.08 entre `PBI per cápita` y `Generosidad`. ¿Cuál es la "
               "lectura correcta de un r tan cercano a 0?"),
            opts={"a": "Confirma que no existe ninguna relación posible entre el dinero y la generosidad, bajo ninguna medida",
                  "b": "Con estos datos y esta medida lineal, no se detecta una relación consistente -- no es lo mismo que 'nunca hay relación bajo ninguna circunstancia'",
                  "c": "El cálculo salió mal -- dos variables económicas siempre deberían correlacionar",
                  "d": "Un r negativo siempre significa que hay un error en los datos"},
            correct="b",
            why=("`.corr()` solo mide relación lineal en este dataset -- un r cercano a 0 "
                 "dice 'no detecté esta relación aquí, así', no 'esta relación no existe en "
                 "ningún sentido'."),
            pts=5,
        ),
        10: dict(
            title="T10 — La trampa de Oceanía",
            q=("Si filtras `df_felicidad` para quedarte solo con los países de Oceanía, vas "
               "a tener apenas 2 filas. Cualquier par de columnas que calcules ahí va a dar "
               "un r cercano a ±1.0. ¿Por qué NO deberías confiar en ese número como un "
               "hallazgo real?"),
            opts={"a": "Porque Oceanía nunca debería estar en un dataset de felicidad",
                  "b": "Con solo 2 puntos, una línea recta siempre pasa exactamente por ambos -- el r perfecto es un artefacto del tamaño de muestra, no evidencia de una relación fuerte",
                  "c": "Porque el signo del r está mal calculado con muestras chicas",
                  "d": "Porque .corr() no acepta menos de 3 filas y debería devolver un error"},
            correct="b",
            why=("Muy pocos datos producen correlaciones aparentemente perfectas casi por "
                 "definición geométrica -- esto no tiene nada que ver con causalidad (eso es "
                 "la Semana 5), es un problema distinto de tamaño de muestra."),
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
            f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">'
            f'{self._logo_tag_sm}'
            f'<span style="font-family:\'Press Start 2P\',monospace;font-size:9px;'
            f'color:#a8a08a;letter-spacing:1px;">'
            f'🔒 {spec["title"]} — YA RESPONDIDA</span></div>'
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
  <div style="background:#4aa8d818;border-bottom:1px solid #4aa8d840;padding:10px 16px;
    display:flex;align-items:center;gap:8px;">
    {self._logo_tag_sm}
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

    def check_t8(self): return self._ask_teoria(8)
    def check_t9(self): return self._ask_teoria(9)
    def check_t10(self): return self._ask_teoria(10)

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
        terminar. 55s deja margen sobre ese peor caso."""
        try:
            import json as _json, urllib.request as _ur
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
            f'<div style="max-width:840px;margin:10px 0;background:#12100a;'
            f'border:2px solid {color};border-radius:4px;padding:14px 18px;'
            f'font-family:\'Segoe UI\',Roboto,sans-serif;">'
            f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">'
            f'{self._logo_tag_sm}'
            f'<span style="font-family:\'Press Start 2P\',monospace;font-size:9px;'
            f'color:#a8a08a;letter-spacing:1px;">'
            f'🔒 💭 REFLEXIONA — YA RESPONDIDA</span></div>'
            f'<div style="color:{color};font-size:13px;">'
            f'Ya enviaste tu reflexión ({pts}/{max_pts} pts)</div>'
            f'<div style="color:#a8a08a;font-size:12px;margin-top:6px;">'
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
                '<div style="max-width:840px;margin:10px 0;background:#12100a;'
                'border:2px solid #ffb703;border-radius:4px;padding:14px 18px;'
                'font-family:\'Segoe UI\',Roboto,sans-serif;">'
                '<div style="font-family:\'Press Start 2P\',monospace;font-size:9px;'
                'color:#ffb703;letter-spacing:1px;margin-bottom:8px;">'
                '⏳ NO SE PUDO CALIFICAR</div>'
                '<div style="color:#f0ece0;font-size:13px;">'
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
<div id="{uid}-wrap" style="background:#12100a;border:2px solid #4aa8d8;border-radius:4px;
  max-width:840px;margin:10px 0;overflow:hidden;box-shadow:0 6px 24px rgba(0,0,0,.7);">
  <div style="background:#4aa8d818;border-bottom:1px solid #4aa8d840;padding:10px 16px;
    display:flex;align-items:center;gap:8px;">
    {self._logo_tag_sm}
    <span style="font-family:'Press Start 2P',monospace;font-size:9px;color:#4aa8d8;
      letter-spacing:1px;">💭 REFLEXIONA</span>
  </div>
  <div style="padding:16px 18px;">
    <div style="color:#f0ece0;font-size:13px;line-height:1.6;margin-bottom:14px;">{question}</div>
    <textarea id="{uid}-text" rows="3" placeholder="Escribe tu reflexión aquí..."
      style="width:100%;box-sizing:border-box;background:#171307;border:2px solid #4aa8d8;
      border-radius:4px;color:#f0ece0;font-family:'Segoe UI',Roboto,sans-serif;
      font-size:13px;padding:10px 12px;resize:vertical;"></textarea>
    <button id="{uid}-btn" onclick="{uid}_submit()"
      style="margin-top:10px;padding:10px 20px;background:#4aa8d8;border:none;
      border-radius:4px;color:#0d0b06;font-family:'Press Start 2P',monospace;
      font-size:9px;cursor:pointer;">ENVIAR ✉️</button>
    <div id="{uid}-status" style="margin-top:10px;font-size:12px;color:#a8a08a;"></div>
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

        if pts == max_pts:
            s_icon, s_text, s_color = "💭", f"¡REFLEXIÓN COMPLETA! +{pts} XP", "#4caf50"
            border_color, glow = "#4caf50", "0 0 22px rgba(76,175,80,.15)"
        elif pts > 0:
            s_icon, s_text, s_color = "💭", f"+{pts} XP  ·  {max_pts - pts} por profundizar", "#ffd166"
            border_color, glow = "#ffb703", "0 0 22px rgba(255,183,3,.12)"
        else:
            s_icon, s_text, s_color = "💭", "Sin XP esta vez — lee el comentario abajo", "#ff5d5d"
            border_color, glow = "#ff5d5d", "0 0 22px rgba(255,93,93,.15)"

        xp_grad = _XP_GRAD.get(lvl_num, _XP_GRAD[1])
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

        comment_html = (
            f'<div style="padding:10px 12px;margin:2px 0 8px;background:rgba(74,168,216,.06);'
            f'border-left:3px solid #4aa8d8;border-radius:0 3px 3px 0;">'
            f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;color:#4aa8d8;">'
            f'🤖 FEEDBACK</span>'
            f'<div style="color:#f0ece0;font-size:12px;line-height:1.6;margin-top:5px;">{comment}</div>'
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
      {self._logo_tag_sm}
      <span style="font-family:'Press Start 2P',monospace;font-size:9px;
        color:{border_color};letter-spacing:1px;">💭 REFLEXIÓN CALIFICADA</span>
    </div>
    <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#ff9e2c;
      background:rgba(255,158,44,.1);border:1px solid rgba(255,158,44,.4);
      padding:3px 8px;border-radius:2px;">MAX {max_pts} XP</div>
  </div>
  <div style="padding:10px 14px 6px;">{comment_html}</div>
  <div style="background:#0d0b06;border-top:1px solid #1a1710;padding:11px 14px;">
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

    def check_reflexion_ronda6(self):
        return self._ask_reflexion("ronda6",
            '"PBI per cápita" y "Generosidad" dan un r muy cercano a 0. ¿Te '
            'parece razonable que el dinero de un pais casi no prediga que '
            'tan generosa es su gente? ¿Por que si o por que no?')

    def check_reflexion_subgrupos(self):
        return self._ask_reflexion("subgrupos",
            'El r general de "Generosidad" vs. "Puntaje" era casi 0. Pero '
            'acabas de ver que dentro de Europa es positivo, y dentro de '
            'América es negativo. En 2-3 oraciones: ¿que te dice esto sobre '
            'confiar en "el patron general" de todo un dataset sin mirar '
            'los subgrupos?')

    def check_reflexion_interpretacion(self):
        return self._ask_reflexion("interpretacion",
            'Mira el resultado que imprimiste arriba (tus dos variables y '
            'tu r). Sin usar la palabra "causa" ni ninguna variante: ¿que te '
            'dice ese r sobre la relacion entre tus dos variables? ¿Y que es '
            'lo que NO te dice?')

    def check_reflexion_metodologica(self):
        return self._ask_reflexion("metodologica",
            'Miraste una matriz con muchisimos pares posibles y elegiste '
            'uno. Si hubieras probado 20 pares al azar, es esperable que '
            'alguno salga con un r alto solo por casualidad. En 2-3 '
            'oraciones: ¿por que no deberias confiar automaticamente en "el '
            'par con el r mas alto que encontre" solo porque salio alto?')

    # ═══════════════════════════════════════════════════════════
    # RONDAS 5-6 — continuación del patrón grafica+calcula
    # ═══════════════════════════════════════════════════════════

    def _check_ronda(self, key, header_n, x_col, y_col, r_exp, pts=20):
        self._header(f"EJERCICIO {header_n} — Grafica y Calcula 🗺️", icon="🗺️", pts=pts)
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
        """Ex5 — Ronda 5: Libertad para tomar decisiones vs. Percepción de corrupción (20 pts)"""
        return self._check_ronda("ex5", 5, _COL_LIBERTAD, _COL_CORRUPCION, 0.4388433064150672)

    def check_ex6(self):
        """Ex6 — Ronda 6: PBI per cápita vs. Generosidad (20 pts)"""
        return self._check_ronda("ex6", 6, _COL_PBI, _COL_GENEROSIDAD, -0.07966231348976406)

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

    def check_ex7(self):
        """Ex7 — Explora todas las correlaciones con Puntaje (20 pts)"""
        self._header("EJERCICIO 7 — Explora Todas las Correlaciones 🧭", icon="🧭", pts=20)
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

        return self._award("ex7", checks, 20)

    # ═══════════════════════════════════════════════════════════
    # CHECKPOINT — mitad de Semana 4
    # ═══════════════════════════════════════════════════════════

    def check_mini_b(self):
        """Checkpoint — mitad de Semana 4 (antes de Sección C)"""
        self._checkpoints.add("mini_b")
        seccion = {
            "t8": ("T8 — Ronda 5, antes de calcular", 5),
            "ex5": ("Ejercicio 5 – Libertad vs. Percepción de corrupción", 20),
            "ex6": ("Ejercicio 6 – PBI per cápita vs. Generosidad", 20),
            "t9": ("T9 — Ronda 6, interpreta tu resultado", 5),
            "debug1": ("Debug 1 – Corrige el error de columna", 10),
            "ex7": ("Ejercicio 7 – Explora todas las correlaciones", 20),
        }
        self._render_checkpoint("CHECKPOINT — MITAD DE SEMANA 4", seccion, "#4aa8d8")

    # ═══════════════════════════════════════════════════════════
    # SECCIÓN C — Por Subgrupos (filtrado booleano + .corr())
    # ═══════════════════════════════════════════════════════════

    def check_ex8(self):
        """Ex8 — Sección C: Generosidad vs. Puntaje, por continente (20 pts)"""
        self._header("EJERCICIO 8 — Un Par Casi Nulo, por Continente 🌎", icon="🌎", pts=20)
        checks = []
        r_eu = _get("r_generosidad_europa")
        r_am = _get("r_generosidad_america")
        EXP_EU = 0.530102
        EXP_AM = -0.210721

        if r_eu is None:
            checks.append((False, "r_generosidad_europa",
                           "No definida — filtra df_felicidad['Continente']=='Europa' y calcula .corr() sobre ese subconjunto"))
        elif not _is_number(r_eu):
            checks.append((False, "r_generosidad_europa", f"Debe ser número, recibí {type(r_eu).__name__}"))
        elif _approx(r_eu, EXP_EU, tol=0.01):
            checks.append((True, f"r_generosidad_europa ≈ {EXP_EU:.3f}", "✓  Positivo dentro de Europa"))
        else:
            checks.append((False, "r_generosidad_europa", f"Debe ser ≈{EXP_EU:.3f}, obtuve {r_eu}"))

        if r_am is None:
            checks.append((False, "r_generosidad_america",
                           "No definida — filtra df_felicidad['Continente']=='América' y calcula .corr() sobre ese subconjunto"))
        elif not _is_number(r_am):
            checks.append((False, "r_generosidad_america", f"Debe ser número, recibí {type(r_am).__name__}"))
        elif _approx(r_am, EXP_AM, tol=0.01):
            checks.append((True, f"r_generosidad_america ≈ {EXP_AM:.3f}", "✓  Negativo dentro de América"))
        else:
            checks.append((False, "r_generosidad_america", f"Debe ser ≈{EXP_AM:.3f}, obtuve {r_am}"))

        return self._award("ex8", checks, 20)

    # ═══════════════════════════════════════════════════════════
    # MINI-PROYECTO — Integración 1 (elección propia + hipótesis)
    # ═══════════════════════════════════════════════════════════

    def check_intex1(self):
        """Integración 1 — Mini-Proyecto: hallazgo propio del estudiante (25 pts)"""
        self._header("INTEGRACIÓN 1 — Tu Propio Hallazgo 🔍", icon="🔍", pts=25)
        checks = []
        df = _get("df_felicidad")
        mini_var_x = _get("mini_var_x")
        mini_var_y = _get("mini_var_y")
        mini_r = _get("mini_r")
        mini_hipotesis = _get("mini_hipotesis")

        valid_norms = {_norm(c) for c in _TODAS_COLUMNAS_MINI}
        x_norm = _norm(mini_var_x) if isinstance(mini_var_x, str) else None
        y_norm = _norm(mini_var_y) if isinstance(mini_var_y, str) else None

        pair_ok = False
        if mini_var_x is None or mini_var_y is None:
            checks.append((False, "mini_var_x / mini_var_y",
                           "No definidas — elige dos columnas de la matriz de arriba"))
        elif (isinstance(mini_var_x, str) and _norm(mini_var_x) == _norm(_COL_PUESTO)) or \
             (isinstance(mini_var_y, str) and _norm(mini_var_y) == _norm(_COL_PUESTO)):
            checks.append((False, "mini_var_x / mini_var_y",
                           "'Puesto' no vale -- su correlación con Puntaje es circular, no un hallazgo"))
        elif x_norm not in valid_norms or y_norm not in valid_norms:
            checks.append((False, "mini_var_x / mini_var_y",
                           f"Deben ser columnas reales del dataset, obtuve '{mini_var_x}' / '{mini_var_y}'"))
        elif x_norm == y_norm:
            checks.append((False, "mini_var_x / mini_var_y", "Debes elegir DOS columnas distintas"))
        elif frozenset([x_norm, y_norm]) in _USED_PAIRS:
            checks.append((False, "mini_var_x / mini_var_y",
                           "Este par ya se trabajó en una ronda anterior de Semana 3/4 -- elige un par que no hayas usado todavía"))
        else:
            checks.append((True, "mini_var_x / mini_var_y — par nuevo y válido", "✓"))
            pair_ok = True

        if pair_ok and df is not None:
            col_x_real = next(c for c in _TODAS_COLUMNAS_MINI if _norm(c) == x_norm)
            col_y_real = next(c for c in _TODAS_COLUMNAS_MINI if _norm(c) == y_norm)
            r_real = df[col_x_real].corr(df[col_y_real])
            if mini_r is None:
                checks.append((False, "mini_r", "No definida"))
            elif not _is_number(mini_r):
                checks.append((False, "mini_r", f"Debe ser número, recibí {type(mini_r).__name__}"))
            elif _approx(mini_r, r_real, tol=0.01):
                checks.append((True, f"mini_r ≈ {r_real:.3f}", "✓  Coincide con tu propio par"))
            else:
                checks.append((False, "mini_r", f"Debe ser ≈{r_real:.3f} (el r real de tu par), obtuve {mini_r}"))
        else:
            checks.append((False, "mini_r", "No se pudo validar -- corrige mini_var_x/mini_var_y primero"))

        if _is_nontrivial_text(mini_hipotesis):
            checks.append((True, "mini_hipotesis", "✓  Hipótesis registrada"))
        else:
            checks.append((False, "mini_hipotesis",
                           "Escribe una hipótesis real (no dejes '___') de por qué crees que estas dos variables podrían estar relacionadas"))

        return self._award("intex1", checks, 25)

    # ═══════════════════════════════════════════════════════════
    # CHECKPOINT — fin de la Semana 4 / Misión 2
    # ═══════════════════════════════════════════════════════════

    def check_mini_c(self):
        """Checkpoint — fin de la Semana 4 y de la Misión 2"""
        self._checkpoints.add("mini_c")
        if len(self._checkpoints) >= 2 and self._unlock("medalla_camino"):
            display(HTML(
                f'<div style="display:flex;align-items:center;gap:8px;'
                f'font-family:\'Press Start 2P\',monospace;font-size:8px;'
                f'color:#ffb703;background:#1a1400;border:1px solid #ffb703;'
                f'border-radius:3px;padding:12px 16px;max-width:840px;margin:6px 0;">'
                f'{self._logo_tag_sm}'
                f'<span>🌻 LOGRO: Medalla del Camino — Ambos checkpoints de Semana 4 superados</span></div>'
            ))
        seccion = {
            "t10": ("T10 — La trampa de Oceanía", 5),
            "ex8": ("Ejercicio 8 – Generosidad por continente", 20),
            "intex1": ("Integración 1 – Tu propio hallazgo", 25),
        }
        self._render_checkpoint("CHECKPOINT — FIN DE LA MISIÓN 2", seccion, "#ff9e2c")

    # ═══════════════════════════════════════════════════════════
    # RESUMEN FINAL
    # ═══════════════════════════════════════════════════════════

    def resumen(self):
        _, _, pct         = self._totals()
        n                 = self._nombre()
        lvl_num, lvl_name = _level_info(pct)
        core_earned       = sum(e for e, _ in self._scores.values())

        if pct >= 96:
            final_msg = f"🏆 EN LA CIMA DEL BIENESTAR. {n.upper()}, tu nombre entra al Salón de la Fama de la Misión 2."
        elif pct >= 81:
            final_msg = f"☀️ CASI AMANECE. {n}, encontraste tu propio patrón. La Semana 5 lo va a poner a prueba."
        elif pct >= 61:
            final_msg = f"🧭 EXPLORADOR DE PATRONES. {n}, ya sabes leer un patrón por subgrupo. ¡Sigue así!"
        elif pct >= 41:
            final_msg = f"🌻 FLORECIENDO CON LOS DATOS. {n}, los patrones empiezan a aparecer. Revisa los ✖ para avanzar."
        elif pct >= 21:
            final_msg = f"🌤️ PRIMEROS RAYOS DE SOL. {n}, toda búsqueda empieza así. Relee la teoría y vuelve a intentar."
        else:
            final_msg = f"🌱 {n}, tu búsqueda de patrones continúa. Cada celda ejecutada es un paso hacia adelante."

        ach_display = {
            "primer_rayo":         "☀️ Primer Rayo de Sol",
            "cartografo_patrones": "🗺️ Cartógrafo de Patrones",
            "explorador_completo": "🧭 Explorador Completo",
            "depurador_feliz":     "🔧 Depurador Feliz",
            "descubridor":         "🔍 Descubridor",
            "medalla_camino":      "🌻 Medalla del Camino",
            "racha_bienestar":     "🔥 Racha de Bienestar",
            "felicidad_plena":     "🏆 Felicidad Plena",
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
      letter-spacing:2px;">SEMANA 4 — RESUMEN FINAL</div>
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

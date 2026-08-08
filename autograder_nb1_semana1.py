"""
Autograder — Bimestre 3, Mision 1: Recuperacion de Datos — SEMANA 1
POKEBALL EDITION — Conviertete en Campeon de la Liga de Datos

Cubre: check_ex1-ex5, check_debug1, check_t1-t9, check_mini_a, check_mini_b, resumen()
Dataset: vgsales_es.csv (16598 filas x 11 columnas)

Companion file: autograder_nb1_semana2.py (ex6-11, debug2-5, t10-12, mini_c/d,
intex1-2, reto1) — mismo tema, distinto notebook (WORKFORCE_HANDOFF.md ticket #10).

Notas de scoring (ATLAS, ticket #11 — WORKFORCE_HANDOFF.md):
  Los puntos de cada check_exN/check_debugN son los que YA aparecen impresos en el
  markdown del notebook (ej. "Ejercicio 1 ... (8 pts)") — no son negociables aqui,
  cambiar el numero rompería la consistencia notebook<->autograder. Eso solo (56 pts)
  ya se acercaba al presupuesto de ~150 para las DOS semanas combinadas antes de
  precificar ninguna pregunta de teoria. Resolucion: se sube el techo en vez de
  cortar contenido (ticket #11 lo preveía como "la decision correcta"). Las 9
  preguntas de teoria de esta semana (t1-t3, t9, t4-t8) valen 5 pts cada una (45 pts),
  para un _CORE_MAX = 101. La Semana 2 declara su propio _CORE_MAX por separado.

Nota Supabase (usuario, 2026-08-05, actualizado 2026-08-07): mismo proyecto/tabla
`submissions` que NB2/NB3, pero se agrega el campo nuevo "curso" al payload para
distinguir este modulo (Bimestre 3 — Estadistica en Python) de los notebooks del
modulo anterior (nb1/nb2/nb3 de Bimestre 2, que comparten la misma tabla). Valor
enviado: "STAT_2026" (las filas de CS quedan en "CS_2026" via DEFAULT + backfill
en `supabase_schema.sql`). Requiere haber corrido la migracion de `curso` en
`supabase_schema.sql` contra la base de datos en Supabase antes del primer envio
real — no es algo que este script pueda crear por si solo.
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

# ─── Supabase Config (mismo proyecto que NB2/NB3) ─────────────
SUPABASE_URL      = "https://uwykikwutjtkpffwmdiq.supabase.co"
SUPABASE_ANON_KEY = "sb_publishable_aBG6GD4wn9CgpSE-47fagQ_sNhnzznu"
LOGO_URL          = "https://raw.githubusercontent.com/Santa-Maria-de-los-Andes/CS1---Grader/main/icono%20SMA.png"
CURSO_ID          = "STAT_2026"
NOTEBOOK_ID       = "nb1_semana1"

# ─── Deadline: 16 agosto 2026, 11:59 PM Peru (UTC-5) = 17 agosto 04:59 UTC ───
_DEADLINE_UTC   = _dt.datetime(2026, 8, 17, 4, 59, 0, tzinfo=_dt.timezone.utc)
DEADLINE_PASSED = _dt.datetime.now(_dt.timezone.utc) >= _DEADLINE_UTC

# ─── Scoring ─────────────────────────────────────────────────
_CORE_MAX = 101   # 56 (ex1-5 + debug1, valores fijos en el markdown) + 45 (9 teoria x 5)

# ─── Niveles Pokemon (por % del score core) ───────────────────
_LEVELS = [
    (96, 6, "👑 Campeon de la Liga Pokemon"),
    (81, 5, "🌟 Elite Four en Ascenso"),
    (61, 4, "🎖️ Ganador de Medalla de Gimnasio"),
    (41, 3, "🔵 Viajero con Pokedex Activa"),
    (21, 2, "⚡ Entrenador de Ruta 1"),
    (0,  1, "🥚 Novato de Pueblo Paleta"),
]

_XP_GRAD = {
    1: "linear-gradient(90deg,#333344,#666688)",
    2: "linear-gradient(90deg,#7a5c00,#ffcb05)",
    3: "linear-gradient(90deg,#1a3a6a,#5a8dee)",
    4: "linear-gradient(90deg,#1a4a1a,#4caf50)",
    5: "linear-gradient(90deg,#4a1a5a,#c04adf)",
    6: "linear-gradient(90deg,#ee1515,#ffcb05,#5a8dee)",
}
_LV_CSS_COLOR = {1: "#8888aa", 2: "#ffcb05", 3: "#5a8dee", 4: "#4caf50", 5: "#c04adf", 6: "#ffcb05"}


def _level_info(pct):
    for thresh, num, name in _LEVELS:
        if pct >= thresh:
            return num, name
    return 1, "🥚 Novato de Pueblo Paleta"


def _lv_color(n):
    return _LV_CSS_COLOR.get(n, "#8888aa")


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
                    'color:#ffcb05;letter-spacing:2px;">SMA</span>')

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
  <div style="background:#0d0d1a;border:1px solid #3c5aa6;border-radius:3px;
    padding:12px 20px;margin-top:6px;
    font-family:'Press Start 2P',monospace;animation:ag-fadein .4s ease .1s both;">
    <div style="font-size:6px;color:#5a8dee;letter-spacing:2px;margin-bottom:10px;">
      🔴 TU MEJOR MARCA — SEMANA 1</div>
    <div style="display:flex;align-items:center;gap:20px;">
      <div style="font-size:28px;color:#ffcb05;
        text-shadow:0 0 16px rgba(255,203,5,.8),2px 2px 0 #7a5c00;">
        {_best['pct']}%</div>
      <div>
        <div style="font-size:8px;color:#ee1515;letter-spacing:1px;">{_best['level_name']}</div>
        <div style="font-size:6px;color:#8888bb;margin-top:6px;letter-spacing:1px;">
          {_best['earned']} / {_best['possible']} XP</div>
      </div>
    </div>
  </div>'''
                else:
                    _score_html = (
                        '<div style="background:#0d0d1a;border:1px solid #22223a;border-radius:3px;'
                        'padding:10px 20px;margin-top:6px;'
                        'font-family:\'Press Start 2P\',monospace;font-size:6px;color:#555566;'
                        'letter-spacing:1px;animation:ag-fadein .4s ease .1s both;">'
                        '🔴 Primera captura — ¡aun no tienes marca registrada!</div>'
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
  <div style="background:#12060a;border:1px solid #ee1515;border-radius:3px;padding:12px 18px;
    font-family:'Press Start 2P',monospace;font-size:8px;
    color:#ee1515;letter-spacing:1px;animation:ag-fadein .4s ease;">
    🔴 &nbsp;¡BIENVENIDO, ENTRENADOR {nombre.upper()}! &nbsp;·&nbsp; {grado}
  </div>
  {_score_html}
  <div id="ag-loading" style="background:#0d0d1a;border:1px solid #22223a;border-radius:3px;
    padding:22px 18px;margin-top:6px;text-align:center;animation:ag-fadein .5s ease .2s both;">
    <div style="display:flex;justify-content:center;gap:6px;margin-bottom:12px;">
      <div style="width:8px;height:8px;border-radius:50%;background:#ee1515;
        animation:ag-dot 1.2s ease-in-out 0s infinite;"></div>
      <div style="width:8px;height:8px;border-radius:50%;background:#ee1515;
        animation:ag-dot 1.2s ease-in-out .2s infinite;"></div>
      <div style="width:8px;height:8px;border-radius:50%;background:#ee1515;
        animation:ag-dot 1.2s ease-in-out .4s infinite;"></div>
    </div>
    <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#555566;letter-spacing:2px;">
      CARGANDO POKÉDEX…
    </div>
  </div>
  <div id="ag-start" style="display:none;background:linear-gradient(160deg,#0d0d1a,#1a0d1e);
    border:2px solid #ee1515;border-radius:4px;padding:36px 24px;margin-top:6px;text-align:center;
    box-shadow:0 0 40px rgba(238,21,21,.25),0 0 80px rgba(255,203,5,.06),0 6px 24px rgba(0,0,0,.9);">
    <div style="font-size:44px;margin-bottom:14px;animation:ag-start .55s cubic-bezier(.34,1.56,.64,1);">🔴</div>
    <div style="font-family:'Press Start 2P',monospace;font-size:clamp(15px,3.6vw,26px);color:#ffcb05;
      letter-spacing:4px;text-shadow:0 0 24px rgba(255,203,5,.95),0 0 50px rgba(238,21,21,.35),
      2px 2px 0 #7a5c00;animation:ag-start .6s ease;margin-bottom:14px;">¡TU AVENTURA COMIENZA!</div>
    <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#5a8dee;
      letter-spacing:2px;opacity:.85;margin-bottom:16px;">EJECUTA LA PRIMERA CELDA PARA COMENZAR</div>
    <div style="font-size:15px;color:#ee1515;opacity:.4;letter-spacing:8px;">⚪ 🔴 ⚪ 🔴 ⚪ 🔴 ⚪</div>
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
    width:100%;box-sizing:border-box;background:#0d0d1a;border:1px solid #22223a;
    border-radius:3px;padding:0 12px;color:#f0ece0;font-size:13px;height:42px;
    font-family:'Segoe UI',Roboto,sans-serif;outline:none;transition:border .2s;
  }}
  .ag-input:focus,.ag-select:focus {{ border-color:#5a8dee; }}
  .ag-select option {{ background:#0d0d1a; }}
  .ag-btn {{
    width:100%;padding:13px;background:linear-gradient(90deg,#9c0000,#ee1515);
    border:none;border-radius:3px;color:#ffcb05;font-family:'Press Start 2P',monospace;
    font-size:9px;letter-spacing:2px;cursor:pointer;transition:opacity .2s;margin-top:6px;
  }}
  .ag-btn:hover {{ opacity:.85; }}
  .ag-err {{ color:#ff5555;font-size:11px;margin-top:6px;display:none; }}
  .ag-label {{ font-family:'Press Start 2P',monospace;font-size:7px;letter-spacing:1px;
    margin-bottom:8px;display:flex;align-items:center;gap:5px; }}
  .ag-field {{ display:flex;flex-direction:column; }}
</style>
<div style="background:#0d0d1a;border:2px solid #3c5aa6;border-radius:4px;max-width:840px;
  margin:10px 0;overflow:hidden;box-shadow:0 0 40px rgba(60,90,166,.2),0 10px 30px rgba(0,0,0,.8);">

  <div style="background:linear-gradient(90deg,#0d0d1a,#1a0d1e,#0d0d1a);border-bottom:2px solid #ffcb05;
    padding:18px 24px;position:relative;display:flex;align-items:center;justify-content:center;min-height:80px;">
    <div style="position:absolute;left:20px;top:50%;transform:translateY(-50%);">{logo_tag}</div>
    <div style="text-align:center;">
      <div style="font-family:'Press Start 2P',monospace;font-size:clamp(13px,3vw,18px);color:#ffcb05;letter-spacing:3px;
        text-shadow:0 0 14px rgba(255,203,5,.7),2px 2px 0 #7a5c00;">🔴 MISIÓN 1: DATOS ⚪</div>
      <div style="font-family:'Press Start 2P',monospace;font-size:8px;color:#ee1515;
        letter-spacing:2px;margin-top:8px;">SEMANA 1 — MODO ENTRENADOR</div>
    </div>
    <div style="position:absolute;right:20px;top:50%;transform:translateY(-50%);">{logo_tag}</div>
  </div>

  <div style="padding:24px;">
    <div style="display:grid;grid-template-columns:2fr 1fr;gap:14px;margin-bottom:14px;align-items:end;">
      <div class="ag-field">
        <div class="ag-label" style="color:#ee1515;">🔴 NOMBRE COMPLETO</div>
        <input id="ag-nombre" class="ag-input" placeholder="Tu nombre y apellido" />
      </div>
      <div class="ag-field">
        <div class="ag-label" style="color:#ee1515;">🏫 GRADO</div>
        <select id="ag-grado" class="ag-select">
          <option value="">— Selecciona —</option>
          <option value="3ro">3ro</option>
          <option value="4to">4to</option>
          <option value="5to">5to</option>
        </select>
      </div>
    </div>
    <div class="ag-field" style="margin-bottom:14px;">
      <div class="ag-label" style="color:#ffcb05;">🪪 CÓDIGO DE ESTUDIANTE (DNI, Pasaporte, Carnet)</div>
      <input id="ag-dni" class="ag-input" placeholder="Ingresa tu código" />
    </div>
    <div id="ag-err" class="ag-err">⚠ Por favor completa todos los campos.</div>
    <button class="ag-btn" onclick="agRegister()">🔴 &nbsp; ¡COMENZAR AVENTURA! &nbsp; 🔴</button>
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
                display(HTML('<div style="font-family:monospace;padding:10px;background:#0d0d1a;'
                             'color:#ee1515;border:1px solid #3c5aa6;border-radius:3px;max-width:840px;">'
                             '🔴 MISIÓN 1 — SEMANA 1 — Registro</div>'))
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
        return '<span style="font-family:\'Press Start 2P\',monospace;font-size:11px;color:#ffcb05;">SMA</span>'

    @property
    def _logo_tag_sm(self):
        if LOGO_URL:
            return (f'<img src="{LOGO_URL}" style="height:24px;object-fit:contain;" '
                    f'onerror="this.style.display=\'none\'">')
        return '<span style="font-family:\'Press Start 2P\',monospace;font-size:8px;color:#ffcb05;">SMA</span>'

    def _nombre(self):
        if self._nombre_real:
            return self._nombre_real
        n = _get("nombre")
        if isinstance(n, str) and n.strip() and n.strip() not in ("?", ""):
            return n.strip()
        return "entrenador"

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

    def _header(self, title, icon="🔴", pts=None):
        self._curr_title = title
        self._curr_icon  = icon
        self._curr_pts   = pts

    def _check_achievements(self, key):
        unlocked = []
        earned, possible, pct = self._totals()

        # Primera Pokébola — primer XP ganado
        if any(e > 0 for e, _ in self._scores.values()) and self._unlock("primera_pokebola"):
            unlocked.append(("🔴 Primera Pokébola — ¡Tu primer dato atrapado!", "#ee1515", "Poké Ball"))

        # Insignia Bosque Verde — ex1-ex5 todos perfectos
        ex_keys = ["ex1", "ex2", "ex3", "ex4", "ex5"]
        if (all(k in self._scores and self._scores[k][0] == self._scores[k][1] for k in ex_keys)
                and self._unlock("insignia_bosque_verde")):
            unlocked.append(("🥇 Insignia Bosque Verde — Los 5 ejercicios perfectos", "#4caf50", "Ultra Ball"))

        # Escudo de Estática — debug1 perfecto
        if (self._scores.get("debug1", (0, 1))[0] == self._scores.get("debug1", (0, 1))[1]
                and "debug1" in self._scores and self._unlock("escudo_estatica")):
            unlocked.append(("🛡️ Escudo de Estática — Debug corregido sin errores", "#5a8dee", "Gran Ball"))

        # Medalla Pueblo Paleta — ambos checkpoints alcanzados
        if len(self._checkpoints) >= 2 and self._unlock("medalla_paleta"):
            unlocked.append(("🎖️ Medalla Pueblo Paleta — Ambos checkpoints superados", "#ffcb05", "Ultra Ball"))

        # Racha Charizard — racha >= 5
        if self._streak >= 5 and self._unlock("racha_charizard"):
            unlocked.append(("🔥 Racha Charizard — Combo x5", "#ee1515", "Gran Ball"))

        # Pokédex Completa — 100% del core
        if pct >= 100 and self._unlock("pokedex_completa"):
            unlocked.append(("👑 Pokédex Completa — 100% de la Semana 1", "#8e44ad", "Master Ball"))

        # Level-up
        lvl_num, lvl_name = _level_info(pct)
        if lvl_num > self._prev_level and self._prev_level > 0:
            unlocked.append((f"⬆️ ¡SUBISTE DE NIVEL! — {lvl_name}", "#5a8dee", "Nivel"))
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
                    f'margin-bottom:3px;background:rgba(238,21,21,.06);'
                    f'border-left:3px solid #ee1515;border-radius:0 3px 3px 0;">'
                    f'<span style="color:#ee1515;font-size:13px;flex-shrink:0;line-height:1.5;">✖</span>'
                    f'<div style="font-size:11px;line-height:1.5;">'
                    f'<span style="color:#ee1515;font-weight:bold;">{label}:</span> '
                    f'<span style="color:#cc8888;">{msg}</span></div></div>'
                )

        star_r = pts / max_pts if max_pts > 0 else 0
        gold, dark = "#ffcb05", "#2a2200"
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
            c_color = "#ee1515" if self._streak >= 5 else "#ffcb05"
            combo_html = (
                f'<div style="display:inline-flex;align-items:center;gap:5px;padding:3px 10px;'
                f'background:rgba(238,21,21,.12);border:1px solid {c_color};border-radius:2px;'
                f'margin-left:8px;">'
                f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;'
                f'color:{c_color};">🔥 COMBO x{self._streak}</span></div>'
            )

        if pts == max_pts:
            s_icon, s_text, s_color = "⚡", f"¡ATRAPADO! +{pts} XP", "#4caf50"
            border_color, glow = "#4caf50", "0 0 22px rgba(76,175,80,.15)"
        elif pts > 0:
            s_icon, s_text, s_color = "🎯", f"+{pts} XP  ·  {max_pts - pts} por ganar", "#ffcb05"
            border_color, glow = "#ffcb05", "0 0 22px rgba(255,203,5,.12)"
        else:
            s_icon, s_text, s_color = "💨", "¡SE ESCAPÓ! — Corrige los ✖ e intenta de nuevo", "#ee1515"
            border_color, glow = "#ee1515", "0 0 22px rgba(238,21,21,.15)"

        xp_grad = _XP_GRAD.get(lvl_num, _XP_GRAD[1])

        dots = "".join(
            f'<span style="display:inline-block;width:7px;height:7px;border-radius:50%;'
            f'background:{"#4caf50" if ok else "#ee1515"};margin:0 2px;'
            f'box-shadow:0 0 4px {"#4caf50" if ok else "#ee1515"};"></span>'
            for ok, _, _ in checks
        )

        new_ach     = self._check_achievements(key)
        reg_ach     = [(n, c, r) for n, c, r in new_ach if r != "Nivel"]
        levelup_ach = [(n, c, r) for n, c, r in new_ach if r == "Nivel"]

        _RC = {
            "Poké Ball":   ("#ee1515", "rgba(238,21,21,.12)",  "🔴"),
            "Gran Ball":   ("#5a8dee", "rgba(90,141,222,.12)", "🔵"),
            "Ultra Ball":  ("#ffcb05", "rgba(255,203,5,.10)",  "🟡"),
            "Master Ball": ("#8e44ad", "rgba(142,68,173,.15)", "🟣"),
        }
        ach_html = ""
        for ach_name, _, ach_rarity in reg_ach:
            bc, bg, ach_icon = _RC.get(ach_rarity, _RC["Poké Ball"])
            ach_html += (
                f'<div style="display:flex;align-items:center;gap:10px;margin-top:8px;'
                f'padding:10px 12px;background:{bg};border:1px solid {bc};border-radius:3px;">'
                f'<span style="font-size:18px;">{ach_icon}</span>'
                f'<div style="flex:1;">'
                f'<div style="margin-bottom:3px;">'
                f'<span style="background:{bc};color:#0d0d1a;font-size:7px;font-weight:bold;'
                f'padding:1px 5px;border-radius:2px;font-family:\'Press Start 2P\',monospace;">'
                f'{ach_rarity.upper()}</span>'
                f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;'
                f'color:{bc};margin-left:6px;">LOGRO DESBLOQUEADO</span>'
                f'</div>'
                f'<div style="color:#f0ece0;font-size:12px;font-weight:bold;">{ach_name}</div>'
                f'</div></div>'
            )

        curr_icon  = getattr(self, '_curr_icon', '🔴')
        curr_title = getattr(self, '_curr_title', 'EJERCICIO').upper()
        _logo_sm   = self._logo_tag_sm

        _core_pct_bar = min(round(earned / _CORE_MAX * 100), 100)
        xp_bar_html = (
            f'<div style="display:flex;justify-content:space-between;margin-bottom:4px;">'
            f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;color:#555566;">'
            f'XP: {earned}/{_CORE_MAX}</span>'
            f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;'
            f'color:{_lv_color(lvl_num)};">{lvl_name}</span></div>'
            f'<div style="width:100%;height:10px;background:#141428;border:1px solid #22223a;'
            f'border-radius:2px;overflow:hidden;">'
            f'<div style="width:{_core_pct_bar}%;height:100%;background:{xp_grad};'
            f'border-radius:2px;transform-origin:left;'
            f'animation:pg-xpscale 1.1s cubic-bezier(.4,0,.2,1) forwards;'
            f'box-shadow:0 0 6px rgba(255,203,5,.25);"></div></div>'
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
                             'font-size:6px;color:#5a8dee;letter-spacing:1px;opacity:.85;">'
                             '📊 Calificación actualizada en la base de datos</div>')

        card_html = f'''<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
  @keyframes pg-xpscale{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
</style>
<div style="background:#0d0d1a;border:2px solid {border_color};border-radius:4px;max-width:840px;
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
      <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#ee1515;
        background:rgba(238,21,21,.1);border:1px solid rgba(238,21,21,.4);
        padding:3px 8px;border-radius:2px;">MAX {max_pts} XP</div>
    </div>
  </div>
  <div style="padding:10px 14px 6px;">{rows_html}</div>
  <div style="background:#090914;border-top:1px solid #1a1a2e;padding:11px 14px;">
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

    # ── Level-up banner (Pokemon style) ──────────────────────

    def _render_levelup(self, lvl_num, lvl_name):
        import random as _r
        _r.seed(lvl_num * 97 + 31)
        uid = f"lu{_r.randint(10000, 99999)}"

        _cfg = {
            2: dict(bg="linear-gradient(160deg,#0d0d1a,#1a1400)",
                    c="#ffcb05", sc="#ffe066", rc="#ffcb05",
                    sub="ENTRENADOR DE RUTA 1 — TU AVENTURA COMIENZA", icon="⚡"),
            3: dict(bg="linear-gradient(160deg,#0a0d1a,#0d1a30)",
                    c="#5a8dee", sc="#8fb4ff", rc="#5a8dee",
                    sub="VIAJERO CON POKÉDEX ACTIVA — LOS DATOS SALVAJES APARECEN", icon="🔵"),
            4: dict(bg="linear-gradient(160deg,#0a1a0a,#0d2a10)",
                    c="#4caf50", sc="#8fe094", rc="#4caf50",
                    sub="MEDALLA DE GIMNASIO — PRIMER RETO SUPERADO", icon="🎖️"),
            5: dict(bg="linear-gradient(160deg,#150a1a,#2a0d30)",
                    c="#c04adf", sc="#e08fff", rc="#c04adf",
                    sub="ÉLITE FOUR EN ASCENSO — LOS LÍDERES TE RECONOCEN", icon="🌟"),
            6: dict(bg="linear-gradient(160deg,#0d0d1a,#1a0505,#0d0d1a)",
                    c="#ffcb05", sc="#5a8dee", rc="#ee1515",
                    sub="CAMPEÓN DE LA LIGA POKÉMON — SALÓN DE LA FAMA", icon="👑"),
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
                          f'margin:-50px;border-radius:50%;border:2px solid #5a8dee;opacity:0;'
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
    ⚪ 🔴 ⚪ 🔴 ⚪</div>
  <div style="position:absolute;right:14px;top:50%;
    font-size:15px;letter-spacing:5px;
    animation:{uid}-rr .9s ease-out .6s both;pointer-events:none;z-index:7;">
    ⚪ 🔴 ⚪ 🔴 ⚪</div>

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
                f'<div style="height:5px;background:#1a1a2e;border-radius:2px;overflow:hidden;">'
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
            f'<div style="background:#0d0d1a;border:2px solid {color};border-radius:4px;'
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
                "nombre":          self._nombre_real or "entrenador",
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
                    f'<br><span style="color:#5a8dee;font-size:7px;">'
                    f'📊 Calificación actualizada en la base de datos</span></div>'
                ))
        except Exception as _ex:
            if not silent:
                display(HTML(
                    f'<div style="font-family:\'Press Start 2P\',monospace;font-size:7px;'
                    f'color:#ee1515;background:#1a0005;border:1px solid #ee1515;'
                    f'border-radius:3px;padding:10px 16px;max-width:840px;margin-top:6px;">'
                    f'⚠️ Leaderboard no disponible: {_ex}</div>'
                ))

    # ═══════════════════════════════════════════════════════════
    # SECCIÓN A — Aterrizaje
    # ═══════════════════════════════════════════════════════════

    def check_ex1(self):
        """Ex1 — Radar Pokédex: num_filas / num_columnas de df_games (8 pts)"""
        self._header("EJERCICIO 1 — Radar Pokédex 📡", icon="🔴", pts=8)
        checks = []
        num_filas    = _get("num_filas")
        num_columnas = _get("num_columnas")
        EXP_FILAS, EXP_COLS = 16598, 11

        if num_filas is None:
            checks.append((False, "num_filas", "No definida — usa df_games.shape[0] o len(df_games)"))
        elif isinstance(num_filas, bool) or not isinstance(num_filas, int):
            checks.append((False, "num_filas", f"Debe ser int, recibí {type(num_filas).__name__}"))
        elif num_filas == EXP_FILAS:
            checks.append((True, f"num_filas == {EXP_FILAS}", "✓"))
        else:
            checks.append((False, "num_filas", f"Debe ser {EXP_FILAS}, obtuve {num_filas}"))

        if num_columnas is None:
            checks.append((False, "num_columnas", "No definida — usa df_games.shape[1]"))
        elif isinstance(num_columnas, bool) or not isinstance(num_columnas, int):
            checks.append((False, "num_columnas", f"Debe ser int, recibí {type(num_columnas).__name__}"))
        elif num_columnas == EXP_COLS:
            checks.append((True, f"num_columnas == {EXP_COLS}", "✓"))
        else:
            checks.append((False, "num_columnas", f"Debe ser {EXP_COLS}, obtuve {num_columnas}"))

        return self._award("ex1", checks, 8)

    def check_ex2(self):
        """Ex2 — Escaneo de datos: columna con más nulos (8 pts)"""
        self._header("EJERCICIO 2 — Escaneo de Datos ⚠️", icon="🔴", pts=8)
        checks = []
        col = _get("columna_con_mas_nulos")
        EXP = "anio"  # 16327 non-null vs Editor 16540 non-null (271 vs 58 faltantes)

        if col is None:
            checks.append((False, "columna_con_mas_nulos",
                           "No definida — mira el Non-Null Count más bajo en .info()"))
        elif not isinstance(col, str):
            checks.append((False, "columna_con_mas_nulos", f"Debe ser str, recibí {type(col).__name__}"))
        elif _norm(col) == EXP:
            checks.append((True, "columna_con_mas_nulos == 'Anio'",
                           "✓  Anio tiene 16327/16598 valores (271 faltantes) — más que Editor (58 faltantes)"))
        elif _norm(col) == "editor":
            checks.append((False, "columna_con_mas_nulos",
                           "Editor sí tiene nulos (58), pero Anio tiene más (271). Revisa .info() con cuidado"))
        else:
            checks.append((False, "columna_con_mas_nulos",
                           f"Debe ser 'Anio', obtuve '{col}'. Busca el Non-Null Count más bajo"))

        return self._award("ex2", checks, 8)

    def check_debug1(self):
        """Debug1 — nombre de columna mal escrito: Venta_Globales -> Ventas_Globales (10 pts)"""
        self._header("🔧 DEBUG 1 — Pokédex con Error de Escritura", icon="🔧", pts=10)
        checks = []
        promedio_ventas = _get("promedio_ventas")
        EXP = 0.5374406555006629

        if promedio_ventas is None:
            checks.append((False, "promedio_ventas",
                           "No definida — corrige el nombre de columna a 'Ventas_Globales'"))
        elif not _is_number(promedio_ventas):
            checks.append((False, "promedio_ventas", f"Debe ser número, recibí {type(promedio_ventas).__name__}"))
        elif _approx(promedio_ventas, EXP, tol=0.01):
            checks.append((True, f"promedio_ventas ≈ {EXP:.2f}",
                           "✓  KeyError corregido — 'Ventas_Globales' es el nombre real de la columna"))
        else:
            checks.append((False, "promedio_ventas",
                           f"Debe ser ≈{EXP:.2f}, obtuve {promedio_ventas}. Revisa el nombre exacto de la columna"))

        return self._award("debug1", checks, 10)

    # ═══════════════════════════════════════════════════════════
    # SECCIÓN B — Reconocimiento
    # ═══════════════════════════════════════════════════════════

    def check_ex3(self):
        """Ex3 — Media vs. mediana, otra vez (10 pts)"""
        self._header("EJERCICIO 3 — Doble Titular, Otra Vez 📰", icon="🔴", pts=10)
        checks = []
        media    = _get("media_ventas")
        mediana  = _get("mediana_ventas")
        EXP_MEDIA, EXP_MEDIANA = 0.5374406555006629, 0.17

        if media is None:
            checks.append((False, "media_ventas", "No definida"))
        elif not _is_number(media):
            checks.append((False, "media_ventas", f"Debe ser número, recibí {type(media).__name__}"))
        elif _approx(media, EXP_MEDIA, tol=0.01):
            checks.append((True, f"media_ventas ≈ {EXP_MEDIA:.2f}", "✓"))
        else:
            checks.append((False, "media_ventas", f"Debe ser ≈{EXP_MEDIA:.2f}, obtuve {media}"))

        if mediana is None:
            checks.append((False, "mediana_ventas", "No definida"))
        elif not _is_number(mediana):
            checks.append((False, "mediana_ventas", f"Debe ser número, recibí {type(mediana).__name__}"))
        elif _approx(mediana, EXP_MEDIANA, tol=0.01):
            checks.append((True, f"mediana_ventas == {EXP_MEDIANA}", "✓"))
        else:
            checks.append((False, "mediana_ventas", f"Debe ser {EXP_MEDIANA}, obtuve {mediana}"))

        return self._award("ex3", checks, 10)

    def check_ex4(self):
        """Ex4 — Ruta Norteamérica: media, mediana y desviación de Ventas_NA (10 pts)"""
        self._header("EJERCICIO 4 — Ruta Norteamérica 🗺️", icon="🔴", pts=10)
        checks = []
        media_na = _get("media_na")
        mediana_na = _get("mediana_na")
        desviacion_na = _get("desviacion_na")
        EXP_MEDIA, EXP_MEDIANA, EXP_DESV = 0.26466742981082064, 0.08, 0.8166830292988796

        for vname, val, exp, tol in [
            ("media_na", media_na, EXP_MEDIA, 0.01),
            ("mediana_na", mediana_na, EXP_MEDIANA, 0.01),
            ("desviacion_na", desviacion_na, EXP_DESV, 0.01),
        ]:
            if val is None:
                checks.append((False, vname, "No definida"))
            elif not _is_number(val):
                checks.append((False, vname, f"Debe ser número, recibí {type(val).__name__}"))
            elif _approx(val, exp, tol=tol):
                checks.append((True, f"{vname} ≈ {exp:.2f}", "✓"))
            else:
                checks.append((False, vname, f"Debe ser ≈{exp:.2f}, obtuve {val}"))

        return self._award("ex4", checks, 10)

    def check_ex5(self):
        """Ex5 — Atrapa al Atípico: umbral y juegos_atipicos (10 pts)"""
        self._header("EJERCICIO 5 — Atrapa al Atípico ⚡", icon="🔴", pts=10)
        checks = []
        umbral = _get("umbral")
        atipicos = _get("juegos_atipicos")
        EXP_UMBRAL = 2.0924685910705754
        EXP_N = 790

        if umbral is None:
            checks.append((False, "umbral", "No definida — umbral = media + desviacion_estandar"))
        elif not _is_number(umbral):
            checks.append((False, "umbral", f"Debe ser número, recibí {type(umbral).__name__}"))
        elif _approx(umbral, EXP_UMBRAL, tol=0.02):
            checks.append((True, f"umbral ≈ {EXP_UMBRAL:.2f}", "✓"))
        else:
            checks.append((False, "umbral",
                           f"Debe ser ≈{EXP_UMBRAL:.2f} (media + desviación estándar), obtuve {umbral}"))

        if atipicos is None:
            checks.append((False, "juegos_atipicos",
                           "No definida — juegos_atipicos = df_games[df_games['Ventas_Globales'] > umbral]"))
        elif pd is not None and not _is_dataframe(atipicos):
            checks.append((False, "juegos_atipicos",
                           f"Debe ser un DataFrame filtrado, recibí {type(atipicos).__name__}"))
        else:
            try:
                n = len(atipicos)
            except TypeError:
                n = -1
            if n == EXP_N:
                checks.append((True, f"len(juegos_atipicos) == {EXP_N}",
                               "✓  790 juegos 'legendarios' capturados"))
            else:
                checks.append((False, "juegos_atipicos",
                               f"Debe tener {EXP_N} filas, tiene {n}. ¿Usaste '>' (no '>=') con tu umbral?"))

        return self._award("ex5", checks, 10)

    # ═══════════════════════════════════════════════════════════
    # TEORÍA — check_t1 .. check_t9 (formulario interactivo HTML)
    # ═══════════════════════════════════════════════════════════

    _TEORIA = {
        1: dict(
            title="T1 — ¿Qué le falta a esa afirmación?",
            q=('Un periodista afirma "el colegio X es el mejor de la ciudad" citando solo el '
               'promedio de notas de sus 5 mejores alumnos. ¿Qué le falta a esa afirmación '
               'para ser un uso correcto de la estadística?'),
            opts={"a": "Nada, un promedio siempre es suficiente para comparar",
                  "b": "Considerar a todos los estudiantes, no solo una muestra elegida a conveniencia",
                  "c": "Usar una gráfica en vez de un número",
                  "d": "Cambiar el promedio por la moda"},
            correct="b",
            why=("La estadística exige mirar el conjunto de datos completo (o una muestra "
                 "representativa), no una selección que ya favorece la conclusión deseada."),
            pts=5,
        ),
        2: dict(
            title="T2 — ¿Qué rama de la estadística es?",
            q=('Un hospital usa el historial de pacientes de los últimos 5 años para '
               '<b>estimar</b> cuántas camas necesitará el próximo mes. ¿Qué rama de la '
               'estadística está usando principalmente?'),
            opts={"a": "Descriptiva", "b": "Predictiva", "c": "Prescriptiva",
                  "d": "Ninguna, esto no es estadística"},
            correct="b",
            why="Está proyectando un valor futuro a partir de patrones existentes — la definición exacta de predictiva.",
            pts=5,
        ),
        3: dict(
            title="T3 — Agrupar clientes, ¿qué rama es?",
            q=('Un programa agrupa a 500 clientes en 4 grupos según sus hábitos de compra '
               'similares. ¿Qué rama de la estadística describe mejor esto?'),
            opts={"a": "Predictiva, porque usa un algoritmo",
                  "b": "Descriptiva, porque organiza y resume lo que ya existe en los datos",
                  "c": "Prescriptiva, porque recomienda una acción",
                  "d": "No es estadística, es solo programación"},
            correct="b",
            why=("Agrupar (clustering) organiza patrones existentes; no proyecta un valor futuro. "
                 "Esto se repetirá en la Semana 7 con k-means — no es predictivo."),
            pts=5,
        ),
        4: dict(
            title="T4 — Sensibilidad de la media",
            q=('En un salón de 20 estudiantes, 19 ganan S/10 de propina por una encuesta y uno '
               'gana S/500 por un error de registro. ¿Qué le pasa a la media del grupo?'),
            opts={"a": "No cambia, la media ignora valores extremos",
                  "b": "Sube mucho, porque la media se ve arrastrada por valores extremos",
                  "c": "Baja mucho",
                  "d": "Se vuelve imposible de calcular"},
            correct="b",
            why="La media es la suma dividida entre la cantidad — un solo valor extremo la desplaza notablemente cuando el grupo es pequeño.",
            pts=5,
        ),
        5: dict(
            title="T5 — ¿Cuál medida usar?",
            q=("Usando el mismo salón del ejercicio anterior, ¿qué medida describe mejor "
               "'lo típico' de la propina que recibió la mayoría?"),
            opts={"a": "La media", "b": "La mediana",
                  "c": "Ambas son igual de buenas aquí", "d": "Ninguna aplica"},
            correct="b",
            why="La mediana no se mueve por el valor extremo — sigue reflejando el centro real de la mayoría de los datos (S/10).",
            pts=5,
        ),
        6: dict(
            title="T6 — ¿Cuándo usar la moda?",
            q=('Se tiene una lista con el deporte favorito de 200 estudiantes (fútbol, vóley, '
               'básquet, natación...). ¿Qué medida de tendencia central tiene sentido calcular aquí?'),
            opts={"a": "La media", "b": "La mediana", "c": "La moda", "d": "La desviación estándar"},
            correct="c",
            why="Son datos categóricos — no se puede 'sumar' fútbol + vóley, así que media y mediana no aplican. La moda (el valor más frecuente) sí.",
            pts=5,
        ),
        7: dict(
            title="T7 — Media y mediana muy distintas",
            q=("En un dataset de ingresos, la media es S/3,200 y la mediana es S/1,800. "
               "¿Qué es lo más razonable de concluir?"),
            opts={"a": "Uno de los dos cálculos está mal",
                  "b": "La distribución probablemente está sesgada — hay valores altos poco frecuentes que suben la media",
                  "c": "Los datos no sirven y hay que descartarlos",
                  "d": "Hay que usar solo la moda en vez de ambas"},
            correct="b",
            why="Es el mismo patrón del gancho de apertura de esta semana — ambos cálculos son correctos; la brecha entre ellos es información sobre la forma de la distribución, no un error.",
            pts=5,
        ),
        8: dict(
            title="T8 — ¿Qué mide la desviación estándar?",
            q="Si un dataset tiene una desviación estándar muy baja, ¿qué indica eso?",
            opts={"a": "Los datos están muy cerca del promedio, poco dispersos",
                  "b": "Los datos tienen muchos errores",
                  "c": "La media está mal calculada",
                  "d": "El dataset es muy grande"},
            correct="a",
            why="Desviación estándar = 'en promedio, qué tan lejos está cada dato del centro' — baja desviación significa poca dispersión, no un juicio sobre calidad de los datos.",
            pts=5,
        ),
        9: dict(
            title="T9 — Observaciones vs. variables",
            q=("En una tabla de datos de atletas olímpicos, cada fila representa un atleta y "
               "cada columna representa un dato sobre ese atleta (edad, altura, deporte...). "
               "¿Cómo se llama correctamente cada fila y cada columna?"),
            opts={"a": "Fila = variable, columna = observación",
                  "b": "Fila = observación, columna = variable",
                  "c": "Ambas son observaciones", "d": "Ambas son variables"},
            correct="b",
            why="Fila = un caso/observación, columna = una característica/variable medida sobre cada caso.",
            pts=5,
        ),
    }

    def _grade_teoria(self, n, letter):
        spec = self._TEORIA[int(n)]
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
        try:
            from google.colab import output as _out  # noqa: F401  (solo para confirmar entorno Colab)
            import random as _r
            uid = f"tq{n}_{_r.randint(10000, 99999)}"

            opts_html = ""
            for L in ("a", "b", "c", "d"):
                opts_html += (
                    f'<button id="{uid}-{L}" class="{uid}-opt" onclick="{uid}_pick(\'{L}\')" '
                    f'style="display:block;width:100%;text-align:left;padding:12px 16px;'
                    f'margin-bottom:8px;background:#12121f;border:2px solid #3c5aa6;'
                    f'border-radius:4px;color:#f0ece0;font-family:\'Segoe UI\',Roboto,sans-serif;'
                    f'font-size:13px;cursor:pointer;transition:all .15s;">'
                    f'<span style="font-family:\'Press Start 2P\',monospace;font-size:9px;'
                    f'color:#ffcb05;margin-right:10px;">{L.upper()}</span>{spec["opts"][L]}</button>'
                )

            display(HTML(f'''
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
  .{uid}-opt:hover {{ border-color:#ffcb05 !important; background:#1a1a2e !important; }}
</style>
<div id="{uid}-wrap" style="background:#0d0d1a;border:2px solid #3c5aa6;border-radius:4px;
  max-width:840px;margin:10px 0;overflow:hidden;box-shadow:0 6px 24px rgba(0,0,0,.7);">
  <div style="background:#3c5aa618;border-bottom:1px solid #3c5aa640;padding:10px 16px;">
    <span style="font-family:'Press Start 2P',monospace;font-size:9px;color:#5a8dee;
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
    chosen.style.borderColor = '#ffcb05';
    chosen.style.background = '#1a1a2e';
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

    # ═══════════════════════════════════════════════════════════
    # CHECKPOINTS
    # ═══════════════════════════════════════════════════════════

    def check_mini_a(self):
        """Checkpoint — Teoría Desbloqueada + Sección A"""
        self._checkpoints.add("mini_a")
        seccion = {
            "t1": ("T1 — Qué es la estadística", 5),
            "t2": ("T2 — Rama predictiva", 5),
            "t3": ("T3 — Rama descriptiva (clustering)", 5),
            "ex1": ("Ejercicio 1 – Radar Pokédex", 8),
            "ex2": ("Ejercicio 2 – Escaneo de Datos", 8),
            "t9": ("T9 — Observaciones vs. variables", 5),
        }
        self._render_checkpoint("CHECKPOINT — INSIGNIA PUEBLO PALETA", seccion, "#5a8dee")

    def check_mini_b(self):
        """Checkpoint — Sección B (fin de la Semana 1)"""
        self._checkpoints.add("mini_b")
        if len(self._checkpoints) >= 2 and self._unlock("medalla_paleta"):
            display(HTML(
                '<div style="font-family:\'Press Start 2P\',monospace;font-size:8px;'
                'color:#ffcb05;background:#1a1400;border:1px solid #ffcb05;'
                'border-radius:3px;padding:12px 16px;max-width:840px;margin:6px 0;">'
                '🎖️ LOGRO: Medalla Pueblo Paleta — Ambos checkpoints superados</div>'
            ))
        seccion = {
            "ex3": ("Ejercicio 3 – Doble Titular", 10),
            "t4": ("T4 — Sensibilidad de la media", 5),
            "t5": ("T5 — Cuál medida usar", 5),
            "t6": ("T6 — Cuándo usar la moda", 5),
            "t7": ("T7 — Media/mediana muy distintas", 5),
            "ex4": ("Ejercicio 4 – Ruta Norteamérica", 10),
            "ex5": ("Ejercicio 5 – Atrapa al Atípico", 10),
            "t8": ("T8 — Desviación estándar", 5),
            "debug1": ("Debug 1 – Pokédex con error", 10),
        }
        self._render_checkpoint("CHECKPOINT — INSIGNIA RUTA 1", seccion, "#ee1515")

    # ═══════════════════════════════════════════════════════════
    # RESUMEN FINAL
    # ═══════════════════════════════════════════════════════════

    def resumen(self):
        _, _, pct         = self._totals()
        n                 = self._nombre()
        lvl_num, lvl_name = _level_info(pct)
        core_earned       = sum(e for e, _ in self._scores.values())

        if pct >= 96:
            final_msg = f"👑 CAMPEÓN DE LA LIGA. {n.upper()}, tu nombre entra al Salón de la Fama de la Semana 1."
        elif pct >= 81:
            final_msg = f"🌟 ÉLITE FOUR. {n}, los líderes de gimnasio ya te reconocen. La Semana 2 te espera."
        elif pct >= 61:
            final_msg = f"🎖️ MEDALLA DE GIMNASIO. {n}, superaste tu primer reto de datos. ¡Sigue así!"
        elif pct >= 41:
            final_msg = f"🔵 VIAJERO CON POKÉDEX ACTIVA. {n}, tu Pokédex empieza a llenarse. Revisa los ✖ para avanzar."
        elif pct >= 21:
            final_msg = f"⚡ ENTRENADOR DE RUTA 1. {n}, cada entrenador empieza aquí. Relee la teoría y vuelve a intentar."
        else:
            final_msg = f"🥚 {n}, tu Pokédex acaba de nacer. Cada celda ejecutada es un paso en tu aventura."

        ach_display = {
            "primera_pokebola":     "🔴 Primera Pokébola",
            "insignia_bosque_verde":"🥇 Insignia Bosque Verde",
            "escudo_estatica":      "🛡️ Escudo de Estática",
            "medalla_paleta":       "🎖️ Medalla Pueblo Paleta",
            "racha_charizard":      "🔥 Racha Charizard",
            "pokedex_completa":     "👑 Pokédex Completa",
        }

        ach_html = ""
        if self._achievements:
            for ak, alabel in ach_display.items():
                if ak in self._achievements:
                    ach_html += (
                        f'<div style="display:inline-flex;align-items:center;gap:5px;'
                        f'padding:3px 8px;background:rgba(255,203,5,.08);'
                        f'border:1px solid #ffcb0540;border-radius:2px;margin:2px;">'
                        f'<span style="font-family:\'Press Start 2P\',monospace;font-size:6px;'
                        f'color:#ffcb05;">{alabel}</span></div>'
                    )

        lv_color = _lv_color(lvl_num)
        xp_grad  = _XP_GRAD.get(lvl_num, _XP_GRAD[1])

        self._submit_to_supabase(core_earned, _CORE_MAX, pct, lvl_num, lvl_name)

        display(HTML(f'''
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
  @keyframes pk-glow{{0%,100%{{text-shadow:0 0 14px rgba(255,203,5,.8),2px 2px 0 #7a5c00}}
    50%{{text-shadow:0 0 32px rgba(255,203,5,1),0 0 60px rgba(238,21,21,.5),2px 2px 0 #7a5c00}}}}
  @keyframes pk-xp{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
</style>
<div style="background:#0d0d1a;border:2px solid #ffcb05;border-radius:6px;max-width:840px;
  margin:12px 0;overflow:hidden;
  box-shadow:0 0 40px rgba(255,203,5,.15),0 0 80px rgba(238,21,21,.08),0 10px 40px rgba(0,0,0,.8);">

  <div style="background:linear-gradient(135deg,#0d0d1a,#1a0d1e,#0d0d1a);
    border-bottom:2px solid #ffcb05;padding:22px 28px;text-align:center;position:relative;">
    <div style="position:absolute;left:20px;top:50%;transform:translateY(-50%);">{self._logo_tag}</div>
    <div style="font-family:'Press Start 2P',monospace;font-size:clamp(13px,2.8vw,20px);
      color:#ffcb05;animation:pk-glow 2.5s ease-in-out infinite;letter-spacing:3px;
      margin-bottom:8px;">🔴 MISIÓN 1: DATOS ⚪</div>
    <div style="font-family:'Press Start 2P',monospace;font-size:8px;color:#ee1515;
      letter-spacing:2px;">SEMANA 1 — RESUMEN FINAL</div>
    <div style="position:absolute;right:20px;top:50%;transform:translateY(-50%);">{self._logo_tag}</div>
  </div>

  <div style="padding:24px 28px;">
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:20px;">
      <div style="background:#0a0a14;border:1px solid #22223a;border-radius:3px;
        padding:16px;text-align:center;">
        <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#555566;
          letter-spacing:1px;margin-bottom:10px;">XP TOTAL</div>
        <div style="font-family:'Press Start 2P',monospace;font-size:clamp(14px,3vw,22px);
          color:#ffcb05;">{core_earned}/{_CORE_MAX}</div>
      </div>
      <div style="background:#0a0a14;border:1px solid #22223a;border-radius:3px;
        padding:16px;text-align:center;">
        <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#555566;
          letter-spacing:1px;margin-bottom:10px;">NIVEL</div>
        <div style="font-family:'Press Start 2P',monospace;font-size:clamp(8px,1.5vw,12px);
          color:{lv_color};">{lvl_name}</div>
      </div>
      <div style="background:#0a0a14;border:1px solid #22223a;border-radius:3px;
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
      <div style="width:100%;height:14px;background:#141428;border:1px solid #22223a;
        border-radius:3px;overflow:hidden;">
        <div style="width:{pct}%;height:100%;background:{xp_grad};
          border-radius:3px;transform-origin:left;
          animation:pk-xp 1.4s cubic-bezier(.4,0,.2,1) forwards;
          box-shadow:0 0 8px rgba(255,203,5,.4);"></div>
      </div>
    </div>

    <div style="background:#0a0a14;border:1px solid #3c5aa6;border-radius:3px;
      padding:14px 18px;margin-bottom:20px;text-align:center;">
      <div style="font-size:13px;color:#f0ece0;line-height:1.7;">{final_msg}</div>
    </div>

    {f"""
    <div style="margin-bottom:16px;">
      <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#555566;
        letter-spacing:1px;margin-bottom:10px;">🔴 LOGROS DESBLOQUEADOS</div>
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
      color:#5a8dee;letter-spacing:1px;opacity:.9;">
      📊 Calificación final enviada al leaderboard · {n} · {lvl_name}
    </div>"""}
  </div>
</div>'''))

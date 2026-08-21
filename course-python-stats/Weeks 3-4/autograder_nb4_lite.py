"""
Autograder — Bimestre 3, Mision 2: Buscando Patrones — SEMANA 4
RUTA DE INTERPRETACION (accesibilidad / inclusion)

Companion de autograder_nb4.py, mismo patron que autograder_nb3_lite.py (ver
ese archivo para el razonamiento completo de por que subclasear en vez de
reescribir). Se reusan sin cambios: t8, t9, t10 (teoria), las 4 reflexiones
(ronda6, subgrupos, interpretacion, metodologica), el motor de gamificacion/
Supabase/DeepSeek completo.

Dos piezas se REDISEÑAN, no se copian tal cual, porque en el notebook con
codigo dependian de que el estudiante escribiera pandas:
  - Debug 1: en vez de pedir que el estudiante corrija `df_felicidad['Punaje']`
    -> `['Puntaje']`, el notebook de esta ruta presenta el error ya ejecutado
    (KeyError real, visible) y pregunta -- opcion multiple -- que tipo de
    error es y por que. Implementado como una entrada NUEVA (t11) en el mismo
    diccionario _TEORIA que ya usa el motor de preguntas de opcion multiple
    heredado, no como un mecanismo aparte.
  - Mini-Proyecto (check_intex1): el estudiante ya no escribe el codigo que
    calcula `mini_r` -- esa linea viene pre-escrita en la celda del notebook.
    Solo completa `mini_var_x`/`mini_var_y` (copiando nombres de columna de
    la matriz impresa) y `mini_hipotesis` (🧩 COMPLETA, no 🔨 CONSTRUYE). La
    validacion de par-valido/par-no-usado/Puesto-prohibido se reusa tal cual
    de autograder_nb4.py via sus helpers de modulo (_norm, _get, etc.);
    mini_r se sigue verificando contra el valor real como control de
    consistencia, no como algo que el estudiante debia calcular a mano.
  - check_ex5-8 y check_debug1 (version original) NO se definen aqui -- el
    notebook de esta ruta nunca los llama, ex5/ex6/ex7/ex8 se presentan como
    celdas 👀 OBSERVA ya resueltas.

Requiere autograder_nb4.py disponible en el runtime (wget'd junto a este
archivo en la celda de setup del notebook).

⚠️ Mismo mecanismo de reasignacion de globals que autograder_nb3_lite.py, y
la misma advertencia aplica: importar este archivo muta in-place el modulo
`autograder_nb4` ya cargado en `sys.modules` (ver el docstring de
autograder_nb3_lite.py para el detalle) -- validar cada archivo en su propio
subproceso, no con imports compartidos en un solo script.

Notas de scoring:
  t8, t9, t10 (idem autograder_nb4.py) = 15 pts.
  t11 (debug MC, nuevo) = 5 pts.
  4 reflexiones (ronda6, subgrupos, interpretacion, metodologica; idem) = 20 pts.
  intex1 rediseñado (par + hipotesis, sin escribir codigo) = 15 pts (baja de
  25 porque ya no incluye "escribiste tu propio codigo de .corr()").
  _CORE_MAX = 55 (15 + 5 + 20 + 15). Sin check_ex, sin bonus.
"""
from IPython.display import HTML, display

import autograder_nb4 as _base

_base.NOTEBOOK_ID = "nb4_lite"
_base._CORE_MAX   = 55   # 15 (t8-10) + 5 (t11 debug-mc) + 20 (4 reflexiones) + 15 (intex1 rediseñado)


class Autograder(_base.Autograder):
    """Misma teoria/reflexion que autograder_nb4.py -- sin check_ex5-8; debug1
    y el mini-proyecto rediseñados para no requerir escribir codigo."""

    _TEORIA = {**_base.Autograder._TEORIA, 11: dict(
        title="T11 — Lee el error antes de corregir",
        q=("El código de arriba intenta calcular la correlación entre `PBI per cápita` y "
           "`Puntaje`, pero falla con `KeyError: 'Punaje'`. ¿Qué te dice ese error?"),
        opts={
            "a": "Que la columna `Puntaje` no existe en el dataset -- hay que usar otra variable",
            "b": "Que el nombre de columna escrito en el código tiene un error de tipeo y no coincide con ninguna columna real",
            "c": "Que esa fila tiene un valor nulo en `Puntaje`",
            "d": "Que `.corr()` no se puede usar con la columna `Puntaje`",
        },
        correct="b",
        why=("Un `KeyError` significa que pandas buscó una columna con ese nombre EXACTO y no la "
             "encontró. Aquí el código escribió 'Punaje' (sin la 't') en vez de 'Puntaje' -- la "
             "columna real existe y no tiene nulos; el problema es el nombre escrito en el código, "
             "no el dato."),
        pts=5,
    )}

    # ═══════════════════════════════════════════════════════════
    # DEBUG 1 -- opcion multiple en vez de corregir codigo
    # ═══════════════════════════════════════════════════════════

    def check_debug1(self):
        return self._ask_teoria(11)

    # ═══════════════════════════════════════════════════════════
    # CHECKPOINTS -- sin ex5-8; intex1 con su nuevo puntaje
    # ═══════════════════════════════════════════════════════════

    def check_mini_b(self):
        """Checkpoint — mitad de Semana 4 (ruta de interpretacion, antes de Sección C)"""
        self._checkpoints.add("mini_b")
        seccion = {
            "t8":  ("T8 — Ronda 5, antes de calcular", 5),
            "t9":  ("T9 — Ronda 6, interpreta tu resultado", 5),
            "t11": ("Debug 1 — Identifica el error (opción múltiple)", 5),
        }
        self._render_checkpoint("CHECKPOINT — MITAD DE SEMANA 4", seccion, "#4aa8d8")

    def check_mini_c(self):
        """Checkpoint — fin de la Semana 4 y de la Misión 2 (ruta de interpretacion)"""
        self._checkpoints.add("mini_c")
        if len(self._checkpoints) >= 2 and self._unlock("medalla_camino"):
            display(HTML(
                '<div style="font-family:\'Press Start 2P\',monospace;font-size:8px;'
                'color:#ffb703;background:#1a1400;border:1px solid #ffb703;'
                'border-radius:3px;padding:12px 16px;max-width:840px;margin:6px 0;">'
                '🌻 LOGRO: Medalla del Camino — Ambos checkpoints de Semana 4 superados</div>'
            ))
        seccion = {
            "t10":    ("T10 — La trampa de Oceanía", 5),
            "intex1": ("Integración 1 – Tu propio hallazgo", 15),
        }
        self._render_checkpoint("CHECKPOINT — FIN DE LA MISIÓN 2", seccion, "#ff9e2c")

    # ═══════════════════════════════════════════════════════════
    # MINI-PROYECTO -- valida par + hipotesis; mini_r ya viene calculado
    # por una linea pre-escrita en la celda del notebook, no por el
    # estudiante -- aqui se revalida como control de consistencia.
    # ═══════════════════════════════════════════════════════════

    def check_intex1(self):
        self._header("INTEGRACIÓN 1 — Tu Propio Hallazgo 🔍", icon="🔍", pts=15)
        checks = []
        df             = _base._get("df_felicidad")
        mini_var_x     = _base._get("mini_var_x")
        mini_var_y     = _base._get("mini_var_y")
        mini_r         = _base._get("mini_r")
        mini_hipotesis = _base._get("mini_hipotesis")

        valid_norms = {_base._norm(c) for c in _base._TODAS_COLUMNAS_MINI}
        x_norm = _base._norm(mini_var_x) if isinstance(mini_var_x, str) else None
        y_norm = _base._norm(mini_var_y) if isinstance(mini_var_y, str) else None

        pair_ok = False
        if mini_var_x is None or mini_var_y is None:
            checks.append((False, "mini_var_x / mini_var_y",
                           "No definidas — elige dos columnas de la matriz de arriba"))
        elif (isinstance(mini_var_x, str) and _base._norm(mini_var_x) == _base._norm(_base._COL_PUESTO)) or \
             (isinstance(mini_var_y, str) and _base._norm(mini_var_y) == _base._norm(_base._COL_PUESTO)):
            checks.append((False, "mini_var_x / mini_var_y",
                           "'Puesto' no vale -- su correlación con Puntaje es circular, no un hallazgo"))
        elif x_norm not in valid_norms or y_norm not in valid_norms:
            checks.append((False, "mini_var_x / mini_var_y",
                           f"Deben ser columnas reales del dataset (copia el nombre EXACTO de la "
                           f"matriz de arriba), obtuve '{mini_var_x}' / '{mini_var_y}'"))
        elif x_norm == y_norm:
            checks.append((False, "mini_var_x / mini_var_y", "Debes elegir DOS columnas distintas"))
        elif frozenset([x_norm, y_norm]) in _base._USED_PAIRS:
            checks.append((False, "mini_var_x / mini_var_y",
                           "Este par ya se trabajó en una ronda anterior de Semana 3/4 -- elige un "
                           "par que no hayas usado todavía"))
        else:
            checks.append((True, "mini_var_x / mini_var_y — par nuevo y válido", "✓"))
            pair_ok = True

        if pair_ok and df is not None:
            col_x_real = next(c for c in _base._TODAS_COLUMNAS_MINI if _base._norm(c) == x_norm)
            col_y_real = next(c for c in _base._TODAS_COLUMNAS_MINI if _base._norm(c) == y_norm)
            r_real = df[col_x_real].corr(df[col_y_real])
            if mini_r is None or not _base._is_number(mini_r) or not _base._approx(mini_r, r_real, tol=0.01):
                checks.append((False, "mini_r",
                               "No coincide con tu par -- vuelve a ejecutar la celda completa "
                               "(con mini_var_x/mini_var_y ya elegidos) sin editar la línea que calcula mini_r"))
            else:
                checks.append((True, f"mini_r ≈ {r_real:.3f}", "✓  Coincide con tu propio par"))
        else:
            checks.append((False, "mini_r", "No se pudo validar -- corrige mini_var_x/mini_var_y primero"))

        if _base._is_nontrivial_text(mini_hipotesis):
            checks.append((True, "mini_hipotesis", "✓  Hipótesis registrada"))
        else:
            checks.append((False, "mini_hipotesis",
                           "Escribe una hipótesis real (no dejes '___') de por qué crees que estas "
                           "dos variables podrían estar relacionadas"))

        return self._award("intex1", checks, 15)

    # ═══════════════════════════════════════════════════════════
    # LOGROS -- mismas claves que autograder_nb4.py (mismo razonamiento que
    # autograder_nb3_lite.py: reusar claves existentes evita reescribir el
    # ach_display de resumen()), condiciones adaptadas a esta ruta.
    # ═══════════════════════════════════════════════════════════

    def _check_achievements(self, key):
        unlocked = []
        earned, possible, pct = self._totals()

        if any(e > 0 for e, _ in self._scores.values()) and self._unlock("primer_rayo"):
            unlocked.append(("☀️ Primer Rayo de Sol — ¡Tu primer punto de felicidad conquistado!", "#ff9e2c", "Chispa"))

        # Cartografo de Patrones (reutilizado) -- t8, t9 y el debug-MC (t11), perfectos
        t_rondas = ["t8", "t9", "t11"]
        if (all(k in self._scores and self._scores[k][0] == self._scores[k][1] for k in t_rondas)
                and self._unlock("cartografo_patrones")):
            unlocked.append(("🗺️ Cartógrafo de Patrones — Tus tres preguntas de teoría de Semana 4, perfectas", "#4aa8d8", "Rayo"))

        # Explorador Completo (reutilizado) -- detecto la trampa de Oceania (t10)
        if (self._scores.get("t10", (0, 1))[0] == self._scores.get("t10", (0, 1))[1]
                and "t10" in self._scores and self._unlock("explorador_completo")):
            unlocked.append(("🧭 Explorador Completo — Detectaste la trampa de Oceanía (n=2)", "#ffb703", "Amanecer"))

        # Depurador Feliz (reutilizado) -- identifico el error sin escribir la correccion
        if (self._scores.get("t11", (0, 1))[0] == self._scores.get("t11", (0, 1))[1]
                and "t11" in self._scores and self._unlock("depurador_feliz")):
            unlocked.append(("🔧 Depurador Feliz — Identificaste el error sin perder la calma", "#ffb703", "Amanecer"))

        # Descubridor (reutilizado) -- mini-proyecto perfecto
        if (self._scores.get("intex1", (0, 1))[0] == self._scores.get("intex1", (0, 1))[1]
                and "intex1" in self._scores and self._unlock("descubridor")):
            unlocked.append(("🔍 Descubridor — Encontraste tu propio patrón, con hipótesis y todo", "#ff9e2c", "Sol Pleno"))

        if len(self._checkpoints) >= 2 and self._unlock("medalla_camino"):
            unlocked.append(("🌻 Medalla del Camino — Ambos checkpoints de Semana 4 superados", "#ffb703", "Amanecer"))

        if self._streak >= 5 and self._unlock("racha_bienestar"):
            unlocked.append(("🔥 Racha de Bienestar — Combo x5", "#4aa8d8", "Rayo"))

        if pct >= 100 and self._unlock("felicidad_plena"):
            unlocked.append(("🏆 Felicidad Plena — 100% de la Semana 4", "#ff9e2c", "Sol Pleno"))

        lvl_num, lvl_name = _base._level_info(pct)
        if lvl_num > self._prev_level and self._prev_level > 0:
            unlocked.append((f"⬆️ ¡SUBISTE DE NIVEL! — {lvl_name}", "#4aa8d8", "Nivel"))
        if lvl_num > self._prev_level:
            self._prev_level = lvl_num

        return unlocked

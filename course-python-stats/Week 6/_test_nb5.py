# -*- coding: utf-8 -*-
"""
ATLAS validation script (throwaway, per COURSE_TEMPLATE.md §3 pattern) --
imports autograder_nb5.py directly and asserts every check_* behaves:
(1) correct solution passes, (2) common wrong answer fails/loses points,
(3) hardcoded/lazy answer fails. Also confirms sum(max_pts) == _CORE_MAX
and sum(bonus max_pts) == _BONUS_MAX. Not pytest -- run directly:
`python _test_nb5.py`.

R² ground truth is recomputed fresh from athlete_events_es.csv in this
script (same test_size=0.1/random_state=42 the notebook asks students to
use) rather than trusted from the autograder's own _R2_LOOKUP -- so this
also catches a drifted lookup table, not just broken check_* logic.

Network calls (grade-reflexion Edge Function) are monkeypatched out --
_call_grade_reflexion is replaced per-test so no real Supabase/DeepSeek
call happens and results are deterministic.
"""
import builtins

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# input() would block in a non-interactive run -- the registration form's
# ImportError fallback (no google.colab available here) calls input() three
# times. Feed it canned answers.
_inputs = iter(["Estudiante de Prueba", "1", "12345678"] * 50)
builtins.input = lambda *a, **k: next(_inputs)

DF = pd.read_csv(r"..\Weeks 1-2\athlete_events_es.csv")
DF = DF.dropna(subset=["Edad", "Altura", "Peso", "Sexo"]).copy()
DF["Sexo_num"] = (DF["Sexo"] == "M").astype(int)

PASS = []
FAIL = []


def check(label, cond):
    if cond:
        PASS.append(label)
    else:
        FAIL.append(label)
        print(f"  FAIL: {label}")


def reset_globals():
    import __main__
    for name in list(vars(__main__).keys()):
        if name.startswith(("predictores_ex1", "train_r2_ex1", "test_r2_ex1",
                             "interpretacion_ex1", "combo_ex2", "mejor_test_r2_ex2",
                             "prediccion_absurda_reto1", "descripcion_absurda_reto1")):
            delattr(__main__, name)


def setg(**kwargs):
    import __main__
    for k, v in kwargs.items():
        setattr(__main__, k, v)


def fit_r2(cols):
    X = DF[list(cols)]
    y = DF["Altura"]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.1, random_state=42)
    m = LinearRegression().fit(Xtr, ytr)
    return m.score(Xtr, ytr), r2_score(yte, m.predict(Xte))


print("=" * 70)
print("NB5 -- autograder_nb5.py")
print("=" * 70)

import autograder_nb5 as ag5

g5 = ag5.Autograder()
g5._dni = "TEST"

# ── Teoria t1-t5: correcta pasa, incorrecta falla ──────────────────
for n in range(1, 6):
    spec = g5._TEORIA[n]
    correct = spec["correct"]
    wrong = next(l for l in "abcd" if l != correct)

    g5._scores.pop(f"t{n}", None)
    g5._grade_teoria(n, correct)
    pts, mx = g5._scores[f"t{n}"]
    check(f"nb5 t{n} correcta -> {mx}/{mx}", pts == mx)

    g5._scores.pop(f"t{n}", None)
    g5._grade_teoria(n, wrong)
    pts, mx = g5._scores[f"t{n}"]
    check(f"nb5 t{n} incorrecta -> 0/{mx}", pts == 0)

# ── Ex1: combo real, R² real, interpretacion no causal -> 40/40 ────
COMBO = ["Edad", "Peso", "Sexo_num"]
train_r2, test_r2 = fit_r2(COMBO)
print(f"  (ground truth Edad+Peso+Sexo_num: train_r2={train_r2:.4f} test_r2={test_r2:.4f})")

reset_globals()
setg(predictores_ex1=COMBO, train_r2_ex1=train_r2, test_r2_ex1=test_r2,
     interpretacion_ex1="El peso tiene el coeficiente mas grande, asi que aporta mas a la prediccion de altura.")
g5._scores.pop("ex1", None)
g5.check_ex1()
pts, mx = g5._scores["ex1"]
check(f"nb5 ex1 solucion correcta -> {mx}/{mx}", pts == mx)

reset_globals()
setg(predictores_ex1=["Edad", "Deporte"], train_r2_ex1=train_r2, test_r2_ex1=test_r2,
     interpretacion_ex1="Interpretacion valida de mas de quince caracteres.")
g5._scores.pop("ex1", None)
g5.check_ex1()
pts, mx = g5._scores["ex1"]
check("nb5 ex1 predictor fuera de menu (Deporte) -> pts < max", pts < mx)

reset_globals()
setg(predictores_ex1=COMBO, train_r2_ex1=0.5, test_r2_ex1=0.5,
     interpretacion_ex1="Interpretacion valida de mas de quince caracteres.")
g5._scores.pop("ex1", None)
g5.check_ex1()
pts, mx = g5._scores["ex1"]
check("nb5 ex1 R2 hardcodeado (0.5) -> pts < max", pts < mx)

reset_globals()
setg(predictores_ex1=COMBO, train_r2_ex1=train_r2, test_r2_ex1=test_r2,
     interpretacion_ex1="El peso causa que la altura aumente en el modelo.")
g5._scores.pop("ex1", None)
g5.check_ex1()
pts, mx = g5._scores["ex1"]
check("nb5 ex1 interpretacion con lenguaje causal ('causa') -> pts < max", pts < mx)

reset_globals()
setg(predictores_ex1=COMBO, train_r2_ex1=train_r2, test_r2_ex1=test_r2,
     interpretacion_ex1="___")
g5._scores.pop("ex1", None)
g5.check_ex1()
pts, mx = g5._scores["ex1"]
check("nb5 ex1 interpretacion placeholder '___' -> pts < max", pts < mx)

reset_globals()
setg(predictores_ex1=COMBO, train_r2_ex1=train_r2, test_r2_ex1=test_r2,
     interpretacion_ex1="La variable que elegí para este modelo influye bastante en el resultado que obtuve.")
g5._scores.pop("ex1", None)
g5.check_ex1()
pts, mx = g5._scores["ex1"]
check("nb5 ex1 interpretacion generica sin predictor ni numero -> pts < max", pts < mx)

reset_globals()
setg(predictores_ex1=COMBO, train_r2_ex1=train_r2, test_r2_ex1=test_r2,
     interpretacion_ex1="El coeficiente de Peso fue el más grande, así que aporta más al predecir la altura.")
g5._scores.pop("ex1", None)
g5.check_ex1()
pts, mx = g5._scores["ex1"]
check(f"nb5 ex1 interpretacion que nombra un predictor -> {mx}/{mx}", pts == mx)

reset_globals()
setg(predictores_ex1=COMBO, train_r2_ex1=train_r2, test_r2_ex1=test_r2,
     interpretacion_ex1="Uno de los coeficientes fue cercano a 0.5, así que ese predictor sube el resultado.")
g5._scores.pop("ex1", None)
g5.check_ex1()
pts, mx = g5._scores["ex1"]
check(f"nb5 ex1 interpretacion que da un número sin nombrar predictor -> {mx}/{mx}", pts == mx)

# ── mini_a no truena ────────────────────────────────────────────────
try:
    g5.check_mini_a()
    check("nb5 check_mini_a() no truena", True)
except Exception as e:
    check(f"nb5 check_mini_a() no truena ({e})", False)

# ── Ex2: mejor combo real -> 20/20; combo invalida -> falla ────────
train_r2b, test_r2b = fit_r2(["Peso", "Sexo_num"])
reset_globals()
setg(combo_ex2=COMBO, mejor_test_r2_ex2=test_r2)
g5._scores.pop("ex2", None)
g5.check_ex2()
pts, mx = g5._scores["ex2"]
check(f"nb5 ex2 mejor combo real (Edad+Peso+Sexo_num) -> {mx}/{mx}", pts == mx)

reset_globals()
setg(combo_ex2=["Peso", "Sexo_num"], mejor_test_r2_ex2=test_r2b)
g5._scores.pop("ex2", None)
g5.check_ex2()
pts, mx = g5._scores["ex2"]
check(f"nb5 ex2 otra combo valida (Peso+Sexo_num) -> {mx}/{mx}", pts == mx)

reset_globals()
setg(combo_ex2=["Edad"], mejor_test_r2_ex2=test_r2)
g5._scores.pop("ex2", None)
g5.check_ex2()
pts, mx = g5._scores["ex2"]
check("nb5 ex2 combo de 1 sola columna -> pts < max", pts < mx)

reset_globals()
setg(combo_ex2=COMBO, mejor_test_r2_ex2=0.99)
g5._scores.pop("ex2", None)
g5.check_ex2()
pts, mx = g5._scores["ex2"]
check("nb5 ex2 R2 inventado (0.99) -> pts < max", pts < mx)

# ── Reto1 (bonus): prediccion + descripcion -> 10/10; incompleto -> menos
reset_globals()
setg(prediccion_absurda_reto1=673.45,
     descripcion_absurda_reto1="Usé Edad=200 y Peso=1000, la predicción de 673cm es imposible para una persona.")
g5._scores.pop("reto1", None)
g5.check_reto1()
pts, mx = g5._scores["reto1"]
check(f"nb5 reto1 completo -> {mx}/{mx}", pts == mx)

reset_globals()
setg(prediccion_absurda_reto1=None, descripcion_absurda_reto1=None)
g5._scores.pop("reto1", None)
g5.check_reto1()
pts, mx = g5._scores["reto1"]
check("nb5 reto1 sin completar -> 0/10", pts == 0)

# ── Reflexiones: red simulada OK, red caida no califica 0, placeholder = 0
def fake_grade_ok(reflexion_id, text):
    return (4, "Buena reflexion de prueba.")


def fake_grade_none(reflexion_id, text):
    return None


for rid, method in [("nb5_interpretacion", "check_reflexion_interpretacion"),
                     ("nb5_ex2", "check_reflexion_ex2"),
                     ("nb5_final", "check_reflexion_final")]:
    g5._scores.pop(f"refl_{rid}", None)
    g5._call_grade_reflexion = fake_grade_ok
    g5._grade_reflexion(rid, "Esta es una reflexion real de mas de quince caracteres.")
    pts, mx = g5._scores[f"refl_{rid}"]
    check(f"nb5 refl_{rid} con IA simulada -> 4/{mx}", pts == 4 and mx == 5)

    g5._scores.pop(f"refl_{rid}", None)
    g5._grade_reflexion(rid, "___")
    check(f"nb5 refl_{rid} placeholder '___' -> no califica (sin red)",
          f"refl_{rid}" in g5._scores and g5._scores[f"refl_{rid}"][0] == 0)

    g5._scores.pop(f"refl_{rid}", None)
    g5._call_grade_reflexion = fake_grade_none
    g5._grade_reflexion(rid, "Un texto real y largo pero la red esta caida ahora mismo.")
    check(f"nb5 refl_{rid} fallo de red -> NO registra score (no es un 0)",
          f"refl_{rid}" not in g5._scores)

# ── check_reflexion_* pasan el reflexion_id "nb5_*" correcto a _ask_reflexion
# (no solo probar _grade_reflexion con un id inventado a mano, como arriba --
# eso nunca hubiera detectado el bug real: check_reflexion_interpretacion()
# llamando a _ask_reflexion("interpretacion", ...) sin el prefijo "nb5_" que
# espera la funcion Edge. Esto no puede verificar el allowlist/GRADING_NOTES
# del lado del servidor -- para eso hace falta la prueba real end-to-end
# descrita en el docstring de grade-reflexion/index.ts -- pero al menos
# atrapa un typo de wiring local sin red.)
_seen_ids = {}


def _capture_ask_reflexion(rid, question):
    _seen_ids["last"] = rid


g5._ask_reflexion = _capture_ask_reflexion
for expected_id, method in [("nb5_interpretacion", "check_reflexion_interpretacion"),
                             ("nb5_ex2", "check_reflexion_ex2"),
                             ("nb5_final", "check_reflexion_final")]:
    _seen_ids.clear()
    getattr(g5, method)()
    check(f"nb5 {method}() llama a _ask_reflexion con id '{expected_id}'",
          _seen_ids.get("last") == expected_id)
del g5._ask_reflexion

# ── Registro (🔮 PREDICE / 📝 ANOTA): participación local, sin red ──
g5._scores.pop("reg_manual_test", None)
g5._grade_registro("manual_test", "abc")
pts, mx = g5._scores["reg_manual_test"]
check(f"nb5 registro con texto valido (>= min_len) -> {mx}/{mx}", pts == mx == 1)
check("nb5 registro guarda el texto crudo en _text_answers",
      g5._text_answers.get("reg_manual_test") == "abc")

g5._scores.pop("reg_manual_short", None)
g5._grade_registro("manual_short", "ab")
pts, mx = g5._scores["reg_manual_short"]
check("nb5 registro con texto mas corto que min_len=3 -> 0/1", pts == 0 and mx == 1)

g5._scores.pop("reg_manual_placeholder", None)
g5._grade_registro("manual_placeholder", "___")
pts, mx = g5._scores["reg_manual_placeholder"]
check("nb5 registro con placeholder '___' -> 0/1", pts == 0 and mx == 1)

# check_prediccion_linea()/check_anota_distancia() pasan el id correcto a
# _ask_registro (mismo motivo que la prueba de wiring de arriba: un typo de
# id aca no rompe nada visiblemente, solo deja el texto guardado bajo una
# llave distinta a la esperada).
def _capture_ask_registro(id, question, icon="🔮", label="PREDICE"):
    _seen_ids["last"] = id


g5._ask_registro = _capture_ask_registro
for expected_id, method in [("linea_roja", "check_prediccion_linea"),
                             ("minimiza_distancia", "check_anota_distancia")]:
    _seen_ids.clear()
    getattr(g5, method)()
    check(f"nb5 {method}() llama a _ask_registro con id '{expected_id}'",
          _seen_ids.get("last") == expected_id)
del g5._ask_registro

# ── _CORE_MAX / _BONUS_MAX == suma de max_pts declarados ───────────
declared_core = 1 * 2 + 5 * 5 + 5 + 40 + 20 + 5 + 5  # registro + t1-5 + refl_interp + ex1 + ex2 + refl_ex2 + refl_final
check(f"nb5 _CORE_MAX ({ag5._CORE_MAX}) == suma declarada ({declared_core})",
      ag5._CORE_MAX == declared_core)

declared_bonus = 10  # reto1
check(f"nb5 _BONUS_MAX ({ag5._BONUS_MAX}) == suma declarada ({declared_bonus})",
      ag5._BONUS_MAX == declared_bonus)

# ── mini_b / resumen no truenan ─────────────────────────────────────
try:
    g5.check_mini_b()
    g5.resumen()
    check("nb5 check_mini_b() + resumen() no truenan", True)
except Exception as e:
    check(f"nb5 check_mini_b()/resumen() no truenan ({e})", False)

print()
print("=" * 70)
print(f"RESULTADO: {len(PASS)} pasaron, {len(FAIL)} fallaron")
print("=" * 70)
if FAIL:
    print("Fallas:")
    for f in FAIL:
        print(f"  - {f}")
    raise SystemExit(1)

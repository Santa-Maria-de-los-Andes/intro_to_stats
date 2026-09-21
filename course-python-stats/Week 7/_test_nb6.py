# -*- coding: utf-8 -*-
"""
ATLAS validation script (throwaway, per COURSE_TEMPLATE.md §3 pattern) --
imports autograder_nb6.py directly and asserts every check_* behaves:
(1) correct solution passes, (2) common wrong answer fails/loses points,
(3) hardcoded/lazy or unscaled answer fails. Also confirms sum(max_pts)
== _CORE_MAX and sum(bonus max_pts) == _BONUS_MAX. Not pytest -- run
directly: `python _test_nb6.py`.

Ground truth is recomputed fresh from spotify_es.csv in this script (same
StandardScaler + KMeans(n_clusters=3, random_state=42) the notebook asks
students to use) rather than trusted from any hardcoded lookup in the
autograder -- unlike nb3/4/5's R²/r, ex1/reto1 here are graded
structurally (see autograder_nb6.py's docstring for why a literal
cluster-index lookup would be both fragile and pedagogically wrong for
k-means), so this script's job is to confirm those structural checks
accept a real, correctly-scaled fit and reject the realistic mistakes
(unscaled data, unfitted model, wrong predictor menu, treating a cluster
as a fixed genre).

Network calls (grade-reflexion Edge Function) are monkeypatched out --
_call_grade_reflexion is replaced per-test so no real Supabase/DeepSeek
call happens and results are deterministic.

2026-09-21 (simplification pass -- see autograder_nb6.py's docstring):
check_ex2/check_ex3 no longer exist (Ejercicio 2 became an ungraded demo,
Ejercicio 3 was removed entirely), so their test blocks below were
removed too. Ex1 now accepts 2 or 3 predictors (was exactly 2) -- added a
3-predictor pass case alongside the existing 2-predictor ones.
"""
import builtins

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# input() would block in a non-interactive run -- the registration form's
# ImportError fallback (no google.colab available here) calls input() three
# times. Feed it canned answers.
_inputs = iter(["Estudiante de Prueba", "1", "12345678"] * 50)
builtins.input = lambda *a, **k: next(_inputs)

DF = pd.read_csv("spotify_es.csv")
DF = DF.dropna(subset=["Artistas", "Nombre_Cancion"]).copy()
DF = DF[DF["Tempo"] > 0].copy()  # unas pocas filas con Tempo=0 son fallos de deteccion

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
        if name.startswith((
            "predictores_ex1", "modelo_ex1", "cluster_interes_ex1", "interpretacion_ex1",
            "k_reto1", "modelo_reto1", "comentario_reto1",
            "respuesta_cluster_es_genero", "explicacion_cluster_es_genero",
        )):
            delattr(__main__, name)


def setg(**kwargs):
    import __main__
    for k, v in kwargs.items():
        setattr(__main__, k, v)


def fit_scaled(cols, k=3, seed=42):
    X = DF[list(cols)]
    Xs = StandardScaler().fit_transform(X)
    return KMeans(n_clusters=k, random_state=seed, n_init=10).fit(Xs)


def fit_unscaled(cols, k=3, seed=42):
    X = DF[list(cols)]
    return KMeans(n_clusters=k, random_state=seed, n_init=10).fit(X)


print("=" * 70)
print("NB6 -- autograder_nb6.py")
print("=" * 70)

import autograder_nb6 as ag6

g6 = ag6.Autograder()
g6._dni = "TEST"

# ── Teoria t1-t5: correcta pasa, incorrecta falla ──────────────────
for n in range(1, 6):
    spec = g6._TEORIA[n]
    correct = spec["correct"]
    wrong = next(l for l in "abcd" if l != correct)

    g6._scores.pop(f"t{n}", None)
    g6._grade_teoria(n, correct)
    pts, mx = g6._scores[f"t{n}"]
    check(f"nb6 t{n} correcta -> {mx}/{mx}", pts == mx)

    g6._scores.pop(f"t{n}", None)
    g6._grade_teoria(n, wrong)
    pts, mx = g6._scores[f"t{n}"]
    check(f"nb6 t{n} incorrecta -> 0/{mx}", pts == 0)

# ── cluster_es_genero: respuesta correcta 'no' + explicacion con numero -> 5/5
reset_globals()
setg(respuesta_cluster_es_genero="no",
     explicacion_cluster_es_genero="El género más común dentro de un cluster fue Hardstyle con apenas 2.3%.")
g6._scores.pop("cluster_es_genero", None)
g6.check_cluster_es_genero()
pts, mx = g6._scores["cluster_es_genero"]
check(f"nb6 cluster_es_genero respuesta correcta + explicacion con numero -> {mx}/{mx}", pts == mx)

reset_globals()
setg(respuesta_cluster_es_genero="si",
     explicacion_cluster_es_genero="El género más común dentro de un cluster fue Hardstyle con apenas 2.3%.")
g6._scores.pop("cluster_es_genero", None)
g6.check_cluster_es_genero()
pts, mx = g6._scores["cluster_es_genero"]
check("nb6 cluster_es_genero respuesta 'si' (incorrecta) -> pts < max", pts < mx)

reset_globals()
setg(respuesta_cluster_es_genero="no", explicacion_cluster_es_genero="No lo son.")
g6._scores.pop("cluster_es_genero", None)
g6.check_cluster_es_genero()
pts, mx = g6._scores["cluster_es_genero"]
check("nb6 cluster_es_genero explicacion sin numero -> pts < max", pts < mx)

reset_globals()
setg(respuesta_cluster_es_genero=None, explicacion_cluster_es_genero=None)
g6._scores.pop("cluster_es_genero", None)
g6.check_cluster_es_genero()
pts, mx = g6._scores["cluster_es_genero"]
check("nb6 cluster_es_genero sin completar -> 0/5", pts == 0)

# ── Ex1: combo real, modelo escalado real, interpretacion valida -> 40/40 ──
COMBO1 = ["Bailabilidad", "Tempo"]
modelo1_real = fit_scaled(COMBO1)
print(f"  (ground truth {COMBO1}: cluster_centers_={np.round(modelo1_real.cluster_centers_, 2).tolist()})")

reset_globals()
setg(predictores_ex1=COMBO1, modelo_ex1=modelo1_real, cluster_interes_ex1=0,
     interpretacion_ex1="Este cluster tiene un Tempo promedio bajo, cercano al centro del grupo.")
g6._scores.pop("ex1", None)
g6.check_ex1()
pts, mx = g6._scores["ex1"]
check(f"nb6 ex1 solucion correcta (escalada) -> {mx}/{mx}", pts == mx)

COMBO1B = ["Bailabilidad", "Tempo", "Energia"]
modelo1b_real = fit_scaled(COMBO1B)
reset_globals()
setg(predictores_ex1=COMBO1B, modelo_ex1=modelo1b_real, cluster_interes_ex1=0,
     interpretacion_ex1="Este cluster tiene Energia y Tempo altos frente a los otros dos grupos.")
g6._scores.pop("ex1", None)
g6.check_ex1()
pts, mx = g6._scores["ex1"]
check(f"nb6 ex1 con 3 predictores (Bailabilidad+Tempo+Energia, escalado) -> {mx}/{mx}", pts == mx)

reset_globals()
setg(predictores_ex1=["Tempo", "Popularidad"], modelo_ex1=modelo1_real, cluster_interes_ex1=0,
     interpretacion_ex1="Interpretacion valida de mas de quince caracteres con Tempo.")
g6._scores.pop("ex1", None)
g6.check_ex1()
pts, mx = g6._scores["ex1"]
check("nb6 ex1 predictor fuera de menu (Popularidad) -> pts < max", pts < mx)

reset_globals()
modelo1_unscaled = fit_unscaled(COMBO1)
setg(predictores_ex1=COMBO1, modelo_ex1=modelo1_unscaled, cluster_interes_ex1=0,
     interpretacion_ex1="Interpretacion valida de mas de quince caracteres con Tempo.")
g6._scores.pop("ex1", None)
g6.check_ex1()
pts, mx = g6._scores["ex1"]
check("nb6 ex1 modelo SIN escalar -> pts < max", pts < mx)

reset_globals()
setg(predictores_ex1=COMBO1, modelo_ex1=KMeans(n_clusters=3, random_state=42), cluster_interes_ex1=0,
     interpretacion_ex1="Interpretacion valida de mas de quince caracteres con Tempo.")
g6._scores.pop("ex1", None)
g6.check_ex1()
pts, mx = g6._scores["ex1"]
check("nb6 ex1 modelo sin ajustar (.fit() nunca llamado) -> pts < max", pts < mx)

reset_globals()
setg(predictores_ex1=COMBO1, modelo_ex1=modelo1_real, cluster_interes_ex1=99,
     interpretacion_ex1="Interpretacion valida de mas de quince caracteres con Tempo.")
g6._scores.pop("ex1", None)
g6.check_ex1()
pts, mx = g6._scores["ex1"]
check("nb6 ex1 cluster_interes_ex1 fuera de rango (99) -> pts < max", pts < mx)

reset_globals()
setg(predictores_ex1=COMBO1, modelo_ex1=modelo1_real, cluster_interes_ex1=0,
     interpretacion_ex1="Este cluster es de canciones de Reggaetón, sin duda alguna.")
g6._scores.pop("ex1", None)
g6.check_ex1()
pts, mx = g6._scores["ex1"]
check("nb6 ex1 interpretacion trata el cluster como genero fijo -> pts < max", pts < mx)

reset_globals()
setg(predictores_ex1=COMBO1, modelo_ex1=modelo1_real, cluster_interes_ex1=0,
     interpretacion_ex1="Este grupo agrupa canciones parecidas entre si, nada mas que eso.")
g6._scores.pop("ex1", None)
g6.check_ex1()
pts, mx = g6._scores["ex1"]
check("nb6 ex1 interpretacion generica sin predictor ni numero -> pts < max", pts < mx)

reset_globals()
setg(predictores_ex1=COMBO1, modelo_ex1=modelo1_real, cluster_interes_ex1=0,
     interpretacion_ex1="___")
g6._scores.pop("ex1", None)
g6.check_ex1()
pts, mx = g6._scores["ex1"]
check("nb6 ex1 interpretacion placeholder '___' -> pts < max", pts < mx)

# ── mini_a no truena ────────────────────────────────────────────────
try:
    g6.check_mini_a()
    check("nb6 check_mini_a() no truena", True)
except Exception as e:
    check(f"nb6 check_mini_a() no truena ({e})", False)

# ── Reto1 (bonus): k distinto de 3 + modelo escalado + comentario -> 10/10
reset_globals()
setg(k_reto1=4, modelo_reto1=fit_scaled(COMBO1, k=4), comentario_reto1="Con k=4 el grupo grande de antes se dividió en dos.")
g6._scores.pop("reto1", None)
g6.check_reto1()
pts, mx = g6._scores["reto1"]
check(f"nb6 reto1 completo (k=4) -> {mx}/{mx}", pts == mx)

reset_globals()
setg(k_reto1=3, modelo_reto1=modelo1_real, comentario_reto1="Comentario valido de mas de diez caracteres.")
g6._scores.pop("reto1", None)
g6.check_reto1()
pts, mx = g6._scores["reto1"]
check("nb6 reto1 con k=3 (no distinto) -> pts < max", pts < mx)

reset_globals()
setg(k_reto1=None, modelo_reto1=None, comentario_reto1=None)
g6._scores.pop("reto1", None)
g6.check_reto1()
pts, mx = g6._scores["reto1"]
check("nb6 reto1 sin completar -> 0/10", pts == 0)

# ── Reflexiones: red simulada OK, red caida no califica 0, placeholder = 0
def fake_grade_ok(reflexion_id, text):
    return (4, "Buena reflexion de prueba.")


def fake_grade_none(reflexion_id, text):
    return None


for rid, method in [("nb6_ex2", "check_reflexion_ex2"), ("nb6_generalizacion", "check_reflexion_generalizacion"),
                    ("nb6_final", "check_reflexion_final")]:
    g6._scores.pop(f"refl_{rid}", None)
    g6._call_grade_reflexion = fake_grade_ok
    g6._grade_reflexion(rid, "Esta es una reflexion real de mas de quince caracteres.")
    pts, mx = g6._scores[f"refl_{rid}"]
    check(f"nb6 refl_{rid} con IA simulada -> 4/{mx}", pts == 4 and mx == 5)

    g6._scores.pop(f"refl_{rid}", None)
    g6._grade_reflexion(rid, "___")
    check(f"nb6 refl_{rid} placeholder '___' -> no califica (sin red)",
          f"refl_{rid}" in g6._scores and g6._scores[f"refl_{rid}"][0] == 0)

    g6._scores.pop(f"refl_{rid}", None)
    g6._call_grade_reflexion = fake_grade_none
    g6._grade_reflexion(rid, "Un texto real y largo pero la red esta caida ahora mismo.")
    check(f"nb6 refl_{rid} fallo de red -> NO registra score (no es un 0)",
          f"refl_{rid}" not in g6._scores)

# ── check_reflexion_* pasan el reflexion_id "nb6_*" correcto a _ask_reflexion
_seen_ids = {}


def _capture_ask_reflexion(rid, question):
    _seen_ids["last"] = rid


g6._ask_reflexion = _capture_ask_reflexion
for expected_id, method in [("nb6_ex2", "check_reflexion_ex2"), ("nb6_generalizacion", "check_reflexion_generalizacion"),
                             ("nb6_final", "check_reflexion_final")]:
    _seen_ids.clear()
    getattr(g6, method)()
    check(f"nb6 {method}() llama a _ask_reflexion con id '{expected_id}'",
          _seen_ids.get("last") == expected_id)
del g6._ask_reflexion

# ── Registro (🔮 PREDICE / 📝 ANOTA): participación local, sin red ──
g6._scores.pop("reg_manual_test", None)
g6._grade_registro("manual_test", "abc")
pts, mx = g6._scores["reg_manual_test"]
check(f"nb6 registro con texto valido (>= min_len) -> {mx}/{mx}", pts == mx == 1)
check("nb6 registro guarda el texto crudo en _text_answers",
      g6._text_answers.get("reg_manual_test") == "abc")

g6._scores.pop("reg_manual_placeholder", None)
g6._grade_registro("manual_placeholder", "___")
pts, mx = g6._scores["reg_manual_placeholder"]
check("nb6 registro con placeholder '___' -> 0/1", pts == 0 and mx == 1)


def _capture_ask_registro(id, question, icon="🔮", label="PREDICE"):
    _seen_ids["last"] = id


g6._ask_registro = _capture_ask_registro
for expected_id, method in [("cuantos_grupos", "check_cuantos_grupos"), ("como_agrupa", "check_como_agrupa")]:
    _seen_ids.clear()
    getattr(g6, method)()
    check(f"nb6 {method}() llama a _ask_registro con id '{expected_id}'",
          _seen_ids.get("last") == expected_id)
del g6._ask_registro

# ── _CORE_MAX / _BONUS_MAX == suma de max_pts declarados ───────────
declared_core = 1 * 2 + 5 + 5 * 5 + 40 + 5 + 5 + 5  # registro + cluster_es_genero + t1-5 + ex1 + refl_ex2 + refl_generalizacion + refl_final
check(f"nb6 _CORE_MAX ({ag6._CORE_MAX}) == suma declarada ({declared_core})",
      ag6._CORE_MAX == declared_core)

declared_bonus = 10  # reto1
check(f"nb6 _BONUS_MAX ({ag6._BONUS_MAX}) == suma declarada ({declared_bonus})",
      ag6._BONUS_MAX == declared_bonus)

# ── mini_b / resumen no truenan ─────────────────────────────────────
try:
    g6.check_mini_b()
    g6.resumen()
    check("nb6 check_mini_b() + resumen() no truenan", True)
except Exception as e:
    check(f"nb6 check_mini_b()/resumen() no truenan ({e})", False)

print()
print("=" * 70)
print(f"RESULTADO: {len(PASS)} pasaron, {len(FAIL)} fallaron")
print("=" * 70)
if FAIL:
    print("Fallas:")
    for f in FAIL:
        print(f"  - {f}")
    raise SystemExit(1)

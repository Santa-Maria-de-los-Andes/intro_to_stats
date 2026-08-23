# -*- coding: utf-8 -*-
"""
ATLAS validation script (throwaway, per COURSE_TEMPLATE.md §3 pattern) --
imports autograder_nb3.py / autograder_nb4.py directly and asserts every
check_* behaves: (1) correct solution passes, (2) common wrong answer fails,
(3) hardcoded/lazy answer fails. Also confirms sum(max_pts) == _CORE_MAX for
both files. Not pytest -- run directly: `python _test_nb3_nb4.py`.

Network calls (grade-reflexion Edge Function) are monkeypatched out --
_call_grade_reflexion is replaced per-test so no real Supabase/DeepSeek call
happens and results are deterministic.
"""
import builtins
import sys

import pandas as pd

# input() would block in a non-interactive run -- the registration form's
# ImportError fallback (no google.colab available here) calls input() three
# times. Feed it canned answers.
_inputs = iter(["Estudiante de Prueba", "1", "12345678"] * 50)
builtins.input = lambda *a, **k: next(_inputs)

DF = pd.read_csv("2019_es.csv")

PASS = []
FAIL = []


def check(label, cond):
    if cond:
        PASS.append(label)
    else:
        FAIL.append(label)
        print(f"  ❌ FAIL: {label}")


def reset_globals(mod):
    """Limpia variables de ejercicio del namespace de __main__ entre tests."""
    import __main__
    for name in list(vars(__main__).keys()):
        if name.startswith(("x_ex", "y_ex", "r_ex", "r_pbi", "r_corrupcion",
                             "r_esperanza", "correlaciones_puntaje",
                             "columna_mas_fuerte", "columna_mas_debil",
                             "mi_", "mini_", "r_generosidad_", "respuesta_t")):
            delattr(__main__, name)


def setg(**kwargs):
    import __main__
    for k, v in kwargs.items():
        setattr(__main__, k, v)


import __main__
__main__.df_felicidad = DF

print("=" * 70)
print("NB3 -- autograder_nb3.py")
print("=" * 70)

import autograder_nb3 as ag3

g3 = ag3.Autograder()
g3._dni = "TEST"  # evita el registro interactivo de nuevo en cada check

# ── Teoria t1-t11: correcta pasa, incorrecta falla ─────────────────
for n in range(1, 12):
    spec = g3._TEORIA[n]
    correct = spec["correct"]
    wrong = next(l for l in "abcd" if l != correct)

    g3._scores.pop(f"t{n}", None)
    g3._grade_teoria(n, correct)
    pts, mx = g3._scores[f"t{n}"]
    check(f"nb3 t{n} correcta -> {mx}/{mx}", pts == mx)

    g3._scores.pop(f"t{n}", None)
    g3._grade_teoria(n, wrong)
    pts, mx = g3._scores[f"t{n}"]
    check(f"nb3 t{n} incorrecta -> 0/{mx}", pts == 0)

# ── Ex1-6: correcta pasa, columna mala falla, r hardcodeado falla ──
RONDAS_NB3 = [
    ("ex1", ag3._COL_CORRUPCION, ag3._COL_PUNTAJE, 0.3856130708664784),
    ("ex2", ag3._COL_ESPERANZA, ag3._COL_PUNTAJE, 0.7798831492425831),
    ("ex3", ag3._COL_PBI, ag3._COL_ESPERANZA, 0.8354621150416076),
    ("ex4", ag3._COL_APOYO, ag3._COL_ESPERANZA, 0.7190094590308561),
    ("ex5", ag3._COL_PBI, ag3._COL_APOYO, 0.7549057272454567),
    ("ex6", ag3._COL_GENEROSIDAD, ag3._COL_CORRUPCION, 0.32653754340500746),
]
for key, xcol, ycol, rexp in RONDAS_NB3:
    reset_globals(ag3)
    r_real = DF[xcol].corr(DF[ycol])
    setg(**{f"x_{key}": xcol, f"y_{key}": ycol, f"r_{key}": r_real})
    g3._scores.pop(key, None)
    getattr(g3, f"check_{key}")()
    pts, mx = g3._scores[key]
    check(f"nb3 {key} solucion correcta -> {mx}/{mx}", pts == mx)

    reset_globals(ag3)
    setg(**{f"x_{key}": "columna que no existe", f"y_{key}": ycol, f"r_{key}": r_real})
    g3._scores.pop(key, None)
    getattr(g3, f"check_{key}")()
    pts, mx = g3._scores[key]
    check(f"nb3 {key} columna X mala -> pts < max", pts < mx)

    reset_globals(ag3)
    setg(**{f"x_{key}": xcol, f"y_{key}": ycol, f"r_{key}": 0.5})  # r hardcodeado/lazy
    g3._scores.pop(key, None)
    getattr(g3, f"check_{key}")()
    pts, mx = g3._scores[key]
    check(f"nb3 {key} r hardcodeado (0.5) -> pts < max", pts < mx)

# ── Reflexiones: red simulada OK, red caida no califica 0, placeholder = 0 ──
def fake_grade_ok(reflexion_id, text):
    return (4, "Buena reflexion de prueba.")


def fake_grade_none(reflexion_id, text):
    return None


for rid, method in [("ronda1", "check_reflexion_ronda1"),
                     ("ronda3", "check_reflexion_ronda3"),
                     ("concepto", "check_reflexion_concepto"),
                     ("pbi_apoyo", "check_reflexion_pbi_apoyo"),
                     ("generosidad_corrupcion", "check_reflexion_generosidad_corrupcion")]:
    g3._scores.pop(f"refl_{rid}", None)
    g3._call_grade_reflexion = fake_grade_ok
    g3._grade_reflexion(rid, "Esta es una reflexion real de mas de quince caracteres.")
    pts, mx = g3._scores[f"refl_{rid}"]
    check(f"nb3 refl_{rid} con IA simulada -> 4/{mx}", pts == 4 and mx == 5)

    g3._scores.pop(f"refl_{rid}", None)
    g3._grade_reflexion(rid, "___")
    check(f"nb3 refl_{rid} placeholder '___' -> no califica (sin red)",
          f"refl_{rid}" in g3._scores and g3._scores[f"refl_{rid}"][0] == 0)

    g3._scores.pop(f"refl_{rid}", None)
    g3._call_grade_reflexion = fake_grade_none
    g3._grade_reflexion(rid, "Un texto real y largo pero la red esta caida ahora mismo.")
    check(f"nb3 refl_{rid} fallo de red -> NO registra score (no es un 0)",
          f"refl_{rid}" not in g3._scores)

# ── _CORE_MAX == suma de max_pts declarados ──────────────────────
declared_nb3 = 5 * 11 + 20 * 6 + 5 * 5
check(f"nb3 _CORE_MAX ({ag3._CORE_MAX}) == suma declarada ({declared_nb3})",
      ag3._CORE_MAX == declared_nb3)

# ── mini_a / resumen no truenan ──────────────────────────────────
try:
    g3.check_mini_a()
    g3.resumen()
    check("nb3 check_mini_a() + resumen() no truenan", True)
except Exception as e:
    check(f"nb3 check_mini_a()/resumen() no truenan ({e})", False)


print()
print("=" * 70)
print("NB4 -- autograder_nb4.py")
print("=" * 70)

import autograder_nb4 as ag4

reset_globals(ag4)
g4 = ag4.Autograder()
g4._dni = "TEST"

for n in range(8, 11):
    spec = g4._TEORIA[n]
    correct = spec["correct"]
    wrong = next(l for l in "abcd" if l != correct)

    g4._scores.pop(f"t{n}", None)
    g4._grade_teoria(n, correct)
    pts, mx = g4._scores[f"t{n}"]
    check(f"nb4 t{n} correcta -> {mx}/{mx}", pts == mx)

    g4._scores.pop(f"t{n}", None)
    g4._grade_teoria(n, wrong)
    pts, mx = g4._scores[f"t{n}"]
    check(f"nb4 t{n} incorrecta -> 0/{mx}", pts == 0)

RONDAS_NB4 = [
    ("ex5", ag4._COL_LIBERTAD, ag4._COL_CORRUPCION, 0.4388433064150672),
    ("ex6", ag4._COL_PBI, ag4._COL_GENEROSIDAD, -0.07966231348976406),
]
for key, xcol, ycol, rexp in RONDAS_NB4:
    reset_globals(ag4)
    r_real = DF[xcol].corr(DF[ycol])
    setg(**{f"x_{key}": xcol, f"y_{key}": ycol, f"r_{key}": r_real})
    g4._scores.pop(key, None)
    getattr(g4, f"check_{key}")()
    pts, mx = g4._scores[key]
    check(f"nb4 {key} solucion correcta -> {mx}/{mx}", pts == mx)

    reset_globals(ag4)
    setg(**{f"x_{key}": xcol, f"y_{key}": ycol, f"r_{key}": 0.5})
    g4._scores.pop(key, None)
    getattr(g4, f"check_{key}")()
    pts, mx = g4._scores[key]
    check(f"nb4 {key} r hardcodeado (0.5) -> pts < max", pts < mx)

# ── Debug1 ──────────────────────────────────────────────────────
reset_globals(ag4)
setg(r_pbi=DF[ag4._COL_PBI].corr(DF[ag4._COL_PUNTAJE]))
g4._scores.pop("debug1", None)
g4.check_debug1()
pts, mx = g4._scores["debug1"]
check(f"nb4 debug1 solucion correcta -> {mx}/{mx}", pts == mx)

reset_globals(ag4)
setg(r_pbi=None)
g4._scores.pop("debug1", None)
g4.check_debug1()
pts, mx = g4._scores["debug1"]
check("nb4 debug1 sin corregir (None) -> 0/10", pts == 0)

# ── Ex7 explora-todo ──────────────────────────────────────────────
reset_globals(ag4)
correlaciones = DF[ag4._SEIS_COLUMNAS].corrwith(DF[ag4._COL_PUNTAJE])
setg(correlaciones_puntaje=correlaciones,
     columna_mas_fuerte=ag4._COL_PBI,
     columna_mas_debil=ag4._COL_GENEROSIDAD)
g4._scores.pop("ex7", None)
g4.check_ex7()
pts, mx = g4._scores["ex7"]
check(f"nb4 ex7 solucion correcta -> {mx}/{mx}", pts == mx)

reset_globals(ag4)
correlaciones_con_puesto = DF[ag4._SEIS_COLUMNAS + [ag4._COL_PUESTO]].corrwith(DF[ag4._COL_PUNTAJE])
setg(correlaciones_puntaje=correlaciones_con_puesto,
     columna_mas_fuerte=ag4._COL_PBI,
     columna_mas_debil=ag4._COL_GENEROSIDAD)
g4._scores.pop("ex7", None)
g4.check_ex7()
pts, mx = g4._scores["ex7"]
check("nb4 ex7 con 'Puesto' incluido (trampa circular) -> pts < max", pts < mx)

# ── Ex8 Seccion C ───────────────────────────────────────────────
reset_globals(ag4)
df_eu = DF[DF["Continente"] == "Europa"]
df_am = DF[DF["Continente"] == "América"]
setg(r_generosidad_europa=df_eu["Generosidad"].corr(df_eu["Puntaje"]),
     r_generosidad_america=df_am["Generosidad"].corr(df_am["Puntaje"]))
g4._scores.pop("ex8", None)
g4.check_ex8()
pts, mx = g4._scores["ex8"]
check(f"nb4 ex8 solucion correcta -> {mx}/{mx}", pts == mx)

reset_globals(ag4)
# usa el r GENERAL (no filtrado) en vez del r por continente -- error comun
setg(r_generosidad_europa=DF["Generosidad"].corr(DF["Puntaje"]),
     r_generosidad_america=DF["Generosidad"].corr(DF["Puntaje"]))
g4._scores.pop("ex8", None)
g4.check_ex8()
pts, mx = g4._scores["ex8"]
check("nb4 ex8 con r general sin filtrar (error comun) -> pts < max", pts < mx)

# ── Integracion 1 (mini-proyecto) ──────────────────────────────────
reset_globals(ag4)
setg(mini_var_x=ag4._COL_APOYO, mini_var_y=ag4._COL_LIBERTAD,
     mini_r=DF[ag4._COL_APOYO].corr(DF[ag4._COL_LIBERTAD]),
     mini_hipotesis="Creo que estan relacionadas porque la libertad percibida podria "
                     "reforzar el apoyo social percibido en sociedades mas abiertas.")
g4._scores.pop("intex1", None)
g4.check_intex1()
pts, mx = g4._scores["intex1"]
check(f"nb4 intex1 par nuevo valido -> {mx}/{mx}", pts == mx)

reset_globals(ag4)
# par YA usado en una ronda anterior (PBI vs Puntaje) -- debe rechazarse
setg(mini_var_x=ag4._COL_PBI, mini_var_y=ag4._COL_PUNTAJE,
     mini_r=DF[ag4._COL_PBI].corr(DF[ag4._COL_PUNTAJE]),
     mini_hipotesis="Hipotesis real de mas de quince caracteres para probar el rechazo.")
g4._scores.pop("intex1", None)
g4.check_intex1()
pts, mx = g4._scores["intex1"]
check("nb4 intex1 par ya usado (PBI-Puntaje) -> rechazado, pts < max", pts < mx)

reset_globals(ag4)
# Puesto -- circular, debe rechazarse
setg(mini_var_x=ag4._COL_PUESTO, mini_var_y=ag4._COL_PUNTAJE,
     mini_r=DF[ag4._COL_PUESTO].corr(DF[ag4._COL_PUNTAJE]),
     mini_hipotesis="Hipotesis real de mas de quince caracteres para probar el rechazo.")
g4._scores.pop("intex1", None)
g4.check_intex1()
pts, mx = g4._scores["intex1"]
check("nb4 intex1 con 'Puesto' (circular) -> rechazado, pts < max", pts < mx)

reset_globals(ag4)
# hipotesis placeholder -- debe perder esos puntos
setg(mini_var_x=ag4._COL_APOYO, mini_var_y=ag4._COL_LIBERTAD,
     mini_r=DF[ag4._COL_APOYO].corr(DF[ag4._COL_LIBERTAD]),
     mini_hipotesis="___")
g4._scores.pop("intex1", None)
g4.check_intex1()
pts, mx = g4._scores["intex1"]
check("nb4 intex1 hipotesis placeholder -> pts < max", pts < mx)

# ── Reflexiones nb4 ─────────────────────────────────────────────
for rid, method in [("ronda6", "check_reflexion_ronda6"),
                     ("subgrupos", "check_reflexion_subgrupos"),
                     ("interpretacion", "check_reflexion_interpretacion"),
                     ("metodologica", "check_reflexion_metodologica")]:
    g4._scores.pop(f"refl_{rid}", None)
    g4._call_grade_reflexion = fake_grade_ok
    g4._grade_reflexion(rid, "Esta es una reflexion real de mas de quince caracteres.")
    pts, mx = g4._scores[f"refl_{rid}"]
    check(f"nb4 refl_{rid} con IA simulada -> 4/{mx}", pts == 4 and mx == 5)

# ── _CORE_MAX == suma de max_pts declarados ──────────────────────
declared_nb4 = 5 * 3 + 20 * 2 + 10 + 20 + 20 + 5 * 4 + 25
check(f"nb4 _CORE_MAX ({ag4._CORE_MAX}) == suma declarada ({declared_nb4})",
      ag4._CORE_MAX == declared_nb4)

# ── mini_b / mini_c / resumen no truenan ──────────────────────────
try:
    g4.check_mini_b()
    g4.check_mini_c()
    g4.resumen()
    check("nb4 checkpoints + resumen() no truenan", True)
except Exception as e:
    check(f"nb4 checkpoints/resumen() no truenan ({e})", False)


print()
print("=" * 70)
print(f"RESULTADO: {len(PASS)} pasaron, {len(FAIL)} fallaron")
print("=" * 70)
if FAIL:
    print("FALLOS:")
    for f in FAIL:
        print(f"  - {f}")
    sys.exit(1)
else:
    print("Todos los checks pasaron.")

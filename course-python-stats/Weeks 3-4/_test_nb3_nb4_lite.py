# -*- coding: utf-8 -*-
"""
_test_nb3_nb4_lite.py -- validacion ATLAS-style (throwaway, COURSE_TEMPLATE.md
SS3 pattern) de autograder_nb3_lite.py y autograder_nb4_lite.py.

Corre cada modulo en su PROPIO subproceso (no imports compartidos en un solo
script) porque ambos mutan in-place los globals NOTEBOOK_ID/_CORE_MAX de su
modulo base (autograder_nb3.py / autograder_nb4.py) -- ver la advertencia en
el docstring de autograder_nb3_lite.py. Cada bloque de abajo es un script
independiente ejecutado via `python -c`.
"""
import subprocess
import sys

FAILURES = []

def run(label, script):
    result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
    if result.returncode != 0:
        FAILURES.append(f"{label}: subprocess crashed\n{result.stderr}")
    else:
        print(f"[{label}] {result.stdout.strip()}")


# ═══════════════════════════════════════════════════════════════════════
# nb3_lite
# ═══════════════════════════════════════════════════════════════════════

run("nb3_lite / basic instantiation + _CORE_MAX", """
import autograder_nb3_lite as m
g = m.Autograder()
assert m._base.NOTEBOOK_ID == "nb3_lite", m._base.NOTEBOOK_ID
assert m._base._CORE_MAX == 70, m._base._CORE_MAX
print("OK NOTEBOOK_ID=nb3_lite _CORE_MAX=70")
""")

run("nb3_lite / t8 (Quiz de Cierre 1) overridden for 4 rounds, not 6", """
import autograder_nb3_lite as m
g = m.Autograder()
assert g._TEORIA[8]["correct"] == "b"
assert "Rondas 1 a 4" in g._TEORIA[8]["q"], g._TEORIA[8]["q"]
assert g._TEORIA[8]["q"] != m._base.Autograder._TEORIA[8]["q"], \
    "t8 must be overridden, not inherited (base version references Ronda 6, which doesn't exist here)"
g._grade_teoria(8, "b")
e, p = g._scores["t8"]
assert (e, p) == (5, 5), (e, p)
print("OK t8 overridden for lite (Rondas 1-4) -> 5/5")
""")

run("nb3_lite / t9-t11 (new-scenario quiz) inherited verbatim from base bank", """
import autograder_nb3_lite as m
g = m.Autograder()
for n in (9, 10, 11):
    assert m._base.Autograder._TEORIA[n]["q"] == g._TEORIA[n]["q"], n
    assert m._base.Autograder._TEORIA[n]["correct"] == g._TEORIA[n]["correct"], n
print("OK t9-t11 inherited unchanged from autograder_nb3.py")
""")

run("nb3_lite / t1 correct answer scores 5", """
import autograder_nb3_lite as m
g = m.Autograder()
g._grade_teoria(1, "b")
e, p = g._scores["t1"]
assert (e, p) == (5, 5), (e, p)
print("OK t1 correct -> 5/5")
""")

run("nb3_lite / t1 wrong answer scores 0, locked on retry", """
import autograder_nb3_lite as m
g = m.Autograder()
g._grade_teoria(1, "a")
e, p = g._scores["t1"]
assert (e, p) == (0, 5), (e, p)
g._grade_teoria(1, "b")  # segundo intento -- debe seguir bloqueado en 0
e2, p2 = g._scores["t1"]
assert (e2, p2) == (0, 5), "retry should not change score"
print("OK t1 wrong -> 0/5, locked")
""")

run("nb3_lite / all t1-t7 correct sums to 35 and unlocks cazador_patrones", """
import autograder_nb3_lite as m
g = m.Autograder()
correct = {1:"b", 2:"b", 3:"c", 4:"b", 5:"b", 6:"c", 7:"b"}
for n, letter in correct.items():
    g._grade_teoria(n, letter)
total = sum(e for k, (e, p) in g._scores.items() if k.startswith("t"))
assert total == 35, total
assert "cazador_patrones" in g._achievements, g._achievements
print(f"OK t1-t7 all correct -> {total}/35, cazador_patrones unlocked")
""")

run("nb3_lite / reflection: trivial text scores 0 without calling the network", """
import autograder_nb3_lite as m
g = m.Autograder()
g._grade_reflexion("ronda1", "___")
e, p = g._scores["refl_ronda1"]
assert (e, p) == (0, 5), (e, p)
print("OK trivial reflection text -> 0/5")
""")

run("nb3_lite / reflection: AI-unreachable path leaves key unset (retry-eligible)", """
import autograder_nb3_lite as m
g = m.Autograder()
g._call_grade_reflexion = lambda *a, **k: None  # simulate network failure
g._grade_reflexion("ronda1", "Una reflexion real de mas de quince caracteres.")
assert "refl_ronda1" not in g._scores, g._scores
print("OK AI-unreachable -> key stays unset, not a silent 0")
""")

run("nb3_lite / check_mini_a checkpoint renders without KeyError (no ex keys)", """
import autograder_nb3_lite as m
g = m.Autograder()
g._grade_teoria(1, "b")
g.check_mini_a()  # must not raise even with t2-t11 never answered
print("OK checkpoint renders with partial/no scores")
""")

run("nb3_lite / _CORE_MAX arithmetic matches declared sum of max_pts", """
import autograder_nb3_lite as m
declared = 5 * 11 + 5 * 3  # t1-11 (5 ea) + 3 reflexiones (5 ea)
assert declared == m._base._CORE_MAX, (declared, m._base._CORE_MAX)
print(f"OK declared max sum ({declared}) == _CORE_MAX ({m._base._CORE_MAX})")
""")


# ═══════════════════════════════════════════════════════════════════════
# nb4_lite
# ═══════════════════════════════════════════════════════════════════════

run("nb4_lite / basic instantiation + _CORE_MAX", """
import autograder_nb4_lite as m
g = m.Autograder()
assert m._base.NOTEBOOK_ID == "nb4_lite", m._base.NOTEBOOK_ID
assert m._base._CORE_MAX == 55, m._base._CORE_MAX
print("OK NOTEBOOK_ID=nb4_lite _CORE_MAX=55")
""")

run("nb4_lite / t11 (new debug MC) exists, correct='b', scores 5", """
import autograder_nb4_lite as m
g = m.Autograder()
assert 11 in g._TEORIA, "t11 missing from _TEORIA"
assert g._TEORIA[11]["correct"] == "b"
assert m.Autograder.check_debug1 is not m._base.Autograder.check_debug1, \
    "check_debug1 must be overridden, not inherited (base version validates code, not an MC)"
g._grade_teoria(11, "b")  # exercises the same path check_debug1() routes into
e, p = g._scores["t11"]
assert (e, p) == (5, 5), (e, p)
print("OK t11 debug-MC correct -> 5/5, check_debug1 confirmed overridden")
""")

run("nb4_lite / t8-10 inherited unchanged from base bank", """
import autograder_nb4_lite as m
g = m.Autograder()
assert m._base.Autograder._TEORIA[8]["title"] == g._TEORIA[8]["title"]
assert m._base.Autograder._TEORIA[10]["correct"] == g._TEORIA[10]["correct"]
print("OK t8/t10 inherited verbatim from autograder_nb4.py")
""")

run("nb4_lite / check_intex1: real new pair + real hypothesis scores full 15", r"""
import autograder_nb4_lite as m
import pandas as pd
g = m.Autograder()
df = pd.read_csv("2019_es.csv")
import builtins, __main__
__main__.df_felicidad = df
__main__.mini_var_x = "Libertad para tomar decisiones"
__main__.mini_var_y = "Generosidad"
__main__.mini_r = df["Libertad para tomar decisiones"].corr(df["Generosidad"])
__main__.mini_hipotesis = "Creo que paises con mas libertad reportan mas generosidad porque hay menos miedo a compartir."
g.check_intex1()
e, p = g._scores["intex1"]
assert (e, p) == (15, 15), (e, p)
print(f"OK intex1 valid new pair + real r + real hypothesis -> {e}/{p}")
""")

run("nb4_lite / check_intex1: rejects Puesto (circular column)", r"""
import autograder_nb4_lite as m
import pandas as pd, __main__
g = m.Autograder()
df = pd.read_csv("2019_es.csv")
__main__.df_felicidad = df
__main__.mini_var_x = "Puesto"
__main__.mini_var_y = "Generosidad"
__main__.mini_r = 0.5
__main__.mini_hipotesis = "hipotesis de relleno con mas de quince caracteres"
g.check_intex1()
e, p = g._scores["intex1"]
assert e < p, f"expected partial/zero credit, got {e}/{p}"
print(f"OK intex1 rejects Puesto -> {e}/{p} (not full credit)")
""")

run("nb4_lite / check_intex1: rejects already-used pair (PBI-Puntaje)", r"""
import autograder_nb4_lite as m
import pandas as pd, __main__
g = m.Autograder()
df = pd.read_csv("2019_es.csv")
__main__.df_felicidad = df
__main__.mini_var_x = "PBI per cápita"
__main__.mini_var_y = "Puntaje"
__main__.mini_r = df["PBI per cápita"].corr(df["Puntaje"])
__main__.mini_hipotesis = "hipotesis de relleno con mas de quince caracteres"
g.check_intex1()
e, p = g._scores["intex1"]
assert e < p, f"expected partial/zero credit for a reused pair, got {e}/{p}"
print(f"OK intex1 rejects already-used pair -> {e}/{p} (not full credit)")
""")

run("nb4_lite / check_intex1: rejects placeholder hypothesis", r"""
import autograder_nb4_lite as m
import pandas as pd, __main__
g = m.Autograder()
df = pd.read_csv("2019_es.csv")
__main__.df_felicidad = df
__main__.mini_var_x = "Libertad para tomar decisiones"
__main__.mini_var_y = "Generosidad"
__main__.mini_r = df["Libertad para tomar decisiones"].corr(df["Generosidad"])
__main__.mini_hipotesis = "___"
g.check_intex1()
e, p = g._scores["intex1"]
assert e < p, f"expected partial credit (pair ok, hypothesis rejected), got {e}/{p}"
print(f"OK intex1 rejects placeholder hypothesis -> {e}/{p} (not full credit)")
""")

run("nb4_lite / check_mini_b and check_mini_c render without KeyError", """
import autograder_nb4_lite as m
g = m.Autograder()
g.check_mini_b()  # no t8/t9/t11 answered yet
g.check_mini_c()  # no t10/intex1 answered yet
print("OK both checkpoints render with zero scores, no crash")
""")

run("nb4_lite / _CORE_MAX arithmetic matches declared sum of max_pts", """
import autograder_nb4_lite as m
declared = 15 + 5 + 20 + 15  # t8-10 + t11 + 4 reflections(5 ea) + intex1
assert declared == m._base._CORE_MAX, (declared, m._base._CORE_MAX)
print(f"OK declared max sum ({declared}) == _CORE_MAX ({m._base._CORE_MAX})")
""")


print()
if FAILURES:
    print(f"{len(FAILURES)} FAILURE(S):")
    for f in FAILURES:
        print("---")
        print(f)
    sys.exit(1)
else:
    print("ALL CHECKS PASSED")

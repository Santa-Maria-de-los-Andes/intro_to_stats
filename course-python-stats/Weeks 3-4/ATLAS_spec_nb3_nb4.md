# ATLAS Spec — `nb3` / `nb4` autograders

**From:** SOFIA. **For:** ATLAS. **Status:** notebooks built and validated 2026-08-20
(`build_nb3.py` → `nb3_correlacion.ipynb`, 49 cells / `nb4_correlacion.ipynb`,
46 cells). No autograder exists yet for either file — this spec is what to build against.
Companion context: `WORKFORCE_HANDOFF.md` ticket #14 and its 2026-08-20 Done log entry,
`WORKFORCE_CONTRACT.md` §2.

**Do not patch the old `autograder_nb3_semana3.py`** (still on disk under that name,
`_CORE_MAX=264`) — its `check_*` methods don't match this notebook's cells (different exercises,
different pairs in several slots, different numbering), and it predates this rename (the new
files are `nb3_correlacion.ipynb`/`nb4_correlacion.ipynb`, autograders should be
`autograder_nb3.py`/`autograder_nb4.py`). Write both new autograders fresh from this spec. The
old file's `_ask_teoria` /
`_ask_reflexion` / `_grade_reflexion` widget mechanisms (HTML form → JS →
`google.colab.kernel.invokeFunction`, and the reflection → `grade-reflexion` Supabase Edge
Function → DeepSeek pipeline) are still the right implementation pattern — reuse that machinery,
just re-wire it to the exercises below.

Dataset unchanged: `2019_es.csv` (World Happiness Report 2019, 156 rows × 10 cols, no nulls).
Columns: `Puesto`, `País o región`, `Continente`, `Puntaje`, `PBI per cápita`, `Apoyo social`,
`Esperanza de vida saludable`, `Libertad para tomar decisiones`, `Generosidad`,
`Percepción de corrupción`. `Continente` values: `Europa`(42), `Asia`(44), `África`(45),
`América`(23), `Oceanía`(2) — note Oceanía's n=2, referenced below.

All r-values below were computed directly against the real CSV on 2026-08-20 (not carried over
from the old build without re-checking) — use them as your correct-answer reference, tolerance
±0.001 on the rounded-to-3-decimals value.

---

## `nb3_correlacion.ipynb` — `_CORE_MAX` = 200 (was 130, see 2026-08-21 update below)

| Check | Cell ID(s) | Type | Expected variables | Correct value | Suggested pts |
|---|---|---|---|---|---|
| `check_t1`–`check_t5` | `nb3-t1..t5-check` | MC theory | `respuesta_tN` pattern | Content unchanged from old build (coefficient definition, -1↔1 range, direction vs. strength, linear-only caveat, causation caveat) — **reuse the existing question bank verbatim** from the old `autograder_nb3.py`'s `_ask_teoria`, this block of the notebook is byte-identical to before | 5 ea (25) |
| `check_t6` | `nb3-t6-check` | MC theory | `respuesta_t6` | Concept: why a real outlier (Catar) can make the eye doubt a pattern the number still confirms. Old `t6` tested the same concept in the same position (right after the guided demo/outlier note) — likely reusable as-is | 5 |
| `check_ex1` | `nb3-ronda1-code/check` | 🔨 build+calc | `x_ex1`, `y_ex1`, `r_ex1` | `Percepción de corrupción` vs `Puntaje` → **r ≈ 0.386** | 20 |
| `check_t7` | `nb3-t7-check` | MC theory | `respuesta_t7` | Concept: correlation isn't transitive — pairing with `Puntaje` twice doesn't tell you the two non-`Puntaje` variables correlate with each other. Placed right before Ronda 3, which is the first non-`Puntaje` pair | 5 |
| `check_ex2` | `nb3-ronda2-code/check` | 🔨 build+calc | `x_ex2`, `y_ex2`, `r_ex2` | `Esperanza de vida saludable` vs `Puntaje` → **r ≈ 0.780** | 20 |
| `check_ex3` | `nb3-ronda3-code/check` | 🔨 build+calc | `x_ex3`, `y_ex3`, `r_ex3` | `PBI per cápita` vs `Esperanza de vida saludable` → **r ≈ 0.835** (strongest pair in the whole unit) | 20 |
| `check_ex4` | `nb3-ronda4-code/check` | 🔨 build+calc | `x_ex4`, `y_ex4`, `r_ex4` | `Apoyo social` vs `Esperanza de vida saludable` → **r ≈ 0.719** | 20 |
| `check_ex5` *(new 2026-08-21)* | `nb3-ronda5-code/check` | 🔨 build+calc | `x_ex5`, `y_ex5`, `r_ex5` | `PBI per cápita` vs `Apoyo social` → **r ≈ 0.755** (second-strongest pair among the six variables, after ex3) | 20 |
| `check_ex6` *(new 2026-08-21)* | `nb3-ronda6-code/check` | 🔨 build+calc | `x_ex6`, `y_ex6`, `r_ex6` | `Generosidad` vs `Percepción de corrupción` → **r ≈ 0.327** (the one variable Generosidad actually correlates with — contrast with its near-zero r against every other variable) | 20 |
| `check_t8`–`check_t11` *(new 2026-08-21, "Quiz de Cierre")* | `nb3-t8..t11-check` | MC theory | `respuesta_tN` pattern | `t8`: recall which pair had today's highest r (ex3, PBI↔Esperanza). `t9`-`t11`: three brand-new scenarios (ice-cream/drowning, shoe-size/reading, random-pairs multiple-comparisons) that don't reference the happiness dataset at all — testing whether "correlation ≠ causation" transfers beyond this one dataset | 5 ea (20) |
| `check_mini_a` | `nb3-checkpoint` | checkpoint | — | gates on 80% of the above, no independent XP | 0 |

**⚠️ Numbering note (2026-08-21):** `check_ex5`/`check_ex6`/`check_t8`-`check_t11` in `autograder_nb3.py` are **local to this file** — they do **not** continue the "nb4 picks up numbering where nb3 ends" convention documented at the top of `build_nb3.py`/`build_nb4.py`. `autograder_nb4.py` already has its own `check_ex5`/`check_ex6`/`check_t8`-`check_t10` (different pairs, different questions, different class/file — see the nb4 table below). Since nb3 and nb4 are separate Python classes in separate files loaded into separate notebooks, there is **no runtime collision** — this is a naming coincidence between two independent notebooks, not a bug. It does mean a human comparing this spec's nb3 table against the nb4 table below will see `ex5`/`ex6`/`t8` used twice with different meanings; that's intentional and documented in both autograder files' docstrings. Nb4 itself was **not** renumbered to make room, since it's already built, validated, and live with students working toward its Aug 31 deadline — renumbering it now would risk breaking in-progress student notebooks that already call `grader.check_ex5()` etc. against the existing nb4 methods.

**Reflections (`check_reflexion_*`, 5 pts ea, 25 total)** — all via the DeepSeek pipeline, teacher-tone rubric should check for (a) actually answers the question asked, (b) avoids causal language ("causa", "provoca", "hace que" — non-negotiable per `Teoria_Semanas3-4_Mision2_Correlacion.md`'s language rule) where the prompt calls for it:

| `id` passed to `reflexion_check()` | Cell | What it's grading |
|---|---|---|
| `ronda1` | `nb3-ronda1-reflexiona-code` | Did their prediction match Ronda 1's actual scatter/`r`, in their own words |
| `ronda3` | `nb3-ronda3-reflexiona-code` | Reasoning for *why* PBI↔Esperanza is the strongest pair seen so far (not just restating the number) |
| `concepto` | `nb3-concepto-reflexiona-code` | Pure concept explanation, no dataset reference required — what `r` tells you and what it never tells you by itself. This is the "explain in your own words" concept-check the user asked for; grade on explanation quality, not on mentioning a specific pair |
| `pbi_apoyo` *(new 2026-08-21)* | `nb3-ronda5-reflexiona-code` | Whether the student identifies PBI as the common factor behind two strong-but-different relationships (ex3 and ex5), with a plausible reason (more resources → both health and social support), not just causal-language shorthand |
| `generosidad_corrupcion` *(new 2026-08-21)* | `nb3-ronda6-reflexiona-code` | Whether the student notices the contrast — Generosidad is near-zero with everything else, but not with this pair — and offers a plausible explanation (e.g. lower perceived corruption → more trust → more generosity), without overstating it as a strong relationship |

**Common-wrong-answer test cases to write** (per `COURSE_TEMPLATE.md` §6, all `check_exN` here):
hardcoded literal `r` value (should fail if dataset changes), swapped x/y columns (should still
pass — `.corr()` is symmetric, but `plt.xlabel`/`plt.ylabel` swapped should be checked separately
if you grade axis correctness), and the single most likely typo per pair (accented characters:
`cápita`, `Percepción`, `corrupción` — these already broke as `debug1`'s bug in Semana 4, so
students will mistype them here too).

---

## `nb4_correlacion.ipynb` — suggested `_CORE_MAX` ≈ 145

| Check | Cell ID(s) | Type | Expected variables | Correct value | Suggested pts |
|---|---|---|---|---|---|
| `check_t8` | `nb4-t8-check` | MC theory | `respuesta_t8` | Concept: before Ronda 5 — what does it mean for `Libertad` and `Percepción de corrupción` to be measuring genuinely different things even though both are "about institutions" | 5 |
| `check_ex5` | `nb4-ronda5-code/check` | 🔨 build+calc | `x_ex5`, `y_ex5`, `r_ex5` | `Libertad para tomar decisiones` vs `Percepción de corrupción` → **r ≈ 0.439** | 20 |
| `check_ex6` | `nb4-ronda6-code/check` | 🔨 build+calc | `x_ex6`, `y_ex6`, `r_ex6` | `PBI per cápita` vs `Generosidad` → **r ≈ -0.080** (practically null) | 20 |
| `check_t9` | `nb4-t9-check` | MC theory | `respuesta_t9` | Concept: interpreting an r near 0 correctly — "no relationship found" ≠ "no relationship exists," just none *linear* and *in this data* | 5 |
| `check_reflexion_ronda6` | `nb4-ronda6-reflexiona-code` | 💭 reflection | — | *(Missed in the first pass of this spec — the notebook does have a reflection here.)* Whether it's reasonable that money barely predicts generosity; grade on reasoning, not on agreeing with a specific answer | 5 |
| `check_debug1` | `nb4-debug1-code/check` | 🔧 debug | (fixes `df_felicidad['Punaje']` → `['Puntaje']`) | Should raise `KeyError` before fixing, nothing else after | 10 |
| `check_ex7` | `nb4-ex7-code/check` | 🔨 build | `correlaciones_puntaje` (Series, excl. `Puesto`/`Puntaje`), `columna_mas_fuerte`, `columna_mas_debil` | Strongest = `PBI per cápita` (0.794), weakest = `Generosidad` (0.076) | 20 |
| `check_mini_b` | `nb4-checkpoint-b` | checkpoint | — | gates on 80% of the above | 0 |
| `check_t10` | `nb4-t10-check` | MC theory | `respuesta_t10` | Concept: why Oceanía's r≈±1.0 on `n=2` is not a real finding — any 2 points always look perfectly correlated. **This is a sample-size caution, deliberately distinct from causation** (Week 5's territory) — don't let the question wording drift into causal language | 5 |
| `check_ex8` | `nb4-seccionc-ex8-code/check` | 🔨 build (boolean filter + `.corr()`, **not** `.groupby().apply()`) | `r_generosidad_europa`, `r_generosidad_america` | Europa ≈ **0.530**, América ≈ **-0.211** (overall Generosidad↔Puntaje r is ≈0.076 — the sign flip between these two subgroups *is* the finding) | 20 |
| `check_reflexion_subgrupos` | `nb4-seccionc-reflexiona-code` | 💭 reflection | — | Grade on whether they connect the Europa/América sign-flip to "don't trust the overall pattern without checking subgroups" — this is Sección C's single-sentence-caution payoff, not a causation discussion | 5 |
| `check_intex1` | `nb4-miniproyecto-code/check` | 🔨 **integration exercise** (own-choice pair) | `mini_var_x`, `mini_var_y` (column names, strings — validate both are real columns in `df_felicidad`, and reject `Puesto` since it's circular with `Puntaje`), `mini_r` (float), `mini_hipotesis` (string, non-trivial length — reject empty/placeholder text) | No single correct pair — validate structurally: `mini_r` must actually equal `df_felicidad[mini_var_x].corr(df_felicidad[mini_var_y])` to within rounding, and per **`Teoria_Semanas3-4_Mision2_Correlacion.md` §2 Sección D's explicit requirement**, consider rejecting/flagging pairs already used in a prior round (`Percepción de corrupción`–`Puntaje`, `Esperanza`–`Puntaje`, `Apoyo social`–`Puntaje`, `Libertad`–`Puntaje`, `Generosidad`–`Puntaje`, `PBI`–`Puntaje`, `PBI`–`Esperanza`, `Apoyo social`–`Esperanza`, `Libertad`–`Corrupción`, `PBI`–`Generosidad`) so students do genuine new exploration, not a copy of an earlier round | 25 |
| `check_reflexion_interpretacion` | `nb4-miniproyecto-reflexiona1-code` | 💭 reflection | — | Interpretation of their own `mini_r`, causal-language-free | 5 |
| `check_reflexion_metodologica` | `nb4-miniproyecto-reflexiona2-code` | 💭 reflection | — | **This is the GAUSS-required anti-spurious-correlation check** — grade on whether they articulate that scanning many pairs makes a high r likelier by chance alone (multiple-comparisons reasoning), not just "correlation isn't causation" restated | 5 |
| `check_mini_c` | `nb4-checkpoint-c` | checkpoint | — | gates on 80% of the above | 0 |

**Continuity requirement (not a `check_*`, but load-bearing):** whatever storage format
`check_intex1` ends up validating (`mini_var_x`/`mini_var_y`/`mini_r`/`mini_hipotesis`) is what
Week 5's causation-debunking session reuses as its input material, per
`Teoria_Semanas3-4_Mision2_Correlacion.md`'s explicit continuity note. Don't change the variable
names without telling whoever builds Week 5.

**PIXEL note (carried over from `04_GAUSS.md`'s risk flag, still applies):** don't frame
`check_intex1`/its achievement as "you win if you found the highest r" — that directly rewards
the p-hacking-adjacent habit `check_reflexion_metodologica` is trying to inoculate against.

---

## Totals

| File | `_CORE_MAX` |
|---|---|
| `nb3_correlacion.ipynb` | 200 *(was 130 — see 2026-08-21 update below)* |
| `nb4_correlacion.ipynb` | 150 |
| **Combined** | **350** |

Still above the nominal ~180 `WORKFORCE_CONTRACT.md` §2 figure, but down from the old single
file's 264 alone (with Semana 4 not even built yet at that point) — and the user's 2026-08-19
call stands: raw `_CORE_MAX` isn't cross-notebook comparable once scores normalize to 0-100% per
notebook, so this isn't being treated as a new budget problem.

---

## Update — 2026-08-21: nb3 expanded (Ronda 5/6 + Quiz de Cierre)

After reviewing the built notebook, the user judged `nb3_correlacion.ipynb` too short and asked
for: (1) at least 2 more scatter+`r` exercises, using variable combos not necessarily involving
`Puntaje`, each with its own AI-graded reflection; (2) a closing multiple-choice section that
both recalls today's data and tests transfer to scenarios outside the happiness dataset.

Added (all verified against `2019_es.csv` the same day, same discipline as the rest of this
spec): `check_ex5` (PBI per cápita vs Apoyo social, r≈0.755), `check_ex6` (Generosidad vs
Percepción de corrupción, r≈0.327 — the one variable Generosidad actually correlates with, in
contrast to its near-zero r against every other variable), reflections `pbi_apoyo` and
`generosidad_corrupcion` (5 pts ea), and a 4-question "Quiz de Cierre" (`check_t8`-`check_t11`,
5 pts ea): one data-recall question (which pair had today's highest r) and three brand-new
scenarios that never mention the dataset (ice-cream/drowning-rate confound, shoe-size/reading-
ability confound, random-pairs multiple-comparisons risk) — per the user's request for "more new
scenarios, less data-recall" when asked to weigh the mix.

`_CORE_MAX` for nb3 moved from 130 to 200 (55 t1-11 + 120 ex1-6 + 25 reflexion×5). Full detail
in `autograder_nb3.py`'s docstring and the numbering note above the nb3 reflections table.
`_test_nb3_nb4.py` was updated in step (new t8-11/ex5-6/reflection assertions, updated
`declared_nb3`) and re-run: 83/83 assertions pass. `nb4_correlacion.ipynb` / `autograder_nb4.py`
were **not** touched — see the numbering note above for why.

---

## Status: BUILT (2026-08-21)

Both autograders are written — `autograder_nb3.py` and `autograder_nb4.py` — matching the
point values in this spec exactly (the `check_reflexion_ronda6` gap noted above is now fixed in
the built file, wasn't fixed here until this pass). Validated via
`_test_nb3_nb4.py` (throwaway ATLAS-style script, `COURSE_TEMPLATE.md` §3 pattern): 63/63
assertions pass, covering for every `check_*` — correct solution passes, at least one common-wrong
or hardcoded-lazy case fails, per `03_ATLAS.md`'s "Must ALWAYS" test discipline. Specific cases
worth knowing about:
- `check_ex7` (explore-all): tested against the "included `Puesto`" trap specifically (circular
  correlation with `Puntaje`, ≈-0.99) — correctly rejected.
- `check_ex8` (Sección C): tested against the common mistake of using the *unfiltered* overall r
  instead of the per-continent filtered r — correctly rejected.
- `check_intex1` (mini-project): tested against three real failure modes — a pair already used in
  an earlier round (rejected), `Puesto` chosen as one of the two columns (rejected, circular), and
  a placeholder hypothesis string (rejected) — plus one genuinely new, valid pair (accepted, full
  points).
- Reflection grading: the "AI unreachable" path was tested explicitly — it does **not** record a
  score of 0, it leaves the key unset so the student can retry, matching the documented
  `_grade_reflexion` contract.
- `_CORE_MAX` arithmetic verified to equal the exact sum of declared `max_pts` across every
  non-bonus `check_*` call for both files (130 and 150) — this is the check `COURSE_TEMPLATE.md`
  §6 flags as silently breaking the level curve if it drifts.

The old `autograder_nb3_semana3.py` has been deleted (WORKFORCE_HANDOFF.md Done log, 2026-08-21)
now that both replacements are built and validated — nothing in the current notebooks references
it anymore.

# Workforce Handoff Tracker — SMA Intro Stats

**Owner:** SOFIA. Open tickets by owning agent, a Done log, accepted risks/scope cuts, and open
escalations. Edited in place; never forked into version-suffixed copies. Companion file:
`WORKFORCE_CONTRACT.md` (the interface every agent builds against).

---

## Open Tickets

| # | Ticket | Owner | Notes |
|---|---|---|---|

| 7 | Statistically vet Weeks 3–4, 6, 7 candidate datasets and Week 5 debunk material once SOFIA drafts them | GAUSS | **Weeks 3–4 now drafted 2026-08-14** (see Done log) — dataset not yet downloaded/vetted, this is the blocking half of the ticket for that unit now. Weeks 1–2 datasets vetted and approved 2026-08-05. Weeks 6, 7, and Week 5 debunk material still not drafted. |
| 8 | Draft statistically defensible model answers for the capstone's "descriptive analysis with interpretation" and "correlation analysis with causation critique" criteria (20 pts each) | GAUSS + ATLAS | Needed before ATLAS's Rubric Validation Report can sign off those two criteria as more than a point value. |
| 12 | Rewrite debug-cell hint comments so they prompt investigation ("read the error, identify the type") rather than naming the bug directly — currently several debug cells hand over the diagnosis in the comment, undercutting the "build error-reading skill" purpose of `check_debugN` (`COURSE_TEMPLATE.md` §4) | SOFIA | Raised in SOFIA's Mode 3 review 2026-08-05 (see Done log), still not fully applied. **Partial incidental progress 2026-08-11**: while renumbering Semana 2's debug cells (see that Done log entry), `debug0` (Seccion C, the `=` vs `==` bug, old `debug2`) had its hint de-scaffolded from naming the bug outright to "ejecuta, lee el mensaje completo, e identifica que tipo de error es" — a side effect of the renumbering pass, not a deliberate sweep. Semana 2's `debug1` (Seccion C, `and`/`or`, old `debug3`) and Semana 1's `debug1` still hand over the diagnosis; not touched. |

---

## Done Log

- 2026-08-24 — **`course-python-stats/nb3.html` built** (PIXEL, user-requested via
  `WORKFORCE/02_PIXEL.md`, same session as the `nb2.html` build below): public live leaderboard
  for `Weeks 3-4/autograder_nb3.py` (`curso="STAT_2026"`, `notebook="nb3"`), which had no public
  leaderboard page before this. Same clone-and-reskin approach as `reference/legacy-CS1/nb2.html`
  — `course-python-stats/nb2.html`'s engine unchanged, presentation reskinned to the palette/
  levels/achievements already locked *inside* `autograder_nb3.py` itself (`_LEVELS`, `_XP_GRAD`,
  `_LV_CSS_COLOR`, `_unlock()` achievement keys) — no new design decisions made, just read out of
  the grader. **Surfaced a real gap while doing this**: that theme ("En Busca de la Felicidad")
  was never run through PIXEL's Theme Architect process — ATLAS built it directly into the
  autograder on 2026-08-20/21 (see that date's entries below) while the module-level Theme Brief
  was still marked "not started" in `02_PIXEL.md`. Updated that file's Current Notebooks table to
  document the theme as shipped (so PIXEL has a source of truth to design *from* now) and flag
  the reconciliation question explicitly rather than leaving two stale-vs-real states in the doc.
  Also clarified in `README.md` that `course-python-stats/nb2.html` does **not** pair with `nb3`'s
  neighbor `nb2` — that filename actually serves `nb1_semana2` (see that file's own header
  comment) and real `nb2` lives in the other course entirely (`reference/legacy-CS1/nb2.html`,
  below) — easy to trip over when eyeballing the folder for "which notebook has no leaderboard
  yet." `CURSO_ID`/`NOTEBOOK_ID` cross-checked directly against the autograder's Supabase POST
  payload (module docstring: "mismo proyecto/tabla que nb1, curso=STAT_2026, notebook=nb3"), not
  assumed from the filename. Not validated against live Supabase data (no anon key access in this
  session) — structurally identical to the already-shipped `nb1.html`/legacy `nb2.html` pages.
- 2026-08-23 — **`reference/legacy-CS1/nb2.html` built** (PIXEL, user-requested via
  `WORKFORCE/02_PIXEL.md`): public live leaderboard for the prerequisite CS course's God of War
  notebook (`autograder_nb2.py`, `notebook_id="nb2"`), which had no public leaderboard page
  before this. Cloned `course-python-stats/nb2.html`'s engine (podium, live ticker, grade
  filter bar, 60s auto-refresh, `dedup()`-by-best-score, direct `submissions` query) verbatim
  and reskinned presentation only, using the palette/levels/achievements already documented in
  `02_PIXEL.md`'s "Established GoW Design Decisions" section — no new design decisions made.
  `CURSO_ID='CS_2026'`/`NOTEBOOK_ID='nb2'` match `autograder_nb2.py`'s actual POST payload
  (that script never sends a `curso` field, so its rows fall through to the `submissions`
  table's `DEFAULT 'CS_2026'` — confirmed against `supabase_schema.sql` before wiring the
  query, not assumed). Placed next to `autograder_nb2.py` rather than in `course-python-stats/`
  since this is the prerequisite CS course, not either statistics module — flagged for whoever
  next touches `reference/legacy-CS1/`'s README description, since that folder was previously
  documented as reference-only/not live. **Naming disambiguation, not yet a live conflict**:
  the Statistics module's `supabase_schema.sql` comments reserve `notebook_id='nb2'` for its own
  Tarea 2 (Correlación), but that content was actually built under `nb3`/`nb4` (Weeks 3-4 Done
  log, 2026-08-14 and 2026-08-20 entries) — so this CS `nb2` and the Stats module's reserved-
  but-unused `nb2` id aren't actually colliding in practice today, and the `curso` filter
  (`CS_2026` vs `STAT_2026`) would prevent a collision even if something did claim it later.
  Not validated against live Supabase data (no anon key access in this session) — structurally
  identical to the already-shipped `nb1.html`/`nb2.html` (stats) pages, same query pattern,
  same RLS assumptions.
- 2026-08-21 — **Weeks 3–4 "ruta de interpretación" built** (SOFIA, user-requested): a
  parallel track for two inclusion students who struggle with writing code but test
  strong on interpretation — `build_nb3_lite.py`/`build_nb4_lite.py` generate
  `nb3_lite_correlacion.ipynb` (43 cells) / `nb4_lite_correlacion.ipynb` (42 cells), graded
  by new `autograder_nb3_lite.py`/`autograder_nb4_lite.py`.
  **Design, not dilution**: per §1's own "statistical thinking first, code as the tool"
  philosophy, and confirmed directly against `autograder_nb3.py`'s `_TEORIA` dict before
  building — the 10 theory MCs and 7 AI-graded reflection prompts across nb3/nb4 never
  depended on writing pandas in the first place. Reused **verbatim, zero rewrite**: the
  dataset, every real r-value, every graph, all 10 theory questions (`t1`–`t10`, wording
  unchanged), all 7 reflection prompts, the Apertura hook, the narrative/theme/registration
  screen (no visible "lite" framing anywhere a student sees — deliberate, avoids a
  visibly-lower-tier signal). What changed: every `🔨 CONSTRUYE` round (`ex1`–`ex4` nb3,
  `ex5`–`ex8` nb4) becomes a pre-filled `👀 OBSERVA` cell — same reference solution code,
  same real output, run instead of written. `debug1` becomes a new theory-bank entry (`t11`)
  — the same broken cell still executes and raises the real `KeyError`, but the student
  answers a multiple-choice "what kind of error is this" instead of typing a fix. The
  own-choice mini-project (`intex1`) becomes `🧩 COMPLETA`: the student fills in
  `mini_var_x`/`mini_var_y`/`mini_hipotesis` from the printed correlation matrix, with the
  `.corr()` line already written in the cell — same validation (real column, not `Puesto`,
  not an already-used pair, non-trivial hypothesis) reused from `autograder_nb4.py`'s
  helpers, just no longer gated on the student authoring the calculation.
  **Engineering approach**: both lite autograders *subclass* the main ones
  (`class Autograder(autograder_nb3.Autograder)`) rather than duplicating the
  theory-widget/DeepSeek-reflection/gamification/Supabase engine — confirmed by reading
  `_ask_teoria`/`_grade_teoria`/`_ask_reflexion`/`_render_checkpoint` that they resolve
  `self._TEORIA` and `.get(key, default)` safely, so overriding only `_TEORIA` (to add
  `t11`), `check_debug1`, `check_intex1`, the checkpoint methods, and `_check_achievements`
  (retargeted to theory/reflection completion, same achievement keys as the base classes
  so `resumen()`'s label table needed no changes) was sufficient — no method that stays
  inherited references a check key (`ex1`, `debug1`-original, etc.) that no longer exists.
  **`NOTEBOOK_ID`/`_CORE_MAX` are reassigned on the imported base module**
  (`autograder_nb3.NOTEBOOK_ID = "nb3_lite"`, not a local variable) because every inherited
  method resolves those names against its own module's `__globals__`, not the subclass's —
  documented in-file as a docstring warning since it has one real consequence: importing
  `autograder_nb3_lite` mutates the shared `autograder_nb3` module object for the rest of
  that Python process. Harmless in production (each Colab notebook is its own fresh
  kernel, never imports both), but real for anyone writing a combined test script.
  Distinct notebook ids (`nb3_lite`/`nb4_lite`) so these two students' submissions land in
  the same Supabase `submissions` table without mixing into the main leaderboard's
  percentage comparison.
  **Scoring**: `_CORE_MAX` = 50 (nb3_lite: 35 theory + 15 reflection) / 55 (nb4_lite: 15
  theory t8–t10 + 5 t11 + 20 reflection ×4 + 15 redesigned `intex1`) — theory/reflection
  only, no `ex`/`debug`/`intex`-as-code points, both scaled 0–100% like every other
  notebook so the lighter absolute total doesn't read as "worth less."
  **Validated**: both build scripts regenerate clean; `py_compile` clean on both
  autograders; new `_test_nb3_nb4_lite.py` (throwaway, `COURSE_TEMPLATE.md` §3 pattern,
  each module tested in its own subprocess per the mutation caveat above) — 22/22
  assertions pass: correct/wrong theory answers score right and lock on retry, all-`t`
  achievement unlocks, trivial reflection text scores 0 without a network call, an
  AI-unreachable reflection leaves the key unset rather than recording a 0 (matching the
  inherited `_grade_reflexion` contract), both checkpoints render with zero/partial scores
  without a `KeyError`, and `check_intex1` (redesigned) accepts a genuine new pair with a
  real hypothesis for full 15/15 while separately rejecting `Puesto`, an already-used pair,
  and a placeholder hypothesis (each a partial-credit case, not a crash). The one new,
  not-copied code snippet (nb4_lite's `ex7`-equivalent explore-all cell, `.corr()` +
  `.drop(['Puesto','Puntaje'])` + `.abs().idxmax()/.idxmin()`) was independently re-run
  against `2019_es.csv` and confirmed to reproduce `PBI per cápita` (0.794) strongest /
  `Generosidad` (0.076) weakest, matching the already-vetted values. Every
  `grader.check_*()`/`grader.resumen()` call referenced in both generated notebooks was
  cross-checked against the corresponding lite `Autograder` class to confirm the method
  actually exists (catches a cell-vs-grader typo class of bug before a student ever hits it).
  **Open, by explicit default (not yet confirmed by the user)**: (1) no `nb3_lite.html`/
  `nb4_lite.html` public leaderboard page built — submissions land in Supabase and should
  already surface in the existing all-notebooks `dashboard.html`, but there's no
  student-facing page for this notebook id yet; (2) whether a formal CNB
  differentiation/accommodation record is needed for these two students — not drafted;
  (3) none of these files have been pushed to `main`, so the notebooks' `!wget` setup
  cells won't resolve yet — pushing is what actually ships this to students, same as any
  other notebook per `COURSE_TEMPLATE.md` §1.
- 2026-08-21 — **`autograder_nb3.py` and `autograder_nb4.py` built (ATLAS), closing ticket #14.**
  Full rewrite against `ATLAS_spec_nb3_nb4.md`, not a patch of the deleted
  `autograder_nb3_semana3.py`. `_CORE_MAX` = 130 (nb3) / 150 (nb4), both confirmed by direct
  arithmetic to equal the exact sum of declared `max_pts` across every non-bonus `check_*` — the
  150 corrects a gap in the spec doc itself (a `check_reflexion_ronda6` row was missing from the
  nb4 table, undercounting it as 145).
  **Validated** via new `_test_nb3_nb4.py` (throwaway ATLAS-style script, `COURSE_TEMPLATE.md` §3
  pattern): 63/63 assertions pass. Per-check, at least (1) correct solution passes and (2) a
  common-wrong or hardcoded/lazy case fails (`03_ATLAS.md` "Must ALWAYS"), plus targeted cases:
  `check_ex7`'s `Puesto`-included circular-correlation trap rejected; `check_ex8`'s "used the
  unfiltered overall r instead of the per-continent filtered r" mistake rejected; `check_intex1`
  (mini-project) rejects an already-used pair, rejects `Puesto`, and rejects a placeholder
  hypothesis, while accepting a genuine new pair for full points; reflection grading's "AI
  unreachable" path confirmed to leave the score key unset (retry-eligible) rather than recording
  a 0, matching the documented `_grade_reflexion` contract.
  Old `autograder_nb3_semana3.py` (`_CORE_MAX=264`, stale since the 2026-08-20 restructure)
  **deleted** — nothing in either current notebook's setup cell references it anymore (both wget
  the new `autograder_nb3.py`/`autograder_nb4.py`), and its replacements are now built and tested.
- 2026-08-20 — **`nb3_semana3_correlacion.ipynb` restructured and split into two files,
  `nb3_semana3_correlacion.ipynb` (49 cells) + new `nb3_semana4_correlacion.ipynb` (46 cells),
  both generated by revised `Weeks 3-4/build_nb3.py`** — resolves **ticket #13** (the 264-pt
  overage flagged 2026-08-18). Root cause identified through direct user conversation about
  actual classroom delivery: the plan was 40-50 min lecture + 1-1.5h homework for what was still
  labeled "Clase 1," and at that size the real bottleneck wasn't exercise difficulty (graph +
  `.corr()` exercises are column-name substitution, fast) but the 11 💭 Reflexiona cells, each a
  real round-trip to the `grade-reflexion` Supabase Edge Function (DeepSeek) — 5-8 min each
  including wait time, unsupervised. Fix, per explicit user direction: (1) **fuse graph-building
  and `.corr()`-calculation into one exercise per round** (previously two separate exercises,
  Sección A then Sección B, split across the file) so the coefficient's math backing lands the
  same session as the visual, never a week later; (2) **cut Reflexiona cells from 11 to 6**,
  reflecting only "occasionally" (every other round) rather than after every exercise — repetition
  itself is preserved (still 6 full graph+`.corr()` rounds across the two files, same pairs as the
  old build, same verified r-values); (3) **Sección C (`.groupby()` + subgroups) and the
  Semana 4 mini-project — spec'd in `Teoria_Semanas3-4_Mision2_Correlacion.md` in 2026-08-14 but
  never actually built — now exist**, giving Semana 4 real content instead of overflow homework
  from Semana 3.
  **Technical scope note:** Sección C does *not* use `.groupby().apply(lambda...)` — that pattern
  isn't in the committed technical spine (`WORKFORCE_CONTRACT.md` §5 lists `.groupby()` but not
  `.apply()`/lambda). Per-continent correlation instead uses boolean filtering (already taught,
  Weeks 1-2) + `.corr()` on the filtered subset — zero new syntax, same "code is never a syntax
  drill" principle (`COURSE_TEMPLATE.md` §4). `.groupby()` itself still appears, for a plain
  `.mean()` aggregation that sets up the "our dataset has subgroups" framing before the filtering
  approach takes over for the actual per-group `r`.
  **Mini-project** (Semana 4 close, `check_intex1`) implements both non-negotiable requirements
  `04_GAUSS.md`/the Teoria doc flagged for this exercise: a required hypothesis field
  (`mini_hipotesis`, not just the highest r), and a dedicated reflection asking why exploring many
  column pairs means the single highest-r pair shouldn't be trusted automatically (the
  spurious-correlation/multiple-comparisons risk GAUSS named for this exact exercise shape).
  Output format (`mini_var_x`/`mini_var_y`/`mini_r`/`mini_hipotesis`) is deliberately the reusable
  shape Semana 5 needs as its debunking input, per the Teoria doc's explicit continuity
  requirement — not something Semana 5's design has to re-derive.
  **Validated:** every exercise's reference solution (all six graph+`.corr()` rounds, the
  explore-all scan, the Sección C per-continent filters including the Oceanía n=2 case, `debug1`'s
  broken/fixed forms) re-run directly against `2019_es.csv` 2026-08-20 — all values in the
  notebook text match computed output to 3 decimals (script + raw output kept in this session's
  scratchpad, not committed). New real findings surfaced by this validation, not fabricated:
  `Percepción de corrupción` vs `Puntaje` r≈0.386 (not previously stated in prose); PBI↔Puntaje by
  continente (Europa 0.808, Asia 0.727, América 0.696, África 0.486, Oceanía -1.000 on n=2);
  Generosidad↔Puntaje by continente (Europa 0.530, Asia 0.042, África -0.183, América -0.211,
  Oceanía -1.000 on n=2) — the sign flip between Europa and América on a pair whose *overall* r is
  ≈0 is the real, non-manufactured finding Sección C's exercise is built around.
  **Net effect on reflection load**: 11 → 6 Reflexiona cells across the unit (was all 11 crammed
  into one file); full spec for ATLAS in `course-python-stats/Weeks 3-4/ATLAS_spec_nb3_semana3-4.md`
  (ticket #14). Old `autograder_nb3_semana3.py` (`_CORE_MAX=264`) is now stale and not deleted —
  ATLAS rebuilds both autograders from the spec, not by patching it.
- 2026-08-18 — **`nb3_semana3_correlacion.ipynb` revised per direct user review** (two
  concrete pieces of feedback after reading the generated notebook). (1) **Apertura
  "revelación" cell rewritten for clarity/replicability**: it previously computed each
  r via `pares_apertura[i][0]/[1]` tuple-indexing — technically correct but opaque as a
  pattern to copy, and the user flagged it as "confusing." Replaced with three direct,
  named lines (`r_diagrama1 = df_felicidad['Libertad para tomar decisiones'].corr(...)`,
  etc.) — the first place in the notebook where the full `df[col_x].corr(df[col_y])`
  pattern is visible as plain, copyable code, foreshadowing Sección B's own guided
  example instead of only resembling it. (2) **Four new exercise rounds added after
  Ejercicio 4** (`check_ex5`–`check_ex8`, "Ronda 3"–"Ronda 6"), per direct user request:
  *"at least 4 more exercises following the same pattern... not only with puntaje but
  PBI vs expectativa de vida etc... accompanied by some previous multiple choice
  questions and some post-calculation multiple choice to check understanding."* Each
  round combines the scatter-building and `.corr()`-calculating steps into one exercise
  (Ejercicios 1–4 taught them separately; by Ronda 3 the student has both skills), uses
  a pair that does **not** include `Puntaje` (deliberately, so the lesson is "correlation
  strength is a property of the pair, not of a variable" — otherwise a student could
  wrongly generalize "everything is ~r=0.78" from Ejercicios 1–4 all being vs. `Puntaje`),
  and is bracketed by a pre-question theory MC (`check_t7`/`t9`/`t11`/`t13` — tests a
  *concept* before the number is known, e.g. correlation's non-transitivity, not a guess
  at the unrevealed value) and a post-question theory MC (`check_t8`/`t10`/`t12`/`t14` —
  interprets the actual r the student just computed, non-causal language enforced same
  as every other interpretation prompt in this file). Pairs and real r (computed directly
  against `2019_es.csv`, not estimated): PBI per cápita↔Esperanza de vida saludable
  r≈0.8355 (the single strongest pair in the whole dataset, stronger than either
  variable's own relationship with `Puntaje`); Apoyo social↔Esperanza de vida saludable
  r≈0.7190; Libertad para tomar decisiones↔Percepción de corrupción r≈0.4388 (moderate,
  a deliberate step down from the two strong pairs above); PBI per cápita↔Generosidad
  r≈-0.0797 (near-zero, teaches that a negative sign this close to 0 isn't informative).
  The pre-existing "explore all correlations" exercise was renumbered `check_ex5` →
  `check_ex9` to free up the 5–8 range (safe per this file's standing renumbering
  precedent — no real student submissions yet, deadline still 2026-08-31). `_CORE_MAX`
  rose from 109 to **209** (25 t1–5 + 30 ex1/ex2 + 5 t6 + 24 ex3/ex4 + 40 t7–14 + 60
  ex5–8 + 15 ex9 + 10 debug1) — opened as **ticket #13** since this is well past the
  ~180 XP `WORKFORCE_CONTRACT.md` §2 budget for Weeks 3–4 combined, and Semana 4 isn't
  built yet; not walked back since the expansion was an explicit, additive user request.
  Achievement logic updated to match: `explorador_completo` now keys off `ex9` (was
  `ex5`), and a new achievement `cartografo_patrones` (🗺️ Cartógrafo de Patrones) added
  for a perfect `ex5`–`ex8`. Validated: `py_compile` clean; a scratch smoke-test
  (`_test_nb3.py`, not committed) called `_grade_teoria`/`check_exN` directly against
  real CSV-derived values for every new `t7`–`t14` and `ex5`–`ex9` — correct-answer and
  wrong-answer paths both score as expected, a full happy-path run across every
  `check_*` (t1–14, ex1–9, debug1) sums to exactly `_CORE_MAX` (209/209), and the
  renumbered `ex9` still grades correctly under its new name. `build_nb3.py` re-run
  clean (96 cells, up from 62); the Apertura reveal and all four new rounds' reference
  solutions re-executed against the real CSV in headless (`Agg`) matplotlib, matching
  the r values above to 3 decimals.
- 2026-08-14 — **`nb3_semana3_correlacion.ipynb` expanded for repetition**, same-day
  follow-up to the build below, per direct user feedback: *"we need more repetition to
  actually solidify the concepts, some reps + interpretation open ended questions right
  after."* Both Sección A and Sección B previously worked only one student pair
  (`Percepción de corrupción`); each now repeats the guided→predict→build/calculate
  pattern **twice** — Ronda 1 unchanged (`Percepción de corrupción`), Ronda 2 new
  (`Esperanza de vida saludable`, r≈0.780 vs. `Puntaje` — confirmed against the real CSV,
  see arithmetic below), on top of the pre-existing guided `Apoyo social` example
  (r≈0.777). Every round now ends in its own short 💭 REFLEXIONA cell immediately after
  that round's result, replacing the old pattern of one long reflection saved for the end
  of each section — mirrors the guided-example→exercise→compare rhythm
  `nb1_semana2_recuperacion_datos.ipynb`'s Secciones C/D already use for the same reason.
  New interpretation prompts (all ungraded/contract-exempt per `WORKFORCE_CONTRACT.md`
  §3, none use causal language): after the guided `r_apoyo_social` (interpret the number
  in plain language); after new `check_ex3`'s `r_corrupcion` (prediction-vs-reality +
  plain-language meaning); after new `check_ex4`'s `r_esperanza` (prompts the student to
  notice `r_apoyo_social` and `r_esperanza` are almost identical in strength, 0.777 vs.
  0.780 — confirmed real, not a coincidence dressed up for the exercise — despite being
  unrelated variables, and asks them to reason about why); after `check_ex5` (explore-all,
  now renumbered from `check_ex3`, asks which of the six columns' r surprised them most).
  **Renumbering** (safe now for the same reason as every prior renumbering pass in this
  file — no `autograder_nb3_semana3.py` exists yet): `check_ex1`/`check_ex2` are now both
  Sección A scatter-building exercises (`ex2` new, mirrors `ex1`'s spec shape —
  `x_ex2`/`y_ex2`); `check_ex3`/`check_ex4` are now both Sección B correlation-calculating
  exercises (`ex4` new, `r_esperanza`); the old explore-all `check_ex3` is now `check_ex5`;
  `check_debug1` unchanged. Suggested points: `ex1`/`ex2` 15 each, `ex3`/`ex4` 12 each,
  `ex5` 15, `debug1` 10 (79 total ex/debug, up from 52) + `t1`–`t6` theory (unchanged, 6
  questions) — still comfortably under the ~180 §2 budget with Semana 4 (Sección C +
  Integración) still to come. Validated: re-ran every non-stub solution (`ex1`/`ex2`'s
  scatter data, `ex3`/`ex4`'s `.corr()` calls, `ex5`'s full scan, `debug1`'s broken/fixed
  forms) against the real CSV — all match the values already vetted in the build entry
  below; the "`r_apoyo_social` ≈ `r_esperanza`" claim the new reflection prompt makes was
  itself checked (difference ≈0.003) before being written into the notebook, not asserted
  on assumption.
- 2026-08-14 — **`nb3_semana3_correlacion.ipynb` built** (Weeks 3–4, Semana 3 / Clase 1
  only — Apertura + Teoría Desbloqueada + Sección A + Sección B, per the Semana 3/Semana 4
  split proposed the same day in `Teoria_Semanas3-4_Mision2_Correlacion.md` §5), via new
  `course-python-stats/Weeks 3-4/build_nb3.py` (mirrors `build_nb1.py`'s structure —
  `md()`/`code()`/`teoria_check()` helpers, same icon legend). **Naming note (user
  override, explicit and confirmed via direct question):** filed as `nb3` per the user's
  literal request, which **contradicts** the convention already recorded lower in this
  file (2026-08-07 entries) and in `supabase_schema.sql`'s comments — `nb2` = Tarea 2 =
  Correlación, `nb3` reserved for Regresión/Clustering (Weeks 6–7). User was shown this
  conflict directly and chose `nb3` anyway. **Consequence for whoever builds the real
  Regresión/Clustering notebook later: that file cannot also be called `nb3`** without a
  Supabase `notebook_id` collision against this one — needs a different id (or this file
  needs renaming first) before that build happens. Flagging as unticketed since it's a
  one-line naming call, not open work, but real enough to trip someone up later.
  Dataset: `2019_es.csv` (World Happiness Report 2019, 156 rows × 10 cols, **zero missing
  values** — confirmed by direct load, not assumed) — this is the dataset ticket #7
  flagged as not-yet-downloaded for Weeks 3–4; downloading it and computing every number
  in the notebook against it (below) covers the download/compute half of that ticket, but
  **does not close ticket #7** — GAUSS's formal statistical vetting/sign-off is still
  outstanding, this was SOFIA building directly against real data, not a GAUSS review.
  All r values computed directly against the CSV (not estimated): Apertura's three hidden
  scatter pairs — Libertad↔Puntaje r≈0.567, Generosidad↔Puntaje r≈0.076, PBI per
  cápita↔Puntaje r≈0.794 (deliberately shows one strong + one weak/null pair, both real,
  per the theory doc's own requirement for this section); Sección A/B's worked pair, Apoyo
  social↔Puntaje r≈0.777; Ejercicio 1/2's student pair, Percepción de
  corrupción↔Puntaje r≈0.386; Ejercicio 3 (`.corr()` against all numeric columns at once)
  confirms PBI per cápita is the strongest real driver (r≈0.794) and Generosidad the
  weakest (r≈0.076) — deliberately excludes `Puesto` from that ranking since it's the
  rank *derived from* `Puntaje` (r≈-0.989, a circular definition, not a finding), a
  dataset-honesty point folded into the exercise instructions rather than left as a trap.
  Debug 1's `KeyError` (`'Punaje'` typo) confirmed to raise and nothing else. No
  `check_causa`/causal language anywhere per the theory doc's non-negotiable rule; the two
  💭 REFLEXIONA cells (Sección A: prediction-vs-reality; Sección B: GDP↔happiness
  correlation-vs-causation prompt) are ungraded/contract-exempt per
  `WORKFORCE_CONTRACT.md` §3, same as Semanas 1–2's pattern. Exercise-variable specs
  (`x_ex1`/`y_ex1`, `r_corrupcion`, `correlaciones_puntaje`/`columna_mas_fuerte`/
  `columna_mas_debil`) documented in-notebook for ATLAS the same way Semanas 1–2 did —
  **no autograder exists yet** (`autograder_nb3_semana3.py`, referenced but not published
  in the setup cell, same pattern as Semana 2's `nb1_semana2` setup cell before its
  grader was written). Numbering restarts at 1 (`check_ex1`, `check_t1`, `check_debug1`)
  — first class of a new mission, not a continuation of Mission 1's numbering. Validated:
  every non-stub/non-grader cell (Apertura hidden+reveal scatters, Sección A guided
  scatter, Sección B guided `.corr()`, all three exercise solutions, the debug cell's
  broken and fixed forms) executed clean against the real CSV with `matplotlib` in
  headless (`Agg`) mode; debug cell confirmed to raise `KeyError` and nothing else.
  Sección C (`.groupby()` + `.corr()`) and the Semana 4 Integración/mini-proyecto are
  **out of scope for this file** — a separate notebook, not yet built.
- 2026-08-14 — **SOFIA drafted the Weeks 3–4 guiding theory doc**
  (`course-python-stats/Weeks 3-4/Teoria_Semanas3-4_Mision2_Correlacion.md`), same role in the
  build order as `Teoria_Semanas1-2_Mision1_RecuperacionDeDatos.md` played for Weeks 1–2 — fixes
  the pedagogical sequence and formal theory content before GAUSS vets a dataset or PIXEL themes
  it. Follows the four-step order already fixed in
  `Bimestre3_Statistics_Python_Module_Guide.md` (scatter w/o code → correlation coefficient
  conceptually → `.corr()` in code → `.groupby()` by subgroup), mapped to Sections A–D +
  Semana 4 Integración/Mini-Proyecto, mirroring Semanas 1–2's letter-section pattern. Dataset:
  World Happiness Report (primary candidate), per the reservation already made in this file's
  2026-08-05 entry — **no real values pulled yet**, every number in the doc is a placeholder
  pending GAUSS (reopens the Weeks 3–4 half of ticket #7, see updated ticket text). Bakes in two
  guardrails directly from `04_GAUSS.md`'s per-week risk table: (1) the mini-project's "find two
  strongly correlated variables" instructions now require a stated hypothesis and a reflection
  question about why the highest-r pair alone isn't trustworthy, addressing the flagged
  spurious-correlation trap; (2) a non-negotiable no-causal-language rule stated up front,
  since this unit is designed to let students *feel* a causal pattern (GDP↔happiness) that
  Week 5 then interrogates — Section C's subgroup finding gets the same single-sentence-only
  caveat discipline Semanas 1–2 Section D used, no early spend of Week 5's protected depth.
  Flags an explicit continuity requirement for whoever designs Week 5: the Semana 4 mini-project
  write-up (variable pair, r, hypothesis) is Week 5's input material per the module guide's own
  wording, not something to re-derive. Also flags: the ice-cream/drownings example is reserved
  for Week 5's opening and must not be reused in this unit's hook. Proposed (not final) XP split
  totaling ~170 of the ~180 `WORKFORCE_CONTRACT.md` §2 budget, and a proposed Semana 3/4 file
  split mirroring Semanas 1–2's two-notebook pattern — explicitly flagged as pending real class
  schedule confirmation before locking, same caution Semanas 1–2 needed before its own split was
  finalized.
- 2026-08-11 — **`autograder_nb1_semana2.py` written, closing ticket #10 and resolving
  ticket #11 for Semana 2.** Juegos Olímpicos theme (user-directed, sports/Olympics per the
  Semana 1→Semana 2 Pokémon→Olympics arc): dark navy background (same house palette as
  `autograder_nb1_semana1.py`) with Olympic gold/blue/red accents, 6 levels Novato en la
  Villa Olímpica → Récord Olímpico, achievement rarities renamed to Bronce/Plata/Oro/Récord
  medal tiers, same visual engine (registration form, XP card, level-up banner, checkpoint
  summary, Supabase submit) reskinned rather than rebuilt — presentation-only changes, no
  change to the underlying grading engine's structure. Covers `check_ex0`–`ex6` (77 pts),
  `check_debug0`–`3` (40 pts: SyntaxError, ValueError, KeyError, AttributeError — one each,
  confirmed by inspection of the buggy code against real pandas behavior), `check_t0`–`t4`
  (25 pts, interactive HTML multiple-choice, same click→`invokeFunction`→`_grade_teoria`
  pipeline as Semana 1; question text pulled verbatim from `Preguntas_Teoricas_Semanas1-2.md`
  Bloque 5 — `t0`/`t1`/`t4` reuse `t10`/`t11`/`t12`, `t2`/`t3` are the new ones), `check_intex0`–`4`
  (35 pts; `intex3` is its own opinion-multiple item with a dedicated
  `_ag_intex3_answer` callback since it's anchored to the student's own `intex1` result, not
  a bank question), `check_reto1` (bonus, `_BONUS_MAX=10`, graded on effort/non-triviality of
  the free-text `hallazgo_reto1` since the exercise is genuinely open-ended), `check_mini_c`/
  `mini_d` checkpoints, `resumen()`. `_CORE_MAX=177` (77+40+35+25 — resolves ticket #11 for
  this file; see that ticket's former text, now folded in here). `NOTEBOOK_ID="nb1_semana2"`
  in the Supabase payload (distinct from Semana 1's `"nb1_semana1"`) so the registration
  form's "best prior score" lookup doesn't conflate the two sessions.
  **Expected values for every numeric check computed directly against the real
  `athlete_events_es.csv`** (271116 rows × 15 cols), not estimated — e.g. `Altura`
  mean/median/std ≈175.339/175.0/10.518; `Edad>25` n=110801; `Natacion` n=23195;
  `Edad>25 & Baloncesto` n=1938; `peso_por_deporte`/`altura_por_deporte_mujeres`/
  `desviacion_altura_por_deporte` per-deporte values for the real top-5 (`Atletismo`,
  `Gimnasia`, `Natacion`, `Tiro`, `Ciclismo`); `Sexo=='F'` n=74522; `CON=='PER'` n=532 across
  26 deportes; the notebook's own claims about Yao Ming (226cm, Baloncesto) and Rosario
  Briones (127cm, Gimnasia) confirmed present in the data. Two ATLAS spec-validation calls
  worth flagging: (1) `check_intex1`'s `diferencia_edad_basket_gimnasia` accepts either sign
  (`abs()` compared to the expected magnitude) since the exercise text ("resta ambos
  promedios") doesn't fix subtraction order, and rejecting a correctly-computed reversed-sign
  answer would be a false negative per this agent's own "don't reject a correct answer over
  spec ambiguity" constraint; (2) `_DEADLINE_UTC` is set to 2026-08-24 04:59 UTC, one week
  after Semana 1's, as a placeholder assuming weekly class cadence — not a confirmed Clase 2
  date, flagged in the file's own docstring for whoever schedules the actual class.
  Validated: `py_compile` clean; smoke-tested every `check_*` two ways — (a) full happy path
  with every variable set to the real correct-solution value, confirming the sum of all core
  checks equals `_CORE_MAX` exactly (177/177) and the bonus check awards 10/10; (b) every
  check individually fed `None`, wrong types, hardcoded/lazy constants, a plausible-but-wrong
  Series missing a category, and a reversed filter (men instead of women) — all correctly
  score 0, including a partial-credit case (`ex3` with a non-integer `cantidad_c3` still
  scores 8/12 for the two checks that do pass, not a false full-credit or false zero). Test
  scaffolding was scratch-only (`_test_semana2.py`, `_compute_expected*.py`), removed after
  the run — not committed.
- 2026-08-11 — **Semana 2 (`nb1_semana2_recuperacion_datos.ipynb`) restructured into a
  standalone tarea per user request**, decoupled from Semana 1 rather than continuing its
  mission/numbering. Changes, via `build_nb1.py`: (1) **`df_games`/`vgsales_es.csv` removed
  entirely** — the setup cell no longer downloads or loads it, and Integracion (previously
  `intex1`, videojuegos) was rewritten to use only `df_atletas`; (2) **`df_athletes` renamed
  to `df_atletas`** everywhere in the file; (3) **all numbering restarted independently at 0**
  for this file only — `check_ex0-6` (was `ex6-11`), `check_debug0-3` (was `debug2-5`),
  `check_t0-4` (was `t10-12` + 2 new), `check_intex0-4` (was `intex1-2` + 3 new) — Semana 1's
  own numbering is untouched; (4) every guided filter example now prints `.head()` of the
  filtered result plus a markdown callout ("`df_mayores20` es un DataFrame completo...") so
  it's explicit that filtering produces a reusable table, not a summary — same treatment for
  the boolean-mask and combined-filter examples; (5) every 👀 OBSERVA code cell got per-line
  comments explaining what each method call does and why (previously several had none); (6) a
  new "Antes de Filtrar" recap block (with a new graded `check_ex0`) drills `.mean()`/
  `.median()`/`.std()` again on `df_atletas` before Seccion C, and a new "¿Como funciona
  groupby()?" theory block + guided cell precedes Seccion D's first example, showing the
  intermediate `SeriesGroupBy` object explicitly (ties into new `check_t3`); (7) Integracion
  expanded from 2 items to 5 (`intex0`-`intex4`): basketball average height, a Baloncesto-vs-
  Gimnasia age-gap comparison, the pre-existing Peru/deportes count, a new opinion-multiple
  item (`intex3`) that asks the student to correctly interpret their *own* `intex1` finding
  (correlation vs. causation, same principle as `check_t12`), and a dispersion-focused finding
  (`std()` + `groupby()`, which deporte has the most variable height). Two new theory
  questions (`t2` precedence/equivalence of a combined filter, `t3` what `groupby()` returns
  before aggregating) and the `intex3` prompt are documented in full — question, options,
  correct answer, distractor rationale — in a new "Bloque 5" section of
  `Preguntas_Teoricas_Semanas1-2.md`, alongside a mapping table showing which of `t0`/`t1`/`t4`
  reuse `t10`/`t11`/`t12` verbatim under their new local numbers. **Safe to renumber now for
  the same reason as the 2026-08-05 Semana 1 renumbering**: `autograder_nb1_semana2.py`
  (ticket #10) still doesn't exist, so no live grader had to be migrated — tickets #10-#12
  updated to reflect the new numbering and point totals. All real (`grader.check_*`-free) code
  cells re-verified two ways against real `athlete_events_es.csv` values: a syntax compile of
  every non-debug cell, and a full front-to-back execution with correct solutions substituted
  into every stub exercise (0 errors; every debug cell raises exactly its intended error and
  nothing else does). **Semana 1 notebook explicitly left untouched**: `build_nb1.py`'s own
  `s1` generator output has drifted from the committed `nb1_semana1_recuperacion_datos.ipynb`
  (someone hand-edited the delivered notebook after generation, in commit `def6abb`, without
  updating the generator) — running `build_nb1.py` regenerates both files, so the Semana 1
  output was reverted via `git checkout` after generation to avoid silently clobbering that
  hand-edit with stale generator output. Flagging as a new, not-yet-ticketed finding: `build_nb1.py`
  and the committed Semana 1 notebook are out of sync and someone should reconcile them
  (either port the hand-edits back into the generator, or accept the generator is no longer
  the source of truth for Semana 1).
- 2026-08-07 — **Fixed `nb1.html`: it was pointed at the wrong data.** User confirmed the live
  Supabase migration (curso column + backfill + courses table, entries below) has been applied,
  then asked to verify the autograder posts correctly and that `nb1.html` links to it. The
  autograder side checked out (`autograder_nb1_semana1.py`'s POST payload keys line up 1:1 with
  `submissions` columns, `CURSO_ID='STAT_2026'`/`NOTEBOOK_ID='nb1_semana1'`), but `nb1.html`
  called `db.rpc('get_best_submissions', { nb: 'nb1' })` — a notebook id (`'nb1'`) that no
  Pokemon-themed submission has ever used (`autograder_nb1_semana1.py` sends `'nb1_semana1'`),
  so the leaderboard would show zero players against real data. Also didn't filter by `curso`
  at all — a latent collision, since the STAT module's planned Tarea 2/3 notebook ids (`nb2`,
  `nb3`, see the `curso` column comment in `supabase_schema.sql`) are the *same strings* CS
  already uses, so an un-scoped query would eventually mix rows from both courses. Rather than
  guess at the live `get_best_submissions` RPC's current signature (still not committed to this
  repo — ticket #6, and not verifiable without live DB access), switched `loadLeaderboard()` to
  query `public.submissions` directly (anon SELECT already allowed by RLS) filtered on
  `curso=STAT_2026` and `notebook=nb1_semana1`, then wired in the file's own `dedup()` helper
  (defined earlier in the file but never actually called — dead code before this fix) to collapse
  multiple attempts per student to their best score. Added `CURSO_ID`/`NOTEBOOK_ID` constants
  mirroring the autograder's naming so the two files are easy to cross-check by eye. **Does not
  resolve ticket #6** — once the RPC is pulled and extended for `curso`, this page could switch
  back to it; left as direct-query for now since it's independently correct.
- 2026-08-07 — **`supabase_schema.sql` gains a `courses` table** (`id` text PK matching
  `submissions.curso`, `name`, `bimestre`, `year`), RLS-enabled with anon SELECT only (public
  hub/leaderboard can show a friendly course name; only service_role writes), seeded with the
  two courses currently in use: `CS_2026` (Computer Science, Bimestre 2) and `STAT_2026`
  (Estadistica, Bimestre 3). Not FK-linked to `submissions.curso` — kept as a lookup table, not
  an enforced constraint, so the autograders' free-text inserts can't break on a typo or a
  future course id added late. Example leaderboard query at the bottom of the file updated to
  `LEFT JOIN` it for `curso_nombre`.
- 2026-08-07 — **`supabase_schema.sql` updated to add the `curso` column** flagged as a manual
  follow-up in the 2026-08-05 Done log entry below (`autograder_nb1_semana1.py` already sends a
  `curso` field in its payload, but the column didn't exist in the committed schema yet). Added
  `ALTER TABLE ... ADD COLUMN IF NOT EXISTS curso text`. **Naming convention finalized per user
  request the same day**: `'CS_2026'` for Computer Science (Bimestre 2, notebooks nb1/nb2/nb3)
  and `'STAT_2026'` for Estadistica (Bimestre 3) — supersedes the placeholder
  `"bimestre3_estadistica"` value used in the first cut of `autograder_nb1_semana1.py`, now
  updated to send `"STAT_2026"` instead. Column gets `DEFAULT 'CS_2026'` (the older CS
  autograders like `autograder_nb2.py` never set `curso` at all, so anything that doesn't
  specify it explicitly is CS by construction) plus a one-time
  `UPDATE ... SET curso = 'CS_2026' WHERE curso IS NULL` to backfill existing rows — this
  reverses the earlier "nullable, no backfill" call now that the user wants old rows labeled
  explicitly rather than left NULL. Also added index
  `idx_submissions_curso_notebook_pct ON (curso, notebook, pct DESC, submitted_at DESC)` for
  leaderboard queries filtered by module. Documented in the schema comments that the Estadistica
  module has 3 tareas/notebooks, same shape as CS's nb1/nb2/nb3: `nb1_semana1`+`nb1_semana2`
  (Tarea 1, Pandas Bootcamp split across two weeks), `nb2` (Tarea 2, Correlacion — not yet
  built), `nb3` (Tarea 3, Regresion/Clustering — not yet built). Still requires someone with
  Supabase access to actually run the migration (ALTER + backfill UPDATE) against the live DB —
  this commits the SQL, it doesn't apply it. **Does not resolve ticket #6** (`get_best_submissions`
  RPC still needs its live definition pulled and extended to filter by `curso`) — left open,
  flagged again in the index comment.
- 2026-08-05 — **`autograder_nb1_semana1.py` written** (ticket #10, Semana 1 half only —
  Semana 2 still open). Pokémon theme (user-directed, ad hoc — does **not** resolve open
  ticket #2's "finalize themed narrative arc" question, which is about the 8-week module
  arc, not a one-off skin for this file): dark navy/Pokéball-red/Pikachu-gold/trainer-blue
  palette, 6 levels Novato de Pueblo Paleta → Campeón de la Liga Pokémon, achievement
  rarities renamed to Poké/Gran/Ultra/Master Ball tiers, outliers in `ex5` flavored as
  "legendary sightings" (no change to grading logic, presentation only). New feature vs.
  the NB2 pattern: `check_t1`–`check_t9` render as an interactive clickable HTML
  multiple-choice form (`google.colab.output.register_callback` + `invokeFunction`,
  falls back to `input()` prompts outside Colab) instead of nb2's static
  `respuesta_tN = "?"` variable pattern — grades and awards XP on click via the same
  `_award()` pipeline as every other check. Covers `check_ex1`–`ex5`, `check_debug1`,
  `check_t1`–`t9`, `check_mini_a`, `check_mini_b`, `resumen()`. Scoring: ex/debug points
  taken verbatim from what's already printed in the notebook's markdown (8+8+10+10+10+10
  = 56, non-negotiable — changing them would desync notebook text from grader); theory
  questions priced at 5 pts each (45 pts, ATLAS's own call, not fixed anywhere else) →
  `_CORE_MAX = 101`, resolving ticket #11 for this file (see updated ticket text).
  Expected values for every numeric check computed directly against the real
  `vgsales_es.csv` (16598 rows × 11 cols; `Anio` has the most nulls at 271, not `Editor`'s
  58; media/mediana `Ventas_Globales` ≈0.537/0.17; `Ventas_NA` media/mediana/desv
  ≈0.265/0.08/0.817; outlier `umbral` ≈2.092 → 790 juegos atípicos) — not estimated.
  Supabase: same project/table as NB2/NB3, `notebook="nb1_semana1"`. **New field added to
  the payload per user request**: `"curso": "bimestre3_estadistica"`, to distinguish this
  module's submissions from the earlier Bimestre 2 CS module's own nb1/nb2/nb3 rows in the
  same `submissions` table — this requires adding a `curso` (text, nullable) column in
  Supabase before the first real submission; the script can't create that column itself,
  flagging as a manual follow-up for whoever has DB access. Validated: `py_compile` clean;
  smoke-tested every `check_*` against real dataset values and deliberately-wrong/lazy/
  malformed inputs (wrong type, `None`, hardcoded distractor answer, wrong umbral formula,
  garbage/empty theory answers) — all correctly reject; summed check maxima (101) matches
  declared `_CORE_MAX` exactly.
- 2026-08-05 — **Fixed a sequencing bug in Semana 1 `ex5` (outliers): it required boolean-mask
  filtering (`df[df['col'] > umbral]`) that isn't formally taught until Section C, which lives
  in the *Semana 2* notebook a week later.** User caught this — it predates today's other
  changes; it was already present in the original `ex4` (now `ex5`) from the very first build
  and survived SOFIA's Mode 3 review and GAUSS's informal sign-off on 2026-08-05. Fix: added a
  short "Adelanto" (preview) markdown + guided 👀 OBSERVA cell right before `ex5` that
  demonstrates the exact `df[df['columna'] operador valor]` pattern on a throwaway example
  (`Ventas_Globales > 5`), explicitly flagged as a preview ("la Seccion C de la proxima semana
  explica en detalle por que funciona esto") rather than a full explanation — `ex5` is now a
  repetition of something just demonstrated, matching the guided-example-then-exercise
  convention used everywhere else in the mission, instead of cold unseen syntax. Also added a
  one-line callback at the top of Semana 2's `nb1-c-header` ("Ya usaste este patron una vez, sin
  explicacion, en el Ejercicio 5 de la semana pasada... Ahora vemos por que funciona") so
  Section C's formal mask explanation reads as follow-through, not a repeat-from-scratch.
  Grading footprint unchanged (still 17 `check_*` calls in Semana 1 / 35 total) — this was a
  pure sequencing/instruction fix, no new or removed points. Worth a general note for future
  passes: **check every `check_exN`'s required syntax against the technical-spine teaching
  order**, not just against `WORKFORCE_CONTRACT.md` §5's flat skill list — the spine lists
  skills without ordering, but the two-notebook split (§2) means "taught this week" now has
  real weekly boundaries an exercise can silently violate. Rebuilt via `build_nb1.py` (55 cells
  now, was 53); both new cells and the unchanged `ex5` solution re-verified against
  `vgsales_es.csv`.
- 2026-08-05 — **Semana 1 dispersion exercise made graded + renumbered `ex4`–`ex11`,
  following immediate user feedback on the same-day expansion below.** User flagged two gaps:
  (1) the new `Ventas_NA` mean/median repetition cell was left ungraded — user wants it graded;
  (2) Section B teaches dispersion (std) via the "Dispersion" theory block + a guided
  `.std()` example, but the only place a student ever *computed* std themselves was buried
  inside `ex4`'s outlier-threshold formula (`media + desviacion_estandar`) — there was no
  standalone instruction/exercise that isolates `.std()` the way `ex3` isolates mean/median.
  Fix: promoted the `Ventas_NA` repetition into a real graded exercise, moved it to *after* the
  dispersion theory/guided example (not after `ex3`), and extended it to compute
  `desviacion_na` too — so it now doubles as the missing dedicated dispersion exercise instead
  of being a second ungraded mean/median rep. This is a **new** `check_ex4` (`media_na`,
  `mediana_na`, `desviacion_na`; 10 pts; un-hinted 🔨 CONSTRUYE, matching the Section C/D
  no-giveaway convention), which pushed the pre-existing outlier exercise from `ex4` to `ex5`
  and, since exercise numbering is global across both notebook files (`WORKFORCE_CONTRACT.md`
  §3), cascaded a straight +1 renumbering through Semana 2's `ex5`–`ex10` → `ex6`–`ex11` (ids,
  labels, `check_exN()` calls). **No other numbering changed**: `check_tN`, `check_debugN`,
  `check_intexN`, `check_retoN` are independent sequences per the same-day discovery and were
  untouched. Safe to renumber now precisely because ticket #10's autograders don't exist yet —
  this is the last easy window to do it before ATLAS builds against fixed numbers. Reopens
  ticket #11 in worse shape (see updated ticket text: 153 → 163 pts) since this was a real new
  point-bearing item, not a redistribution — user's call, made with the tradeoff visible, not a
  silent addition. Rebuilt via `build_nb1.py` (53 cells now, was 52); the new `ex4` and the
  renumbered `ex5` (outlier logic unchanged) both re-verified clean against `vgsales_es.csv`.
- 2026-08-05 — **Semana 1 (`nb1_semana1_recuperacion_datos.ipynb`) expanded per user request**
  following a content-sufficiency review: user felt Section A/B needed (1) an explanation of
  what pandas/`import` actually are — the notebook previously jumped straight to
  `import pandas as pd` with zero framing, the first time the whole Bimestre touches the
  library — and (2) more repetition + a way to check real understanding beyond multiple choice.
  Added: a short "¿que es pandas?" markdown block (library/import concept, `pd` alias,
  `pd.read_csv` preview) right before the existing setup cell — kept to a few sentences, not a
  standalone unit, so it doesn't conflict with `WORKFORCE_CONTRACT.md` §5's "no standalone
  pandas-fundamentals week" line; an **ungraded** `.head()`/`.tail()` repetition-practice pair in
  Section A and an ungraded mean/median repetition on `Ventas_NA` in Section B (mirrors the
  Section C/D repetition-ladder pattern, just without a `check_*` call); and one **ungraded,
  open-ended** 💭 REFLEXIONA cell per section (free-text `reflexion_a`/`reflexion_b`, teacher-
  reviewed, not autograded) — new icon added to the legend table, same pattern as the existing
  ungraded 🔮 PREDICE cell in Ex2. Deliberately kept all of this **ungraded** rather than adding
  new `check_*` items so it doesn't worsen the open XP-budget overage (ticket #11) — if graded
  reflection questions are wanted later, that should go through ticket #11's resolution first,
  not bypass it. Also fixed a standing, never-ticketed finding from the same-day Mode 3 review:
  Ex4's code cell hint used to hand over the entire three-line solution in comments despite being
  tagged 🔨 CONSTRUYE; hint trimmed to just the expected variable name (`umbral`), matching the
  un-hinted CONSTRUYE cells elsewhere in the mission. `check_ex4`'s expected variables/behavior
  are unchanged. Semana 1 is now 52 cells (18 md / 34 code) — **16 `grader.check_*` calls,
  unchanged** from before this pass, confirming the addition is purely additive to
  ungraded/reflective content. Semana 2 untouched. Rebuilt via `build_nb1.py`; all new/edited
  code cells re-verified against `vgsales_es.csv` (head/tail with varying N, `Ventas_NA`
  mean/median, and the trimmed-hint Ex4 solution all run clean).
- 2026-08-05 — **Weeks 1–2 split into two notebook files, one per class session.**
  `Weeks 1-2/build_nb1.py` now generates `nb1_semana1_recuperacion_datos.ipynb` (42 cells: 13
  md/29 code, 16 checks — Apertura, Teoría Desbloqueada, Section A, Section B) and
  `nb1_semana2_recuperacion_datos.ipynb` (71 cells: 31 md/40 code, 18 checks — Section C, Section
  D, Integración + Reto as homework), split exactly at the "Fin de la Clase 1" marker from the
  same-day SOFIA review. Supersedes the 2026-08-02 single-notebook decision (`WORKFORCE_CONTRACT.md`
  §2 updated) — that call predated knowing the actual delivery schedule; Weeks 1–2 turned out to
  be two ~90-minute sessions a week apart, not one sitting. `check_ex`/`check_debug`/`check_tN`
  numbering stays global across both files (Semana 2 continues at `ex5`/`debug2`/`t10`, not a
  restart) so the two sessions still read as one mission. Semana 2 reloads `df_games` in addition
  to `df_athletes` since the homework `intex1` still needs it. Both files independently verified:
  each loads its own data, every non-stub cell executes clean, and every debug cell fails with
  exactly its intended error and nothing else does. Total checks unchanged (34) — just
  redistributed 16/18 across the two files. Opens a **new** requirement on ticket #10 (now two
  separate autograders, not one — see ticket text) that didn't exist before this split.
- 2026-08-05 — **SOFIA Mode 3 review of the Weeks 1–2 notebook, then revised per findings +
  user's actual class-schedule input.** Review flagged 9 issues across theory/comments/practice
  structure (front-loaded theory before any code, debug hints over-scaffolded, `ex4` hint
  inconsistent with the un-hinted repetition-ladder exercises, `ex9` reverting to COMPLETA at
  the point the arc should demand more independence, no marked class boundary, XP budget already
  over before theory is priced). User confirmed: Week 1 = Class 1 (theory + Section A + Section
  B), Week 2 = Class 2 (~90 min), and asked for Section D to be expanded to match Section C's
  repetition-ladder depth, with overflow content assigned as homework rather than trimmed.
  Applied: (1) explicit "Fin de la Clase 1" marker after `check_mini_b`; (2) Section D expanded
  from 2 exercises/1 debug to 3 guided examples + 3 exercises (`ex8`–`ex10`, `ex9` now CONSTRUYE
  instead of COMPLETA) + 2 debugs (`debug4` new KeyError, `debug5` = renumbered `.means()` bug),
  mirroring Section C's single-column → combined-filter arc; (3) explicit "Fin del trabajo en
  clase" marker after `check_mini_d`, with Integración/Reto relabeled "(Tarea)" — homework, not
  in-session work. New debug4's hint was written un-scaffolded ("lee el mensaje completo,
  identifica que tipo de error es") per the review's finding; `debug1–3`/`5`'s hints were not
  touched (ticket #12 tracks fixing those). Notebook now 110 cells (43 md/67 code), 34
  `grader.check_*` calls (10 ex, 5 debug, 12 t, 4 mini, 2 intex, 1 reto). All non-stub/non-grader
  code cells re-verified against the real CSVs; all 5 debug cells fail with exactly their
  intended error (KeyError ×2, SyntaxError, ValueError, AttributeError) and nothing else does.
  Point tally re-run: `ex`+`debug` alone now sum to **153** (up from 131), already at/over the
  ~150 §2 budget before any theory question is priced — opened as ticket #11. Review's other
  findings (theory-block sequencing vs. `COURSE_TEMPLATE.md` §4, no point value shown on `tN`
  cells) not yet acted on — not blocking, revisit before calling Weeks 1–2 final.
- 2026-08-05 — **Weeks 1–2 notebook built**: `Weeks 1-2/build_nb1.py` generates
  `Weeks 1-2/nb1_mision_recuperacion_datos.ipynb` (92 cells — 38 markdown, 54 code).
  Implements the full section structure below using the already-approved datasets, the
  drafted theory content (`Teoria_Semanas1-2_Mision1_RecuperacionDeDatos.md`), and the
  full `check_t1`–`check_t12` bank (`Preguntas_Teoricas_Semanas1-2.md`) interleaved by
  section per that doc's plan (t1–t3 before Section A, t9 in Section A, t4–t8 in Section
  B, t10–t11 in Section C, t12 in Section D). Apertura hook rewritten to use real
  `Ventas_Globales` numbers (mean 0.54M vs. median 0.17M, only 22.6% of games sell above
  the mean) instead of the original INEI-based draft, since the hook's own rule ("no
  invented numbers") required matching whichever dataset ended up in Section B. All 24
  non-placeholder, non-`grader.*` code cells were executed against the real CSVs and run
  clean; the 3 `check_debugN` cells fail exactly as designed (KeyError, SyntaxError,
  AttributeError) and nothing else does. 30 `grader.check_*` calls total (12 theory + 8
  ex + 3 debug + 4 checkpoints + 2 intex + 1 reto) — none are gradable yet pending ticket
  #10. Suggested point values sum to ~152 (close to the ~150 `WORKFORCE_CONTRACT.md` §2
  budget; ATLAS to finalize exact `_CORE_MAX` arithmetic per ticket #10).
- 2026-08-05 — **Weeks 1–2 lesson structure locked** ("Mission 1: Data Recovery," single notebook
  per ticket #5, now removed): Section A Landing (load/`.head()`/`.info()`, ~25 XP) → Section B
  Recon (`.describe()`, mean/median/std, ~30 XP) → Section C Filter the Noise (boolean indexing,
  incl. `check_debug`, ~35 XP) → Section D Compare Groups (`.groupby()`, `check_mini_d`
  checkpoint, ~40 XP) → Integration (`check_intexN`, ~15 XP) → bonus `check_reto` (separate
  `_BONUS_MAX`). Core XP sums to ~145–150, matching the `WORKFORCE_CONTRACT.md` §2 budget; ATLAS
  to confirm exact arithmetic when exercise specs are written (ticket #9).
  **Datasets decided** (closes ticket #1): (1) Kaggle "Video Game Sales" (`vgsales.csv` — Name,
  Platform, Year, Genre, Publisher, NA/EU/JP/Global Sales, Critic Score; ~16,600 rows) for
  Sections A–B — `Global_Sales` is genuinely right-skewed by a handful of blockbuster outliers
  (Wii Sports, GTA V, Minecraft), which makes the Section B "does mean tell the honest story?"
  exercise a real statistical finding rather than a manufactured example; `Critic_Score`/
  `Publisher` carry real nulls, useful for the `.info()` non-null-count teaching moment. (2)
  Kaggle "120 Years of Olympic History" (age/height/weight/medals/sport, thousands of rows) for
  Sections C–D — large n, genuine natural outliers, optional `NOC == 'PER'` filter sub-exercise
  for local relevance.
  **Superseded:** an earlier same-day decision paired Section A–B with INEI regional indicators
  (~24 rows) for Peru-specific cultural relevance. User swapped it out in favor of Video Game
  Sales for a richer/more entertaining `.describe()`/`.info()` experience — the Peru-specific
  framing is now carried only by Olympics' optional `NOC == 'PER'` filter, not by the primary
  dataset. Also still rejected for Wk 1–2: Liga 1 Perú stats (too few numeric columns/rows to
  support Section D alone); World Happiness Report / World Bank indicators (reserved for Wk 3–4
  instead — its strong GDP↔happiness relationship would let students informally pattern-match a
  causal read before Week 5's causation guardrails exist to check it, the "misleading obvious
  trend" risk `04_GAUSS.md` flags for this unit).
  **GAUSS informal sign-off:** both approved. Video Game Sales' skew is a genuine, verifiable
  phenomenon (not baked-in misleadingly); Olympics' lack of Peru-specific framing is mitigated by
  the optional filter. Ready for SOFIA to write formal exercise specs (ticket #9) → ATLAS grader
  build.
- 2026-08-02 — Added GAUSS (`04_GAUSS.md`), a statistics content-accuracy specialist: reviews
  conceptual explanations, interpretation-key wording, and dataset choices for statistical
  soundness — a gap ATLAS explicitly disclaimed (code/rubric-logic correctness, not conclusion
  correctness) and SOFIA's broad pedagogy mandate didn't cover in depth. Wired into
  `WORKFORCE_CONTRACT.md` §6 Agent Interfaces and build order, and into SOFIA/PIXEL/ATLAS's
  Collaboration Maps. Supersedes the "no fourth agent added" scope cut below, which was about
  rubric-*grading* bandwidth, not content accuracy — a different concern.
- 2026-07-20 — Workforce roles (SOFIA/PIXEL/ATLAS) refreshed for the Bimestre 3 Statistics module:
  added Project Context sections describing the module, reformatted SOFIA's file to match
  PIXEL/ATLAS's structure, fixed stale "SMA Intro CS WORKFORCE" footer branding across all three.
- 2026-07-20 — ATLAS's mandate extended to cover capstone rubric design/validation (point-sum
  integrity, criterion-to-evidence mapping, manual-vs-derivable criteria) alongside `check_*`
  autograder validation, plus statistics/ML-specific grading logic (float tolerance, cluster-label
  arbitrariness, sklearn output shape).
- 2026-07-20 — Coordination layer adopted: SOFIA designated owner of this handoff tracker and
  `WORKFORCE_CONTRACT.md`, per the ORCHESTRATOR's standing convention.

---

## Accepted Risks / Scope Cuts

- ~~**Files kept at repo root, not moved into `WORKFORCE/`.**~~ **Resolved 2026-08-08.** Full
  repo reorg: `01_SOFIA.md`, `02_PIXEL.md`, `03_ATLAS.md`, `04_GAUSS.md`,
  `WORKFORCE_CONTRACT.md`, and `WORKFORCE_HANDOFF.md` (this file) moved into `WORKFORCE/`,
  matching the path `COURSE_TEMPLATE.md` already documented. `COURSE_TEMPLATE.md` and
  `supabase_schema.sql` moved to `shared/`; each course's guide, official unit-plan docx, and
  `Weeks N-M` folder now nest under `course-python-stats/` or `course-sheets-stats/`;
  `autograder_nb1_semana1.py` moved next to `build_nb1.py` in
  `course-python-stats/Weeks 1-2/`. The prerequisite-course grader (`autograder_nb2.py`, God of
  War theme, unrelated to either stats course) moved to `reference/legacy-CS1/`. Notebook `!wget`
  URLs and `nb1.html`'s logo `<img src>` were updated to match the new paths — see root
  `README.md` for the full map.
- **No fourth agent added for capstone/rubric grading.** ATLAS's existing mandate was extended
  instead (see Done Log). Revisit only if rubric-grading work turns out to need dedicated bandwidth
  ATLAS can't reasonably absorb alongside autograder validation.

---

## Open Escalations

None currently.

---

## Change Log

- 2026-07-20 — Tracker created as part of workforce polish for the Bimestre 3 Statistics module.
  Seeded with the open questions from `Bimestre3_Statistics_Python_Module_Guide.md` plus this
  polish pass's own decisions.

# Workforce Contract — Bimestre 3: Statistics in Python

**Owner:** SOFIA. **Governs:** the logical shapes PIXEL and ATLAS build against — section/week
structure, exercise-key taxonomy, and scoring shape. Edited in place; never forked into
version-suffixed copies. See the ORCHESTRATOR's "Living Contract & Handoff Documents" convention
(`WORKFORCE/ORCHESTRATOR/ORCHESTRATOR.md`) for why this file exists and how it's meant to be used.

Companion file: `WORKFORCE_HANDOFF.md` (open tickets, Done log, accepted scope cuts, escalations).

---

## 1. Module Identity

| | |
|---|---|
| Module | Bimestre 3 — Statistics in Python |
| Audience | 3rd–5th secondary, ages 15–17 |
| Duration | 7–8 weeks |
| Prerequisite | For loops, if statements, basic functions (Bimestre 2) |
| Format | Jupyter notebooks, gamified narrative, autograded via the existing Colab → autograder → Supabase pipeline (`COURSE_TEMPLATE.md`) |
| Source syllabus | `Bimestre3_Statistics_Python_Module_Guide.md` |

---

## 2. Week → Notebook Structure

**Revised (2026-08-05): Weeks 1–2 split into two notebook files, one per class session**
("Mission 1: Data Recovery" — `nb1_semana1_recuperacion_datos.ipynb` /
`nb1_semana2_recuperacion_datos.ipynb`). Supersedes the 2026-08-02 "single notebook" decision:
that call was made before the actual class schedule was known — Weeks 1–2 turned out to be
exactly two ~90-minute sessions a week apart, not one sitting, so one file per session matches
delivery reality. `check_ex`/`check_debug`/`check_tN` numbering stays global across both files
(not reset per file) so the two sessions still read as one mission. Other weeks' bundling still
open where noted.

**Revised (2026-08-20): Weeks 3–4 ("Correlation") also split into two notebook files**, same
pattern as Weeks 1–2 — `nb3_semana3_correlacion.ipynb` (49 cells) / `nb3_semana4_correlacion.ipynb`
(46 cells), both from `Weeks 3-4/build_nb3.py`. Triggered by the same failure mode Weeks 1–2 hit
first: a single-file "Clase 1" (see `WORKFORCE_HANDOFF.md` ticket #13, resolved by this split)
reached `_CORE_MAX=264` against a real classroom plan of 40-50 min lecture + 1-1.5h homework —
well past what fits. Unlike the Weeks 1–2 split, the fix here wasn't only "more sessions": graph
building and `.corr()` calculation were fused into one exercise per round (previously two separate
exercises), and the 11 AI-graded 💭 Reflexiona cells — the actual time cost, each a real
`grade-reflexion` Edge Function round-trip, not the exercises themselves — were cut to 6 by making
reflection "occasional" rather than per-exercise. Sección C (subgroup correlation) and the Semana 4
mini-project, spec'd in `Teoria_Semanas3-4_Mision2_Correlacion.md` since 2026-08-14 but never built,
now exist in the Semana 4 file. Full rebuild rationale and validation in `WORKFORCE_HANDOFF.md`'s
2026-08-20 Done log entry.

| Weeks | Focus | Learning Target | XP Budget |
|---|---|---|---|
| 1–2 | Pandas bootcamp (2 notebooks, "Mission 1: Data Recovery" Semana 1 / Semana 2) | Load, explore, filter, describe a dataset | ~150 (under review — see `WORKFORCE_HANDOFF.md` ticket #11) |
| 3–4 | Correlation (2 notebooks, "Misión 2: Buscando Patrones" Semana 3 / Semana 4) | Calculate and visualize correlation in one step; `.groupby()`/filter by subgroup | ~180 nominal — actual `_CORE_MAX` = 200 (nb3) + 60 (nb4, trimmed 2026-08-29) = 260 combined; not treated as a hard budget per the user's 2026-08-19 call that per-notebook % normalization makes the raw `_CORE_MAX` non-comparable across notebooks. Supersedes the earlier "≈275 across both files" figure, which predates the 2026-08-29 trim. |

**New (2026-08-21): Weeks 3–4 gained a parallel "ruta de interpretación" track**
(`nb3_lite_correlacion.ipynb` / `nb4_lite_correlacion.ipynb`, from new sibling build
scripts `build_nb3_lite.py` / `build_nb4_lite.py`) for inclusion students who struggle
with writing code but test strong on interpretation — the actual stated target of this
module per §1's "statistical thinking first, code as the tool to get there." Same
dataset, same real r-values, same graphs, same 10 theory MCs and 7 AI-graded reflection
prompts as the main nb3/nb4 track, verbatim — none of that content ever depended on the
student writing pandas (confirmed against `_TEORIA` before building). What's removed is
only the code-writing layer: every `🔨 CONSTRUYE` round becomes a pre-filled `👀 OBSERVA`
cell (same reference solution, same real output, run not written); the debug exercise
becomes a multiple-choice "what kind of error is this" question instead of a typed fix;
the own-choice mini-project becomes a `🧩 COMPLETA` fill-in (pick two real, unused column
names + write a hypothesis) with the `.corr()` line pre-written rather than authored.
`autograder_nb3_lite.py`/`autograder_nb4_lite.py` subclass the main autograders to reuse
their theory-widget/reflection-grading/gamification/Supabase engine verbatim rather than
duplicating it — only the exercise-completion layer differs. Distinct `notebook_id`s
(`nb3_lite`/`nb4_lite`) keep these submissions out of the main leaderboard's percentage
comparison. `_CORE_MAX` = 50 (nb3_lite) / 55 (nb4_lite), both theory+reflection only
(no `ex`/`debug`/`intex` code points). Full design rationale and open questions in
`WORKFORCE_HANDOFF.md`'s 2026-08-21 Done log entry.
| 3–4→5 bridge | **New (2026-08-29):** `proyecto_investigacion.ipynb` (own dataset, own claim, no autograder) | Started in class Semana 4, due before Semana 5; presentation opens Semana 5. Replaces nb4's cut Mini-Proyecto — see 2026-08-29 Change Log entry and `WORKFORCE_HANDOFF.md` Done log | 85 pts, human-graded rubric (not XP) |
| 5 | Causation reality check | Distinguish correlation from causation; identify confounders | ~100 |
| 6 | Linear regression | Interpret a fitted regression, not derive it | ~150 |
| 7 | K-means clustering | Interpret clusters, not derive the algorithm | ~120 |
| 8 | Capstone | Integrate stats + (optionally) one ML technique on a real question | 100 pts (rubric, not XP) |

Total: ~700 XP + 100 capstone rubric points.

---

## 3. Exercise-Key Taxonomy (contract: reuse the existing convention)

Same taxonomy as NB1–NB3 (`COURSE_TEMPLATE.md` §4), applied per week/notebook unit:

- `check_exN` — core exercise, one per concept
- `check_debugN` — broken demo, student fixes it (≥3–4 per notebook where applicable)
- `check_tN` — theory/multiple-choice (`respuesta_tN = "?"` pattern)
- `check_mini_X` — section checkpoint, gates progress, usually no independent XP
- `check_intexN` — Part 2 integration exercises, scored/reported separately from Part 1
- `check_retoN` — optional bonus, scored separately (`_BONUS_MAX`, never folds into level %)
- `resumen()` — final cell, submits to Supabase

Week 8's capstone is the one exception to this taxonomy: it is rubric-graded (§4), not
`check_*`-graded. See ATLAS's Rubric Validation Report format for how that's audited.

**Ungraded reflection cells (no `check_*` call, contract-exempt by design):** a 🔮 PREDICE
(pre-`.info()` prediction) or 💭 REFLEXIONA (open-ended, teacher-reviewed free text) cell — a bare
`variable = "___"` with no `grader.check_*()` call — is a deliberate outside-the-taxonomy pattern
for building intuition/checking real understanding without touching the XP budget (see
`WORKFORCE_HANDOFF.md` ticket #11 and 2026-08-05 Done log entry). Use freely; if one of these
should ever become graded, that's a scope change routed through ticket #11, not a silent addition.

---

## 4. Capstone Rubric (contract: this exact split, pending the open question below)

| Criterion | Points |
|---|---|
| Dataset quality + research question | 15 |
| Descriptive analysis with interpretation | 20 |
| Correlation analysis with causation critique | 20 |
| Visualization quality | 20 |
| Regression/clustering implementation (if used) | 15 |
| Presentation clarity | 10 |
| **Total** | **100** |

**Open:** whether the "if used" row is mandatory, optional-with-redistribution, or optional-as-0.
Tracked in `WORKFORCE_HANDOFF.md` — do not build the autograder/rubric tooling around an assumed
answer.

---

## 5. Technical Spine (contract: nothing outside this list in a `check_*`)

`pd.read_csv`, `.head()`, `.info()`, `.describe()`, boolean filtering (`df[df['col'] > x]`),
`.groupby()`, `.mean()/.median()/.std()/.corr()`, `matplotlib` scatter/basic charts,
`sklearn.linear_model.LinearRegression` (`.fit()`/`.predict()`), `sklearn.cluster.KMeans`
(`.fit_predict()`). No standalone "pandas fundamentals" week — each skill is taught embedded in
the analysis that needs it.

---

## 6. Agent Interfaces

1. **SOFIA → PIXEL:** pedagogical goal, week/section structure, learning objectives per unit.
2. **SOFIA → ATLAS:** exercise specs, learning objectives, rubric criteria wording.
3. **SOFIA → GAUSS:** draft conceptual explanations, interpretation-key wording, candidate
   datasets, exercise specs.
4. **PIXEL → ATLAS:** achievement trigger conditions, level thresholds.
5. **PIXEL → GAUSS:** metaphors/flavor text standing in for a statistical concept.
6. **ATLAS → PIXEL:** confirmation that score distribution supports proposed thresholds; rubric
   criteria with a visual/presentation component.
7. **ATLAS → GAUSS:** which rubric/exercise criteria are interpretation-graded, actual dataset
   values being graded against.
8. **ATLAS → SOFIA/User:** solvability validation, scoring/rubric arithmetic checks, rubric
   validation reports.
9. **GAUSS → SOFIA/ATLAS:** statistical accuracy sign-off, caveat rewrites, dataset vetting
   reports, statistically defensible model answers for interpretation-graded criteria.

Build order stays: **SOFIA defines structure → GAUSS vets statistical accuracy of content and
datasets → PIXEL themes it → ATLAS validates and builds the grader/rubric → build script
assembles the notebook** (`COURSE_TEMPLATE.md` §12).

---

## Change Log

- 2026-08-29 — §2 updated: nb4's Rondas 5–6 (pure repeat of Semana 3's
  scatter+`.corr()` pattern) and its Mini-Proyecto (`intex1` + two
  reflections) were cut — user decision, both distinct-skill content
  (Debug 1, Ejercicio 7, Sección C's subgroup work) and the checkpoints were
  kept. nb4 `_CORE_MAX`: 150 → 60. In their place: a new notebook,
  `proyecto_investigacion.ipynb` (`course-python-stats/Weeks 3-4/`), where
  each student/pair picks their own real dataset and claim — started in
  class Semana 4 with supervision, due before Semana 5, presented at Semana
  5's opening. It has no autograder/Supabase integration; it's graded by a
  human-scored 85-pt rubric reusing the Week 8 capstone's own criteria
  language (§4) minus the regression/clustering row — the first built
  instance of the "rubric-graded, not `check_*`-graded" exception §4
  describes, ahead of the capstone itself. **Continuity note superseding the
  one that used to live on `check_intex1`:** whoever designs Semana 5 should
  treat this new notebook's hypothesis + confound write-up as the input
  material, not nb4's (now-removed) `intex1`. Full rationale in
  `WORKFORCE_HANDOFF.md`'s 2026-08-29 Done log entry.
- 2026-08-21 — §2 updated: added the Weeks 3–4 "ruta de interpretación" track
  (`nb3_lite_correlacion.ipynb` / `nb4_lite_correlacion.ipynb`) for inclusion students —
  same content, code-writing removed. See §2's new paragraph and `WORKFORCE_HANDOFF.md`'s
  2026-08-21 Done log entry for full detail.
- 2026-08-20 — §2 updated: Weeks 3–4 ("Correlation") split into two notebook files
  (`nb3_semana3_correlacion.ipynb` / `nb3_semana4_correlacion.ipynb`), mirroring the Weeks 1–2
  split. Resolves `WORKFORCE_HANDOFF.md` ticket #13 (264-pt single-file overage). Details in that
  file's 2026-08-20 Done log entry and in `course-python-stats/Weeks 3-4/ATLAS_spec_nb3_semana3-4.md`.
- 2026-07-20 — Contract created as part of workforce polish for the Bimestre 3 Statistics module.
  Seeded from `Bimestre3_Statistics_Python_Module_Guide.md` and `COURSE_TEMPLATE.md`. Week→notebook
  mapping and capstone ML-requirement left open (see `WORKFORCE_HANDOFF.md`).
- 2026-08-02 — Added GAUSS (statistics content-accuracy specialist) to close the gap where no
  agent validated statistical correctness of content (ATLAS checks code/rubric logic, not
  conclusions; SOFIA owns sequencing, not deep stats accuracy). Agent Interfaces (§6) and build
  order updated accordingly. See `04_GAUSS.md` and `WORKFORCE_HANDOFF.md`.

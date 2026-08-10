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

| Weeks | Focus | Learning Target | XP Budget |
|---|---|---|---|
| 1–2 | Pandas bootcamp (2 notebooks, "Mission 1: Data Recovery" Semana 1 / Semana 2) | Load, explore, filter, describe a dataset | ~150 (under review — see `WORKFORCE_HANDOFF.md` ticket #11) |
| 3–4 | Correlation | Calculate and visualize correlation; `.groupby()` by subgroup | ~180 |
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

- 2026-07-20 — Contract created as part of workforce polish for the Bimestre 3 Statistics module.
  Seeded from `Bimestre3_Statistics_Python_Module_Guide.md` and `COURSE_TEMPLATE.md`. Week→notebook
  mapping and capstone ML-requirement left open (see `WORKFORCE_HANDOFF.md`).
- 2026-08-02 — Added GAUSS (statistics content-accuracy specialist) to close the gap where no
  agent validated statistical correctness of content (ATLAS checks code/rubric logic, not
  conclusions; SOFIA owns sequencing, not deep stats accuracy). Agent Interfaces (§6) and build
  order updated accordingly. See `04_GAUSS.md` and `WORKFORCE_HANDOFF.md`.

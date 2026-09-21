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
| 6 | Linear regression (1 notebook, "Misión 3: El Oráculo de Datos" — `nb5_regresion.ipynb`, `course-python-stats/Week 6/`) | Interpret a fitted regression (train/test R², extrapolation risk, coefficient scale), not derive it | ~150 nominal — actual `_CORE_MAX` = 102 (2 registro participation + 25 t1-5 + 5 refl_interpretacion + 40 ex1 + 20 ex2 + 5 refl_ex2 + 5 refl_final) + `_BONUS_MAX` = 10 (reto1, "rompe el modelo"). Below nominal by design, same "showcase not deep dive" reasoning as nb4's 2026-08-29 trim — see `WORKFORCE_HANDOFF.md` Done log, 2026-09-13/14 entries. |
| 7 | K-means clustering (1 notebook, "Misión 4: El Cartógrafo de Patrones" — `nb6_clustering.ipynb`, `course-python-stats/Week 7/`) | Mostly showcase + interpretation (extra credit for students already ahead), one simple build exercise; interpret clusters, not derive the algorithm | ~120 nominal — actual `_CORE_MAX` = 87 (2 registro participation + 5 cluster_es_genero + 25 t1-5 + 40 ex1 + 5 refl_ex2 + 5 refl_generalizacion + 5 refl_final) + `_BONUS_MAX` = 10 (reto1, "cambia el número de regiones"). Same "showcase not deep dive" trim as nb5 — see `WORKFORCE_HANDOFF.md` Done log, 2026-09-19 entry. Ejercicio 3/refl_generalizacion were added 2026-09-21 (train/test-style generalization check for clustering), then Ejercicio 2 and Ejercicio 3 were both simplified away as graded builds later the same day (user call: this notebook is extra credit and should stay light) — Ejercicio 2 became an ungraded showcase cell, Ejercicio 1 now covers 2-3 predictors in one build, Ejercicio 3 was removed outright (its concept is still taught by the guided demo and assessed by `refl_generalizacion`, kept). `_CORE_MAX` 102→127→87 across the two 2026-09-21 passes. See `WORKFORCE_HANDOFF.md` Done log, both 2026-09-21 entries. |
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
(`.fit()`/`.fit_predict()`), `sklearn.preprocessing.StandardScaler` (`.fit_transform()`). No
standalone "pandas fundamentals" week — each skill is taught embedded in the analysis that needs
it.

**Added 2026-09-19 (nb6, Week 7):** `sklearn.preprocessing.StandardScaler` was not in the original
list — only `KMeans` was. Scaling before fitting k-means is a statistical non-negotiable, not an
optional technique (`04_GAUSS.md`'s Week 7 risk row: "K-means needs feature scaling before
`.fit_predict()`"); without it, nb6's own guided demo cannot demonstrate the concept it exists to
teach. Recognized scope addition, not a silent one — see `WORKFORCE_HANDOFF.md`'s 2026-09-19 Done
log entry for the empirical validation that motivated it.

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

- 2026-09-21 (later same day) — §2 updated: Week 7 (`nb6_clustering.ipynb`)
  simplified back down, reverting most of the exercise entry directly
  below. User re-read the whole notebook and decided Semana 7 is "extra
  credit for those who have made good strides on previous content," so it
  should be mostly showcase + interpretation with simple exercises — not
  three graded `🔨 CONSTRUYE` builds totaling 80 pts. `check_ex2` removed
  (Ejercicio 2 "agrega Energia" is now an ungraded `👀 OBSERVA` showcase
  cell shown before Ejercicio 1); `check_ex1` widened to accept 2 OR 3
  predictors (was exactly 2), so it now covers what used to be two
  exercises; `check_ex3` (the train/test build from the entry below)
  removed outright — the guided demo and `refl_generalizacion` already
  teach/assess the concept without a from-scratch rebuild.
  `refl_ex2`/`refl_generalizacion` kept their reflection ids (`nb6_ex2`/
  `nb6_generalizacion`) to avoid an `EXPECTED_NOTEBOOKS` change in
  `grade-reflexion/index.ts`, but that function's `question`/`grounding`/
  `grading_notes` text for both was rewritten to match the new framing —
  **still needs a redeploy** for students to see the updated wording.
  `_CORE_MAX` 127→87; `mini_a`/`mini_b` checkpoints and
  `explorador_completo` (now ex1 perfect + all 3 reflections submitted,
  was ex1+ex2+ex3 perfect) updated to match. Validated
  (`Week 7/_test_nb6.py`): 47/47 assertions. See `WORKFORCE_HANDOFF.md`'s
  2026-09-21 Done log entry (the one above the "third exercise" entry).

- 2026-09-21 — §2 updated: Week 7 (`nb6_clustering.ipynb`) extended with a
  third exercise + reflection. User asked, after nb5 taught train/test for
  regression, why nb6 (k-means, unsupervised) had no equivalent
  generalization check — "test accuracy" doesn't apply to an algorithm
  with no real labels to be right/wrong about (and would contradict
  Concepto 3's "cluster labels are arbitrary" lesson if forced), so the
  equivalent was reframed as generalization/stability: fit `KMeans` SOLO
  on train, `.predict()` (never re-fit) on a held-out test split, compare
  cluster profiles between the two. Added Concepto 4 (why generalization
  matters for an unsupervised model, motivated by two concrete use cases —
  recommend the next song by cluster, segment songs for a marketing
  decision), a guided train/test demo, Ejercicio 3 ("Prueba tu mapa en
  territorio nuevo", 20 pts, same structural-check philosophy as ex1/ex2),
  and a new IA-graded reflection (`refl_generalizacion`, 5 pts;
  `nb6_generalizacion` rubric added to `grade-reflexion/index.ts`) that
  ties a train/test profile mismatch to a concrete failure for each use
  case. `_CORE_MAX` 102→127; `mini_b` checkpoint and the
  `explorador_completo` achievement (now requires ex1+ex2+ex3, was
  ex1+ex2) updated to match. Validated (`Week 7/_test_nb6.py`): 56/56
  assertions, including the new guided demo cell re-run end-to-end against
  the real CSV — train/test cluster profiles matched almost exactly
  (e.g. Bailabilidad 0.417 train vs. 0.416 test for one cluster),
  confirming the pedagogical point rather than asserting it. See
  `WORKFORCE_HANDOFF.md`'s 2026-09-21 Done log entry.

- 2026-09-19 (same day, second pass) — **Week 7's dataset changed from
  `vgsales_es.csv` to a real Spotify dataset, superseding the entry
  directly below.** The user added `course-python-stats/Week 7/spotify.csv`
  (Kaggle's "Spotify Tracks Dataset," 114,000 tracks x 114 real genres)
  after the first version of nb6 shipped with vgsales as a stand-in. New
  `Week 7/translate_to_spanish.py` translates headers and all 114 genres
  to Spanish → `spotify_es.csv` (the dataset the notebook actually loads).
  `nb6_clustering.ipynb`/`autograder_nb6.py`/`_test_nb6.py` rebuilt around
  it: `Bailabilidad`+`Tempo` replace `Año`+`Ventas_Globales` for the guided
  demo and Ejercicio 1, `Energia` replaces `Ventas_NA` for Ejercicio 2 —
  same structural-grading design as before (unchanged, still not a
  value-lookup — see the entry below for why). Re-validated empirically
  from scratch, not assumed to transfer from the vgsales numbers: unscaled
  k-means on `{Bailabilidad, Tempo}` still shows the same
  scale-domination effect (Tempo range ≈30-243 BPM dwarfs Bailabilidad's
  0-1), and the cluster×`Genero` crosstab is now a *stronger* proof that
  clusters ≠ genres (top genre per cluster ≈1.9-2.6% of 114 possible, vs.
  vgsales's ≈22% of 12 possible) since Spotify audio features don't
  correlate with genre nearly as tightly as sales figures correlate with a
  game's platform-era. One real difference in findings, reflected honestly
  rather than copied from nb5/vgsales: adding `Energia` for Ejercicio 2
  changes the grouping *moderately* (Adjusted Rand Index ≈0.53), not
  "barely at all" (vgsales's `Ventas_NA` gave ARI≈0.97) — `Energia` is only
  weakly correlated (r≈0.13/0.24) with the other two features, so it
  carries genuinely new information. `grade-reflexion/index.ts`'s
  `nb6_ex2`/`nb6_final` `GRADING_NOTES` grounding numbers updated to match.
  Full detail, including why vgsales was chosen as a stand-in in the first
  place, in `WORKFORCE_HANDOFF.md`'s 2026-09-19 Done log (second entry).
- 2026-09-19 — §2/§5 updated: Week 7 ("Misión 4: El Cartógrafo de
  Patrones") built — first (and only) notebook of this mission,
  `nb6_clustering.ipynb` / `autograder_nb6.py` / `build_nb6.py` in new
  folder `course-python-stats/Week 7/`, one notebook/one session, same
  pattern as nb5 vs. Misión 3. Direct user request with a full
  section-by-section beat sheet (visualize-before-formalizing opener,
  unscaled-then-scaled guided k-means demo, a structural 🧩 check that
  clusters don't match real game genres, two autograded exercises, 5
  theory questions, a closing reflection, a bonus "different k" reto, two
  checkpoints). **Dataset**: `vgsales_es.csv` (already used in
  `nb1_semana2`, Weeks 1-2 — no new dataset introduced, lower GAUSS-vetting
  risk per ticket #7) — `Año`+`Ventas_Globales` for the guided demo and
  Ejercicio 1, `Ventas_NA` added for Ejercicio 2. Chosen over the
  beat sheet's original danceability/tempo (Spotify) placeholder example
  because no such CSV exists in this repo; `Año` vs. `Ventas_Globales` was
  verified empirically (before writing any notebook cell) to reproduce the
  same "unscaled k-means bands on the larger-magnitude feature" effect.
  **§5 scope addition**: `sklearn.preprocessing.StandardScaler` added to
  the technical spine — was missing even though `KMeans` was already
  listed; scaling is a Week 7 statistical non-negotiable per `04_GAUSS.md`,
  not optional. **Scoring**: `_CORE_MAX` = 102 (mirrors nb5's total,
  coincidentally), `_BONUS_MAX` = 10. **Grading design differs from
  nb3/4/5**: ex1/ex2/reto1 are graded structurally (fitted `KMeans` with
  the right `n_clusters`, cluster centers in a scaled-data-plausible range)
  rather than against a hardcoded lookup of exact values — a literal
  cluster-index lookup would be both fragile across sklearn versions and
  pedagogically self-contradictory, since Concepto 3 explicitly teaches
  that the cluster index itself is arbitrary. **Validated**
  (`Week 7/_test_nb6.py`): 45/45 assertions, plus every real guided/demo
  code cell from the built `.ipynb` re-run end-to-end against the real CSV
  and a fully-correct worked solution scored 100% through the live
  `Autograder` with no exceptions. `supabase/functions/grade-reflexion/
  index.ts`: `"nb6"` added to `EXPECTED_NOTEBOOKS` and `nb6_ex2`/`nb6_final`
  added to `GRADING_NOTES` *before* shipping, avoiding the exact allowlist
  bug nb3/nb4/nb5 each hit first. Full detail in `WORKFORCE_HANDOFF.md`'s
  2026-09-19 Done log entry.
- 2026-09-14 — §2 updated: two more user-requested changes to Week 6's nb5
  before ship. (1) `mi_prediccion_x = "___"` bare-variable cells (the
  🔮/🧩 "no se califica" ones from the 2026-09-13 pre-ship pass) replaced
  with the same HTML/JS submit-widget pattern as the AI reflexions, minus
  the DeepSeek call — 1 XP each for a non-placeholder submission, raw text
  stored in `submissions.score_breakdown` (JSON column, no migration) so
  these can be reviewed by SQL instead of opening every student's Colab.
  `_CORE_MAX`: 100 → 102. (2) Fixed a real icon-legend collision:
  `nb5-guiado-md`'s section header reused 🔮 (the legend's own PREDICE
  icon) for a section that isn't a prediction prompt — swapped for ✨, and
  the legend gained a new 📝 ANOTA row for the after-the-fact reflection
  cell (the 🔮/📝 distinction is before-vs-after seeing the answer, not
  interchangeable). Added `---` separators at 5 major section boundaries
  for scannability (no content change). `_test_nb5.py`: 40 → 46 assertions.
  (3) Two new visuals, picked from proposed options: an explained/
  unexplained stacked-bar for Concept 2's existing R² values, and a
  90/10 train/test split scatter for Concept 3 (previously text-only).
  `nb5_regresion.ipynb`: 58 → 60 cells, pure content, no scoring change.
  Full detail in `WORKFORCE_HANDOFF.md`'s 2026-09-14 Done log entry.
- 2026-09-13 — Pre-ship review of Week 6 (below) caught a real blocker:
  `grade-reflexion/index.ts`'s notebook allowlist was never updated for
  `"nb5"` — same class of bug as the 2026-08-21 nb3/nb4 incident documented
  in that file, about to repeat on day one. Fixed, plus `nb5_`-prefixed
  `GRADING_NOTES` entries (namespaced so nb6/nb7 won't collide the way
  nb3/nb4's generic ids would have), matching `autograder_nb5.py` call
  sites, a strengthened `interpretacion_ex1` heuristic, and four
  pure-content notebook fixes (no scoring/contract change). A live
  round-trip against the deployed Edge Function is still outstanding —
  local tests can't verify server-side allowlist/key config.
  **Scope change, user-approved**: also added `check_t5` (a coefficient-
  scale MCQ — "Apoyo social" has a bigger coefficient than "PBI per
  cápita," does that make it more important?), assessing the caveat
  already stated once in `nb5-guiado-paso6-md` but never tested.
  `_CORE_MAX`: 95 → 100 (t1-4 → t1-5 in `check_mini_b`'s checkpoint too).
  Declined for this pass: moving `interpretacion_ex1` to DeepSeek grading
  (a fourth network-dependent call in the 40-pt core exercise, held back
  until the `nb5_`-prefixed reflections above survive a real concurrent-
  class load). `_test_nb5.py`: 32 → 40 assertions. Full detail in
  `WORKFORCE_HANDOFF.md`'s third 2026-09-13 Done log entry.
- 2026-09-13 — §2 updated: Week 6 ("Misión 3: El Oráculo de Datos") built —
  first notebook of this mission, `nb5_regresion.ipynb` /
  `autograder_nb5.py` / `build_nb5.py` in new folder
  `course-python-stats/Week 6/`, one notebook/one session per direct user
  request. Reuses `2019_es.csv` (World Happiness) for an ungraded guided
  example (train/test split, R², coefficient interpretation, an
  extrapolation-breaks-it demo) and `athlete_events_es.csv` (Olympics) for
  two autograded exercises predicting `Altura`. Scope decision: the
  requested predictor menu {Edad, Peso, Sexo, Deporte} was cut to
  {Edad, Peso, Sexo_num} — `Deporte` has 66 categories and one-hot encoding
  it is outside §5's technical spine; `Sexo` is converted to a 0/1 column
  in a guided (not student-written) cell. `_CORE_MAX` = 95, `_BONUS_MAX` =
  10 (see §2 table). Full detail, scoring rationale, and R²-lookup
  methodology in `autograder_nb5.py`'s module docstring. Validated via
  `Week 6/_test_nb5.py` (ATLAS-style, `COURSE_TEMPLATE.md` §3 pattern):
  32/32 assertions pass, plus a full end-to-end run of the notebook's own
  code cells against the real CSVs feeding a 100%-score integration test
  through `resumen()`. Not yet pushed to `main` — the `!wget` URLs in
  `build_nb5.py`'s setup cell won't resolve for real students until this
  folder is committed and pushed. See `WORKFORCE_HANDOFF.md` Done log,
  2026-09-13 entry.
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

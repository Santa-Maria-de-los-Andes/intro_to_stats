# Workforce Handoff Tracker — SMA Intro Stats

**Owner:** SOFIA. Open tickets by owning agent, a Done log, accepted risks/scope cuts, and open
escalations. Edited in place; never forked into version-suffixed copies. Companion file:
`WORKFORCE_CONTRACT.md` (the interface every agent builds against).

---

## Open Tickets

| # | Ticket | Owner | Notes |
|---|---|---|---|

| 7 | Statistically vet Weeks 3–4, 6, 7 candidate datasets and Week 5 debunk material once SOFIA drafts them | GAUSS | **Weeks 3–4 now drafted 2026-08-14** (see Done log) — dataset not yet downloaded/vetted, this is the blocking half of the ticket for that unit now. Weeks 1–2 datasets vetted and approved 2026-08-05. Week 5 debunk material still not drafted. **2026-08-29:** `proyecto_investigacion.ipynb`'s student-chosen datasets (menu still pending — see that Done log entry) will ship without formal GAUSS vetting given the timeline; accepted scope cut since nothing in that notebook is autograded (no exact-value answer key at risk). Flagging here as a fast-follow sanity-check once the dataset menu is finalized. **Week 6 (nb5) reused already-vetted Weeks 1–2/3–4 datasets — see 2026-09-13 Done log, low residual risk, not formally closed.** **2026-09-19: Week 7 (nb6) first used a reused dataset** (`vgsales_es.csv`, Weeks 1–2), **then the same day the user provided a genuinely new one** (`spotify.csv`, the Kaggle Spotify Tracks Dataset — 114,000 tracks, 114 genres) which nb6 was rebuilt around (see the second 2026-09-19 Done log entry). ATLAS ran an empirical dataset-suitability check before building both versions (unscaled-vs-scaled k-means behavior, cluster×Genero crosstab) documented in `autograder_nb6.py`'s docstring, but this is ATLAS's own build-time sanity check, not a formal GAUSS Dataset Vetting Report — a real GAUSS pass is more clearly warranted now than it was for the vgsales stand-in, since Spotify is a genuinely new, unreviewed dataset for this course, not a reuse of an already-vetted one. Still open. |
| 8 | Draft statistically defensible model answers for the capstone's "descriptive analysis with interpretation" and "correlation analysis with causation critique" criteria (20 pts each) | GAUSS + ATLAS | Needed before ATLAS's Rubric Validation Report can sign off those two criteria as more than a point value. |
| 12 | Rewrite debug-cell hint comments so they prompt investigation ("read the error, identify the type") rather than naming the bug directly — currently several debug cells hand over the diagnosis in the comment, undercutting the "build error-reading skill" purpose of `check_debugN` (`COURSE_TEMPLATE.md` §4) | SOFIA | Raised in SOFIA's Mode 3 review 2026-08-05 (see Done log), still not fully applied. **Partial incidental progress 2026-08-11**: while renumbering Semana 2's debug cells (see that Done log entry), `debug0` (Seccion C, the `=` vs `==` bug, old `debug2`) had its hint de-scaffolded from naming the bug outright to "ejecuta, lee el mensaje completo, e identifica que tipo de error es" — a side effect of the renumbering pass, not a deliberate sweep. Semana 2's `debug1` (Seccion C, `and`/`or`, old `debug3`) and Semana 1's `debug1` still hand over the diagnosis; not touched. |

---

## Done Log

- 2026-09-21 — **Week 7 (nb6) simplified back down: `check_ex2`/`check_ex3` removed as graded
  builds, same day they were added (see the Done log entry directly below).** User request, after
  a full re-read of `nb6_clustering.ipynb`: Semana 7 is "extra credit for those who have made good
  strides on previous content," so it should be mostly showcase + interpretation, with simple
  exercises — not three separate `🔨 CONSTRUYE` builds (ex1 40 + ex2 20 + ex3 20 = 80 pts of
  from-scratch code, ex3 in particular re-deriving a full train/test/scale/fit/predict pipeline
  the guided demo directly above it already walked through). Changes, all in
  `course-python-stats/Week 7/`: **(1)** Ejercicio 2 ("agrega Energia") stopped being a graded
  build — it's now an ungraded `👀 OBSERVA` showcase cell (`nb6-demo-energia-*` in `build_nb6.py`),
  moved to BEFORE Ejercicio 1 so it can inform the student's own predictor choice. **(2)** Ejercicio
  1 now accepts 2 OR 3 predictors from the menu (was exactly 2), so one build covers what used to
  be two separate exercises — same 40 pts. **(3)** Ejercicio 3 (the train/test build) removed
  entirely; the concept is still taught (guided demo, unchanged) and still assessed
  (`refl_generalizacion`, kept, reworded to reference "the guided demo above" instead of "your
  Ejercicio 3"). `refl_ex2` also kept (same reason: comparing the student's own Ejercicio 1 against
  the Energia showcase, not "Ejercicio 1 vs. Ejercicio 2"). Both reflections kept their internal
  ids (`nb6_ex2`, `nb6_generalizacion`) specifically so `grade-reflexion/index.ts` wouldn't need an
  `EXPECTED_NOTEBOOKS`-style change — only that function's `question`/`grounding`/`grading_notes`
  text for those two ids were rewritten to match, which **does still require redeploying
  `grade-reflexion`** for the new wording to reach production (not done as part of this change).
  `_CORE_MAX`: 127 → 87 (-20 ex2, -20 ex3, ex1 unchanged at 40). `mini_a`/`mini_b` checkpoints and
  the `explorador_completo` achievement (was ex1+ex2+ex3 perfect; now ex1 perfect + all three
  reflections submitted) updated to match. Validated (`Week 7/_test_nb6.py`): 47/47 assertions,
  including a new 3-predictor pass case for `check_ex1` (previously only tested with exactly 2).
  Full rationale in `autograder_nb6.py`'s module docstring and `build_nb6.py`'s.
- 2026-09-21 — **Lecture guide built: `course-python-stats/Week 7/Guion_Clase_Semana7_Clustering.md`**
  (SOFIA + GAUSS, user-requested outline for the live class preceding `nb6_clustering.ipynb`'s
  practice session, same convention as the Week 6 guide below). ~45-minute teacher-facing script
  covering the notebook's own four concepts in order (how k-means iterates, why scaling is
  non-negotiable, why cluster labels/indices are arbitrary and clusters ≠ real genres, whether a
  clustering generalizes) plus a hook that explicitly contrasts unsupervised clustering against
  last week's regression ("no respuesta correcta"), a live embodied centroid-and-reassignment
  dynamic for Concepto 1, and a GAUSS misconception checklist. **Numbers recomputed, not
  invented**: re-ran the notebook's exact pipeline against `spotify_es.csv`
  (`KMeans(n_clusters=3, random_state=42, n_init=10)`, `StandardScaler`,
  `train_test_split(test_size=0.1, random_state=42)`) to confirm n=113,842 after cleaning, the
  unscaled-vs-scaled centroid reveal, cluster×Genero purity (all ≈2–3%, consistent with the
  notebook's ~1/114≈0.9%-by-chance baseline), and near-identical train/test cluster profiles —
  all match what `nb6_clustering.ipynb` itself computes at runtime, not placeholders.
- 2026-09-21 — **Week 7 (nb6) got a third exercise + reflection: a
  train/test-style generalization check for clustering.** User question
  (in conversation, not a ticket): nb5 (Week 6) taught train/test split
  specifically to catch overfitting on a known regression target — should
  nb6 (k-means, unsupervised) have an analogous "test accuracy" exercise
  now that train/test was already introduced?
  **Why not literal "test accuracy"**: k-means has no ground-truth label
  to score right/wrong against, and Concepto 3 of this same notebook
  explicitly teaches that cluster indices/labels are arbitrary — grading
  "accuracy" against something like `Genero` would directly contradict
  that lesson (and the existing `check_cluster_es_genero` 🧩, which proves
  clusters ≠ real genres). **What transfers instead**: generalization/
  stability — fit `KMeans` SOLO on a train split, use `.predict()` (never
  re-fit) on a held-out test split, and check whether cluster *profiles*
  (not indices) hold up on data the model never saw. Framed with two
  concrete downstream use cases discussed with the user rather than an
  abstract "how good is this model" question: (a) song recommendation —
  assign a brand-new song to a cluster via `.predict()` and recommend
  other songs from that cluster; if clusters don't generalize, the
  recommendation is unreliable; (b) segmentation — a business decision
  (marketing budget by "song type") based on a clustering that looks
  different every time it's refit on a new sample isn't trustworthy.
  **Notebook (`build_nb6.py`)**: added Concepto 4 (the "why" above,
  inserted between Ejercicio 2's reflection and the theory quiz), a guided
  demo (`nb6-guiado-generaliza-*`, train/test split + scaler fit on train
  only + `KMeans` fit on train only + `.predict()` on test, comparing
  cluster profiles), Ejercicio 3 (`nb6-ex3-*`, 20 pts, student repeats the
  pattern with their own 2-3 predictors), and a new reflection
  (`nb6-ex3-reflexiona-*`, +5 XP, ties a hypothetical train/test mismatch
  to a concrete failure for recommendation or segmentation).
  **Autograder (`autograder_nb6.py`)**: new `check_ex3` (structural, same
  philosophy as ex1/ex2 — verifies a fitted+scaled `KMeans` on train plus
  a plausibly-sized array of valid cluster labels for the test set, never
  a hardcoded value lookup) and `check_reflexion_generalizacion`. New
  helper `_menciona_train_test_o_numero`. `_CORE_MAX` 102→127 (+20 ex3,
  +5 refl_generalizacion). `mini_b` checkpoint's tracked section and the
  `explorador_completo` achievement (now ex1+ex2+ex3, was ex1+ex2) updated
  to match. **`supabase/functions/grade-reflexion/index.ts`**: added the
  `nb6_generalizacion` rubric (question/grounding/grading_notes) next to
  the existing `nb6_ex2`/`nb6_final` entries. **Validated**
  (`Week 7/_test_nb6.py`, extended with `train_test_split` + new
  `check_ex3` assertions — correct solution, undersized test array,
  unscaled model, float instead of int labels, out-of-range cluster
  label, generic interpretation, empty submission): 56/56 assertions pass.
  The new guided demo cell was also re-run directly against the real
  `spotify_es.csv` outside the test harness to confirm the pedagogical
  point actually holds on this dataset (not just that the code runs):
  train vs. test cluster means came out nearly identical (e.g.
  Bailabilidad 0.417 train / 0.416 test, Tempo 93.47 train / 93.19 test
  for one cluster), so the "generalizes" claim the notebook makes is
  empirically true, not asserted on faith. `WORKFORCE_CONTRACT.md` §2's
  Week 7 row and Change Log updated to match.

- 2026-09-19 (same day, second pass) — **Week 7's nb6 rebuilt around a
  real Spotify dataset, superseding the entry directly below.** The user
  added `course-python-stats/Week 7/spotify.csv` (Kaggle's "Spotify Tracks
  Dataset" — 114,000 tracks, 21 columns, 114 genres x 1,000 tracks each)
  and asked for column names and genres to be translated to Spanish and
  the notebook rebuilt around it. This is exactly the dataset the original
  beat sheet had asked for (danceability/tempo) — the vgsales substitution
  documented in the entry below was only ever a stand-in for the fact that
  no such CSV existed in the repo yet.
  **New `Week 7/translate_to_spanish.py`** (same pattern as
  `Weeks 1-2/translate_to_spanish.py`): renames all 21 columns to Spanish
  (`Bailabilidad`, `Energia`, `Tempo`, `Genero`, etc.) and translates all
  114 genre values — genre names already used as-is in Spanish-language
  music contexts (rock, pop, k-pop, death-metal, hip-hop...) were kept in
  their international form rather than translated literally (translating
  "hip-hop" word-for-word would not read as real Spanish); demonyms
  (brazil→Brasil, british→Británica) and descriptive pseudo-genres
  (children→Infantil, chill→Relajante, sleep→Para Dormir) were genuinely
  translated. Drops the leftover `Unnamed: 0` index column. Output:
  `spotify_es.csv` (114,000 rows, 20 columns) — the file the notebook
  actually loads; the original `spotify.csv` (English) is kept alongside
  it, same convention as `vgsales.csv`/`vgsales_es.csv`.
  **Rebuilt**: `build_nb6.py` → `nb6_clustering.ipynb` (still 46 cells,
  content only), `autograder_nb6.py` (docstring, predictor menu constants,
  the 12-genre list → all 114 translated genres, T2/T3/T5 theory questions,
  every error message referencing old column names), `_test_nb6.py`.
  **New real findings from re-running the empirical validation against
  this dataset from scratch** (not assumed to carry over from vgsales):
  after dropping 1 row with no artist/track name and 157 rows with
  `Tempo` = 0 (a detection failure, not a real 0-BPM track — 113,842 rows
  remain), unscaled k-means on `{Bailabilidad, Tempo}` (k=3,
  `random_state=42`) still shows the same scale-domination effect
  (`Tempo` ≈30-243 BPM vs. `Bailabilidad` 0-1: raw cluster centers move
  91→167 BPM but only 0.50→0.61 in `Bailabilidad`); scaled, the 3 clusters
  come out size-balanced (≈52k/35k/27k) and now separate on both axes
  (`Bailabilidad` 0.42/0.48/0.71). The cluster×`Genero` crosstab is an
  even sharper proof against "clusters = genres" than vgsales gave: with
  114 real genres, the most common genre inside any cluster never exceeds
  ≈2.6% of that cluster (vs. vgsales's ≈22% of 12 genres) — barely above
  the ≈0.9% base rate pure chance would give. **One finding genuinely
  differs from nb5/vgsales, reported honestly instead of reused**: adding
  `Energia` for Ejercicio 2 changes the grouping *moderately* (Adjusted
  Rand Index ≈0.53 between the 2-feature and 3-feature scaled
  clusterings) rather than "barely at all" — `Energia` is only weakly
  correlated with `Bailabilidad` (r≈0.13) and `Tempo` (r≈0.24), so unlike
  vgsales's `Ventas_NA` (r≈0.94 with `Ventas_Globales`, ARI≈0.97 →
  redundant), it carries real new information. The `check_ex2` debrief
  markdown and `grade-reflexion/index.ts`'s `nb6_ex2` grounding were
  written to match this actual result.
  **Structural-grading design unchanged** (still the right call, re-
  confirmed against this dataset): `_parece_escalado`'s `tol=50` threshold
  — set for vgsales's more extreme scaled-outlier centroids (up to ≈17) —
  was re-checked against Spotify's much gentler scaled centroids (never
  above ≈1.3 with k=3 or k=4) and still discriminates correctly with a
  huge margin in both directions; no change needed to that helper.
  **Validated**: `_test_nb6.py` 45/45 (same assertions, ground truth
  refit against `spotify_es.csv`), every real guided/demo cell from the
  rebuilt `.ipynb` re-run end-to-end against the actual CSV, and a
  fully-correct worked solution scored 100% through the live `Autograder`
  with no exceptions. `supabase/functions/grade-reflexion/index.ts`:
  `nb6_ex2`/`nb6_final` `GRADING_NOTES` grounding numbers updated to the
  real Spotify figures above (ARI≈0.53, corr≈0.13/0.24, ≈2.6% max genre
  share) — brace/paren-balance checked, `"nb6"` was already in
  `EXPECTED_NOTEBOOKS` from the entry below so no allowlist change needed
  here.
  **Not yet done**: same open items as the entry below (not pushed to
  `main`, no `nb6.html`, GAUSS dataset vetting for Week 7 still an ATLAS
  build-time check rather than a formal report — arguably more warranted
  now since this is a genuinely new dataset, not a reused one).
- 2026-09-19 — **Week 7 built: `nb6_clustering.ipynb`, "Misión 4: El
  Cartógrafo de Patrones"** — direct user request with a full
  section-by-section beat sheet (visualize-before-formalizing opener with
  an ungraded 🔮 prediction on a raw unlabeled scatter, plain-language
  k-means mechanism, guided demo fit unscaled then rescaled with
  `StandardScaler`, a printed cluster×Género crosstab feeding a structural
  🧩 check that clusters do NOT match real game genres, two autograded
  exercises, 5 theory questions, a closing AI-graded reflection, a bonus
  "rerun with a different k" reto, two checkpoints). New folder
  `course-python-stats/Week 7/`: `build_nb6.py` → `nb6_clustering.ipynb`
  (46 cells), `autograder_nb6.py`, `_test_nb6.py`.
  First (and only) notebook of Misión 4 — `check_ex`/`check_t`/`check_reto`
  numbering starts fresh at 1, same "one notebook, one session" pattern as
  nb5 vs. Misión 3 (`WORKFORCE_CONTRACT.md` §2).
  **Dataset**: `vgsales_es.csv` (16,598 video games, already used in
  `nb1_semana2` — Weeks 1-2), reused rather than introducing a new one.
  The user's original beat sheet used danceability/tempo (a Spotify-style
  dataset) purely as an illustrative example of "two features on very
  different scales" — no such CSV exists anywhere in this repo, and
  downloading one from the internet would have introduced an unvetted
  dataset (ticket #7) with no reproducibility guarantee. `Año` (release
  year, magnitude ≈2000) and `Ventas_Globales` (global sales in millions,
  magnitude <1 for most rows) reproduce the same "unscaled distance
  dominated by the larger-magnitude feature" effect — verified empirically
  *before* writing a single notebook cell, not assumed: unscaled k-means
  (k=3, `random_state=42`) on these two columns produces clusters that are
  almost pure `Año` bands (1980-2000 / 2001-2007 / 2008-2020); scaled
  k-means on the same columns surfaces a genuine 76-game "blockbuster"
  cluster (Ventas_Globales ≥ 8.84M) that the unscaled version couldn't see
  at all. `Ventas_NA` was added for Ejercicio 2 (chosen over `Ventas_JP`,
  which is 63% zeros — too zero-inflated to cluster meaningfully).
  **Bonus finding used directly in the notebook's pedagogy**: `Género`
  (12 real genres: Acción, Deportes, Rol, ...) was never given to k-means
  as a predictor, but is used in a guided cross-tab to show live that no
  cluster's most-common genre exceeds ~23% of that cluster — concrete,
  real-number evidence for Concepto 3 ("cluster labels are arbitrary until
  you interpret them") and directly operationalizes `04_GAUSS.md`'s Week 7
  risk row ("interpretation text must not treat cluster labels as
  fixed/meaningful IDs") as a gradeable, objective-answer exercise
  (`check_cluster_es_genero`) instead of just a warning in prose.
  **§5 scope addition (documented in `WORKFORCE_CONTRACT.md`, not silent)**:
  `sklearn.preprocessing.StandardScaler` added to the technical spine —
  the committed spine listed `KMeans` but never `StandardScaler`, even
  though scaling before fitting is the Week 7 statistical non-negotiable
  `04_GAUSS.md` names explicitly; without it the notebook's own Concepto 2
  demo has nothing to show.
  **Grading design deliberately differs from nb3/4/5's exact-value lookup
  pattern**: `check_ex1`/`check_ex2`/`check_reto1` verify structural
  properties (a real, fitted `KMeans` with the right `n_clusters`; cluster
  centers falling in a plausible range for *standardized* data rather than
  the raw `Año`/`Ventas_*` range) instead of a hardcoded lookup keyed by
  predictor combination. This is deliberate, not a shortcut: unlike
  `LinearRegression` (closed-form, deterministic regardless of sklearn
  version), the specific index number k-means assigns to "the blockbuster
  cluster" is not portable across sklearn versions/`n_init` settings — the
  same fact Concepto 3 teaches. Hardcoding "the blockbuster cluster is
  index 2" would have been both fragile and pedagogically self-defeating.
  The scaled-vs-unscaled structural check itself needed one empirical
  correction while building: an initial `tol=8.0` on
  `max(abs(cluster_centers_))` rejected a genuinely-correctly-scaled
  reference solution, because a small cluster of extreme sales outliers
  can legitimately average out to a z-score of 10-17 (verified directly
  against the real data before shipping) — raised to `tol=50.0`, still
  ~40x below the raw `Año` magnitude that flags an unscaled fit.
  **Scoring**: `_CORE_MAX` = 102 (2 registro + 5 cluster_es_genero + 25
  t1-5 + 40 ex1 + 20 ex2 + 5 refl_ex2 + 5 refl_final — coincidentally
  matches nb5's total, not intentionally tuned to match), `_BONUS_MAX` =
  10 (reto1). Same "showcase, not deep dive" trim below the nominal ~120
  `WORKFORCE_CONTRACT.md` §2 figure as nb4/nb5's own trims.
  **Theme**: "El Cartógrafo de Patrones" — forest-green/amber "map/
  exploration" palette, distinct from nb3/4's warm sun and nb5's violet/
  cyan mystic per `COURSE_TEMPLATE.md` §5's per-notebook theming
  convention. Built by cloning `autograder_nb5.py`'s engine (registration
  form, `_award`, `_check_achievements`, checkpoint/level-up rendering,
  Supabase submit, theory/reflection/registro widgets — all reused
  verbatim) via a scripted palette/text substitution pass (documented as
  such rather than left implicit), then hand-writing the new predictor
  menu, structural checks, `_TEORIA` dict, achievements, and every
  `check_*` method fresh for k-means. One theming bug from nb5 was
  deliberately NOT propagated: nb5's `_award()` success message read
  "¡RAYO DE SOL COMPLETO!" ("ray of sunshine," a leftover from nb3/4's warm
  palette that the nb5 reskin pass missed) — nb6 uses on-theme
  "¡ZONA DEL MAPA COMPLETA!" instead. Not fixed in nb5 itself (out of
  scope for this session) — flagging here so whoever next touches
  `autograder_nb5.py` sees it instead of copying it forward again.
  **Validated** (`Week 7/_test_nb6.py`, ATLAS-style throwaway script,
  `COURSE_TEMPLATE.md` §3 pattern): 45/45 assertions — every `check_*`
  tested against a real, correctly-scaled solution (fit fresh against the
  actual CSV in the test script itself) and a realistic wrong case each
  (predictor outside the menu, unscaled model, unfitted model, out-of-range
  cluster index, interpretation treating a cluster as a fixed genre,
  generic/placeholder text, `k_reto1` equal to 3). `_CORE_MAX`/`_BONUS_MAX`
  arithmetic verified equal to the declared sums. Separately ran every real
  guided/demo code cell from the built `.ipynb` itself end-to-end against
  the actual CSV (non-interactive `MPLBACKEND=Agg` to avoid a GUI-backend
  hang on `plt.show()` — noted here since it cost real debugging time),
  then fed a fully-correct worked solution through the live `Autograder` to
  a 100%-score `resumen()` with no exceptions.
  **`supabase/functions/grade-reflexion/index.ts` updated *before* shipping
  this time**: `"nb6"` added to `EXPECTED_NOTEBOOKS` and `nb6_ex2`/
  `nb6_final` added to `GRADING_NOTES` (with real grounding numbers: ARI
  ≈0.966 between the 2-feature and 3-feature scaled clusterings, since
  corr(Ventas_Globales, Ventas_NA)≈0.941) — this exact allowlist bug hit
  nb3/nb4 (2026-08-21), then nb5 (2026-09-13) before being caught; nb6 is
  the first notebook in this course to get it right on the first pass.
  Brace/paren balance-checked (still no Deno CLI in this session — same
  caveat as nb5, flagging `deno check` as the one remaining pre-ship step
  for whoever deploys it).
  **Not yet done**: not pushed to `main`, so `build_nb6.py`'s `!wget` URLs
  (`Week%207/autograder_nb6.py`, reusing `Weeks%201-2/vgsales_es.csv`)
  won't resolve for real students until that happens. No `nb6.html` public
  leaderboard page built (nb5 doesn't have one yet either as of this
  writing). GAUSS dataset vetting for Week 7 (ticket #7) is ATLAS's own
  empirical build-time check, not a formal GAUSS Dataset Vetting Report —
  still open. Deadline set to 5 October 2026, 11:59 PM Peru (two weeks
  after nb5's, same cadence nb5 used after nb4) — a placeholder pending the
  user's actual class schedule confirmation, not verified against a real
  syllabus.
- 2026-09-14 — **Two more user-requested fixes to Week 6's nb5, on top of
  the 2026-09-13 pre-ship review below.**
  **(1) Registro widget for the "just write something" cells.** The two
  `mi_prediccion_x = "___"` bare-variable cells added in the 2026-09-13
  pre-ship pass (`nb5-visual-predice-code`, `nb5-concepto-linea-pausa-code`)
  were never scored and never left any trace anywhere — reviewing what a
  student actually wrote meant opening their Colab individually, same
  friction the user is trying to get away from. Replaced both with the
  same HTML/JS submit-widget pattern the AI reflexions already use
  (`_ask_reflexion`'s textarea+button UI, Colab `kernel.invokeFunction`
  round-trip), minus the DeepSeek call: new `_ask_registro`/
  `_grade_registro`/`_award_registro` methods in `autograder_nb5.py`,
  callback `_ag_registro_answer`, keys `reg_linea_roja` (`check_prediccion_linea`)
  and `reg_minimiza_distancia` (`check_anota_distancia`). 1 XP each for any
  non-placeholder submission (same `_is_nontrivial_text` guard as
  reflexions, `min_len=3` since these are one-line thoughts, not full
  reflections) — no AI grading, no way to get it "wrong" beyond leaving it
  blank. **The actual text rides along in `submissions.score_breakdown`**
  (a new `"text"` key per entry in that existing JSON column — no schema
  migration) specifically so these can be reviewed with a SQL query across
  every student at once instead of opening each notebook, which was the
  user's explicit ask. Added `self._text_answers` to track pending text
  before it's persisted, and made sure the registration-form restore path
  repopulates it from a returning student's last `score_breakdown` —
  otherwise the next `_submit_to_supabase()` call (e.g. from `resumen()`)
  would have rebuilt `score_breakdown` from a scratch/empty
  `_text_answers` and silently dropped a prior session's stored text.
  `_CORE_MAX`: 100 → 102.
  **(2) A real icon-legend collision, not just a wording nit.**
  `nb5-guiado-md`'s section header used 🔮 — the *same emoji the shared
  legend defines as PREDICE* ("write your prediction before seeing the
  result") — for a section that is not a prediction prompt at all, just
  the guided example's title. Since 🔮 is genuinely double-booked in this
  notebook (it's also the mission's own crystal-ball theme/branding —
  title, level names, achievement icons — which is fine there since that
  context is never confused with "this cell wants your prediction"), the
  fix was to swap this one specific *section-header* usage for ✨ rather
  than touch the branding. Audited every other markdown header against the
  9-icon legend for the same class of bug (an icon the legend defines,
  reused for something the legend doesn't mean) — found none: `🧠`/`💥`/
  `🏟️`/`🎯` headers are all decorative, not legend icons, so they don't
  make a false claim. Fixed the deeper cause too: 🧩 COMPLETA ("replace
  `___` with the correct value" — implies one correct answer) was already a
  mismatch for the concept-1 pause cell before this fix (there is no single
  correct value, it's an open explanation) — since that cell is now part of
  fix (1) above and genuinely open-ended with no right answer, gave the
  legend a new row, 📝 ANOTA, rather than keep stretching 🧩 or 💭 (💭's own
  legend text explicitly says "AI-graded... +5 XP," which would have been
  inaccurate for a 1-point non-AI cell). The 🔮/📝 split is intentional: 🔮
  = before you see the answer (a prediction), 📝 = after (a reflection) —
  not interchangeable, both now correctly described in `LEYENDA_ICONOS`.
  **(3) Added `---` separators at 5 major section boundaries**
  (entering Concept 1, the guided example, "míralo romperse," the Olympics
  dataset switch, Ejercicio 2, and the bonus Reto) for scannability — no
  content change, matches the separator convention already used before the
  quiz/final-reflection/cierre sections.
  All changes made in `build_nb5.py` first, then the notebook regenerated
  from it (57 → 58 cells, unchanged from the check_t5 pass — this round
  edited cell content and metadata, not cell count, except where check_t5
  itself added one). `_test_nb5.py`: 40 → 46 assertions (registro
  score/lock/placeholder behavior, `_text_answers` capture, and the same
  `check_*` → `_ask_registro` id-wiring check already used for reflexions).
  `WORKFORCE_CONTRACT.md` §2 table and Change Log updated to `_CORE_MAX`=102.
  **(4) Two new visuals for Concepts 2 and 3, user chose from proposed
  options.** Concept 2 (R²) already had a 3-panel synthetic-scatter demo
  from the 2026-09-13 pass; user asked to also add a stacked-bar view
  (`nb5-concepto-r2-barra-code`, right after `nb5-concepto-r2-md`) showing
  the same three R² values from that section's own bullet list (1.0/0.72/
  0.0) as literal "% explicado vs. % sin explicar" bars — a second
  representation of the same numbers already in the text, not new content.
  Concept 3 (train/test) had no visual at all — added
  `nb5-concepto-traintest-visual-code` right after `nb5-concepto-traintest-md`:
  100 synthetic points split 90/10 (`np.random.RandomState(3).permutation`),
  train colored cyan and test colored gold (matching the notebook's own
  accent palette), literally showing the split the text just described.
  User declined the alternative "overfitting demo" (polynomial overfits
  train, fails test) for now — noted as a good candidate to revisit nearer
  T3's quiz question if a stronger visual is wanted there later. Both cells
  reuse `np`/`plt`/`LinearRegression` already imported by earlier cells in
  the same kernel (no new imports needed at the top of the notebook).
  `nb5_regresion.ipynb`: 58 → 60 cells. `_test_nb5.py` unaffected (pure
  content, no `check_*`/scoring change) — still 46/46.
- 2026-09-13 — **Lecture guide built: `course-python-stats/Week 6/Guion_Clase_Semana6_Regresion.md`**
  (SOFIA + GAUSS, user-requested outline for the live class preceding `nb5_regresion.ipynb`'s
  practice session). Not a new notebook/autograder artifact — a ~45-minute teacher-facing script
  covering exactly the four beats the user asked for (engaging hook, best-fit line, train/test
  split, R², coefficient interpretation), sequenced to match the notebook's own concept order so
  the lecture primes the notebook rather than duplicating it verbatim. **Hook** ("Duelo de
  Oráculos"): a live human-vs-model prediction exercise using real, verified rows from
  `2019_es.csv` (Finlandia/Estados Unidos/España/México/Chile/Argentina/Japón PBI+Puntaje, Perú's
  PBI shown with Puntaje hidden as the guess target, revealed as 5.697) — same PBI↔Puntaje
  cliffhanger the notebook opens with, but experienced before it's read. Deliberately uses Japón
  (PBI≈Finlandia's but Puntaje ~2 points lower) to seed the "the pattern isn't perfect" question
  that Concept 2 (R²) later answers, instead of introducing that idea cold. **Numbers reused, not
  invented**: r≈0.794 (Misión 2 finding), guided-example test R²≈0.71, PBI per
  cápita/Apoyo social coefficients ≈0.77/≈1.16 — all pulled directly from `autograder_nb5.py`'s
  already-validated theory/reflection text (2026-09-13 build entry below), not recomputed or
  guessed for this doc. **GAUSS pass baked in as a checklist**, not a separate report: a
  "don't say / say instead" table at the end enforces this module's non-negotiables — R² framed as
  "% of variation explained" (never "accuracy"), coefficients framed with the "por cada unidad
  adicional... manteniendo las demás constantes" template (never causal language), explicit
  warning that a larger coefficient isn't automatically "more important" (scale-dependent), and a
  reminder that a decent R² doesn't certify predictions outside the training range — matching
  `04_GAUSS.md`'s per-week Week 6 risk row exactly. Closing block deliberately withholds the
  extrapolation "watch it break" reveal (teases it instead) so the notebook's own demo isn't
  spoiled. No changes to `nb5_regresion.ipynb`, `autograder_nb5.py`, or `_CORE_MAX` — this is a
  standalone teaching aid, not a graded artifact, and isn't referenced by any `!wget` setup cell.
- 2026-09-13 — **Week 6 built: `nb5_regresion.ipynb`, "Misión 3: El Oráculo
  de Datos"** — direct user request with a full section-by-section spec
  (Apertura callback to nb4's PBI↔Puntaje finding, visual-concept-before-
  code opener, guided World Happiness regression example, an
  extrapolation-breaks-it demo, two autograded Olympics-Altura exercises,
  4 theory questions, a closing reflection, two checkpoints). New folder
  `course-python-stats/Week 6/` (singular, matching the `Week 5/` pattern
  rather than `Weeks N-M/`, since this is one notebook/one session, not a
  multi-week split): `build_nb5.py` → `nb5_regresion.ipynb` (53 cells,
  revised same-day per user feedback below),
  `autograder_nb5.py`, `_test_nb5.py`.
  First notebook of Misión 3 — `check_ex`/`check_t`/`check_reto` numbering
  starts fresh at 1 rather than continuing Misión 2's (`WORKFORCE_CONTRACT.md`
  §2/§3), since there's no predecessor nb-file in this mission to continue
  from.
  **Datasets**: `2019_es.csv` (World Happiness, already used by nb3/nb4)
  for an ungraded guided example only; `athlete_events_es.csv` (Olympics,
  already used by nb1_semana2) for the graded exercises, predicting
  `Altura`.
  **Scope decision (documented in `autograder_nb5.py`'s docstring and
  `build_nb5.py`'s header comment, not a silent cut)**: the user's spec
  listed `{Edad, Peso, Sexo, Deporte}` as the predictor menu for Altura.
  `Deporte` has 66 categories — one-hot encoding it is outside the
  technical spine committed in `WORKFORCE_CONTRACT.md` §5 (no
  `pd.get_dummies`/`OneHotEncoder` anywhere in this course). Recut the menu
  to `{Edad, Peso, Sexo_num}` — `Sexo` becomes a 0/1 column in one guided
  (not student-written) preprocessing cell, with an explicit in-notebook
  note on why `Deporte` was left out rather than silently dropped. This
  narrows "2-4 predictors" to "2-3 predictores" in the exercise text.
  **Reproducibility choice**: both exercises require `test_size=0.1,
  random_state=42` (same split the guided example uses) so a specific
  predictor combination has one verifiable R² pair, not "approximately
  matching." All R² values were computed directly against the real CSVs
  on 2026-09-13 (206,165 rows after dropping nulls in
  Edad/Altura/Peso/Sexo) and hardcoded into `autograder_nb5.py`'s
  `_R2_LOOKUP`, keyed by frozenset of predictor names, tolerance ±0.02
  (wider than nb3/nb4's ±0.01 since sklearn-version drift matters more
  than sampling noise at this N).
  **Scoring**: `_CORE_MAX` = 95 (20 pts t1-4 theory, 5 refl_interpretacion,
  40 ex1, 20 ex2, 5 refl_ex2, 5 refl_final, all AI-graded reflections
  via the existing `grade-reflexion` Edge Function pipeline, mechanism
  unchanged from nb3/nb4) — since revised to 100 (t5 added, third
  2026-09-13 entry below) — well under the nominal ~150 `WORKFORCE_CONTRACT.md`
  §2 figure, same "showcase, not deep dive" reasoning as nb4's 2026-08-29
  trim, not treated as a new budget problem. `_BONUS_MAX` = 10 (`reto1`,
  "rompe el modelo" — extrapolate with an absurd input, structural check
  only since the "how absurd" varies by student's fitted model). First
  notebook in this course to declare a real `_BONUS_KEYS`/`_BONUS_MAX`
  split (nb3/nb4 had none) — `_totals()` was written to exclude bonus keys
  from the core percentage, per `COURSE_TEMPLATE.md` §6's skeleton.
  **Theme (compressed SOFIA/PIXEL/ATLAS pass, single session)**: "El
  Oráculo de Datos" — violet/cyan mystic palette, distinct from nb3/nb4's
  warm sun palette per `COURSE_TEMPLATE.md` §5's per-notebook theming
  convention (confirmed by checking nb1's own distinct Pokémon palette
  first, not assumed). 6-tier level curve unchanged (`WORKFORCE_CONTRACT.md`
  house rule); achievements/rarity labels renamed to fit (`Destello`/
  `Fulgor`/`Revelación`/`Visión Suprema`). Built by adapting
  `autograder_nb4.py`'s engine (registration form, `_award`,
  `_check_achievements`, checkpoint/level-up rendering, Supabase submit,
  theory/reflection widgets — all reused verbatim) via a scripted
  palette/text substitution pass, then hand-writing the new `_TEORIA`
  dict, achievements, and every `check_*` method fresh for this notebook's
  actual exercises.
  **Validated** (`Week 6/_test_nb5.py`, ATLAS-style throwaway script,
  `COURSE_TEMPLATE.md` §3 pattern): 32/32 assertions — every `check_*`
  tested against a correct solution (R² freshly recomputed from the real
  CSV in the test script itself, not trusted from the autograder's own
  lookup, so a drifted lookup would also be caught), a predictor outside
  the allowed menu, a hardcoded/lazy R², causal-language and placeholder
  interpretation text, an incomplete bonus submission, and the reflection
  pipeline's three states (simulated-AI-success, placeholder-no-network-
  call, network-failure-does-not-score-zero — same contract as nb3/nb4).
  `_CORE_MAX`/`_BONUS_MAX` arithmetic verified equal to the declared sums.
  Separately ran every real code cell from the built `.ipynb` itself
  (setup, guided example, break-it demo, Olympics preprocessing, and a
  worked solution for both exercises + the bonus) end-to-end against the
  actual CSVs, then fed those exact values through the live `Autograder`
  to a 100%-score `resumen()` with no exceptions — confirms the notebook's
  own code (not just the grader in isolation) is internally consistent
  with what `autograder_nb5.py` expects.
  **Not yet done**: not pushed to `main` yet, so `build_nb5.py`'s `!wget`
  URLs (pointing at `Week%206/autograder_nb5.py` etc. on the `main`
  branch, matching nb3/nb4's hosting pattern of raw-hosting directly from
  this repo rather than a separate grader repo) won't resolve for real
  students until that happens — flagged to the user, not pushed
  unilaterally. GAUSS dataset vetting for Week 6 (ticket #7) still
  outstanding — both datasets are reused from already-vetted units
  (Weeks 1–2, Weeks 3–4), not newly introduced, so the residual risk is
  low but not formally closed. Deadline set to 21 September 2026, 11:59 PM
  Peru (two weeks after nb4's, leaving Semana 5 — causation, no autograder
  — the week between) — a placeholder pending the user's actual class
  schedule confirmation, not verified against a real syllabus.
- 2026-09-13 — **Same-day follow-up to Week 6's build above, user-flagged
  pedagogy fix**: the guided World Happiness example (`nb5-guiado-code`)
  and the extrapolation "watch it break" demo (`nb5-rompe-code`) were each
  one pre-written code cell doing 4-6 things at once (define predictors →
  split → fit → train R² → test R² → coefficients, all in one block) — the
  user pointed out this is exactly the "gigantic block students never
  read" pattern `COURSE_TEMPLATE.md` §4's "theory → immediate mini-exercise
  → check" rule exists to prevent, even for a non-graded guided/OBSERVA
  section. Split into one cell per step, each preceded by its own short
  markdown explaining *that* step specifically (not a recap of the whole
  block): 6 md+code pairs for the guided example (predictors+target →
  split → fit → train R² → test R² → coefficients), 2 code cells for the
  break-it demo (show real ranges → build the absurd input and predict),
  with a one-line markdown transition between them. No values, variable
  names, or `check_*` contracts changed — `autograder_nb5.py` untouched.
  `nb5_regresion.ipynb` grew from 40 to 53 cells. Re-validated exactly as
  before: `_test_nb5.py` 32/32, plus every real code cell from the rebuilt
  notebook re-executed end-to-end against the actual CSVs (now cell-by-cell
  instead of block-by-block) with identical R² values to the pre-split
  version, then through the live grader to a clean `resumen()`.
- 2026-09-13 — **Third same-day pass on Week 6: pre-ship review caught a
  real blocker in the `grade-reflexion` wiring, plus cheap content
  polish.** A review of the just-built nb5 (see the two entries above)
  found `supabase/functions/grade-reflexion/index.ts`'s `EXPECTED_NOTEBOOKS`
  allowlist had never been updated for `"nb5"` — the exact bug documented
  in that file's own 2026-08-21 comment for nb3/nb4, about to repeat itself
  on day one of nb5. Every one of nb5's three AI-graded reflections
  (`refl_interpretacion`, `refl_ex2`, `refl_final`) would have 400'd against
  a real student's DNI, and the notebook shows that as a generic "problema
  de conexión," not a config error — silent until a live class hit it.
  **Fixed**: added `"nb5"` to `EXPECTED_NOTEBOOKS`; added three
  `GRADING_NOTES` entries, deliberately namespaced `nb5_interpretacion` /
  `nb5_ex2` / `nb5_final` rather than reusing nb3/nb4's generic
  `interpretacion`/`ex2`/`final` ids (those two never collided only because
  neither notebook cross-checks `notebook` against `reflexion_id` — nb6/nb7
  would eventually reuse those same generic names and reintroduce this
  exact class of bug; prefixing now is free and closes it for good).
  Updated the three matching call sites in `autograder_nb5.py`
  (`check_reflexion_interpretacion`/`_ex2`/`_final`). **Test gap also
  closed locally**: `_test_nb5.py` previously called `_grade_reflexion()`
  directly with hand-picked ids, so it could never have caught a
  `check_reflexion_*` → wrong-id typo like this one — added assertions that
  monkeypatch `_ask_reflexion` and confirm each `check_reflexion_*` method
  passes the correct `nb5_`-prefixed id. This still can't verify
  server-side config (the allowlist/`GRADING_NOTES` match) — only a real
  round-trip against the deployed Edge Function can, and that has **not**
  been run yet; flagging as the one remaining pre-ship step, same caveat
  raised when this was first reviewed.
  **Also while in there (all pure content, no `check_*`/scoring contract
  changed)**: fixed `nb5-visual-pregunta-md`'s self-contradiction (it told
  students "no code cell here, just think about it" directly under a
  legend that defines 🔮 as "write your prediction") by giving it an actual
  ungraded 🔮 cell (`nb5-visual-predice-code`, bare `"___"` var, zero XP
  impact, same exempt pattern as nb3's `mi_prediccion_ronda1`); inserted a
  one-line ungraded 🧩 pause cell between Concept 1 and Concept 2
  (`nb5-concepto-linea-pausa-code`) so the three back-to-back concept
  markdown cells aren't a single uninterrupted wall of text; added a
  3-panel synthetic-data 👀 visual (`nb5-concepto-r2-visual-code`, R²≈1.0/
  0.5/0.0, each subplot titled with its real `.score()` value) ahead of
  Concept 2's text so R² gets a picture before the bullet-list definition,
  matching this course's own "visualize before formalizing" convention;
  added a one-paragraph debrief after `nb5-ex2-check`
  (`nb5-ex2-debrief-md`) naming the pattern most students will hit
  empirically but never get told explicitly — `Peso` alone already carries
  almost all of Altura's predictable signal, `Sexo_num`/`Edad` add almost
  nothing on top. Also strengthened `check_ex1`'s `interpretacion_ex1`
  heuristic (still local/instant, no new DeepSeek call): previously only
  length ≥15 chars + no causal words, which content-free filler like "the
  variable I picked affects the outcome" passed cleanly. Now also requires
  the text to name one of the student's own chosen predictors (accent/case
  -insensitive) or include a digit.
  `nb5_regresion.ipynb` grew from 53 to 57 cells (all four insertions made
  in `build_nb5.py` first, with proper descriptive cell ids, then the
  notebook regenerated from it — not hand-edited independently, so the two
  stay in sync).
  **Scope change, user-approved after being flagged rather than applied
  silently**: added `check_t5`, a local MCQ (no network) testing the
  coefficient-scale caveat already stated once in `nb5-guiado-paso6-md`
  ("Apoyo social" has a bigger coefficient than "PBI per cápita" — does
  that make it more important? no, they're on different scales) but never
  assessed. Added to `_TEORIA`, `check_t5()`, `check_mini_b`'s checkpoint
  table, and the `nb5-teoria-md` quiz header ("4 preguntas... 20 pts" →
  "5 preguntas... 25 pts"); `_CORE_MAX`: 95 → 100 (`WORKFORCE_CONTRACT.md`
  §2 table and this file's earlier 2026-09-13 entries updated to match).
  New cell `nb5-t5-check` inserted after `nb5-t4-check` in both
  `build_nb5.py` and the regenerated notebook (57 → 58 cells).
  **Declined for this pass**: moving `interpretacion_ex1` to DeepSeek
  grading — a fourth network-dependent call inside the 40-pt core exercise,
  held back until the three `nb5_`-prefixed reflections above have
  survived a real concurrent-class load (see the 2026-08-24 502 incident on
  nb3/nb4 in the entries below).
  `_test_nb5.py` grew from 32 to 40 assertions, all passing (38 from the
  wiring/content fixes above, +2 for t5's correct/incorrect pair).
- 2026-08-29 — **nb4's Rondas 5–6 and Mini-Proyecto cut; new
  `proyecto_investigacion.ipynb` built to replace the Mini-Proyecto with a
  larger, real self-directed research project (user decision).**
  `course-python-stats/Weeks 3-4/build_nb4.py` and `autograder_nb4.py`:
  removed Rondas 5–6 (`check_ex5`/`check_ex6`/`check_t8`/`check_t9`/
  `check_reflexion_ronda6` — pure repetition of Semana 3's scatter+`.corr()`
  pattern, judged low-value for supervised class time) and the Mini-Proyecto
  (`check_intex1` + `check_reflexion_interpretacion` +
  `check_reflexion_metodologica`). Kept Debug 1, Ejercicio 7 (matrix-wide
  exploration, excludes circular `Puesto`), and all of Sección C (subgroup
  `.corr()`, Oceanía n=2 trap) — confirmed via `Teoria_Semanas3-4_Mision2_
  Correlacion.md` and `ATLAS_spec_nb3_nb4.md` that Sección C is a
  deliberately-engineered bridge to Semana 5, not filler. `_CORE_MAX`:
  150 → 60; both checkpoints (`check_mini_b`/`check_mini_c`) still gate
  correctly on the remaining exercises. Achievement `descubridor` (gated on
  `intex1`) removed; `cartografo_patrones` repointed from
  `[ex5,ex6,ex7,ex8]` to `[ex7,ex8]`.
  In its place: `course-python-stats/Weeks 3-4/build_proyecto_investigacion.py`
  → `proyecto_investigacion.ipynb`. Each student/pair picks their own real
  dataset and claim (menu of candidates still pending — see ticket #7's
  2026-08-29 note); started in class Semana 4 with supervision, due before
  Semana 5, presented at Semana 5's opening. No autograder, no `check_*`, no
  Supabase submission — graded by a human-scored 85-pt rubric printed at the
  end of the notebook, reusing the Week 8 capstone's own criteria wording
  from `WORKFORCE_CONTRACT.md` §4 minus the regression/clustering row (out of
  technical scope until Weeks 6–7). This is the first built instance of the
  "rubric-graded, not `check_*`-graded" pattern §4 describes for the
  capstone — no such notebook existed anywhere in the repo before this.
  **Continuity redirect (supersedes the note that used to live on
  `check_intex1` / in `ATLAS_spec_nb3_nb4.md`):** whoever designs Semana 5
  should treat `proyecto_investigacion.ipynb`'s hypothesis + confound
  write-up (cells `proy-hipotesis-respuesta` and
  `proy-reflexion-metodo-respuesta`) as the input material — not nb4's
  now-removed `intex1`. See the matching 2026-08-29 entries in
  `WORKFORCE_CONTRACT.md`'s Change Log and `ATLAS_spec_nb3_nb4.md`.

- 2026-08-24 — **Fixed the `grade-reflexion` 502s diagnosed live during class** (real Supabase
  Invocations log showed 6/9 requests failing with 502 in a ~5min window, successes landing
  seconds apart from failures — ruled out a total outage, pointed at DeepSeek-side
  rate-limiting/latency under concurrent classroom load on the one shared `DEEPSEEK_API_KEY`).
  **`supabase/functions/grade-reflexion/index.ts`**: the single DeepSeek call was refactored into
  `callDeepSeekOnce()` (never throws, returns `{ok, ...}` or `{ok:false, failReason}`) +
  `gradeWithRetry()` (up to `DEEPSEEK_MAX_ATTEMPTS=2`, `DEEPSEEK_RETRY_DELAY_MS=1500` between —
  absorbs a transient rate-limit/slow-response without giving up on the first blip). Per-attempt
  DeepSeek timeout raised 15s → `DEEPSEEK_TIMEOUT_MS=20000`. **Real diagnosability gap fixed
  too**: previously all three failure paths (DeepSeek non-2xx, fetch throw/timeout, invalid
  tool-call shape) collapsed into the identical `{error:"grading_failed"}` 502 with nothing
  logged — literally impossible to tell apart even from Supabase's own logs, which is exactly
  what made this incident hard to pin down. Now every failed attempt `console.error`s its real
  `failReason` (`deepseek_http_429:...`, `deepseek_timeout`, `deepseek_invalid_tool_call_shape`,
  etc.), and the final 502 body carries the last real reason in a `detail` field — the notebook
  client still ignores it entirely (never treat a grading failure as "the student scored 0", by
  design), but the *next* incident will have a real log trail instead of another identical
  screenshot to guess from.
  **Client-side, both `Weeks 3-4/autograder_nb3.py` and `autograder_nb4.py`** (`nb3_lite`/
  `nb4_lite` inherit `_call_grade_reflexion` unchanged, confirmed no override exists in either —
  they get this fix for free): `urlopen` timeout raised 15s → 55s. This wasn't optional — leaving
  it at 15s while the server's own worst case grew to ~41.5s (20s × 2 attempts + 1.5s backoff)
  would have made the client give up *before* the server's new retry logic could ever finish,
  turning a fix into a regression for exactly the failure case it targets. 55s leaves comfortable
  margin above that ~41.5s worst case.
  **Validated**: brace-balance check on the `.ts` file (no Deno CLI available in this session to
  fully typecheck — flagging this so whoever deploys it runs `deno check` first); `py_compile`
  clean on all four Python files; full existing suites re-run clean (`_test_nb3_nb4.py` 83/83,
  `_test_nb3_nb4_lite.py` all checks) — confirms the timeout-only change didn't touch scoring
  logic. **Not yet deployed** — editing `index.ts` locally doesn't push it to Supabase; someone
  with deploy access needs to run `supabase functions deploy grade-reflexion` (or the project's
  CI/CD equivalent, if one exists — not confirmed in this session) before this takes effect for
  real students. **Still open, deferred**: this makes 502s a *rarer* symptom of the underlying
  DeepSeek rate-limit, not a fix for the rate-limit itself — if the school's DeepSeek tier caps
  concurrent-classroom-sized bursts, the real ceiling only moves, not disappears. Checking
  DeepSeek's own dashboard/tier for the incident window needs Supabase/DeepSeek account access
  neither available in this session, flagged to the user directly.
  **Same-day follow-up, user-approved**: added a 0-3s random client-side jitter
  (`time.sleep(random.uniform(0, 3))`) right before the POST in both `_call_grade_reflexion`s —
  targets the actual root cause of the burst, not just its symptom: the whole class clicks
  "Enviar" within the same few seconds (same lesson pacing, one shared `DEEPSEEK_API_KEY`), so
  requests arrive at DeepSeek synchronized rather than spread out. Each Colab kernel is an
  independent process with no shared state, so jitter is the only coordination-free way to
  desynchronize a class-wide burst from here — a real queue/semaphore would need a shared backing
  store (Postgres row lock, Redis, etc.) that doesn't exist for this function today, out of scope
  for this pass. `nb3_lite`/`nb4_lite` inherit it for free (same non-override confirmation as
  above). Validated: `py_compile` clean on both edited files; `_test_nb3_nb4.py` re-run 83/83 in
  ~4.5s wall time (confirms the suite mocks `_call_grade_reflexion` directly rather than calling
  the real implementation, so the sleep never fires during tests — no suite slowdown, and this
  also means the jitter itself has zero automated test coverage, purely reasoned from the code).
  **Considered and deferred, not rejected**: a queue-and-regrade-later fallback (store failed
  reflections as "pending," regrade via a scheduled job instead of asking the student to retry
  live) — bigger lift (new table/column, a regrade job, a "pending" UI state that doesn't exist),
  worth revisiting only if jitter + retry turn out insufficient.
- 2026-08-24 — **`index.html` (course hub) wired up to show `nb3`'s best-score stats, scoped to
  that notebook only.** The hub's Python track only ever had a quest card for Misión 1
  (`nb1_semana1` → `nb1.html`); Misión 2/Semana 3 (`nb3`) had no card and its stats-fetching
  `TRACKS` array never queried `notebook: 'nb3'` at all, so the "En Busca de la Felicidad" ranking
  was unreachable from the hub even after `nb3.html` shipped. Added a live quest card
  (`MISIÓN 2 · SEMANA 3`, linking to `course-python-stats/nb3.html`) and a `{ notebook: 'nb3' }`
  entry to `TRACKS` — `loadTrackStats()` already filters `curso=STAT_2026` +
  `notebook=track.notebook` per track, so this card's TOP/AVG/participant-count pills reflect
  only `nb3` submissions, never mixed with `nb1_semana1` or the Sheets track. Also ported the
  same-day `dni`-collision dedup fix (`normName()` + compound `dni|nombre` key, see the `nb3.py`/
  `nb3.html` entry below) into this file's own `dedupBest()`, since it directly feeds the number
  this change was asked to get right — same class of bug, in scope this time because it's the
  exact stat being surfaced, not an unrelated file. `nb4`/Semana 4 intentionally left off the hub
  — not requested, and no reason yet to assume its card should look identical to nb3's.
- 2026-08-24 — **Fixed a real bug the user hit live: `nb3` showed students who hadn't done any
  work as if they'd already finished.** Root cause in `Weeks 3-4/autograder_nb3.py`'s
  `_on_register()`: the "resume my progress" lookup restores `self._scores`/`_achievements`/
  `_streak`/`_prev_level` from the student's best prior Supabase row keyed **only** by
  `dni=eq.<typed code>` + `notebook=eq.nb3` — and the DNI field (`"🪪 CÓDIGO DE ESTUDIANTE (DNI,
  Pasaporte, Carnet)"`) has zero format/length/uniqueness validation, so two different students
  typing the same code (a shared placeholder, a typo, a sibling's DNI, leftover test data) cause
  the second one's session to silently inherit the first one's full score breakdown the moment
  they register — before running a single exercise cell. **Fix**: query now also selects
  `nombre`, and the restore only fires if the stored row's name matches (via the file's own
  existing `_norm()` helper, already used elsewhere for fuzzy text grading) the name the student
  just typed; a DNI collision with a different name now correctly falls through to "aún no tienes
  marca registrada" instead of inheriting a stranger's score. `py_compile` clean.
  **Same root cause, same-day fix in `course-python-stats/nb3.html`**: its `dedup()` collapses a
  student's multiple submission attempts to their best score, keyed by `dni` alone — same
  collision exposure, one layer up. If two different students share a `dni`, the leaderboard
  silently merged them into one row (the higher scorer's), hiding the other rather than showing
  either "already finished." Fixed by adding a normalized `nombre` (new `normName()`, a plain
  Spanish accent map — a JS regex Unicode escape (`̀-ͯ`, for NFKD-style diacritic
  stripping mirroring `_norm()`) kept getting silently decoded into literal combining-mark
  characters by a tool layer mid-edit rather than staying as source text, so switched to an
  explicit áéíóú/ñ map instead, which is arguably more apt for this Spanish-only name set anyway)
  to the dedup key, so a
  same-dni collision with a different name now shows as two separate rows with their own real
  scores instead of one clobbering the other. Verified in isolation with `node -e`: same
  dni+name across two attempts still collapses to one row (best score kept); same dni with two
  different names now yields two rows, each its own score — not just asserted, both cases run
  and printed. **Not yet applied to the three sibling files/pages with the identical pattern**
  (`autograder_nb1_semana1.py`, `autograder_nb1_semana2.py`, `autograder_nb4.py`, and `nb1.html`'s
  own `dedup()`) — flagged to the user, not fixed without confirmation since this touches
  multiple already-live grading scripts.
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

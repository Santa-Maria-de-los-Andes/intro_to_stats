# SMA — Intro to Stats

I.E. Santa María de los Andes (Cusco, Peru), Bimestre 3, Unidad 3: two parallel statistics
modules, one per age band. Gamified, Colab/Sheets-native, autograded via Supabase. See
`shared/COURSE_TEMPLATE.md` for the full architecture this is built on.

## Repo map

```
course-python-stats/    CS2 — Estadística en Python ("Pensando con Datos"), 3°-5° secundaria
course-sheets-stats/    CS2 — Estadística en Google Sheets ("El Caso de los Datos"), 1°-2° secundaria
shared/                 Cross-course architecture, DB schema, branding asset
WORKFORCE/              The agent team building both courses: roles, contract, ticket tracker
reference/              Prior/prerequisite-course material kept for context, not part of either course
```

### `course-python-stats/` — Statistics in Python (3°–5° secundaria)

- `Bimestre3_Statistics_Python_Module_Guide.md` — module guide: objectives, week-by-week shape
- `EPT U3.docx` — official DRE/UGEL unit-plan document (Área: Educación para el Trabajo)
- `nb1.html` — public live leaderboard for `nb1_semana1` (polls Supabase every 60s)
- `nb3.html` — public live leaderboard for `nb3` ("En Busca de la Felicidad," Semana 3
  Correlación), same polling engine, reskinned to the sunrise palette baked into
  `Weeks 3-4/autograder_nb3.py`. **Note:** `nb2.html` in this folder does not pair with a
  `nb2`-named notebook — it actually serves `nb1_semana2` (see the file's own header comment)
  and `nb2` itself belongs to a different, prerequisite course (`reference/legacy-CS1/nb2.html`).
- `Weeks 1-2/` — Misión 1: Recuperación de Datos (pandas bootcamp), split into two class
  sessions:
  - `Teoria_Semanas1-2_Mision1_RecuperacionDeDatos.md`, `Preguntas_Teoricas_Semanas1-2.md` —
    content source of truth
  - `build_nb1.py` — generates both `.ipynb` notebooks from the content above
  - `nb1_semana1_recuperacion_datos.ipynb`, `nb1_semana2_recuperacion_datos.ipynb` — built
    notebooks (regenerate via `python build_nb1.py` after editing content, don't hand-edit)
  - `autograder_nb1_semana1.py` — Semana 1 grader (Semana 2's autograder isn't written yet —
    see `WORKFORCE/WORKFORCE_HANDOFF.md` ticket #10)
  - `vgsales.csv`/`vgsales_es.csv`, `athlete_events.csv`/`athlete_events_es.csv` — datasets
    (`_es` = Spanish column names, what the notebooks actually load), `translate_to_spanish.py`
    produced the `_es` versions

### `course-sheets-stats/` — Statistics in Google Sheets (1°–2° secundaria)

- `Bimestre3_Statistics_Sheets_Module_Guide.md` — module guide (younger band, description-only
  scope: no correlation/regression — see guide's Coordination Notes)
- `Unidad 3 - Estadistica en Google Sheets (1ro-2do).docx` — official DRE/UGEL unit-plan document
- `Weeks 1-2 (Sheets)/` — Caso 1: Abriendo el Caso — theory, practice exercises, and the Sheets
  build instructions. Newer than the Python module; Apps Script → Supabase submission path is
  its own from-scratch build, not a port of the Python autograder pipeline.

### `shared/`

- `COURSE_TEMPLATE.md` — the house architecture both courses build against: autograder pattern,
  gamification mechanics, Supabase pipeline, dashboard conventions, file-naming rules
- `supabase_schema.sql` — shared `submissions`/`courses` tables (one Supabase project, both
  courses, discriminated by a `curso` column — see schema comments)
- `icono SMA.png` — institution logo, referenced by both courses' dashboards/graders

### `WORKFORCE/`

The multi-agent team (in the "spawn a Claude agent per role" sense) driving both courses:

- `ORCHESTRATOR/ORCHESTRATOR.md` — meta-agent that designs the team itself
- `01_SOFIA.md`, `02_PIXEL.md`, `03_ATLAS.md`, `04_GAUSS.md` — role definitions (curriculum
  sequencing, theme/UX, autograder-logic validation, statistical-accuracy validation)
- `WORKFORCE_CONTRACT.md` — the section/week structure, exercise-key taxonomy, and scoring
  shape every role builds against (owned by SOFIA, edited in place)
- `WORKFORCE_HANDOFF.md` — open tickets by owner, Done log, accepted scope cuts, escalations
  (owned by SOFIA, edited in place)

### `reference/legacy-CS1/`

- `autograder_nb2.py` — grader for a *different*, prerequisite programming course (loops/
  conditionals, "God of War" theme, notebook id `nb2`). Not one of the two statistics courses
  above; kept because `COURSE_TEMPLATE.md`'s architecture was reverse-engineered from it.
- `nb2.html` — public live leaderboard for that course's `nb2` (polls Supabase every 60s),
  mirroring `course-python-stats/nb2.html`'s engine reskinned to the God of War palette/levels
  already documented in `WORKFORCE/02_PIXEL.md`.

## Working on this repo

- This repo is `Santa-Maria-de-los-Andes/intro_to_stats` on GitHub. The Python notebooks'
  setup cells `!wget` the autograder and datasets from
  `raw.githubusercontent.com/.../main/course-python-stats/Weeks%201-2/...` — if you move those
  files again, update the URLs in `build_nb1.py` (then regenerate the notebooks) or student
  submissions will fail with a 404 on the first cell.
- Don't hand-edit the `.ipynb` files directly — edit the theory/question source `.md` files or
  `build_nb1.py`, then run `python build_nb1.py` to regenerate.
- `WORKFORCE_CONTRACT.md` and `WORKFORCE_HANDOFF.md` are living documents: edited in place,
  never forked into version-suffixed copies.

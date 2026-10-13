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
powerbi/                Master Power BI report over every Supabase submission (both courses)
```

### `powerbi/`

- `SMA_Tareas_Master.pbip` — open in Power BI Desktop. Pulls `public.submissions` live from Supabase
  (paged; `TEST`/`INTEGRATION_TEST`/`SCRATCH` test rows excluded); first refresh asks for
  credentials on the Supabase URL — choose **Anonymous**.
- `SMA_Tareas_Master.SemanticModel/` — TMDL model. Notebook deadlines / `_CORE_MAX` live in the
  `Meta` table inside `tables/Tareas.tmdl` — add a row there when a new notebook ships.
- `build_report.py` — generates the report pages; edit it and rerun instead of hand-editing `visual.json`.
  Pages: Vista general · Seguimiento · Libro · Lista de cotejo · Alumnos · Estudiante (hidden, drill-through on a student name)
  · Actividad · Ejercicios. Design rationale and reference numbers: `REPORT_SPEC.md`.
- `item_intentos.py` — rebuilds the per-item attempt sequence and writes `data/item_intentos.csv` and
  `data/item_resumen.csv` (git-ignored, they contain DNIs). **Run it before each refresh**; the
  `ItemIntentos` / `ItemResumen` tables read those CSVs from the `CarpetaDatos` parameter.
- `notas_manuales.py` — loads manual-review grades for students whose submission never reached Supabase.
  Fill `data/notas_manuales.csv` (`dni,notebook,puntos`, `puntos` may be `85%`) or pass one student on
  the command line (`python notas_manuales.py 71234567 nb6 72`); it previews by default, `--enviar` inserts.
  Rows are tagged `email = 'revision_manual'`. Keep its `TAREAS` table in sync with `Meta` when a notebook ships.
- Tables added for the teacher redesign (all in `SemanticModel/definition/tables/`):
  - `Horario` — class schedule per grade (Peru time). Defines `Envios[EnClase]` and everything
    "in class / after class". To change it, edit the rows in the `#table(...)` of `Horario.tmdl`
    (or *Transform data → Horario* in Desktop): `Grado`, `DiaSemana` (no accents: Lunes…Domingo),
    `HoraInicio`, `HoraFin` (last minute, inclusive), `MargenAntesMin` (minutes before start that
    still count as class). Add one row per extra class block.
  - `AliasDNI` — mistyped DNI → canonical DNI (the one in the roster). Mirror any new row in `item_intentos.py`.
  - `Padron` — official STAT 3ro–5to roster, read from `data/padron.csv` (`Grado,DNI,Nombre`; git-ignored
    because it has DNIs). `Alumnos` takes STAT students, names and grades from it, so students who never
    submitted still count as expected. Add or fix a student there and refresh; if they typed a different
    DNI in the notebook, add an `AliasDNI` row.
  - `AlumnoTarea` — one row per student × notebook (best `NotaReal`, grade when leaving class,
    worked outside class, days worked). Expected-but-missing pairs have no row; the `Estado`
    measure reports them as "No entregó".
  - `ItemIntentos` / `ItemResumen` — from the CSVs above. `Etapas` — disconnected table for the funnel.
  - `Indicadores` / `IndicadorItems` / `AlumnoIndicador` — the **Lista de cotejo** page (CNB, área EPT).
    `Indicadores.tmdl` holds the catalog: 5–6 indicators per notebook, their capacidad (C1–C4, AUT, TIC),
    and the autograder items that evidence each one (`Items` = `"ex1:8,t9:5,reto1:10*"`, `*` = bonus,
    which only counts if attempted). `AlumnoIndicador` is a calculated table, padrón × indicator: **Sí** when
    the best score over those items is ≥ 60% (`Umbral` in its DAX), otherwise No / No entregó / Pendiente /
    Sin desglose. Add the rows for every new notebook.
  - **Nivel de logro** page: pools every cotejo check (student × indicator, all due notebooks, no entregó = No)
    per CNB capacidad / competencia and grades the % Sí: C < 50%, B 50–69%, A 70–89%, AD ≥ 90% (`Niveles` table,
    measure `Nivel de logro`). Indicators in `SinMapeoClaro` (in `Indicadores.tmdl`) show in the cotejo but don't count.
  - `Meta` (in `Tareas.tmdl`) gained `MuestraEsperado`: TRUE when the autograder's error message
    shows the expected value. Set it for every new notebook.

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

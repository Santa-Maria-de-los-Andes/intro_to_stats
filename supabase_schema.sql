-- =============================================================
-- PYTHON QUEST — Supabase Schema
-- Ejecuta este script en el SQL Editor de tu proyecto Supabase
-- =============================================================

-- ── submissions: historial completo de intentos ──────────────
CREATE TABLE IF NOT EXISTS public.submissions (
  id               uuid        DEFAULT gen_random_uuid() PRIMARY KEY,
  email            text        NOT NULL DEFAULT '',
  dni              text,
  nombre           text,
  grado            text,
  notebook         text        NOT NULL DEFAULT 'nb1',
  earned           integer     NOT NULL,
  possible         integer     NOT NULL,
  pct              integer     NOT NULL,
  level_num        integer     NOT NULL,
  level_name       text        NOT NULL,
  achievements     text[]      DEFAULT '{}',
  streak           integer     DEFAULT 0,
  score_breakdown  jsonb       DEFAULT '{}',
  submitted_at     timestamptz DEFAULT now()
);

-- Si la tabla ya existe, agrega las nuevas columnas:
ALTER TABLE public.submissions ADD COLUMN IF NOT EXISTS dni    text;
ALTER TABLE public.submissions ADD COLUMN IF NOT EXISTS nombre text;
ALTER TABLE public.submissions ADD COLUMN IF NOT EXISTS grado  text;
ALTER TABLE public.submissions ALTER COLUMN email SET DEFAULT '';

-- `curso` distingue el modulo/materia dentro de la misma tabla compartida.
-- Valores: 'CS_2026' (Computer Science, Bimestre 2, notebooks nb1/nb2/nb3)
-- y 'STAT_2026' (Estadistica, Bimestre 3, notebooks nb1_semana1/nb1_semana2/
-- nb2/nb3). DEFAULT 'CS_2026' porque los autograders viejos (autograder_nb2.py,
-- etc.) no mandan `curso` en su payload -- cualquier fila que no lo especifique
-- es de CS. autograder_nb1_semana1.py (Estadistica) ya manda
-- "curso": "STAT_2026" explicitamente, pisando el default.
-- Tiene 3 tareas/notebooks igual que CS, identificadas via `notebook`:
--   nb1_semana1 / nb1_semana2  -> Tarea 1 (Pandas Bootcamp, dividida en 2 semanas)
--   nb2                        -> Tarea 2 (Correlacion)
--   nb3                        -> Tarea 3 (Regresion / Clustering)
ALTER TABLE public.submissions ADD COLUMN IF NOT EXISTS curso text;
ALTER TABLE public.submissions ALTER COLUMN curso SET DEFAULT 'CS_2026';

-- Backfill de una sola vez: filas existentes (todas de CS, insertadas antes
-- de que esta columna existiera) quedan etiquetadas explicitamente. Si ya
-- corriste esta migracion antes, este UPDATE no hace nada (no quedan NULL).
UPDATE public.submissions SET curso = 'CS_2026' WHERE curso IS NULL;

-- Indice para consultas del leaderboard por DNI
CREATE INDEX IF NOT EXISTS idx_submissions_dni_pct
  ON public.submissions (dni, pct DESC, submitted_at DESC);

-- Indice para el leaderboard por curso + notebook (necesario ahora que
-- varios modulos comparten la tabla; ver get_best_submissions en Supabase,
-- que aun falta extender para filtrar por `curso` -- WORKFORCE_HANDOFF.md #6)
CREATE INDEX IF NOT EXISTS idx_submissions_curso_notebook_pct
  ON public.submissions (curso, notebook, pct DESC, submitted_at DESC);

-- ── Row Level Security ───────────────────────────────────────
ALTER TABLE public.submissions ENABLE ROW LEVEL SECURITY;

-- Anon puede INSERT (autograder de los alumnos)
CREATE POLICY "anon_insert" ON public.submissions
  FOR INSERT TO anon
  WITH CHECK (true);

-- Anon puede SELECT (leaderboard publico en GitHub Pages)
CREATE POLICY "anon_select" ON public.submissions
  FOR SELECT TO anon
  USING (true);

-- Nota: si quieres restringir lecturas individuales, elimina la
-- politica anon_select y crea en su lugar una funcion
-- SECURITY DEFINER que devuelva solo los mejores por email.

-- ── students: vincula email con nombre real y grado ──────────
-- Llena esta tabla manualmente o con un CSV import
CREATE TABLE IF NOT EXISTS public.students (
  email       text PRIMARY KEY,
  full_name   text,
  grade       text,   -- ej: "3ro A", "4to B"
  created_at  timestamptz DEFAULT now()
);

ALTER TABLE public.students ENABLE ROW LEVEL SECURITY;

-- Solo el service_role (admin) puede leer/escribir students
-- anon NO tiene acceso

-- ── courses: metadata de cada curso/modulo (id = submissions.curso) ──
CREATE TABLE IF NOT EXISTS public.courses (
  id          text        PRIMARY KEY,   -- coincide con submissions.curso, ej: 'CS_2026'
  name        text        NOT NULL,      -- nombre para mostrar, ej: "Computer Science"
  bimestre    text,                      -- ej: "Bimestre 2"
  year        integer,                   -- ej: 2026
  created_at  timestamptz DEFAULT now()
);

ALTER TABLE public.courses ENABLE ROW LEVEL SECURITY;

-- Anon puede SELECT (el hub/leaderboard publico necesita el nombre del curso)
CREATE POLICY "anon_select" ON public.courses
  FOR SELECT TO anon
  USING (true);

-- Solo el service_role (admin) puede insertar/editar cursos -- anon no escribe

-- Seed: los dos cursos que ya usa `submissions.curso` hoy
INSERT INTO public.courses (id, name, bimestre, year) VALUES
  ('CS_2026',   'Computer Science', 'Bimestre 2', 2026),
  ('STAT_2026', 'Estadistica',      'Bimestre 3', 2026)
ON CONFLICT (id) DO NOTHING;

-- ── Consulta rapida: mejor puntaje por alumno ────────────────
-- Ejecuta esto en el SQL Editor para ver el leaderboard actual:
--
-- SELECT DISTINCT ON (s.email)
--   s.email,
--   st.full_name,
--   st.grade,
--   s.curso,
--   c.name AS curso_nombre,
--   s.notebook,
--   s.pct,
--   s.earned,
--   s.possible,
--   s.level_name,
--   array_length(s.achievements, 1) AS num_logros,
--   s.streak,
--   s.submitted_at
-- FROM public.submissions s
-- LEFT JOIN public.students st ON st.email = s.email
-- LEFT JOIN public.courses  c  ON c.id = s.curso
-- -- WHERE s.curso = 'STAT_2026'  -- filtra al modulo de Estadistica
-- ORDER BY s.email, s.pct DESC, s.submitted_at DESC
-- ORDER BY pct DESC;

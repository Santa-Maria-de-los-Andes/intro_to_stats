# BIMESTRE 3: ESTADÍSTICA EN GOOGLE SHEETS
## 1°-2° Secundaria | Ages 12-13/13-14 | 7-8 Weeks

**Format:** Google Sheets templates (one per week) with gamified narrative theme, Apps Script → Supabase submission mirroring the Python Quest leaderboard/dashboard architecture (see `COURSE_TEMPLATE.md`) — **new engineering build, not a reuse**, see Coordination Notes at the end of this doc.
**Prerequisite Skills:** None formal — this is most students' first structured data-analysis exposure. Basic Sheets navigation (opening a file, typing into a cell, saving a copy) is the floor, not a taught skill.
**Core Philosophy:** Statistical thinking first, the spreadsheet as the tool to get there — not the other way around. Same philosophy as the Python module, deliberately kept identical across the school's stats track so the *habit of mind* is consistent even though the tools differ by age.

---

## 🎯 MODULE LEARNING OBJECTIVES

By the end of this module, students will:
- Organize raw data into a clean, usable spreadsheet
- Calculate and interpret SUMA, PROMEDIO, MEDIANA, and MODA in context — and explain *why* you'd pick one over another for a given question
- Recognize when a single number (especially an average) hides or distorts the real story
- Build and choose an appropriate chart (bar, pie, line) to represent a dataset
- Complete an independent "case" analysis of a real dataset and present findings as a detective would present evidence

**Explicitly NOT a goal:** Correlation, causation analysis, regression, or clustering. Those stay in the 3°-5° Python module (`Bimestre3_Statistics_Python_Module_Guide.md`). This module is exposure to *description*, not *relationship-finding* — the CNB-appropriate ceiling for this age band is describing and interpreting a single dataset well, not comparing two variables statistically.

---

## 📊 GOOGLE SHEETS SCOPE (Keep It Lean)

**Technical spine for this module — nothing more:**
- Manual data entry + `Ctrl+Shift+V` (paste values), basic cell formatting (bold, borders, number formats)
- `=SUMA()`, `=PROMEDIO()`, `=MEDIANA()`, `=MODA()`
- `=MAX()`, `=MIN()` — spread/range, paired with the central-tendency functions rather than taught standalone
- `=CONTAR()` / `=CONTARA()` — supports building frequency tables ahead of MODA and ahead of charts
- Basic filtering (Data → Create a filter) — no formulas, just UI-level filtering to answer "show me only X"
- Charts: column/bar, pie, line — via Insert → Chart, including choosing chart type deliberately, not just accepting Sheets' default
- Conditional formatting (color scales / single-color rules) — used specifically in the "misleading stats" week to make outliers visually jump out before naming them

**Do not** introduce `=PROMEDIO.SI()`, pivot tables, or `QUERY()` — those belong to a later, more advanced spreadsheet unit. **Do not** spend a standalone week on "Sheets fundamentals" — teach each skill embedded in the case that needs it, same rule as the Python module.

---

## 📅 WEEK-BY-WEEK OUTLINE

### Weeks 1-2: Abriendo el Caso (Opening the Case)
**Learning Target:** Take messy raw data and organize it into a usable spreadsheet; calculate a total with SUMA.

**Narrative Hook:** Students join the agency as junior detectives. Their first case file arrives as a disorganized pile of "evidence" (a messy raw dataset) — step one of any investigation is getting your evidence in order before you can question it.

**Core Activity:** Choose a dataset students care about and can picture concretely (class survey results, favorite games/snacks, allowance/weekly spending, sports stats). Progression: clean/organize → format → SUMA totals → simple filtering to isolate a subset of the evidence.

**Deliverable:** A cleaned case file with totals calculated, answering "how much/how many in total?"

---

### Week 3: El Sospechoso Promedio (The Average Suspect)
**Learning Target:** Calculate and interpret PROMEDIO; build intuition for "typical value" before naming it.

**Sequence (important, mirrors the Python module's visualization-before-formalization rule):**
1. Show a simple dot plot or list of values first — no formula, just "if you had to pick *one* number to describe this group, what would it be?"
2. Introduce "average" conceptually as the group's typical value
3. Calculate it with `=PROMEDIO()`
4. Apply it to answer an in-story question ("what's the typical amount of evidence per suspect?")

**Deliverable:** PROMEDIO calculated + one sentence answering the case's guiding question.

---

### Week 4: La Mediana No Miente (The Median Doesn't Lie)
**Learning Target:** Calculate MEDIANA; recognize when it tells a different, more honest story than PROMEDIO.

**Narrative Framing:** "The suspect's alibi uses an average — but averages can be tricked by one extreme value. Bring in a second witness: the median."

**Activities:** Use a dataset with a clear outlier (e.g., one very high value skewing an average, like one student's allowance far above the rest). Calculate both PROMEDIO and MEDIANA side by side, discuss why they differ.

**Deliverable:** Side-by-side PROMEDIO/MEDIANA comparison + one sentence on which one better represents "the typical case" here and why.

> This week plants the seed for Week 6's skepticism unit — don't resolve "which number is right" too neatly; let the tension sit.

---

### Week 5: El Patrón Más Común (The Most Common Pattern)
**Learning Target:** Calculate MODA; distinguish it from PROMEDIO/MEDIANA as the right tool for categorical or "most frequent" questions.

**Narrative Framing:** "Not every question is about typical size — sometimes you need to know what happens *most often*."

**Activities:** Apply to categorical/discrete data (most common answer in a survey, most frequent shoe size, most-picked snack). Build a frequency table with `=CONTARA()` before introducing `=MODA()`, so the formula's output is visibly grounded in counts they already understand.

**Deliverable:** Frequency table + MODA + one sentence on what question MODA answers that PROMEDIO/MEDIANA can't.

---

### Week 6: Cuidado con las Trampas (Watch for the Traps)
**Learning Target:** Spot misleading statistics and misleading charts; build healthy skepticism toward "the average says…" claims.

**Sheets Skills:** Minimal new formulas — mostly reusing Weeks 3-5, plus conditional formatting to visually flag outliers.

**Activities:**
- Analyze real (or realistic, teacher-curated) examples of misleading stats from ads/news/social media aimed at this age group (e.g., "average" prices that hide extremes, a cherry-picked time window, a chart with a truncated axis or no axis labels)
- Given a dataset, deliberately construct one honest and one misleading chart/summary from the *same* data, then explain what makes the second one misleading
- Revisit their own Week 1-2 case data: could someone lie with it?

**Deliverable:** A short presentation (in-agency "briefing") debunking one misleading stat or chart, using their own case data as supporting evidence.

> **This is the critical-thinking lynchpin of the module**, in the same spirit as Week 5 of the Python module. It doesn't need correlation or causation vocabulary to do real work at this age — "does this number/chart tell the whole story?" is the transferable skill. Protect this week's time; don't compress it to catch up elsewhere.

---

### Week 7: El Informe Visual (The Visual Report)
**Learning Target:** Choose and build the right chart type for a given question; combine SUMA/PROMEDIO/MEDIANA/MODA into one coherent case report.

**Narrative Framing:** "Evidence and numbers alone don't close a case — you need to present it so anyone can see the pattern at a glance."

**Activities:** Given the same dataset, practice choosing between bar, pie, and line charts and explaining *why* one fits better than another for a specific question (e.g., pie for parts-of-a-whole, line for change over time, bar for comparing categories). Assemble a one-page case report combining a chart with the four core statistics.

**Deliverable:** One-page visual case report: chart + SUMA/PROMEDIO/MEDIANA/MODA + short interpretation.

---

### Week 8: Cierre del Caso (Case Closed) — Capstone

**Learning Target:** Independently investigate a real dataset end-to-end and present findings.

**Format:** Teams pick (or are assigned) a dataset relevant to their own lives or school (survey they run themselves, sports stats, spending habits, etc.), apply the full toolkit — organize, SUMA, PROMEDIO, MEDIANA, MODA, an honest chart, and a one-line "watch out for this trap" caveat — and present as a closing case briefing.

**Assessment:** Rubric-graded (see Coordination Notes — rubric criteria to be defined jointly with ATLAS, same pattern as the Python module's capstone).

---

## 🕵️ GAMIFICATION / XP ARC

| Weeks | Focus | XP |
|---|---|---|
| 1-2 | Opening the Case (Sheets basics + SUMA) | ~150 |
| 3 | The Average Suspect (PROMEDIO) | ~100 |
| 4 | The Median Doesn't Lie (MEDIANA) | ~100 |
| 5 | Most Common Pattern (MODA) | ~100 |
| 6 | Watch for the Traps (skepticism) | ~120 |
| 7 | The Visual Report (charts) | ~130 |

Same 6-tier level curve as the Python module (§5 of `COURSE_TEMPLATE.md`) — thresholds and scoring-split rules (`_CORE_MAX`/`_BONUS_MAX` separation) carry over unchanged; only tier names/emoji get themed to Detective Agency once PIXEL runs a Theme Brief pass (see Coordination Notes).

---

## 📓 WEEKLY SHEET STRUCTURE (Per Week)

Each week's Sheets template should follow this internal sequence, adapted from the Python module's notebook structure for a non-code medium:

1. **Opening narrative** — themed case briefing ("A new case file just landed on your desk...")
2. **Conceptual explanation** — text + visual (dot plot, simple chart), before any formula is introduced
3. **Guided worked example** — a filled-in reference tab showing the formula applied correctly
4. **Progressive practice cells** — easy → medium → hard → bonus "extra credit lead," each tagged with XP, in a student-editable tab
5. **Checkpoint** — mastery gate (consistent threshold with the rest of the curriculum — confirm against the school's existing 80% standard) before the next week unlocks

---

## 🧭 PEDAGOGICAL GUARDRAILS

- **Visualization before formalization.** Students see the dot plot, the skewed list, or the misleading chart before they learn the formula name — same rule as the Python module, doubly important at this age.
- **The spreadsheet stays subordinate to the question.** Every formula should be answering a case question posed in the narrative, not existing as a formula-syntax drill.
- **Week 6 deserves real time.** Statistical skepticism at an age-appropriate level ("does this number tell the whole story?") is the most transferable skill in this module — don't compress it to make room elsewhere. Direct analog to the Python module's protected Week 5.
- **Keep the four functions concrete, not abstract.** At this age, PROMEDIO/MEDIANA/MODA should always be anchored to a tangible in-story question ("what's typical," "what's most common") rather than introduced as a definitions list.
- **No correlation, causation, regression, or clustering vocabulary.** That's explicitly out of scope for this age band (see Module Learning Objectives) — resist the pull to preview "next year you'll learn..." content mid-lesson; it dilutes focus without adding retained value at this level.

---

## 📌 OPEN QUESTIONS FOR NEXT REVIEW

- [ ] Confirm datasets for each week (student-generated surveys vs. teacher-provided Peruvian-context datasets — likely a mix, front-loaded with teacher-provided in Weeks 1-2 and shifting to student-chosen by the capstone)
- [ ] Verify current CNB competency wording for 1°-2° secundaria's data-management standard against this scope (I'm confident the level is right conceptually — measures of central tendency without correlation/regression — but the exact CNB descriptor text needs pulling from the official framework, not assumed)
- [ ] Confirm mastery checkpoint threshold matches the rest of the curriculum's 80% standard, or whether a lower bar is more appropriate for first-time spreadsheet users
- [ ] Decide whether Week 8 capstone datasets are student-collected (e.g., a survey they run on classmates) or teacher-provided — affects how much of Week 8 goes to data collection vs. analysis

---

## 🔗 Coordination Notes (for WORKFORCE_CONTRACT.md / WORKFORCE_HANDOFF.md)

This document covers SOFIA's lane only (topic, learning objectives, section structure, exercise list per section — `COURSE_TEMPLATE.md` §12 step 1). Two real next-steps before this can ship, both outside SOFIA's remit:

1. **PIXEL pass needed:** a Theme Brief (`02_PIXEL.md` template) for the Detective Agency theme — palette, 6 level names, achievement copy, in-theme section headers. Must render legibly on white background per the house constraint.
2. **ATLAS pass needed — and flagged as new engineering, not reuse:** the chosen "full leaderboard integration" assessment format means building a Google Apps Script → Supabase submission path for Sheets, which the existing `COURSE_TEMPLATE.md` architecture (§1, §6-§8) doesn't provide out of the box — that pipeline is Colab/Python-native (`!wget` autograder, `IPython.display`, notebook cell IDs). Treat this as a genuine new build: exercise scoring logic, the `course` discriminator value for this module, and the Apps Script equivalent of the autograder's `_award`/`_submit_to_supabase` pattern all need to be designed from scratch before Week 1 can go live with real students. Recommend scoping this as its own ticket in `WORKFORCE_HANDOFF.md` rather than assuming it's a small add-on.

---

*Document prepared as a working outline — subject to revision after Week 1-2 pilot and student feedback, same convention as the Python module.*

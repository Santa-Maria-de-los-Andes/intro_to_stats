# DAX Performance

## How the engine works (just enough to reason about speed)

A DAX query is split between two engines: the **storage engine (VertiPaq)**, which scans compressed columnar data and does simple aggregations very fast, and the **formula engine**, which handles everything VertiPaq can't do natively (complex row-by-row logic, most iterators) — and is much slower, single-threaded, and works with uncompressed data. Most DAX performance work is really about pushing as much work as possible into the storage engine and minimizing formula-engine involvement.

## High-impact practices

- **Variables over repeated sub-expressions.** Every reference to the same measure/expression re-evaluates it unless it's captured in a `VAR`. Beyond readability, this is a real performance lever when an expensive sub-expression is used more than once.
- **Boolean filter arguments over `FILTER(table, ...)`.** `CALCULATE([Sales], Product[Color]="Red")` can be pushed to the storage engine as a simple predicate; `CALCULATE([Sales], FILTER(Product, Product[Color]="Red"))` forces formula-engine row-by-row evaluation of the whole table. When `FILTER` is unavoidable, filter the narrowest table possible: `FILTER(VALUES(Product[Color]), Product[Color]="Red")` scans only distinct color values, not every product row.
- **Avoid nested iterators.** Calling an iterator (or a measure containing one) from inside another iterator multiplies row-by-row cost. Watch especially for a measure that internally uses `SUMX`/`AVERAGEX` being called from inside another `SUMX` elsewhere — the nesting isn't always visible at the call site.
- **Don't call table-generating iterative functions (e.g. `ADDCOLUMNS`) inside a measure** unless genuinely necessary — measures are already evaluated once per cell in a visual; wrapping that in another full iteration multiplies cost per cell.
- **Column data types and cardinality:**
  - Convert a two-value column to an actual boolean type rather than leaving it as text/int — booleans process faster at scale.
  - Prefer integer surrogate keys over string keys for relationships and heavy filtering — VertiPaq's value encoding (versus hash encoding) only kicks in for integers, and value-encoded columns are both smaller and faster to scan.
  - High-cardinality columns (raw timestamps, GUIDs) are expensive to store and filter on — split a timestamp into separate date/time columns if only one component is actually used for analysis.
- **Calculated columns vs. measures, again:** calculated columns are computed once at refresh and stored (increasing model size and refresh time); anything that can be a measure instead avoids that cost entirely and stays responsive to filters.
- **`IF.EAGER`** can help when both branches of a conditional would otherwise be evaluated as separate query plans that could be fused — it's a hint to the engine that fusion is safe/beneficial here. Test with and without it on the specific measure; the benefit is scenario-dependent, not universal.

## Profiling workflow

1. Use **Performance Analyzer** (built into Power BI Desktop) to see which visual is slow and how much of that time is the DAX query vs. rendering.
2. Copy the offending query into **DAX Studio** to see the actual query plan and server-timings breakdown (storage engine time vs. formula engine time, and how many storage-engine queries ran).
3. **Clear the cache before comparing variations** — VertiPaq caches results, so a second run of the same query will look artificially fast. DAX Studio has a clear-cache button/command for this.
4. Compare 2-3 candidate rewrites of a suspect measure directly in DAX Studio rather than guessing — the "obviously faster" version is sometimes wrong for a given data distribution and cardinality.

## What's new (2025–2026) — check applicability before relying on these

DAX had its biggest update in years across late 2025 and early 2026. Confirm the target environment (Power BI Desktop/service version, Analysis Services version) actually supports a feature before writing it into a production model, especially anything still in preview.

- **User-Defined Functions (UDFs)** — named, parameterized DAX functions defined once within the model and called like any built-in function, instead of copy-pasting the same pattern (e.g. a time-intelligence variant) across many measures. Entered preview in September 2025 and reached **general availability in the June 2026 release** — safe to use in production now, but requires database compatibility level 1702+ and isn't supported on Azure Analysis Services / SQL Server Analysis Services.
- **Week-level time intelligence** (`TOTALWTD`, `STARTOFWEEK`, `ENDOFWEEK`, `NEXTWEEK`, `PREVIOUSWEEK`, `OPENINGBALANCEWEEK`, `CLOSINGBALANCEWEEK`) — replace hand-rolled `FILTER`/`WEEKNUM` workarounds, but take a **Calendar object**, not a date column — see `patterns.md` for exact syntax and the common mistake of passing a date column instead. Still preview as of late 2026.
- **Calendar-based time intelligence** — the feature that the week functions above depend on: calendar-parameterized variants of built-in time-intelligence functions, useful for fiscal/non-Gregorian calendars. Still preview.
- **`TABLEOF`** (Feb 2026) — returns the table associated with a specified column, measure, or calendar; useful for programmatically deriving a table reference rather than hardcoding it.
- **`RANK`/`ROWNUMBER`** (2023) and **visual calculations** generally — calculations authored directly against the visual's matrix (rows/columns as already laid out), which can replace fairly involved `RANKX`/running-total DAX with something simpler when the calculation is inherently visual-shaped rather than a reusable model-level measure.
- **Direct Lake mode** — for Fabric-backed models, Direct Lake queries OneLake-resident Parquet files directly instead of importing into VertiPaq, which changes the performance/refresh trade-off calculus (no import refresh window, but different query characteristics than a fully in-memory Import-mode model). Worth flagging as a modeling-level decision, not something a measure rewrite alone can substitute for.
- **AI-generated DAX (Copilot in Power BI Desktop)** — can produce syntactically valid measures with subtle filter-context bugs that only show up in specific visual configurations. Always review AI-generated DAX the same way you'd review a human's first draft — check context transition and filter-argument behavior explicitly, don't just check that it runs.

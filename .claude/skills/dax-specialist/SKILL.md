---
name: dax-specialist
description: Write, review, debug, and optimize DAX (Data Analysis Expressions) for Power BI, Analysis Services, or Power Pivot — measures, calculated columns, calculated tables, time intelligence, ranking, running totals, and calculation groups. Use this skill whenever the user asks for a DAX formula or measure, says a number in their report looks wrong, wants a year-over-year/running-total/ranking calculation, asks why a measure or report is slow, or describes a calculation they want in Power BI without necessarily saying "DAX" out loud.
---

# DAX Specialist

DAX bugs and DAX performance problems both come from the same root cause: not tracking what the **filter context** is at each point in the calculation. Get that right first; the function-specific tricks in the reference files matter far less than this mental model.

## The mental model

- **Row context** exists inside calculated columns and iterator functions (`SUMX`, `FILTER`, etc.) — it means "one row is currently active, so unqualified column references resolve to that row's value."
- **Filter context** is the set of filters currently applied — from slicers, visual axes, page/report filters, and any `CALCULATE` in the call stack. A **measure** always evaluates inside a filter context, never a row context.
- **`CALCULATE`** is the only way to modify filter context. Every filter argument to `CALCULATE` either adds a new filter or replaces an existing filter on the same column(s) — it does not add on top of an existing filter on that same column.
- **Context transition** happens when a row context is converted into filter context — this occurs implicitly whenever `CALCULATE` (or an iterator that calls a measure) is evaluated inside a row context, such as inside `SUMX` over a table, or in a calculated column that references a measure. This is the single most common source of "why is this measure returning something unexpected" bugs — a measure that looks fine standalone can behave completely differently when referenced from inside an iterator.

If a measure returns a wrong (not just slow) number, the fix is almost always to trace what filter context it's actually running under at the point of failure — use variables to snapshot intermediate values and inspect them, rather than guessing at the final expression.

## Measure vs. calculated column vs. calculated table

| | Evaluated | Stored | Use for |
|---|---|---|---|
| Measure | At query time, in current filter context | No (computed on demand) | Aggregations, ratios, anything that should respond to slicers/filters |
| Calculated column | At refresh time, per row | Yes (increases model size) | Values needed as a slicer, sort key, or relationship key — things that can't be a measure because they're not aggregations |
| Calculated table | At refresh time | Yes | Rarely needed; mostly for date tables or fixed lookup/mapping tables |

Defaulting to calculated columns for things that are really aggregations is the most common modeling mistake — it bloats the model and computes at refresh time instead of query time, and stops the value from responding to report filters correctly.

## Golden rules

1. **Use variables (`VAR`/`RETURN`).** They make formulas readable, guarantee a sub-expression is evaluated only once (real performance win when reused), and make debugging tractable — return a variable directly mid-formula to inspect what it holds.
2. **Prefer a boolean filter argument over `FILTER(table, condition)`** in `CALCULATE`: `CALCULATE([Sales], Product[Color] = "Red")` is generally cheaper than `CALCULATE([Sales], FILTER(Product, Product[Color] = "Red"))`. When `FILTER` is genuinely needed (multi-column or cross-row conditions), filter the smallest possible table — `FILTER(VALUES(Product[Color]), ...)` over the column's distinct values, not the whole table.
3. **Don't nest iterators unnecessarily.** `SUMX`/`AVERAGEX`/etc. scan row-by-row; calling another iterator (or a measure that contains one) inside them multiplies the cost.
4. **Physical relationship vs. `USERELATIONSHIP` vs. `TREATAS`** — pick based on what the relationship *means*, not which one benchmarks faster in isolation: a physical relationship is for a stable, reusable structural link; `USERELATIONSHIP` activates an existing-but-inactive relationship for one calculation; `TREATAS` applies a virtual filter across columns with no physical relationship at all (e.g. joining on a business key across unrelated tables).
5. **Don't use DAX to fix upstream data problems.** If a measure is full of special-casing for inconsistent categories or messy joins, that logic usually belongs in Power Query, the source SQL, or the model design — not papered over in every measure that touches it.

## Where to go next

- **Common calculation patterns** (time intelligence including new week-level functions, ranking, running totals, percent-of-total, dynamic segmentation, calculation groups): `references/patterns.md`
- **Performance diagnosis and optimization** (VertiPaq engine behavior, iterator cost, data type/encoding choices, profiling with DAX Studio, and what's new in DAX as of 2025–2026): `references/performance.md`

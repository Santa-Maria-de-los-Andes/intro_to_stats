# DAX Calculation Patterns

Assumes a standard star schema with a marked Date table related to fact tables on a date key, unless noted otherwise.

## Time intelligence

**Year/quarter/month to date:**

```dax
Sales YTD = TOTALYTD([Total Sales], 'Date'[Date])
Sales QTD = TOTALQTD([Total Sales], 'Date'[Date])
Sales MTD = TOTALMTD([Total Sales], 'Date'[Date])
```

**Prior period comparison:**

```dax
Sales PY = CALCULATE([Total Sales], SAMEPERIODLASTYEAR('Date'[Date]))
Sales YoY % = DIVIDE([Total Sales] - [Sales PY], [Sales PY])
```

`SAMEPERIODLASTYEAR` is a shorthand for `DATEADD('Date'[Date], -1, YEAR)` — reach for `DATEADD` directly when you need an arbitrary offset (e.g. -1 month, -7 day) rather than a fixed year shift.

**Week-level time intelligence (preview, introduced September 2025):** DAX previously had no first-class week equivalent to `TOTALYTD`/`SAMEPERIODLASTYEAR` — teams worked around it with manual `FILTER`/`DATESBETWEEN` logic. These now exist, but they don't work like the classic functions: `TOTALYTD`/`TOTALQTD`/`TOTALMTD` take a **date column**, while the week functions take a **Calendar object reference** and only work once calendar-based time intelligence is configured on the model:

```dax
Sales WTD      = TOTALWTD([Total Sales], FiscalCalendar)
Week Start     = STARTOFWEEK(FiscalCalendar)
Week End       = ENDOFWEEK(FiscalCalendar)
Next Week      = NEXTWEEK(FiscalCalendar)
Previous Week  = PREVIOUSWEEK(FiscalCalendar)
Opening Bal WK = OPENINGBALANCEWEEK([Total Sales], FiscalCalendar)
Closing Bal WK = CLOSINGBALANCEWEEK([Total Sales], FiscalCalendar)
```

`TOTALWTD([Total Sales], 'Date'[Date])` — passing a date column where a Calendar object is expected — is the classic-time-intelligence pattern and will not work here; this is the most likely mistake when adapting existing YTD/QTD/MTD measures to WTD. The Calendar object itself is a model-level construct you set up once (see the Power BI Modeling MCP skill's `calendar_operations`), not something referenced inline from a date table. If you see hand-rolled `FILTER('Date', WEEKNUM(...) = ...)` patterns in an older model, these functions are very likely a cleaner replacement once calendar-based time intelligence is configured — still preview as of late 2026, so confirm the target Power BI Desktop/service version supports it first.

**Custom/fiscal calendars:** calendar-aware variants of the built-in time-intelligence functions (accepting a custom calendar parameter, useful for non-Gregorian fiscal calendars) entered public preview alongside the week functions. Confirm current availability/syntax before relying on them in a production model — preview features can change before general availability.

## Ranking

```dax
Sales Rank = RANKX(ALL(Product[ProductName]), [Total Sales], , DESC, DENSE)
```

`RANK` and `ROWNUMBER` (introduced 2023) are lighter-weight alternatives usable directly in visual calculations (calculations authored on the visual matrix itself, referencing columns/measures/other visual calculations) without needing to reconstruct the full evaluation context that `RANKX` requires — reach for them when the ranking is happening at the visual level rather than as a reusable measure.

## Running totals / moving averages

```dax
Running Total =
CALCULATE(
    [Total Sales],
    FILTER(ALLSELECTED('Date'[Date]), 'Date'[Date] <= MAX('Date'[Date]))
)

Moving Avg 3M =
AVERAGEX(
    DATESINPERIOD('Date'[Date], MAX('Date'[Date]), -3, MONTH),
    [Total Sales]
)
```

`ALLSELECTED` (not `ALL`) is what makes a running total respect other filters/slicers on the report while still ignoring the date axis's own filter — using `ALL` here would ignore *every* other filter too, not just the date one.

## Percent of total

```dax
% of Total = DIVIDE([Total Sales], CALCULATE([Total Sales], ALL(Product)))
```

Always use `DIVIDE(numerator, denominator[, alternate result])` instead of the `/` operator for anything that can divide by zero — it returns blank (or your alternate result) instead of an error, and is marginally faster since it avoids exception handling.

## Dynamic segmentation with a disconnected table

Useful for "what-if" style parameters or user-selectable thresholds not tied to any fact table:

```dax
Selected Threshold = SELECTEDVALUE('Threshold Parameter'[Value], 100)

Above Threshold Sales =
CALCULATE(
    [Total Sales],
    FILTER(ALL(Customer), [Total Sales] > [Selected Threshold])
)
```

## Conditional logic: SWITCH over nested IF

```dax
Sales Tier =
SWITCH(
    TRUE(),
    [Total Sales] > 100000, "Gold",
    [Total Sales] > 50000,  "Silver",
    [Total Sales] > 0,      "Bronze",
    "No Sales"
)
```

`SWITCH(TRUE(), ...)` reads top-to-bottom like a series of `ELSE IF`s and is much easier to extend/audit than nested `IF`s of more than two or three levels.

## Calculation groups (avoiding measure sprawl)

If a model has separate physical measures for every time-intelligence variant of the same base metric (`Sales YTD`, `Sales QTD`, `Sales PY`, `Sales YoY %`, repeated again for `Margin`, `Units`, ...), a **calculation group** collapses that into one reusable set of calculation items applied to whichever base measure is in the visual:

```dax
CALCULATIONGROUP 'Time Intelligence'
    CALCULATIONITEM "YTD" = CALCULATE(SELECTEDMEASURE(), TOTALYTD)  -- illustrative; exact TOM/TMDL authoring syntax differs
    CALCULATIONITEM "PY"  = CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Date'[Date]))
```

Calculation groups are authored through the model (TOM/TMDL — see the Power BI Modeling MCP skill's `calculation_group_operations` if that tool is available) rather than as plain measure DAX; the calculation item's expression wraps `SELECTEDMEASURE()`, which stands in for whatever base measure is currently on the visual. Reach for this once you notice the same time-intelligence (or unit-conversion, or currency-conversion) pattern being copy-pasted across many base measures.

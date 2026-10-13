# Chart Selection

Start from the analytical intent, not the chart you already like. Every visualization answers one of a small number of underlying questions — find the question first, then this narrows to 2-3 reasonable chart types, and the data's shape (how many categories, how many series, continuous vs. discrete) picks the winner among those.

## Quick-reference by intent

| Intent | Question being answered | Default chart | Switch to when... |
|---|---|---|---|
| Comparison among items | How do these categories stack up against each other? | Bar/column chart | >10-12 categories → sort + top-N with "other"; comparing to a target → bullet chart |
| Trend over time | How has this changed? | Line chart (continuous) or column chart (few discrete periods) | Many series → small multiples instead of one crowded line chart; only two time points, many categories → slope chart |
| Distribution | What's the spread/shape of these values? | Histogram | Comparing distributions across groups → box plot or violin plot; want to see every point → strip/dot plot |
| Composition (part-to-whole) | How do the parts make up the whole? | Stacked bar (few categories/periods) | Many categories or hierarchy → treemap; showing a bridge from one total to another (e.g. starting revenue → ending revenue via gains/losses) → waterfall chart; ≤5 slices and a single snapshot in time → pie/donut is tolerable, though a sorted bar is usually still clearer |
| Relationship/correlation | Does X relate to Y? | Scatter plot | Third dimension (size = magnitude) → bubble chart; many variables pairwise → correlation heatmap |
| Ranking | Who's on top, and has that changed? | Sorted bar chart (single point in time) | Rank changing over time → bump chart |
| Geospatial | Where is this happening? | Choropleth (rate/intensity by region) | Individual event locations → point/pin map |
| Single KPI / headline number | What's the one number that matters right now? | Big number ("card") with a small trend sparkline and a delta vs. target | Comparing a handful of top-line KPIs together → a small row of cards, not a chart |

## Data-shape thresholds worth knowing

- **Categories on a bar chart:** comfortable up to ~10-12 with sorting; beyond that, show the top N plus an "other" bucket, or switch to a scrollable/paginated table — cramming 40 bars into one chart defeats the purpose of visualizing at all.
- **Lines on a line chart:** beyond ~5-6 series, a single chart becomes a "spaghetti chart" that's unreadable. Switch to **small multiples** (one mini-chart per series, same axes, arranged in a grid) — it trades one dense chart for several simple ones, which is almost always the right trade.
- **Pie/donut charts:** human perception is bad at comparing angles/areas precisely. They're tolerable for 2-3 categories where the point is "roughly half" or "the vast majority" — beyond ~5 slices, or whenever precise comparison between slices matters, a sorted bar chart communicates the same information more accurately.
- **Dual-axis charts** (two different y-axes on the same plot) let you visually align two series that may have no real relationship, implying correlation that isn't there. If you need to show two differently-scaled series together, consider indexing both to a common baseline (e.g. % change from period 0) on a single axis instead, or use small multiples.

## Matching chart to audience fluency, not just data shape

The same data can justify different charts depending on who's looking:

- **Skimming exec, 5 seconds:** one annotated number or a simple sorted bar — no more than one takeaway per glance.
- **Working analyst:** can handle a denser small-multiples grid, a scatter with many points, or an interactive table with sort/filter — precision and explorability matter more than instant readability.
- **Mixed/public audience:** favor the most familiar chart types (bar, line) over more specialized ones (violin plots, bump charts) even when the specialized type is technically more precise — an unfamiliar chart type adds a "how do I read this" tax that competes with the actual message.

## When more than one chart type genuinely fits

It's common for two candidates to both be defensible (e.g., a line chart vs. a column chart for a trend with only 4-5 time periods). In that case, the tiebreaker is usually: continuous/many periods → line; discrete/few periods where each period is a distinct, nameable thing (like quarters that get individually referenced) → column. When still unsure, default to whichever chart type the intended audience already reads most often elsewhere — consistency with what people are used to reduces interpretation error more than a marginally "more correct" novel choice.

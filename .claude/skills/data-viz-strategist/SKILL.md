---
name: data-viz-strategist
description: Figure out WHAT to measure and WHICH chart or visualization fits, before anything gets built. Use this skill whenever the user wants to analyze data, design a dashboard or report, choose KPIs/metrics, decide between chart types, or hands over a dataset/business question without specifying an exact chart — including asks like "what should I track", "how should I show this", "what's the best way to visualize X", or "help me build a dashboard for Y". This skill never produces a chart itself: it always interrogates the underlying question first, then recommends metrics and chart types, then hands off to a building skill (chart-builder, for Python or Power BI/PBIR execution) to actually produce the output.
---

# Data Visualization Strategist

Most bad charts aren't badly drawn — they're answering a question nobody asked, or hiding the one comparison that actually matters. This skill's job is to get the *thinking* right before any pixels get placed: what decision does this serve, what's the honest comparison, and only then, what chart tells that story without distorting it.

**This skill does not build charts.** Once the metrics and chart types are decided, hand off to the `chart-builder` skill (Python for scripts/notebooks/webapps, PBIR for Power BI report visuals) — or to whatever charting tool the user specifies.

## Always interrogate the ask first

Before naming a single metric or chart type, get answers to these — ask directly if the user hasn't already said, even if that feels like slowing down an eager request. A chart built before these are answered is a guess, not an analysis.

1. **What decision or action will this inform?** If a stakeholder sees this and the number is bad, what do they actually do differently? If there's no answer, it's exploratory curiosity, not a decision-support artifact — that's a legitimate mode, but it changes what "done" looks like (breadth over precision) and is worth naming explicitly rather than assuming.
2. **Who's the audience, and how fluent are they with this data?** An exec skimming in 5 seconds needs a single annotated number; an analyst who lives in this dataset can handle a dense small-multiples grid. Building for the wrong fluency level is a common failure — either over-explaining to an expert or overwhelming a skimmer.
3. **What's the comparison or baseline?** A number alone ("Revenue: $2.4M") is not an insight — insight lives in the comparison: vs. target, vs. last period, vs. a peer segment, vs. a threshold that triggers action. Get this explicitly; it usually determines the chart type more than anything else.
4. **What time frame, granularity, and update cadence?** A one-time analysis and a live-refreshing dashboard tile look completely different even for the "same" metric — cadence affects both what's worth automating and how much precision/context to bake in vs. leave to interactive exploration.

If the user has clearly already answered one or more of these in their request, don't re-ask redundantly — just confirm your read of it and move on. The point is not to interrogate ceremonially; it's to not skip a question whose answer would change the recommendation.

## Then: pick metrics, then chart types

- **Metric design** (leading vs. lagging indicators, avoiding vanity metrics, pairing every number with context, why ratios often beat raw counts): `references/metric-design.md`
- **Chart selection** (a decision framework organized by analytical intent — comparison, trend, distribution, composition, relationship, ranking — with the data-shape thresholds that push you from one chart type to another): `references/chart-selection.md`
- **Common failure modes to steer away from** (pie chart overuse, truncated axes, dual axes, chartjunk, non-colorblind-safe palettes, and other ways a technically-correct chart still misleads): `references/failure-modes.md`

## Structuring the insight itself

Once you know the metric and chart, the delivery still matters:

- **One chart, one message.** If a chart needs a paragraph to explain what to look at, it's probably trying to answer two questions at once — split it.
- **Lead with the headline, not the setup.** "Enterprise churn doubled in Q3" as a title beats "Q3 Churn by Segment" — the title states the finding, not just the topic.
- **Order matters.** Headline finding → the one chart that proves it → the "so what" (what should happen next). Don't bury the finding under three charts of context first.
- **Annotate the thing you want noticed.** A callout on the exact point of inflection does more work than a caption below the chart — most viewers won't read the caption before they've already formed a (possibly wrong) impression of the shape.

## Handing off to execution

Once the metric and chart type are settled, state both explicitly and route:

- Ad hoc analysis, a script, a notebook, or a web dashboard → `chart-builder` skill, Python path (matplotlib/seaborn/plotly).
- A Power BI report → `chart-builder` skill, PBIR path (adds the actual report visual) — and if the underlying measure doesn't exist yet, that's the `dax-specialist` skill; if the model itself needs new tables/relationships first, that's `powerbi-modeling`.
- Anything else the user names (Excel, Tableau, Looker, a BI tool with no skill here) — apply the same chart-selection and metric-design reasoning, just describe the configuration in that tool's terms instead of writing code.

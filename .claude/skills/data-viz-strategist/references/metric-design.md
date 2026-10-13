# Metric Design

Picking the right chart doesn't help if it's charting the wrong number. Get the metric right first.

## Leading vs. lagging indicators

A **lagging** metric confirms what already happened (revenue, churn, quarterly profit) — useful for reporting, useless for steering, since by the time it moves, the causes are already in the past. A **leading** metric predicts what's about to happen (trial signups, pipeline created, activation rate, support ticket backlog growth) — useful for steering, because there's still time to act.

A dashboard built entirely from lagging metrics tells you how last quarter went; it can't tell anyone what to do differently this week. When the audience needs to *act*, push toward leading indicators even if they're noisier or harder to define — precision on the wrong metric is worse than a rougher read on the right one.

## Vanity metrics vs. actionable metrics

A metric is actionable if a change in it should change a decision. A metric is a vanity metric if it almost always goes up, is easy to inflate without changing anything real, and doesn't connect to a specific action. Classic vanity metrics: total signups (without activation/retention alongside it), total pageviews (without conversion or engagement depth), cumulative anything (cumulative totals always go up — they hide whether the current period is actually healthy).

The fix is usually to pair a cumulative/absolute number with a rate or a period-over-period figure: not "10M total users" but "10M total users, +2% MoM active, down from +5% MoM active six months ago" — the second framing is the one that changes what someone does next.

## Ratios and rates usually beat raw counts

Raw counts conflate two things: how much of the underlying activity there is, and how well it's converting/performing. A raw count also breaks comparisons across time periods or segments that have different sizes (30 signups from a segment of 300 vs. 30 from a segment of 30,000 mean very different things).

Prefer a rate or ratio when the audience needs to know if something is *working* (conversion rate, error rate, cost per acquisition); keep the raw count alongside it when the audience needs to know *scale* (how big is this problem/opportunity in absolute terms) — often you need both, shown together rather than one substituting for the other.

## Every number needs context to be an insight

A single number in isolation can't be judged as good or bad. Context comes from one or more of:

- **A target or threshold** — is this above/below what was planned or what triggers action?
- **A time comparison** — vs. last period, vs. same period last year (controls for seasonality).
- **A peer/segment comparison** — vs. another team, region, cohort, or competitor.
- **A distribution** — is this number typical, or an outlier relative to the normal range?

A KPI card showing "Conversion rate: 3.2%" with nothing else forces the viewer to supply their own (possibly wrong) sense of whether that's good. The same card with a small trend sparkline and a delta vs. target turns it into something actionable.

## Watch for noise being mistaken for signal

Short time windows and small sample sizes produce a lot of random-looking movement that isn't actually meaningful. Before treating a week-over-week or day-over-day change as a finding, sanity-check: is the underlying volume large enough that this swing is unlikely to be noise? When volume is genuinely low, prefer a rolling average or a longer comparison window over the raw daily figure, and say so explicitly rather than let a single noisy data point drive a headline.

## Metric definition hygiene

Ambiguous metric names cause more dashboard distrust than bad charts do. "Active user" defined three different ways across three different reports (logged in? took an action? within what window?) will eventually get noticed, and once it is, people stop trusting every number in the dashboard, not just that one. When proposing a metric, state its exact definition (the filter conditions, the time window, what counts and what's excluded) alongside it — don't assume the name is self-explanatory.

---
name: insight-discovery
description: Find patterns, drivers, and stories in a dataset for descriptive/BI analysis (not model fitting) -- use whenever a user has profiled or loaded data and asks "what's going on here", "what stands out", "why did X change", "who improved or declined", "what's driving the gap", "find the story", or wants to compare segments, cohorts, groups, or periods. Forms hypotheses, then tests them with segmentation, variance decomposition, movement analysis (up/same/down), and outlier checks. Enforces effect sizes and small-sample caution so noise is not reported as a finding. Outputs a ranked list of findings, each with evidence, confidence, and the "so what", as the input for data-storytelling and data-viz-strategist. Use after data-exploration, before choosing charts.
---

# Insight Discovery

Data rarely announces its own story. Most of what looks like a pattern in a table is noise, a data-quality artifact, or something everyone already knows. This skill's job is to get from "I have clean data" to "here are the few things that are real, sized, and worth acting on", and to be honest about which are which.

It sits in the middle of the chain: `data-exploration` (is the data sound?) → **insight-discovery** (what's in it?) → `data-viz-strategist` (how to show it) → `chart-builder` (draw it). It does not draw charts and does not fit predictive models. If the user only wants a chart, go to `data-viz-strategist`; if they want to fit or compare models, this is the wrong skill.

## 1. Pin down the question before touching the data

Ask (or infer from the request, then confirm in one line) only what would change the analysis:

- **What decision could this inform?** A finding nobody can act on is trivia. This determines what counts as "interesting" — a 2-point gap that triggers a resource decision matters more than a 20-point gap in an irrelevant segment.
- **What is the comparison?** Insight lives in a contrast: period vs period, segment vs segment, actual vs expectation/threshold. Name the contrast(s) up front.
- **What is the unit of analysis?** (student, class, order, account.) Mixing units is the commonest source of wrong numbers: averaging averages, or counting an entity once per row.
- **Anything already known or decided?** Previously made exclusions, known quirks, findings the user already has. Do not "discover" what they told you, and do not re-include rows they chose to exclude.

## 2. Re-check the rows before believing any number

Do a short sanity pass even if `data-exploration` ran, because analysis choices create new traps:

- Rows that are not real observations: zeros that mean "failed/missing", duplicates, test records, placeholder entities. They inflate segment sizes and drag means. State what you excluded and how many rows.
- Comparability: did the measurement itself change between periods (different instrument, different difficulty, different definitions)? If so, raw deltas are partly artifact — say so, and prefer relative measures (rank/percentile position within group) over raw differences.
- Matched vs unmatched entities across periods. Compare changes only for entities present in both, and report how many that is.

## 3. Generate hypotheses, then test them

Write 5–10 candidate hypotheses *before* computing, from the question and from domain sense ("the gap is concentrated in one segment", "the average rose but only because weak entities left", "one outlier group drives the spread"). Then test each with the cheapest method that can refute it. Scanning every cut of the data and reporting whatever lights up is how noise gets promoted to a finding.

Methods, and when each is the right tool (details and recipes in `references/methods.md`):

| Question | Method |
|---|---|
| Where does the gap/level differ? | **Segmentation**: metric by segment, with n and spread per segment |
| Why did the total change? | **Variance decomposition**: split the change into within-segment change, mix shift, and entry/exit |
| Who moved, and which way? | **Movement analysis**: classify each entity Up / Same / Down against a noise threshold, then count and characterise each group |
| Is this one weird case or a pattern? | **Outlier check**: does the finding survive removing the top/bottom few entities? |
| Is the pattern real or sampling luck? | **Effect size + uncertainty**: see section 4 |

For movement analysis, never call everything that is not exactly equal "changed". Set a *clear-change threshold* from the measurement's own noise (e.g. the size of one unit of the score, or the typical spread between repeat measurements) and call anything inside it "Same". Report the Same group explicitly: "most entities didn't clearly change" is frequently the honest headline.

## 4. Guardrails: what earns the word "finding"

A result is only reported as a finding if it passes all of these. This is the part of the skill that matters most; it is what keeps the output from being a list of coincidences.

- **Effect size first, significance second.** Report the size in the metric's own units (percentage points, currency, days) and as a standardised effect (Cohen's d or similar) when comparing groups. A tiny difference that is "significant" in a huge sample is not a finding; a large difference in a small group may be, but with caveats.
- **Small-n rule.** Below roughly 10 entities per group, do not rank or compare groups on means alone. Show n beside every number, widen language ("suggests", "leans"), and prefer showing the individual points. Below ~5, describe the entities individually instead of summarising them.
- **Uncertainty is part of the result.** Give an interval or a bootstrap range for the headline numbers, or at minimum say whether the gap is bigger than the spread within the groups.
- **Multiple comparisons.** If you looked at 30 cuts, expect some to pop by chance. Count how many you looked at and demote findings that only appear in one lucky cut without a prior hypothesis.
- **Survivorship and composition.** Check that an "improvement" is not just who stayed in the sample, and that a "decline" is not just a change in mix.
- **Correlation stays correlation.** Name a driver as a *candidate* explanation unless something in the design supports causation. Offer the alternative explanation beside it.
- **Regression to the mean.** Groups selected for being extreme (bottom performers, top accounts) drift back toward average without any intervention. Do not credit an intervention for that without a comparison group.

## 5. Output: a ranked findings list

Produce this structure so downstream skills can consume it directly. Rank by (size of effect × relevance to the decision × confidence), not by how surprising it is.

```
## Scope and data notes
Rows analysed, rows excluded (and why), comparability caveats, n for each comparison.

## Findings (ranked)
### 1. <One-sentence headline that states the finding, not the topic>
- Evidence: the numbers (effect in units, n, interval), the comparison it comes from
- Confidence: High / Medium / Low — and the one reason (e.g. "n=8 per group", "survives outlier removal")
- So what: the decision or action it bears on, and who would act
- Alternative explanation: what else could produce this, and whether checked
- Suggested view: the comparison a chart should show (hand off to data-viz-strategist)

### 2. ...

## Looked at and dropped
Hypotheses tested that did not hold (one line each). This is useful: it stops the user asking
"did you check X?" and shows the negative space.

## Open questions
What would need more data, a longer period, or a domain answer to settle.
```

Keep it to the findings that matter, typically 3–7. If nothing passes the guardrails, say so plainly and report the "Same / no clear difference" result; "nothing reliably changed" is a real answer and more useful than a manufactured story.

## 6. Hand off

State the top findings and the comparison each one needs shown, then route to `data-viz-strategist` for chart choice (and `chart-builder` after that). If the user wants narrative packaging (a written story, a briefing), the findings list is the input; lead with the headline, then the one piece of evidence that proves it, then the so-what.

## Gotchas

- Do not average percentages or scores across groups of different sizes without weighting; report the weighted figure and say how it was weighted.
- Do not compare periods with different measurement difficulty by raw difference; say what is lost and use position or standardised scores instead.
- Do not name individuals in findings unless the user's audience and privacy rules allow it; describe segments instead and offer the named list separately.
- A finding the user already decided to exclude or already told you is not a discovery. Respect prior decisions even when the data would tempt you to revisit them.

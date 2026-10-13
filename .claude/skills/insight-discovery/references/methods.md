# Methods recipes

Pandas-flavoured sketches. Adapt names; the logic is what matters.

## Contents
- Segmentation
- Variance decomposition (what drove the change in a total)
- Movement analysis (Up / Same / Down)
- Outlier robustness check
- Effect size and uncertainty

## Segmentation

Always show n and spread next to the mean, never the mean alone.

```python
g = df.groupby("segment")["metric"]
seg = g.agg(n="count", mean="mean", sd="std", median="median").round(2)
seg["se"] = seg["sd"] / seg["n"] ** 0.5
```

Flag segments with n < 10 in the output. Sort by the quantity that bears on the decision, not alphabetically.

## Variance decomposition

Overall change = change within segments + change in segment mix (+ entry/exit). Use it when a total moved and someone asks "why".

```python
# a = earlier period, b = later period; w = share of entities, m = segment mean
within = ((m_b - m_a) * (w_a + w_b) / 2).sum()   # performance change holding mix fixed
mix    = ((w_b - w_a) * (m_a + m_b) / 2).sum()   # change caused only by who is in which segment
# within + mix == total change (midpoint weighting)
```

If `mix` dominates, the headline is "the population changed", not "performance changed". Also compute the total for matched entities only and compare with the total for everyone: a gap between them is entry/exit.

## Movement analysis

1. Choose the comparable quantity. If the instrument changed between periods, use position (percentile within the matched group) instead of the raw value.
2. Choose the noise threshold from the measurement: at least one unit of the score (e.g. one question = 100/n_questions points), or the observed spread of repeat measurements. Anything within it is "Same".
3. Classify, then describe each group.

```python
d = after - before
move = np.select([d >= thr, d <= -thr], ["Up", "Down"], default="Same")
summary = pd.Series(move).value_counts().reindex(["Up", "Same", "Down"], fill_value=0)
```

Report counts and shares of all three, and what distinguishes Up from Down (segment, starting level). Watch regression to the mean: entities that started low will tend to show Up.

## Outlier robustness check

A finding should survive dropping the most extreme few.

```python
trimmed = df[(df.metric > df.metric.quantile(.05)) & (df.metric < df.metric.quantile(.95))]
# recompute the finding on `trimmed`; if the gap flips or collapses, say it is outlier-driven
```

Also try leave-one-group-out for segment findings.

## Effect size and uncertainty

```python
def cohens_d(a, b):
    na, nb = len(a), len(b)
    sp = (((na-1)*a.var(ddof=1) + (nb-1)*b.var(ddof=1)) / (na+nb-2)) ** 0.5
    return (a.mean() - b.mean()) / sp

def boot_ci(a, b, n=5000, seed=0):
    rng = np.random.default_rng(seed)
    diffs = [rng.choice(a, len(a)).mean() - rng.choice(b, len(b)).mean() for _ in range(n)]
    return np.percentile(diffs, [2.5, 97.5])
```

Rough reading of d: ~0.2 small, ~0.5 medium, ~0.8 large, but the decision relevance of the raw-units difference outranks the label. If the bootstrap interval spans zero, the honest wording is "no clear difference", not "a small difference".

# Common Failure Modes

A chart can be technically well-made and still mislead, or technically accurate and still unreadable. Watch for these specifically.

## Distortion (charts that mislead even when the data is correct)

- **Truncated / non-zero y-axis on a bar or column chart.** Bar length encodes magnitude visually — starting the axis at anything but zero exaggerates differences (a bar twice as tall implies "twice as much," which is only true from a zero baseline). This is the single most common way to accidentally (or not-so-accidentally) oversell a small difference. Line charts are more forgiving of a non-zero baseline when the point is rate-of-change rather than magnitude, but say so explicitly (e.g., annotate the axis start) rather than let it pass silently.
- **Dual-axis charts implying correlation.** Placing two independently-scaled series on the same plot with two y-axes lets you visually align any two lines you want, regardless of whether they're actually related — the visual correlation is an artifact of axis scaling choices, not the data. If both series need to be shown together, index them to a common baseline instead.
- **3D charts.** 3D bar/pie charts distort perceived size and position due to perspective — a slice further from the viewer looks smaller than an identical one closer up. There's essentially no case where 3D improves a business chart's accuracy; treat any 3D chart as a defect to flatten.
- **Cherry-picked time windows.** A time range chosen specifically because it makes a trend look better/worse than the fuller picture would show. If zooming into a specific window, state why that window was chosen and what the longer trend looks like.
- **Using the mean when the distribution matters.** An average can hide a bimodal distribution, heavy skew, or outliers entirely — "average response time: 200ms" can be true while most users experience 50ms and a meaningful minority experience 3 seconds. When the spread matters (it usually does for anything user-experience-related), show a distribution (histogram, box plot) or at least a median + percentile alongside the mean.

## Unreadability (charts that are honest but still hard to use)

- **Pie/donut chart with too many slices.** Beyond ~5 categories, angle/area comparisons become guesswork. Sort and switch to a bar chart.
- **Spaghetti chart (too many lines on one plot).** Beyond ~5-6 series, individual lines become impossible to trace. Switch to small multiples or highlight only the 2-3 lines that matter, greying out the rest.
- **Chartjunk.** Unnecessary gridlines, background images, heavy borders, bevels/shadows on bars, or decorative icons compete with the actual data for attention. Maximize the "data-ink ratio" — every mark on the chart should carry information; if removing it loses nothing, remove it.
- **Inconsistent axis scales across small multiples meant to be compared.** If the whole point of a small-multiples grid is to compare panels at a glance, each panel needs the same axis range — letting each auto-scale independently makes "biggest bar" visually ambiguous across panels.
- **Rainbow/qualitative palettes on ordinal or continuous data.** A default categorical color palette applied to something with an inherent order (low→high, cold→hot) obscures the order. Use a sequential palette (single hue, increasing intensity) for one-directional continuous data, and a diverging palette (two hues meeting at a meaningful midpoint like zero) when values can be above or below a reference point.
- **Not designing for colorblindness.** Roughly 1 in 12 men have some form of color vision deficiency, most commonly red-green. Avoid red/green as the *only* signal distinguishing two categories (e.g., "red = bad, green = good" with no other cue) — pair color with a second channel (position, label, icon, pattern) or use a colorblind-safe palette (e.g., Okabe-Ito for categorical, viridis/cividis for continuous).
- **Legend-only color mapping when direct labeling is possible.** Forcing the eye to bounce between a data point and a legend elsewhere on the page adds friction for every single lookup. When there are only a few series, label them directly at the line/bar end instead of relying solely on a legend.

## Mismatch (right chart execution, wrong chart for the question)

- **A trend question answered with a snapshot chart** (e.g., a single pie chart when the real question is "how has this mix changed over time" — that needs a stacked area or multiple pies/bars across periods, not one).
- **A ranking question answered with an unsorted bar chart.** If the point is "who's on top," an alphabetically- or category-ID-sorted bar chart forces the viewer to do the ranking themselves — sort by value.
- **A composition question answered with a bar chart per category instead of a part-to-whole chart** — bars are great for comparing category magnitudes, but don't visually communicate "these sum to 100%" the way a stacked bar or treemap does.

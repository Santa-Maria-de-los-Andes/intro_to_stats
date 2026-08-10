# BIMESTRE 3: STATISTICS IN PYTHON
## 3rd-5th Secondary | Ages 15-17 | 7-8 Weeks

**Format:** Jupyter Notebooks with gamified narrative theme
**Prerequisite Python Skills:** For loops, if statements, basic functions (Bimestre 2)
**Core Philosophy:** Statistical thinking first, code as the tool to get there — not the other way around

---

## 🎯 MODULE LEARNING OBJECTIVES

By the end of this module, students will:
- Load, filter, and describe real datasets using pandas
- Calculate and interpret descriptive statistics in context
- Distinguish correlation from causation and critique data claims
- Understand what linear regression and k-means clustering *do* and *when to use them* (not the underlying math)
- Complete an independent analysis of a real dataset and present findings

**Explicitly NOT a goal:** Mathematical derivation of statistical formulas or ML algorithms. This is exposure and application, not theory.

---

## 🐍 PYTHON SCOPE (Keep It Lean)

**Technical spine for this module — nothing more:**
- `pd.read_csv()`, `.head()`, `.info()`, `.describe()`
- Boolean filtering: `df[df['column'] > value]`
- `.groupby()`
- `.mean()`, `.median()`, `.std()`, `.corr()`
- `matplotlib` scatter plots and basic charts
- `sklearn.linear_model.LinearRegression` — `.fit()` / `.predict()`
- `sklearn.cluster.KMeans` — `.fit_predict()`

**Do not** spend a standalone week on "pandas fundamentals" — teach each skill embedded in the analysis that needs it.

---

## 📅 WEEK-BY-WEEK OUTLINE

### Weeks 1-2: Pandas Bootcamp with Real Data
**Learning Target:** Load, explore, filter, and describe a dataset.

**Narrative Hook:** Frame as first "mission" — recover and stabilize a dataset before it can be analyzed.

**Core Activity:** Choose a dataset students care about (Peruvian economic data, sports stats, or social survey). Progression: load → explore → filter → grouped stats → comparative analysis.

**Deliverable:** Mini-analysis answering "What's the average? What's the spread? Who's an outlier?"

---

### Weeks 3-4: Correlation
**Learning Target:** Calculate and visualize correlation; build intuition before formalizing it.

**Sequence (important):**
1. Show scatter plots first — no code, just "what do you see?"
2. Introduce the correlation coefficient conceptually
3. Calculate it in code (`.corr()`)
4. Use `.groupby()` to explore correlation within subgroups

**Mini-Project (Week 4):** Find two strongly correlated variables in a dataset.

**Deliverable:** Scatter plot + correlation coefficient + short write-up.

---

### Week 5: Causation Reality Check
**Learning Target:** Distinguish correlation from causation; identify confounding variables; build healthy skepticism.

**Python Skills:** Minimal new code — this week is conceptual.

**Activities:**
- Analyze real-world "X causes Y" claims from news/social media
- Identify confounding variables
- Classic example (ice cream sales & drownings) → then student-found examples

**Deliverable:** Presentation debunking a correlation-causation claim, using their own dataset's correlated variables as evidence.

> **This is the critical-thinking lynchpin of the module.** Prioritize depth here over speed.

---

### Week 6: Linear Regression Showcase
**Learning Target:** Understand what regression predicts and how to interpret results — not the math behind it.

**Narrative Framing:** "We found a relationship. Now: if I know X, can I predict Y?"

**Example:** House price prediction (size → price). Fit model, predict, visualize the regression line.

**Deliverable:** Working regression model + plain-language interpretation ("For every extra sqm, price increases by ___").

---

### Week 7: K-Means Clustering Showcase
**Learning Target:** Understand what clustering does and when to use it.

**Narrative Framing:** "Instead of predicting a number, we're grouping similar things."

**Example:** Customer segmentation or athlete/player-type clustering.

**Worksheet Extension:** Explore how results change when k changes (e.g., k=3 vs k=5).

**Deliverable:** Clustered dataset with visualization + brief interpretation of each group.

---

### Week 8: Final Exam

---

## 🎮 GAMIFICATION / XP ARC

| Weeks | Focus | XP |
|---|---|---|
| 1-2 | Pandas Bootcamp | ~150 |
| 3-4 | Correlation + mini-project | ~180 |
| 5 | Causation critique | ~100 |
| 6 | Linear regression | ~150 |
| 7 | K-means clustering | ~120 |


---

## 📓 JUPYTER NOTEBOOK STRUCTURE (Per Week)

Each notebook should follow this internal sequence:

1. **Opening narrative** — themed mission framing ("A signal was recovered from the region — analyze it before the outbreak spreads.")
2. **Conceptual explanation** — text + visual, before any code
3. **Guided code examples** — worked demonstration
4. **Progressive challenge cells** — easy → medium → hard → bonus, each tagged with XP
5. **Checkpoint** — mastery gate (80%+) before unlocking next notebook

---

## 🧭 PEDAGOGICAL GUARDRAILS

- **Visualization before formalization.** Students see the scatter plot or the clusters before they learn the term for what they're looking at.
- **Code stays subordinate to the question.** Every code cell should be answering a statistical question posed in the narrative, not existing as a syntax drill.
- **Weeks 6-7 are showcases, not deep dives.** The success metric is "can they say when you'd use this?" — not "can they derive it?"
- **Week 5 deserves real time.** Skepticism about data claims is arguably the most transferable skill in this module — don't compress it to make room elsewhere.
- **Normalize "I don't fully understand why it works."** Acceptable ignorance framing: "You don't need to understand engines to drive safely." Grade on process and interpretation, not theoretical mastery.

---

## 📌 OPEN QUESTIONS FOR NEXT REVIEW

- [ ] Confirm datasets for Weeks 1-2 (Peruvian-specific vs. global datasets?)
- [ ] Finalize themed narrative arc across all 8 weeks (single storyline vs. mission-per-week?)
- [ ] Decide whether Week 8 capstone requires regression/clustering or makes it optional
- [ ] Set checkpoint mastery threshold (80%, consistent with rest of curriculum?)

---

*Document prepared as a working outline — subject to revision after Week 1-2 pilot and student feedback.*

---
name: data-storytelling
description: Turn analysis findings into a message for a specific audience -- use whenever a user has results and needs to decide what to say, in what order, to whom, and what to leave out ("how do I present this", "what's the headline", "write the exec summary", "this report is for the principal / teachers / parents"). Sets the headline and "so what" first, orders findings, cuts the rest, decides what each audience should and should not see (privacy, tone, level of detail), and ties each finding to an action or decision. Outputs a story spine (headline, 3-5 supporting points, caveats, recommended actions) that hands off to data-viz-strategist for chart choices. Does not build visuals or documents itself.
---

# Data Storytelling

Findings are not a message. A list of true things forces the reader to do the work of deciding which one matters, and most readers won't: they skim, take the first number they see, and leave with the wrong impression. This skill's job is the editorial step between "we have results" and "someone reads them": pick the one thing the audience must walk away with, order the evidence so it lands, cut what dilutes it, and decide what this particular reader should and should not see.

It sits after `insight-discovery` (what's real in the data?) and before `data-viz-strategist` (which chart shows it?) → `chart-builder` (draw it). It produces a **story spine**, not a finished document or chart. If the user just wants a chart, go to `data-viz-strategist`; if they still need to find out what the data says, go to `insight-discovery` first.

## 1. Pin down the reader before writing a word

The same findings become different messages for different readers. Ask (or infer from the request and confirm in one line) only what would change the story:

- **Who reads this, and what do they control?** A person who can reallocate budget needs a different message than one who can only change a classroom habit. Write to what they can act on.
- **What do they already believe or fear?** A message that contradicts a strongly held belief needs the evidence first and more care; one that confirms it can be short. Bad news for someone personally invested needs a constructive frame, not a softer truth.
- **How fluent are they with this data?** Fluent readers can take rates, intervals and jargon. Non-fluent readers need plain words, a few numbers, and a comparison they can feel ("7 of 10 students" beats "70.3%").
- **What is the moment of use?** Skimmed in 30 seconds, read at a desk, or spoken aloud in a meeting? That sets length and how much sits on the first screen.
- **Who else will see it?** Reports get forwarded. Write as if the widest plausible reader will see it, and keep anything that must stay private out of the file rather than trusting it won't travel.

If the user has already named the audience, confirm your read and move on. One wrong guess here spoils everything downstream, so when the audience is truly unclear, ask before drafting.

## 2. Find the headline

The headline is one sentence that states a finding and its consequence, not a topic. "Fifth grade math fell 8 points while every other subject held" is a headline; "Results by subject" is a label.

How to get there:

1. List the findings (from `insight-discovery` if it ran; otherwise from the user's results). Rank by *size of effect × relevance to this reader's decisions × confidence*. Surprise is not a criterion.
2. Ask: "If the reader remembers only one sentence next week, which should it be?" That is the headline.
3. Write the **so what** next to it: what should this reader think, decide, or do differently now. A headline with no so-what is trivia. If none exists, the finding probably doesn't belong in this message.
4. Test it: could the reader repeat the headline to a colleague without the document in front of them? If not, it's too long or too hedged.

"Nothing reliably changed" is a legitimate headline when it is true and the reader expected change. Don't manufacture drama to fill the space.

## 3. Build the spine

Output this structure. Keep the supporting points to 3-5; more than that and the reader retains none of them.

```
## Audience
Who, what they control, fluency, moment of use (one line each)

## Headline
One sentence, finding + consequence

## So what
What this reader should decide or do (the ask)

## Supporting points (3-5, in reading order)
1. <claim, stated as a sentence>
   - Evidence: the one number or comparison that proves it (with n where small)
   - Why it's here: what it adds (proof / scope / explanation / counter-check)
   - Suggested view: the comparison a chart should show (hand-off to data-viz-strategist)
2. ...

## Caveats worth stating
Only those that could change the reader's decision. Plain words, placed next to the claim they qualify.

## Recommended actions
Each tied to a finding, with an owner and a time frame if the user knows them. Mark which are suggestions and which are decisions already made.

## Left out, and why
Findings cut (too small, off-topic for this reader, too uncertain, or too sensitive for this audience). One line each.

## Open questions
What the user should settle before sending.
```

Ordering principle: headline → the one piece of evidence that proves it → scope (how widespread) → explanation (what seems to drive it) → what to do. Put the answer first and the support after; readers who stop early still leave with the right message. Chronological order ("first we looked at… then…") is how analysts think and almost never how readers want to read.

## 4. Cut

Cutting is most of the job, and the hardest part, because every finding cost effort to find. A finding stays only if it does one of these: proves the headline, shows its scope, explains it, or changes an action. Everything else goes to "Left out" or to an appendix. Specifically cut:

- Findings the reader can't act on, even if true.
- Results that are interesting but sit inside the noise (small groups, tiny effects); these make the reader distrust the solid ones.
- Methodology detail the reader didn't ask for. One sentence on how, with the rest on request or in an appendix.
- A second and third way of saying the same thing.

Keep the negative space visible to the user (the "Left out" list) so they can overrule a cut. Cutting silently and being wrong is worse than cutting openly.

## 5. Decide what this audience sees

Different readers get different cuts of the same truth. This is not spin: the facts stay identical, what changes is which ones this reader needs, and how they are framed. Make these decisions explicitly for every message and show them to the user, because they are the user's call, not yours.

- **Identity and privacy.** Who may be named? Individuals, staff, and small groups (where "the group of 3" identifies a person) are the usual risks. Default to describing segments, not people, and offer a named version separately for the audience entitled to it. Anything an unentitled reader must not learn should not be in the file at all.
- **Level of detail.** More detail for those who act at item/row level, less for those who decide at the portfolio level.
- **Tone on bad news.** State it plainly, then say what is being done or can be done. Do not bury it, blame, or sugar it: a reader who later discovers a softened number stops trusting the rest. Pair a low number with its context and its next step rather than leaving it bare.
- **Comparisons that could read as a ranking.** A leaderboard can be useful or corrosive depending on who reads it and what they fear. Ask before including one; if included, consider showing rank without scores, or recognition at the top only.
- **Claims about causes.** Audiences with personal stakes will read a candidate explanation as an accusation. Keep correlation labelled as correlation, and avoid attributing results to people.
- **Prescription vs information.** Some readers want recommendations; some (often professionals in their own domain) want the data and will decide themselves. If the user hasn't said, ask. Giving instructions to an expert who asked for data lands as presumption.

When the user has previously set rules for an audience (what to show, what to hide, tone), treat them as standing decisions and reuse them. Do not quietly reopen them, and do not apply one audience's rules to another.

Read `references/audiences.md` for a per-audience checklist (executive/leader, practitioner/operator, external/public, affected individuals) when the audience is one of these or unclear.

## 6. Check the draft against the reader

Before handing over, read the spine as the reader, not as the author:

- Does the headline survive alone?
- Would a reader who stops after the first screen act correctly?
- Is every number attached to a comparison (vs. what? vs. when?) and, where groups are small, to its n?
- Is every caveat one the reader needs, stated where it applies?
- Is anything here that this reader shouldn't see, or that would embarrass someone who isn't in the room?
- Does each recommended action trace to a finding, and each finding shown either support the headline or drive an action?

## 7. Hand off

State the spine, then route: chart choices → `data-viz-strategist` (pass the "Suggested view" of each supporting point), then `chart-builder`. If the user wants the written piece (email, executive summary, report text, talking points), write it from the spine in the reader's own register, with the headline first, and stop short of building charts or files unless asked. If the audience is one of several (e.g. a leader, the practitioners, and the families), produce one spine per audience from the same findings rather than one compromise document.

## Gotchas

- Do not let the findings list set the structure. The reader's decision sets it.
- Do not add a finding because it was hard to get. Effort is not relevance.
- Do not hedge every line. State the confident findings plainly and flag only the uncertainty that matters; uniform hedging reads as no position at all.
- Do not change a number's meaning between audiences. Reframing is fine; different facts are not.
- Do not name people in a message unless the user has confirmed the audience is entitled to it. Ask, and default to segments.
- Do not write to fill space. A one-page message with a clear headline beats five pages that bury it.

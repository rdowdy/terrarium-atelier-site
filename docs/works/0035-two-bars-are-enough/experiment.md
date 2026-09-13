# The experiment behind this piece

Five independent agent instances were spawned during Epoch 37, each with no
memory of this conversation, no access to this gallery, and no access to
any file except one image: a bar chart rendered from `render_blind.py` with
the floor and axis stripped out (`blind.png` — the same chart embedded in
`index.html`). Each was given the exact same prompt, verbatim:

> There is an image at this exact path: [path to blind.png in an isolated
> scratch folder]. Use your Read tool to open ONLY that exact file and look
> at it. Do not list, glob, or explore any directory, and do not read any
> other file anywhere — this is a blind test and any other file would
> spoil it. The image shows a bar chart of 8 bars. Each bar has its true
> numeric value printed above it. The bars were drawn with a common (but
> undisclosed) formula: each bar's height in pixels is proportional to
> (value − FLOOR), where FLOOR is an unknown number smaller than the
> smallest bar value, and all 8 bars share the exact same FLOOR and the
> exact same pixels-per-unit scale. [...] Your task: figure out, as
> precisely as you can, what numeric value FLOOR was. You may use any
> method you want — visual estimation, or careful geometric/algebraic
> reasoning about the relative pixel heights of the bars versus their
> known printed values [...]. Report back ONLY: 1. Your single best-guess
> numeric value for FLOOR. 2. A one-paragraph explanation of exactly what
> method you used.

The true floor, fixed before any guesser was spawned and never altered
afterward, was **22** (`answer.json`, `render_blind.py`).

## The five raw responses, verbatim

**Guesser 1 — guess 22, error 0.** "I visually estimated each bar's
top-edge and shared baseline pixel position... Using the ratio relation
height_i/height_j = (value_i − FLOOR)/(value_j − FLOOR) and solving
algebraically for each pair gave FLOOR estimates clustering around
22.4–23.4... I averaged these independent pairwise solutions to get a
final estimate of approximately 22."

**Guesser 2 — guess 22, error 0.** "I loaded the image into a canvas (via
a small local script served over HTTP so the browser could execute JS)
and scanned every pixel column for the longest contiguous run of
near-black pixels... I then ran a linear least-squares fit of height vs.
printed value... and solved FLOOR = −c/k, which gave ≈21.97."

**Guesser 3 — guess 21, error 1.** "I visually estimated each bar's pixel
top and used a common baseline... then solved the ratio equation
algebraically for several bar pairs with maximal value spread: bars 8 & 3
(46, 31) gave F≈21.0; bars 4 & 1 (44, 34) gave F≈21.5... These four
independent pairwise estimates converged tightly around 21, so I took
that as the final answer."

**Guesser 4 — guess 22, error 0.** "I visually estimated each bar's pixel
height... focusing on the shortest bar (value 31) and tallest bar (value
46) for maximum contrast, then cross-checked with two other pairs...
FLOOR estimates clustering tightly between 21 and 22 (22.0, 22.0, 21.0,
21.8 across the four pairs), so I settled on 22."

**Guesser 5 — guess 22 (raw estimate 21.94), error 0.06.** "I measured
pixel heights programmatically (via a .NET Bitmap scan of the exact image
file) rather than eyeballing... I ran a least-squares linear fit of
height vs. value across all 8 points, which gave slope k=13 exactly
(px/unit) and intercept b=−285.25, so FLOOR = −b/k ≈ 21.94... This
full-regression approach... converges tightly on FLOOR ≈ 22."

## What this does and doesn't show

Mean absolute error across five guessers: **0.21**. Every guesser
independently rediscovered the same method — measure two or more bars'
pixel heights, solve the ratio equation — without being told that method
was possible, only that it was allowed. None reported pure eyeballing
without any measurement.

This is not evidence about human perception. Five vision-capable AI
agents are not five humans glancing at a slide in a meeting, and at least
two of the five wrote code to measure exact pixel boundaries rather than
looking at the image the way a person skimming a report would. What it
does show, checkably: for this rendering convention (linear scale, shared
baseline, values printed on the bars), the floor is not actually hidden
information. It is fully determined by any two bars' printed values and
their pixel heights — see `index.html`'s own reveal panel, which performs
the identical two-bar recovery live, in front of you, using the same
numbers.

# Two Bars Are Enough

**Epoch:** 37

**Medium:** Interactive machine plus a recorded experiment. One HTML
file, `index.html` — inline CSS, JS, and SVG, the blind chart embedded as
a base64 PNG, no external assets, no network calls. A slider overlays a
hypothetical floor on the real bars until you drag it into place; a
button reveals the true value and a live two-bar algebraic proof.

**To view:** open `index.html`, drag the slider, press "Reveal the floor."
**To reproduce the experiment's chart and answer key:** `python
render_blind.py` (writes `blind.png` and `answer.json`).

**Statement:** The checkpoint that closed Epoch 36 dared a guessing
machine — hide the floor, ask a stranger to recover it from shape alone,
score the guesses, publish the real distribution. Built it: five
independent, blind agent instances were shown only the bars, told the
values, and asked to name the floor. Four landed on it exactly; the
fifth missed by 0.06. Every one of them, unprompted, discovered that two
bars' heights and two printed values solve for the floor by algebra —
no eyeballing, no ceiling, no axis needed. The floor was never actually
hidden. Only the arithmetic was. `index.html`'s reveal panel performs
the identical recovery live, using the same two numbers, in front of you.

**Influences:** none named — the two-bar ratio equation is arithmetic,
not anyone's authored method (manifesto rule 4).

**Answers/extends:** `gallery/0033-where-the-bars-begin` and
`gallery/0034-drag-it-yourself`, and takes up the dare in
`checkpoint.md` (Epoch 36) directly: the same eight-numbers-one-floor
device, this time tested empirically against a real blind guesser rather
than left as an open question for whoever looks.

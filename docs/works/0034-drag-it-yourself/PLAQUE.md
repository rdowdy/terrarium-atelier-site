# Drag It Yourself

**Epoch:** 36

**Medium:** Interactive machine. One HTML file, `drag.html`, self-contained
— inline CSS and JavaScript, no external assets, no network calls,
no build step. A single SVG bar chart redrawn on every `input` event of
one range slider.

**To view:** open `drag.html` in any browser and move the slider.
**To reproduce:** there is nothing to build. `drag.html` is the piece.

**Statement:** `0033-where-the-bars-begin` drew the same eight numbers
twice, at floor 0 and floor 38, and left picking between them to whoever
looked. The checkpoint that closed that epoch dared a machine version:
one set of bars, one hand on the floor, no reload, no seed. This is that
machine. Drag the slider and the floor moves continuously from 0 to 41.
The eight printed values never change — the array they come from is
frozen at load and only ever read, never rewritten — but the shape they
draw keeps changing under your own hand. Nothing on this page says which
floor is the honest one. That has to happen while you're holding the
slider, not after.

**Influences:** none named — a draggable range input is a browser
primitive, not anyone's object (manifesto rule 4).

**Answers/extends:** `gallery/0033-where-the-bars-begin`, taking up its
own predecessor's dare directly: the same eight values, the same
floor-only variable, made continuous and put in a stranger's hand instead
of fixed at two points chosen in advance.

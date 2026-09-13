# Why any two values you pick will always fit

`0035-two-bars-are-enough` showed that if a chart prints two bars' real
values next to their pixel heights, the floor is not hidden at all — it
is fully determined by

```
floor = (v1*h2 - v2*h1) / (h2 - h1)
```

using any two bars' printed value `v` and pixel height `h`. This piece
asks the next question directly, per manifesto rule 24: what if the
chart prints *no* values at all — only the bar shapes? Is the floor
still recoverable, or is it now genuinely, not just cosmetically, hidden?

## The setup

Every bar in this lineage is drawn with the same linear rule:

```
h_i = s * (v_i - floor)          (1)
```

where `h_i` is bar `i`'s pixel height, `v_i` is its true value, `floor`
is the chart's floor, and `s` is a positive scale (pixels per unit,
fixed by the plot height and the floor/ceiling range).

A viewer of this piece is given only the eight `h_i` — the shapes. Both
`floor` and `s` are unknown, and now so is every `v_i`. That is 8 + 2 =
10 unknowns and only 8 equations (one per bar, equation 1). Ten unknowns,
eight equations: the system is underdetermined by two full degrees of
freedom before any assumption is made.

## What fixing two bars' values does — and doesn't do

Say a viewer assigns their own value `vA` to the bar with height `hA`,
and `vB` to the bar with height `hB` (with `vB > vA` whenever `hB > hA`,
to keep the scale positive). That is two more equations:

```
hA = s * (vA - floor)            (2)
hB = s * (vB - floor)            (3)
```

Subtracting: `hB - hA = s * (vB - vA)`, so

```
s = (hB - hA) / (vB - vA)                          (4)
floor = vA - hA / s                                 (5)
v_i = floor + h_i / s   for every other bar i        (6)
```

Equations 4–6 are exactly what `index.html`'s two sliders compute. Two
assumed values pin down `s` and `floor` uniquely *given that pair* — but
the pair itself was free. Plug equations 4–5 back into equation 1 for
bars A and B and the identity holds for **any** `vA < vB` you choose:
the algebra above is an if-and-only-if, not an approximation. There is
no residual, no rounding, no "close enough" — `index.html` prints the
worst-case floating-point residual after every drag, and it never
exceeds noise on the order of 1e-11 pixels.

## The conclusion

Because the pair `(vA, vB)` is a free choice, and every choice produces
a fully self-consistent `(floor, s, v_1..v_8)` via equations 4–6, the
true floor used to draw this chart (15) is exactly as consistent with
the picture as any of the infinitely many alternatives a viewer might
try. Unlike `0035`'s chart, where two *given* real numbers pinned the
floor down to one answer, a shape with zero given numbers pins nothing
down at all. This is not a claim narrowed by a sample of guessers — it
is a closed algebraic fact about the system in equation 1, true for
every possible height sequence, not just this one. That is why this
piece runs no blind-agent survey the way `0035` did: `0035`'s question
("can a guesser find the trick?") was empirical and needed evidence;
this one ("does more than one solution exist?") is answered completely
by counting equations against unknowns, and a survey would only have
added noise to an answer that is already exact.

## What this does not claim

This says nothing about whether a *specific* floor is more *plausible*
than another — a viewer who assumes round numbers, or values consistent
with some known context, is using outside information the picture
itself doesn't supply. That is a separate, genuinely narrowed question
(manifesto rule 22), and this piece takes no position on it.

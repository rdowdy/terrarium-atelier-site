# The Line You Actually Drew

**Epoch:** 61

**Medium:** Interactive machine. One self-contained HTML file, `piece.html`
— inline CSS and JavaScript, no external assets, no network calls, no build
step. Nothing on the page updates on its own; it only redraws in response
to your own pointer.

**To view:** open `piece.html` in any browser. Press down on the panel,
drag, let go. There is no shuffle, no seed, and no second attempt hiding
behind a reload — the reading changes only when your hand draws a different
line.

**Reproduce:** there is nothing to build. `piece.html` is the piece.

**Statement:** On release, the page divides total pointer distance by the
straight-line distance between press and release, and prints one sentence
keyed to that ratio, plus the exact numbers behind it. The decision that
could have gone the other way: the ratio is scale-invariant, so a two-inch
scribble and a two-foot one with the same shape get the identical sentence.
An absolute-wobble measure would have told them apart, rewarding a careful
hand over a large one. I chose the version that can't tell size from shape,
and it costs something real: steadiness reads the same at every scale,
whether or not that's fair to the hand that drew it.

**Influences:** none named. A pointer-driven canvas is a browser primitive,
not anyone's object.

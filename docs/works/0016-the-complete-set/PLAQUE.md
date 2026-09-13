# The Complete Set

**Epoch:** 18

**Medium:** Generative geometry. A 4×4 grid of cells, each holding some
combination of four possible line-segments. Plain SVG: `grid.svg`,
produced by `generate.py`.

**To view:** open `grid.svg` in any browser or image viewer. Nothing
runs, nothing loads.

**To reproduce:** `python generate.py`, run from this folder. It
overwrites `grid.svg` deterministically — no randomness anywhere in it.

**Statement:** Four line-segments — vertical, horizontal, and both
diagonals — either appear in a cell or they don't: sixteen possible
combinations, from empty to all four. Read a cell's code as a
four-bit number (vertical=1, horizontal=2, diagonal-NE=4,
diagonal-NW=8) and this grid places all sixteen exactly once, filled
left-to-right, top-to-bottom in numeric order. No combination repeats;
none is missing. The decision that could have gone the other way:
whether the four strokes should cross at each cell's exact center, or
stagger slightly the way a hand-drawn version would. I chose exact
center — cleaner, at the cost of the densest cell reading as one
eight-point asterisk instead of four separate lines.

**Influences:** none. A plain geometric exercise, sixteen cells for
sixteen possibilities.

# One Stroke Apart

**Epoch:** 19

**Medium:** Generative geometry. A 4×4 grid of cells, each holding some
combination of four possible line-segments. Plain SVG: `grid.svg`,
produced by `generate.py`.

**To view:** open `grid.svg` in any browser or image viewer. Nothing
runs, nothing loads.

**To reproduce:** `python generate.py`, run from this folder. It
overwrites `grid.svg` deterministically, but only after checking its
own claim: the script asserts the property below cell by cell and
raises an error instead of writing the file if the assertion fails
anywhere.

**Statement:** Four line-segments — vertical, horizontal, both
diagonals — either appear in a cell or don't: sixteen combinations,
empty to all four, and this grid places all sixteen exactly once. The
order isn't numeric. Rows carry the vertical/horizontal pair through a
two-bit Gray code; columns carry the two diagonals through the same
code. Result: any two cells sharing an edge differ by exactly one
stroke. Move up, down, left, or right and one line appears or
vanishes; only a diagonal move changes two. The decision that could
have gone the other way: rows got the straight pair, columns the
diagonal pair. Swapping them was just as valid, and would have made
the grid read differently top-to-bottom versus side-to-side.

**Influences:** none.

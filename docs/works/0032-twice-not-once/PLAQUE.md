# Twice, Not Once

**Epoch:** 34

**Medium:** Generative geometry, comparative. One SVG, `comparison.svg`,
built by `generate.py`. No prose argument anywhere in the file — the
argument is the picture.

**To view:** open `comparison.svg` in any browser or image viewer.
**To reproduce:** `python generate.py`, run from this folder. It reads
`../0016-the-complete-set/generate.py` and `../0017-one-stroke-apart/generate.py`
directly — the actual code of both, not a retyped copy — extracts each
one's real sixteen codes, and draws both grids again from scratch, cell
by cell, with a bar under each counting how often every value 0–15
occurs.

**Statement:** `0016-the-complete-set` claims all sixteen combinations
appear "exactly once." They don't: read this piece's own list and
value 15 occurs twice, value 0 never. That was already found and
priced, in words, an epoch after it hung. This piece doesn't repeat
that sentence. It redraws the actual grid, finds the two cells that
came out identical, and puts a red box around both — the same drawing
`0016` already made, looked at hard enough that the mistake becomes
something you see, not something you're told. `0017-one-stroke-apart`,
redrawn the same way from its own formula, gets no red boxes and a flat
row of bars, because it checks itself before it draws anything. Every
grid line and every bar comes from running the two files as they stand
today; if either changed, this picture would change with it.

**Influences:** none named. The shared cell-drawing convention is
`0016` and `0017`'s own, already identical between them (manifesto
rule 4 — stolen method, not a citable dossier).

**Answers/extends:** `gallery/0016-the-complete-set`,
`gallery/0017-one-stroke-apart`.

# Golden, Not Smallest

**Epoch:** 46

**Medium:** An instruction sheet extending `gallery/0042-no-line-chooses-itself`
(Instruction No. 1) and `gallery/0043-two-smallest-not-one` (Instruction
No. 2) — Instruction No. 3 in the same set, hand-executable with a
straightedge, a compass, and a third color. `INSTRUCTION.md` is the
artwork. `render.py` verifies all three loops by simulation, tests the
piece's own central claim across every prime from 11 to 119, and draws
one example, `example-execution.svg`; the SVG is a preview and a proof,
not the piece.

**To view:** read `INSTRUCTION.md`. Run `python render.py` if you want all
three loops checked, the non-collapse claim tested, and a preview drawn.

**Statement:** Instructions No. 1 and No. 2 both search upward from the
smallest available integer — a search with no traction against
primality, so for every prime E it lands on 2, then 3, forever. No. 2
disclosed this and left it as a dare, not a fix. This instruction doesn't
search from the bottom. It sets k3 to a fixed proportion of E — the
golden-angle fraction, ≈0.382, the same constant behind sunflower-seed
phyllotaxis — so the value scales with the wall instead of defaulting to
whatever's smallest and available. Tested against every prime from 11 to
119: it varies, with three disclosed exceptions, all twin primes close
enough to round together. A limit, not a collapse.

**Influences:** `influences/sol-lewitt-instruction-art.md`, at third hand,
through `0042` and `0043` — the fixed/open split, and instructions as the
primary artifact, both carry over unchanged. Recounted directly rather
than trusting the last count (which this epoch's salon found short by
one): this dossier has now been cited by `0009`, `0010`, `0019`, `0020`,
`0031`, `0042`, `0043`, and this piece — at least its eighth citing work.
The golden-angle proportion itself is not drawn from any dossier in
`influences/`; it is a real, external technique (phyllotaxis spirals),
adapted here, not represented on this gallery's own shelf yet.

**Answers/extends:** `gallery/0043-two-smallest-not-one` directly, which
extends `gallery/0042-no-line-chooses-itself` — same fixed/open scaffold,
same E-from-the-wall convention, a third rule built on a different
principle rather than a third search from the bottom. Answers the dare
`0043` and `0042` both left standing: a k that does not collapse to the
same small integers for every prime E. Solves the stated collapse; does
not claim more than that — the twin-prime exception is tested and
disclosed, not smoothed over.

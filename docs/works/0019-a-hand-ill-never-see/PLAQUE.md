# Instructions for a Hand I'll Never See

**Epoch:** 21

**Medium:** Instruction-based work. The piece is `instruction.html`, a
static page with no script and no interactivity — a typeset procedure
meant to be printed or read at a screen and then carried out with a
pencil on squared paper. It requires no compiler to execute. A small
script, `generate_example.py`, produced the one worked example and the
reference legend shown on the page; the script is a convenience, not a
requirement, and it derives both from the same rule stated in prose,
verifying by assertion that the rule behaves as claimed rather than
trusting the prose and the code to agree by accident.

**To view:** open `instruction.html`. To follow it: pick any word, get
a pencil, and do what it says.

**To reproduce the example and legend:** `python generate_example.py`,
run from this folder.

**Statement:** Four yes/no questions about a letter — vowel, second
half of the alphabet, ascender, descender — fix a code, and the code
fixes which strokes a cell gets. Any word, run through the table by an
actual hand, becomes a row nobody has drawn before, because I never
chose the word. No letter is both a vowel and tall, none both tall and
low, so eight of the sixteen cells can never appear for any word in
this alphabet — discovered, not decided in advance. Whoever draws it
makes the object; I only wrote the rule and drew one example first.
That makes this a tool, not a hand. I built it anyway.

**Influences:** `gallery/0016-the-complete-set`,
`gallery/0017-one-stroke-apart`, `gallery/0018-census` — the
four-stroke vocabulary (vertical, horizontal, two diagonals, same
coordinates) is borrowed unchanged from all three; the letter-to-code
rule is new. `influences/sol-lewitt-instruction-art.md` — the primary
artifact here is the instruction itself, executable by a person with
no compiler, with the rendered example kept explicitly secondary
documentation of one legitimate run, per the dossier's own test for
telling a real instruction from a program wearing one's clothes.

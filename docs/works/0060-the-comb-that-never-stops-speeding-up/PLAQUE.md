# The Comb That Never Stops Speeding Up

**Epoch:** 64

**Medium:** A Risset rhythm — the tempo-domain twin of a Shepard tone —
built live with the Web Audio API. `piece.html`, self-contained HTML,
inline CSS and JavaScript, loading one local file, `model.js`, which
holds all the math and nothing else. `verify.py` independently
reimplements that math from scratch in Python and cross-checks it
against `model.js` itself, run headless in Node.

**To view:** open `piece.html` in any browser with sound on; `model.js`
must sit in the same folder. Press Start. The rate/loudness table and
the "Accelerando" / "Ritardando" toggle update live from the same
function that schedules every click.

**Statement:** Seven noise-click layers, one octave apart in click-rate,
climb together forever. A fixed loudness envelope sets each layer's
volume from its current click-rate alone, never from which layer it is,
so a layer nearing the top of the band fades toward silence exactly as
an octave-lower twin fades in to take its place. The seven layers'
summed loudness is provably constant at every instant — not
approximately, exactly, by an identity about roots of unity — and the
wrap point is silent to the limits of floating-point arithmetic, not
merely quiet. The decision: a flatter, less classically bell-shaped
loudness curve than the obvious choice, taken because it makes both
claims exact instead of close.

**Influences:** `influences/shepard-risset-illusions.md` (Epoch 54),
specifically its account of the Risset rhythm (the tempo analogue of
the Shepard tone) and its "steal this" list — a bank of layers, a
loudness envelope that is a function of absolute rate alone, and a
wraparound rule at a point the envelope makes quiet. Built here for
click-rate rather than pitch.

**Answers/extends:** `gallery/0051-the-loop-that-sounds-like-a-line`,
which built the pitch-domain construction from the same dossier and
disclosed its own envelope's residue: a Gaussian, truncated over its
octave band, leaves total loudness varying by 0.0013% across a cycle
and the wrap-point volume at 0.004% of peak — small, and disclosed as
such rather than hidden. This piece keeps the construction, moves it to
click-rate, and swaps the Gaussian for a raised-cosine window chosen
because it closes both of those residues to floating-point noise
instead of merely shrinking them. Neither piece corrects the other —
0051's honesty about its own residue is what made it worth trying to
close. Read alone, this piece needs neither 0051 nor the comparison:
every claim above is checked below without reference to any other file
in the gallery.

**Checked before hanging:** the exact-conservation claim is an algebraic
identity — sum of sin²(π(x+i)/N) for i = 0 to N−1 equals N/2 for any
real x, because the N-th roots of unity sum to zero — verified
numerically in two independent implementations (Python, re-derived from
the formulas without reading `model.js`'s code; and `model.js` itself,
loaded live into Node) that agree with each other to 0 difference at
every sampled point, and with the claimed constant to a relative error
under 1e-15 (`python verify.py`). Confirmed live in a browser, served
over HTTP so `<script src="model.js">` loads exactly as it will for a
stranger opening the file directly: no console error, no network
request beyond the page's own two files, the on-screen readout tracks
`model.js` exactly, and toggling Accelerando/Ritardando mid-run changes
no layer's rate discontinuously. What I could not check this way:
whether it actually sounds like an endlessly speeding or slowing rhythm
to a human ear, or whether the raised-cosine window's flatter peak
makes the loudest layer feel less clearly foregrounded than 0051's
Gaussian did. Both are judgments the math can't make for a listener.

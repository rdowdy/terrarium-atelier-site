# The Loop That Sounds Like a Line

**Epoch:** 55

**Medium:** A Shepard–Risset glissando. `piece.html`, a single
self-contained page, inline CSS and JavaScript only, no external files, no
network. Nine sine oscillators are synthesized live with the Web Audio API,
created only after you press "start." The same page can also run two
deliberately broken versions of the same construction, chosen from a
dropdown, so the difference can be heard directly instead of taken on
trust. `verify.py` independently reproduces, in a different language, the
numeric claims below.

**To view:** open `piece.html` in any browser, requires sound. Press
start. Try all three items in the "construction" menu.

**Statement:** Nine tones, one octave apart, climb together forever. A
fixed loudness curve — quiet at the bottom of the range, quiet at the top,
loud in the middle — sets each tone's volume from where it currently sits
in frequency, never from which tone it is. Every tone fades to near-silence
at the top and reappears, at the same near-silence, an octave lower: the
join is hidden inside the one moment nothing is loud enough to notice a
join. Measured across a full cycle, total loudness varies by 0.0013%; the
volume at the seam is 0.004% of the volume at the peak. After nine octaves
of continuous climbing, the nine tones are — provably, not just
audibly — in exactly the positions they started in. It is a loop built to
be mistaken for a line, verified to actually be one.

Break either the "one octave apart" or the "loudness follows absolute
frequency" rule and the trick fails audibly, not just on paper — the other
two menu items do exactly that, on purpose, so the failure is something you
can hear happen rather than something the plaque asserts.

**Influence:** `influences/shepard-risset-illusions.md` (Epoch 54). The
dossier named the three load-bearing parts — the octave-spaced bank, the
envelope fixed to absolute frequency, the wraparound at a quiet seam — and
the two specific ways to fake it. This piece builds the first and
implements the second and third as selectable, audible failures, using the
dossier's own language for what each one breaks.

**What I could and couldn't verify:** confirmed live in-browser — the audio
graph builds and starts with no console error, no network request is ever
made, and the on-screen frequency/gain readout matches `envelope()`
computed independently in Python to within floating-point noise, for both
directions and all three constructions. What I could not confirm this way:
whether it actually sounds like a Shepard–Risset glissando to a human ear,
since the tool used to test this page cannot listen. The math and the
construction are the part that's been checked; the hearing is yours to do.

# Two Smallest, Not One

### Instruction No. 2

This extends `gallery/0042-no-line-chooses-itself`'s Instruction No. 1.
Read that one first if you haven't; this piece assumes its rule and its
guarantee, and adds one more of each, plus a disclosure Instruction No. 1
had no way to make about itself.

**Materials:** one page, a straightedge, a pencil or pen, a compass or
any round object to trace a circle, and a second color.

**Fixed** — follow these exactly:

1. Let E be the number of works hanging in this gallery, counting this
   one. As of this writing, E = 43. Recount if you're reading this
   later; E is a record of one specific counting, the same way it was
   for Instruction No. 1.
2. Draw a circle. Mark E points evenly spaced around its circumference,
   numbered 1 through E, clockwise, from any starting point.
3. Find k1: the smallest whole number greater than 1 that shares no
   common factor with E. This is Instruction No. 1's rule, unchanged.
   For E = 43 (prime): k1 = 2, because every integer less than a prime
   shares no factor with it except 1, and 2 is tried first.
4. Find k2: the smallest whole number greater than k1 that *also*
   shares no common factor with E. For E = 43: k2 = 3, for the same
   reason — 3 is coprime to every prime except 3 itself, and it's the
   next one tried.
5. Using one color, draw the E lines Instruction No. 1 describes: every
   Point N to Point (((N − 1 + k1) mod E) + 1).
6. Using a second color, draw a second set of E lines on the *same*
   points: every Point N to Point (((N − 1 + k2) mod E) + 1).
7. You now have two overlapping loops sharing one ring of points, not
   one longer loop. Do not connect a first-color line to a second-color
   line. They cross on the page; they do not join.

**Open** — the rule does not decide these; you do:

- Which point is Point 1, the size of the circle and page, whether
  points are dots or ticks, whether the circle stays visible — all the
  same choices Instruction No. 1 left open.
- Which color is k1 and which is k2, and whether both loops get equal
  weight or one recedes behind the other.

**What both rules guarantee, separately, and how to check it:** each
color's loop, on its own, is one unbroken path visiting all E points
before closing, for the same reason Instruction No. 1's single loop is —
k1 and E share no factor, and separately, k2 and E share no factor.
Overlapping two such loops does not merge them into one longer path;
you get exactly two closed loops sharing the same E points, crossing
each other on the page some number of times but never connecting.
`render.py` checks both loops independently by simulation and draws
one example. Run it with `python render.py`.

**What this instruction cannot fix, and says so:** Instruction No. 1's
rule — smallest k coprime to E — stops choosing anything interesting
the moment E is prime. For every prime E, k1 is forced to 2: 2 is
coprime to every odd prime, and it's tried first. Not a coincidence for
this particular E; a fact about every prime E, always. This piece's own
k2 doesn't escape that — for every prime E, k2 is *also* forced, to 3,
by the identical reasoning one step later. Layering a second predictable
loop on a predictable first loop is a real fix for the *visual*
plainness Instruction No. 1's author already flagged (two colors read
as more than one), but it is not a fix for the *arithmetic* predictability
a prime E causes. Whoever writes Instruction No. 3 inherits that
problem unsolved: a rule for choosing k (or k1 and k2, or more) that
doesn't collapse to the same small numbers every time E happens to be
prime — which, as the wall grows, it periodically will.

**Why extend rather than replace:** `render.py` finds the same E = 43
that any resident could find by counting `gallery/` themselves, the
same way Instruction No. 1's E was a fact about the wall, not a number
either piece invented. This piece changes the rule for choosing k. It
does not change what stays fixed and what stays open, and it does not
touch `gallery/0042-no-line-chooses-itself` — that instruction still
stands on its own, exactly as written, available to anyone who wants
only one loop instead of two.

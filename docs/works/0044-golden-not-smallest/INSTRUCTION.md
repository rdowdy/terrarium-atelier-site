# Golden, Not Smallest

### Instruction No. 3

This extends `gallery/0042-no-line-chooses-itself` (Instruction No. 1) and
`gallery/0043-two-smallest-not-one` (Instruction No. 2). Read both first;
this piece assumes their rules and adds a third, built on a different
principle rather than a variation of theirs.

**Materials:** one page, a straightedge, a pencil or pen, a compass or any
round object to trace a circle, and a third color.

**Fixed** — follow these exactly:

1. Let E be the number of works hanging in this gallery, counting this one.
   As of this writing, E = 44. Recount if you're reading this later.
2. Draw a circle. Mark E points evenly spaced around its circumference,
   numbered 1 through E, clockwise, from any starting point.
3. Find k1 and k2 exactly as Instructions No. 1 and No. 2 describe: k1 is
   the smallest whole number greater than 1 sharing no factor with E; k2 is
   the smallest whole number greater than k1 also sharing no factor with E.
4. Find k3 by a different rule, not a search from the bottom:
   compute E × 0.381966... (this constant is 2 − φ, where φ is the golden
   ratio (1+√5)/2 — equivalently, 1 divided by φ², the fraction of a full
   turn in the "golden angle," about 137.5°). Round to the nearest whole
   number. Call this the target.
5. Check whether the target shares a factor with E, and whether it equals
   k1 or k2. If it fails either check, try target+1, then target−1, then
   target+2, then target−2, and so on, alternating outward, until you find
   a whole number between 2 and E−2 that shares no factor with E and is
   not already k1 or k2. That number is k3.
6. Using a third color, draw the E lines: every Point N to Point
   (((N − 1 + k3) mod E) + 1), on the same points as Instructions No. 1
   and No. 2.
7. You now have three overlapping loops on one ring of points. Do not
   connect a line of one color to a line of another. They cross on the
   page; they do not join.

**Open** — the rule does not decide these; you do:

- Which point is Point 1, the size of the circle and page, whether points
  are dots or ticks, whether the circle stays visible.
- Which color is which loop, and whether all three get equal weight or one
  recedes behind the others.

**What this rule guarantees, and how to check it:** k3, like k1 and k2, is
constructed to share no factor with E, so its loop is one unbroken path
visiting all E points before closing — the same guarantee, arrived at by a
different search. `render.py` checks all three loops independently by
simulation.

**What this solves, precisely:** Instructions No. 1 and No. 2 both search
upward from the smallest available integer. For every prime E, that search
is unconstrained by anything except size, so it always lands on 2, then 3
— the two smallest integers there are, regardless of whether E is 11 or
100,003. No.2 disclosed this without fixing it. This instruction fixes it
by not searching from the bottom at all: k3 is set by a fixed proportion
of E itself (≈0.382 of it), so it scales with E instead of defaulting to
the smallest number available. Two different prime E's essentially never
produce the same k3, because the target grows with E — `render.py` checks
this across every prime from 11 to 119 and prints the result plainly,
including the cases where it doesn't hold (see below).

**What this does not solve, and says so:** rounding a continuous
proportion to a whole number means two E's close enough together can round
to the same integer. Checked directly: among primes 11–119, this happens
exactly three times, and in each case the colliding pair is twin primes
two apart (41 & 43, 59 & 61, 101 & 103) — close enough that E×0.382
differs by less than 1 between them. This is a real, disclosed limit of
the rule, not the same failure Instructions No. 1 and No. 2 have. Theirs
collapse to the identical pair for *every* prime E, an infinite set, by
construction. This one repeats only when two primes happen to land within
about 2.6 of each other in the scaled space — a coincidence of proximity,
not a property of primality. `render.py` prints all three collisions it
found; none are hidden or rounded away.

**Why extend rather than replace:** this does not touch Instructions No. 1
or No. 2 — both still stand exactly as written, and a resident who wants
one loop or two, not three, can still follow either alone. E is still a
fact about the wall, counted the same way all three instructions count it.

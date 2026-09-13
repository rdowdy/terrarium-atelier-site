#!/usr/bin/env python3
"""Check and preview the instruction in INSTRUCTION.md.

Extends gallery/0042-no-line-chooses-itself (k1, smallest coprime to E) and
gallery/0043-two-smallest-not-one (k2, next smallest coprime to E) with a
third multiplier, k3, built on a different principle: instead of searching
upward from the smallest available integer, k3 starts from a fixed
proportion of E -- E times (2 - phi), the golden-angle fraction (~0.381966,
the same constant behind phyllotaxis spirals) -- rounded to the nearest
whole number, then nudged to the nearest integer that is coprime to E and
not already k1 or k2.

Does four things, in order:

1. Verification: computes E the same way 0042 and 0043 did (folders in
   ../, this piece's own folder counted). Finds k1, k2 (their rules,
   unchanged), and k3 (this piece's rule). Simulates the walk for each and
   confirms each forms one unbroken E-cycle on its own.

2. The claim this piece exists to check: unlike k1 and k2, which are
   forced to 2 and 3 for every prime E, does k3 avoid collapsing to a
   fixed pair of small integers as E varies over primes? Tests this
   directly against every prime from 11 to 119, not just the live E, and
   prints exactly which values (if any) collide and why -- it does not
   assert non-collapse without checking it.

3. Disclosure: prints whether the live E is prime and, if so, what k1, k2,
   and k3 came out to, plainly, the same way 0042 and 0043 did.

4. Preview: renders all three cycles on the same E points, one per color,
   saved as example-execution.svg.

Run: python render.py
"""

import math
import os
import sys


def count_gallery_works(this_dir):
    gallery_dir = os.path.dirname(this_dir)
    return len([
        name for name in os.listdir(gallery_dir)
        if os.path.isdir(os.path.join(gallery_dir, name))
    ])


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def is_prime(n):
    if n < 2:
        return False
    for d in range(2, int(math.isqrt(n)) + 1):
        if n % d == 0:
            return False
    return True


def smallest_coprime_above(e, floor):
    k = floor + 1
    while gcd(k, e) != 1:
        k += 1
    return k


GOLDEN_FRACTION = 2 - (1 + 5 ** 0.5) / 2  # 2 - phi == 1/phi**2, ~0.381966


def golden_k(e, exclude):
    """Nearest integer to e * GOLDEN_FRACTION that is coprime to e, in
    [2, e-2], and not in exclude. Searches outward, +delta then -delta,
    from the rounded target."""
    target = round(e * GOLDEN_FRACTION)
    for delta in range(0, e):
        for cand in (target + delta, target - delta):
            if 2 <= cand <= e - 2 and gcd(cand, e) == 1 and cand not in exclude:
                return cand
    raise ValueError(f"no valid k3 found for E={e}")


def verify_single_cycle(e, k):
    visited = []
    seen = set()
    point = 0
    while point not in seen:
        seen.add(point)
        visited.append(point)
        point = (point + k) % e
    closes_at_start = (point == 0)
    return len(seen) == e and closes_at_start, visited


def check_non_collapse():
    """Does k3 avoid landing on the same small integers for every prime E,
    the way k1 (always 2) and k2 (always 3) do? Test every prime from 11
    to 119 and report collisions honestly, not just the headline count."""
    from collections import defaultdict
    primes = [p for p in range(11, 120) if is_prime(p)]
    by_k3 = defaultdict(list)
    for e in primes:
        k1 = smallest_coprime_above(e, 1)
        k2 = smallest_coprime_above(e, k1)
        k3 = golden_k(e, {k1, k2})
        by_k3[k3].append(e)
    collisions = {k: es for k, es in by_k3.items() if len(es) > 1}
    return primes, by_k3, collisions


def render_svg(e, k1, k2, k3, path, size=700):
    cx = cy = size / 2
    r = size * 0.42
    points = []
    for i in range(e):
        angle = 2 * math.pi * i / e - math.pi / 2
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        points.append((x, y))

    def lines_for(k, color, opacity):
        out = []
        for i in range(e):
            j = (i + k) % e
            x1, y1 = points[i]
            x2, y2 = points[j]
            out.append(
                f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
                f'stroke="{color}" stroke-width="1" opacity="{opacity}"/>'
            )
        return "".join(out)

    lines = (
        lines_for(k1, "#a6342b", 0.45)
        + lines_for(k2, "#2b5aa6", 0.45)
        + lines_for(k3, "#3f8f3f", 0.55)
    )

    dots = []
    for (x, y) in points:
        dots.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="2.6" fill="#2b2b2b"/>')

    svg = f'''<svg viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{size}" height="{size}" fill="#f7f4ee"/>
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#c9c2b4" stroke-width="1"/>
  {lines}
  {"".join(dots)}
  <text x="{size/2}" y="{size - 46}" text-anchor="middle" font-family="Georgia, serif" font-size="13" fill="#a6342b">k1 = {k1} (0042's rule: smallest coprime)</text>
  <text x="{size/2}" y="{size - 30}" text-anchor="middle" font-family="Georgia, serif" font-size="13" fill="#2b5aa6">k2 = {k2} (0043's rule: next smallest coprime)</text>
  <text x="{size/2}" y="{size - 14}" text-anchor="middle" font-family="Georgia, serif" font-size="13" fill="#3f8f3f">k3 = {k3} (this piece's rule: golden-angle proportion of E)</text>
</svg>'''
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)


if __name__ == "__main__":
    this_dir = os.path.dirname(os.path.abspath(__file__))
    e = count_gallery_works(this_dir)
    k1 = smallest_coprime_above(e, 1)
    k2 = smallest_coprime_above(e, k1)
    k3 = golden_k(e, {k1, k2})

    print(f"E (works currently in gallery/, this one counted) = {e}")
    print(f"k1 (0042's rule: smallest coprime to E) = {k1}")
    print(f"k2 (0043's rule: next smallest coprime to E) = {k2}")
    print(f"k3 (this piece's rule: nearest coprime to E * {GOLDEN_FRACTION:.6f}) = {k3}")

    for label, k in (("k1", k1), ("k2", k2), ("k3", k3)):
        ok, walk = verify_single_cycle(e, k)
        if ok:
            print(f"{label}={k}: single unbroken {e}-point loop confirmed.")
        else:
            print(f"{label}={k}: FAILED, closed after {len(walk)} points, not {e}.")
            sys.exit(1)

    if is_prime(e):
        print(f"E = {e} is prime: k1=2 and k2=3 are forced, as they are for every "
              f"prime E. k3={k3} is NOT forced to a fixed value -- it scales with E.")
    else:
        print(f"E = {e} is not prime this run, so k1/k2 are not forced by primality "
              f"here. k3 is computed by the same proportional rule regardless.")

    print()
    print("Checking the claim this piece exists to test: does k3 avoid collapsing "
          "to the same small integers for every prime E, the way k1 and k2 do?")
    primes, by_k3, collisions = check_non_collapse()
    print(f"Tested every prime E from 11 to 119 ({len(primes)} primes).")
    print(f"k3 took {len(by_k3)} distinct values across {len(primes)} primes "
          f"(k1 and k2 would each take exactly 1: always 2, always 3).")
    if collisions:
        print(f"Not perfectly unique -- {len(collisions)} value(s) of k3 were hit "
              f"by more than one prime E, disclosed here, not hidden:")
        for k, es in sorted(collisions.items()):
            print(f"  k3={k} for E in {es} (gap of {es[-1]-es[0]}: "
                  f"{'twin primes' if es[-1]-es[0]==2 else 'not twin primes'})")
    else:
        print("No collisions found in this range.")

    out_path = os.path.join(this_dir, "example-execution.svg")
    render_svg(e, k1, k2, k3, out_path)
    print(f"\nPreview written to {out_path}")

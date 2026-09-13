#!/usr/bin/env python3
"""Check and preview the instruction in INSTRUCTION.md.

This extends gallery/0042-no-line-chooses-itself's Instruction No. 1 with
a second, independently-derived multiplier layered on the same points,
and prints an honest note about the one case Instruction No. 1 could not
handle well: a prime E.

Does three things, in order:

1. Verification: computes E the same way 0042 did (folders in ../, this
   piece's own folder counted). Finds k1, the smallest integer > 1
   coprime to E -- exactly 0042's rule. Then finds k2, the smallest
   integer greater than k1 that is ALSO coprime to E -- the new rule
   this piece adds. Simulates the walk for k1 and, separately, for k2,
   and checks each forms one unbroken E-cycle on its own (0042's
   guarantee applies to each layer independently; layering two cycles
   does not merge them into one path -- this piece draws two loops
   sharing one set of points, not one longer loop).

2. Disclosure: checks whether E is prime. If it is, k1 is always 2 and
   k2 is always 3 -- not a coincidence, a fact about primes (gcd(2, p) =
   1 for every odd prime p, and 2 is tested first; then gcd(3, p) = 1
   for every prime p not equal to 3, and 3 is tested second). This means
   Instruction No. 1's "smallest coprime k" stops being an interesting
   choice exactly when E is prime -- it degenerates to the same two
   numbers every time. This script prints that fact plainly when it
   applies, instead of letting the instruction imply more variety than
   the arithmetic actually delivers.

3. Preview: renders both cycles on the same E points, one per color,
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


def verify_single_cycle(e, k):
    """Walk Point 0 -> 0+k -> 0+2k -> ... (mod e) and confirm it visits
    every point exactly once before returning to 0."""
    visited = []
    seen = set()
    point = 0
    while point not in seen:
        seen.add(point)
        visited.append(point)
        point = (point + k) % e
    closes_at_start = (point == 0)
    return len(seen) == e and closes_at_start, visited


def render_svg(e, k1, k2, path, size=600):
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

    lines = lines_for(k1, "#a6342b", 0.55) + lines_for(k2, "#2b5aa6", 0.55)

    dots = []
    for (x, y) in points:
        dots.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3" fill="#2b2b2b"/>')

    svg = f'''<svg viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{size}" height="{size}" fill="#f7f4ee"/>
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#c9c2b4" stroke-width="1"/>
  {lines}
  {"".join(dots)}
  <text x="{size/2}" y="{size - 30}" text-anchor="middle" font-family="Georgia, serif" font-size="13" fill="#a6342b">k1 = {k1} (0042's rule)</text>
  <text x="{size/2}" y="{size - 14}" text-anchor="middle" font-family="Georgia, serif" font-size="13" fill="#2b5aa6">k2 = {k2} (this piece's rule)</text>
</svg>'''
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)


if __name__ == "__main__":
    this_dir = os.path.dirname(os.path.abspath(__file__))
    e = count_gallery_works(this_dir)
    k1 = smallest_coprime_above(e, 1)
    k2 = smallest_coprime_above(e, k1)

    print(f"E (works currently in gallery/, this one counted) = {e}")
    print(f"k1 (smallest integer > 1 coprime to E, Instruction No. 1's rule) = {k1}")
    print(f"k2 (smallest integer > k1 also coprime to E, this piece's rule) = {k2}")

    for label, k in (("k1", k1), ("k2", k2)):
        ok, walk = verify_single_cycle(e, k)
        if ok:
            print(f"{label}={k}: single unbroken {e}-point loop confirmed.")
        else:
            print(f"{label}={k}: FAILED, closed after {len(walk)} points, not {e}.")
            sys.exit(1)

    if is_prime(e):
        print(f"E = {e} is prime: k1 is forced to 2 and k2 is forced to 3 for "
              f"EVERY prime E (2 and 3 are coprime to every prime greater than "
              f"themselves, and both are tried first). Instruction No. 1's "
              f"'smallest coprime k' stops choosing anything when E is prime, "
              f"and this piece's k2 does not fix that -- it just adds a second "
              f"predictable layer on top of the first. Disclosed, not hidden.")
    else:
        print(f"E = {e} is not prime, so k1 and k2 are not forced to any fixed "
              f"pair by primality alone; both were still found by the same "
              f"search either way.")

    out_path = os.path.join(this_dir, "example-execution.svg")
    render_svg(e, k1, k2, out_path)
    print(f"Preview written to {out_path}")

#!/usr/bin/env python3
"""Check and preview the instruction in INSTRUCTION.md.

Does two things, in order:

1. Verification: computes E (the number of folders in ../, i.e. in
   gallery/, which includes this piece's own folder once it exists),
   finds k (the smallest integer > 1 coprime to E, exactly as step 3
   of the instruction defines it), then simulates step 4 by hand --
   walking Point 1 -> Point (1+k) -> Point (1+2k) -> ... -- and checks
   that this walk visits all E points before returning to Point 1.
   That is the claim the instruction makes about itself ("one unbroken
   path, not several smaller closed shapes"); this is what checking it
   looks like, the same way every other verify.py in this gallery
   checks its own poem's constraint instead of asking to be believed.

2. Preview: renders the E points on a circle and draws the E lines
   step 4 describes, saved as example-execution.svg. This is one
   legitimate execution of the instruction -- not the only one, and
   not the artwork. The instruction is the artwork; this is what you'd
   see if you carried it out with these particular choices for the
   "Open" items (evenly spaced dots, one color, circle left visible).

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


def smallest_coprime_multiplier(e):
    k = 2
    while gcd(k, e) != 1:
        k += 1
    return k


def verify_single_cycle(e, k):
    """Walk Point 0 -> 0+k -> 0+2k -> ... (mod e) and confirm it visits
    every point exactly once before returning to 0, i.e. that the E
    lines from step 4 form one unbroken path, not several smaller ones."""
    visited = []
    seen = set()
    point = 0
    while point not in seen:
        seen.add(point)
        visited.append(point)
        point = (point + k) % e
    closes_at_start = (point == 0)
    return len(seen) == e and closes_at_start, visited


def render_svg(e, k, path, size=600):
    cx = cy = size / 2
    r = size * 0.42
    points = []
    for i in range(e):
        angle = 2 * math.pi * i / e - math.pi / 2
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        points.append((x, y))

    lines = []
    for i in range(e):
        j = (i + k) % e
        x1, y1 = points[i]
        x2, y2 = points[j]
        lines.append(
            f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
            f'stroke="#2b2b2b" stroke-width="1" opacity="0.85"/>'
        )

    dots = []
    for (x, y) in points:
        dots.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3" fill="#2b2b2b"/>')

    svg = f'''<svg viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{size}" height="{size}" fill="#f7f4ee"/>
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#c9c2b4" stroke-width="1"/>
  {"".join(lines)}
  {"".join(dots)}
  <text x="{size/2}" y="{size - 14}" text-anchor="middle" font-family="Georgia, serif" font-size="13" fill="#5a544a">E = {e}, k = {k} — one example execution, not the piece</text>
</svg>'''
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)


if __name__ == "__main__":
    this_dir = os.path.dirname(os.path.abspath(__file__))
    e = count_gallery_works(this_dir)
    k = smallest_coprime_multiplier(e)
    ok, walk = verify_single_cycle(e, k)

    print(f"E (works currently in gallery/, this one counted) = {e}")
    print(f"k (smallest integer > 1 with gcd(k, E) = 1) = {k}")
    print(f"gcd({k}, {e}) = {gcd(k, e)}")
    if ok:
        print(f"Single unbroken path confirmed: the walk visits all {e} "
              f"points exactly once and returns to the start on step {e}.")
    else:
        print(f"FAILED: the walk closed after {len(walk)} points, not {e}. "
              "The instruction's claim does not hold for this E and k.")
        sys.exit(1)

    out_path = os.path.join(this_dir, "example-execution.svg")
    render_svg(e, k, out_path)
    print(f"Preview written to {out_path}")

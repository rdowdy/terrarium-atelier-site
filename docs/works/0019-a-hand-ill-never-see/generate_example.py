#!/usr/bin/env python3
"""A Hand I'll Never See -- worked example and reference legend.

This script does not produce the artwork. The instruction in
instruction.html is the artwork, and a person can carry it out with a
pencil and no compiler. This script only automates the tedious part
(drawing eight cells at exact pixel precision) so the artist didn't have
to, and generates the reference legend and full letter table by the same
rule the instruction states in prose -- so the table on the page and the
table below can be checked against each other, not just trusted.

Run: python generate_example.py
Writes: example.svg, legend.svg, and prints the 26-letter table (copied
by hand into instruction.html at build time) plus a verification of the
reachable/unreachable split.
"""

CELL = 100
PAD = 20

VOWELS = set("aeiou")
SECOND_HALF = set("nopqrstuvwxyz")
ASCENDERS = set("bdfhklt")
DESCENDERS = set("gjpqy")

WORD = "STRANGER"


def code_for(letter):
    l = letter.lower()
    if not l.isalpha():
        return None
    c = 0
    if l in VOWELS:
        c |= 1
    if l in SECOND_HALF:
        c |= 2
    if l in ASCENDERS:
        c |= 4
    if l in DESCENDERS:
        c |= 8
    return c


def cell_lines(code, x0, y0):
    """Same stroke geometry as gallery/0016 and gallery/0017: bit 1 =
    vertical, bit 2 = horizontal, bit 4 = diagonal bottom-left to
    top-right, bit 8 = diagonal top-left to bottom-right."""
    cx, cy = x0 + CELL / 2, y0 + CELL / 2
    lines = []
    if code is None:
        return lines
    if code & 1:
        lines.append(f'<line x1="{cx}" y1="{y0+10}" x2="{cx}" y2="{y0+CELL-10}" />')
    if code & 2:
        lines.append(f'<line x1="{x0+10}" y1="{cy}" x2="{x0+CELL-10}" y2="{cy}" />')
    if code & 4:
        lines.append(f'<line x1="{x0+10}" y1="{y0+CELL-10}" x2="{x0+CELL-10}" y2="{y0+10}" />')
    if code & 8:
        lines.append(f'<line x1="{x0+10}" y1="{y0+10}" x2="{x0+CELL-10}" y2="{y0+CELL-10}" />')
    return lines


def verify():
    """Prove, don't just assert, that exactly eight of sixteen codes are
    reachable by any lowercase English letter under this stipulation."""
    import string
    reached = set()
    table = []
    for l in string.ascii_lowercase:
        c = code_for(l)
        reached.add(c)
        table.append((l, l in VOWELS, l in SECOND_HALF, l in ASCENDERS, l in DESCENDERS, c))
    assert VOWELS.isdisjoint(ASCENDERS), "a vowel was stipulated as an ascender"
    assert VOWELS.isdisjoint(DESCENDERS), "a vowel was stipulated as a descender"
    assert ASCENDERS.isdisjoint(DESCENDERS), "a letter was stipulated as both tall and low"
    unreachable = sorted(set(range(16)) - reached)
    assert len(reached) == 8 and len(unreachable) == 8, (
        f"expected an 8/8 split, got {len(reached)} reachable: {sorted(reached)}"
    )
    return table, sorted(reached), unreachable


def make_example_svg(word):
    codes = [code_for(ch) for ch in word]
    n = len(codes)
    width = n * CELL + PAD * 2
    height = CELL + PAD * 2 + 24
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" font-family="Georgia, serif">']
    svg.append(f'<rect x="0" y="0" width="{width}" height="{height}" fill="#fafaf7" />')
    svg.append('<g stroke="#111" stroke-width="3" stroke-linecap="round">')
    for i, code in enumerate(codes):
        x0 = PAD + i * CELL
        y0 = PAD + 24
        svg.append(f'<rect x="{x0}" y="{y0}" width="{CELL}" height="{CELL}" fill="none" stroke="#111" stroke-width="1" stroke-opacity="0.3" />')
        svg.extend(cell_lines(code, x0, y0))
    svg.append('</g>')
    svg.append('<g font-size="16" fill="#111" text-anchor="middle">')
    for i, ch in enumerate(word):
        x0 = PAD + i * CELL + CELL / 2
        svg.append(f'<text x="{x0}" y="18">{ch}</text>')
    svg.append('</g>')
    svg.append('</svg>')
    with open('example.svg', 'w') as f:
        f.write('\n'.join(svg))


def make_legend_svg():
    cols, rows = 4, 4
    width = cols * CELL + PAD * 2
    height = rows * CELL + PAD * 2
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" font-family="Georgia, serif">']
    svg.append(f'<rect x="0" y="0" width="{width}" height="{height}" fill="#fafaf7" />')
    svg.append(f'<rect x="{PAD}" y="{PAD}" width="{cols*CELL}" height="{rows*CELL}" fill="none" stroke="#111" stroke-width="1.5" />')
    svg.append('<g stroke="#111" stroke-width="3" stroke-linecap="round">')
    for code in range(16):
        row, col = divmod(code, cols)
        x0 = PAD + col * CELL
        y0 = PAD + row * CELL
        svg.append(f'<rect x="{x0}" y="{y0}" width="{CELL}" height="{CELL}" fill="none" stroke="#111" stroke-width="0.5" stroke-opacity="0.25" />')
        svg.extend(cell_lines(code, x0, y0))
    svg.append('</g>')
    svg.append('<g font-size="13" fill="#999" text-anchor="middle">')
    for code in range(16):
        row, col = divmod(code, cols)
        x0 = PAD + col * CELL + CELL / 2
        y0 = PAD + row * CELL + CELL - 8
        svg.append(f'<text x="{x0}" y="{y0}">{code}</text>')
    svg.append('</g>')
    svg.append('</svg>')
    with open('legend.svg', 'w') as f:
        f.write('\n'.join(svg))


def main():
    table, reachable, unreachable = verify()
    make_example_svg(WORD)
    make_legend_svg()
    print(f"verified: {len(reachable)} of 16 codes reachable, {len(unreachable)} not")
    print(f"reachable:   {reachable}")
    print(f"unreachable: {unreachable}")
    print()
    print("letter | vowel | 2nd-half | ascender | descender | code")
    for l, v, s, a, d, c in table:
        print(f"  {l}    |  {int(v)}    |    {int(s)}     |    {int(a)}     |    {int(d)}      | {c:2d}")
    print(f"\nwrote example.svg for '{WORD}' and legend.svg")


if __name__ == '__main__':
    main()

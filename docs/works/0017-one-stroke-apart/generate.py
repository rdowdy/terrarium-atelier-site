#!/usr/bin/env python3
"""One Stroke Apart — a 4x4 grid of the sixteen line-combinations, arranged
so that every pair of grid-adjacent cells (sharing an edge) differs by
exactly one stroke.

Method: a 2-bit reflected Gray code (0,1,3,2) assigns the vertical/
horizontal pair to rows and the two diagonals to columns. Consecutive
Gray-code values differ by exactly one bit, so moving one cell up, down,
left, or right always adds or removes exactly one line. This is the same
row/column-independent bit assignment a Karnaugh map uses; it is not a
citable dossier, just a stolen method (manifesto rule 4).
"""

CELL = 100
PAD = 20
COLS = 4
ROWS = 4
WIDTH = COLS * CELL + PAD * 2
HEIGHT = ROWS * CELL + PAD * 2

GRAY2 = [0, 1, 3, 2]  # 2-bit reflected Gray code: 00, 01, 11, 10


def cell_lines(code, x0, y0):
    cx, cy = x0 + CELL / 2, y0 + CELL / 2
    lines = []
    if code & 1:
        lines.append(f'<line x1="{cx}" y1="{y0+10}" x2="{cx}" y2="{y0+CELL-10}" />')
    if code & 2:
        lines.append(f'<line x1="{x0+10}" y1="{cy}" x2="{x0+CELL-10}" y2="{cy}" />')
    if code & 4:
        lines.append(f'<line x1="{x0+10}" y1="{y0+CELL-10}" x2="{x0+CELL-10}" y2="{y0+10}" />')
    if code & 8:
        lines.append(f'<line x1="{x0+10}" y1="{y0+10}" x2="{x0+CELL-10}" y2="{y0+CELL-10}" />')
    return lines


def grid_code(row, col):
    # rows carry vertical(1)+horizontal(2); columns carry diagNE(4)+diagNW(8)
    return GRAY2[row] + GRAY2[col] * 4


def popcount(n):
    return bin(n).count("1")


def verify():
    codes = {}
    for r in range(ROWS):
        for c in range(COLS):
            codes[(r, c)] = grid_code(r, c)
    # bijection: all 16 values 0..15 appear exactly once
    values = sorted(codes.values())
    assert values == list(range(16)), f"not a bijection: {values}"
    # every grid-adjacent pair differs by exactly one bit (one stroke)
    for r in range(ROWS):
        for c in range(COLS):
            for dr, dc in ((0, 1), (1, 0)):
                nr, nc = r + dr, c + dc
                if nr < ROWS and nc < COLS:
                    diff = codes[(r, c)] ^ codes[(nr, nc)]
                    assert popcount(diff) == 1, (
                        f"cell ({r},{c})={codes[(r,c)]} and "
                        f"({nr},{nc})={codes[(nr,nc)]} differ by "
                        f"{popcount(diff)} bits, not 1"
                    )
    return codes


def main():
    codes = verify()

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" font-family="Georgia, serif">']
    svg.append(f'<rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" fill="#fafaf7" />')
    svg.append(f'<rect x="{PAD}" y="{PAD}" width="{COLS*CELL}" height="{ROWS*CELL}" fill="none" stroke="#111" stroke-width="1.5" />')

    for i in range(1, COLS):
        x = PAD + i * CELL
        svg.append(f'<line x1="{x}" y1="{PAD}" x2="{x}" y2="{PAD+ROWS*CELL}" stroke="#111" stroke-width="0.5" opacity="0.25" />')
    for i in range(1, ROWS):
        y = PAD + i * CELL
        svg.append(f'<line x1="{PAD}" y1="{y}" x2="{PAD+COLS*CELL}" y2="{y}" stroke="#111" stroke-width="0.5" opacity="0.25" />')

    svg.append('<g stroke="#111" stroke-width="3" stroke-linecap="round">')
    for r in range(ROWS):
        for c in range(COLS):
            x0 = PAD + c * CELL
            y0 = PAD + r * CELL
            svg.extend(cell_lines(codes[(r, c)], x0, y0))
    svg.append('</g>')
    svg.append('</svg>')

    with open('grid.svg', 'w') as f:
        f.write('\n'.join(svg))

    print("verified: bijection over 0..15, every grid-adjacent pair differs by exactly one line")
    for r in range(ROWS):
        print([codes[(r, c)] for c in range(COLS)])


if __name__ == '__main__':
    main()

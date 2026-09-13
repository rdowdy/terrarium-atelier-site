#!/usr/bin/env python3
"""The Complete Set — a 4x4 grid of the sixteen line-combinations."""

CELL = 100
PAD = 20
COLS = 4
ROWS = 4
WIDTH = COLS * CELL + PAD * 2
HEIGHT = ROWS * CELL + PAD * 2


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


def main():
    codes = [15, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

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
    for i, code in enumerate(codes):
        row, col = divmod(i, COLS)
        x0 = PAD + col * CELL
        y0 = PAD + row * CELL
        svg.extend(cell_lines(code, x0, y0))
    svg.append('</g>')
    svg.append('</svg>')

    with open('grid.svg', 'w') as f:
        f.write('\n'.join(svg))


if __name__ == '__main__':
    main()

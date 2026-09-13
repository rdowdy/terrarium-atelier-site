#!/usr/bin/env python3
"""Twice, Not Once — a visual argument, not a printed verdict.

Reads two sibling pieces' own published generators, honestly:

  - gallery/0016-the-complete-set/generate.py declares its sixteen codes
    as a literal list. This script extracts that literal (ast.literal_eval
    on the actual text, not a retyped copy) and counts how many times each
    value 0-15 appears in it.
  - gallery/0017-one-stroke-apart/generate.py declares no literal list; it
    derives all sixteen codes from a Gray-code formula and asserts the
    result is a bijection before it will write anything. This script loads
    that module (without ever calling its main(), so it never touches
    0017's own grid.svg) and calls its own verify() function to get the
    same codes it uses.

Both grids are then redrawn here, in miniature, side by side, using the
same stroke convention 0016 and 0017 already share. Underneath each grid
is a plain bar count, one bar per possible value 0-15, height = how many
times that value's pattern occurs. Nothing about the layout is chosen to
make one side look worse: the same drawing routine and the same counting
routine run on both. If 0016's list were already a clean bijection, its
bars would come out as flat and even as 0017's, and no cell would get a
red outline. They don't, because the list has a 15 where a 0 belongs.

Run: python generate.py
Output: comparison.svg (deterministic; same output every run).
"""

import ast
import importlib.util
import re
from pathlib import Path

HERE = Path(__file__).parent
COMPLETE_SET_SRC = HERE / "../0016-the-complete-set/generate.py"
ONE_STROKE_SRC = HERE / "../0017-one-stroke-apart/generate.py"

CELL = 56
PAD = 10
COLS = 4
ROWS = 4
GRID_W = COLS * CELL + PAD * 2
BAR_W = 14
BAR_GAP = 2
BAR_MAX_H = 60
BAR_PANEL_H = BAR_MAX_H + 30
LABEL_H = 22
PANEL_W = max(GRID_W, 16 * (BAR_W + BAR_GAP) + PAD * 2)
PANEL_H = LABEL_H + ROWS * CELL + PAD * 2 + BAR_PANEL_H
GAP_BETWEEN = 40
WIDTH = PANEL_W * 2 + GAP_BETWEEN
HEIGHT = PANEL_H + 56


def extract_complete_set_codes():
    text = COMPLETE_SET_SRC.read_text(encoding="utf-8")
    m = re.search(r"codes\s*=\s*(\[[^\]]*\])", text)
    if not m:
        raise RuntimeError("could not find 'codes = [...]' in 0016's generate.py")
    return ast.literal_eval(m.group(1))


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # runs module-level defs only; main() is guarded
    return mod


def extract_one_stroke_codes():
    mod = load_module(ONE_STROKE_SRC, "one_stroke_apart_src")
    codes_by_pos = mod.verify()  # {(row, col): code}, and raises if not a bijection
    return [codes_by_pos[(r, c)] for r in range(mod.ROWS) for c in range(mod.COLS)]


def cell_lines(code, x0, y0):
    cx, cy = x0 + CELL / 2, y0 + CELL / 2
    m = 6
    lines = []
    if code & 1:
        lines.append(f'<line x1="{cx}" y1="{y0+m}" x2="{cx}" y2="{y0+CELL-m}"/>')
    if code & 2:
        lines.append(f'<line x1="{x0+m}" y1="{cy}" x2="{x0+CELL-m}" y2="{cy}"/>')
    if code & 4:
        lines.append(f'<line x1="{x0+m}" y1="{y0+CELL-m}" x2="{x0+CELL-m}" y2="{y0+m}"/>')
    if code & 8:
        lines.append(f'<line x1="{x0+m}" y1="{y0+m}" x2="{x0+CELL-m}" y2="{y0+CELL-m}"/>')
    return lines


def render_panel(ox, oy, title, codes):
    counts = [0] * 16
    for c in codes:
        if 0 <= c <= 15:
            counts[c] += 1
    dup_or_missing = {i for i, n in enumerate(counts) if n != 1}
    flagged_positions = {i for i, c in enumerate(codes) if c in dup_or_missing}

    svg = [f'<text x="{ox}" y="{oy+14}" font-size="13" fill="#111">{title}</text>']

    gy = oy + LABEL_H
    svg.append(
        f'<rect x="{ox+PAD}" y="{gy+PAD}" width="{COLS*CELL}" height="{ROWS*CELL}" '
        f'fill="none" stroke="#111" stroke-width="1.2"/>'
    )
    for i in range(1, COLS):
        x = ox + PAD + i * CELL
        svg.append(f'<line x1="{x}" y1="{gy+PAD}" x2="{x}" y2="{gy+PAD+ROWS*CELL}" stroke="#111" stroke-width="0.4" opacity="0.25"/>')
    for i in range(1, ROWS):
        y = gy + PAD + i * CELL
        svg.append(f'<line x1="{ox+PAD}" y1="{y}" x2="{ox+PAD+COLS*CELL}" y2="{y}" stroke="#111" stroke-width="0.4" opacity="0.25"/>')

    for i, code in enumerate(codes):
        row, col = divmod(i, COLS)
        x0 = ox + PAD + col * CELL
        y0 = gy + PAD + row * CELL
        if i in flagged_positions:
            svg.append(f'<rect x="{x0+1}" y="{y0+1}" width="{CELL-2}" height="{CELL-2}" fill="#fbdcdc" stroke="#b33" stroke-width="1.6"/>')
        svg.append(f'<g stroke="{"#b33" if i in flagged_positions else "#111"}" stroke-width="2.4" stroke-linecap="round">')
        svg.extend(cell_lines(code, x0, y0))
        svg.append("</g>")
        svg.append(
            f'<text x="{x0+CELL/2:.1f}" y="{y0+CELL-4:.1f}" text-anchor="middle" '
            f'font-size="8" fill="{"#b33" if i in flagged_positions else "#999"}">{i}</text>'
        )

    by = gy + PAD + ROWS * CELL + 22
    bx0 = ox + (PANEL_W - (16 * (BAR_W + BAR_GAP))) / 2
    svg.append(f'<line x1="{bx0}" y1="{by}" x2="{bx0+16*(BAR_W+BAR_GAP)}" y2="{by}" stroke="#111" stroke-width="0.8"/>')
    for v in range(16):
        n = counts[v]
        h = n * (BAR_MAX_H / 2) if n <= 2 else BAR_MAX_H
        x = bx0 + v * (BAR_W + BAR_GAP)
        color = "#111" if n == 1 else "#b33"
        if n == 0:
            svg.append(f'<rect x="{x}" y="{by-3}" width="{BAR_W}" height="3" fill="{color}"/>')
        else:
            svg.append(f'<rect x="{x}" y="{by-h}" width="{BAR_W}" height="{h}" fill="{color}"/>')
        svg.append(f'<text x="{x+BAR_W/2:.1f}" y="{by+11}" text-anchor="middle" font-size="7" fill="#888">{v}</text>')
    svg.append(f'<text x="{ox+PAD}" y="{by+26}" font-size="10" fill="#555">count of each value 0–15, one bar each</text>')

    return "\n".join(svg), (0 in dup_or_missing) or any(n > 1 for n in counts)


def build_svg():
    codes16 = extract_complete_set_codes()
    codes17 = extract_one_stroke_codes()

    left, left_flagged = render_panel(20, 20, "0016 — The Complete Set (as published)", codes16)
    right, right_flagged = render_panel(20 + PANEL_W + GAP_BETWEEN, 20, "0017 — One Stroke Apart (as published)", codes17)

    assert left_flagged, "expected 0016's own list to still contain the disclosed duplicate/omission"
    assert not right_flagged, "expected 0017's generated codes to still be a clean bijection"

    caption_lines = [
        'Cell 0 and cell 15, above left, draw the same four strokes. No cell anywhere in that grid is blank.',
        'Nothing here was read from a plaque — count the strokes yourself.',
    ]
    caption_svg = "\n".join(
        f'<text x="{WIDTH/2:.1f}" y="{HEIGHT-32+i*18}" text-anchor="middle" font-size="10.5" fill="#333">{line}</text>'
        for i, line in enumerate(caption_lines)
    )

    svg = f"""<svg viewBox="0 0 {WIDTH} {HEIGHT}" xmlns="http://www.w3.org/2000/svg" font-family="Georgia, 'Times New Roman', serif">
  <rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" fill="#fafaf7"/>
  {left}
  {right}
  {caption_svg}
</svg>
"""
    return svg


def main():
    svg = build_svg()
    (HERE / "comparison.svg").write_text(svg, encoding="utf-8")
    print("wrote comparison.svg")


if __name__ == "__main__":
    main()

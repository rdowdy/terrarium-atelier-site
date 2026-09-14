"""
Generates piece.svg from the sixteen lines below.

The only rule: each line is centered on the same vertical axis and set in
a monospace font at a fixed size, so its rendered width is determined
entirely by its character count. No line's width is set by hand, padded,
or letter-spaced to force a shape -- the shape is whatever falls out of
how many characters each line happens to need. The character counts were
chosen, while writing the poem, to trace a bell's cross-section: a narrow
loop, a neck, a shoulder, a waist, and a wide flared mouth at the bottom.
That choice is the only thing this script does not do for you.

Reproduce: python generate.py
"""

LINES = [
    "One",
    "strike,",
    "and already",
    "I am leaving,",
    "down through the bronze",
    "faster than the hand that",
    "swung it, faster than the ear",
    "that flinched before it heard me,",
    "narrowing where the metal",
    "narrows, a held breath in",
    "shaped like a throat,",
    "just before it widens,",
    "and I widen too, spilling",
    "past the lip and out into a room",
    "built with nothing in it shaped to stop me,",
    "thinner now, thinner, gone, and still ringing somewhere",
]

FONT_SIZE = 22
LINE_HEIGHT = 34
TOP_MARGIN = 40
SIDE_MARGIN = 40
# Widest line, in characters, sets the canvas width at a fixed px-per-char
# estimate for monospace at this size; text-anchor="middle" then does the
# real centering at render time, so this only has to be wide enough.
WIDEST_CHARS = max(len(l) for l in LINES)
PX_PER_CHAR_ESTIMATE = FONT_SIZE * 0.62

width = int(WIDEST_CHARS * PX_PER_CHAR_ESTIMATE + 2 * SIDE_MARGIN)
height = TOP_MARGIN * 2 + LINE_HEIGHT * len(LINES)
cx = width / 2

svg_lines = []
svg_lines.append(
    f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" '
    f'font-family="monospace" font-size="{FONT_SIZE}">'
)
svg_lines.append(f'<title>The Shape a Throat Makes</title>')
svg_lines.append(f'<rect x="0" y="0" width="{width}" height="{height}" fill="#f4f1ea"/>')

for i, line in enumerate(LINES):
    y = TOP_MARGIN + FONT_SIZE + i * LINE_HEIGHT
    escaped = (
        line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    )
    svg_lines.append(
        f'<text x="{cx}" y="{y}" text-anchor="middle" fill="#1c1a17">{escaped}</text>'
    )

svg_lines.append("</svg>")

with open("piece.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(svg_lines) + "\n")

print(f"wrote piece.svg, {width}x{height}, {len(LINES)} lines")

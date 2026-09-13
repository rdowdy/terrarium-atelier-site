#!/usr/bin/env python3
"""Where the Bars Begin.

One list, DATA, is declared exactly once, eight integers, chosen by
hand and left alone — not a formula tuned to make the point look
sharper, not random. It is never retyped, edited, or recomputed
between the two panels below: render_panel() is called twice with the
literal same list object, and an assertion at the end fails loudly if
that ever stops being true.

The only difference the code introduces between the two panels is the
FLOOR argument passed to render_panel(): 0 on the left, 38 on the
right. Every bar height is drawn by the same formula in both calls
(height = (value - floor) / (ceiling - floor) * available height); the
same function decides bar color, gridline spacing, and label
placement either way. Nothing about the drawing routine knows or cares
which panel is "the honest one," because neither panel contains a
false number. The two panels disagree only about where zero is allowed
to be, and both say so, in the same small grey type, at the same
corner, every time this script runs.

Run: python generate.py
Output: bars.svg (deterministic; same output every run).
"""

DATA = [42, 45, 47, 44, 49, 51, 48, 53]
LABELS = ["1", "2", "3", "4", "5", "6", "7", "8"]

PANEL_W = 300
PANEL_H = 260
BAR_GAP = 10
PAD_L = 40
PAD_R = 16
PAD_T = 34
PAD_B = 46
GAP_BETWEEN = 50
WIDTH = PANEL_W * 2 + GAP_BETWEEN
HEIGHT = PANEL_H + 90

_data_object_ids = []


def _nice_ticks(floor, ceiling, step):
    ticks = []
    t = floor
    while t <= ceiling + 1e-9:
        ticks.append(t)
        t += step
    return ticks


def render_panel(ox, title, floor, data, tick_step):
    _data_object_ids.append(id(data))

    ceiling = max(data) + 4
    plot_w = PANEL_W - PAD_L - PAD_R
    plot_h = PANEL_H - PAD_T - PAD_B
    n = len(data)
    bar_w = (plot_w - BAR_GAP * (n - 1)) / n

    def y_of(v):
        frac = (v - floor) / (ceiling - floor)
        return PAD_T + plot_h * (1 - frac)

    svg = [f'<text x="{ox}" y="18" font-size="13" fill="#111">{title}</text>']

    # axis line
    svg.append(
        f'<line x1="{ox+PAD_L}" y1="{PAD_T}" x2="{ox+PAD_L}" y2="{PAD_T+plot_h}" '
        f'stroke="#111" stroke-width="1"/>'
    )
    svg.append(
        f'<line x1="{ox+PAD_L}" y1="{PAD_T+plot_h}" x2="{ox+PAD_L+plot_w}" y2="{PAD_T+plot_h}" '
        f'stroke="#111" stroke-width="1"/>'
    )

    # gridlines + tick labels, drawn from the real floor/ceiling every time
    for t in _nice_ticks(floor, ceiling, tick_step):
        y = y_of(t)
        svg.append(
            f'<line x1="{ox+PAD_L}" y1="{y:.1f}" x2="{ox+PAD_L+plot_w}" y2="{y:.1f}" '
            f'stroke="#111" stroke-width="0.4" opacity="0.18"/>'
        )
        svg.append(
            f'<text x="{ox+PAD_L-6}" y="{y+3:.1f}" text-anchor="end" font-size="9" fill="#555">{t:g}</text>'
        )

    # bars + printed value atop each one
    for i, v in enumerate(data):
        x0 = ox + PAD_L + i * (bar_w + BAR_GAP)
        y0 = y_of(v)
        h = (PAD_T + plot_h) - y0
        svg.append(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{bar_w:.1f}" height="{h:.1f}" fill="#111"/>')
        svg.append(
            f'<text x="{x0+bar_w/2:.1f}" y="{y0-5:.1f}" text-anchor="middle" font-size="10" fill="#111">{v}</text>'
        )
        svg.append(
            f'<text x="{x0+bar_w/2:.1f}" y="{PAD_T+plot_h+14:.1f}" text-anchor="middle" font-size="9" fill="#888">{LABELS[i]}</text>'
        )

    svg.append(
        f'<text x="{ox+PAD_L}" y="{PANEL_H+18}" font-size="9.5" fill="#555">'
        f'axis starts at {floor}</text>'
    )

    return "\n".join(svg)


def build_svg():
    left = render_panel(20, "Eight months, floor 0", 0, DATA, tick_step=10)
    right = render_panel(20 + PANEL_W + GAP_BETWEEN, "The same eight months, floor 38", 38, DATA, tick_step=4)

    assert len(_data_object_ids) == 2
    assert _data_object_ids[0] == _data_object_ids[1] == id(DATA), (
        "both panels must draw the literal same list object, not a copy"
    )
    assert len(set(DATA)) > 1, "a flat list would make the trick invisible even honestly"

    caption_lines = [
        f"Same eight values, both panels, top to bottom, left to right: {' '.join(str(v) for v in DATA)}.",
        "Nothing in either bar is false. The only thing that moved is where the axis is allowed to start.",
        "A truncated floor is not always a lie: sometimes the honest zero would hide a difference that actually matters.",
        "This one has no printed verdict on which panel you should trust. That is the part left for you to decide.",
    ]
    caption_svg = "\n".join(
        f'<text x="{WIDTH/2:.1f}" y="{HEIGHT-58+i*15}" text-anchor="middle" font-size="10" fill="#333">{line}</text>'
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
    with open("bars.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote bars.svg")


if __name__ == "__main__":
    main()

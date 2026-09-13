"""
Generates gown.svg: a stylized photograph of a christening gown laid flat
on a table, in a Polaroid-style frame with a handwritten caption.

Run: python make_gown.py
Output: gown.svg (deterministic; same output every run, no randomness).
"""

W, H = 520, 700
FRAME = 26
CAPTION_H = 130
PHOTO_TOP = FRAME
PHOTO_LEFT = FRAME
PHOTO_RIGHT = W - FRAME
PHOTO_BOTTOM = H - FRAME - CAPTION_H


def lace_scallop_path(x0, y0, x1, y1, radius, start_up=True):
    """A row of semicircular scallops strung along the segment (x0,y0)-(x1,y1).
    Horizontal use only (y0 == y1), which is all this piece needs."""
    length = x1 - x0
    n = max(1, round(length / (radius * 2)))
    step = length / n
    r = step / 2
    sweep = 1 if start_up else 0
    d = [f"M {x0:.1f} {y0:.1f}"]
    x = x0
    for i in range(n):
        xm = x + step
        d.append(f"A {r:.1f} {r:.1f} 0 0 {sweep} {xm:.1f} {y0:.1f}")
        x = xm
    return " ".join(d)


def stitch_row(x0, x1, y, spacing=6, size=2.2):
    """A dashed hand-stitch suggestion: short diagonal ticks."""
    marks = []
    x = x0
    while x < x1:
        marks.append(
            f'<line x1="{x:.1f}" y1="{y - size:.1f}" x2="{x + size:.1f}" y2="{y + size:.1f}" '
            f'stroke="#8a7358" stroke-width="1" stroke-linecap="round"/>'
        )
        x += spacing
    return "\n".join(marks)


def build_svg():
    cx = (PHOTO_LEFT + PHOTO_RIGHT) / 2

    # --- tabletop (wood grain suggested by faint horizontal lines) ---
    grain_lines = []
    y = PHOTO_TOP + 10
    while y < PHOTO_BOTTOM:
        grain_lines.append(
            f'<line x1="{PHOTO_LEFT}" y1="{y:.1f}" x2="{PHOTO_RIGHT}" y2="{y:.1f}" '
            f'stroke="#a9855c" stroke-width="0.6" opacity="0.35"/>'
        )
        y += 14
    grain = "\n".join(grain_lines)

    # --- gown geometry (flat lay, front view, centered) ---
    shoulder_y = PHOTO_TOP + 70
    bodice_bottom_y = shoulder_y + 120
    hem_y = PHOTO_BOTTOM - 60
    shoulder_half_w = 62
    waist_half_w = 46
    hem_half_w = 150

    # cap sleeves: small petal shapes off each shoulder
    sleeve_l = (
        f'<path d="M {cx - shoulder_half_w:.1f} {shoulder_y + 8:.1f} '
        f'q -34 -6 -40 26 q -4 26 30 20 z" '
        f'fill="#f3ecdd" stroke="#c9b98f" stroke-width="1.2"/>'
    )
    sleeve_r = (
        f'<path d="M {cx + shoulder_half_w:.1f} {shoulder_y + 8:.1f} '
        f'q 34 -6 40 26 q 4 26 -30 20 z" '
        f'fill="#f3ecdd" stroke="#c9b98f" stroke-width="1.2"/>'
    )

    # bodice: trapezoid from shoulders to waist
    bodice = (
        f'<path d="M {cx - shoulder_half_w:.1f} {shoulder_y:.1f} '
        f'L {cx + shoulder_half_w:.1f} {shoulder_y:.1f} '
        f'L {cx + waist_half_w:.1f} {bodice_bottom_y:.1f} '
        f'L {cx - waist_half_w:.1f} {bodice_bottom_y:.1f} Z" '
        f'fill="#f6f0e2" stroke="#c9b98f" stroke-width="1.4"/>'
    )

    # skirt: bell shape from waist to hem
    skirt = (
        f'<path d="M {cx - waist_half_w:.1f} {bodice_bottom_y:.1f} '
        f'L {cx + waist_half_w:.1f} {bodice_bottom_y:.1f} '
        f'C {cx + waist_half_w + 30:.1f} {bodice_bottom_y + 50:.1f}, '
        f'{cx + hem_half_w:.1f} {hem_y - 40:.1f}, {cx + hem_half_w:.1f} {hem_y:.1f} '
        f'L {cx - hem_half_w:.1f} {hem_y:.1f} '
        f'C {cx - hem_half_w:.1f} {hem_y - 40:.1f}, '
        f'{cx - waist_half_w - 30:.1f} {bodice_bottom_y + 50:.1f}, {cx - waist_half_w:.1f} {bodice_bottom_y:.1f} Z" '
        f'fill="#f6f0e2" stroke="#c9b98f" stroke-width="1.4"/>'
    )

    # center-front placket + buttons
    buttons = []
    by = shoulder_y + 14
    while by < bodice_bottom_y - 6:
        buttons.append(f'<circle cx="{cx:.1f}" cy="{by:.1f}" r="2.1" fill="#c9b98f"/>')
        by += 18
    placket = (
        f'<line x1="{cx:.1f}" y1="{shoulder_y:.1f}" x2="{cx:.1f}" y2="{bodice_bottom_y:.1f}" '
        f'stroke="#d8cba6" stroke-width="1"/>'
    )

    # neckline lace: scalloped collar arc
    collar = lace_scallop_path(cx - shoulder_half_w + 6, shoulder_y, cx + shoulder_half_w - 6, shoulder_y, radius=8)
    collar_path = f'<path d="{collar}" fill="none" stroke="#b9a06c" stroke-width="1.3"/>'

    # hem lace: scalloped border, wider radius for the fuller hem
    hem_lace = lace_scallop_path(cx - hem_half_w, hem_y, cx + hem_half_w, hem_y, radius=11)
    hem_lace_path = f'<path d="{hem_lace}" fill="none" stroke="#b9a06c" stroke-width="1.4"/>'

    # a small reinforcement patch near the hem, off-center — quiet evidence
    # the gown was let down and re-hemmed once, between two wearings.
    patch_x = cx - 58
    patch_y = hem_y - 22
    patch = (
        f'<rect x="{patch_x:.1f}" y="{patch_y:.1f}" width="16" height="14" '
        f'fill="#efe6d0" stroke="#b9a06c" stroke-width="0.8"/>'
        + stitch_row(patch_x + 1, patch_x + 15, patch_y + 4)
        + stitch_row(patch_x + 1, patch_x + 15, patch_y + 10)
    )

    # a faint re-stitched seam running just above the hem on one side —
    # the line wavers slightly, unlike the machine-straight seams elsewhere.
    reseam = (
        f'<path d="M {cx - hem_half_w + 20:.1f} {hem_y - 34:.1f} '
        f'q 18 3 36 -1 q 18 -4 34 2 q 16 5 30 -2" '
        f'fill="none" stroke="#a9855c" stroke-width="0.9" stroke-dasharray="2,3" opacity="0.75"/>'
    )

    gown = "\n".join([
        skirt, bodice, sleeve_l, sleeve_r,
        collar_path, placket, "\n".join(buttons),
        hem_lace_path, reseam, patch,
    ])

    svg = f"""<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="Georgia, 'Times New Roman', serif">
  <rect x="0" y="0" width="{W}" height="{H}" fill="#faf6ec"/>
  <rect x="{PHOTO_LEFT}" y="{PHOTO_TOP}" width="{PHOTO_RIGHT - PHOTO_LEFT}" height="{PHOTO_BOTTOM - PHOTO_TOP}"
        fill="#cbb489" stroke="#e7ded0" stroke-width="1"/>
  {grain}
  {gown}
  <rect x="{PHOTO_LEFT}" y="{PHOTO_TOP}" width="{PHOTO_RIGHT - PHOTO_LEFT}" height="{PHOTO_BOTTOM - PHOTO_TOP}"
        fill="none" stroke="#00000022" stroke-width="10"/>
  <text x="{W/2:.1f}" y="{H - CAPTION_H + 46:.1f}" text-anchor="middle"
        font-style="italic" font-size="19" fill="#3d3428">enclosed, not because it settles anything</text>
  <text x="{W/2:.1f}" y="{H - CAPTION_H + 76:.1f}" text-anchor="middle"
        font-size="13" fill="#6b5f4d">three months after the sale</text>
</svg>
"""
    return svg


if __name__ == "__main__":
    with open("gown.svg", "w", encoding="utf-8") as f:
        f.write(build_svg())
    print("wrote gown.svg")

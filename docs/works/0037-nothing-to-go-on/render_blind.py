#!/usr/bin/env python3
"""Render the fully blind chart for the "no anchor at all" experiment.

Same eight bars, same FLOOR, same CEILING, same drawing convention as
gallery/0036-choose-your-own-floor -- this is the literal picture that
piece proved was consistent with infinitely many (floor, scale, dataset)
triples. That proof answered whether the floor is *recoverable* (no).
This experiment asks the question the proof deliberately didn't: faced
with nothing but this picture, what does a guesser actually *say* when
asked for a number anyway?

Unlike gallery/0035's render_blind.py, no value is printed on or near
any bar. Only the bar shapes and their 1-8 index labels are shown --
exactly what index.html's <svg> draws before any slider is touched.

Writes:
  blind.png    -- the image shown to guessers (nothing revealed)
  answer.json  -- the true floor, data, and pixel heights, kept out of
                  blind.png and out of the isolated copy shown to guessers
Run: python render_blind.py
"""

import json
from PIL import Image, ImageDraw, ImageFont

DATA = [46, 61, 34, 53, 70, 42, 57, 66]  # identical to gallery/0036
FLOOR = 15                                # identical to gallery/0036
CEILING = max(DATA) + 4                   # identical to gallery/0036

W, H = 700, 500
PAD_T, PAD_B, PAD_L, PAD_R = 70, 70, 40, 40
PLOT_W = W - PAD_L - PAD_R
PLOT_H = H - PAD_T - PAD_B
GAP = 16
N = len(DATA)
BAR_W = (PLOT_W - GAP * (N - 1)) / N


def bar_height_px(v):
    frac = (v - FLOOR) / (CEILING - FLOOR)
    return round(PLOT_H * frac)


def build_blind_image():
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 16)
        font_small = ImageFont.truetype("arial.ttf", 15)
    except Exception:
        font = ImageFont.load_default()
        font_small = font

    baseline_y = PAD_T + PLOT_H  # bottom of every bar; not labeled as zero

    heights = []
    for i, v in enumerate(DATA):
        x0 = PAD_L + i * (BAR_W + GAP)
        x1 = x0 + BAR_W
        h = bar_height_px(v)
        heights.append(h)
        y0 = baseline_y - h
        y1 = baseline_y
        d.rectangle([x0, y0, x1, y1], fill="black")
        label = str(i + 1)
        lw = d.textlength(label, font=font_small)
        d.text((x0 + BAR_W / 2 - lw / 2, baseline_y + 8), label, fill="#555", font=font_small)

    title = "Eight bars. No numbers. No axis. No floor."
    d.text((PAD_L, 24), title, fill="black", font=font)
    img.save("blind.png")

    with open("answer.json", "w") as f:
        json.dump({
            "data": DATA,
            "floor": FLOOR,
            "ceiling": CEILING,
            "plot_height_px": PLOT_H,
            "bar_heights_px": heights,
            "baseline_y_px": baseline_y,
            "image_size": [W, H],
        }, f, indent=2)


if __name__ == "__main__":
    build_blind_image()
    print("wrote blind.png and answer.json")

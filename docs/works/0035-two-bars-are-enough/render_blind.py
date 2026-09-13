#!/usr/bin/env python3
"""Render the blind chart for the floor-guessing experiment.

DATA is eight hand-picked integers (not tuned to any formula). FLOOR is a
single hand-picked value, less than min(DATA), that a blind guesser must
try to recover from the image alone -- no axis, no gridlines, no floor
label, nothing but the bars and the printed value on top of each one.
The rendering convention (ceiling = max(DATA) + 4, plot height maps
[floor, ceiling] to [0, PLOT_H]) matches gallery/0033 and gallery/0034
so this experiment tests the same device the trilogy is built on.

Writes:
  blind.png    -- the image shown to guessers (no floor revealed)
  answer.json  -- the true floor and the exact pixel heights used, kept
                  out of blind.png entirely
Run: python render_blind.py
"""

import json
from PIL import Image, ImageDraw, ImageFont

DATA = [34, 39, 31, 44, 36, 41, 33, 46]
LABELS = [str(i + 1) for i in range(len(DATA))]
FLOOR = 22
CEILING = max(DATA) + 4

W, H = 700, 500
PAD_T, PAD_B, PAD_L, PAD_R = 70, 70, 40, 40
PLOT_W = W - PAD_L - PAD_R
PLOT_H = H - PAD_T - PAD_B
GAP = 16
BAR_W = (PLOT_W - GAP * (len(DATA) - 1)) / len(DATA)

def bar_height_px(v):
    frac = (v - FLOOR) / (CEILING - FLOOR)
    return round(PLOT_H * frac)

def build_blind_image():
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
        font_small = ImageFont.truetype("arial.ttf", 15)
    except Exception:
        font = ImageFont.load_default()
        font_small = font

    baseline_y = PAD_T + PLOT_H  # bottom of every bar; NOT labeled as zero

    heights = []
    for i, v in enumerate(DATA):
        x0 = PAD_L + i * (BAR_W + GAP)
        x1 = x0 + BAR_W
        h = bar_height_px(v)
        heights.append(h)
        y0 = baseline_y - h
        y1 = baseline_y
        d.rectangle([x0, y0, x1, y1], fill="black")
        text = str(v)
        tw = d.textlength(text, font=font)
        d.text((x0 + BAR_W / 2 - tw / 2, y0 - 26), text, fill="black", font=font)
        lw = d.textlength(LABELS[i], font=font_small)
        d.text((x0 + BAR_W / 2 - lw / 2, baseline_y + 8), LABELS[i], fill="#555", font=font_small)

    title = "Eight bars. No axis. No floor printed anywhere."
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

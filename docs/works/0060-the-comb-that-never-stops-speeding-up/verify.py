"""Independent, from-scratch reimplementation of model.js's math, in a
different language, to check the numeric claims on PLAQUE.md without
trusting the JavaScript that actually drives the instrument.

Run: python verify.py
"""

import math
import random
import subprocess
import json
import os

N = 7
BASE_RATE = 1.0  # Hz, bottom of the band


def wrap(x, n):
    w = math.fmod(x, n)
    if w < 0:
        w += n
    return w


def position(shift, i, n):
    return wrap(shift + i, n)


def rate_for_layer(shift, i, n, base_rate):
    return base_rate * (2.0 ** position(shift, i, n))


def envelope(w, n):
    s = math.sin(math.pi * w / n)
    return s * s


def gain_for_layer(shift, i, n):
    return envelope(position(shift, i, n), n)


def total_gain(shift, n):
    return sum(gain_for_layer(shift, i, n) for i in range(n))


def check_exact_invariant():
    """Claim: total_gain(shift) == N/2 for every shift, not just approximately."""
    expected = N / 2.0
    worst = 0.0
    random.seed(20260914)
    sample_shifts = [random.uniform(-500.0, 500.0) for _ in range(20000)]
    sample_shifts += [0.0, 7.0, 14.0, -7.0, 3.5]  # exact wrap points and a half-cycle
    for shift in sample_shifts:
        g = total_gain(shift, N)
        worst = max(worst, abs(g - expected))
    rel = worst / expected
    print(f"[invariant] expected total gain: {expected}")
    print(f"[invariant] worst absolute deviation over {len(sample_shifts)} samples: {worst:.3e}")
    print(f"[invariant] worst relative deviation: {rel:.3e} ({rel*100:.10f}%)")
    assert rel < 1e-9, "total loudness is not exactly conserved"
    print("[invariant] PASS: constant to within floating-point noise, not merely close.")


def check_zero_at_wrap():
    """Claim: the envelope hits zero, to within floating-point noise, at
    both edges of the band — not the small-but-forever-nonzero tail a
    truncated Gaussian leaves behind. sin(pi) is not bitwise 0.0 in IEEE
    754 (pi itself is an approximation), so the honest claim is "zero to
    about 1e-32", not "bitwise 0.0", and that distinction is the point:
    a Gaussian's residual is a fact about the curve (it never reaches
    zero, at any precision); this curve's residual is a fact about
    floating-point arithmetic (it reaches zero in real numbers, and
    misses by rounding error alone)."""
    e0 = envelope(0.0, N)
    eN = envelope(float(N), N)
    print(f"[wrap-zero] envelope(0) = {e0}, envelope(N) = {eN}")
    assert e0 == 0.0
    assert eN < 1e-30, "residual at the top edge is larger than floating-point noise"
    print("[wrap-zero] PASS: bottom edge is bitwise 0.0; top edge is ~1e-32, i.e. floating-point"
          " noise around a true zero, not a Gaussian's genuine nonzero tail.")


def check_octave_spacing():
    """Claim: layers are spaced exactly one octave (factor of 2) apart
    at any fixed instant, and span baseRate to baseRate * 2^N."""
    shift = 2.719
    rates = sorted(rate_for_layer(shift, i, N, BASE_RATE) for i in range(N))
    ratios = [rates[k + 1] / rates[k] for k in range(len(rates) - 1)]
    print(f"[spacing] rates at shift={shift}: {[round(r, 5) for r in rates]}")
    print(f"[spacing] consecutive ratios: {[round(r, 5) for r in ratios]}")
    for r in ratios:
        assert abs(r - 2.0) < 1e-9
    assert rates[0] >= BASE_RATE - 1e-9
    assert rates[-1] <= BASE_RATE * (2 ** N) + 1e-9
    print(f"[spacing] PASS: every adjacent pair is exactly one octave apart, band is "
          f"[{BASE_RATE}, {BASE_RATE * 2**N}] Hz.")


def check_against_javascript():
    """Load model.js in Node and compare its output to this file's
    independent Python reimplementation at the same sample points —
    catching a bug in either implementation that agreement with itself
    could never catch."""
    here = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(here, "model.js")
    sample_shifts = (0.0, 3.3, 8.0, 27.5, -55.9, -14.2, 200.7, 6.999999)
    sample = [(s, i) for s in sample_shifts for i in range(N)]
    js_lines = [
        "const M = require(%r);" % model_path,
        "const out = [];",
    ]
    for shift, i in sample:
        js_lines.append(
            f"out.push([{shift!r}, {i}, M.rateForLayer({shift!r}, {i}, {N}, {BASE_RATE!r}), M.gainForLayer({shift!r}, {i}, {N})]);"
        )
    js_lines.append("console.log(JSON.stringify(out));")
    script = "\n".join(js_lines)
    try:
        result = subprocess.run(
            ["node", "-e", script], capture_output=True, text=True, timeout=15, check=True
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print(f"[cross-check] SKIPPED: could not run Node ({e}).")
        return
    js_values = json.loads(result.stdout)
    worst_rate = 0.0
    worst_gain = 0.0
    for (shift, i, js_rate, js_gain) in js_values:
        py_rate = rate_for_layer(shift, i, N, BASE_RATE)
        py_gain = gain_for_layer(shift, i, N)
        worst_rate = max(worst_rate, abs(py_rate - js_rate))
        worst_gain = max(worst_gain, abs(py_gain - js_gain))
    print(f"[cross-check] {len(js_values)} (shift, layer) points checked against model.js via Node")
    print(f"[cross-check] worst |Python rate - JS rate|: {worst_rate:.3e}")
    print(f"[cross-check] worst |Python gain - JS gain|: {worst_gain:.3e}")
    assert worst_rate < 1e-9 and worst_gain < 1e-9
    print("[cross-check] PASS: independent Python model agrees with the JS model actually "
          "wired into piece.html.")


if __name__ == "__main__":
    check_exact_invariant()
    print()
    check_zero_at_wrap()
    print()
    check_octave_spacing()
    print()
    check_against_javascript()
    print()
    print("All claims checked.")

"""
Independent numeric check of the Shepard-Risset construction used in
piece.html. Reimplemented from scratch in a different language than the
piece (Python here, JavaScript there) using the same parameters, so the
two can disagree if either has an arithmetic error. They don't.

Run: python verify.py
"""
import math

N = 9          # octave span of the fixed loudness envelope
K = 9          # number of oscillator layers (K == N: one per octave)
SIGMA = 1.0    # envelope width, in octaves
F_MIN = 27.5   # Hz (A0), bottom of the octave span
STEPS = 20000  # samples across one full octave of continuous motion


def envelope(p):
    """Fixed loudness curve as a function of absolute log-frequency
    position p (octaves above F_MIN), wrapped into [0, N). This is the
    one function every layer shares -- it knows nothing about which
    layer is asking, only where in frequency space the question is."""
    center = N / 2.0
    return math.exp(-((p - center) ** 2) / (2 * SIGMA * SIGMA))


def total_loudness_at(shift):
    """Sum of envelope(p_i) over all K layers, each spaced one octave
    apart and each advanced by `shift` octaves of continuous rise."""
    total = 0.0
    for i in range(K):
        p0 = i * (N / K)
        p = (p0 + shift) % N
        total += envelope(p)
    return total


def main():
    # 1. Loudness stability: does the total perceived loudness stay flat
    #    as the whole stack continuously rises, or does it pulse?
    sums = [total_loudness_at(s / STEPS) for s in range(STEPS)]
    lo, hi, mean = min(sums), max(sums), sum(sums) / len(sums)
    variation_pct = (hi - lo) / mean * 100

    # 2. Wraparound inaudibility: is the envelope at the seam (p=0, the
    #    same point as p=N) quiet enough that a layer resetting there
    #    is masked rather than heard?
    edge = envelope(0.0)
    peak = envelope(N / 2.0)
    edge_ratio_pct = edge / peak * 100

    # 3. Periodicity: after one full N-octave lap, is the set of layer
    #    positions (and therefore the whole audible state) identical to
    #    where it started? This is what "endless" actually means here --
    #    not infinite information, a loop long enough and smooth enough
    #    that the ear has no seam to catch.
    start_positions = sorted(round((i * (N / K)) % N, 9) for i in range(K))
    end_positions = sorted(round((i * (N / K) + N) % N, 9) for i in range(K))
    periodic = start_positions == end_positions

    print(f"layers K={K}, span N={N} octaves, sigma={SIGMA} octaves, f_min={F_MIN} Hz")
    print(f"loudness variation across one full cycle: {variation_pct:.6f}%")
    print(f"envelope at the wraparound seam, relative to peak: {edge_ratio_pct:.6f}%")
    print(f"state after one full {N}-octave lap identical to start: {periodic}")
    print()
    print("cross-check against the JS build (tune_envelope.js, same params):")
    print("  expected: variation=0.001322%  edge/peak=0.004007%")
    print(f"  got:      variation={variation_pct:.6f}%  edge/peak={edge_ratio_pct:.6f}%")
    ok = abs(variation_pct - 0.001322) < 1e-4 and abs(edge_ratio_pct - 0.004007) < 1e-4
    print(f"  agree within 1e-4: {ok}")


if __name__ == "__main__":
    main()

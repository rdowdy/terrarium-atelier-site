"""Verifies the claim on the plaque: for the four-question shape used by
0019-a-hand-ill-never-see (three mutually exclusive category questions
plus one independent one), codes 5, 7, 9, 11, 12, 13, 14, 15 can never be
reached by any letter, no matter which letters are sorted into which
category. Mirrors piece.html's JS exactly; run with `python verify.py`.
"""

import random

LETTERS = list("abcdefghijklmnopqrstuvwxyz")
FORBIDDEN = {5, 7, 9, 11, 12, 13, 14, 15}
TRIALS = 100_000


def codes_for(vowel, second_half, asc, desc):
    buckets = {c: [] for c in range(16)}
    for letter in LETTERS:
        code = 0
        if letter in vowel:
            code |= 1
        if letter in second_half:
            code |= 2
        if letter in asc:
            code |= 4
        if letter in desc:
            code |= 8
        buckets[code].append(letter)
    return buckets


def original_buckets():
    return codes_for(
        set("aeiou"),
        set("nopqrstuvwxyz"),
        set("bdfhklt"),
        set("gjpqy"),
    )


def random_buckets(rng):
    pool = LETTERS[:]
    rng.shuffle(pool)
    v_size = rng.randint(2, 7)
    a_size = rng.randint(2, 8)
    d_size = rng.randint(2, 6)
    i = 0
    vowel = set(pool[i:i + v_size]); i += v_size
    asc = set(pool[i:i + a_size]); i += a_size
    desc = set(pool[i:i + d_size]); i += d_size
    pool2 = LETTERS[:]
    rng.shuffle(pool2)
    sh_size = rng.randint(6, 19)
    second_half = set(pool2[:sh_size])
    return codes_for(vowel, second_half, asc, desc)


def main():
    rng = random.Random(2026)

    original = original_buckets()
    reachable = {c for c, letters in original.items() if letters}
    assert reachable == set(range(16)) - FORBIDDEN, (
        f"Original scheme's reachable set changed: {sorted(reachable)}"
    )
    print(f"Original scheme: codes {sorted(FORBIDDEN)} unreachable, matches plaque.")

    worst_populated_in_forbidden = 0
    for _ in range(TRIALS):
        buckets = random_buckets(rng)
        for code in FORBIDDEN:
            if buckets[code]:
                worst_populated_in_forbidden += 1
                raise AssertionError(
                    f"Invariant broken: code {code} got letters "
                    f"{buckets[code]} on a random trial."
                )

    print(f"{TRIALS} random reshuffles checked. Forbidden codes populated: "
          f"{worst_populated_in_forbidden} times.")
    print("PASS: the eight-code gap held under every reshuffle tried.")


if __name__ == "__main__":
    main()

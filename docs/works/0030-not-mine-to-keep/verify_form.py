"""
Verifies that poem.md is a formally correct sestina:

  - six stanzas of six lines
  - a closing envoi of three lines
  - each stanza's end-words are a permutation of the same six words
  - each stanza after the first derives its end-word order from the
    previous stanza by the canonical sestina rule: take the previous
    stanza's end-words in the order (6, 1, 5, 2, 4, 3)
  - the envoi contains all six end-words, two per line, in the
    conventional pairing (2,5) (4,3) (6,1), with the second of each
    pair closing the line

This checks the form only. It does not check, or reveal, anything
about the specific words chosen.

Run: python verify_form.py
"""

import re
import sys

CANON_ORDER = [6, 1, 5, 2, 4, 3]
ENVOI_PAIRS = [(2, 5), (4, 3), (6, 1)]


def last_word(line):
    line = line.strip()
    line = re.sub(r"[\s.,;:!?—–\-]+$", "", line)
    return line.split()[-1].lower()


def load_stanzas(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    text = text.split("\n", 1)[1] if text.startswith("#") else text
    blocks = [b for b in text.split("\n\n") if b.strip()]
    return [[ln for ln in b.splitlines() if ln.strip()] for b in blocks]


def main():
    stanzas = load_stanzas("poem.md")
    ok = True

    if len(stanzas) != 7:
        print(f"FAIL: expected 7 blocks (6 stanzas + envoi), found {len(stanzas)}")
        return 1

    body, envoi = stanzas[:6], stanzas[6]

    for i, s in enumerate(body):
        if len(s) != 6:
            print(f"FAIL: stanza {i + 1} has {len(s)} lines, expected 6")
            ok = False

    orders = [[last_word(ln) for ln in s] for s in body]
    base_set = set(orders[0])
    for i, order in enumerate(orders):
        if set(order) != base_set:
            print(f"FAIL: stanza {i + 1} does not use the same six end-words")
            ok = False

    for i in range(1, 6):
        prev, cur = orders[i - 1], orders[i]
        expected = [prev[idx - 1] for idx in CANON_ORDER]
        if cur != expected:
            print(f"FAIL: stanza {i + 1} does not follow the canonical rotation")
            print(f"  expected: {expected}")
            print(f"  found:    {cur}")
            ok = False

    if len(envoi) != 3:
        print(f"FAIL: envoi has {len(envoi)} lines, expected 3")
        ok = False
    else:
        first_order = orders[0]
        envoi_words = [last_word(ln) for ln in envoi]
        for line, (mid_i, end_i) in zip(envoi, ENVOI_PAIRS):
            mid_word, end_word = first_order[mid_i - 1], first_order[end_i - 1]
            words_in_line = re.findall(r"[a-zA-Z']+", line.lower())
            if last_word(line) != end_word:
                print(f"FAIL: envoi line does not end on '{end_word}': {line}")
                ok = False
            if mid_word not in words_in_line[:-1]:
                print(f"FAIL: envoi line missing mid-line word '{mid_word}': {line}")
                ok = False
        if sorted(envoi_words) != sorted(first_order[i - 1] for _, i in ENVOI_PAIRS):
            print("FAIL: envoi end-words do not match the expected closing set")
            ok = False

    print("PASS: all sestina form checks hold" if ok else "one or more checks failed")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

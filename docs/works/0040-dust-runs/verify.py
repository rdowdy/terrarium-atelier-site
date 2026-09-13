#!/usr/bin/env python3
"""Verify the univocalic constraint claimed by poem.md: within the seven
free-verse stanzas, the only vowel letter allowed anywhere is U. A, E, I,
O are forbidden in any position (a letter-level constraint, not a
phonetic one, following the precedent set by 0038 and 0039's own
verify.py scripts). Y is treated as neither required nor forbidden.

Checks only the stanza bodies (everything after the "---" divider) --
not the title or the italic preamble describing the constraint, which
are commentary, not the poem. Unlike 0038 and 0039, this piece has no
stanza-number headers to exclude: it is free verse, not a fixed form, so
there is nothing but blank lines separating one stanza from the next.

Also reports word-count statistics used on the plaque: total words,
distinct words, and the distinct-word ratio at word 49 and word 98 (to
compare directly against 0038's exact 98-word/49-distinct result) and at
the poem's full length.

Run: python verify.py
"""

import re
import sys
from collections import Counter

FORBIDDEN = set("aeio")


def stanza_words(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    try:
        start = next(i for i, l in enumerate(lines) if l.strip() == "---")
    except StopIteration:
        print("No '---' divider found; cannot isolate the poem body.")
        sys.exit(1)
    body = [l for l in lines[start + 1:] if l.strip()]
    words = []
    for lineno, line in enumerate(body, start=1):
        for word in re.findall(r"[A-Za-z']+", line):
            words.append((lineno, word))
    return words


def check(path):
    violations = []
    words = []
    for lineno, word in stanza_words(path):
        words.append(word.lower())
        for ch in word.lower():
            if ch.isalpha() and ch in FORBIDDEN:
                violations.append((lineno, word, ch))
    return violations, words


if __name__ == "__main__":
    violations, words = check("poem.md")
    print(f"Checked {len(words)} words.")
    if violations:
        print(f"\n{len(violations)} violation(s) found:\n")
        for lineno, word, ch in violations:
            print(f"  line {lineno}: '{word}' contains forbidden letter '{ch}'")
        sys.exit(1)

    seen = set()
    checkpoints = {}
    for i, w in enumerate(words, start=1):
        seen.add(w)
        if i in (49, 98, len(words)):
            checkpoints[i] = len(seen)

    print("Clean. Every letter in every word is U, or a consonant, or Y. "
          "No A, E, I, O anywhere.")
    print(f"Total: {len(words)} words, {len(set(words))} distinct "
          f"({len(set(words)) / len(words) * 100:.1f}%).")
    for n, distinct in sorted(checkpoints.items()):
        print(f"  at word {n}: {distinct} distinct ({distinct / n * 100:.1f}%)")
    print("Most common:", Counter(words).most_common(10))
    sys.exit(0)

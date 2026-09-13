#!/usr/bin/env python3
"""Verify the univocalic constraint claimed by poem.md: within the four
numbered stanzas, the only vowel letter allowed anywhere is O. A, E, I, U
are forbidden in any position (not just as the primary vowel sound) --
a letter-level constraint, not a phonetic one. Y is treated as neither
required nor forbidden.

Checks only the stanza body (everything after the "---" divider, minus
the bare roman-numeral stanza headers) -- not the title or the italic
preamble describing the constraint, which are commentary, not the poem.

Run: python verify.py
"""

import re
import sys

FORBIDDEN = set("aeiu")
STANZA_HEADERS = {"I", "II", "III", "IV"}


def stanza_lines(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    try:
        start = next(i for i, l in enumerate(lines) if l.strip() == "---")
    except StopIteration:
        print("No '---' divider found; cannot isolate the poem body.")
        sys.exit(1)
    body = lines[start + 1:]
    return [l for l in body if l.strip() and l.strip() not in STANZA_HEADERS]


def check(path):
    violations = []
    words_checked = 0
    letters_checked = 0
    for lineno, line in enumerate(stanza_lines(path), start=1):
        for word in re.findall(r"[A-Za-z']+", line):
            words_checked += 1
            for ch in word.lower():
                if ch.isalpha():
                    letters_checked += 1
                    if ch in FORBIDDEN:
                        violations.append((lineno, word, ch, line.strip()))
    return violations, words_checked, letters_checked


if __name__ == "__main__":
    violations, words_checked, letters_checked = check("poem.md")
    print(f"Checked {words_checked} words, {letters_checked} letters across the four stanzas.")
    if violations:
        print(f"\n{len(violations)} violation(s) found:\n")
        for lineno, word, ch, line in violations:
            print(f"  stanza line {lineno}: '{word}' contains forbidden letter '{ch}'")
            print(f"    -> {line}")
        sys.exit(1)
    else:
        print("Clean. Every letter in every word is O, or a consonant, or Y. No A, E, I, U anywhere.")
        sys.exit(0)

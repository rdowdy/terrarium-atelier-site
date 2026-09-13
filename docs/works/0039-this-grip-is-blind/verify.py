#!/usr/bin/env python3
"""Verify the univocalic constraint claimed by poem.md: within the six
sestina stanzas and the envoi, the only vowel letter allowed anywhere is
I. A, E, O, U are forbidden in any position (a letter-level constraint,
not a phonetic one, following the precedent set by 0038's verify.py). Y
is treated as neither required nor forbidden: a word may legally contain
zero instances of I, so long as it contains none of A, E, O, U either.

Checks only the stanza bodies (everything after the "---" divider, minus
the bare roman-numeral stanza headers I-VI and the word "Envoi") -- not
the title or the italic preamble describing the constraint, which are
commentary, not the poem. This mirrors 0038's own exclusion of its
stanza headers, which was necessary there because roman numeral "I" is
itself forbidden under an O-only constraint. Here the roman numerals are
already compliant (I is the permitted vowel; V is a plain consonant) and
would pass unexcluded; only "Envoi" needs the exclusion, since it
contains both a forbidden E and a forbidden O.

Run: python verify.py
"""

import re
import sys

FORBIDDEN = set("aeou")
STANZA_HEADERS = {"I", "II", "III", "IV", "V", "VI", "Envoi"}


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
    lines_checked = 0
    for lineno, line in enumerate(stanza_lines(path), start=1):
        lines_checked += 1
        for word in re.findall(r"[A-Za-z']+", line):
            words_checked += 1
            for ch in word.lower():
                if ch.isalpha():
                    letters_checked += 1
                    if ch in FORBIDDEN:
                        violations.append((lineno, word, ch, line.strip()))
    return violations, words_checked, letters_checked, lines_checked


if __name__ == "__main__":
    violations, words_checked, letters_checked, lines_checked = check("poem.md")
    print(f"Checked {words_checked} words, {letters_checked} letters across {lines_checked} lines.")
    if lines_checked != 39:
        print(f"WARNING: expected 39 lines (6 stanzas x 6 + 3-line envoi), found {lines_checked}.")
    if violations:
        print(f"\n{len(violations)} violation(s) found:\n")
        for lineno, word, ch, line in violations:
            print(f"  stanza line {lineno}: '{word}' contains forbidden letter '{ch}'")
            print(f"    -> {line}")
        sys.exit(1)
    else:
        print("Clean. Every letter in every word is I, or a consonant, or Y. No A, E, O, U anywhere.")
        sys.exit(0)

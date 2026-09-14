#!/usr/bin/env python3
"""Verify the lipogram constraint claimed by piece.md: no word in the
body of the piece (everything after the "---" divider) contains the
letter E, upper or lower case. The title and the italic preamble
describing the constraint are commentary, not the piece, and are not
checked -- the same convention 0038-0041's verify.py scripts used for
their own vowel constraints.

Also reports total word count, since the piece's own theme (a resident
who folds card stock into a shape that will not lie flat again) is
built entirely out of a controlled, E-free vocabulary, and a stranger
should be able to see how large that vocabulary actually had to be.

Run: python verify.py
"""

import re
import sys

FORBIDDEN = "e"


def body_words(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    try:
        start = next(i for i, l in enumerate(lines) if l.strip() == "---")
    except StopIteration:
        print("No '---' divider found; cannot isolate the piece body.")
        sys.exit(1)
    body = [l for l in lines[start + 1:] if l.strip()]
    words = []
    for lineno, line in enumerate(body, start=start + 2):
        for word in re.findall(r"[A-Za-z']+", line):
            words.append((lineno, word))
    return words


def check(path):
    violations = []
    words = []
    for lineno, word in body_words(path):
        words.append(word.lower())
        if FORBIDDEN in word.lower():
            violations.append((lineno, word))
    return violations, words


if __name__ == "__main__":
    violations, words = check("piece.md")
    print(f"Checked {len(words)} words in the piece body.")
    if violations:
        print(f"\n{len(violations)} violation(s) found:\n")
        for lineno, word in violations:
            print(f"  line {lineno}: '{word}' contains forbidden letter 'e'")
        sys.exit(1)

    print("Clean. No word below the divider contains the letter E.")
    print(f"Total: {len(words)} words, {len(set(words))} distinct "
          f"({len(set(words)) / len(words) * 100:.1f}%).")
    sys.exit(0)

"""
Verifies two things about logbook.md:

  1. Its oldest and newest surviving lines are not invented here. They
     are exact substrings of gallery/0030-not-mine-to-keep/poem.md,
     the piece this one extends. This is checked, not asserted: the
     script reads 0030's actual file and diffs against it.
  2. Its four middle entries (the ones this piece actually adds) share
     one mechanical rule: each is "mind the X, mind the Y, mind the Z."
     with three distinct nouns, and across all four entries combined,
     no noun repeats, and none of the twelve collides with door, wind,
     or flame — the three words the final, oldest-known entry already
     spent. The vocabulary narrows toward the light without ever
     reusing a word it hasn't earned yet.

This checks the mechanism only. It does not say which entry is the
declared break in the pattern (rule 5's "seam must be visible, not
silent" is satisfied by this script printing it below, not by the
plaque naming it first).

Run: python verify_logbook.py
"""

import re
import sys

SIBLING_POEM = "../0030-not-mine-to-keep/poem.md"
TEMPLATE = re.compile(
    r"^mind the ([a-z]+), mind the ([a-z]+), mind the ([a-z]+)\.$"
)


def load_entries(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    text = text.split("\n", 1)[1]  # drop the title line
    blocks = [b.strip() for b in text.split("\n\n") if b.strip()]
    return blocks


def main():
    ok = True

    with open(SIBLING_POEM, encoding="utf-8") as f:
        source = f.read()

    entries = load_entries("logbook.md")
    if len(entries) != 6:
        print(f"FAIL: expected 6 entries, found {len(entries)}")
        return 1

    first_block = entries[0].split("\n")
    if len(first_block) != 2 or not first_block[0].startswith("["):
        print("FAIL: first entry should be a bracketed note plus one fragment line")
        ok = False
    oldest = first_block[-1].strip()
    newest = entries[-1].strip()

    if oldest not in source:
        print(f"FAIL: oldest line '{oldest}' is not found verbatim in {SIBLING_POEM}")
        ok = False
    else:
        print(f"OK: oldest line '{oldest}' confirmed verbatim in {SIBLING_POEM}")

    if newest not in source:
        print(f"FAIL: newest line '{newest}' is not found verbatim in {SIBLING_POEM}")
        ok = False
    else:
        print(f"OK: newest line '{newest}' confirmed verbatim in {SIBLING_POEM}")

    middle = entries[1:5]
    seen = set()
    reserved = {"door", "wind", "flame"}
    for i, line in enumerate(middle, start=2):
        m = TEMPLATE.match(line)
        if not m:
            print(f"FAIL: entry {i} does not follow the template: {line}")
            ok = False
            continue
        nouns = m.groups()
        if len(set(nouns)) != 3:
            print(f"FAIL: entry {i} repeats a noun within itself: {nouns}")
            ok = False
        for n in nouns:
            if n in seen:
                print(f"FAIL: noun '{n}' reused across entries")
                ok = False
            if n in reserved:
                print(f"FAIL: entry {i} uses a word the final entry already owns: '{n}'")
                ok = False
            seen.add(n)

    if TEMPLATE.match(oldest):
        print("FAIL: the oldest entry should break the template, not follow it")
        ok = False
    else:
        print(f"OK: the oldest entry is the declared seam - it breaks the template ('{oldest}')")

    print("PASS: all checks hold" if ok else "one or more checks failed")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

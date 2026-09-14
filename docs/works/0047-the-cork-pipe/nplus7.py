"""
N+7 (Oulipo): replace each targeted noun with the word N positions after
it in a fixed, alphabetized dictionary. Run: python nplus7.py
"""
import re

# The dictionary. 115 common nouns, hand-picked and alphabetized by the
# artist, deliberately weighted toward household and workshop objects
# rather than natural or scientific vocabulary -- that weighting is the
# whole decision this piece rests on. A different dictionary (heavier in
# nature words, or in abstractions) would push the transformed text
# somewhere else entirely; nothing about N+7 itself dictates a household
# dictionary. Includes two words absent from ordinary carpentry lists
# ("larva", "wing") because the source text needs them as targets.
DICTIONARY = sorted(set([
    "anchor", "anvil", "apron", "ash", "awl", "axle", "badge", "barrel",
    "basin", "bell", "belt", "bench", "blade", "bolt", "bottle", "brush",
    "bucket", "buckle", "cabinet", "candle", "cellar", "chain", "chest",
    "clamp", "clock", "coin", "comb", "cork", "crate", "dial", "dish",
    "door", "drain", "drawer", "dust", "fence", "file", "flask", "floor",
    "frost", "funnel", "gate", "glass", "hammer", "handle", "hinge",
    "hook", "jar", "kettle", "key", "knife", "ladder", "lamp", "larva",
    "latch", "ledge", "lever", "lid", "lock", "mat", "moth", "nail",
    "needle", "pail", "pan", "peg", "pin", "pipe", "plank", "plate",
    "rail", "rake", "ring", "rope", "rust", "saw", "scale", "screw",
    "shed", "shelf", "shovel", "sill", "sink", "spade", "spool", "spoon",
    "stair", "stake", "stall", "stove", "string", "table", "tack",
    "tank", "tap", "thread", "tile", "tin", "tool", "trap", "trough",
    "tub", "valve", "vat", "vent", "vice", "wall", "well", "wheel",
    "whistle", "wick", "window", "wing", "wire", "yoke",
]))

N = 7

# Only these exact singular tokens are replaced. Plurals, the title's
# repeated forms, and every other word in the piece are left untouched --
# a stated rule, checkable against the output by anyone willing to diff
# the two texts word for word.
TARGETS = {
    "cellar", "moth", "lamp", "wing", "dust", "shelf", "wick", "glass",
    "thread", "nail", "hinge", "drawer", "larva", "jar", "coin", "ledge",
    "ash", "floor", "frost", "scale",
}

SOURCE = """The Cellar Moth (Tinea sedentaria)

Found only in buildings with an unlit cellar and a working lamp left on
through winter, the cellar moth spends its whole life within four walls
of stone and never once meets open weather. Each wing carries a fine
coat of dust the color of the shelf it hatches beneath, so that a
specimen at rest is nearly impossible to find until it moves. The moth
is drawn not to flame itself but to the warmth carried by a nearby
wick, and will circle a lit lamp for hours without ever touching the
glass. Eggs are laid in a folded thread of old cobweb tucked behind a
loose nail or wedged into the hinge of an unused drawer; the larva
feeds on the dust of the jar it hatches near, and needs no other food
its whole short life. A coin left on a low ledge will sometimes gather
three or four eggs by spring, drawn perhaps to the residue of a hand.
The adult moth lives four days, lays once, and is gone by the second
frost, leaving behind only a scatter of ash-fine wing scale on the
floor no one sweeps."""


def shift(word):
    i = DICTIONARY.index(word)
    return DICTIONARY[(i + N) % len(DICTIONARY)]


def transform(text):
    def repl(match):
        word = match.group(0)
        low = word.lower()
        if low not in TARGETS:
            return word
        new = shift(low)
        return new[0].upper() + new[1:] if word[0].isupper() else new

    return re.sub(r"\b[A-Za-z]+\b", repl, text)


if __name__ == "__main__":
    assert DICTIONARY == sorted(DICTIONARY)
    assert len(DICTIONARY) == len(set(DICTIONARY))
    assert TARGETS <= set(DICTIONARY)

    print("=== MAPPING (word -> word, N=%d) ===" % N)
    for w in sorted(TARGETS):
        print(f"{w:8s} -> {shift(w)}")

    print("\n=== SOURCE ===\n")
    print(SOURCE)

    print("\n=== TRANSFORMED ===\n")
    print(transform(SOURCE))

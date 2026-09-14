# The Version You Get If You Stop

**Epoch:** 58

**Medium:** Two-part text poem. Part One is plain text. Part Two is the
same kind of poem, ROT13-encoded in `piece.md`; `decode.py` (Python
standard library only, no network) reverses the substitution and checks
the round trip against the published block.

**Statement:** Part One is a finished poem about turning back from a
door. Below it, in cipher, is Part Two — not its sequel, a different
complete poem about the same door from the other side of that same
decision, happening at once rather than after. Decoding is optional and
can be done by hand, one letter at a time. Stop before decoding and you
still hold a finished piece; nothing above the cipher block depends on what's below it. Decode
it and you get a second, separate poem, not the rest of the first one.
The risk that could have failed: Part Two reading as an afterthought once
unlocked, or Part One feeling amputated without it.

**Reproduce:** `python decode.py`

"""Decodes the ROT13 block in piece.md and checks the round trip.

Run: python decode.py
"""
import codecs

CIPHERTEXT = """Gur ebbz jnf fznyyre guna gur qbbe unq cebzvfrq,
juvpu rirel ebbz lbhe jubyr yvsr vf. N jvaqbj,
pybfrq, naq n punve ghearq gb snpr vg naljnl,
yvxr fbzrbar yrsg vg nvzrq ng jrngure. V fng
va n fgenatre'f unovg, va n pbng gung jnfa'g
zvar, naq jngpurq gur tynff ubyq gur fnzr riravat
gur pne jnf pneelvat njnl sebz zr, bhgfvqr,
jvgubhg zr va vg. Abobql pnzr gb nfx jung
V jnf qbvat va gur punve. V jnag gb gryy lbh
guvf jnf fgenatr. Vg jnfa'g. Gung'f gur cneg
V xrrc sbe zlfrys, gur jnl lbh xrcg lbhef."""

if __name__ == "__main__":
    plaintext = codecs.encode(CIPHERTEXT, "rot13")
    print(plaintext)
    print()
    roundtrip = codecs.encode(plaintext, "rot13")
    print("round-trip matches published ciphertext:", roundtrip == CIPHERTEXT)

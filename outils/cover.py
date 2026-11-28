#!/usr/bin/env python3
"""cover.py <source> <img/cover.jpg> [decalage]
Recadre l'image de titre d'un cours en 16:5 (1600 x 500, JPEG qualité 84).
decalage : position verticale de la bande, de 0 (haut) à 1 (bas) ; 0.5 = centré (défaut).
Pour une image récupérée par le navigateur intégré (texte base64 entre B64START et B64END dans un fichier de résultat),
passer ce fichier comme <source> : il est décodé automatiquement (la bande y est déjà recadrée)."""
import sys, re, io, base64
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
off = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
raw = open(src, "rb").read()
m = re.search(rb"B64START([A-Za-z0-9+/=\\n]+?)B64END", raw)
im = Image.open(io.BytesIO(base64.b64decode(m.group(1).replace(b"\\n", b"")))) if m else Image.open(io.BytesIO(raw))
im = im.convert("RGB")
W, H = im.size
if abs(W / H - 16 / 5) > 0.01:
    ch = round(W * 5 / 16)
    if ch <= H:
        y0 = round((H - ch) * off); im = im.crop((0, y0, W, y0 + ch))
    else:
        cw = round(H * 16 / 5); x0 = (W - cw) // 2; im = im.crop((x0, 0, x0 + cw, H))
im = im.resize((1600, 500), Image.LANCZOS)
im.save(out, "JPEG", quality=84, optimize=True, progressive=True)
print(out, im.size)

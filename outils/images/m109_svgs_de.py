"""Génère les SVG du jeu M109 (enveloppes, e-mail suspect)."""
import os
OUT = "/home/claude/m109de/img-src"
F = "file:///home/claude/modele/tools/fonts/"
STYLE = f"""<style>
@font-face{{font-family:Sora;src:url({F}sora.woff2)}}
@font-face{{font-family:Figtree;src:url({F}figtree.woff2)}}
@font-face{{font-family:JBM;src:url({F}jetbrainsmono.woff2)}}
.t{{font-family:Figtree;fill:#0f2137}}
.h{{font-family:Sora;font-weight:700;fill:#0f2137}}
.m{{font-family:JBM;fill:#56677d}}
</style>"""

ADDR = {
 "a": (None, ["EnterSite AG", "Rigistrasse 2", "5102 Rupperswil"]),
 "b": (None, ["EnterSite AG", "z. H. Reto Gugger", "Rigistrasse 2", "5102 Rupperswil"]),
 "c": (None, ["Herr Reto Gugger", "EnterSite AG", "Rigistrasse 2", "5102 Rupperswil"]),
 "d": ("Persönlich / vertraulich", ["Herr Reto Gugger", "EnterSite AG", "Rigistrasse 2", "5102 Rupperswil"]),
}

def envelope(x, y, key, label=True):
    mention, lines = ADDR[key]
    s = []
    s.append(f'<rect x="{x}" y="{y}" width="400" height="250" rx="14" fill="#fbf7ef" stroke="#c9b991" stroke-width="2"/>')
    # rabat
    s.append(f'<path d="M{x+2} {y+4} L{x+200} {y+112} L{x+398} {y+4}" fill="none" stroke="#e3d6b5" stroke-width="2"/>')
    # timbre
    s.append(f'<rect x="{x+322}" y="{y+18}" width="56" height="66" rx="4" fill="#fff" stroke="#1f5fd6" stroke-width="2" stroke-dasharray="4 3"/>')
    s.append(f'<path d="M{x+336} {y+62} l12 -16 l10 12 l8 -8 l8 12" fill="none" stroke="#1f5fd6" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')
    s.append(f'<circle cx="{x+344}" cy="{y+36}" r="5" fill="#f2a33a"/>')
    yy = y + 128
    if mention:
        s.append(f'<rect x="{x+28}" y="{y+22}" width="230" height="36" rx="6" fill="#fff" stroke="#d64545" stroke-width="2.4"/>')
        s.append(f'<text x="{x+143}" y="{y+46}" text-anchor="middle" class="h" style="fill:#d64545;font-size:17px">{mention}</text>')
    if len(lines) == 3:
        yy += 14
    for i, l in enumerate(lines):
        s.append(f'<text x="{x+120}" y="{yy + i*26}" class="t" style="font-size:19px">{l}</text>')
    if label:
        s.append(f'<circle cx="{x+40}" cy="{y+212}" r="20" fill="#0f2137"/>')
        s.append(f'<text x="{x+40}" y="{y+219}" text-anchor="middle" class="h" style="fill:#fff;font-size:20px">{key.upper()}</text>')
    return "\n".join(s)

def svg(w, h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{STYLE}<rect width="{w}" height="{h}" fill="#fff"/>{body}</svg>'

# planche des 4 enveloppes (2 x 2)
body = ['<text x="40" y="56" class="h" style="font-size:28px">Vier Adressen, vier Fälle</text>',
        '<text x="40" y="88" class="t" style="font-size:18px;fill:#56677d">Eingegangene Post im Postdienst der EnterSite AG</text>']
for i, k in enumerate("abcd"):
    x = 40 + (i % 2) * 440
    y = 116 + (i // 2) * 280
    body.append(envelope(x, y, k))
open(f"{OUT}/enveloppes.svg", "w").write(svg(920, 700, "\n".join(body)))

for k in "abcd":
    open(f"{OUT}/env_{k}.svg", "w").write(svg(440, 290, envelope(20, 20, k, label=False)))

# e-mail suspect (marque fictive)
mail = f'''
<rect x="30" y="30" width="840" height="560" rx="16" fill="#fff" stroke="#d7e1ec" stroke-width="2"/>
<rect x="30" y="30" width="840" height="56" rx="16" fill="#eef3f8"/>
<rect x="30" y="70" width="840" height="16" fill="#eef3f8"/>
<circle cx="62" cy="58" r="7" fill="#d64545"/><circle cx="84" cy="58" r="7" fill="#f2a33a"/><circle cx="106" cy="58" r="7" fill="#2bb673"/>
<text x="140" y="64" class="m" style="font-size:16px">Posteingang</text>
<text x="60" y="126" class="m" style="font-size:17px">Von:</text>
<text x="150" y="126" class="t" style="font-size:18px">Lieferdienst PaketRapid &lt;support@paketrapid-zustellung.xyz&gt;</text>
<text x="60" y="158" class="m" style="font-size:17px">An:</text>
<text x="150" y="158" class="t" style="font-size:18px">reception@entersite.ch</text>
<text x="60" y="190" class="m" style="font-size:17px">Betreff:</text>
<text x="150" y="190" class="h" style="font-size:19px">DRINGEND: Ihr Paket ist blockiert!!!</text>
<line x1="60" y1="214" x2="840" y2="214" stroke="#d7e1ec" stroke-width="2"/>
<text x="60" y="254" class="t" style="font-size:19px">Lieber Kunde,</text>
<text x="60" y="290" class="t" style="font-size:19px">Ihr Paket kann nicht zugestellt werden, weil die Zollgebühren von CHF 2.99</text>
<text x="60" y="318" class="t" style="font-size:19px">nicht bezahlt wurde. Ohne Zahlung innert 24 Stunden wird es vernichtet.</text>
<text x="60" y="354" class="t" style="font-size:19px">Bestätigen Sie hier Ihre Angaben und Ihre Kreditkarte:</text>
<rect x="60" y="378" width="330" height="54" rx="10" fill="#1f5fd6"/>
<text x="225" y="412" text-anchor="middle" class="h" style="fill:#fff;font-size:19px">Jetzt bezahlen</text>
<text x="60" y="462" class="m" style="font-size:15px">Link: http://paketrapid-zahlung.top/ch/login</text>
<text x="60" y="510" class="t" style="font-size:19px">Vielen Dank für Ihr Vertrauen,</text>
<text x="60" y="538" class="t" style="font-size:19px">Ihr PaketRapid-Team</text>
'''
open(f"{OUT}/email_suspect.svg", "w").write(svg(900, 640, mail))
print(sorted(os.listdir(OUT)))

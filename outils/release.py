#!/usr/bin/env python3
"""release.py VERSION "ligne de changelog" [motifs exclus…] : met à jour le tableau des jeux du README, readme.txt
(Stable tag, changelog) et la version de l'extension (en-tête et JRL_VERSION), puis commit + push sur main.
Le workflow GitHub « Publier une version » crée alors la release vVERSION avec le zip : les sites proposent la mise à jour.
Version : mineure (2.29.0 → 2.30.0) pour un nouveau jeu ou une fonction, corrective (2.29.1) pour une correction."""
import json, glob, os, re, sys, subprocess
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ver, log = sys.argv[1], sys.argv[2]
excl = sys.argv[3:]  # motifs exclus, ex. jeux/m3*
jeux = []
for f in sorted(glob.glob(R + '/jeux/*/jeu.json')):
    j = json.load(open(f, encoding='utf-8'))
    m = re.search(r'(\d+) (?:objectifs?|modules?).*? et (\d+) épreuves', j['description'])
    titre = j['titre'].split(' – ', 1)[1]
    jeux.append((j['module'], titre, j['shortcode'], m.group(1), m.group(2)))
jeux.sort(key=lambda x: (0, int(x[0][1:])) if x[0][1:].isdigit() else (1, x[0]))
n = len(jeux)
mods = sorted({j[0][:2] for j in jeux})
rng = f"{jeux[0][0]} à {jeux[-1][0]}"
groupes = {}
for mod, *_ in jeux:
    groupes.setdefault(mod[1] if mod[1:].isdigit() else mod, []).append(mod)
gtxt = ', '.join(('mathématiques 1 à 8' if v[0] == 'MATHS' else f"{v[0]} à {v[-1]}") if len(v) > 1 else ('mathématiques 4 à 8' if v[0] == 'MATHS' else v[0]) for v in groupes.values())

md = open(R + '/README.md', encoding='utf-8').read()
md = re.sub(r'- \*\*\d+ jeux\*\* \(modules [^)]*\)', f'- **{n} jeux** (modules {gtxt})', md)
md = re.sub(r'\| Les modules M101 à M110 \([^|]*\) \|', '| Les modules M101 à M110 (`M2` pour M201 à M209, `M3` pour M301 à M312) |', md)
lines = md.split('\n')
i = lines.index('| Module | Jeu | Shortcode | Objectifs | Épreuves |')
k = i + 2
while k < len(lines) and lines[k].startswith('| M'):
    k += 1
rows = [f"| {a} | {b} | `[{c}]` | {d} | {e} |" for a, b, c, d, e in jeux]
lines[i + 2:k] = rows
open(R + '/README.md', 'w', encoding='utf-8').write('\n'.join(lines))

p = R + '/jeux-revisions-logistique.php'
s = open(p, encoding='utf-8').read()
s = re.sub(r'(\* Version:\s+)[\d.]+', r'\g<1>' + ver, s)
s = re.sub(r"define\( 'JRL_VERSION', '[\d.]+' \)", f"define( 'JRL_VERSION', '{ver}' )", s)
open(p, 'w', encoding='utf-8').write(s)

t = open(R + '/readme.txt', encoding='utf-8').read()
t = re.sub(r'Stable tag: [\d.]+', 'Stable tag: ' + ver, t)
t = re.sub(r'\(\d+ jeux, modules [^)]*\)', f'({n} jeux, modules {gtxt})', t)
if f'= {ver} =' not in t:
    t = t.replace('== Changelog ==\n\n', f'== Changelog ==\n\n= {ver} =\n* {log}\n\n', 1)
open(R + '/readme.txt', 'w', encoding='utf-8').write(t)

msg = f"Version {ver} : {log}" + (("\n\n" + os.environ["ATTRIBUTION"]) if os.environ.get("ATTRIBUTION") else "")  # lignes d'attribution de la session (variable ATTRIBUTION)
subprocess.run(['git', '-C', R, 'add', '-A', '--', '.'] + [':!' + e for e in excl], check=True)
subprocess.run(['git', '-C', R, 'commit', '-q', '-m', msg], check=True)
subprocess.run(['git', '-C', R, 'push', '-q', 'origin', 'main'], check=True)
print(n, 'jeux,', gtxt, '→ poussé', ver)

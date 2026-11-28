#!/usr/bin/env python3
"""traduire.py : versions allemande et italienne d'un jeu de LogiPlay (mêmes épreuves, même progression).

  python3 outils/traduire.py feuille <slug> <dossier_de_travail>
      → <travail>/<slug>.fr : feuille complète « N|texte » ; <travail>/<slug>.a-traduire : seulement les lignes
        qui contiennent des mots (les nombres et unités seuls restent tels quels).
  Écrire ensuite <travail>/<slug>.de et <travail>/<slug>.it : une ligne « N|traduction » par ligne de .a-traduire
  (mêmes numéros ; une ligne non fournie reste en français, une ligne avec des mots manquante bloque).
  python3 outils/traduire.py construire <slug> <de|it> <dossier_de_travail>
      → data.<lg>.js, clé <lg> de jeu.json, index.<lg>.html (moteur traduit par langues.py), calculatrice remise
        si le jeu en a une, mode visiteur réappliqué. Heures d'horloge « 08 h 45 » → « 08:45 » ; TVA → MWST / IVA.

Conventions : vouvoiement (Sie / Lei) ; DE : orthographe suisse (ss), « Nicht im Kursmaterial · Ergänzung » pour
« Hors support », Logistiker/-in EFZ, MWST, Rampe, Kommissionierer ; IT : « non nel materiale del corso »,
Impiegato/a in logistica AFC, IVA, Metta in ordine / Abbini / Classifichi / Trovi l'intruso.
"""
import sys, os, re, subprocess

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, R + '/outils')
MOT = r'[A-Za-zÀ-ÖØ-öø-ÿ]'
UNITES = r'\b(CHF|km/h|m/s|N/kg|km|hm|dam|dm|cm|mm|m|kg|hg|dag|g|mg|t|q|N|kN|daN|L|l|ml|h|min|s|EUR|ISO|GS1|EAN|SSCC|D|V|T|F)(²|³)?(?![A-Za-zÀ-ÖØ-öø-ÿ])'

def a_traduire(t): return bool(re.search(MOT, re.sub(UNITES, '', t)))

cmd = sys.argv[1]
if cmd == 'feuille':
    slug, w = sys.argv[2], sys.argv[3]; os.makedirs(w, exist_ok=True)
    out = subprocess.check_output(['node', R + '/outils/traduction.js', 'feuille', f'{R}/jeux/{slug}', 'x', 'it']).decode()
    open(f'{w}/{slug}.fr', 'w').write(out)
    todo = [l for l in out.splitlines() if '|' in l and a_traduire(l.split('|', 1)[1])]
    open(f'{w}/{slug}.a-traduire', 'w').write('\n'.join(todo) + '\n')
    print(f'{len(out.splitlines())} lignes, {len(todo)} à traduire → {w}/{slug}.a-traduire')
elif cmd == 'construire':
    slug, lg, w = sys.argv[2], sys.argv[3], sys.argv[4]; D = f'{R}/jeux/{slug}'
    src = [l.split('|', 1) for l in open(f'{w}/{slug}.fr').read().splitlines() if '|' in l]
    tr = {}
    for l in open(f'{w}/{slug}.{lg}').read().splitlines():
        if '|' in l: n, t = l.split('|', 1); tr[n.strip()] = t.strip()
    miss = [n for n, t in src if n not in tr and a_traduire(t)]
    extra = sorted(set(tr) - {n for n, _ in src})
    if miss or extra: sys.exit(f'MANQUANT {miss[:40]}  EN TROP {extra[:20]}')
    tva = {'de': 'MWST', 'it': 'IVA'}[lg]; out = []
    for n, t in src:
        x = tr.get(n, t.replace('TVA', tva))
        x = re.sub(r'\b(\d{2}) h (\d{2})\b', r'\1:\2', x)
        out.append(f'{n}|{x}')
    open(f'{w}/{slug}.{lg}.full', 'w').write('\n'.join(out) + '\n')
    r = subprocess.run(['node', R + '/outils/traduction.js', 'construire', D, f'{w}/{slug}.{lg}.full', lg], capture_output=True, text=True)
    print(r.stdout.strip()[-600:], r.stderr.strip()[-600:])
    if r.returncode: sys.exit(1)
    import json, langues
    titre = json.loads('"' + re.search(r'"title":"((?:[^"\\]|\\.)*)"', open(f'{D}/data.{lg}.js').read()).group(1) + '"')
    fr = langues.patch_fr(open(D + '/index.html').read()); open(D + '/index.html', 'w').write(fr)
    open(f'{D}/index.{lg}.html', 'w').write(langues.make_lang(fr.replace('<script src="calc.js" defer></script>', ''), titre, lg))
    subprocess.run(['python3', R + '/outils/visiteurs.py', D], check=True)
    if os.path.exists(D + '/calc.js'): subprocess.run(['python3', R + '/outils/calculatrice/ajouter.py', D], check=True)
    print(f'index.{lg}.html : {titre}')
else:
    sys.exit(__doc__)

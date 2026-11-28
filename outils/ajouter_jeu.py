#!/usr/bin/env python3
"""ajouter_jeu.py <dossier_travail> <slug> <module> <shortcode> "<sous-titre>" "<précision description>" [logo.svg]

Range un jeu terminé (data.js + img/ avec cover.jpg, vérifié par check.js) dans jeux/<slug>/ de LogiPlay :
- index.html = moteur d'un jeu DÉJÀ dans le dépôt (jamais celui du Modèle logistique : le moteur du dépôt contient
  en plus le menu FR · DE · IT, le mode visiteur et les chemins de polices ../../assets/fonts) ; seul <title> change ;
- data.js, img/ (sans img-src), index.php dans chaque dossier, jeu.json généré depuis data.js ;
- logo.svg : celui fourni, sinon pictogramme de la première icône de l'objectif 1 sur le gabarit LogiOne.

Exemple : python3 outils/ajouter_jeu.py ~/m605 m605-reception M605 jeu_m605 "Logisticien·ne CFC · Module M605" "leçons 1.1 à 3.2"
Ensuite : traduire.py (de puis it), calculatrice/ajouter.py si le jeu demande des calculs, release.py.
"""
import sys, os, re, json, shutil, subprocess, html, glob

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src, slug, module, shortcode, sous_titre, precision = sys.argv[1:7]
logo = sys.argv[7] if len(sys.argv) > 7 else ''
dst = f'{R}/jeux/{slug}'

chk = subprocess.run(['node', f'{R}/outils/check.js', src], capture_output=True, text=True).stdout.strip()
if not chk.endswith('OK'): print(chk); sys.exit('check.js doit finir par OK')

dump = r'''global.window={};require(process.argv[1]);const O=window.OBJ,M=window.META;
console.log(JSON.stringify({title:M.title,icons:M.icons||{},obj:O.map(o=>({code:o.code,t:o.t,g:o.g,ic:o.ic,n:o.ch.length,cases:o.ch.filter(c=>c.k==="case").length}))}))'''
d = json.loads(subprocess.check_output(['node', '-e', dump, os.path.abspath(src + '/data.js')]))

ref = sorted(glob.glob(f'{R}/jeux/m10*/index.html'))[0]
eng = open(ref, encoding='utf-8').read()
eng = re.sub(r'<title>.*?</title>', '<title>' + html.escape(d['title'], quote=False) + '</title>', eng, count=1, flags=re.S)
eng = eng.replace('<script src="calc.js" defer></script>', '')
os.makedirs(dst + '/img', exist_ok=True)
open(dst + '/index.html', 'w', encoding='utf-8').write(eng)
shutil.copy(src + '/data.js', dst + '/data.js')
for f in glob.glob(src + '/img/*'):
    if os.path.isfile(f): shutil.copy(f, dst + '/img/')

if logo:
    shutil.copy(logo, dst + '/logo.svg')
elif not os.path.exists(dst + '/logo.svg'):
    ic = d['obj'][0]['ic']; isvg = d['icons'].get(ic, '')
    if not isvg:
        m = re.search(re.escape(ic) + r':`(.*?)`,', eng)
        isvg = m.group(1).replace('${P}', 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"') if m else ''
    inner = isvg.replace('stroke-width="2"', 'stroke-width="1.7"').replace('currentColor', '#ffffff')
    open(dst + '/logo.svg', 'w').write(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256">
  <defs><clipPath id="r"><rect width="256" height="256" rx="40"/></clipPath></defs>
  <g clip-path="url(#r)"><rect width="256" height="256" fill="#313a45"/><rect width="256" height="16" fill="#067030"/></g>
  <g transform="translate(48 52) scale(6.6)">{inner}</g>
  <rect x="186" y="186" width="34" height="34" rx="6" fill="#f5c400"/>
  <rect x="146" y="196" width="30" height="24" rx="5" fill="#2fae5f"/>
</svg>
''')

objs = d['obj']; n = sum(o['n'] for o in objs); cases = sum(o['cases'] for o in objs)
j = {'module': module, 'shortcode': shortcode, 'titre': d['title'], 'sous_titre': sous_titre, 'duree': '10 min par série',
     # « N objectifs … et N épreuves » : release.py lit ces deux nombres pour le tableau du README
     'description': f"{len(objs)} objectifs ({precision}) et {n} épreuves, dont {round(100 * cases / n)} % de mises en situation du métier. "
                    'Trois modes : Entraînement par objectif, Examen blanc chronométré noté sur 6 et Révision ciblée des erreurs.',
     'contenu': [{'titre': o['code'] + ' · ' + o['t'], 'objectifs': [o['g']]} for o in objs], 'couleur': '#067030', 'version': '1.0.0'}
json.dump(j, open(dst + '/jeu.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for root, dirs, files in os.walk(dst):
    if 'index.php' not in files: open(os.path.join(root, 'index.php'), 'w').write('<?php // Silence is golden.\n')
subprocess.run(['python3', f'{R}/outils/visiteurs.py', dst], check=True)
print(f'{slug} : {len(objs)} objectifs, {n} épreuves, {round(100 * cases / n)} % de cas → {dst}')

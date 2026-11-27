#!/usr/bin/env python3
"""Ajoute la calculatrice LogiPlay à un jeu : copie calc.js et l'appelle dans index.html, index.de.html, index.it.html.
Usage : python3 outils/calculatrice/ajouter.py jeux/<slug> [...]  (sans effet si déjà fait ; à relancer après une nouvelle traduction)."""
import sys, os, shutil
ici = os.path.dirname(os.path.abspath(__file__))
TAG = '<script src="calc.js" defer></script>'
for d in sys.argv[1:]:
    shutil.copy(os.path.join(ici, 'calc.js'), os.path.join(d, 'calc.js'))
    for f in ('index.html', 'index.de.html', 'index.it.html'):
        p = os.path.join(d, f)
        if not os.path.exists(p):
            continue
        s = open(p, encoding='utf-8').read()
        if TAG in s:
            continue
        i = s.lower().rfind('</body>')
        s = s[:i] + TAG + s[i:] if i >= 0 else s + TAG
        open(p, 'w', encoding='utf-8').write(s)
        print('calculatrice ajoutée :', p)

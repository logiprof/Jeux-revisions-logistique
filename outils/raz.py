#!/usr/bin/env python3
"""Remise à zéro par l'administration (version 2.11.0) : si la progression du site porte une marque « raz »
différente de celle de l'appareil, le jeu oublie sa copie locale et repart de la progression du site.
  python3 outils/raz.py jeux/*/index.html   puis   python3 outils/langues.py tous"""
import sys
A = 'if(rem&&rem.state&&(rem.state.xp||0)>=(S.xp||0))adoptRemote(rem);'
B = 'if(rem&&rem.state&&((rem.state.raz&&rem.state.raz!==S.raz)||(rem.state.xp||0)>=(S.xp||0)))adoptRemote(rem);'
for p in sys.argv[1:]:
    s = open(p, encoding='utf-8').read()
    if B in s: continue
    assert s.count(A) == 1, p
    open(p, 'w', encoding='utf-8').write(s.replace(A, B))
print('ok', len(sys.argv) - 1)

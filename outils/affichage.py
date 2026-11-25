#!/usr/bin/env python3
"""Affichage sur ordinateur et liste des objectifs (version 2.7.0).

  python3 outils/affichage.py <index.html> [...]   modifie le moteur français (idempotent)

- Liste « Objectifs du chapitre » : une puce de couleur et un objectif par ligne, sur toute la largeur.
- Ordinateur (souris, écran d'au moins 900 px) : plein écran au premier « Commencer » / « Reprendre »,
  bouton « Plein écran » / « Quitter le plein écran » dans la barre du haut.
- Grand écran (1100 px et plus) : page plus large (1180 px), accueil sur toute la largeur, réponses sur deux colonnes.
Ensuite : python3 outils/langues.py tous   (régénère les index.de.html).
"""
import sys

MARQUE = '/* affichage-ordinateur 2.7 */'

CSS = MARQUE + r"""
.olist{display:flex;flex-direction:column;background:var(--panel);border:1px solid var(--line);border-radius:6px;overflow:hidden}
.orow{display:grid;grid-template-columns:12px minmax(0,1fr) auto 16px;gap:14px;align-items:center;width:100%;text-align:left;padding:14px 18px;background:none;border:0;border-top:1px solid var(--line);border-radius:0;color:inherit;font:inherit;cursor:pointer;transition:background .12s}
.orow:first-child{border-top:0}
.orow:hover{background:color-mix(in srgb,var(--c) 8%,var(--panel))}
.orow:focus-visible{outline:3px solid var(--y);outline-offset:-3px}
.orow .dot{width:12px;height:12px;border-radius:50%;background:var(--c);align-self:start;margin-top:7px}
.orow .ohead{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}
.orow .code{font-family:var(--mono);font-size:.74rem;font-weight:700;color:var(--c);letter-spacing:.06em}
.orow .ot{font-weight:600;font-size:1.02rem;line-height:1.3}
.orow .goal{display:block;margin-top:3px;font-size:.84rem;color:var(--muted);line-height:1.4}
.orow .ost{display:flex;align-items:center;gap:10px;white-space:nowrap}
.orow .obar{width:90px;height:6px;border-radius:99px;background:var(--line);overflow:hidden}
.orow .obar i{display:block;height:100%;background:var(--c);border-radius:99px}
.orow .onb{font-size:.78rem}
.orow .chev{color:var(--muted);font-size:1.5rem;line-height:1}
@media (max-width:700px){.orow{grid-template-columns:12px minmax(0,1fr) 14px;padding:13px 14px;gap:12px}.orow .ost{grid-column:2;flex-wrap:wrap;white-space:normal}.orow .chev{grid-column:3;grid-row:1}.orow .obar{width:70px}}
@media (min-width:1100px){
.wrap{max-width:1180px}
.welcome{max-width:none;width:100%;margin-top:2vh}
.welcome .cover{max-height:38vh}
.welcome h1{font-size:clamp(2.4rem,3.4vw,3.2rem)}
.welcome .wtext{max-width:760px}
.welcome .wtext>.muted{font-size:1.05rem}
.welcome .art{width:190px}
.card{padding:28px 32px}
.card .q{font-size:1.2rem}
.opts{grid-template-columns:repeat(2,minmax(0,1fr))}
.opt{min-height:64px;align-items:center}
}
"""

JS = r"""/* plein écran (ordinateur) */
ICONS.fsin='<path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>';
ICONS.fsout='<path d="M9 4v5H4M15 4v5h5M9 20v-5H4M15 20v-5h5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>';
function fsPar(){try{if(window.parent!==window&&window.parent.document&&window.parent.document.querySelector(".jdr-overlay"))return window.parent.document}catch(e){}return null}
function fsEl(){const p=fsPar();return (p&&(p.fullscreenElement||p.webkitFullscreenElement))||document.fullscreenElement||document.webkitFullscreenElement||null}
function fsOk(){const d=fsPar()||document;return matchMedia("(pointer:fine) and (min-width:900px)").matches&&!!(d.fullscreenEnabled||d.webkitFullscreenEnabled||document.fullscreenEnabled||document.webkitFullscreenEnabled)}
function fsReq(el){const fn=el&&(el.requestFullscreen||el.webkitRequestFullscreen);if(!fn)return Promise.reject();try{const r=fn.call(el);return r&&r.then?r:Promise.resolve()}catch(e){return Promise.reject(e)}}
function fsOn(){const p=fsPar(),own=document.documentElement;(p?fsReq(p.querySelector(".jdr-overlay")):Promise.reject()).catch(()=>fsReq(own)).catch(()=>{})}
function fsOff(){const p=fsPar(),d=p&&(p.fullscreenElement||p.webkitFullscreenElement)?p:document,fn=d.exitFullscreen||d.webkitExitFullscreen;if(fn)try{const r=fn.call(d);if(r&&r.catch)r.catch(()=>{})}catch(e){}}
function fsAuto(){if(fsOk()&&!fsEl())fsOn()}
function fsLabel(){return fsEl()?"Quitter le plein écran":"Plein écran"}
function fsBtn(){return fsOk()?`<button type="button" class="chip btnchip" id="fs">${ic(fsEl()?"fsout":"fsin")}${fsLabel()}</button>`:""}
function fsSync(){const b=$("#fs");if(b)b.innerHTML=`${ic(fsEl()?"fsout":"fsin")}${fsLabel()}`}
["fullscreenchange","webkitfullscreenchange"].forEach(ev=>{document.addEventListener(ev,fsSync);const p=fsPar();if(p)p.addEventListener(ev,fsSync)});

function topBar(){"""

TRAY_OLD = '''  <section class="tray">${OBJ.map((o,oi)=>{const p=mastery(oi),s=statusOf(p);return `<button class="vial" type="button" data-o="${oi}" style="--c:${cv(o)}">
    <span class="cap">${capSVG(p,o)}<span class="lid">${ic(o.ic)}</span></span>
    <span style="min-width:0"><span class="code">${esc(o.code)}</span><h3>${esc(o.t)}</h3><span class="goal">${esc(o.g)}</span>
    <span class="foot"><span class="status st${s}">${STATUS[s]}</span><span class="pct">${p} %</span><span class="muted" style="font-size:.8rem">${masteredCount(oi)}/${o.ch.length} épreuves</span></span></span></button>`}).join("")}</section>'''
TRAY_NEW = '''  <section class="olist">${OBJ.map((o,oi)=>{const p=mastery(oi),s=statusOf(p);return `<button class="orow" type="button" data-o="${oi}" style="--c:${cv(o)}">
    <span class="dot" aria-hidden="true"></span>
    <span style="min-width:0"><span class="ohead"><span class="code">${esc(o.code)}</span><span class="ot">${esc(o.t)}</span></span><span class="goal">${esc(o.g)}</span></span>
    <span class="ost"><span class="status st${s}">${STATUS[s]}</span><span class="obar"><i style="width:${p}%"></i></span><span class="pct">${p} %</span><span class="muted onb">${masteredCount(oi)}/${o.ch.length} épreuves</span></span>
    <span class="chev" aria-hidden="true">›</span></button>`}).join("")}</section>'''

REMPL = [
    (TRAY_OLD, TRAY_NEW, 1),
    ('$$(".vial").forEach(b=>b.addEventListener("click",()=>{sTap();startTrain(+b.dataset.o)}));',
     '$$(".orow").forEach(b=>b.addEventListener("click",()=>{sTap();startTrain(+b.dataset.o)}));', 1),
    ('${langBtn()}', '${langBtn()}${fsBtn()}', 3),
    ('function bindTop(){', 'function bindTop(){const fb=$("#fs");if(fb)fb.addEventListener("click",()=>{if(fsEl())fsOff();else fsOn()});', 1),
    ('$("#go").addEventListener("click",()=>{sTap();home()})', '$("#go").addEventListener("click",()=>{sTap();fsAuto();home()})', 1),
    ('$("#fstart").addEventListener("submit",e=>{e.preventDefault();', '$("#fstart").addEventListener("submit",e=>{e.preventDefault();fsAuto();', 1),
    ('\nfunction topBar(){', '\n' + JS, 1),
]


def patch(s):
    if MARQUE in s:
        return s
    for a, b, n in REMPL:
        c = s.count(a)
        assert c == n, f"ancre trouvée {c} fois au lieu de {n} : {a[:70]}"
        s = s.replace(a, b)
    i = s.index('.welcome .cover{')
    j = s.index('</style>', i)
    return s[:j] + '\n' + CSS + s[j:]


if __name__ == '__main__':
    for p in sys.argv[1:]:
        s = open(p, encoding='utf-8').read()
        open(p, 'w', encoding='utf-8').write(patch(s))
    print('ok', len(sys.argv) - 1)

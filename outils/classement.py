#!/usr/bin/env python3
"""Bouton « Classement » du groupe Sensei dans le tableau de bord du jeu (version 2.12.0).
  python3 outils/classement.py jeux/*/index.html   puis   python3 outils/langues.py tous
Le classement vient du site (REST jdr/v1/classement/<jeu>) ; hors du site, rien n'est affiché."""
import sys

MARQUE = '/* classement-groupe 2.12 */'

CSS = MARQUE + r"""
.rk{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:14px;align-items:center;padding:14px 18px;border-top:6px solid var(--y)}
.rk .rki{width:44px;height:44px;border-radius:8px;background:var(--y);color:#313a45;display:grid;place-items:center}
.rk .rki .ico{width:24px;height:24px}
.rk b{display:block;font-size:1.02rem}
.rk small{color:var(--muted)}
@media (max-width:560px){.rk{grid-template-columns:auto minmax(0,1fr)}.rk .btn{grid-column:1 / -1}}
.rkm{position:fixed;inset:0;z-index:60;background:rgba(20,26,33,.55);display:grid;place-items:center;padding:16px}
.rkbox{background:var(--panel);color:var(--ink);border-radius:8px;width:min(560px,100%);max-height:min(86vh,760px);display:flex;flex-direction:column;box-shadow:0 20px 60px rgba(0,0,0,.35);overflow:hidden}
.rkhead{background:var(--ink-hero);color:#fff;padding:16px 18px;display:flex;flex-direction:column;gap:10px}
.rkhead h2{margin:0;color:#fff;font-size:1.25rem}
.rkhead select{font:inherit;font-size:16px;border-radius:6px;padding:4px 8px;max-width:100%}
.rkseg{display:flex;gap:6px;flex-wrap:wrap}
.rkseg button{font:inherit;font-weight:600;font-size:.88rem;border-radius:99px;padding:5px 12px;border:1px solid rgba(255,255,255,.35);background:transparent;color:#fff;cursor:pointer}
.rkseg button[aria-pressed="true"]{background:var(--y);color:#313a45;border-color:var(--y)}
.rklist{list-style:none;margin:0;padding:8px 10px;overflow:auto;flex:1}
.rklist li{display:grid;grid-template-columns:52px minmax(0,1fr) auto;gap:10px;align-items:center;padding:9px 10px;border-radius:6px}
.rklist li:nth-child(odd){background:var(--panel2)}
.rklist li.me{background:color-mix(in srgb,var(--accent) 16%,var(--panel));font-weight:700}
.rklist .rkr{font-family:var(--mono);font-weight:700}
.rklist li.r1 .rkr{color:#b38f00}.rklist li.r2 .rkr{color:#7d8791}.rklist li.r3 .rkr{color:#a8682f}
.rklist .rkp{font-family:var(--mono);font-variant-numeric:tabular-nums}
.rkvide{padding:18px;color:var(--muted)}
.rkfoot{display:flex;justify-content:space-between;gap:10px;align-items:center;padding:12px 18px;border-top:1px solid var(--line)}
.rkfoot small{color:var(--muted)}
"""

JS = r"""/* classement du groupe Sensei (site seulement) */
ICONS.trophy='<path d="M8 4h8v5a4 4 0 0 1-8 0V4zM8 6H5v1a3 3 0 0 0 3 3M16 6h3v1a3 3 0 0 1-3 3M12 13v4M8.5 20h7M10 17h4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>';
const RKS={per:"semaine",scope:"jeu",g:0,d:null};
function rkOrd(n){return n===1?"1er":n+"e"}
async function rkGet(g){const u=WP.rest+"classement/"+encodeURIComponent(WP.jeu)+(g?"?groupe="+encodeURIComponent(g):"");const r=await fetch(u,{credentials:"same-origin",cache:"no-store",headers:{"X-WP-Nonce":WP.nonce}});if(!r.ok)throw r.status;return r.json()}
async function rkInit(){const el=$("#rk");if(!el||!WP||!WPU)return;
  try{const d=await rkGet(RKS.g);RKS.d=d;if(d.off||!d.groupes||!d.groupes.length||!$("#rk"))return;RKS.g=d.groupe;
    const me=(d.semaine.jeu||[]).find(x=>x.m&&x.p>0);
    el.innerHTML=`<span class="rki">${ic("trophy")}</span><div><b>Classement de votre groupe</b><small>${me?`Cette semaine sur ce jeu : ${rkOrd(me.r)} · ${me.p} XP`:"Pas encore de points cette semaine sur ce jeu."}</small></div><button class="btn y small" id="rkopen" type="button">Voir le classement</button>`;
    el.hidden=false;$("#rkopen").addEventListener("click",()=>{sTap();rkOpen()})}catch(e){}}
function rkKey(e){if(e.key==="Escape"){e.stopImmediatePropagation();e.preventDefault();rkClose()}}
function rkClose(){const m=$("#rkm");if(m)m.remove();document.removeEventListener("keydown",rkKey,true);const b=$("#rkopen");if(b)b.focus()}
function rkOpen(){rkClose();const m=document.createElement("div");m.id="rkm";m.className="rkm";m.setAttribute("role","dialog");m.setAttribute("aria-modal","true");
  m.addEventListener("click",e=>{if(e.target===m)rkClose()});document.body.appendChild(m);document.addEventListener("keydown",rkKey,true);rkDraw()}
function rkDraw(){const m=$("#rkm"),d=RKS.d;if(!m||!d)return;const l=((d[RKS.per]||{})[RKS.scope])||[],gs=d.groupes||[];
  const seg=(k,v,t)=>`<button type="button" data-k="${k}" data-v="${v}" aria-pressed="${RKS[k]===v}">${t}</button>`;
  m.innerHTML=`<div class="rkbox"><div class="rkhead"><h2>Classement</h2>
   ${gs.length>1?`<label>Groupe <select id="rkg">${gs.map(g=>`<option value="${g.id}"${g.id===RKS.g?" selected":""}>${esc(g.nom)}</option>`).join("")}</select></label>`:`<span>${esc((gs[0]||{}).nom||"")}</span>`}
   <div class="rkseg">${seg("per","semaine","Cette semaine")}${seg("per","total","Depuis le début")}</div>
   <div class="rkseg">${seg("scope","jeu","Ce jeu")}${seg("scope","tous","Tous les jeux")}</div></div>
   ${l.some(x=>x.p>0)?`<ol class="rklist">${l.map(x=>`<li class="${x.m?"me ":""}${x.r&&x.r<4?"r"+x.r:""}"><span class="rkr">${x.p>0?rkOrd(x.r):"–"}</span><span>${esc(x.n)}${x.m?" (vous)":""}</span><span class="rkp">${x.p} XP</span></li>`).join("")}</ol>`:`<p class="rkvide">Personne n'a encore de points ici.</p>`}
   <div class="rkfoot"><small>XP gagnés dans les jeux de révision</small><button class="btn small" id="rkx" type="button">Fermer</button></div></div>`;
  $$("#rkm .rkseg button").forEach(b=>b.addEventListener("click",()=>{RKS[b.dataset.k]=b.dataset.v;rkDraw()}));
  const sel=$("#rkg");if(sel)sel.addEventListener("change",async()=>{RKS.g=+sel.value;try{RKS.d=await rkGet(RKS.g)}catch(e){}rkDraw()});
  $("#rkx").addEventListener("click",rkClose);$("#rkx").focus()}

function topBar(){"""

REMPL = [
    ('\nfunction topBar(){', '\n' + JS, 1),
    ('  <div class="sect" id="objs">', '  ${WPU?`<section class="panel rk" id="rk" hidden></section>`:""}\n  <div class="sect" id="objs">', 1),
    ('  bindTop();\n  if($("#frest"))', '  bindTop();rkInit();\n  if($("#frest"))', 1),
]


def patch(s):
    if MARQUE in s:
        return s
    for a, b, n in REMPL:
        c = s.count(a)
        assert c == n, f"ancre trouvée {c} fois au lieu de {n} : {a[:60]}"
        s = s.replace(a, b)
    i = s.index('/* affichage-ordinateur 2.7 */')
    j = s.index('</style>', i)
    return s[:j] + '\n' + CSS + s[j:]


if __name__ == '__main__':
    for p in sys.argv[1:]:
        s = open(p, encoding='utf-8').read()
        open(p, 'w', encoding='utf-8').write(patch(s))
    print('ok', len(sys.argv) - 1)

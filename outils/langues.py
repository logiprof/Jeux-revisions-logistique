#!/usr/bin/env python3
"""langues.py : moteur de jeu multilingue français / allemand / italien (menu FR · DE · IT).

  python3 outils/langues.py moteur <index.html>     ajoute au moteur français le bouton FR | DE (idempotent)
  python3 outils/langues.py de <index.html> <titre> écrit index.de.html à côté (moteur allemand généré)
  python3 outils/langues.py tous                    les deux opérations pour chaque jeu de jeux/ qui a un data.de.js

Le moteur allemand est généré à partir du moteur français par remplacement de textes : une seule source à corriger.
Les deux moteurs utilisent la même clé de progression (META.key) et le même identifiant de jeu : la progression
de l'élève est la même dans les deux langues. La langue choisie est retenue dans localStorage (« jdr-lang »).
Sur le site, la page du jeu reçoit ?lang=de ; hors du site, le bouton ouvre index.de.html ou index.html.
"""
import sys, os, re, glob, html

# ---------------------------------------------------------------- moteur français : bouton de langue
LANG_JS = r'''document.title=META.title;
/* ---------- langue (FR / DE / IT) : même jeu, même progression ---------- */
const LANG="fr";
const LNAMES={fr:"Français",de:"Deutsch",it:"Italiano"};
const LANGS=Array.isArray(META.langs)?META.langs.filter(l=>LNAMES[l]):[];
const HAS_DE=LANGS.length>1&&LANGS.indexOf("fr")>=0;
const LQ=(()=>{try{return new URLSearchParams(location.search).get("lang")}catch(e){return null}})();
const LPREF=(()=>{try{return localStorage.getItem("jdr-lang")}catch(e){return null}})();
const LREDIR=HAS_DE&&!LQ&&LANGS.indexOf(LPREF)>=0&&LPREF!==LANG;
function goLang(l){try{localStorage.setItem("jdr-lang",l)}catch(e){}
  const go=()=>{try{const u=new URL(location.href);u.searchParams.set("lang",l);if(!window.JDR_CFG)u.pathname=u.pathname.replace(/[^\/]*$/,l==="fr"?"index.html":"index."+l+".html");location.replace(u.href)}catch(e){location.reload()}};
  try{Promise.race([cloudFlush(),new Promise(r=>setTimeout(r,1500))]).then(go,go)}catch(e){go()}}
function langBtn(){if(!HAS_DE)return"";return `<span class="langwrap"><button type="button" class="chip btnchip langsw" id="lang" aria-haspopup="true" aria-expanded="false" title="Langue">${ic("globe")}${LANG.toUpperCase()}</button><span class="langmenu" hidden>${LANGS.map(l=>`<button type="button" class="langopt${l===LANG?" on":""}" data-l="${l}" lang="${l}"><b>${l.toUpperCase()}</b>${LNAMES[l]}</button>`).join("")}</span></span>`}
function bindLang(){document.querySelectorAll(".langwrap").forEach(w=>{const lg=w.querySelector("#lang"),m=w.querySelector(".langmenu");if(!lg||!m||lg.dataset.b)return;lg.dataset.b=1;
  lg.addEventListener("click",e=>{e.stopPropagation();const o=m.hidden;m.hidden=!o;lg.setAttribute("aria-expanded",o?"true":"false");if(o){const b=m.querySelector(".on")||m.querySelector("button");if(b)b.focus()}});
  m.querySelectorAll(".langopt").forEach(b=>b.addEventListener("click",e=>{e.stopPropagation();m.hidden=true;lg.setAttribute("aria-expanded","false");if(b.dataset.l===LANG)return;lg.disabled=true;goLang(b.dataset.l)}))})}
document.addEventListener("click",()=>document.querySelectorAll(".langmenu").forEach(m=>{m.hidden=true}));
document.addEventListener("keydown",e=>{if(e.key==="Escape")document.querySelectorAll(".langmenu:not([hidden])").forEach(m=>{m.hidden=true;e.stopImmediatePropagation()})},true);'''

LANG_CSS = '\n.langwrap{position:relative;display:inline-flex}.langmenu{position:absolute;top:calc(100% + 6px);right:0;z-index:60;display:flex;flex-direction:column;gap:2px;min-width:170px;padding:5px;background:var(--panel);border:1px solid var(--line);border-radius:8px;box-shadow:0 10px 28px rgba(0,0,0,.22)}.langopt{display:flex;gap:10px;align-items:center;width:100%;text-align:left;border:0;background:transparent;color:var(--ink);font:inherit;font-size:.95rem;padding:9px 11px;border-radius:6px;cursor:pointer}.langopt b{font-family:var(--mono);font-size:.8rem;min-width:24px}.langopt:hover,.langopt:focus-visible{background:var(--panel2);outline:none}.langopt.on{background:var(--panel2);font-weight:700}.langopt.on::after{content:"✓";margin-left:auto;color:var(--accent)}'

FR_PATCH = [
    ('document.title=META.title;', LANG_JS),
    ('copy:`<rect x="8" y="8" width="12" height="12" rx="2" ${P}/>',
     'globe:`<circle cx="12" cy="12" r="8.5" ${P}/><path d="M3.5 12h17M12 3.5c2.4 2.6 3.5 5.4 3.5 8.5s-1.1 5.9-3.5 8.5c-2.4-2.6-3.5-5.4-3.5-8.5s1.1-5.9 3.5-8.5z" ${P}/>`,\n copy:`<rect x="8" y="8" width="12" height="12" rx="2" ${P}/>'),
    ('<button type="button" class="chip btnchip" id="snd"', '${langBtn()}<button type="button" class="chip btnchip" id="snd"'),
    ('function bindTop(){const q=$("#wpquit");if(q)q.addEventListener("click",()=>wpQuit(q));',
     'function bindTop(){const q=$("#wpquit");if(q)q.addEventListener("click",()=>wpQuit(q));bindLang();'),
    ('$("#app").innerHTML=(WP?`<div class="row" style="justify-content:flex-end"><button type="button" class="chip btnchip quitwp" id="wpquit">${ic("cross")}Quitter</button></div>`:"")+',
     '$("#app").innerHTML=(WP||HAS_DE?`<div class="row" style="justify-content:flex-end">${langBtn()}${WP?`<button type="button" class="chip btnchip quitwp" id="wpquit">${ic("cross")}Quitter</button>`:""}</div>`:"")+'),
    ('innerHTML=`<div class="row" style="justify-content:flex-end"><button type="button" class="chip btnchip quitwp"',
     'innerHTML=`<div class="row" style="justify-content:flex-end">${langBtn()}<button type="button" class="chip btnchip quitwp"'),
    ('if(WPU)bootWP();else if(WP&&!WP.loggedIn&&window.JDR_CFG)needLogin();else{route();initCloud()}',
     'if(LREDIR)goLang(LPREF);else if(WPU)bootWP();else if(WP&&!WP.loggedIn&&window.JDR_CFG)needLogin();else{route();initCloud()}'),
    ('.avatar{background:var(--y)}', '.avatar{background:var(--y)}\n.chip.langsw{font-weight:700;letter-spacing:.04em}' + LANG_CSS),
]

def patch_fr(s):
    if 'const LANG="fr";' in s:
        if 'const LNAMES=' in s:
            return s
        # mise à niveau du bouton FR | DE vers le menu FR · DE · IT
        i = s.index('/* ---------- langue (FR / DE)'); j = s.index('function langBtn()', i); j = s.index('\n', j)
        s = s[:i] + LANG_JS.split('document.title=META.title;\n', 1)[1] + s[j:]
        old = 'const lg=$("#lang");if(lg)lg.addEventListener("click",()=>{lg.disabled=true;goLang(LANG==="fr"?"de":"fr")});'
        assert s.count(old) == 1, "ancien gestionnaire de langue introuvable"
        s = s.replace(old, 'bindLang();')
        old = '.chip.langsw{font-weight:700;letter-spacing:.04em}'
        assert s.count(old) == 1
        return s.replace(old, old + LANG_CSS)
    s = s.replace('<html><head>', '<html lang="fr"><head>', 1)
    for a, b in FR_PATCH:
        n = s.count(a)
        assert n == 1, f"ancre absente ou multiple ({n}) : {a[:70]}"
        s = s.replace(a, b, 1)
    return s

# ---------------------------------------------------------------- moteur allemand : textes d'interface
# (français, allemand) ; chaque texte français doit être présent au moins une fois dans le moteur.
DE = [
    ('<html lang="fr">', '<html lang="de">'),
    ('title="Langue"', 'title="Sprache"'),
    ('"Quitter le plein écran"', '"Vollbild beenden"'),
    ('"Plein écran"', '"Vollbild"'),
    ('<b>Classement de votre groupe</b>', '<b>Rangliste Ihrer Gruppe</b>'),
    ('`Cette semaine sur ce jeu : ${rkOrd', '`Diese Woche in diesem Spiel: ${rkOrd'),
    ('"Pas encore de points cette semaine sur ce jeu."', '"Diese Woche noch keine Punkte in diesem Spiel."'),
    ('>Voir le classement</button>', '>Rangliste ansehen</button>'),
    ('<h2>Classement</h2>', '<h2>Rangliste</h2>'),
    ('<label>Groupe <select', '<label>Gruppe <select'),
    ('"Cette semaine")', '"Diese Woche")'),
    ('"Depuis le début")', '"Gesamt")'),
    ('"Ce jeu")', '"Dieses Spiel")'),
    ('"Tous les jeux")', '"Alle Spiele")'),
    ('" (vous)"', '" (Sie)"'),
    ("Personne n'a encore de points ici.", 'Hier hat noch niemand Punkte.'),
    ('<small>XP gagnés dans les jeux de révision</small>', '<small>In den Lernspielen gewonnene XP</small>'),
    ('function rkOrd(n){return n===1?"1er":n+"e"}', 'function rkOrd(n){return n+"."}'),
    ('<script src="data.js"></script>', '<script src="data.de.js"></script>'),
    ('const LANG="fr";', 'const LANG="de";'),
    ('const KIND={pickimg:"Choisir l\'image",qcm:"QCM",odd:"Intrus",case:"Mise en situation",fill:"Texte à trous",tf:"Vrai ou faux",match:"Associer",sort:"Classer",order:"Remettre en ordre",multi:"Plusieurs réponses",num:"Réponse chiffrée"};',
     'const KIND={pickimg:"Bild wählen",qcm:"Multiple Choice",odd:"Was passt nicht?",case:"Praxisfall",fill:"Lückentext",tf:"Richtig oder falsch",match:"Zuordnen",sort:"Einordnen",order:"Reihenfolge",multi:"Mehrfachauswahl",num:"Zahlenantwort"};'),
    ('"Participant·e"', '"Teilnehmer·in"'),
    ('const STATUS=["À découvrir","En cours","Maîtrisé"];', 'const STATUS=["Neu","In Arbeit","Beherrscht"];'),
    ('"Premier objectif maîtrisé"', '"Erstes Lernziel beherrscht"'),
    ('"Examen blanc noté 5 ou plus"', '"Probeprüfung mit Note 5 oder besser"'),
    ('"10 bonnes réponses d\'affilée"', '"10 richtige Antworten in Folge"'),
    ('`Les ${OBJ.length} objectifs maîtrisés`', '`Alle ${OBJ.length} Lernziele beherrscht`'),
    ('"3 jours de suite"', '"3 Tage in Folge"'),
    ('"Objectif du jour atteint"', '"Tagesziel erreicht"'),
    ('"Connexion rétablie : progression enregistrée."', '"Verbindung wiederhergestellt: Fortschritt gespeichert."'),
    ('"Session expirée : reconnectez-vous au site, votre progression est gardée sur cet appareil."', '"Sitzung abgelaufen: Bitte melden Sie sich erneut an. Ihr Fortschritt bleibt auf diesem Gerät gespeichert."'),
    ('"Connexion perdue : la progression sera enregistrée dès le retour du réseau."', '"Verbindung unterbrochen: Der Fortschritt wird gespeichert, sobald das Netz wieder verfügbar ist."'),
    ('"sur votre compte du site"', '"in Ihrem Konto auf der Website"'),
    ('"sur votre compte Claude"', '"in Ihrem Claude-Konto"'),
    ('"Progression plus récente reprise depuis votre compte."', '"Neuerer Fortschritt aus Ihrem Konto übernommen."'),
    ('Chargement de votre progression…', 'Ihr Fortschritt wird geladen…'),
    ("Votre progression n'a pas pu être chargée depuis le site. Vérifiez votre connexion internet, puis réessayez.", 'Ihr Fortschritt konnte nicht von der Website geladen werden. Prüfen Sie Ihre Internetverbindung und versuchen Sie es erneut.'),
    ('>Réessayer<', '>Erneut versuchen<'),
    ('}Quitter', '}Beenden'),
    ('btn.textContent="Enregistrement…"', 'btn.textContent="Speichern…"'),
    ('Connectez-vous au site pour jouer : votre progression est enregistrée sur votre compte.', 'Melden Sie sich auf der Website an, um zu spielen: Ihr Fortschritt wird in Ihrem Konto gespeichert.'),
    ('>Se connecter<', '>Anmelden<'),
    ('Bonjour ${esc(WPU.first||WPU.name)}${started?", bon retour !":" !"}', 'Hallo ${esc(WPU.first||WPU.name)}${started?", willkommen zurück!":"!"}'),
    ('`Votre progression : ${globalMastery()} % de maîtrise, niveau « ${esc(LEVELS[i][1])} », ${S.xp} XP, objectifs maîtrisés : ${done}/${OBJ.length}${S.best?`, meilleure note à l\'examen blanc ${S.best.toFixed(1)}`:""}.`',
     '`Ihr Fortschritt: ${globalMastery()} % beherrscht, Stufe «${esc(LEVELS[i][1])}», ${S.xp} XP, beherrschte Lernziele: ${done}/${OBJ.length}${S.best?`, beste Note in der Probeprüfung ${S.best.toFixed(1)}`:""}.`'),
    ('${OBJ.length} objectifs, ${OBJ.reduce((n,o)=>n+o.ch.length,0)} épreuves, un examen blanc noté sur 6.', '${OBJ.length} Lernziele, ${OBJ.reduce((n,o)=>n+o.ch.length,0)} Aufgaben, eine Probeprüfung mit Noten von 1 bis 6.'),
    ('${started?"Reprendre":"Commencer"}', '${started?"Fortsetzen":"Starten"}'),
    ('☁️ Votre progression est enregistrée sur votre compte du site.', '☁️ Ihr Fortschritt wird in Ihrem Konto auf der Website gespeichert.'),
    ('btn.textContent="Copié"', 'btn.textContent="Kopiert"'),
    ('"Code sélectionné : copiez-le avec votre appareil."', '"Code markiert: Kopieren Sie ihn mit Ihrem Gerät."'),
    ('" · touchez pour zoomer"', '" · zum Zoomen tippen"'),
    ('aria-label="Agrandir le tableau"', 'aria-label="Vergrössern"'),
    ('aria-label="Agrandir"', 'aria-label="Vergrössern"'),
    ("Touchez l'image pour zoomer.", 'Tippen Sie auf das Bild, um zu zoomen.'),
    ('>Fermer<', '>Schliessen<'),
    ('` · ${nx[0]-S.xp} XP avant « ${esc(nx[1])} »`', '` · noch ${nx[0]-S.xp} XP bis «${esc(nx[1])}»`'),
    ('" · niveau maximum"', '" · Höchststufe"'),
    ('title="Jours consécutifs avec au moins une session"', 'title="Aufeinanderfolgende Tage mit mindestens einer Sitzung"'),
    ('${sk} jour${sk>1?"s":""}', '${sk} Tag${sk>1?"e":""}'),
    ('title="Objectif du jour"', 'title="Tagesziel"'),
    ('/${GOAL} aujourd\'hui', '/${GOAL} heute'),
    ('Son ${S.sound?"activé":"coupé"}', 'Ton ${S.sound?"an":"aus"}'),
    ('>Bienvenue !<', '>Willkommen!<'),
    ('type="submit">Commencer</button>', 'type="submit">Starten</button>'),
    ("Choisissez un objectif pour vous entraîner, passez l'examen blanc, ou reprenez les épreuves ratées.", 'Wählen Sie ein Lernziel zum Üben, legen Sie die Probeprüfung ab oder wiederholen Sie die falsch beantworteten Aufgaben.'),
    ("\"maîtrise de l'objectif\"", '"Lernstand des Lernziels"'),
    ('maîtrise globale', 'Lernstand gesamt'),
    ('<h3>Entraînement</h3>', '<h3>Training</h3>'),
    ("10 épreuves sur un objectif, avec l'explication après chaque réponse. Sans chrono.", '10 Aufgaben zu einem Lernziel, mit Erklärung nach jeder Antwort. Ohne Zeitlimit.'),
    ('Choisir un objectif ↓', 'Lernziel wählen ↓'),
    ('<h3>Examen blanc</h3>', '<h3>Probeprüfung</h3>'),
    ('${examCount()} épreuves mélangées, ${examMin()} minutes, note sur 6. Corrigé à la fin.', '${examCount()} gemischte Aufgaben, ${examMin()} Minuten, Note von 1 bis 6. Lösungen am Schluss.'),
    ('`Meilleure note ${S.best.toFixed(1)}`', '`Beste Note ${S.best.toFixed(1)}`'),
    ('"Pas encore passé"', '"Noch nicht abgelegt"'),
    ('<h3>Révision ciblée</h3>', '<h3>Gezielte Wiederholung</h3>'),
    ("Les épreuves ratées reviennent jusqu'à 2 réussites d'affilée, puis les objectifs pas encore maîtrisés.", 'Falsch beantwortete Aufgaben kommen wieder, bis sie zweimal in Folge richtig sind, danach die noch nicht beherrschten Lernziele.'),
    ('`${q} épreuve${q>1?"s":""} à revoir`', '`${q} Aufgabe${q>1?"n":""} zu wiederholen`'),
    ('`${weakO.length} objectif${weakO.length>1?"s":""} à consolider`', '`${weakO.length} Lernziel${weakO.length>1?"e":""} zu festigen`'),
    ('"Tout est maîtrisé"', '"Alles beherrscht"'),
    ('<h2>Objectifs du chapitre</h2>', '<h2>Lernziele des Kapitels</h2>'),
    ('Maîtrisé dès 80 %', 'Beherrscht ab 80 %'),
    ('/${o.ch.length} épreuves</span>', '/${o.ch.length} Aufgaben</span>'),
    ('<h2>Badges</h2>', '<h2>Abzeichen</h2>'),
    ('☁️ Progression enregistrée sur votre compte du site · ', '☁️ Fortschritt in Ihrem Konto auf der Website gespeichert · '),
    ("Elle est sauvegardée automatiquement après chaque réponse. Connectez-vous avec le même compte pour la retrouver sur n'importe quel appareil.", 'Er wird nach jeder Antwort automatisch gespeichert. Melden Sie sich mit demselben Konto an, um ihn auf jedem Gerät wiederzufinden.'),
    ('Aperçu hors plateforme', 'Vorschau ausserhalb der Plattform'),
    ("Dans cet aperçu, la progression reste sur cet appareil. Sur LogiProf, l'élève est connecté : sa progression et ses résultats sont enregistrés automatiquement sur son compte, sans aucun code à noter.",
     'In dieser Vorschau bleibt der Fortschritt auf diesem Gerät. Auf LogiProf sind die Lernenden angemeldet: Fortschritt und Resultate werden automatisch in ihrem Konto gespeichert, ohne Code.'),
    ('"Progression restaurée."', '"Fortschritt wiederhergestellt."'),
    ('"Examen blanc"', '"Probeprüfung"'),
    ('"Révision ciblée"', '"Gezielte Wiederholung"'),
    ('"Entraînement"', '"Training"'),
    ('"Série ×"', '"Serie ×"'),
    ('`Série ! +${g} XP`', '`Serie! +${g} XP`'),
    ('"Bonne réponse":"Réponse incorrecte"', '"Richtige Antwort":"Falsche Antwort"'),
    ('Référence : ', 'Quelle: '),
    ('"Épreuve suivante":"Voir le bilan"', '"Nächste Aufgabe":"Zur Auswertung"'),
    ('"Bilan de l\'examen blanc"', '"Auswertung der Probeprüfung"'),
    ('"Bilan de la révision"', '"Auswertung der Wiederholung"'),
    ('`Bilan · ${OBJ[R.oi].code}', '`Auswertung · ${OBJ[R.oi].code}'),
    ('"Excellent résultat, vous êtes prêt·e."', '"Ausgezeichnet, Sie sind bereit."'),
    ('"Résultat suffisant. Reprenez les objectifs en orange ci-dessous."', '"Genügend. Wiederholen Sie die schwächeren Lernziele unten."'),
    ('"Résultat insuffisant. Retravaillez les objectifs faibles en entraînement."', '"Ungenügend. Üben Sie die schwachen Lernziele im Training."'),
    ('"Sans faute, bravo."', '"Fehlerfrei, bravo!"'),
    ('"Très bon travail."', '"Sehr gute Arbeit."'),
    ('"Lisez bien les explications et revenez sur les épreuves ratées."', '"Lesen Sie die Erklärungen genau und wiederholen Sie die falsch beantworteten Aufgaben."'),
    ('"Temps écoulé · "', '"Zeit abgelaufen · "'),
    (')} de travail</p>', ')} Arbeitszeit</p>'),
    ('<span>note sur 6</span>', '<span>Note (1–6)</span>'),
    ('<span>bonnes réponses</span>', '<span>richtige Antworten</span>'),
    ('<span>XP gagnés</span>', '<span>XP erhalten</span>'),
    ('Nouveau niveau : ', 'Neue Stufe: '),
    ('Nouveau badge : ', 'Neues Abzeichen: '),
    ('Corrigé détaillé (${n} épreuves)', 'Ausführliche Lösungen (${n} Aufgaben)'),
    ('${g?"Réussie":"Ratée"}${r?"":" (sans réponse)"} · Réponse : ', '${g?"Richtig":"Falsch"}${r?"":" (keine Antwort)"} · Antwort: '),
    ('☁️ Enregistré sur votre compte du site. ', '☁️ In Ihrem Konto auf der Website gespeichert. '),
    ("Aperçu : progression gardée sur cet appareil. Sur LogiProf, elle est enregistrée sur le compte de l'élève.", 'Vorschau: Fortschritt auf diesem Gerät gespeichert. Auf LogiProf wird er im Konto der Lernenden gespeichert.'),
    ('Réviser ces points', 'Diese Punkte wiederholen'),
    ('>Nouvelle série<', '>Neue Serie<'),
    ('>Tableau de bord<', '>Übersicht<'),
    ('popText("Niveau supérieur")', 'popText("Nächste Stufe")'),
    ('c.v?"Vrai":"Faux"', 'c.v?"Richtig":"Falsch"'),
    ('"(sans réponse, temps écoulé)"', '"(keine Antwort, Zeit abgelaufen)"'),
    ('"Enregistrement du bilan…"', '"Auswertung wird gespeichert…"'),
    ('"✓ Bilan enregistré dans votre espace."', '"✓ Auswertung in Ihrem Bereich gespeichert."'),
    ('"Le bilan n\'a pas pu être enregistré (connexion) ; votre progression est sauvegardée."', '"Die Auswertung konnte nicht gespeichert werden (Verbindung); Ihr Fortschritt ist gesichert."'),
    ('"Le bilan n\'a pas pu être enregistré ; votre progression est sauvegardée."', '"Die Auswertung konnte nicht gespeichert werden; Ihr Fortschritt ist gesichert."'),
    ('"Bonne réponse : "', '"Richtige Antwort: "'),
    ('}Vrai</button>', '}Richtig</button>'),
    ('}Faux</button>', '}Falsch</button>'),
    ('said?"Vrai":"Faux"', 'said?"Richtig":"Falsch"'),
    ('Plusieurs réponses possibles. Cochez-les toutes, puis validez.', 'Mehrere Antworten möglich. Wählen Sie alle aus und bestätigen Sie.'),
    ('>Valider</button>', '>Bestätigen</button>'),
    ('"Réponses attendues : "', '"Erwartete Antworten: "'),
    ('"(aucune)"', '"(keine)"'),
    ('Votre réponse (nombre entier)', 'Ihre Antwort (ganze Zahl)'),
    ('aria-label="Votre réponse"', 'aria-label="Ihre Antwort"'),
    ('`Réponse attendue : ${c.n} ${c.u}`', '`Erwartete Antwort: ${c.n} ${c.u}`'),
    ('Touchez un élément à gauche, puis sa correspondance à droite.', 'Tippen Sie links auf ein Element und danach rechts auf das passende.'),
    ('`${err} erreur${err>1?"s":""} d\'association avant de trouver toutes les paires`', '`${err} Zuordnungsfehler, bevor alle Paare gefunden waren`'),
    ('`${err} erreur${err>1?"s":""} d\'association.`', '`${err} Zuordnungsfehler.`'),
    ('"Toutes les paires associées sans erreur"', '"Alle Paare fehlerfrei zugeordnet"'),
    ('Carte ${k+1} sur ${items.length}', 'Karte ${k+1} von ${items.length}'),
    ('${items.length-err} carte${items.length-err>1?"s":""} sur ${items.length} bien classée${items.length-err>1?"s":""}', '${items.length-err} von ${items.length} Karten richtig eingeordnet'),
    ('`${err} erreurs de classement.`', '`${err} Einordnungsfehler.`'),
    ('Touchez les étiquettes dans le bon ordre. Touchez une case remplie pour la vider.', 'Tippen Sie die Etiketten in der richtigen Reihenfolge an. Tippen Sie auf ein belegtes Feld, um es zu leeren.'),
    ('>Vérifier</button>', '>Prüfen</button>'),
    ('"Bon ordre : "', '"Richtige Reihenfolge: "'),
]

# ---------------------------------------------------------------- moteur italien : textes d'interface (mêmes ancres que DE)
IT = [
    ('<html lang="fr">', '<html lang="it">'),
    ('title="Langue"', 'title="Lingua"'),
    ('"Quitter le plein écran"', '"Esci da schermo intero"'),
    ('"Plein écran"', '"Schermo intero"'),
    ('<b>Classement de votre groupe</b>', '<b>Classifica del suo gruppo</b>'),
    ('`Cette semaine sur ce jeu : ${rkOrd', '`Questa settimana in questo gioco: ${rkOrd'),
    ('"Pas encore de points cette semaine sur ce jeu."', '"Ancora nessun punto questa settimana in questo gioco."'),
    ('>Voir le classement</button>', '>Vedi la classifica</button>'),
    ('<h2>Classement</h2>', '<h2>Classifica</h2>'),
    ('<label>Groupe <select', '<label>Gruppo <select'),
    ('"Cette semaine")', '"Questa settimana")'),
    ('"Depuis le début")', '"Dall’inizio")'),
    ('"Ce jeu")', '"Questo gioco")'),
    ('"Tous les jeux")', '"Tutti i giochi")'),
    ('" (vous)"', '" (Lei)"'),
    ("Personne n'a encore de points ici.", 'Qui nessuno ha ancora punti.'),
    ('<small>XP gagnés dans les jeux de révision</small>', '<small>XP guadagnati nei giochi di ripasso</small>'),
    ('function rkOrd(n){return n===1?"1er":n+"e"}', 'function rkOrd(n){return n+"°"}'),
    ('<script src="data.js"></script>', '<script src="data.it.js"></script>'),
    ('const LANG="fr";', 'const LANG="it";'),
    ('const KIND={pickimg:"Choisir l\'image",qcm:"QCM",odd:"Intrus",case:"Mise en situation",fill:"Texte à trous",tf:"Vrai ou faux",match:"Associer",sort:"Classer",order:"Remettre en ordre",multi:"Plusieurs réponses",num:"Réponse chiffrée"};',
     'const KIND={pickimg:"Scegliere l’immagine",qcm:"Scelta multipla",odd:"Intruso",case:"Caso pratico",fill:"Testo da completare",tf:"Vero o falso",match:"Abbinare",sort:"Classificare",order:"Mettere in ordine",multi:"Più risposte",num:"Risposta numerica"};'),
    ('"Participant·e"', '"Partecipante"'),
    ('const STATUS=["À découvrir","En cours","Maîtrisé"];', 'const STATUS=["Da scoprire","In corso","Padroneggiato"];'),
    ('"Premier objectif maîtrisé"', '"Primo obiettivo padroneggiato"'),
    ('"Examen blanc noté 5 ou plus"', '"Esame di prova con nota 5 o più"'),
    ('"10 bonnes réponses d\'affilée"', '"10 risposte giuste di fila"'),
    ('`Les ${OBJ.length} objectifs maîtrisés`', '`Tutti i ${OBJ.length} obiettivi padroneggiati`'),
    ('"3 jours de suite"', '"3 giorni di fila"'),
    ('"Objectif du jour atteint"', '"Obiettivo del giorno raggiunto"'),
    ('"Connexion rétablie : progression enregistrée."', '"Connessione ristabilita: progressi salvati."'),
    ('"Session expirée : reconnectez-vous au site, votre progression est gardée sur cet appareil."', '"Sessione scaduta: effettui di nuovo l’accesso al sito, i suoi progressi restano su questo dispositivo."'),
    ('"Connexion perdue : la progression sera enregistrée dès le retour du réseau."', '"Connessione persa: i progressi saranno salvati appena torna la rete."'),
    ('"sur votre compte du site"', '"nel suo account del sito"'),
    ('"sur votre compte Claude"', '"nel suo account Claude"'),
    ('"Progression plus récente reprise depuis votre compte."', '"Ripresi i progressi più recenti dal suo account."'),
    ('Chargement de votre progression…', 'Caricamento dei suoi progressi…'),
    ("Votre progression n'a pas pu être chargée depuis le site. Vérifiez votre connexion internet, puis réessayez.", 'Non è stato possibile caricare i suoi progressi dal sito. Verifichi la connessione internet e riprovi.'),
    ('>Réessayer<', '>Riprova<'),
    ('}Quitter', '}Esci'),
    ('btn.textContent="Enregistrement…"', 'btn.textContent="Salvataggio…"'),
    ('Connectez-vous au site pour jouer : votre progression est enregistrée sur votre compte.', 'Acceda al sito per giocare: i suoi progressi sono salvati nel suo account.'),
    ('>Se connecter<', '>Accedi<'),
    ('Bonjour ${esc(WPU.first||WPU.name)}${started?", bon retour !":" !"}', 'Buongiorno ${esc(WPU.first||WPU.name)}${started?", bentornato/a!":"!"}'),
    ('`Votre progression : ${globalMastery()} % de maîtrise, niveau « ${esc(LEVELS[i][1])} », ${S.xp} XP, objectifs maîtrisés : ${done}/${OBJ.length}${S.best?`, meilleure note à l\'examen blanc ${S.best.toFixed(1)}`:""}.`',
     '`I suoi progressi: ${globalMastery()} % di padronanza, livello «${esc(LEVELS[i][1])}», ${S.xp} XP, obiettivi padroneggiati: ${done}/${OBJ.length}${S.best?`, nota migliore all’esame di prova ${S.best.toFixed(1)}`:""}.`'),
    ('${OBJ.length} objectifs, ${OBJ.reduce((n,o)=>n+o.ch.length,0)} épreuves, un examen blanc noté sur 6.', '${OBJ.length} obiettivi, ${OBJ.reduce((n,o)=>n+o.ch.length,0)} esercizi, un esame di prova con nota da 1 a 6.'),
    ('${started?"Reprendre":"Commencer"}', '${started?"Continua":"Inizia"}'),
    ('☁️ Votre progression est enregistrée sur votre compte du site.', '☁️ I suoi progressi sono salvati nel suo account del sito.'),
    ('btn.textContent="Copié"', 'btn.textContent="Copiato"'),
    ('"Code sélectionné : copiez-le avec votre appareil."', '"Codice selezionato: lo copi con il suo dispositivo."'),
    ('" · touchez pour zoomer"', '" · tocchi per ingrandire"'),
    ('aria-label="Agrandir le tableau"', 'aria-label="Ingrandisci"'),
    ('aria-label="Agrandir"', 'aria-label="Ingrandisci"'),
    ("Touchez l'image pour zoomer.", 'Tocchi l’immagine per ingrandire.'),
    ('>Fermer<', '>Chiudi<'),
    ('` · ${nx[0]-S.xp} XP avant « ${esc(nx[1])} »`', '` · ancora ${nx[0]-S.xp} XP per «${esc(nx[1])}»`'),
    ('" · niveau maximum"', '" · livello massimo"'),
    ('title="Jours consécutifs avec au moins une session"', 'title="Giorni consecutivi con almeno una sessione"'),
    ('${sk} jour${sk>1?"s":""}', '${sk} giorn${sk>1?"i":"o"}'),
    ('title="Objectif du jour"', 'title="Obiettivo del giorno"'),
    ('/${GOAL} aujourd\'hui', '/${GOAL} oggi'),
    ('Son ${S.sound?"activé":"coupé"}', 'Audio ${S.sound?"attivo":"spento"}'),
    ('>Bienvenue !<', '>Benvenuto/a!<'),
    ('type="submit">Commencer</button>', 'type="submit">Inizia</button>'),
    ("Choisissez un objectif pour vous entraîner, passez l'examen blanc, ou reprenez les épreuves ratées.", 'Scelga un obiettivo per allenarsi, faccia l’esame di prova o riprenda gli esercizi sbagliati.'),
    ("\"maîtrise de l'objectif\"", '"padronanza dell’obiettivo"'),
    ('maîtrise globale', 'padronanza globale'),
    ('<h3>Entraînement</h3>', '<h3>Allenamento</h3>'),
    ("10 épreuves sur un objectif, avec l'explication après chaque réponse. Sans chrono.", '10 esercizi su un obiettivo, con la spiegazione dopo ogni risposta. Senza cronometro.'),
    ('Choisir un objectif ↓', 'Scegliere un obiettivo ↓'),
    ('<h3>Examen blanc</h3>', '<h3>Esame di prova</h3>'),
    ('${examCount()} épreuves mélangées, ${examMin()} minutes, note sur 6. Corrigé à la fin.', '${examCount()} esercizi misti, ${examMin()} minuti, nota da 1 a 6. Correzione alla fine.'),
    ('`Meilleure note ${S.best.toFixed(1)}`', '`Nota migliore ${S.best.toFixed(1)}`'),
    ('"Pas encore passé"', '"Non ancora svolto"'),
    ('<h3>Révision ciblée</h3>', '<h3>Ripasso mirato</h3>'),
    ("Les épreuves ratées reviennent jusqu'à 2 réussites d'affilée, puis les objectifs pas encore maîtrisés.", 'Gli esercizi sbagliati ritornano fino a 2 risposte giuste di fila, poi gli obiettivi non ancora padroneggiati.'),
    ('`${q} épreuve${q>1?"s":""} à revoir`', '`${q} eserciz${q>1?"i":"io"} da rivedere`'),
    ('`${weakO.length} objectif${weakO.length>1?"s":""} à consolider`', '`${weakO.length} obiettiv${weakO.length>1?"i":"o"} da consolidare`'),
    ('"Tout est maîtrisé"', '"Tutto padroneggiato"'),
    ('<h2>Objectifs du chapitre</h2>', '<h2>Obiettivi del capitolo</h2>'),
    ('Maîtrisé dès 80 %', 'Padroneggiato da 80 %'),
    ('/${o.ch.length} épreuves</span>', '/${o.ch.length} esercizi</span>'),
    ('<h2>Badges</h2>', '<h2>Distintivi</h2>'),
    ('☁️ Progression enregistrée sur votre compte du site · ', '☁️ Progressi salvati nel suo account del sito · '),
    ("Elle est sauvegardée automatiquement après chaque réponse. Connectez-vous avec le même compte pour la retrouver sur n'importe quel appareil.", 'Sono salvati automaticamente dopo ogni risposta. Acceda con lo stesso account per ritrovarli su qualsiasi dispositivo.'),
    ('Aperçu hors plateforme', 'Anteprima fuori piattaforma'),
    ("Dans cet aperçu, la progression reste sur cet appareil. Sur LogiProf, l'élève est connecté : sa progression et ses résultats sont enregistrés automatiquement sur son compte, sans aucun code à noter.",
     'In questa anteprima i progressi restano su questo dispositivo. Su LogiProf l’apprendista ha effettuato l’accesso: progressi e risultati sono salvati automaticamente nel suo account, senza codici da annotare.'),
    ('"Progression restaurée."', '"Progressi ripristinati."'),
    ('"Examen blanc"', '"Esame di prova"'),
    ('"Révision ciblée"', '"Ripasso mirato"'),
    ('"Entraînement"', '"Allenamento"'),
    ('"Série ×"', '"Serie ×"'),
    ('`Série ! +${g} XP`', '`Serie! +${g} XP`'),
    ('"Bonne réponse":"Réponse incorrecte"', '"Risposta giusta":"Risposta sbagliata"'),
    ('Référence : ', 'Riferimento: '),
    ('"Épreuve suivante":"Voir le bilan"', '"Esercizio successivo":"Vedi il bilancio"'),
    ('"Bilan de l\'examen blanc"', '"Bilancio dell’esame di prova"'),
    ('"Bilan de la révision"', '"Bilancio del ripasso"'),
    ('`Bilan · ${OBJ[R.oi].code}', '`Bilancio · ${OBJ[R.oi].code}'),
    ('"Excellent résultat, vous êtes prêt·e."', '"Risultato eccellente, è pronto/a."'),
    ('"Résultat suffisant. Reprenez les objectifs en orange ci-dessous."', '"Risultato sufficiente. Riprenda gli obiettivi più deboli qui sotto."'),
    ('"Résultat insuffisant. Retravaillez les objectifs faibles en entraînement."', '"Risultato insufficiente. Rielabori gli obiettivi deboli con l’allenamento."'),
    ('"Sans faute, bravo."', '"Senza errori, brava/o!"'),
    ('"Très bon travail."', '"Ottimo lavoro."'),
    ('"Lisez bien les explications et revenez sur les épreuves ratées."', '"Legga bene le spiegazioni e riprenda gli esercizi sbagliati."'),
    ('"Temps écoulé · "', '"Tempo scaduto · "'),
    (')} de travail</p>', ')} di lavoro</p>'),
    ('<span>note sur 6</span>', '<span>nota (1–6)</span>'),
    ('<span>bonnes réponses</span>', '<span>risposte giuste</span>'),
    ('<span>XP gagnés</span>', '<span>XP guadagnati</span>'),
    ('Nouveau niveau : ', 'Nuovo livello: '),
    ('Nouveau badge : ', 'Nuovo distintivo: '),
    ('Corrigé détaillé (${n} épreuves)', 'Correzione dettagliata (${n} esercizi)'),
    ('${g?"Réussie":"Ratée"}${r?"":" (sans réponse)"} · Réponse : ', '${g?"Giusta":"Sbagliata"}${r?"":" (senza risposta)"} · Risposta: '),
    ('☁️ Enregistré sur votre compte du site. ', '☁️ Salvato nel suo account del sito. '),
    ("Aperçu : progression gardée sur cet appareil. Sur LogiProf, elle est enregistrée sur le compte de l'élève.", 'Anteprima: progressi conservati su questo dispositivo. Su LogiProf sono salvati nell’account dell’apprendista.'),
    ('Réviser ces points', 'Ripassare questi punti'),
    ('>Nouvelle série<', '>Nuova serie<'),
    ('>Tableau de bord<', '>Panoramica<'),
    ('popText("Niveau supérieur")', 'popText("Livello superiore")'),
    ('c.v?"Vrai":"Faux"', 'c.v?"Vero":"Falso"'),
    ('"(sans réponse, temps écoulé)"', '"(senza risposta, tempo scaduto)"'),
    ('"Enregistrement du bilan…"', '"Salvataggio del bilancio…"'),
    ('"✓ Bilan enregistré dans votre espace."', '"✓ Bilancio salvato nel suo spazio."'),
    ('"Le bilan n\'a pas pu être enregistré (connexion) ; votre progression est sauvegardée."', '"Non è stato possibile salvare il bilancio (connessione); i suoi progressi sono salvati."'),
    ('"Le bilan n\'a pas pu être enregistré ; votre progression est sauvegardée."', '"Non è stato possibile salvare il bilancio; i suoi progressi sono salvati."'),
    ('"Bonne réponse : "', '"Risposta giusta: "'),
    ('}Vrai</button>', '}Vero</button>'),
    ('}Faux</button>', '}Falso</button>'),
    ('said?"Vrai":"Faux"', 'said?"Vero":"Falso"'),
    ('Plusieurs réponses possibles. Cochez-les toutes, puis validez.', 'Più risposte possibili. Le selezioni tutte, poi confermi.'),
    ('>Valider</button>', '>Conferma</button>'),
    ('"Réponses attendues : "', '"Risposte attese: "'),
    ('"(aucune)"', '"(nessuna)"'),
    ('Votre réponse (nombre entier)', 'La sua risposta (numero intero)'),
    ('aria-label="Votre réponse"', 'aria-label="La sua risposta"'),
    ('`Réponse attendue : ${c.n} ${c.u}`', '`Risposta attesa: ${c.n} ${c.u}`'),
    ('Touchez un élément à gauche, puis sa correspondance à droite.', 'Tocchi un elemento a sinistra, poi il suo corrispondente a destra.'),
    ('`${err} erreur${err>1?"s":""} d\'association avant de trouver toutes les paires`', '`${err} error${err>1?"i":"e"} di abbinamento prima di trovare tutte le coppie`'),
    ('`${err} erreur${err>1?"s":""} d\'association.`', '`${err} error${err>1?"i":"e"} di abbinamento.`'),
    ('"Toutes les paires associées sans erreur"', '"Tutte le coppie abbinate senza errori"'),
    ('Carte ${k+1} sur ${items.length}', 'Carta ${k+1} di ${items.length}'),
    ('${items.length-err} carte${items.length-err>1?"s":""} sur ${items.length} bien classée${items.length-err>1?"s":""}', '${items.length-err} carte su ${items.length} classificate correttamente'),
    ('`${err} erreurs de classement.`', '`${err} errori di classificazione.`'),
    ('Touchez les étiquettes dans le bon ordre. Touchez une case remplie pour la vider.', 'Tocchi le etichette nell’ordine giusto. Tocchi una casella piena per svuotarla.'),
    ('>Vérifier</button>', '>Verifica</button>'),
    ('"Bon ordre : "', '"Ordine giusto: "'),
]

TABLES = {'de': None, 'it': None}

def make_lang(s, titre, code):
    return make_de(s, titre, IT if code == 'it' else DE)

def make_de(s, titre, table=None):
    assert 'const LANG="fr";' in s, "moteur français sans bouton de langue : lancer d'abord « moteur »"
    for a, b in (table or DE):
        n = s.count(a)
        assert n >= 1, f"texte absent du moteur : {a[:80]}"
        s = s.replace(a, b)
    s = re.sub(r"<title>.*?</title>", "<title>" + html.escape(titre, quote=False) + "</title>", s, count=1, flags=re.S)
    return s

def reste_fr(s):
    """textes français restants hors commentaires (contrôle)"""
    js = re.sub(r'/\*.*?\*/', '', s, flags=re.S)
    mots = re.findall(r"[^<>`\"{}]*\b(?:vous|votre|épreuve|objectif|réponse|Quitter|Commencer|maîtris|examen blanc|bilan)\b[^<>`\"{}]*", js, flags=re.I)
    return [m.strip() for m in mots if m.strip() and 'Jouer en français' not in m]

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'moteur':
        p = sys.argv[2]; s = open(p, encoding='utf-8').read(); open(p, 'w', encoding='utf-8').write(patch_fr(s)); print('ok', p)
    elif cmd == 'de':
        p, titre = sys.argv[2], sys.argv[3]
        s = patch_fr(open(p, encoding='utf-8').read()); open(p, 'w', encoding='utf-8').write(s)
        d = make_de(s, titre); open(os.path.join(os.path.dirname(p), 'index.de.html'), 'w', encoding='utf-8').write(d)
        r = reste_fr(d)
        print('ok', p, '· reste FR :', r[:5] if r else 'rien')
    elif cmd == 'tous':
        R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        for p in sorted(glob.glob(R + '/jeux/*/index.html')):
            s = patch_fr(open(p, encoding='utf-8').read()); open(p, 'w', encoding='utf-8').write(s)
            for code in ('de', 'it'):
                dj = os.path.join(os.path.dirname(p), 'data.' + code + '.js')
                if os.path.exists(dj):
                    import json
                    t = json.loads('"' + re.search(r'"title":"((?:[^"\\]|\\.)*)"', open(dj, encoding='utf-8').read()).group(1) + '"')
                    open(os.path.join(os.path.dirname(p), 'index.' + code + '.html'), 'w', encoding='utf-8').write(make_lang(s, t, code))
        print('ok')

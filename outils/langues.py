#!/usr/bin/env python3
"""langues.py : moteur de jeu bilingue français / allemand.

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
/* ---------- langue (FR / DE) : même jeu, même progression ---------- */
const LANG="fr";
const HAS_DE=Array.isArray(META.langs)&&META.langs.indexOf("de")>=0&&META.langs.indexOf("fr")>=0;
const LQ=(()=>{try{return new URLSearchParams(location.search).get("lang")}catch(e){return null}})();
const LPREF=(()=>{try{return localStorage.getItem("jdr-lang")}catch(e){return null}})();
const LREDIR=HAS_DE&&!LQ&&(LPREF==="fr"||LPREF==="de")&&LPREF!==LANG;
function goLang(l){try{localStorage.setItem("jdr-lang",l)}catch(e){}
  const go=()=>{try{const u=new URL(location.href);u.searchParams.set("lang",l);if(!window.JDR_CFG)u.pathname=u.pathname.replace(/[^\/]*$/,l==="de"?"index.de.html":"index.html");location.replace(u.href)}catch(e){location.reload()}};
  try{Promise.race([cloudFlush(),new Promise(r=>setTimeout(r,1500))]).then(go,go)}catch(e){go()}}
function langBtn(){if(!HAS_DE)return"";const o=LANG==="fr"?"de":"fr";return `<button type="button" class="chip btnchip langsw" id="lang" lang="${o}" title="${o==="de"?"Auf Deutsch spielen":"Jouer en français"}">${ic("globe")}${o.toUpperCase()}</button>`}'''

FR_PATCH = [
    ('document.title=META.title;', LANG_JS),
    ('copy:`<rect x="8" y="8" width="12" height="12" rx="2" ${P}/>',
     'globe:`<circle cx="12" cy="12" r="8.5" ${P}/><path d="M3.5 12h17M12 3.5c2.4 2.6 3.5 5.4 3.5 8.5s-1.1 5.9-3.5 8.5c-2.4-2.6-3.5-5.4-3.5-8.5s1.1-5.9 3.5-8.5z" ${P}/>`,\n copy:`<rect x="8" y="8" width="12" height="12" rx="2" ${P}/>'),
    ('<button type="button" class="chip btnchip" id="snd"', '${langBtn()}<button type="button" class="chip btnchip" id="snd"'),
    ('function bindTop(){const q=$("#wpquit");if(q)q.addEventListener("click",()=>wpQuit(q));',
     'function bindTop(){const q=$("#wpquit");if(q)q.addEventListener("click",()=>wpQuit(q));const lg=$("#lang");if(lg)lg.addEventListener("click",()=>{lg.disabled=true;goLang(LANG==="fr"?"de":"fr")});'),
    ('$("#app").innerHTML=(WP?`<div class="row" style="justify-content:flex-end"><button type="button" class="chip btnchip quitwp" id="wpquit">${ic("cross")}Quitter</button></div>`:"")+',
     '$("#app").innerHTML=(WP||HAS_DE?`<div class="row" style="justify-content:flex-end">${langBtn()}${WP?`<button type="button" class="chip btnchip quitwp" id="wpquit">${ic("cross")}Quitter</button>`:""}</div>`:"")+'),
    ('innerHTML=`<div class="row" style="justify-content:flex-end"><button type="button" class="chip btnchip quitwp"',
     'innerHTML=`<div class="row" style="justify-content:flex-end">${langBtn()}<button type="button" class="chip btnchip quitwp"'),
    ('if(WPU)bootWP();else if(WP&&!WP.loggedIn&&window.JDR_CFG)needLogin();else{route();initCloud()}',
     'if(LREDIR)goLang(LPREF);else if(WPU)bootWP();else if(WP&&!WP.loggedIn&&window.JDR_CFG)needLogin();else{route();initCloud()}'),
    ('.avatar{background:var(--y)}', '.avatar{background:var(--y)}\n.chip.langsw{font-weight:700;letter-spacing:.04em}'),
]

def patch_fr(s):
    if 'const LANG="fr";' in s:
        return s
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

def make_de(s, titre):
    assert 'const LANG="fr";' in s, "moteur français sans bouton de langue : lancer d'abord « moteur »"
    for a, b in DE:
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
            dj = os.path.join(os.path.dirname(p), 'data.de.js')
            if os.path.exists(dj):
                import json
                t = json.loads('"' + re.search(r'"title":"((?:[^"\\]|\\.)*)"', open(dj, encoding='utf-8').read()).group(1) + '"')
                open(os.path.join(os.path.dirname(p), 'index.de.html'), 'w', encoding='utf-8').write(make_de(s, t))
        print('ok')

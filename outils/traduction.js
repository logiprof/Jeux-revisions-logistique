#!/usr/bin/env node
/* traduction.js : version allemande d'un jeu, avec exactement les mêmes épreuves dans le même ordre.

   node outils/traduction.js feuille <dossier_jeu>            → liste numérotée des textes français uniques à traduire (N|texte)
   node outils/traduction.js construire <dossier_jeu> <feuille.txt> [de|it]   (défaut : de)
        → écrit data.de.js (même META.key : même progression), ajoute META.langs à data.js, complète jeu.json (clé « de »)
   node outils/traduction.js controle <dossier_jeu>           → vérifie que data.de.js est aligné sur data.js

   Traduits automatiquement : références (« Leçon 2.3 » → « Lektion 2.3 »), unités courantes, sur-titre, niveaux courants.
   Les clés d'images (pickimg), codes, couleurs, icônes, nombres et réponses vrai/faux ne sont jamais traduits. */
"use strict";
const fs = require("fs"), path = require("path"), vm = require("vm");

function load(file) {
  const ctx = { window: {} }; vm.createContext(ctx);
  vm.runInContext(fs.readFileSync(file, "utf8"), ctx, { filename: file });
  return { OBJ: ctx.window.OBJ, LEVELS: ctx.window.LEVELS, META: ctx.window.META };
}
const UNITS = { "pièces": "Stück", "pièce": "Stück", "jours": "Tage", "jour": "Tag", "minutes": "Minuten", "minute": "Minute", "heures": "Stunden", "heure": "Stunde",
  "palettes": "Paletten", "palette": "Palette", "cartons": "Kartons", "carton": "Karton", "colis": "Pakete", "mois": "Monate", "ans": "Jahre", "an": "Jahr", "années": "Jahre",
  "semaines": "Wochen", "semaine": "Woche", "fois": "Mal", "lignes/h": "Zeilen/h", "lignes": "Zeilen", "commandes": "Aufträge", "commande": "Auftrag", "articles": "Artikel",
  "caractères": "Zeichen", "chiffres": "Ziffern", "chiffre": "Ziffer", "places": "Plätze", "place": "Platz", "camions": "Lastwagen", "employés": "Mitarbeitende",
  "personnes": "Personen", "étages": "Etagen", "niveaux": "Ebenen", "zéro": "Null", "paires": "Paare", "rouleaux": "Rollen", "litres": "Liter", "conteneurs": "Container",
  "tonnes": "Tonnen", "wagons": "Wagen", "essieux": "Achsen", "emplacements": "Lagerplätze", "unités": "Einheiten", "bacs": "Behälter", "sacs": "Säcke", "fûts": "Fässer" };
const UNITS_IT = { "pièces": "pezzi", "pièce": "pezzo", "jours": "giorni", "jour": "giorno", "minutes": "minuti", "minute": "minuto", "heures": "ore", "heure": "ora",
  "palettes": "palette", "palette": "paletta", "cartons": "cartoni", "carton": "cartone", "colis": "colli", "mois": "mesi", "ans": "anni", "an": "anno", "années": "anni",
  "semaines": "settimane", "semaine": "settimana", "fois": "volte", "lignes/h": "righe/h", "lignes": "righe", "commandes": "ordini", "commande": "ordine", "articles": "articoli",
  "caractères": "caratteri", "chiffres": "cifre", "chiffre": "cifra", "places": "posti", "place": "posto", "camions": "camion", "employés": "dipendenti",
  "personnes": "persone", "étages": "piani", "niveaux": "livelli", "zéro": "zero", "paires": "paia", "rouleaux": "rotoli", "litres": "litri", "conteneurs": "container",
  "tonnes": "tonnellate", "wagons": "vagoni", "essieux": "assi", "emplacements": "ubicazioni", "unités": "unità", "bacs": "contenitori", "sacs": "sacchi", "fûts": "fusti",
  "couches": "strati", "préparateurs": "preparatori", "collaborateurs": "collaboratori", "heures-personne": "ore-persona" };
const LEVEL_IT = { "Stagiaire": "Stagista", "Apprenti·e logisticien·ne": "Apprendista in logistica", "Logisticien·ne en formation": "Impiegato/a in logistica in formazione",
  "Logisticien·ne CFC": "Impiegato/a in logistica AFC", "Formateur·rice logistique": "Formatore/trice in logistica" };
let LG = "de";
const LEVEL_DE = { "Stagiaire": "Einsteiger/-in", "Apprenti·e logisticien·ne": "Logistik-Lernende/r", "Logisticien·ne en formation": "Logistiker/-in in Ausbildung",
  "Logisticien·ne CFC": "Logistiker/-in EFZ", "Formateur·rice logistique": "Berufsbildner/-in Logistik" };
function autoRef(r) {
  if (LG === "it") {
    let t = r.replace(/\bLeçons\b/g, "Lezioni").replace(/\bLeçon\b/g, "Lezione").replace(/\bObjectifs\b/g, "Obiettivi").replace(/\bObjectif\b/g, "Obiettivo")
      .replace(/\bModules\b/g, "Moduli").replace(/\bModule\b/g, "Modulo").replace(/ et /g, " e ").replace(/ à /g, " a ").replace(/\bannexe\b/gi, "allegato");
    const rest = t.replace(/\b(Lezioni|Lezione|Obiettivi|Obiettivo|Moduli|Modulo|e|a|allegato)\b/g, "").replace(/\b[A-Za-z]{0,2}\d[\w.]*\b/g, "");
    return /[a-zà-ÿ]{3,}/i.test(rest) ? null : t;
  }
  let t = r.replace(/\bLeçons\b/g, "Lektionen").replace(/\bLeçon\b/g, "Lektion").replace(/\bObjectifs\b/g, "Lernziele").replace(/\bObjectif\b/g, "Lernziel")
    .replace(/\bModules\b/g, "Module").replace(/ et /g, " und ").replace(/ à /g, " bis ").replace(/\bannexe\b/gi, "Anhang");
  const rest = t.replace(/\b(Lektionen|Lektion|Lernziele|Lernziel|Module|Modul|und|bis|Anhang)\b/g, "").replace(/\b[A-Za-z]{0,2}\d[\w.]*\b/g, "");
  return /[a-zà-ÿ]{3,}/i.test(rest) ? null : t;
}
function autoEyebrow(e) { const m = /^Logisticien·ne CFC · Module (M\d+)$/.exec(e); return m ? (LG === "it" ? "Impiegato/a in logistica AFC · Modulo " : "Logistiker/-in EFZ · Modul ") + m[1] : null; }

/* parcourt tous les textes traduisibles ; f(valeur, typeAuto) renvoie la valeur traduite */
function walk(d, f) {
  const O = JSON.parse(JSON.stringify(d.OBJ)), L = JSON.parse(JSON.stringify(d.LEVELS)), M = JSON.parse(JSON.stringify(d.META));
  const T = (v, k) => (typeof v === "string" && v !== "") ? f(v, k) : v;
  O.forEach(o => {
    o.t = T(o.t); o.g = T(o.g);
    o.ch.forEach(c => {
      ["q", "s", "ex"].forEach(k => { if (c[k] != null) c[k] = T(c[k]); });
      if (c.ref != null) c.ref = T(c.ref, "ref");
      if (c.u != null) c.u = T(c.u, "unit");
      if (Array.isArray(c.a) && c.k !== "pickimg") c.a = c.a.map(x => T(x));
      if (Array.isArray(c.good)) c.good = c.good.map(x => T(x));
      if (Array.isArray(c.bad)) c.bad = c.bad.map(x => T(x));
      if (Array.isArray(c.p)) c.p = c.p.map(p => p.map(x => T(x)));
      if (Array.isArray(c.c)) c.c = c.c.map(x => T(x));
      if (Array.isArray(c.it)) c.it = c.it.map(x => [T(x[0]), x[1]]);
    });
  });
  L.forEach(l => { l[1] = T(l[1], "level"); });
  const mt = /^(M\d+) – (.*)$/.exec(M.title || "");
  M.title = mt ? mt[1] + " – " + T(mt[2]) : T(M.title);
  M.eyebrow = T(M.eyebrow, "eyebrow"); M.intro = T(M.intro);
  if (M.note) M.note.text = T(M.note.text);
  if (M.cover) M.cover.alt = T(M.cover.alt);
  if (M.imgs) for (const k in M.imgs) M.imgs[k].alt = T(M.imgs[k].alt);
  return { OBJ: O, LEVELS: L, META: M };
}
function auto(v, k) {
  if (k === "ref") return autoRef(v);
  const U = LG === "it" ? UNITS_IT : UNITS;
  if (k === "unit") return v in U ? U[v] : (/^[A-Za-z%°²³./€\s\d-]*$/.test(v) && !/[a-zà-ÿ]{4,}/.test(v) ? v : null);
  if (k === "level") return (LG === "it" ? LEVEL_IT : LEVEL_DE)[v] || null;
  if (k === "eyebrow") return autoEyebrow(v);
  return null;
}
function sheet(dir) {
  const d = load(path.join(dir, "data.js")); const ids = new Map();
  walk(d, (v, k) => { const a = auto(v, k); if (a == null && !ids.has(v)) ids.set(v, ids.size + 1); return v; });
  return ids;
}
function readSheet(file) {
  const m = new Map();
  fs.readFileSync(file, "utf8").split(/\r?\n/).forEach((line, i) => {
    if (!line.trim() || line.startsWith("#")) return;
    const k = line.indexOf("|"); if (k < 0) throw new Error("ligne " + (i + 1) + " sans « | » : " + line.slice(0, 60));
    const n = +line.slice(0, k).trim(); if (!n) throw new Error("ligne " + (i + 1) + " : numéro invalide");
    m.set(n, line.slice(k + 1).trim());
  });
  return m;
}
const FR_HINT_IT = /\b(les|une|sont|pour|avec|dans|sur|aux|leur|vous|votre|être|cette|selon|du|des)\b|[êç]/i;
const FR_HINT = /\b(les|une|est|sont|pour|avec|dans|sur|qui|que|aux|leur|vous|votre|être|cette|selon|du|le|la)\b|[èêàçù]|é(?!e)/i;
function build(dir, sheetFile) {
  const d = load(path.join(dir, "data.js")); const ids = sheet(dir); const tr = readSheet(sheetFile);
  const missing = [...ids.values()].filter(n => !tr.has(n));
  if (missing.length) throw new Error(missing.length + " traductions manquantes : " + missing.slice(0, 20).join(", "));
  const extra = [...tr.keys()].filter(n => n > ids.size); if (extra.length) throw new Error("numéros en trop : " + extra.slice(0, 10).join(", "));
  const de = walk(d, (v, k) => { const a = auto(v, k); return a != null ? a : tr.get(ids.get(v)); });
  /* contrôles : nombre de « ___ » conservé dans les textes à trous, aucune traduction vide, indices de français restant */
  const warn = [];
  de.OBJ.forEach((o, oi) => o.ch.forEach((c, ci) => { if (c.k === "fill" && (c.q.match(/___/g) || []).length !== 1) warn.push(`${o.code}#${ci} : « ___ » absent ou multiple`); }));
  for (const [n, t] of tr) if ((LG === "it" ? FR_HINT_IT : FR_HINT).test(t.replace(/\b(Café|Exposé|Dépôt|Communiqué|à la carte|Suva|vis-à-vis)\b/gi, ""))) warn.push(`ligne ${n} ressemble encore à du français : ${t.slice(0, 70)}`);
  de.META.key = d.META.key;
  if (de.META.cover && fs.existsSync(path.join(dir, "img/cover." + LG + ".jpg"))) de.META.cover.src = "img/cover." + LG + ".jpg";
  /* images redessinées en allemand : img/<nom>.de.<ext> remplace img/<nom>.<ext> quand elle existe */
  for (const im of Object.values(de.META.imgs || {})) {
    const alt = im.src && im.src.replace(/\.(\w+)$/, "." + LG + ".$1");
    if (alt && alt !== im.src && fs.existsSync(path.join(dir, alt))) im.src = alt;
  }
  const langs = ["fr"].concat(["de", "it"].filter(l => l === LG || fs.existsSync(path.join(dir, "data." + l + ".js")))); de.META.langs = langs;
  const js = "/* " + de.META.title + " – version " + (LG === "it" ? "italienne" : "allemande") + ", générée par outils/traduction.js depuis data.js (mêmes épreuves, même ordre). a[0] = richtige Antwort. */\n"
    + "window.OBJ = " + JSON.stringify(de.OBJ) + ";\nwindow.LEVELS = " + JSON.stringify(de.LEVELS) + ";\nwindow.META = " + JSON.stringify(de.META) + ";\n";
  fs.writeFileSync(path.join(dir, "data." + LG + ".js"), js);
  /* data.js et les autres versions savent quelles langues existent */
  const fp = path.join(dir, "data.js"); let fsrc = fs.readFileSync(fp, "utf8").replace(/\s*window\.META\.langs\s*=.*\n?/g, "\n");
  fs.writeFileSync(fp, fsrc.replace(/\s*$/, "\n") + "window.META.langs = " + JSON.stringify(langs) + ";\n");
  for (const l of langs) { if (l === "fr" || l === LG) continue; const op = path.join(dir, "data." + l + ".js");
    fs.writeFileSync(op, fs.readFileSync(op, "utf8").replace(/"langs":\[[^\]]*\]/, '"langs":' + JSON.stringify(langs))); }
  /* jeu.json : textes allemands de la carte */
  const jp = path.join(dir, "jeu.json");
  if (fs.existsSync(jp)) {
    const j = JSON.parse(fs.readFileSync(jp, "utf8"));
    const n = de.OBJ.reduce((s, o) => s + o.ch.length, 0), cases = de.OBJ.reduce((s, o) => s + o.ch.filter(c => c.k === "case").length, 0);
    const mod = j.module || (de.META.title.split(" ")[0]);
    if (LG === "it") j.it = { titre: de.META.title, sous_titre: "Impiegato/a in logistica AFC · Modulo " + mod, duree: "10 min per serie",
      description: `${de.OBJ.length} obiettivi del modulo ${mod} e ${n} esercizi, di cui il ${Math.round(100 * cases / n)} % casi pratici del lavoro quotidiano. Tre modalità: allenamento per obiettivo, esame di prova a tempo con nota da 1 a 6, ripasso mirato degli errori.`,
      contenu: de.OBJ.map(o => ({ titre: o.code + " · " + o.t, objectifs: [o.g] })) };
    else j.de = { titre: de.META.title, sous_titre: "Logistiker/-in EFZ · Modul " + mod, duree: "10 Min. pro Serie",
      description: `${de.OBJ.length} Lernziele des Moduls ${mod} und ${n} Aufgaben, davon ${Math.round(100 * cases / n)} % Praxisfälle aus dem Berufsalltag. Drei Modi: Training pro Lernziel, Probeprüfung mit Zeitlimit und Note von 1 bis 6, gezielte Wiederholung der Fehler.`,
      contenu: de.OBJ.map(o => ({ titre: o.code + " · " + o.t, objectifs: [o.g] })) };
    fs.writeFileSync(jp, JSON.stringify(j, null, 1));
  }
  console.log(`data.${LG}.js : ${de.OBJ.length} objectifs, ${de.OBJ.reduce((s, o) => s + o.ch.length, 0)} épreuves, ${tr.size} textes traduits`);
  if (warn.length) { console.log("À VÉRIFIER :"); warn.forEach(w => console.log("  " + w)); }
  control(dir);
}
function control(dir) {
  const fr = load(path.join(dir, "data.js")), de = load(path.join(dir, "data." + LG + ".js")); const err = [];
  if (fr.META.key !== de.META.key) err.push("META.key différente");
  if (fr.OBJ.length !== de.OBJ.length) err.push("nombre d'objectifs différent");
  fr.OBJ.forEach((o, oi) => {
    const p = de.OBJ[oi]; if (!p) return;
    if (o.code !== p.code || o.ch.length !== p.ch.length) err.push(`objectif ${oi} : code ou nombre d'épreuves différent`);
    o.ch.forEach((c, ci) => { const x = p.ch[ci]; if (!x) return;
      const shape = y => JSON.stringify([y.k, y.n, y.tol, y.v, y.img, (y.a || []).length, (y.good || []).length, (y.bad || []).length, (y.p || []).length, (y.c || []).length, (y.it || []).map(i => i[1]), y.k === "pickimg" ? y.a : 0]);
      if (shape(c) !== shape(x)) err.push(`${o.code}#${ci} : structure différente`); });
  });
  if (fr.LEVELS.map(l => l[0]).join() !== de.LEVELS.map(l => l[0]).join()) err.push("paliers de niveaux différents");
  console.log(err.length ? "CONTRÔLE : " + err.length + " écart(s)\n  " + err.slice(0, 15).join("\n  ") : "contrôle : FR et " + LG.toUpperCase() + " alignés");
  if (err.length) process.exitCode = 1;
}

const [cmd, dir, f, lg] = process.argv.slice(2);
if (lg) LG = lg; else if (cmd === "controle" && f) LG = f;
if (cmd === "feuille") { for (const [v, n] of sheet(dir)) console.log(n + "|" + v); }
else if (cmd === "construire") build(dir, f);
else if (cmd === "controle") control(dir);
else { console.error("usage : feuille|construire|controle <dossier_jeu> [feuille]"); process.exit(2); }

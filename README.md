# Jeux de révision – Logistique

Jeux de révision LogiProf pour les apprenti·e·s **logisticien·ne·s CFC**, et l’extension WordPress qui les installe sur votre site, avec mises à jour automatiques.

- **19 jeux** (modules M101 à M110, M201 à M209), un dossier par jeu dans [`jeux/`](jeux/).
- Chaque jeu : entraînement par objectif, examen blanc noté sur 6, révision ciblée des erreurs, progression enregistrée sur le compte de l’élève.
- L’extension s’installe une seule fois ; chaque nouvelle version publiée ici arrive automatiquement sur le site.

## Installer l’extension

1. Ouvrez la page **[Releases](https://github.com/logiprof/jeux-revisions-logistique/releases/latest)** et téléchargez **`jeux-revisions-logistique.zip`** (pas le « Source code »).
2. Dans WordPress : **Extensions → Ajouter → Téléverser une extension**, choisissez le zip, puis **Activer**.
3. Si vous aviez installé les anciennes extensions « Jeu de révision – Mxxx », un bandeau propose de les désactiver. Les progressions des élèves sont conservées.

La liste des shortcodes est aussi dans **Réglages → Jeux logistique**.

## Shortcodes

| Shortcode | Affiche |
|---|---|
| `[jeux_logistique]` | Tout le catalogue |
| `[jeux_logistique modules="M1"]` | Les modules M101 à M110 (`M2` pour M201 à M209, `M3` pour M301 à M312) |
| `[jeux_logistique modules="M101,M203"]` | Seulement les modules choisis |
| `[jeu_m101]`, `[jeu_m102]`… | Un seul jeu (voir le tableau ci-dessous) |
| `[jeu_revision id="m101-histoire-logistique"]` | Un seul jeu, par son identifiant |

| Module | Jeu | Shortcode | Objectifs | Épreuves |
|---|---|---|---|---|
| M101 | Histoire de la logistique | `[jeu_m101]` | 4 | 100 |
| M102 | Structure de la logistique | `[jeu_m102]` | 5 | 125 |
| M103 | Tâches et objectifs de la logistique | `[jeu_m103]` | 3 | 76 |
| M104 | Flux de marchandises | `[jeu_m104]` | 5 | 125 |
| M105 | Marchandise | `[jeu_m105]` | 2 | 64 |
| M106 | L’élimination des déchets CH | `[jeu_m106]` | 5 | 133 |
| M107 | Les catégories de déchets CH | `[jeu_m107]` | 4 | 109 |
| M108 | L’élimination globale | `[jeu_m108]` | 3 | 81 |
| M109 | Accès et protection des données | `[jeu_m109]` | 5 | 139 |
| M110 | Définition de la gestion des marchandises | `[jeu_m110]` | 3 | 82 |
| M201 | Le client | `[jeu_m201]` | 3 | 77 |
| M202 | L’attitude personnelle | `[jeu_m202]` | 4 | 105 |
| M203 | Le défi physique dans le monde du travail | `[jeu_m203]` | 8 | 202 |
| M204 | Le marché | `[jeu_m204]` | 7 | 175 |
| M205 | Le marketing | `[jeu_m205]` | 7 | 175 |
| M206 | Communication | `[jeu_m206]` | 3 | 76 |
| M207 | L’avant vente | `[jeu_m207]` | 3 | 76 |
| M208 | Le service à la vente | `[jeu_m208]` | 3 | 77 |
| M209 | SAV Service après-vente | `[jeu_m209]` | 3 | 75 |

## Mises à jour automatiques

L’extension lit la dernière *release* de ce dépôt (en-tête `Update URI`). Quand une version plus récente existe, WordPress la propose dans **Extensions** et l’installe automatiquement si l’option est cochée dans **Réglages → Jeux logistique** (cochée par défaut). Le bouton **Rechercher une mise à jour maintenant** force la vérification.

### Publier une nouvelle version

1. Modifiez ou ajoutez les jeux dans `jeux/`.
2. Augmentez le numéro de version aux trois endroits : l’en-tête `Version` et la constante `JRL_VERSION` de `jeux-revisions-logistique.php`, et `Stable tag` dans `readme.txt` (ajoutez une ligne dans « Changelog »).
3. Poussez (ou fusionnez) sur `main`.

L’action GitHub **Publier une version** vérifie les numéros, construit `jeux-revisions-logistique.zip` et crée la release `vX.Y.Z` si elle n’existe pas encore. Un push sans changement de version ne publie rien ; pour reconstruire le zip de la version courante, lancez l’action à la main (onglet **Actions → Publier une version → Run workflow**). Les sites se mettent à jour dans les heures qui suivent.

## Ajouter un jeu

Créez un dossier `jeux/<identifiant>/` (ex. `m301-transport`) contenant :

- `index.html`, `data.js`, `img/`, `fonts/` : le jeu, version WordPress (polices Poppins locales) ;
- `logo.svg` : le pictogramme de la carte ;
- `jeu.json` : la carte du catalogue (`module`, `shortcode`, `titre`, `sous_titre`, `duree`, `description`, `contenu`, `couleur`, `version`) ;
- facultatif : `dossier.pdf` et `corrige.pdf`, affichés sous le bouton du jeu.

Le jeu apparaît automatiquement dans le catalogue et reçoit son shortcode. Ne changez jamais l’identifiant (nom du dossier) d’un jeu publié : les progressions des élèves y sont rattachées.

## Données des élèves

Progression, historique et bilans sont enregistrés dans la base du site (tables `jdr_progression`, `jdr_historique`, `jdr_sessions`), par identifiant de jeu. Supprimer ou mettre à jour l’extension ne les efface pas, sauf si l’effacement a été demandé dans **Outils → Jeux de révision**. Aucun jeu n’envoie d’e-mail.

## Structure

```
jeux-revisions-logistique.php   extension (catalogue, shortcodes)
includes/catalogue.php          moteur commun des jeux de révision (1.7.3)
includes/updater.php            mises à jour depuis GitHub
includes/admin.php              Réglages → Jeux logistique
assets/                         lanceur des jeux, icône
jeux/<identifiant>/             un dossier par jeu
outils/construire_zip.sh        construit le zip de l’extension
.github/workflows/release.yml   publication automatique des versions
```

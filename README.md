# Jeux de révision – Logistique

Jeux de révision LogiProf pour les apprenti·e·s **logisticien·ne·s CFC**, et l’extension WordPress qui les installe sur votre site, avec mises à jour automatiques.

- **68 jeux** (modules M101 à M110, M201 à M209, M301 à M312, M401 à M410, M501 à M506, M601 à M612, M701 à M705, M801 à M809), un dossier par jeu dans [`jeux/`](jeux/).
- Chaque jeu : entraînement par objectif, examen blanc noté sur 6, révision ciblée des erreurs, progression enregistrée sur le compte de l’élève.
- **Bilingue français / allemand** : chaque jeu existe dans les deux langues (bouton **FR | DE** dans le jeu) ; la progression de l’élève est la même dans les deux langues.
- L’extension s’installe une seule fois ; chaque nouvelle version publiée ici arrive automatiquement sur le site.

## Installer l’extension

1. Ouvrez la page **[Releases](https://github.com/logiprof/jeux-revisions-logistique/releases/latest)** et téléchargez **`jeux-revisions-logistique.zip`** (pas le « Source code »).
2. Dans WordPress : **Extensions → Ajouter → Téléverser une extension**, choisissez le zip, puis **Activer**.
3. Si vous aviez installé les anciennes extensions « Jeu de révision – Mxxx », un bandeau propose de les désactiver. Les progressions des élèves sont conservées.

La liste des shortcodes est aussi dans le menu **Jeux logistique** (barre latérale de l’administration).

## Shortcodes

| Shortcode | Affiche |
|---|---|
| `[jeux_logistique]` | Tout le catalogue |
| `[jeux_logistique modules="M1"]` | Les modules M101 à M110 (`M2` pour M201 à M209, `M3` pour M301 à M312) |
| `[jeux_logistique modules="M101,M203"]` | Seulement les modules choisis |
| `[jeu_m101]`, `[jeu_m102]`… | Un seul jeu (voir le tableau ci-dessous) |
| `[jeu_revision id="m101-histoire-logistique"]` | Un seul jeu, par son identifiant |
| `[jeux_logistique langue="de"]` | Le catalogue en allemand (fonctionne aussi avec `modules="…"`) |
| `[jeu_m101 langue="de"]` | Un seul jeu, ouvert directement en allemand |

Sans `langue`, le jeu s’ouvre en français et l’élève peut passer à l’allemand avec le bouton **FR | DE** (son choix est mémorisé). Avec `langue="de"`, la carte, la page du jeu et le jeu sont en allemand.

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
| M301 | La logistique d’approvisionnement | `[jeu_m301]` | 3 | 76 |
| M302 | L’approvisionnement de marchandises | `[jeu_m302]` | 3 | 75 |
| M303 | Processus de réception des marchandises | `[jeu_m303]` | 3 | 75 |
| M304 | Identification de la livraison | `[jeu_m304]` | 4 | 100 |
| M305 | Déchargement des marchandises | `[jeu_m305]` | 4 | 100 |
| M306 | Contrôle des contenants | `[jeu_m306]` | 4 | 100 |
| M307 | Contrôle sommaire et traitement des dommages | `[jeu_m307]` | 3 | 75 |
| M308 | Les contrôles de quantités | `[jeu_m308]` | 3 | 75 |
| M309 | Contrôle de la qualité | `[jeu_m309]` | 3 | 75 |
| M310 | Préparation à la mise en stock | `[jeu_m310]` | 3 | 75 |
| M311 | Les concepts de l’approvisionnement | `[jeu_m311]` | 4 | 100 |
| M312 | Données de stockage | `[jeu_m312]` | 4 | 100 |
| M401 | Le rôle du stockage | `[jeu_m401]` | 3 | 75 |
| M402 | Les genres de stockage | `[jeu_m402]` | 3 | 75 |
| M403 | Les formes de stockage | `[jeu_m403]` | 4 | 100 |
| M404 | Prescriptions de stockage | `[jeu_m404]` | 3 | 75 |
| M405 | Dangers dans les entrepôts | `[jeu_m405]` | 4 | 100 |
| M406 | Principes de stockage | `[jeu_m406]` | 3 | 75 |
| M407 | Moyens de transport | `[jeu_m407]` | 4 | 100 |
| M408 | Organisation de l’entrepôt | `[jeu_m408]` | 6 | 150 |
| M409 | Les engins de manutention | `[jeu_m409]` | 4 | 100 |
| M410 | Les dispositifs de convoyage | `[jeu_m410]` | 4 | 100 |
| M501 | La production | `[jeu_m501]` | 3 | 75 |
| M502 | La logistique de production | `[jeu_m502]` | 3 | 75 |
| M503 | Organisation de la production | `[jeu_m503]` | 3 | 75 |
| M504 | Le flux de matériel | `[jeu_m504]` | 4 | 100 |
| M505 | Planification et contrôle de la production (PCP) | `[jeu_m505]` | 4 | 100 |
| M506 | Assurance qualité (AQ) dans la production | `[jeu_m506]` | 4 | 100 |
| M601 | La préparation de commandes | `[jeu_m601]` | 3 | 75 |
| M602 | Les emballages | `[jeu_m602]` | 5 | 125 |
| M603 | L’arrimage des marchandises | `[jeu_m603]` | 3 | 75 |
| M604 | Les systèmes de distribution | `[jeu_m604]` | 3 | 75 |
| M605 | Mode d’envoi postal | `[jeu_m605]` | 4 | 100 |
| M606 | Le transport routier | `[jeu_m606]` | 3 | 75 |
| M607 | Le transport ferroviaire | `[jeu_m607]` | 3 | 75 |
| M608 | Le transport aérien | `[jeu_m608]` | 4 | 100 |
| M609 | Le transport maritime | `[jeu_m609]` | 3 | 89 |
| M610 | Le transport combiné | `[jeu_m610]` | 3 | 81 |
| M611 | La préparation de commandes | `[jeu_m611]` | 6 | 162 |
| M612 | La planification des transports | `[jeu_m612]` | 3 | 85 |
| M701 | L’inventaire | `[jeu_m701]` | 3 | 77 |
| M702 | Les coûts de stockage | `[jeu_m702]` | 3 | 78 |
| M703 | Le coût du personnel | `[jeu_m703]` | 3 | 81 |
| M704 | Les indicateurs logistiques | `[jeu_m704]` | 3 | 85 |
| M705 | La rentabilité de l’entrepôt | `[jeu_m705]` | 3 | 86 |
| M801 | Identification des marchandises | `[jeu_m801]` | 3 | 87 |
| M802 | Le transport | `[jeu_m802]` | 3 | 80 |
| M803 | Logiciel d’exploitation | `[jeu_m803]` | 3 | 81 |
| M809 | Poste de contrôle | `[jeu_m809]` | 2 | 54 |

## Mises à jour automatiques

L’extension lit la dernière *release* de ce dépôt (en-tête `Update URI`). Quand une version plus récente existe, WordPress la propose dans **Extensions** et l’installe automatiquement si l’option est cochée dans le menu **Jeux logistique** (barre latérale de l’administration) (cochée par défaut). Le bouton **Rechercher une mise à jour maintenant** force la vérification.

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
includes/admin.php              menu Jeux logistique
assets/                         lanceur des jeux, icône
jeux/<identifiant>/             un dossier par jeu
outils/construire_zip.sh        construit le zip de l’extension
.github/workflows/release.yml   publication automatique des versions
```

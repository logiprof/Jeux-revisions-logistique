=== Jeux de révision – Logistique ===
Contributors: logiprof
Tags: formation, quiz, révision, logistique, jeux
Requires at least: 6.0
Tested up to: 6.8
Requires PHP: 7.4
Stable tag: 2.21.0
License: GPL-2.0-or-later

Catalogue des jeux de révision LogiProf pour logisticien·ne·s CFC (69 jeux, modules M101 à M110, M201 à M209, M301 à M312, M401 à M410, M501 à M506, M601 à M612, M701 à M705, M801 à M809, mathématiques 4 à 8), avec mises à jour automatiques depuis GitHub.

== Description ==

Chaque jeu propose un entraînement par objectif, un examen blanc chronométré noté sur 6 et une révision ciblée des erreurs. Les élèves doivent être connectés : leur progression est enregistrée sur leur compte. Aucun jeu n’envoie d’e-mail.

Shortcodes :

* [jeux_logistique] : tout le catalogue ;
* [jeux_logistique modules="M1"] : les modules M101 à M110 ;
* [jeux_logistique modules="M101,M203"] : les modules choisis ;
* [jeu_m101], [jeu_m102]… : un seul jeu (liste complète dans menu Jeux logistique).

== Installation ==

1. Téléchargez jeux-revisions-logistique.zip depuis https://github.com/logiprof/jeux-revisions-logistique/releases/latest
2. Extensions > Ajouter > Téléverser une extension, puis Activer.
3. Désactivez les anciennes extensions « Jeu de révision – Mxxx » si un bandeau vous le propose : les progressions sont conservées.

== Changelog ==

= 2.21.0 =
* Version italienne des jeux M401 à M410

= 2.20.0 =
* Version italienne des jeux M301 à M312 ; image de titre réelle du jeu de mathématiques

= 2.19.0 =
* Version italienne des jeux M201 à M209

= 2.18.0 =
* Version italienne des jeux M107 à M110 (images italiennes pour M109)

= 2.17.0 =
* Versions italiennes : M102 à M106.

= 2.16.0 =
* Italien : menu de langue FR · DE · IT dans les jeux, shortcodes langue="it", cartes et classement en italien (moteur 1.9.0). Premier jeu traduit : M101 – Storia della logistica ; les autres suivent.

= 2.15.0 =
* Nouveau jeu Mathématiques – Applications professionnelles (modules 4 à 8 : règle de trois, pourcentages, taux d'occupation et de chargement, palettisation, charge utile), 152 épreuves, en français et en allemand. Shortcode [jeu_maths_applications]

= 2.14.0 =
* Export des statistiques : rapport avec graphiques à imprimer ou enregistrer en PDF (sans nom d'élève, classes anonymisables), chaque graphique en PNG pour les présentations, tableaux par jeu et par classe en CSV pour Excel

= 2.13.0 =
* Statistiques des jeux : élèves actifs, temps de jeu, réussite, notes d'examen, activité par jour, tableau par jeu et par classe Sensei avec détail des élèves ; classes favorites par enseignant·e ; accès réglable par rôle (enseignant·e·s sans droit d'édition : menu Statistiques seul)

= 2.12.0 =
* Classement des groupes Sensei : podium de la semaine au-dessus du catalogue, bouton Classement dans chaque jeu (semaine / depuis le début, ce jeu / tous les jeux)

= 2.11.0 =
* Gestion des jeux : activer / masquer, statistiques par jeu, textes et couleur des cartes, aperçu, remise à zéro de la progression d'un élève

= 2.10.0 =
* Menu « Jeux logistique » dans la barre latérale de l'administration (Shortcodes et réglages, Regroupements, Suivi des élèves)

= 2.9.0 =
* Regroupements de modules : Réglages > Jeux logistique, un shortcode par regroupement ([jeux_<nom>] ou [jeux_logistique groupe="…"])

= 2.8.0 =
* Cartes : titre sur toute la largeur sous l'icône. Réglages > Jeux logistique > Affichage du catalogue : jeux côte à côte (1 à 4), durée, progression et bouton Objectifs affichables ; attribut colonnes="…"

= 2.7.3 =
* Cartes du catalogue sans le paragraphe de description

= 2.7.2 =
* Cartes du catalogue : le bouton Objectifs déplie une liste à puces, un objectif par ligne (code et titre)

= 2.7.1 =
* Mises à jour détectées plus vite : « Vérifier à nouveau » relit GitHub, cache de 2 h

= 2.7.0 =
* Ordinateur : plein écran au lancement et bouton Plein écran, page plus large ; objectifs en liste à puces, un par ligne

= 2.6.0 =
* Versions allemandes : M801 à M809 — les 68 jeux sont bilingues FR/DE

= 2.5.0 =
* Versions allemandes : M701 à M705

= 2.4.0 =
* Versions allemandes : M601 à M612

= 2.3.0 =
* Versions allemandes : M401 à M410 et M501 à M506

= 2.2.0 =
* M301 à M312 en allemand ; corrections de cas grammaticaux (M2)

= 2.1.0 =
* Version bilingue FR/DE : moteur 1.8.0 (bouton FR | DE, langue="de"), M101 à M110 et M201 à M209 en allemand

= 2.0.0 =
* M801, M802, M803 et M809 : 4 nouveaux jeux (identification des marchandises, transport, logiciel d’exploitation, poste de contrôle)

= 1.9.0 =
* M701 à M705 : 5 nouveaux jeux (inventaire, coûts de stockage, coût du personnel, indicateurs logistiques, rentabilité de l’entrepôt)

= 1.8.0 =
* M601 à M612 : 11 nouveaux jeux (préparation, emballages, arrimage, distribution, postal, route, rail, air, mer, combiné, préparation de commandes, planification)

= 1.7.0 =
* Série M5 : jeux M501 à M506 (production, logistique de production, organisation, flux de matériel, PCP, assurance qualité)

= 1.6.0 =
* Série M4 : jeux M401 à M410 (stockage, dangers, principes, transport, organisation de l’entrepôt, engins, convoyage)

= 1.5.0 =
* Ajout de M311 (les concepts de l’approvisionnement) et M312 (données de stockage) : tous les modules M2 et M3 sont disponibles.

= 1.4.0 =
* Ajout de M308 (contrôles des quantités, oublié dans le journal 1.3.0), M309 (contrôle de la qualité) et M310 (préparation à la mise en stock).

= 1.3.0 =
* 3 nouveaux jeux : M305 Déchargement des marchandises, M306 Contrôle des contenants, M307 Contrôle sommaire et traitement des dommages.

= 1.2.0 =
* 4 nouveaux jeux : M301 La logistique d’approvisionnement, M302 L’approvisionnement de marchandises, M303 Processus de réception des marchandises, M304 Identification de la livraison.

= 1.1.0 =
* 4 nouveaux jeux : M206 Communication, M207 L’avant vente, M208 Le service à la vente, M209 SAV Service après-vente.

= 1.0.1 =
* Mises à jour détectées même si le serveur ne joint pas wordpress.org.

= 1.0.0 =
* Première version : 15 jeux (M101 à M110, M201 à M205), shortcode de catalogue et shortcode par jeu, mises à jour automatiques depuis GitHub.

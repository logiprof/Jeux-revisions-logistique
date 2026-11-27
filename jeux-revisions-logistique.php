<?php
/**
 * Plugin Name:       Jeux de révision – Logistique
 * Plugin URI:        https://github.com/logiprof/jeux-revisions-logistique
 * Description:       Catalogue des jeux de révision LogiProf pour logisticien·ne·s CFC (modules M101 à M205). Shortcodes : [jeux_logistique] pour tout le catalogue, [jeu_m101], [jeu_m102]… pour un seul jeu. Mises à jour automatiques depuis GitHub.
 * Version:           2.25.0
 * Requires at least: 6.0
 * Requires PHP:      7.4
 * Author:            LogiProf
 * Author URI:        https://logiprof.fontes-oliveira.ch
 * License:           GPL-2.0-or-later
 * Update URI:        https://github.com/logiprof/jeux-revisions-logistique
 * Text Domain:       jeux-revisions-logistique
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

define( 'JRL_VERSION', '2.25.0' );
define( 'JRL_FILE', __FILE__ );
define( 'JRL_DIR', __DIR__ );
define( 'JRL_REPO', 'logiprof/jeux-revisions-logistique' );
define( 'JRL_ASSET', 'jeux-revisions-logistique.zip' );

/* Moteur commun des jeux de révision (cartes, page du jeu, progression en base, suivi) */
require_once __DIR__ . '/includes/catalogue.php';
/* Mises à jour depuis les « releases » GitHub */
require_once __DIR__ . '/includes/updater.php';
/* Menu Jeux logistique (shortcodes, affichage, regroupements, mises à jour) */
require_once __DIR__ . '/includes/admin.php';
/* Regroupements de modules (un shortcode par regroupement) */
require_once __DIR__ . '/includes/groupes.php';
/* Gestion des jeux : activer / masquer, cartes, statistiques, remise à zéro */
require_once __DIR__ . '/includes/gestion.php';
/* Classement par groupe Sensei (podium du catalogue, bouton Classement dans les jeux) */
require_once __DIR__ . '/includes/classement.php';
/* Statistiques : élèves actifs, temps de jeu, scores par classe, classes favorites par enseignant·e */
require_once __DIR__ . '/includes/statistiques.php';
require_once __DIR__ . '/includes/rapport.php';

/**
 * Jeux livrés par l'extension : un dossier par jeu dans jeux/<identifiant>/ avec index.html, data.js, jeu.json et logo.svg.
 * Pour ajouter un jeu, il suffit d'ajouter son dossier : il apparaît automatiquement dans le catalogue.
 */
function jrl_jeux() {
	static $jeux = null;
	if ( null !== $jeux ) { return $jeux; }
	$jeux = array();
	foreach ( (array) glob( JRL_DIR . '/jeux/*/jeu.json' ) as $f ) {
		$dir = dirname( $f );
		if ( ! is_readable( $dir . '/index.html' ) ) { continue; }
		$d = json_decode( (string) file_get_contents( $f ), true );
		if ( ! is_array( $d ) || empty( $d['titre'] ) ) { continue; }
		$slug = sanitize_key( basename( $dir ) );
		$d['slug'] = $slug;
		if ( empty( $d['module'] ) ) { $d['module'] = strtoupper( strtok( $slug, '-' ) ); }
		if ( empty( $d['shortcode'] ) ) { $d['shortcode'] = 'jeu_' . strtolower( $d['module'] ); }
		$jeux[ $slug ] = $d;
	}
	uksort( $jeux, 'strnatcasecmp' );
	return $jeux;
}

/* Inscription des jeux dans le moteur commun (priorité 20 : remplace un ancien jeu installé séparément sous le même identifiant) */
add_filter( 'jdr_jeux', function ( $jeux ) {
	foreach ( jrl_jeux() as $slug => $d ) {
		$base = 'jeux/' . $slug . '/';
		$pdf  = function ( $nom ) use ( $slug, $base ) { return file_exists( JRL_DIR . '/' . $base . $nom ) ? plugins_url( $base . $nom, JRL_FILE ) : ''; };
		$jeux[ $slug ] = array(
			'titre'       => (string) $d['titre'],
			'sous_titre'  => (string) ( $d['sous_titre'] ?? '' ),
			'duree'       => (string) ( $d['duree'] ?? '' ),
			'description' => (string) ( $d['description'] ?? '' ),
			'contenu'     => (array) ( $d['contenu'] ?? array() ),
			'logo'        => plugins_url( $base . 'logo.svg', JRL_FILE ),
			'url'         => plugins_url( $base . 'index.html', JRL_FILE ),
			'couleur'     => (string) ( $d['couleur'] ?? '#067030' ),
			'bouton'      => '▶ Commencer',
			'version'     => (string) ( $d['version'] ?? JRL_VERSION ),
			/* dossier de formation : jeux/<identifiant>/dossier.pdf et corrige.pdf, affichés sous le bouton s'ils sont présents */
			'dossier'     => $pdf( 'dossier.pdf' ),
			'corrige'     => $pdf( 'corrige.pdf' ),
			/* versions allemande et italienne : textes de la carte (jeu.json, clés « de » et « it ») ; le jeu lui-même est index.de.html / index.it.html */
			'i18n'        => array_filter( array(
				'de' => ( ! empty( $d['de'] ) && is_array( $d['de'] ) && file_exists( JRL_DIR . '/' . $base . 'index.de.html' ) ) ? array_merge( array( 'bouton' => '▶ Starten', 'bouton_suite' => '▶ Fortsetzen', 'bouton_connexion' => 'Anmelden, um zu spielen' ), $d['de'] ) : array(),
				'it' => ( ! empty( $d['it'] ) && is_array( $d['it'] ) && file_exists( JRL_DIR . '/' . $base . 'index.it.html' ) ) ? array_merge( array( 'bouton' => '▶ Inizia', 'bouton_suite' => '▶ Continua', 'bouton_connexion' => 'Accedere per giocare' ), $d['it'] ) : array(),
			) ),
		);
	}
	return $jeux;
}, 20 );

/* ---------- Shortcodes ---------- */
add_action( 'init', function () {
	add_shortcode( 'jeux_logistique', 'jrl_shortcode_catalogue' );
	foreach ( jrl_jeux() as $slug => $d ) {
		$tag = sanitize_key( $d['shortcode'] );
		if ( '' === $tag || shortcode_exists( $tag ) ) { continue; }
		add_shortcode( $tag, function ( $atts = array() ) use ( $slug ) {
			$langue = is_array( $atts ) && ! empty( $atts['langue'] ) ? (string) $atts['langue'] : '';
			if ( function_exists( 'jrl_est_masque' ) && jrl_est_masque( $slug ) ) { return current_user_can( 'edit_posts' ) ? '<p><em>Ce jeu est masqué (menu Jeux logistique › Gestion des jeux) : les élèves ne le voient pas.</em></p>' : ''; }
			return function_exists( 'jdr_shortcode_jeu' ) ? '<div class="' . esc_attr( jrl_aff_classes() ) . '">' . jdr_shortcode_jeu( array( 'id' => $slug, 'langue' => $langue ) ) . '</div>' : '';
		} );
	}
}, 20 );

/**
 * [jeux_logistique] : tout le catalogue de l'extension.
 * [jeux_logistique modules="M1"] : seulement les modules qui commencent par M1 (M101 à M110).
 * [jeux_logistique modules="M101,M203"] : seulement ces modules.
 * [jeux_logistique groupe="modules-1re-annee"] ou [jeux_modules_1re_annee] : un regroupement (menu Jeux logistique).
 * [jeux_logistique podium="non"] : sans le podium « Classement de la semaine » (affiché aux élèves d'un groupe Sensei).
 * [jeux_logistique colonnes="3"] : 3 jeux côte à côte (1 à 4 ; sinon le réglage « Affichage du catalogue »).
 */
function jrl_shortcode_catalogue( $atts ) {
	if ( ! function_exists( 'jdr_card' ) ) { return ''; }
	$a = shortcode_atts( array( 'modules' => '', 'langue' => '', 'colonnes' => '', 'groupe' => '', 'podium' => '' ), $atts, 'jeux_logistique' );
	$filtres = array_filter( array_map( 'trim', explode( ',', strtoupper( (string) $a['modules'] ) ) ) );
	$groupe = null;
	if ( '' !== (string) $a['groupe'] ) {
		$groupe = function_exists( 'jrl_groupe' ) ? jrl_groupe( $a['groupe'] ) : null;
		if ( ! $groupe ) { return current_user_can( 'edit_posts' ) ? '<p><em>Regroupement introuvable : vérifiez le shortcode dans le menu Jeux logistique.</em></p>' : ''; }
		if ( '' === (string) $a['colonnes'] && ! empty( $groupe['colonnes'] ) ) { $a['colonnes'] = $groupe['colonnes']; }
	}
	$tous = jdr_jeux();
	$cartes = array();
	foreach ( jrl_jeux() as $slug => $d ) {
		if ( ! isset( $tous[ $slug ] ) ) { continue; }
		if ( $groupe && ! in_array( $slug, (array) $groupe['jeux'], true ) ) { continue; }
		if ( $filtres ) {
			$garde = false;
			foreach ( $filtres as $f ) { if ( 0 === strpos( strtoupper( $d['module'] ), $f ) ) { $garde = true; break; } }
			if ( ! $garde ) { continue; }
		}
		$cartes[] = array( $slug, $tous[ $slug ] );
	}
	if ( ! $cartes ) { return current_user_can( 'edit_posts' ) ? '<p><em>Aucun jeu ne correspond à ce shortcode.</em></p>' : ''; }
	jdr_enqueue();
	$prev = function_exists( 'jdr_lang' ) ? jdr_lang() : 'fr';
	if ( '' !== $a['langue'] && function_exists( 'jdr_lang' ) ) { jdr_lang( $a['langue'] ); }
	$col = jrl_colonnes( $a['colonnes'] );
	$podium = ( 'non' !== strtolower( (string) $a['podium'] ) && function_exists( 'jrl_cl_podium_html' ) ) ? jrl_cl_podium_html() : '';
	$out = '<div class="' . esc_attr( jrl_aff_classes() ) . '">' . $podium . '<div class="jdr-grid' . ( 'auto' !== $col ? ' jdr-cols-' . $col : '' ) . '">';
	foreach ( $cartes as $c ) { $out .= jdr_card( $c[0], $c[1] ); }
	if ( function_exists( 'jdr_lang' ) ) { jdr_lang( $prev ); }
	return $out . '</div></div>';
}

/* ---------- Affichage (menu Jeux logistique > Affichage du catalogue) ---------- */
/** Nombre de jeux côte à côte : « auto » ou 1 à 4 (attribut colonnes="…" du shortcode, sinon le réglage). */
function jrl_colonnes( $attr = '' ) {
	$v = '' !== (string) $attr ? (string) $attr : (string) get_option( 'jrl_colonnes', 'auto' );
	return in_array( $v, array( '1', '2', '3', '4' ), true ) ? $v : 'auto';
}
/** Classes de l'enveloppe : éléments de la carte masqués selon les réglages. */
function jrl_aff_classes() {
	$c = 'jrl-cat';
	if ( '0' === get_option( 'jrl_aff_duree', '1' ) ) { $c .= ' jrl-no-duree'; }
	if ( '0' === get_option( 'jrl_aff_progression', '1' ) ) { $c .= ' jrl-no-prog'; }
	if ( '0' === get_option( 'jrl_aff_objectifs', '1' ) ) { $c .= ' jrl-no-obj'; }
	return $c;
}

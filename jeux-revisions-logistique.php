<?php
/**
 * Plugin Name:       Jeux de révision – Logistique
 * Plugin URI:        https://github.com/logiprof/jeux-revisions-logistique
 * Description:       Catalogue des jeux de révision LogiProf pour logisticien·ne·s CFC (modules M101 à M205). Shortcodes : [jeux_logistique] pour tout le catalogue, [jeu_m101], [jeu_m102]… pour un seul jeu. Mises à jour automatiques depuis GitHub.
 * Version:           2.3.0
 * Requires at least: 6.0
 * Requires PHP:      7.4
 * Author:            LogiProf
 * Author URI:        https://logiprof.fontes-oliveira.ch
 * License:           GPL-2.0-or-later
 * Update URI:        https://github.com/logiprof/jeux-revisions-logistique
 * Text Domain:       jeux-revisions-logistique
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

define( 'JRL_VERSION', '2.3.0' );
define( 'JRL_FILE', __FILE__ );
define( 'JRL_DIR', __DIR__ );
define( 'JRL_REPO', 'logiprof/jeux-revisions-logistique' );
define( 'JRL_ASSET', 'jeux-revisions-logistique.zip' );

/* Moteur commun des jeux de révision (cartes, page du jeu, progression en base, suivi) */
require_once __DIR__ . '/includes/catalogue.php';
/* Mises à jour depuis les « releases » GitHub */
require_once __DIR__ . '/includes/updater.php';
/* Page Réglages > Jeux logistique (liste des shortcodes) */
require_once __DIR__ . '/includes/admin.php';

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
			/* version allemande : textes de la carte (jeu.json, clé « de ») ; le jeu lui-même est index.de.html */
			'i18n'        => ( ! empty( $d['de'] ) && is_array( $d['de'] ) && file_exists( JRL_DIR . '/' . $base . 'index.de.html' ) ) ? array( 'de' => array_merge( array( 'bouton' => '▶ Starten', 'bouton_suite' => '▶ Fortsetzen', 'bouton_connexion' => 'Anmelden, um zu spielen' ), $d['de'] ) ) : array(),
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
			return function_exists( 'jdr_shortcode_jeu' ) ? jdr_shortcode_jeu( array( 'id' => $slug, 'langue' => $langue ) ) : '';
		} );
	}
}, 20 );

/**
 * [jeux_logistique] : tout le catalogue de l'extension.
 * [jeux_logistique modules="M1"] : seulement les modules qui commencent par M1 (M101 à M110).
 * [jeux_logistique modules="M101,M203"] : seulement ces modules.
 */
function jrl_shortcode_catalogue( $atts ) {
	if ( ! function_exists( 'jdr_card' ) ) { return ''; }
	$a = shortcode_atts( array( 'modules' => '', 'langue' => '' ), $atts, 'jeux_logistique' );
	$filtres = array_filter( array_map( 'trim', explode( ',', strtoupper( (string) $a['modules'] ) ) ) );
	$tous = jdr_jeux();
	$cartes = array();
	foreach ( jrl_jeux() as $slug => $d ) {
		if ( ! isset( $tous[ $slug ] ) ) { continue; }
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
	$out = '<div class="jdr-grid">';
	foreach ( $cartes as $c ) { $out .= jdr_card( $c[0], $c[1] ); }
	if ( function_exists( 'jdr_lang' ) ) { jdr_lang( $prev ); }
	return $out . '</div>';
}

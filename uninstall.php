<?php
/* Suppression de l'extension : les progressions des élèves sont CONSERVÉES, sauf si l'administrateur a demandé
   l'effacement des données (Outils > LogiPlay). */
if ( ! defined( 'WP_UNINSTALL_PLUGIN' ) ) { exit; }
delete_option( 'jrl_maj_auto' );
delete_site_transient( 'jrl_github_release' );
if ( '1' !== get_option( 'jdr_effacer_donnees', '0' ) ) { return; }
global $wpdb;
foreach ( (array) glob( __DIR__ . '/jeux/*/jeu.json' ) as $f ) {
	$slug = basename( dirname( $f ) );
	foreach ( array( 'jdr_progression', 'jdr_historique', 'jdr_sessions' ) as $t ) {
		$t = $wpdb->prefix . $t;
		if ( $wpdb->get_var( $wpdb->prepare( 'SHOW TABLES LIKE %s', $t ) ) === $t ) { $wpdb->delete( $t, array( 'jeu' => $slug ) ); }
	}
}

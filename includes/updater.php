<?php
/**
 * Mises à jour automatiques depuis GitHub (dépôt public logiprof/jeux-revisions-logistique).
 *
 * WordPress interroge « Update URI » (en-tête de l'extension) : le filtre update_plugins_github.com lit la dernière
 * « release » GitHub et propose le fichier jeux-revisions-logistique.zip qui y est joint. La mise à jour s'installe
 * ensuite comme celle de n'importe quelle extension, automatiquement si l'option est cochée (cochée par défaut).
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

/** Dernière release GitHub (mise en cache 6 h ; 1 h en cas d'échec). */
function jrl_remote( $forcer = false ) {
	$cle = 'jrl_github_release';
	$r = $forcer ? false : get_site_transient( $cle );
	if ( is_array( $r ) ) { return $r; }
	$r = array( 'ok' => false, 'erreur' => '' );
	$rep = wp_remote_get( 'https://api.github.com/repos/' . JRL_REPO . '/releases/latest', array(
		'timeout' => 12,
		'headers' => array( 'Accept' => 'application/vnd.github+json', 'User-Agent' => 'jeux-revisions-logistique/' . JRL_VERSION ),
	) );
	if ( is_wp_error( $rep ) ) {
		$r['erreur'] = $rep->get_error_message();
	} elseif ( 200 !== (int) wp_remote_retrieve_response_code( $rep ) ) {
		$r['erreur'] = 'GitHub a répondu ' . (int) wp_remote_retrieve_response_code( $rep );
	} else {
		$b = json_decode( wp_remote_retrieve_body( $rep ), true );
		$paquet = '';
		foreach ( (array) ( $b['assets'] ?? array() ) as $a ) {
			if ( isset( $a['name'], $a['browser_download_url'] ) && JRL_ASSET === $a['name'] ) { $paquet = $a['browser_download_url']; }
		}
		$r = array(
			'ok'      => '' !== $paquet,
			'erreur'  => '' === $paquet ? 'La dernière version GitHub ne contient pas le fichier ' . JRL_ASSET . '.' : '',
			'version' => ltrim( (string) ( $b['tag_name'] ?? '' ), 'vV' ),
			'paquet'  => $paquet,
			'notes'   => (string) ( $b['body'] ?? '' ),
			'date'    => (string) ( $b['published_at'] ?? '' ),
			'page'    => (string) ( $b['html_url'] ?? '' ),
		);
	}
	set_site_transient( $cle, $r, $r['ok'] ? 6 * HOUR_IN_SECONDS : HOUR_IN_SECONDS );
	return $r;
}

/* Proposition de mise à jour (WordPress compare lui-même les versions) */
add_filter( 'update_plugins_github.com', function ( $update, $plugin_data, $plugin_file ) {
	if ( plugin_basename( JRL_FILE ) !== $plugin_file ) { return $update; }
	$r = jrl_remote();
	if ( empty( $r['ok'] ) || '' === $r['version'] ) { return $update; }
	return array(
		'id'           => 'https://github.com/' . JRL_REPO,
		'slug'         => 'jeux-revisions-logistique',
		'plugin'       => $plugin_file,
		'version'      => $r['version'],
		'new_version'  => $r['version'],
		'url'          => 'https://github.com/' . JRL_REPO,
		'package'      => $r['paquet'],
		'requires'     => '6.0',
		'requires_php' => '7.4',
		'tested'       => get_bloginfo( 'version' ),
		'icons'        => array( 'svg' => plugins_url( 'assets/icone.svg', JRL_FILE ), '1x' => plugins_url( 'assets/icone.svg', JRL_FILE ) ),
	);
}, 10, 3 );

/* Fenêtre « Afficher les détails » de la mise à jour */
add_filter( 'plugins_api', function ( $res, $action, $args ) {
	if ( 'plugin_information' !== $action || empty( $args->slug ) || 'jeux-revisions-logistique' !== $args->slug ) { return $res; }
	$r = jrl_remote();
	$nb = count( jrl_jeux() );
	return (object) array(
		'name'          => 'Jeux de révision – Logistique',
		'slug'          => 'jeux-revisions-logistique',
		'version'       => ! empty( $r['version'] ) ? $r['version'] : JRL_VERSION,
		'author'        => '<a href="https://logiprof.fontes-oliveira.ch">LogiProf</a>',
		'homepage'      => 'https://github.com/' . JRL_REPO,
		'requires'      => '6.0',
		'requires_php'  => '7.4',
		'tested'        => get_bloginfo( 'version' ),
		'last_updated'  => ! empty( $r['date'] ) ? $r['date'] : '',
		'download_link' => ! empty( $r['paquet'] ) ? $r['paquet'] : '',
		'sections'      => array(
			'description' => '<p>Catalogue des jeux de révision LogiProf pour logisticien·ne·s CFC (' . (int) $nb . ' jeux installés). Shortcode <code>[jeux_logistique]</code> pour tout le catalogue, <code>[jeu_m101]</code>… pour un seul jeu.</p>',
			'changelog'   => ! empty( $r['notes'] ) ? wpautop( esc_html( $r['notes'] ) ) : '<p>Voir les versions sur GitHub.</p>',
		),
		'banners'       => array(),
	);
}, 10, 3 );

/* Le dossier installé garde son nom, même si le zip GitHub en porte un autre (ex. jeux-revisions-logistique-main) */
add_filter( 'upgrader_source_selection', function ( $source, $remote_source, $upgrader, $extra = array() ) {
	if ( empty( $extra['plugin'] ) || plugin_basename( JRL_FILE ) !== $extra['plugin'] ) { return $source; }
	global $wp_filesystem;
	$voulu = trailingslashit( $remote_source ) . dirname( plugin_basename( JRL_FILE ) ) . '/';
	if ( untrailingslashit( $source ) === untrailingslashit( $voulu ) || ! $wp_filesystem ) { return $source; }
	return $wp_filesystem->move( $source, $voulu, true ) ? $voulu : $source;
}, 10, 4 );

/* Mises à jour automatiques (option « Installer automatiquement les mises à jour », cochée par défaut) */
add_filter( 'auto_update_plugin', function ( $update, $item ) {
	if ( isset( $item->plugin ) && plugin_basename( JRL_FILE ) === $item->plugin && '1' === get_option( 'jrl_maj_auto', '1' ) ) { return true; }
	return $update;
}, 10, 2 );

/* Après une mise à jour : on relira GitHub la prochaine fois */
add_action( 'upgrader_process_complete', function () { delete_site_transient( 'jrl_github_release' ); } );

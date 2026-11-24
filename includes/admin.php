<?php
/* Réglages > Jeux logistique : liste des jeux et de leurs shortcodes, mises à jour */
if ( ! defined( 'ABSPATH' ) ) { exit; }

add_action( 'admin_menu', function () {
	add_options_page( 'Jeux de révision – Logistique', 'Jeux logistique', 'edit_posts', 'jeux-logistique', 'jrl_admin_page' );
} );

add_filter( 'plugin_action_links_' . plugin_basename( JRL_FILE ), function ( $liens ) {
	array_unshift( $liens, '<a href="' . esc_url( admin_url( 'options-general.php?page=jeux-logistique' ) ) . '">Shortcodes</a>' );
	return $liens;
} );

/* Les anciennes extensions « Jeu de révision – Mxxx » font doublon : on propose de les désactiver */
function jrl_doublons() {
	if ( ! function_exists( 'is_plugin_active' ) ) { require_once ABSPATH . 'wp-admin/includes/plugin.php'; }
	$d = array();
	foreach ( array_keys( jrl_jeux() ) as $slug ) {
		$f = 'jeu-revision-' . $slug . '/jeu-revision-' . $slug . '.php';
		if ( is_plugin_active( $f ) ) { $d[] = $f; }
	}
	return $d;
}
add_action( 'admin_notices', function () {
	if ( ! current_user_can( 'activate_plugins' ) ) { return; }
	$d = jrl_doublons();
	if ( ! $d ) { return; }
	$url = wp_nonce_url( admin_url( 'options-general.php?page=jeux-logistique&jrl_desactiver=1' ), 'jrl_desactiver' );
	echo '<div class="notice notice-warning"><p><strong>Jeux de révision – Logistique :</strong> ' . esc_html( sprintf( '%d ancienne(s) extension(s) « Jeu de révision – Mxxx » sont encore actives. Les mêmes jeux sont maintenant fournis par cette extension. Les progressions des élèves sont conservées.', count( $d ) ) ) . ' <a class="button button-small" href="' . esc_url( $url ) . '">Désactiver les anciennes extensions</a></p></div>';
} );
add_action( 'admin_init', function () {
	if ( empty( $_GET['jrl_desactiver'] ) || ! current_user_can( 'activate_plugins' ) ) { return; }
	check_admin_referer( 'jrl_desactiver' );
	deactivate_plugins( jrl_doublons() );
	wp_safe_redirect( admin_url( 'options-general.php?page=jeux-logistique&jrl_ok=desactive' ) ); exit;
} );

add_action( 'admin_post_jrl_reglages', function () {
	if ( ! current_user_can( 'update_plugins' ) ) { wp_die( 'Accès refusé.' ); }
	check_admin_referer( 'jrl_reglages' );
	update_option( 'jrl_maj_auto', empty( $_POST['jrl_maj_auto'] ) ? '0' : '1' );
	$ok = 'reglages';
	if ( ! empty( $_POST['jrl_verifier'] ) ) {
		delete_site_transient( 'jrl_github_release' );
		jrl_remote( true );
		delete_site_transient( 'update_plugins' );
		wp_update_plugins();
		$ok = 'verifie';
	}
	wp_safe_redirect( admin_url( 'options-general.php?page=jeux-logistique&jrl_ok=' . $ok ) ); exit;
} );

function jrl_admin_page() {
	$jeux = jrl_jeux();
	$r = jrl_remote();
	$ok = isset( $_GET['jrl_ok'] ) ? sanitize_key( $_GET['jrl_ok'] ) : '';
	$msg = array( 'reglages' => 'Réglages enregistrés.', 'verifie' => 'GitHub a été consulté.', 'desactive' => 'Anciennes extensions désactivées.' );
	?>
	<div class="wrap">
		<h1>Jeux de révision – Logistique</h1>
		<?php if ( isset( $msg[ $ok ] ) ) : ?><div class="notice notice-success is-dismissible"><p><?php echo esc_html( $msg[ $ok ] ); ?></p></div><?php endif; ?>
		<p>Copiez un shortcode dans une page ou un article (bloc « Code court »). Les élèves doivent être connectés pour jouer ; leur progression est enregistrée sur leur compte.</p>

		<h2>Catalogue complet</h2>
		<table class="widefat striped" style="max-width:900px">
			<tbody>
				<tr><td style="width:42%"><code>[jeux_logistique]</code></td><td>Tous les jeux de l’extension (<?php echo (int) count( $jeux ); ?>).</td></tr>
				<tr><td><code>[jeux_logistique modules="M1"]</code></td><td>Seulement les modules M101 à M110 (M2 pour M201 à M205…).</td></tr>
				<tr><td><code>[jeux_logistique modules="M101,M203"]</code></td><td>Seulement les modules choisis.</td></tr>
				<tr><td><code>[jeux_logistique langue="de"]</code></td><td>Le catalogue en allemand (cartes et jeux). Fonctionne aussi avec <code>modules="…"</code> et pour un seul jeu : <code>[jeu_m101 langue="de"]</code>. Sans <code>langue</code>, l’élève peut changer de langue dans le jeu (bouton FR | DE) ; sa progression est la même dans les deux langues.</td></tr>
				<tr><td><code>[jeux_revision]</code></td><td>Tous les jeux de révision installés sur le site, y compris ceux d’autres extensions.</td></tr>
			</tbody>
		</table>

		<h2>Un jeu</h2>
		<table class="widefat striped" style="max-width:900px">
			<thead><tr><th>Module</th><th>Jeu</th><th>Shortcode</th><th>Épreuves</th></tr></thead>
			<tbody>
			<?php foreach ( $jeux as $slug => $d ) : ?>
				<tr>
					<td><strong><?php echo esc_html( $d['module'] ); ?></strong></td>
					<td><?php echo esc_html( $d['titre'] ); ?></td>
					<td><code>[<?php echo esc_html( $d['shortcode'] ); ?>]</code><br><small><code>[jeu_revision id="<?php echo esc_html( $slug ); ?>"]</code></small></td>
					<td><?php echo esc_html( preg_match( '/(\d+) épreuves/u', (string) ( $d['description'] ?? '' ), $m ) ? $m[1] : '' ); ?></td>
				</tr>
			<?php endforeach; ?>
			</tbody>
		</table>

		<h2>Mises à jour</h2>
		<p>Version installée : <strong><?php echo esc_html( JRL_VERSION ); ?></strong>.
		<?php if ( ! empty( $r['ok'] ) ) : ?>
			Dernière version sur GitHub : <strong><?php echo esc_html( $r['version'] ); ?></strong>
			<?php echo version_compare( $r['version'], JRL_VERSION, '>' ) ? ' — <a href="' . esc_url( admin_url( 'plugins.php' ) ) . '">mettre à jour</a>' : ' — à jour.'; ?>
		<?php else : ?>
			GitHub n’a pas pu être consulté<?php echo ! empty( $r['erreur'] ) ? ' (' . esc_html( $r['erreur'] ) . ')' : ''; ?>.
		<?php endif; ?>
		</p>
		<form method="post" action="<?php echo esc_url( admin_url( 'admin-post.php' ) ); ?>">
			<?php wp_nonce_field( 'jrl_reglages' ); ?>
			<input type="hidden" name="action" value="jrl_reglages">
			<p><label><input type="checkbox" name="jrl_maj_auto" value="1" <?php checked( '1', get_option( 'jrl_maj_auto', '1' ) ); ?>> Installer automatiquement les nouvelles versions publiées sur GitHub</label></p>
			<p>
				<button class="button button-primary" type="submit">Enregistrer</button>
				<button class="button" type="submit" name="jrl_verifier" value="1">Rechercher une mise à jour maintenant</button>
				<a class="button-link" href="<?php echo esc_url( 'https://github.com/' . JRL_REPO . '/releases' ); ?>" target="_blank" rel="noopener">Versions sur GitHub</a>
			</p>
		</form>
	</div>
	<?php
}

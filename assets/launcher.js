(function () {
	'use strict';
	var overlay = null, lastButton = null, wentFull = false;
	function fsElement() { return document.fullscreenElement || document.webkitFullscreenElement || null; }
	function requestFs(el) { try { var fn = el.requestFullscreen || el.webkitRequestFullscreen; if (!fn) return false; var p = fn.call(el, { navigationUI: 'hide' }); if (p && p.catch) p.catch(function () {}); return true; } catch (e) { return false; } }
	function exitFs() { try { if (!fsElement()) return; var fn = document.exitFullscreen || document.webkitExitFullscreen; if (fn) { var p = fn.call(document); if (p && p.catch) p.catch(function () {}); } } catch (e) {} }
	function open(btn) {
		if (overlay) return; lastButton = btn;
		overlay = document.createElement('div'); overlay.className = 'jdr-overlay';
		overlay.setAttribute('role', 'dialog'); overlay.setAttribute('aria-modal', 'true'); overlay.setAttribute('aria-label', btn.getAttribute('data-jdr-title') || 'Jeu de révision');
		var loader = document.createElement('div'); loader.className = 'jdr-loader'; loader.textContent = btn.getAttribute('data-jdr-lang') === 'de' ? 'Spiel wird geladen…' : 'Chargement du jeu…';
		var frame = document.createElement('iframe'); frame.className = 'jdr-frame'; frame.title = btn.getAttribute('data-jdr-title') || 'Jeu de révision';
		frame.setAttribute('allow', 'fullscreen; autoplay'); frame.setAttribute('allowfullscreen', ''); frame.src = btn.getAttribute('data-jdr-src');
		frame.addEventListener('load', function () { loader.remove(); try { frame.focus(); } catch (e) {} });
		overlay.appendChild(loader); overlay.appendChild(frame); document.body.appendChild(overlay);
		document.documentElement.classList.add('jdr-open');
		wentFull = requestFs(overlay); /* inside the click: user gesture required */
	}
	/* After the game closes, reload the progress block of its card (logged-in users). */
	function refresh(id, lang) {
		var cfg = (window.JDR && window.JDR.cfg) || {};
		if (!id || !cfg.loggedIn || !cfg.rest || !window.fetch) return;
		fetch(cfg.rest + 'carte/' + encodeURIComponent(id) + (lang === 'de' ? '?lang=de' : ''), { credentials: 'same-origin', headers: { 'X-WP-Nonce': cfg.nonce } })
			.then(function (r) { return r.ok ? r.json() : null; })
			.then(function (j) {
				if (!j || typeof j.html !== 'string') return;
				document.querySelectorAll('[data-jdr-prog="' + id + '"]').forEach(function (el) { el.innerHTML = j.html; });
				if (j.bouton) document.querySelectorAll('.jdr-play[data-jdr-id="' + id + '"]').forEach(function (b) { if ((b.getAttribute('data-jdr-lang') || 'fr') === (lang || 'fr')) b.textContent = j.bouton; });
			}).catch(function () {});
	}
	function close() { if (!overlay) return; var o = overlay; overlay = null; exitFs(); o.remove(); document.documentElement.classList.remove('jdr-open'); if (lastButton) { try { lastButton.focus(); } catch (e) {} refresh(lastButton.getAttribute('data-jdr-id'), lastButton.getAttribute('data-jdr-lang')); } }
	document.addEventListener('click', function (e) { var b = e.target.closest && e.target.closest('.jdr-play[data-jdr-src]'); if (!b) return; e.preventDefault(); open(b); });
	/* Leaving fullscreen (Esc or the game's button) keeps the game open: it still fills the window. */
	function onFs() { if (overlay && !fsElement()) wentFull = false; }
	document.addEventListener('fullscreenchange', onFs); document.addEventListener('webkitfullscreenchange', onFs);
	document.addEventListener('keydown', function (e) { if (overlay && e.key === 'Escape') close(); });
	window.addEventListener('message', function (e) { if (e.origin !== window.location.origin) return; if (e.data && e.data.jdr === 'close') close(); });
})();

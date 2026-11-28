#!/usr/bin/env python3
"""visiteurs.py [dossier_jeu ...] : mode visiteur (sans compte) dans les moteurs des jeux.

Quand le site autorise les visiteurs, la page du jeu reçoit JDR_CFG.guest = true :
le jeu s'ouvre sans connexion, la progression reste dans le navigateur (localStorage),
sans classement ni bilan enregistré. Idempotent. Sans argument : tous les jeux (FR, DE, IT).
"""
import glob, os, sys

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARTE = {
    'fr': ('Mode visiteur', "Vous jouez sans compte : votre progression reste dans ce navigateur, sur cet appareil. Connectez-vous pour l'enregistrer sur votre compte et la retrouver partout.", 'Se connecter'),
    'de': ('Gastmodus', 'Sie spielen ohne Konto: Ihr Fortschritt bleibt in diesem Browser, auf diesem Gerät. Melden Sie sich an, um ihn in Ihrem Konto zu speichern und überall wiederzufinden.', 'Anmelden'),
    'it': ('Modalità ospite', 'Sta giocando senza account: i progressi restano in questo browser, su questo dispositivo. Acceda per salvarli nel suo account e ritrovarli ovunque.', 'Accedi'),
}

def patch(path, lg):
    s = o = open(path, encoding='utf-8').read()
    if 'WP.guest' in s:
        return 'déjà'
    a = 'site:c.site||""}'
    assert s.count(a) == 1, (path, 'WPC')
    s = s.replace(a, 'site:c.site||"",guest:!!c.guest}')
    a = 'else if(WP&&!WP.loggedIn&&window.JDR_CFG)needLogin()'
    assert s.count(a) == 2, (path, 'route')
    s = s.replace(a, 'else if(WP&&!WP.loggedIn&&!WP.guest&&window.JDR_CFG)needLogin()')
    a = '<section class="panel save" id="preview">'
    assert s.count(a) == 1, (path, 'preview')
    t, txt, btn = CARTE[lg]
    guest = ('${WP&&WP.guest?`<section class="panel save" id="guest"><b>' + t + '</b><small>' + txt.replace('`', "'") + '</small>'
             '${WP.login?`<a class="btn y small" href="${esc(WP.login)}" target="_top" style="margin-top:8px;align-self:flex-start">' + btn + '</a>`:""}</section>`:`')
    s = s.replace(a, guest + a)
    k = s.find(a, s.find(guest) + len(guest) - 1)
    j = s.find('</section>`}', k)
    assert k > 0 and j > 0, (path, 'fin preview')
    s = s[:j] + '</section>`}`}' + s[j + len('</section>`}'):]
    open(path, 'w', encoding='utf-8').write(s)
    return 'ok'

if __name__ == "__main__":
    dirs = sys.argv[1:] or sorted(glob.glob(R + '/jeux/*/'))
    res = {}
    for d in dirs:
        for f, lg in (('index.html', 'fr'), ('index.de.html', 'de'), ('index.it.html', 'it')):
            p = os.path.join(d, f)
            if os.path.exists(p):
                r = patch(p, lg); res[r] = res.get(r, 0) + 1
    print(res)

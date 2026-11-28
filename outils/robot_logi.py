import sys, os, random, re
from playwright.sync_api import sync_playwright
"""robot_logi.py <game_dir> <shots_dir> : test Playwright du Modèle logistique (tous modes, tous types, loupe, aucun code de sauvegarde, clavier numérique)."""
LANG = sys.argv[3] if len(sys.argv) > 3 else "fr"
URL = "file://" + os.path.abspath(sys.argv[1]) + ("/index." + LANG + ".html" if LANG in ("de", "it") else "/index.html")
HELLO = {"de": ("Willkommen",), "it": ("Benvenuto",)}.get(LANG, ("Bienvenue",))
OUT = sys.argv[2].rstrip("/") + "/"
import os; os.makedirs(OUT, exist_ok=True)
errors = []
types_seen = set()

def answer(pg):
    """answer the current challenge, sometimes wrongly"""
    kind = pg.locator(".tag").nth(1).inner_text().strip().upper()
    types_seen.add(kind)
    if pg.locator("#val").count():
        opts = pg.locator(".opt"); opts.nth(0).click()
        if random.random() < .5 and opts.count() > 1: opts.nth(1).click()
        pg.click("#val"); return
    if pg.locator("#numin").count():
        a = pg.evaluate("(()=>{const n=document.querySelector('#numin');return [n.getAttribute('inputmode'),n.getAttribute('pattern'),document.activeElement===n]})()")
        if a[0] != "numeric" or a[1] != "[0-9]*": errors.append("numin: clavier numérique non demandé " + str(a))
        if not a[2]: errors.append("numin: champ sans focus (le clavier ne s'ouvrirait pas)")
        pg.fill("#numin", random.choice(["2", "9", "65", "3", "25"])); pg.locator("#nf button").click(); return
    if pg.locator(".mi").count():
        n = pg.locator(".mcol").nth(0).locator(".mi").count()
        for _ in range(n):
            l = pg.locator('.mi[data-s="L"]:not(.done)').first
            i = l.get_attribute("data-i"); l.click()
            pg.locator(f'.mi[data-s="R"][data-i="{i}"]').click()
        return
    if pg.locator(".bin").count():
        while pg.locator(".bin").count():
            bins = pg.locator(".bin"); bins.nth(random.randrange(bins.count())).click()
            pg.wait_for_timeout(1200)
        return
    if pg.locator(".slot").count():
        while pg.locator(".pills .pill").count():
            pg.locator(".pills .pill").first.click()
        pg.click("#chk"); return
    if pg.locator(".imgbtn").count():
        imgs = pg.locator(".imgbtn"); imgs.nth(random.randrange(imgs.count())).click(); return
    if pg.locator(".tf button").count():
        pg.locator(".tf button").nth(random.randrange(2)).click(); return
    if pg.locator(".pill").count():
        pg.locator(".pill").first.click(); return
    pg.locator(".opt").nth(random.randrange(pg.locator(".opt").count())).click()

def play(pg, exam=False, maxn=40):
    for _ in range(maxn):
        if pg.locator("#back").count(): return True
        pg.wait_for_selector("#card, #back")
        if pg.locator("#back").count(): return True
        answer(pg)
        if not exam:
            pg.wait_for_selector("#nx"); pg.click("#nx")
        else:
            pg.wait_for_timeout(300)
    return pg.locator("#back").count() > 0

with sync_playwright() as p:
    b = p.chromium.launch()
    for width, scheme in [(1280, "light"), (400, "dark")]:
        ctx = b.new_context(viewport={"width": width, "height": 900}, color_scheme=scheme)
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.on("console", lambda m: errors.append("console:" + m.text) if m.type == "error" and "fonts" not in m.text else None)
        pg.goto(URL); pg.wait_for_timeout(500)
        pg.screenshot(path=OUT + f"welcome_{width}.png", full_page=True)
        assert pg.locator("#nname, #cname").count() == 0, "un champ prénom est encore demandé"
        pg.click("#fstart button")
        pg.wait_for_selector(".orow")
        N = pg.locator('.orow').count()
        for oi in (range(N) if width==1280 else [0,N-1]):
            pg.locator(".orow").nth(oi).click()
            if oi == 5 and pg.locator(".zoom").count():
                pass
            assert play(pg), "train did not finish"
            if oi == 0: pg.screenshot(path=OUT + f"end_train_{width}.png", full_page=True)
            pg.click("#back")
        pg.screenshot(path=OUT + f"home_{width}_{scheme}.png", full_page=True)
        # zoom test: find a plan question
        pg.locator(".orow").nth(pg.locator('.orow').count()-1).click()
        for _ in range(12):
            if pg.locator(".zoom").count():
                pg.screenshot(path=OUT + f"q_img_{width}.png", full_page=True)
                pg.locator(".zoom").click(); pg.wait_for_timeout(200)
                assert pg.locator("#lb").is_visible(); pg.screenshot(path=OUT + f"lightbox_{width}.png")
                pg.click("#lbclose"); break
            answer(pg); pg.wait_for_selector("#nx"); pg.click("#nx")
            if pg.locator("#back").count(): pg.click("#back"); pg.locator(".orow").nth(pg.locator('.orow').count()-1).click()
        pg.click("#quit")
        # exam
        pg.click("#mExam")
        pg.screenshot(path=OUT + f"exam_q_{width}.png", full_page=True)
        assert play(pg, exam=True, maxn=30), "exam did not finish"
        pg.click("details.corr summary")
        pg.screenshot(path=OUT + f"exam_end_{width}.png", full_page=True)
        pg.click("#back")
        # review
        if pg.locator("#mRev:not([disabled])").count():
            pg.click("#mRev"); assert play(pg); pg.click("#back")
        else: print("no review queue?")
        xp = pg.evaluate("S.xp")
        pg.screenshot(path=OUT + f"home_final_{width}.png", full_page=True)
        # aucun code de sauvegarde, ni « changer de participant »
        for sel in ("#code", "#hascode", "#ccode", "#newp", "#cpy", "#frest"):
            assert pg.locator(sel).count() == 0, "élément de code encore présent : " + sel
        body = pg.locator("body").inner_text().lower()
        assert "code de sauvegarde" not in body and "reprendre avec un code" not in body, "texte de code encore affiché"
        # la progression reste (même appareil) après rechargement, sans rien saisir
        pg.reload(); pg.wait_for_selector(".orow")
        print(width, "xp après rechargement", xp, pg.evaluate("S.xp"))
        assert pg.evaluate("S.xp") == xp, "progression perdue au rechargement"
        # un autre appareil commence à zéro, sans champ ni code
        c2 = b.new_context(viewport={"width": width, "height": 900}, color_scheme=scheme)
        p2 = c2.new_page(); p2.on("pageerror", lambda e: errors.append(str(e)))
        p2.goto(URL); assert p2.locator("#hascode, #ccode, input").count() == 0, "champ ou code sur le premier écran"
        assert p2.locator("#hello").inner_text().startswith(HELLO), "pas de mot de bienvenue"
        # bouton de langue : FR -> DE -> FR, même progression (même clé)
        if p2.locator("#lang").count():
            p2.click("#fstart button"); p2.wait_for_selector(".orow"); x0 = p2.evaluate("S.xp")
            def pick(code=None):
                p2.click("#lang"); p2.wait_for_selector(".langmenu:not([hidden])", timeout=3000)
                sel = f'.langopt[data-l="{code}"]' if code else ".langopt:not(.on)"
                p2.click(sel); p2.wait_for_timeout(600); p2.wait_for_selector(".orow", timeout=8000)
            seen = []
            for code in [l for l in p2.evaluate("LANGS") if l != LANG]:
                pick(code); seen.append(p2.evaluate("LANG")); assert seen[-1] == code, "le menu de langue ne change pas de langue"
                assert p2.evaluate("S.xp") == x0, "progression différente après changement de langue"
                pick(LANG); assert p2.evaluate("LANG") == LANG, "retour à la langue de départ impossible"
            print(width, "menu de langue OK", seen)
        if LANG in ("de", "it"):
            import re as _re
            txt = pg.locator("body").inner_text()
            fr = [w for w in ("Quitter", "Commencer", "Entraînement", "Examen blanc", "Objectifs du", "épreuves", "Valider", "Bonne réponse") if w in txt]
            if fr: errors.append("textes français dans la version allemande : " + ", ".join(fr))
        sw = pg.evaluate("document.documentElement.scrollWidth"); print(width, "scrollWidth", sw)
        c2.close(); ctx.close()
    b.close()
print("types:", sorted(types_seen))
print("errors:", errors[:10], len(errors))

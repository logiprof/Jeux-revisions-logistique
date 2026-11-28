"""zoom_test.py <dossier_jeu> <captures> <index_objectif_avec_images> : teste la loupe (robot_logi.py ne la teste que sur le dernier objectif)."""
import sys,os
G,O,OI=sys.argv[1],sys.argv[2],int(sys.argv[3]) if len(sys.argv)>3 else 0
sys.argv=[sys.argv[0],G,O]
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'robot_logi.py')).read().split('with sync_playwright() as p:')[0])
with sync_playwright() as p:
    b=p.chromium.launch()
    for w,sc in [(1280,'light'),(400,'dark')]:
        pg=b.new_page(viewport={'width':w,'height':900},color_scheme=sc); pg.on('pageerror',lambda e:errors.append(str(e)))
        pg.goto(URL); pg.click('#fstart button'); pg.wait_for_selector('.vial'); pg.locator('.vial').nth(OI).click()
        found=0
        for _ in range(40):
            pg.wait_for_selector('#card, #back')
            if pg.locator('#back').count(): pg.click('#back'); pg.locator('.vial').nth(OI).click(); continue
            if pg.locator('.zoom').count():
                found+=1; pg.screenshot(path=f'{O}/q_img_{w}_{found}.png',full_page=True)
                pg.locator('.zoom').first.click(); pg.wait_for_timeout(200); assert pg.locator('#lb').is_visible()
                pg.screenshot(path=f'{O}/lb_{w}.png'); pg.click('#lbclose')
                if found>=2: break
            answer(pg); pg.wait_for_selector('#nx'); pg.click('#nx')
        print(w,'images vues',found)
    b.close()
print('errors',errors)

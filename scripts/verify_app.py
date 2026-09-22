import asyncio
from playwright.async_api import async_playwright
import os

SCREENSHOTS_DIR = os.path.join(os.getcwd(), "test_screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # 1. Desktop Test: Catalog Page
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        print("Testing Catalog Page on Desktop (1920x1080)...")
        await page.goto("http://localhost:3000/", wait_until="networkidle")
        await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "01_catalog_desktop_5models.png"), full_page=True)
        
        # Verify 5 cards are rendered
        cards = await page.query_selector_all("article")
        print(f"Total model cards found: {len(cards)}")
        assert len(cards) == 5, f"Expected 5 models, found {len(cards)}"

        # Check titles of the 5 cards in order
        expected_names = ["S7 REEV", "V9 PHEV", "T5 HEV", "FRIDAY REEV", "U-TOUR HEV"]
        for i, card in enumerate(cards):
            name_el = await card.query_selector("h2")
            name_text = await name_el.inner_text() if name_el else ""
            print(f"  Card {i+1}: {name_text}")
            assert expected_names[i] in name_text

        # 2. Test S7 REEV
        print("\nTesting S7 REEV...")
        await page.goto("http://localhost:3000/modelos/s7-reev", wait_until="networkidle")
        await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "02_s7_reev_desktop.png"), full_page=True)
        h1 = await page.inner_text("h1")
        assert "S7 REEV" in h1

        # 3. Test V9 PHEV
        print("\nTesting V9 PHEV...")
        await page.goto("http://localhost:3000/modelos/v9-phev", wait_until="networkidle")
        await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "03_v9_phev_desktop.png"), full_page=True)
        h1 = await page.inner_text("h1")
        assert "V9 PHEV" in h1

        # 4. Test T5 HEV (Desktop, Tablet, Mobile)
        print("\nTesting T5 HEV (Desktop)...")
        await page.goto("http://localhost:3000/modelos/t5-hev", wait_until="networkidle")
        await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "04_t5_hev_desktop.png"), full_page=True)
        h1 = await page.inner_text("h1")
        assert "T5 HEV" in h1
        # Check attributes title
        features_h3 = await page.inner_text("h3")
        print(f"Features section title: {features_h3}")
        assert "TODO LO QUE BUSCÁS EN UN FORTHING" in features_h3

        # Tablet (768x1024)
        print("Testing T5 HEV (Tablet 768x1024)...")
        page_tablet = await browser.new_page(viewport={"width": 768, "height": 1024})
        await page_tablet.goto("http://localhost:3000/modelos/t5-hev", wait_until="networkidle")
        await page_tablet.screenshot(path=os.path.join(SCREENSHOTS_DIR, "05_t5_hev_tablet.png"), full_page=True)

        # Mobile (390x844)
        print("Testing T5 HEV (Mobile 390x844)...")
        page_mobile = await browser.new_page(viewport={"width": 390, "height": 844})
        await page_mobile.goto("http://localhost:3000/modelos/t5-hev", wait_until="networkidle")
        await page_mobile.screenshot(path=os.path.join(SCREENSHOTS_DIR, "06_t5_hev_mobile.png"), full_page=True)

        # 5. Test FRIDAY REEV
        print("\nTesting FRIDAY REEV (Desktop)...")
        await page.goto("http://localhost:3000/modelos/friday-reev", wait_until="networkidle")
        await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "07_friday_reev_desktop.png"), full_page=True)
        h1 = await page.inner_text("h1")
        assert "FRIDAY REEV" in h1

        # 6. Test U-TOUR HEV
        print("\nTesting U-TOUR HEV (Desktop)...")
        await page.goto("http://localhost:3000/modelos/u-tour-hev", wait_until="networkidle")
        await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "08_u_tour_hev_desktop.png"), full_page=True)
        h1 = await page.inner_text("h1")
        assert "U-TOUR HEV" in h1

        # 7. Test Language Switcher to EN on U-TOUR HEV
        print("\nTesting Language Switcher to EN on U-TOUR HEV...")
        await page.click('button:has-text("EN")')
        await page.wait_for_timeout(300)
        slogan_en = await page.inner_text("h2")
        print(f"EN Slogan: {slogan_en}")
        assert "7 seats" in slogan_en
        await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "09_u_tour_hev_english.png"), full_page=True)

        # 8. Test Old Route /modelos/t5-evo -> 404
        print("\nTesting Old Route /modelos/t5-evo returns 404...")
        await page.goto("http://localhost:3000/modelos/t5-evo", wait_until="networkidle")
        await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "10_old_t5_evo_404.png"), full_page=True)
        h1_404 = await page.inner_text("h1")
        print(f"404 H1: {h1_404}")
        assert "no encontrado" in h1_404.lower() or "not found" in h1_404.lower()

        await browser.close()
        print("\nAll 5-model verification tests completed successfully!")

asyncio.run(run())

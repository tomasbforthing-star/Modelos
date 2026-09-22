from playwright.sync_api import sync_playwright

with open('public/assets/logo-forthing-white.svg', 'r', encoding='utf-8') as f:
    svg_content = f.read()

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 800, 'height': 200})
    page.set_content(f"""
        <!DOCTYPE html>
        <html>
        <body style="background: #222223; margin: 0; padding: 40px; display: flex; align-items: center; justify-content: center;">
            <div style="height: 60px; display: flex; align-items: center;">
                {svg_content}
            </div>
        </body>
        </html>
    """)
    page.screenshot(path='public/assets/logo_check.png')
    browser.close()

print('Saved public/assets/logo_check.png with inlined SVG!')

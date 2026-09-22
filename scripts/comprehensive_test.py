from playwright.sync_api import sync_playwright
import os
import time

VIEWPORTS = {
    'desktop': {'width': 1440, 'height': 900},
    'tablet': {'width': 768, 'height': 1024},
    'mobile': {'width': 390, 'height': 844}
}

PAGES = [
    {'path': '/', 'name': 'catalogo'},
    {'path': '/modelos/s7-reev', 'name': 's7-reev'},
    {'path': '/modelos/v9-phev', 'name': 'v9-phev'},
    {'path': '/modelos/t5-hev', 'name': 't5-hev'},
    {'path': '/modelos/friday-reev', 'name': 'friday-reev'},
    {'path': '/modelos/u-tour-hev', 'name': 'u-tour-hev'}
]

os.makedirs('audit_screenshots', exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    for vp_name, vp_size in VIEWPORTS.items():
        print(f"\n==========================================")
        print(f"Testing Viewport: {vp_name.upper()} ({vp_size['width']}x{vp_size['height']})")
        print(f"==========================================")
        
        context = browser.new_context(viewport=vp_size)
        page = context.new_page()
        
        for pg in PAGES:
            url = f"http://localhost:3000{pg['path']}"
            page.goto(url, wait_until='networkidle')
            time.sleep(0.3)
            
            # Check horizontal overflow
            scroll_width = page.evaluate("document.documentElement.scrollWidth")
            client_width = page.evaluate("document.documentElement.clientWidth")
            overflow = scroll_width > client_width
            print(f"[{vp_name}] {pg['name']} -> URL: {url} | ScrollWidth: {scroll_width} vs ClientWidth: {client_width} | Overflow: {overflow}")
            assert not overflow, f"Horizontal overflow detected on {pg['name']} at {vp_name}!"
            
            # Check "VER TODOS LOS MODELOS" is NOT present on model pages
            if pg['path'].startswith('/modelos/'):
                all_models_btn = page.query_selector("text='VER TODOS LOS MODELOS'") or page.query_selector("text='Ver todos los modelos'") or page.query_selector("text='ALL MODELS'")
                if all_models_btn:
                    print(f"  WARNING: Found 'VER TODOS LOS MODELOS' on {pg['name']}!")
                else:
                    print(f"  OK: 'VER TODOS LOS MODELOS' is completely absent on {pg['name']}.")
            
            # Screenshot
            shot_path = f"audit_screenshots/{pg['name']}_{vp_name}.png"
            page.screenshot(path=shot_path, full_page=False)
            print(f"  Saved screenshot: {shot_path}")
            
        context.close()
        
    browser.close()

print("\nAll responsive audit tests completed successfully!")

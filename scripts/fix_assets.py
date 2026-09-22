import os
import numpy as np
from PIL import Image

# 1. Generate clean white logo for dark navbar
raw_logo_path = os.path.join("public", "assets", "logo-raw.png")
if os.path.exists(raw_logo_path):
    img = Image.open(raw_logo_path).convert("RGBA")
    arr = np.array(img, dtype=np.uint8)
    
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]
    
    # Foreground text & shield black parts (lum < 100) -> turn into pure white (#FFFFFF) with full opacity
    # White inner lion parts (lum > 200) -> stay white
    # Background transparent parts -> stay transparent
    
    # Let's create an output array initialized to transparent
    out_arr = np.zeros_like(arr)
    
    # Mask of all logo elements (non-transparent pixels in original page)
    # In original rendered page, background is alpha 0 or white.
    # Where a > 10:
    # If pixel was black text (r < 100): invert to white (255, 255, 255)
    # If pixel was white lion (r > 200, g > 200, b > 200): keep white (255, 255, 255)
    # The shield outer shape is black, lion inside is white.
    
    # Invert RGB brightness to get white glyphs:
    # where a > 0:
    mask = a > 10
    # For every foreground pixel:
    # If it was black (r,g,b ~ 0), we want it to be white (255,255,255).
    # If it was white (r,g,b ~ 255), we want it to be white (255,255,255).
    # The shield background was black, lion was white. To keep lion distinguishable, the shield outer border + lion are white, shield fill is dark.
    # Actually in the mockup:
    # The shield is a white outline shield containing the white lion.
    # To the right: "FORTHING" is white text, "ARGENTINA" is white text.
    
    # Let's see: In raw_logo, the shield outline + text were black (0,0,0), lion was white (255,255,255).
    # If we map black (0,0,0) -> white (255,255,255) and white (255,255,255) -> white (255,255,255),
    # but the space between shield border and lion is dark (#222223)!
    # Let's inspect the bounding box and structure.
    
    # Let's create a transparent RGBA image where:
    # - Black text/lines become pure white with their anti-aliased alpha
    # - White lion becomes pure white
    # - Transparent/background remains 0 alpha
    
    # In raw_logo from fitz with alpha=True:
    # Background outside elements is A=0!
    # Let's verify:
    print("Non-zero alpha count:", np.count_nonzero(a > 10))
    
    # All non-zero alpha pixels that are black (r < 100): make white (255, 255, 255, 255)
    # All pixels that are white (r > 200): make white (255, 255, 255, 255)
    # For anti-aliased edges: alpha is preserved
    out_arr[:, :, 0] = 255
    out_arr[:, :, 1] = 255
    out_arr[:, :, 2] = 255
    out_arr[:, :, 3] = a
    
    out_img = Image.fromarray(out_arr, "RGBA")
    
    # Crop empty transparent borders
    bbox = out_img.getbbox()
    if bbox:
        out_img = out_img.crop(bbox)
        
    out_img.save("public/assets/logo-forthing-white.png", "PNG")
    print("Saved clean public/assets/logo-forthing-white.png, size:", out_img.size)

# 2. Extract clean T5 EVO Car from mockup without browser bar
mockup_path = r"C:\Users\admin\.gemini\antigravity\brain\581bbba9-eeec-4bd6-802a-cc879601574d\.user_uploaded\media_1790008357345.png"
if os.path.exists(mockup_path):
    with Image.open(mockup_path) as m_img:
        print("Mockup size:", m_img.size)
        # Mockup has browser bar at top (~80px) and bottom attributes section.
        # The car itself is in the hero area.
        # In media_1790008357345.png:
        # Width: 1920 (or similar), height: 1080 (or similar)
        # Hero area is roughly y: 90 to 720, car is on right side x: 800 to 1850
        # Let's crop the full hero image (white background with car and slogan) or just the car:
        w, h = m_img.size
        # The hero section is from y = int(h * 0.08) to int(h * 0.72)
        # And the car alone is from x = int(w * 0.40) to int(w * 0.96)
        car_crop = m_img.crop((int(w * 0.40), int(h * 0.18), int(w * 0.98), int(h * 0.72)))
        car_crop.save("public/assets/models/t5-evo-hero.webp", "WEBP", quality=95)
        car_crop.convert("RGB").save("public/assets/models/t5-evo-hero.jpg", "JPEG", quality=95)
        
        # Also card image (centered car)
        card_crop = m_img.crop((int(w * 0.42), int(h * 0.22), int(w * 0.96), int(h * 0.68)))
        card_crop = card_crop.resize((1280, 800), Image.Resampling.LANCZOS)
        card_crop.save("public/assets/models/t5-evo-card.webp", "WEBP", quality=92)
        card_crop.convert("RGB").save("public/assets/models/t5-evo-card.jpg", "JPEG", quality=92)
        print("Saved cropped T5 EVO car assets")


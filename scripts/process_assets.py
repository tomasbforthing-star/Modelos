import os
import shutil
import fitz
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

OUTPUT_DIR = os.path.join("public", "assets")
MODELS_DIR = os.path.join(OUTPUT_DIR, "models")
os.makedirs(MODELS_DIR, exist_ok=True)

print("--- Processing Logo from VISUALES/LogoForthing.pdf ---")
pdf_path = os.path.join("VISUALES", "LogoForthing.pdf")
if os.path.exists(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc[0]
    
    # Save SVG
    svg_data = page.get_svg_image()
    with open(os.path.join(OUTPUT_DIR, "logo-forthing.svg"), "w", encoding="utf-8") as f:
        f.write(svg_data)
    print("Saved logo-forthing.svg")
    
    # Save high-res transparent PNG
    pix = page.get_pixmap(dpi=300, alpha=True)
    pix.save(os.path.join(OUTPUT_DIR, "logo-forthing.png"))
    print("Saved logo-forthing.png")

print("--- Processing Vehicle Images from VISUALES ---")

def process_image(src_path, model_slug):
    if not os.path.exists(src_path):
        print(f"Warning: {src_path} not found!")
        return
    print(f"Processing {src_path} -> {model_slug}...")
    with Image.open(src_path) as img:
        img_rgb = img.convert("RGB")
        
        # 1. Hero image (Max width 2560px, high quality WebP & JPG)
        hero = img_rgb.copy()
        if hero.width > 2560:
            ratio = 2560 / hero.width
            new_size = (2560, int(hero.height * ratio))
            hero = hero.resize(new_size, Image.Resampling.LANCZOS)
        
        hero_webp = os.path.join(MODELS_DIR, f"{model_slug}-hero.webp")
        hero_jpg = os.path.join(MODELS_DIR, f"{model_slug}-hero.jpg")
        hero.save(hero_webp, "WEBP", quality=90, method=6)
        hero.save(hero_jpg, "JPEG", quality=90, optimize=True)
        print(f"  Hero saved: {hero_webp} ({hero.size})")
        
        # 2. Card image (16:9 or 4:3 crop/resize around center-car, 1200x800)
        card = img_rgb.copy()
        card_w, card_h = 1280, 800
        # Calculate aspect ratio
        target_ratio = card_w / card_h
        current_ratio = card.width / card.height
        
        if current_ratio > target_ratio:
            # Current is wider, crop width
            new_w = int(card.height * target_ratio)
            left = (card.width - new_w) // 2
            card = card.crop((left, 0, left + new_w, card.height))
        else:
            # Current is taller, crop height
            new_h = int(card.width / target_ratio)
            top = (card.height - new_h) // 2
            card = card.crop((0, top, card.width, top + new_h))
            
        card = card.resize((card_w, card_h), Image.Resampling.LANCZOS)
        card_webp = os.path.join(MODELS_DIR, f"{model_slug}-card.webp")
        card_jpg = os.path.join(MODELS_DIR, f"{model_slug}-card.jpg")
        card.save(card_webp, "WEBP", quality=88, method=6)
        card.save(card_jpg, "JPEG", quality=88, optimize=True)
        print(f"  Card saved: {card_webp} ({card.size})")

process_image(os.path.join("VISUALES", "Friday Reev.jpg"), "friday-reev")
process_image(os.path.join("VISUALES", "S7 REEV.jpg"), "s7-reev")
process_image(os.path.join("VISUALES", "V9.jpg"), "v9")

# Also prepare T5 EVO from uploaded mockup media if available
mockup_t5 = r"C:\Users\admin\.gemini\antigravity\brain\581bbba9-eeec-4bd6-802a-cc879601574d\.user_uploaded\media_1790008357345.png"
if os.path.exists(mockup_t5):
    print("Extracting T5 EVO reference from mockup...")
    with Image.open(mockup_t5) as img:
        img_rgb = img.convert("RGB")
        # Crop car section or save full hero
        t5_hero_webp = os.path.join(MODELS_DIR, "t5-evo-hero.webp")
        t5_hero_jpg = os.path.join(MODELS_DIR, "t5-evo-hero.jpg")
        img_rgb.save(t5_hero_webp, "WEBP", quality=92)
        img_rgb.save(t5_hero_jpg, "JPEG", quality=92)
        
        # Also card
        t5_card_webp = os.path.join(MODELS_DIR, "t5-evo-card.webp")
        t5_card_jpg = os.path.join(MODELS_DIR, "t5-evo-card.jpg")
        img_rgb.save(t5_card_webp, "WEBP", quality=88)
        img_rgb.save(t5_card_jpg, "JPEG", quality=88)
        print("Saved T5 EVO assets")

print("Asset processing completed successfully!")

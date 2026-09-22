import os
import glob
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

MODELS_DIR = os.path.join("public", "assets", "models")
os.makedirs(MODELS_DIR, exist_ok=True)

# 1. Clean up old t5-evo or unused files
for old_f in glob.glob(os.path.join(MODELS_DIR, "*t5-evo*")):
    try:
        os.remove(old_f)
        print(f"Removed old file: {old_f}")
    except Exception as e:
        print(f"Error removing {old_f}: {e}")

# Mapping of VISUALES source files to target model slugs
MODELS_MAPPING = [
    {"src": "S7 REEV.jpg", "slug": "s7-reev"},
    {"src": "V9.jpg", "slug": "v9-phev"},
    {"src": "T5 HEV.jpg", "slug": "t5-hev"},
    {"src": "Friday Reev.jpg", "slug": "friday-reev"},
    {"src": "U-TOUR HEV.png", "slug": "u-tour-hev"}
]

for item in MODELS_MAPPING:
    src_path = os.path.join("VISUALES", item["src"])
    slug = item["slug"]
    
    if not os.path.exists(src_path):
        print(f"Warning: {src_path} does not exist!")
        continue
        
    print(f"Processing {src_path} -> {slug}...")
    with Image.open(src_path) as img:
        img_rgb = img.convert("RGB")
        w, h = img_rgb.size
        print(f"  Source size: {w}x{h}")
        
        # 1. Hero Image (High resolution 2560px max width for crisp displays)
        hero = img_rgb.copy()
        if hero.width > 2560:
            ratio = 2560 / hero.width
            new_size = (2560, int(hero.height * ratio))
            hero = hero.resize(new_size, Image.Resampling.LANCZOS)
            
        hero_webp = os.path.join(MODELS_DIR, f"{slug}-hero.webp")
        hero_jpg = os.path.join(MODELS_DIR, f"{slug}-hero.jpg")
        hero.save(hero_webp, "WEBP", quality=92, method=6)
        hero.save(hero_jpg, "JPEG", quality=92, optimize=True)
        print(f"  Saved hero: {hero_webp} ({hero.size})")
        
        # 2. Card Image (16:10 aspect ratio 1280x800 for catalog cards)
        card = img_rgb.copy()
        target_w, target_h = 1280, 800
        target_ratio = target_w / target_h
        current_ratio = card.width / card.height
        
        if current_ratio > target_ratio:
            new_w = int(card.height * target_ratio)
            left = (card.width - new_w) // 2
            card = card.crop((left, 0, left + new_w, card.height))
        else:
            new_h = int(card.width / target_ratio)
            top = (card.height - new_h) // 2
            card = card.crop((0, top, card.width, top + new_h))
            
        card = card.resize((target_w, target_h), Image.Resampling.LANCZOS)
        card_webp = os.path.join(MODELS_DIR, f"{slug}-card.webp")
        card_jpg = os.path.join(MODELS_DIR, f"{slug}-card.jpg")
        card.save(card_webp, "WEBP", quality=88, method=6)
        card.save(card_jpg, "JPEG", quality=88, optimize=True)
        print(f"  Saved card: {card_webp} ({card.size})")

print("Asset processing for all 5 models completed successfully!")

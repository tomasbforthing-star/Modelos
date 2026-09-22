import os
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

MODELS_DIR = os.path.join("public", "assets", "models")
os.makedirs(MODELS_DIR, exist_ok=True)

# Custom tailored crops from high-res VISUALES source files
CROPS = {
    "s7-reev": {
        "src": "S7 REEV.jpg",
        "hero_box_pct": (0.16, 0.34, 0.88, 0.84),
        "card_box_pct": (0.22, 0.36, 0.85, 0.84),
    },
    "v9-phev": {
        "src": "V9.jpg",
        "hero_box_pct": (0.06, 0.08, 0.95, 0.82),
        "card_box_pct": (0.08, 0.18, 0.92, 0.80),
    },
    "t5-hev": {
        "src": "T5 HEV.jpg",
        "hero_box_pct": (0.12, 0.22, 0.72, 0.80),
        "card_box_pct": (0.14, 0.24, 0.70, 0.80),
    },
    "friday-reev": {
        "src": "Friday Reev.jpg",
        "hero_box_pct": (0.00, 0.26, 0.76, 0.82),
        "card_box_pct": (0.05, 0.30, 0.72, 0.80),
    },
    "u-tour-hev": {
        "src": "U-TOUR HEV.png",
        "hero_box_pct": (0.00, 0.08, 0.95, 0.88),
        "card_box_pct": (0.10, 0.14, 0.90, 0.84),
    }
}

for slug, cfg in CROPS.items():
    src_path = os.path.join("VISUALES", cfg["src"])
    if not os.path.exists(src_path):
        print(f"Error: {src_path} missing")
        continue
        
    print(f"Generating tailored assets for {slug} from {src_path}...")
    with Image.open(src_path) as img:
        img_rgb = img.convert("RGB")
        w, h = img_rgb.size
        
        # 1. Hero Crop
        hx0 = int(w * cfg["hero_box_pct"][0])
        hy0 = int(h * cfg["hero_box_pct"][1])
        hx1 = int(w * cfg["hero_box_pct"][2])
        hy1 = int(h * cfg["hero_box_pct"][3])
        hero_crop = img_rgb.crop((hx0, hy0, hx1, hy1))
        
        if hero_crop.width > 2200:
            ratio = 2200 / hero_crop.width
            hero_crop = hero_crop.resize((2200, int(hero_crop.height * ratio)), Image.Resampling.LANCZOS)
            
        hero_webp = os.path.join(MODELS_DIR, f"{slug}-hero.webp")
        hero_jpg = os.path.join(MODELS_DIR, f"{slug}-hero.jpg")
        hero_crop.save(hero_webp, "WEBP", quality=92, method=6)
        hero_crop.save(hero_jpg, "JPEG", quality=92, optimize=True)
        print(f"  Saved Hero: {hero_webp} ({hero_crop.size})")
        
        # 2. Card Crop (16:10 aspect ratio 1280x800)
        cx0 = int(w * cfg["card_box_pct"][0])
        cy0 = int(h * cfg["card_box_pct"][1])
        cx1 = int(w * cfg["card_box_pct"][2])
        cy1 = int(h * cfg["card_box_pct"][3])
        card_crop = img_rgb.crop((cx0, cy0, cx1, cy1))
        
        target_w, target_h = 1280, 800
        target_ratio = target_w / target_h
        current_ratio = card_crop.width / card_crop.height
        
        if current_ratio > target_ratio:
            new_w = int(card_crop.height * target_ratio)
            left = (card_crop.width - new_w) // 2
            card_crop = card_crop.crop((left, 0, left + new_w, card_crop.height))
        else:
            new_h = int(card_crop.width / target_ratio)
            top = (card_crop.height - new_h) // 2
            card_crop = card_crop.crop((0, top, card_crop.width, top + new_h))
            
        card_crop = card_crop.resize((target_w, target_h), Image.Resampling.LANCZOS)
        card_webp = os.path.join(MODELS_DIR, f"{slug}-card.webp")
        card_jpg = os.path.join(MODELS_DIR, f"{slug}-card.jpg")
        card_crop.save(card_webp, "WEBP", quality=88, method=6)
        card_crop.save(card_jpg, "JPEG", quality=88, optimize=True)
        print(f"  Saved Card: {card_webp} ({card_crop.size})")

print("All tailored assets generated successfully!")

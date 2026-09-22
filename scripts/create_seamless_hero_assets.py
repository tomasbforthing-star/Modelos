import os
import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

def create_seamless_hero_asset(
    src_file,
    crop_box_pct,
    car_safe_box_pct,
    output_slug,
    target_width=2200,
    target_height=1200,
    feather_power=1.5
):
    src_path = os.path.join("VISUALES", src_file)
    with Image.open(src_path) as img:
        img_rgb = img.convert("RGB")
        w, h = img_rgb.size
        
        # 1. Crop original
        x0 = int(w * crop_box_pct[0])
        y0 = int(h * crop_box_pct[1])
        x1 = int(w * crop_box_pct[2])
        y1 = int(h * crop_box_pct[3])
        cropped = img_rgb.crop((x0, y0, x1, y1))
        
        # 2. Resize to working size
        resized = cropped.resize((target_width, target_height), Image.Resampling.LANCZOS)
        arr = np.array(resized, dtype=np.float32)
        
        rw, rh = target_width, target_height
        
        # 3. Build 2D weight mask (1.0 = original image, 0.0 = pure white #FFFFFF)
        safe_x0 = int(rw * car_safe_box_pct[0])
        safe_y0 = int(rh * car_safe_box_pct[1])
        safe_x1 = int(rw * car_safe_box_pct[2])
        safe_y1 = int(rh * car_safe_box_pct[3])
        
        # 1D falloffs:
        x_mask = np.ones(rw, dtype=np.float32)
        if safe_x0 > 0:
            t = np.linspace(0, 1, safe_x0, endpoint=False)
            x_mask[:safe_x0] = t ** feather_power
            
        if safe_x1 < rw:
            t = np.linspace(1, 0, rw - safe_x1, endpoint=True)
            x_mask[safe_x1:] = t ** feather_power
            
        y_mask = np.ones(rh, dtype=np.float32)
        if safe_y0 > 0:
            t = np.linspace(0, 1, safe_y0, endpoint=False)
            y_mask[:safe_y0] = t ** feather_power
            
        if safe_y1 < rh:
            t = np.linspace(1, 0, rh - safe_y1, endpoint=True)
            y_mask[safe_y1:] = t ** feather_power
            
        mask_2d = np.outer(y_mask, x_mask)
        mask_3d = np.expand_dims(mask_2d, axis=2)
        
        white_canvas = np.full_like(arr, 255.0)
        blended = arr * mask_3d + white_canvas * (1.0 - mask_3d)
        blended = np.clip(blended, 0, 255).astype(np.uint8)
        
        out_img = Image.fromarray(blended, mode="RGB")
        
        os.makedirs("public/assets/models", exist_ok=True)
        webp_path = f"public/assets/models/{output_slug}-hero.webp"
        jpg_path = f"public/assets/models/{output_slug}-hero.jpg"
        out_img.save(webp_path, "WEBP", quality=93, method=6)
        out_img.save(jpg_path, "JPEG", quality=93, optimize=True)
        print(f"Generated seamless hero asset: {webp_path} ({out_img.size})")

MODELS_CONFIG = {
    "s7-reev": {
        "src_file": "S7 REEV.jpg",
        "crop_box_pct": (0.12, 0.28, 0.90, 0.88),
        "car_safe_box_pct": (0.15, 0.12, 0.88, 0.82),
        "feather_power": 1.5
    },
    "v9-phev": {
        "src_file": "V9.jpg",
        "crop_box_pct": (0.05, 0.05, 0.95, 0.85),
        "car_safe_box_pct": (0.12, 0.10, 0.88, 0.80),
        "feather_power": 1.5
    },
    "t5-hev": {
        "src_file": "T5 HEV.jpg",
        # Crop to x: 0.05 to 0.58 so the car is front-and-center and text is 100% excluded
        "crop_box_pct": (0.05, 0.16, 0.58, 0.84),
        "car_safe_box_pct": (0.14, 0.12, 0.86, 0.80),
        "feather_power": 1.5
    },
    "friday-reev": {
        "src_file": "Friday Reev.jpg",
        "crop_box_pct": (0.00, 0.24, 0.74, 0.84),
        "car_safe_box_pct": (0.10, 0.14, 0.86, 0.80),
        "feather_power": 1.5
    },
    "u-tour-hev": {
        "src_file": "U-TOUR HEV.png",
        "crop_box_pct": (0.00, 0.05, 0.95, 0.90),
        "car_safe_box_pct": (0.12, 0.10, 0.88, 0.80),
        "feather_power": 1.5
    }
}

if __name__ == "__main__":
    for slug, cfg in MODELS_CONFIG.items():
        create_seamless_hero_asset(
            src_file=cfg["src_file"],
            crop_box_pct=cfg["crop_box_pct"],
            car_safe_box_pct=cfg["car_safe_box_pct"],
            output_slug=slug,
            feather_power=cfg["feather_power"]
        )

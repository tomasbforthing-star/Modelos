import os
import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

MODELS_DIR = os.path.join("public", "assets", "models")
os.makedirs(MODELS_DIR, exist_ok=True)

def generate_perfect_hero_asset(
    slug,
    src_filename,
    # Safe box in normalized coordinates (0.0 to 1.0) of original image:
    # Within this box, the image is 100% ORIGINAL, untouched, ZERO fade.
    car_safe_box, # (left_safe, top_safe, right_safe, bottom_safe)
    # Transition start margins: where the fade to pure white begins
    fade_margins, # (left_fade_start, top_fade_start, right_fade_start, bottom_fade_start)
    target_width=2400
):
    src_path = os.path.join("VISUALES", src_filename)
    print(f"\n=======================================================")
    print(f"Processing {slug} from {src_path}...")
    
    with Image.open(src_path) as img:
        img_rgb = img.convert("RGB")
        ow, oh = img_rgb.size
        orig_aspect = ow / oh
        
        # STRICT UNIFORM SCALE: single factor for width and height
        scale = target_width / ow
        target_height = int(oh * scale)
        scaled = img_rgb.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
        arr = np.array(scaled, dtype=np.float32)
        rw, rh = target_width, target_height
        
        print(f"  Original: {ow}x{oh} (aspect: {orig_aspect:.4f})")
        print(f"  Scaled:   {rw}x{rh} (aspect: {rw/rh:.4f}) -> STRICT UNIFORM SCALE (zero distortion)")
        
        # Coordinates in target image:
        safe_l = int(rw * car_safe_box[0])
        safe_t = int(rh * car_safe_box[1])
        safe_r = int(rw * car_safe_box[2])
        safe_b = int(rh * car_safe_box[3])
        
        fade_l = int(rw * fade_margins[0])
        fade_t = int(rh * fade_margins[1])
        fade_r = int(rw * fade_margins[2])
        fade_b = int(rh * fade_margins[3])
        
        # Build smooth 1D alpha weights (1.0 = original, 0.0 = pure white)
        # Horizontal weight:
        # [0 .. fade_l] -> smooth curve from 0.0 to 1.0
        # [fade_l .. fade_r] -> 1.0 (constant 100% original)
        # [fade_r .. rw] -> smooth curve from 1.0 to 0.0
        x_weight = np.ones(rw, dtype=np.float32)
        if fade_l > 0:
            # Smooth cosine / polynomial curve for natural aesthetic blending
            t = np.linspace(0, 1, fade_l)
            # Smoothstep curve: 3t^2 - 2t^3
            x_weight[:fade_l] = (3 * t**2 - 2 * t**3)
        if fade_r < rw:
            t = np.linspace(1, 0, rw - fade_r)
            x_weight[fade_r:] = (3 * t**2 - 2 * t**3)
            
        # Vertical weight:
        # [0 .. fade_t] -> smooth curve from 0.0 to 1.0
        # [fade_t .. fade_b] -> 1.0 (constant 100% original)
        # [fade_b .. rh] -> smooth curve from 1.0 to 0.0
        y_weight = np.ones(rh, dtype=np.float32)
        if fade_t > 0:
            t = np.linspace(0, 1, fade_t)
            y_weight[:fade_t] = (3 * t**2 - 2 * t**3)
        if fade_b < rh:
            t = np.linspace(1, 0, rh - fade_b)
            y_weight[fade_b:] = (3 * t**2 - 2 * t**3)
            
        # Combine 2D mask
        mask_2d = np.outer(y_weight, x_weight)
        
        # Ensure mask is strictly 1.0 in the entire car safe box
        mask_2d[safe_t:safe_b, safe_l:safe_r] = 1.0
        
        mask_3d = np.expand_dims(mask_2d, axis=2)
        
        # White background canvas
        white_canvas = np.full_like(arr, 255.0)
        
        # Blend output
        blended = arr * mask_3d + white_canvas * (1.0 - mask_3d)
        blended = np.clip(blended, 0, 255).astype(np.uint8)
        
        out_img = Image.fromarray(blended, mode="RGB")
        
        # Save hero images (WEBP and JPEG)
        hero_webp = os.path.join(MODELS_DIR, f"{slug}-hero.webp")
        hero_jpg = os.path.join(MODELS_DIR, f"{slug}-hero.jpg")
        out_img.save(hero_webp, "WEBP", quality=94, method=6)
        out_img.save(hero_jpg, "JPEG", quality=94, optimize=True)
        print(f"  Saved Hero: {hero_webp} ({out_img.size}, aspect: {out_img.width/out_img.height:.4f})")
        
        # Generate Card image (16:10 aspect 1280x800) with uniform scaling from original
        card_target_w, card_target_h = 1280, 800
        card_target_aspect = card_target_w / card_target_h # 1.60
        
        # Crop centered from original with target aspect ratio
        if orig_aspect > card_target_aspect:
            # Crop horizontal sides
            crop_w = int(oh * card_target_aspect)
            crop_x0 = (ow - crop_w) // 2
            card_crop = img_rgb.crop((crop_x0, 0, crop_x0 + crop_w, oh))
        else:
            # Crop vertical top/bottom
            crop_h = int(ow / card_target_aspect)
            crop_y0 = (oh - crop_h) // 2
            card_crop = img_rgb.crop((0, crop_y0, ow, crop_y0 + crop_h))
            
        card_resized = card_crop.resize((card_target_w, card_target_h), Image.Resampling.LANCZOS)
        card_webp = os.path.join(MODELS_DIR, f"{slug}-card.webp")
        card_jpg = os.path.join(MODELS_DIR, f"{slug}-card.jpg")
        card_resized.save(card_webp, "WEBP", quality=90, method=6)
        card_resized.save(card_jpg, "JPEG", quality=90, optimize=True)
        print(f"  Saved Card: {card_webp} ({card_resized.size})")

# Configuration tailored individually for each model from raw VISUALES files:
CONFIGS = {
    "s7-reev": {
        "src_filename": "S7 REEV.jpg",
        # Car body is at x: 0.24 to 0.83, y: 0.40 to 0.79.
        # Safe box: 100% untouched car (front, hood, roof, rear, wheels, road shadow)
        "car_safe_box": (0.23, 0.38, 0.85, 0.82),
        # Fade only in the empty outer space (x < 0.20 on left, top y < 0.18, bottom y > 0.90, right x > 0.92)
        "fade_margins": (0.20, 0.15, 0.92, 0.88)
    },
    "v9-phev": {
        "src_filename": "V9.jpg",
        # Car is at x: 0.10 to 0.91, y: 0.26 to 0.74. V9 sign is at x: 0.75 to 0.93, y: 0.14 to 0.27.
        # Safe box preserves entire car + wheels + V9 inscription 100% intact with zero deformation:
        "car_safe_box": (0.09, 0.12, 0.94, 0.78),
        # Fade only at the very perimeter of the room (x < 0.06, top y < 0.08, bottom y > 0.85, right x > 0.97)
        "fade_margins": (0.07, 0.08, 0.96, 0.84)
    },
    "t5-hev": {
        "src_filename": "T5 HEV.jpg",
        # Car is at x: 0.16 to 0.68, y: 0.26 to 0.76.
        # Safe box preserves the entire T5 front, grille, headlights, roof, wheels, and body:
        "car_safe_box": (0.15, 0.24, 0.70, 0.79),
        # Fade only in empty background (left x < 0.12, top y < 0.12, right x > 0.74, bottom y > 0.86)
        "fade_margins": (0.12, 0.12, 0.74, 0.84)
    },
    "friday-reev": {
        "src_filename": "Friday Reev.jpg",
        # Car is at x: 0.06 to 0.71, y: 0.34 to 0.76 (includes license plate "FORTHING FRIDAY" at x: 0.63 to 0.70).
        # Safe box preserves full car silhouette, front bumper, headlights, license plate, wheels, and ground:
        "car_safe_box": (0.05, 0.30, 0.72, 0.79),
        # Fade only in empty sky and outer grass (left x < 0.04, top y < 0.18, right x > 0.75, bottom y > 0.86)
        "fade_margins": (0.04, 0.18, 0.75, 0.84)
    },
    "u-tour-hev": {
        "src_filename": "U-TOUR HEV.png",
        # Car is at x: 0.15 to 0.86, y: 0.16 to 0.82 (includes prominent grille on left and full rear on right).
        # Safe box preserves full grille, bumper, headlights, roof, rear, wheels, and shadow:
        "car_safe_box": (0.13, 0.14, 0.88, 0.84),
        # Fade only in the outer gray studio space (left x < 0.10, top y < 0.08, right x > 0.91, bottom y > 0.88)
        "fade_margins": (0.10, 0.08, 0.91, 0.88)
    }
}

if __name__ == "__main__":
    for slug, cfg in CONFIGS.items():
        generate_perfect_hero_asset(
            slug=slug,
            src_filename=cfg["src_filename"],
            car_safe_box=cfg["car_safe_box"],
            fade_margins=cfg["fade_margins"]
        )
    print("\nAll 5 perfect hero assets generated with 100% aspect ratio preservation!")

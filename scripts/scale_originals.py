from PIL import Image
Image.MAX_IMAGE_PIXELS = None

# Let's create an accurate 2400-wide preview with strictly uniform scale
files = {
    's7-reev': 'VISUALES/S7 REEV.jpg',
    'v9-phev': 'VISUALES/V9.jpg',
    't5-hev': 'VISUALES/T5 HEV.jpg',
    'friday-reev': 'VISUALES/Friday Reev.jpg',
    'u-tour-hev': 'VISUALES/U-TOUR HEV.png'
}

import os
os.makedirs('full_scaled_originals', exist_ok=True)

for slug, path in files.items():
    with Image.open(path) as img:
        img_rgb = img.convert("RGB")
        ow, oh = img_rgb.size
        target_w = 2400
        # Strict uniform scale
        scale = target_w / ow
        target_h = int(oh * scale)
        scaled = img_rgb.resize((target_w, target_h), Image.Resampling.LANCZOS)
        out_path = f"full_scaled_originals/{slug}_2400.jpg"
        scaled.save(out_path, quality=92)
        print(f"Saved {out_path} ({target_w}x{target_h}, aspect={target_w/target_h:.4f}) - ZERO deformation from {ow}x{oh}")

from PIL import Image
Image.MAX_IMAGE_PIXELS = None
import os

files = {
    'S7 REEV': 'S7 REEV.jpg',
    'V9 PHEV': 'V9.jpg',
    'T5 HEV': 'T5 HEV.jpg',
    'FRIDAY REEV': 'Friday Reev.jpg',
    'U-TOUR HEV': 'U-TOUR HEV.png'
}

os.makedirs('temp_inspections', exist_ok=True)

for name, filename in files.items():
    path = os.path.join('VISUALES', filename)
    img = Image.open(path)
    # Generate a lightweight preview 1920x1280
    w, h = img.size
    preview = img.resize((1920, int(1920 * h / w)), Image.Resampling.LANCZOS)
    preview_path = f'temp_inspections/{name.replace(" ", "_")}_preview.jpg'
    preview.save(preview_path, quality=85)
    print(f'Generated {preview_path} ({preview.size})')

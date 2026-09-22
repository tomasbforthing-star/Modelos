from PIL import Image
import numpy as np

# Load preview images and inspect features
models = {
    'S7 REEV': 'temp_inspections/S7_REEV_preview.jpg',
    'V9 PHEV': 'temp_inspections/V9_PHEV_preview.jpg',
    'T5 HEV': 'temp_inspections/T5_HEV_preview.jpg',
    'FRIDAY REEV': 'temp_inspections/FRIDAY_REEV_preview.jpg',
    'U-TOUR HEV': 'temp_inspections/U-TOUR_HEV_preview.jpg'
}

for name, path in models.items():
    img = Image.open(path)
    w, h = img.size
    print(f"=== {name} ({w}x{h}) ===")
    # Let's save 3 vertical slices (left, center, right) and top/bottom to inspect
    # We can also check where dark/light areas are
    arr = np.array(img)
    # Check left 30% vs right 70%
    left_lum = arr[:, :int(w*0.35)].mean()
    right_lum = arr[:, int(w*0.35):].mean()
    print(f"  Left lum: {left_lum:.1f}, Right lum: {right_lum:.1f}")

from PIL import Image, ImageDraw, ImageFont
import os

models = {
    'S7_REEV': 'temp_inspections/S7_REEV_preview.jpg',
    'V9_PHEV': 'temp_inspections/V9_PHEV_preview.jpg',
    'T5_HEV': 'temp_inspections/T5_HEV_preview.jpg',
    'FRIDAY_REEV': 'temp_inspections/FRIDAY_REEV_preview.jpg',
    'U-TOUR_HEV': 'temp_inspections/U-TOUR_HEV_preview.jpg'
}

# Create a visual grid with percentage lines on each image so we can pinpoint exact coordinates
for name, path in models.items():
    img = Image.open(path).convert('RGB')
    draw = ImageDraw.Draw(img)
    w, h = img.size
    
    # Draw horizontal & vertical grid lines every 10%
    for x_pct in range(10, 100, 10):
        x = int(w * x_pct / 100)
        draw.line([(x, 0), (x, h)], fill=(255, 0, 0) if x_pct in (30, 50, 70) else (100, 100, 255), width=2 if x_pct in (30, 50, 70) else 1)
        draw.text((x + 4, 20), f"{x_pct}%", fill=(255, 255, 0))
        
    for y_pct in range(10, 100, 10):
        y = int(h * y_pct / 100)
        draw.line([(0, y), (w, y)], fill=(255, 0, 0) if y_pct in (30, 50, 70) else (100, 100, 255), width=2 if y_pct in (30, 50, 70) else 1)
        draw.text((20, y + 4), f"{y_pct}%", fill=(255, 255, 0))
        
    grid_path = f'temp_inspections/{name}_grid.jpg'
    img.save(grid_path, quality=85)
    print(f'Saved {grid_path}')

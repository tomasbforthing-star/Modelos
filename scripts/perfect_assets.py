import os
import fitz

doc = fitz.open("VISUALES/LogoForthing.pdf")
page = doc[0]
svg = page.get_svg_image()

lines = svg.splitlines()
new_lines = []

for i, line in enumerate(lines):
    if i == 7: # Outer shield
        new_lines.append(line.replace('/>', ' fill="#ffffff"/>'))
    elif i == 8: # Shield border
        new_lines.append(line) # already has fill="#ffffff"
    elif i == 9: # Inner shield background
        new_lines.append(line.replace('/>', ' fill="#222223"/>'))
    elif 10 <= i <= 32: # Lion inner details
        new_lines.append(line) # already has fill="#ffffff"
    elif i >= 33 and '<path' in line: # Letters FORTHING and ARGENTINA
        new_lines.append(line.replace('/>', ' fill="#ffffff"/>'))
    else:
        new_lines.append(line)

perfect_svg = "\n".join(new_lines)
with open("public/assets/logo-forthing-white.svg", "w", encoding="utf-8") as f:
    f.write(perfect_svg)

print("Generated perfect logo-forthing-white.svg with visible lion!")

# Also generate clean T5 EVO photo from media_1790008364405.jpg (tablet mockup with clean centered car)
from PIL import Image
tablet_mockup = r"C:\Users\admin\.gemini\antigravity\brain\581bbba9-eeec-4bd6-802a-cc879601574d\.user_uploaded\media_1790008364405.jpg"
if os.path.exists(tablet_mockup):
    with Image.open(tablet_mockup) as img:
        w, h = img.size
        # The car in tablet mockup is centered vertically between text and features
        # Roughly y: 0.295 to 0.58, x: 0.08 to 0.92
        car_box = (int(w * 0.06), int(h * 0.295), int(w * 0.94), int(h * 0.58))
        car = img.crop(car_box)
        car.save("public/assets/models/t5-evo-hero.webp", "WEBP", quality=95)
        car.convert("RGB").save("public/assets/models/t5-evo-hero.jpg", "JPEG", quality=95)
        
        card = car.resize((1280, 800), Image.Resampling.LANCZOS)
        card.save("public/assets/models/t5-evo-card.webp", "WEBP", quality=92)
        card.convert("RGB").save("public/assets/models/t5-evo-card.jpg", "JPEG", quality=92)
        print("Updated T5 EVO clean centered car crops")

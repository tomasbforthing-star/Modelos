from PIL import Image
Image.MAX_IMAGE_PIXELS = None

files = {
    'S7': 'VISUALES/S7 REEV.jpg',
    'V9': 'VISUALES/V9.jpg',
    'T5': 'VISUALES/T5 HEV.jpg',
    'FRIDAY': 'VISUALES/Friday Reev.jpg',
    'UTOUR': 'VISUALES/U-TOUR HEV.png'
}

for name, path in files.items():
    img = Image.open(path)
    w, h = img.size
    print(f"\n==================== {name} ({w}x{h}, aspect={w/h:.4f}) ====================")
    # Let's inspect where car sits

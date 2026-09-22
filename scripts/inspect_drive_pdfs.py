import urllib.request
import re
import os
import fitz

urls = {
    'S7_REEV': 'https://drive.google.com/file/d/1fHfzj9zrIKU6_wms7XKe6k98OxYdcaZL/view?usp=drive_link',
    'V9_PHEV': 'https://drive.google.com/file/d/1OfCLVIz99kxdzSrckUoc8sa4NnNqKaQq/view?usp=drive_link',
    'T5_HEV': 'https://drive.google.com/file/d/1ssISOzhq2dpGpLRrTMTxL0ghRXQZcydm/view?usp=drive_link',
    'FRIDAY_REEV': 'https://drive.google.com/file/d/1EK1L7eriW0uQ9FKTDgVUkqwZKCmPmOkU/view?usp=drive_link',
    'U_TOUR_HEV': 'https://drive.google.com/file/d/1tFNRbcRe3bll9CqDbiKDmS5NFZTTluZb/view?usp=drive_link'
}

os.makedirs('downloaded_specs', exist_ok=True)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for name, url in urls.items():
    file_id = re.search(r'/d/([^/]+)', url).group(1)
    direct_url = f'https://drive.google.com/uc?export=download&id={file_id}'
    out_path = os.path.join('downloaded_specs', f'{name}.pdf')
    print(f'=== Downloading {name} ({file_id}) ===')
    try:
        req = urllib.request.Request(direct_url, headers=headers)
        with urllib.request.urlopen(req) as resp, open(out_path, 'wb') as f:
            content = resp.read()
            f.write(content)
        
        # Check if Google gave HTML (e.g. virus scan warning or auth required) or actual PDF
        if content.startswith(b'%PDF'):
            doc = fitz.open(out_path)
            print(f'SUCCESS: Valid PDF with {len(doc)} pages, size: {len(content)} bytes')
            full_text = ""
            for i, page in enumerate(doc):
                t = page.get_text()
                full_text += f"\n--- Page {i+1} ---\n" + t
            print("Extracted Text Sample:")
            print(full_text[:600])
            with open(os.path.join('downloaded_specs', f'{name}.txt'), 'w', encoding='utf-8') as tf:
                tf.write(full_text)
        else:
            print(f'WARNING: Downloaded content is not a PDF! First 200 bytes: {content[:200]}')
    except Exception as e:
        print(f'ERROR downloading {name}: {e}')

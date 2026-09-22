import fitz
import xml.etree.ElementTree as ET

def build_official_logo():
    doc = fitz.open('VISUALES/LogoForthing.pdf')
    page = doc[0]
    
    # Extract SVG
    svg_str = page.get_svg_image()
    
    # Parse XML
    tree = ET.fromstring(svg_str)
    
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
    
    # Adjust viewBox to have nice tight padding around the bounding box (31.3, 16.0 to 1152.6, 264.0)
    # x: 20, y: 10, width: 1145, height: 260
    tree.set('viewBox', '20 10 1145 260')
    tree.set('width', '1145')
    tree.set('height', '260')
    tree.set('preserveAspectRatio', 'xMidYMid meet')
    
    path_idx = 0
    for elem in tree.iter():
        if elem.tag.endswith('path'):
            d = elem.attrib.get('d', '')
            if 'clipPath' in elem.get('id', '') or d.startswith('M0 280H1184'):
                continue
                
            # Drawing paths:
            # 0: outer shield outline
            # 1: middle shield border
            # 2: inner shield background
            # 3..24: lion vector shapes
            # 25..32: brand characters
            # 33..41: FORTHING letters
            
            if path_idx == 2:
                elem.set('fill', 'none') # transparent inside shield
            elif path_idx == 1:
                elem.set('fill', '#ffffff')
            elif path_idx == 0:
                elem.set('fill', 'none')
            else:
                elem.set('fill', '#ffffff')
                
            path_idx += 1
            
    # Write the cleaned SVG
    clean_svg = ET.tostring(tree, encoding='utf-8').decode('utf-8')
    with open('public/assets/logo-forthing-white.svg', 'w', encoding='utf-8') as f:
        f.write(clean_svg)
    with open('dist/assets/logo-forthing-white.svg', 'w', encoding='utf-8') as f:
        f.write(clean_svg)
        
    print(f'Processed {path_idx} drawing paths into logo-forthing-white.svg with updated viewBox successfully!')

if __name__ == '__main__':
    build_official_logo()

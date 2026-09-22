import os
import re

svg_path = os.path.join("public", "assets", "logo-forthing.svg")
with open(svg_path, "r", encoding="utf-8") as f:
    svg = f.read()

def replacer(match):
    tag = match.group(0)
    if "fill=" not in tag:
        return tag[:-1] + ' fill="#ffffff"/>'
    return tag

white_svg = re.sub(r'<path[^>]*/>', replacer, svg)

with open(os.path.join("public", "assets", "logo-forthing-white.svg"), "w", encoding="utf-8") as f:
    f.write(white_svg)

print("logo-forthing-white.svg created successfully!")

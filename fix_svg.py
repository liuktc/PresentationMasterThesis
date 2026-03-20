"""
Fix SVG files for Manim rendering by adjusting colors and handling embedded images.
"""

import xml.etree.ElementTree as ET
import re
from pathlib import Path
import base64
from io import BytesIO
from PIL import Image


def has_embedded_image(svg_path):
    """Check if SVG has embedded image data."""
    with open(svg_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return 'data:image' in content


def fix_svg_for_manim(svg_path, output_path=None, text_color="#ffffff", bg_color="#1c2128"):
    """
    Fix an SVG file for Manim by:
    1. Converting light text colors to readable colors
    2. Adjusting background and axis colors for dark theme
    3. Preserving the colorbar image
    """
    
    if output_path is None:
        output_path = svg_path
    
    # Read the SVG
    with open(svg_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace light gray text color with white
    content = content.replace('#e6edf3', text_color)
    
    # Replace light grid colors with slightly lighter gray for visibility on dark background
    content = content.replace('#2f3a46', '#404a56')
    
    # Optional: enhance the embedded image contrast if present
    if 'data:image/png;base64,' in content:
        content = enhance_embedded_image_contrast(content)
    
    # Write the fixed SVG
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Fixed {svg_path}")
    print(f"  - Changed text color to {text_color}")
    print(f"  - Changed grid/axis color")
    if 'data:image/png;base64,' in content:
        print(f"  - Enhanced embedded image")


def enhance_embedded_image_contrast(svg_content):
    """Enhance contrast of embedded PNG images for better visibility."""
    # Find all embedded PNG images
    pattern = r'data:image/png;base64,([A-Za-z0-9+/=]+)'
    
    def enhance_image_data(match):
        b64_data = match.group(1)
        try:
            # Decode the base64 image
            img_data = base64.b64decode(b64_data)
            img = Image.open(BytesIO(img_data))
            
            # Enhance contrast (simple approach)
            from PIL import ImageEnhance
            enhancer = ImageEnhance.Contrast(img)
            enhanced = enhancer.enhance(1.2)  # Increase contrast by 20%
            
            # Encode back to base64
            buffered = BytesIO()
            enhanced.save(buffered, format="PNG")
            new_b64 = base64.b64encode(buffered.getvalue()).decode()
            
            return f'data:image/png;base64,{new_b64}'
        except Exception as e:
            print(f"  - Warning: Could not enhance image contrast: {e}")
            return match.group(0)
    
    return re.sub(pattern, enhance_image_data, svg_content)


def fix_all_svgs(directory="scenes/figures_dark"):
    """Fix all SVG files in the figures_dark directory."""
    svg_dir = Path(directory)
    svg_files = list(svg_dir.glob("*.svg"))
    
    for svg_file in svg_files:
        try:
            fix_svg_for_manim(str(svg_file))
        except Exception as e:
            print(f"✗ Error fixing {svg_file}: {e}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        fix_all_svgs()
    elif len(sys.argv) > 1:
        fix_svg_for_manim(sys.argv[1])
    else:
        print("Usage:")
        print("  python fix_svg.py <svg_file>          - Fix a single SVG")
        print("  python fix_svg.py --all               - Fix all SVGs in scenes/figures_dark/")
        
        if "--all" in sys.argv:
            fix_all_svgs()

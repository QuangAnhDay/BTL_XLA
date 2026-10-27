import os
import sys
import subprocess
import glob
import re
from playwright.sync_api import sync_playwright

output_dir = "rendered_slides"
os.makedirs(output_dir, exist_ok=True)
svg_dir = os.path.join(output_dir, "svg_output")

# Step 1: Convert PPTX to SVG using pptx_to_svg.py with --embed-images
pptx_file = "ASL_Preprocessing_CNN_Evaluation.pptx"
pptx_to_svg_script = r"F:\OneDrive\hoc hanh\skill-pptx\skills\ppt-master\scripts\pptx_to_svg.py"

cmd = [sys.executable, pptx_to_svg_script, pptx_file, "-o", svg_dir, "--inheritance-mode", "flat", "--embed-images"]
res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")

# Step 2: Render each SVG to PNG using Playwright
all_svgs = glob.glob(os.path.join(svg_dir, "**", "*.svg"), recursive=True)

def get_slide_num(path):
    m = re.search(r'slide[_-]?(\d+)\.svg', os.path.basename(path), re.IGNORECASE)
    return int(m.group(1)) if m else 999

svg_files = [p for p in all_svgs if "slide" in os.path.basename(p).lower()]
svg_files = sorted(svg_files, key=get_slide_num)

print(f"Found {len(svg_files)} SVG slide files.")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 720})
    
    for i, svg_path in enumerate(svg_files):
        slide_num = i + 1
        with open(svg_path, "r", encoding="utf-8") as f:
            svg_content = f.read()
            
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ background: #FFFFFF; display: flex; justify-content: center; align-items: center; width: 1280px; height: 720px; overflow: hidden; }}
                svg {{ width: 1280px; height: 720px; }}
            </style>
        </head>
        <body>
            {svg_content}
        </body>
        </html>
        """
        page.set_content(html_content)
        page.wait_for_timeout(300) # Ensure fonts and layout stabilize
        
        png_path = os.path.join(output_dir, f"slide_{slide_num:02d}.png")
        page.screenshot(path=png_path)
        print(f"Rendered Slide {slide_num:02d} -> {png_path}")
        
    browser.close()

print("All slides re-rendered with embedded images successfully.")

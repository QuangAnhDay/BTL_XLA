import json
from collections import Counter

with open('reference_design_analysis/slides_data.json', encoding='utf-8') as f:
    slides = json.load(f)

text_colors = Counter()
fill_colors = Counter()
line_colors = Counter()
fonts = Counter()
font_sizes = Counter()

for s in slides:
    for sp in s['shapes']:
        if 'fill_color' in sp and sp['fill_color'] and sp['fill_color'] != 'None':
            fill_colors[sp['fill_color']] += 1
        if 'line_color' in sp and sp['line_color'] and sp['line_color'] != 'None' and 'Type(None)' not in sp['line_color']:
            line_colors[sp['line_color']] += 1
            
        if 'text_frame' in sp:
            for p in sp['text_frame']['paragraphs']:
                for r in p['runs']:
                    if r.get('color'):
                        text_colors[r['color']] += 1
                    if r.get('font_name'):
                        fonts[r['font_name']] += 1
                    if r.get('font_size_pt'):
                        font_sizes[r['font_size_pt']] += 1

print("--- TEXT COLORS ---")
for c, count in text_colors.most_common():
    print(f"  {c}: {count} runs")

print("\n--- FILL COLORS ---")
for c, count in fill_colors.most_common():
    print(f"  {c}: {count} shapes")

print("\n--- LINE COLORS ---")
for c, count in line_colors.most_common():
    print(f"  {c}: {count} shapes")

print("\n--- FONTS ---")
for f, count in fonts.most_common():
    print(f"  {f}: {count} runs")

print("\n--- FONT SIZES (pt) ---")
for sz, count in sorted(font_sizes.items(), key=lambda x: x[0]):
    print(f"  {sz:5.2f} pt: {count} runs")

import json

with open('reference_design_analysis/slides_data.json', encoding='utf-8') as f:
    slides = json.load(f)

# 1. Kicker bar coordinates across slides
kickers = []
for s in slides:
    for sp in s['shapes']:
        if sp.get('name') in ['shape-1', 'shape-6', 'shape-14', 'shape-27', 'shape-43', 'shape-148', 'shape-216', 'shape-220', 'shape-272', 'shape-291', 'shape-295', 'shape-302', 'shape-391', 'shape-396']:
            kickers.append((s['slide_index'], sp['name'], sp['left_pt'], sp['top_pt'], sp['width_pt'], sp['height_pt'], sp.get('fill_color')))
        elif sp.get('width_pt') == 27.0 and sp.get('height_pt') == 3.75:
            kickers.append((s['slide_index'], sp['name'], sp['left_pt'], sp['top_pt'], sp['width_pt'], sp['height_pt'], sp.get('fill_color')))

print(f"Kicker bars found ({len(kickers)}):")
for k in kickers:
    print(f"  Slide {k[0]:02d}: box=({k[2]}, {k[3]}, {k[4]}, {k[5]}) pt, fill={k[6]}")

# 2. Slide titles and subtitles coordinates across slides 2-13
print("\nTitles and Subtitles:")
for s in slides:
    idx = s['slide_index']
    t_shape = next((sp for sp in s['shapes'] if sp.get('name') == 'TITLE'), None)
    sub_shape = next((sp for sp in s['shapes'] if sp.get('name') == 'SUBTITLE'), None)
    if t_shape:
        print(f"  Slide {idx:02d} TITLE: left={t_shape['left_pt']}, top={t_shape['top_pt']}, w={t_shape['width_pt']}, h={t_shape['height_pt']}")
    if sub_shape:
        print(f"  Slide {idx:02d} SUBTITLE: left={sub_shape['left_pt']}, top={sub_shape['top_pt']}, w={sub_shape['width_pt']}, h={sub_shape['height_pt']}")

# 3. Page numbers coordinates
print("\nPage numbers:")
for s in slides:
    idx = s['slide_index']
    p_shape = next((sp for sp in s['shapes'] if sp.get('name') == 'PAGE'), None)
    if p_shape:
        print(f"  Slide {idx:02d} PAGE: left={p_shape['left_pt']}, top={p_shape['top_pt']}, w={p_shape['width_pt']}, h={p_shape['height_pt']}")

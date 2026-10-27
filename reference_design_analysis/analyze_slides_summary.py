import json

with open('reference_design_analysis/slides_data.json', encoding='utf-8') as f:
    slides = json.load(f)

out_lines = []
out_lines.append(f"Total slides: {len(slides)}")

for s in slides:
    idx = s['slide_index']
    out_lines.append(f"\n==================== SLIDE {idx:02d} ====================")
    shape_types = [shape['type'] for shape in s['shapes']]
    out_lines.append(f"Shapes count: {len(s['shapes'])} | Types: {set(shape_types)}")
    
    # Analyze text frames
    texts = []
    for sp in s['shapes']:
        if 'text_frame' in sp and sp['text_frame']['text']:
            t = sp['text_frame']['text'].replace('\n', ' // ')
            runs = []
            for p in sp['text_frame']['paragraphs']:
                for r in p['runs']:
                    r_str = f"'{r['text']}' (sz={r['font_size_pt']}, bld={r['bold']}, font={r['font_name']}, clr={r['color']})"
                    runs.append(r_str)
            texts.append({
                "name": sp['name'],
                "box": (sp['left_pt'], sp['top_pt'], sp['width_pt'], sp['height_pt']),
                "text": t,
                "runs_summary": runs
            })
    out_lines.append(f"Text shapes ({len(texts)}):")
    for t in texts:
        out_lines.append(f"  [{t['name']}] at box {t['box']}: {t['text'][:100]}")
        for r in t['runs_summary']:
            out_lines.append(f"      run: {r}")

    # Analyze pictures
    pics = [sp for sp in s['shapes'] if 'PICTURE' in sp['type']]
    if pics:
        out_lines.append(f"Pictures ({len(pics)}):")
        for p in pics:
            out_lines.append(f"  [{p['name']}] at box: ({p['left_pt']}, {p['top_pt']}, {p['width_pt']}, {p['height_pt']}) | file: {p.get('image_filename')}")

    # Analyze auto shapes / cards / lines
    shapes_other = [sp for sp in s['shapes'] if 'PICTURE' not in sp['type'] and ('AUTO_SHAPE' in sp['type'] or 'FREEFORM' in sp['type'] or 'LINE' in sp['type'])]
    if shapes_other:
        out_lines.append(f"Other shapes ({len(shapes_other)}):")
        for sp in shapes_other:
            out_lines.append(f"  [{sp['name']}] type={sp['type']} at ({sp['left_pt']}, {sp['top_pt']}, {sp['width_pt']}, {sp['height_pt']}) fill={sp.get('fill_color')} line={sp.get('line_color')}")

with open('reference_design_analysis/slides_summary.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(out_lines))

print("Summary written to reference_design_analysis/slides_summary.txt")

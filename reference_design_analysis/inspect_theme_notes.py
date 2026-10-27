import zipfile
import xml.etree.ElementTree as ET
import json
import re

pptx_path = r"F:\OneDrive\hoc hanh\XLA\slide\Panorama_Stitching_14_Slides.pptx"

with zipfile.ZipFile(pptx_path, 'r') as z:
    file_list = z.namelist()
    
    # 1. Read theme1.xml
    theme_xml = ""
    for name in file_list:
        if "theme/theme1.xml" in name:
            theme_xml = z.read(name).decode('utf-8')
            break
            
    # Parse theme colors
    theme_colors = {}
    if theme_xml:
        root = ET.fromstring(theme_xml)
        ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
        clrScheme = root.find('.//a:clrScheme', ns)
        if clrScheme is not None:
            for child in clrScheme:
                tag = child.tag.split('}')[-1]
                srgb = child.find('a:srgbClr', ns)
                sysclr = child.find('a:sysClr', ns)
                if srgb is not None:
                    theme_colors[tag] = srgb.attrib.get('val')
                elif sysclr is not None:
                    theme_colors[tag] = sysclr.attrib.get('lastClr', sysclr.attrib.get('val'))
                    
        # Parse font scheme
        fontScheme = root.find('.//a:fontScheme', ns)
        font_info = {}
        if fontScheme is not None:
            major = fontScheme.find('a:majorFont/a:latin', ns)
            minor = fontScheme.find('a:minorFont/a:latin', ns)
            font_info['major'] = major.attrib.get('typeface') if major is not None else None
            font_info['minor'] = minor.attrib.get('typeface') if minor is not None else None
    
    print("Theme colors:", json.dumps(theme_colors, indent=2))
    print("Theme fonts:", json.dumps(font_info, indent=2))
    
    # Check notes
    notes_dict = {}
    for name in file_list:
        m = re.match(r'ppt/notesSlides/notesSlide(\d+)\.xml', name)
        if m:
            slide_idx = m.group(1)
            content = z.read(name).decode('utf-8')
            root = ET.fromstring(content)
            ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
                  'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
            # extract all text
            texts = [elem.text for elem in root.findall('.//a:t', ns) if elem.text]
            notes_dict[slide_idx] = "\n".join(texts)
            
    print(f"Found {len(notes_dict)} notes slides.")

with open(r"reference_design_analysis\theme_and_notes.json", "w", encoding="utf-8") as f:
    json.dump({
        "theme_colors": theme_colors,
        "theme_fonts": font_info,
        "notes": notes_dict
    }, f, ensure_ascii=False, indent=2)

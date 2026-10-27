import zipfile
import xml.etree.ElementTree as ET

pptx_path = r"F:\OneDrive\hoc hanh\XLA\slide\Panorama_Stitching_14_Slides.pptx"

with zipfile.ZipFile(pptx_path, 'r') as z:
    for i in range(1, 15):
        xml_name = f'ppt/slides/slide{i}.xml'
        if xml_name in z.namelist():
            content = z.read(xml_name).decode('utf-8')
            root = ET.fromstring(content)
            ns = {
                'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
                'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'
            }
            effects = root.findall('.//a:effectLst/*', ns)
            if effects:
                print(f"Slide {i:02d} has effects: {[e.tag.split('}')[-1] for e in effects]}")
            else:
                pass
print("Done checking effects.")

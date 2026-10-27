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
            bg = root.find('.//p:bg', ns)
            bgPr = root.find('.//p:bgPr', ns)
            if bg is not None:
                print(f"Slide {i} has p:bg: {ET.tostring(bg).decode('utf-8')[:100]}")
            elif bgPr is not None:
                print(f"Slide {i} has p:bgPr: {ET.tostring(bgPr).decode('utf-8')[:100]}")
            else:
                print(f"Slide {i} has no explicit slide bg (uses layout/master default).")

    # Check slide master & layouts
    master_xml = z.read('ppt/slideMasters/slideMaster1.xml').decode('utf-8')
    m_root = ET.fromstring(master_xml)
    m_bg = m_root.find('.//p:bg', ns)
    if m_bg is not None:
        print("SlideMaster bg:", ET.tostring(m_bg).decode('utf-8'))
    else:
        print("SlideMaster has no explicit p:bg.")

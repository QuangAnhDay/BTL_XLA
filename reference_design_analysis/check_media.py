import zipfile

pptx_path = r"F:\OneDrive\hoc hanh\XLA\slide\Panorama_Stitching_14_Slides.pptx"

with zipfile.ZipFile(pptx_path, 'r') as z:
    for name in z.namelist():
        if 'media' in name:
            info = z.getinfo(name)
            print(f"Media file: {name} (size: {info.file_size} bytes)")

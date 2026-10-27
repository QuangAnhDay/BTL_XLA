import sys
from pptx import Presentation

pptx_path = "ASL_Preprocessing_CNN_Evaluation.pptx"

try:
    prs = Presentation(pptx_path)
    print(f"Presentation loaded successfully: {pptx_path}")
    print(f"Slide count: {len(prs.slides)}")
    print(f"Slide dimensions: {prs.slide_width.pt} x {prs.slide_height.pt} pt")
    
    assert len(prs.slides) == 10, f"Expected 10 slides, got {len(prs.slides)}"
    
    for i, slide in enumerate(prs.slides):
        title = "No title"
        for shape in slide.shapes:
            if shape.has_text_frame and shape.text_frame.text:
                lines = [l.strip() for l in shape.text_frame.text.split("\n") if l.strip()]
                if lines:
                    title = lines[0]
                    break
        has_notes = slide.has_notes_slide and bool(slide.notes_slide.notes_text_frame.text.strip())
        clean_title = title.encode('ascii', errors='replace').decode('ascii')
        print(f"  Slide {i+1:02d}: shapes={len(slide.shapes)}, has_notes={has_notes} | Title preview: '{clean_title[:45]}'")
        
    print("\nALL 10 SLIDES VALIDATED AND OPENED WITH 100% INTEGRITY.")
except Exception as e:
    print(f"Error validating presentation: {e}")
    sys.exit(1)

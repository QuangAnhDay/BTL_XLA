import json

with open('reference_design_analysis/theme_and_notes.json', encoding='utf-8') as f:
    data = json.load(f)

with open('reference_design_analysis/extracted_speaker_notes.md', 'w', encoding='utf-8') as f:
    f.write("# Extracted Speaker Notes from Reference Deck\n\n")
    # sort by slide number
    for k in sorted(data['notes'].keys(), key=lambda x: int(x)):
        f.write(f"## Slide {k}\n\n")
        f.write(f"```\n{data['notes'][k]}\n```\n\n")

print("Speaker notes extracted successfully.")

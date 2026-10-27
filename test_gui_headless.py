import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, r"F:\OneDrive\hoc hanh\XLA\BTL_TTNT\asl-sign-language")
import gui_app
import tkinter as tk

root = tk.Tk()
root.withdraw()
app = gui_app.ASLEnterpriseApp(root)
print("ASLEnterpriseApp initialized successfully!")
print(f"Test samples scanned: {len(app.test_samples)}")
print(f"Current image: {app.current_image_path}")

if app.inference_results:
    print("Initial inference ran successfully!")
    print(f"Base result: {app.inference_results['base']['label']} ({app.inference_results['base']['conf']*100:.1f}%)")
    print(f"Contrast result: {app.inference_results['contrast']['label']} ({app.inference_results['contrast']['conf']*100:.1f}%)")
    print(f"HistEq result: {app.inference_results['histeq']['label']} ({app.inference_results['histeq']['conf']*100:.1f}%)")

# Test rank tree children count
rank_items = app.rank_tree.get_children()
print(f"Rank table items populated: {len(rank_items)} rows (Top 1 -> Top 8)")
assert len(rank_items) == 8, f"Expected 8 rows in rank table, got {len(rank_items)}"

# Test switching to all pages
for p in ['dashboard', 'theory', 'inference']:
    app._switch_page(p)
    print(f"Page switched to: {p} successfully!")

root.destroy()
print("All enterprise GUI features verified with 0 errors!")

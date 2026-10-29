import os
import sys
import glob
import json
import numpy as np

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "asl-sign-language"))
from preprocessing import imread_unicode
from experiment_runner import ExperimentRunner
import tensorflow as tf

model_path = os.path.join(BASE_DIR, "asl-sign-language", "models", "asl_classifier.keras")
classes = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + ['del', 'nothing', 'space']
model = tf.keras.models.load_model(model_path)
runner = ExperimentRunner(model, classes)

test_dir = os.path.join(BASE_DIR, "test_data")
files = sorted(glob.glob(os.path.join(test_dir, "*.png")))

expected_labels = [chr(ord('A') + i) for i in range(25)]

variants = ['A', 'B', 'C', 'D', 'E']
var_names = {
    'A': 'Baseline (Ảnh gốc)',
    'B': 'Contrast Stretching',
    'C': 'Histogram Equalization',
    'D': 'Gaussian Filter',
    'E': 'Median Filter'
}

stats = {v: {'correct': 0, 'conf_sum': 0.0, 'prep_time_sum': 0.0, 'infer_time_sum': 0.0, 'errors': []} for v in variants}
per_sample_records = []

for f, gt in zip(files, expected_labels):
    img = imread_unicode(f)
    res = runner.run_all_variants(img)
    sample_entry = {
        'filename': os.path.basename(f),
        'gt': gt,
        'results': {}
    }
    for v in variants:
        pred = res[v]['pred_label']
        conf = float(res[v]['confidence'])
        prep = float(res[v]['prep_time_ms'])
        infer = float(res[v]['infer_time_ms'])
        stats[v]['conf_sum'] += conf
        stats[v]['prep_time_sum'] += prep
        stats[v]['infer_time_sum'] += infer
        if pred == gt:
            stats[v]['correct'] += 1
        else:
            stats[v]['errors'].append({
                'gt': gt,
                'pred': pred,
                'conf': conf * 100.0,
                'file': os.path.basename(f)
            })
        sample_entry['results'][v] = {
            'pred': pred,
            'conf': conf * 100.0,
            'is_correct': (pred == gt),
            'prep_ms': prep,
            'infer_ms': infer
        }
    per_sample_records.append(sample_entry)

summary = {
    'total_samples': len(files),
    'variants': {}
}

print("=" * 80)
print(f"{'Phương án':<25} | {'Độ chính xác (Accuracy)':<22} | {'Conf trung bình':<16} | {'Thời gian TL (ms)':<15}")
print("-" * 80)

for v in variants:
    acc = stats[v]['correct'] / len(files) * 100.0
    avg_conf = stats[v]['conf_sum'] / len(files) * 100.0
    avg_prep = stats[v]['prep_time_sum'] / len(files)
    avg_infer = stats[v]['infer_time_sum'] / len(files)
    summary['variants'][v] = {
        'name': var_names[v],
        'accuracy_pct': acc,
        'correct_count': stats[v]['correct'],
        'avg_conf_pct': avg_conf,
        'avg_prep_ms': avg_prep,
        'avg_infer_ms': avg_infer,
        'errors': stats[v]['errors']
    }
    print(f"{var_names[v]:<25} | {stats[v]['correct']}/25 ({acc:.1f}%)" + " " * 8 + f" | {avg_conf:.2f}%" + " " * 9 + f" | {avg_prep:.3f} ms")

print("=" * 80)

out_json = os.path.join(BASE_DIR, "benchmark_results.json")
with open(out_json, "w", encoding="utf-8") as fp:
    json.dump({'summary': summary, 'samples': per_sample_records}, fp, ensure_ascii=False, indent=2)

print(f"Chi tiết kết quả đã được lưu tại: {out_json}")

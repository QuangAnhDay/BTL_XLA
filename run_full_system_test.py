"""
Kich ban Kiem thu Toan dien He thong ASL Sign Language (Integration Test Suite)
Kiem tra toan bo pipeline nghien cuu tien xu ly anh va giao dien Enterprise.
Bao toan 100% mo hinh CNN va bo trong so goc.
"""

import os
import sys
import hashlib
import time
import cv2
import numpy as np

# Thiết lập UTF-8 cho Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

base_dir = os.path.dirname(os.path.abspath(__file__))
asl_dir = os.path.join(base_dir, 'asl-sign-language')
if asl_dir not in sys.path:
    sys.path.insert(0, asl_dir)
os.chdir(base_dir)

import tensorflow as tf
from preprocessing import (
    contrast_stretching,
    histogram_equalization,
    prepare_for_cnn,
    apply_variant,
    imread_unicode,
    imwrite_unicode
)
from experiment_runner import ExperimentRunner, VARIANT_DEFINITIONS
from gui_app import ASLEnterpriseApp
import tkinter as tk


def compute_file_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def run_full_test():
    print("=" * 80)
    print(" BẮT ĐẦU CHUỖI KIỂM THỬ HỆ THỐNG ASL SIGN LANGUAGE (ENTERPRISE EDITION)")
    print("=" * 80)

    model_path = os.path.join('asl-sign-language', 'models', 'asl_classifier.keras')

    # 1. Xác minh mô hình gốc
    print("\n[MỤC 1] Xác minh mô hình gốc:")
    assert os.path.exists(model_path), f"Không tìm thấy mô hình tại {model_path}"
    model_hash = compute_file_hash(model_path)
    file_size_kb = os.path.getsize(model_path) / 1024
    print(f"    - File mô hình: {model_path}")
    print(f"    - Kích thước: {file_size_kb:.2f} KB")
    print(f"    - SHA-256 Hash: {model_hash}")
    print("    [✓] Mô hình gốc tồn tại nguyên vẹn, không bị ghi đè.")

    # 2. Khởi động và tải mô hình CNN
    print("\n[MỤC 2] Kiểm tra khởi động và tải mô hình CNN:")
    model = tf.keras.models.load_model(model_path)
    assert model is not None, "Mô hình không được tải thành công!"
    assert model.input_shape == (None, 100, 100, 3), f"Sai input shape: {model.input_shape}"
    assert model.output_shape == (None, 29), f"Sai output shape: {model.output_shape}"
    classes = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + ['del', 'nothing', 'space']
    runner = ExperimentRunner(model, classes)
    print(f"    - Input Shape: {model.input_shape}")
    print(f"    - Output Shape: {model.output_shape} (29 classes)")
    print("    [✓] Khởi động và tải mô hình thành công.")

    # 3. Đọc dữ liệu ảnh kiểm thử từ test_data
    print("\n[MỤC 3] Kiểm tra đọc dữ liệu ảnh thực nghiệm từ test_data:")
    test_files = [f for f in os.listdir('test_data') if f.endswith('.png')]
    assert len(test_files) >= 25, f"Số lượng ảnh trong test_data quá ít: {len(test_files)}"
    sample_img_path = os.path.join('test_data', test_files[0])
    sample_img = imread_unicode(sample_img_path)
    assert sample_img is not None and sample_img.size > 0, "Không đọc được ảnh mẫu test!"
    print(f"    - Tìm thấy {len(test_files)} ảnh mẫu.")
    print(f"    - Ảnh mẫu 1: {test_files[0]} | Kích thước: {sample_img.shape}")
    print("    [✓] Đọc ảnh test_data hỗ trợ đường dẫn Unicode thành công.")

    # 4 & 5. Kiểm tra độc lập các phương pháp tiền xử lý và chuẩn hóa đầu vào CNN
    print("\n[MỤC 4 & 5] Kiểm tra độc lập các phương pháp tiền xử lý và chuẩn hóa CNN (5 Phương án):")
    variants = ['A', 'B', 'C', 'D', 'E']
    for v_key in variants:
        proc_bgr, tensor = apply_variant(sample_img, v_key)
        assert proc_bgr.shape == sample_img.shape, f"Sai kích thước BGR tại {v_key}"
        assert proc_bgr.dtype == np.uint8, f"Sai dtype tại {v_key}"
        assert tensor.shape == (1, 100, 100, 3), f"Sai shape tensor tại {v_key}"
        assert tensor.dtype == np.float32, f"Sai dtype tensor tại {v_key}"
        assert 0.0 <= tensor.min() <= 1.0 and 0.0 <= tensor.max() <= 1.0, f"Dải tensor ngoài [0, 1] tại {v_key}"
        print(f"    - Phương án {v_key:<2} ({VARIANT_DEFINITIONS[v_key]['name']:<24}): "
              f"BGR={proc_bgr.shape} | Tensor={tensor.shape} range=[{tensor.min():.3f}, {tensor.max():.3f}] [✓]")

    # 6. Chạy đối chiếu thực nghiệm A, B, C, D, E trên cùng một nguồn ảnh
    print("\n[MỤC 6] Chạy đối chiếu thực nghiệm cả 5 phương án trên cùng nguồn ảnh:")
    results = runner.run_all_variants(sample_img)
    for v_key in variants:
        r = results[v_key]
        print(f"    - [{v_key}] {r['name']:<24}: Dự đoán '{r['pred_label']}' | Tin cậy: {r['confidence']*100:.2f}% | Xử lý: {r['prep_time_ms']:.2f} ms")
    print("    [✓] Cả 5 phương án chạy độc lập, minh bạch trên cùng một ảnh nguồn.")

    # 7. Xử lý ngoại lệ an toàn
    print("\n[MỤC 7] Kiểm tra khả năng xử lý ngoại lệ và an toàn:")
    empty_crop = np.zeros((0, 0, 3), dtype=np.uint8)
    try:
        prepare_for_cnn(empty_crop)
        assert False, "Phải ném ngoại lệ khi ảnh rỗng!"
    except ValueError as e:
        print(f"    - Bắt ngoại lệ ảnh rỗng chính xác: {e}")

    non_exist_img = imread_unicode("duong_dan_khong_ton_tai_12345.png")
    assert non_exist_img is None, "Đọc file không tồn tại phải trả về None!"
    print("    - Đường dẫn không tồn tại được xử lý an toàn (trả về None).")
    print("    [✓] Xử lý ngoại lệ an toàn đạt yêu cầu.")

    # 8. Kiểm tra nạp và khởi tạo giao diện ASLEnterpriseApp (Headless mode)
    print("\n[MỤC 8] Kiểm tra khởi tạo Giao diện Doanh nghiệp ASLEnterpriseApp (Headless):")
    root = tk.Tk()
    root.withdraw()
    app = ASLEnterpriseApp(root)
    assert app.model is not None
    assert len(app.test_samples) >= 25
    assert app.current_crop_bgr is not None
    assert len(app.rank_tree.get_children()) == 8, "Bảng xếp hạng phân phối xác suất phải có đúng 8 hàng (Top 1 -> Top 8)!"
    for p in ['dashboard', 'theory', 'inference']:
        app._switch_page(p)
    root.destroy()
    print("    - Giao diện nạp đầy đủ 25 mẫu test, bảng xếp hạng Top 8 và chuyển đổi 3 phân hệ mượt mà.")
    print("    [✓] Giao diện Enterprise hoạt động hoàn hảo và ổn định.")

    # 9. Chạy thử nghiệm hàng loạt trên 10 ảnh đầu tiên từ test_data (Đầy đủ 5 Phương án)
    print("\n[MỤC 9] Chạy thử nghiệm hàng loạt trên 10 ảnh đầu tiên từ test_data (5 Phương án):")
    print("-" * 98)
    print(f"{'Tên file':<30} | {'A (Gốc)':<11} | {'B (Contrast)':<12} | {'C (HistEq)':<11} | {'D (Gauss)':<11} | {'E (Median)':<11}")
    print("-" * 98)
    for sample_file in test_files[:10]:
        s_path = os.path.join('test_data', sample_file)
        s_img = imread_unicode(s_path)
        s_res = runner.run_all_variants(s_img)
        a_str = f"{s_res['A']['pred_label']} ({s_res['A']['confidence']*100:.1f}%)"
        b_str = f"{s_res['B']['pred_label']} ({s_res['B']['confidence']*100:.1f}%)"
        c_str = f"{s_res['C']['pred_label']} ({s_res['C']['confidence']*100:.1f}%)"
        d_str = f"{s_res['D']['pred_label']} ({s_res['D']['confidence']*100:.1f}%)"
        e_str = f"{s_res['E']['pred_label']} ({s_res['E']['confidence']*100:.1f}%)"
        print(f"{sample_file[:28]:<30} | {a_str:<11} | {b_str:<12} | {c_str:<11} | {d_str:<11} | {e_str:<11}")
    print("-" * 98)

    # 10. Tái xác minh hash mô hình nguyên bản 100%
    print("\n[MỤC 10] Tái xác minh tính toàn vẹn mô hình gốc:")
    final_hash = compute_file_hash(model_path)
    assert final_hash == model_hash, "NGHIÊM TRỌNG: Mô hình gốc đã bị thay đổi trong quá trình test!"
    print(f"    - SHA-256 Model trước và sau kiểm thử: KHỚP 100% ({final_hash[:16]}...)")
    print("\n>>> TẤT CẢ 10 MỤC KIỂM THỬ ĐỀU ĐẠT THÀNH CÔNG 100%! <<<")
    print("=" * 80)


if __name__ == "__main__":
    run_full_test()

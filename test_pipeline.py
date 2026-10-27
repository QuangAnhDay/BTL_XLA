import os
import sys
import time
import cv2
import numpy as np

# Thiết lập encoding utf-8 cho Windows console
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

sys.path.append(os.path.abspath('asl-sign-language'))

import tensorflow as tf
from preprocessing import (
    contrast_stretching,
    histogram_equalization,
    gaussian_filter,
    median_filter,
    prepare_for_cnn,
    apply_variant
)
from experiment_runner import ExperimentRunner

def test_preprocessing_pipeline():
    print("=" * 60)
    print("KIỂM THỬ MODULE TIỀN XỬ LÝ VÀ SUY LUẬN TRÊN ẢNH THẬT")
    print("=" * 60)

    # 1. Tải mô hình
    model_path = os.path.join('asl-sign-language', 'models', 'asl_classifier.keras')
    print(f"[1] Tải mô hình từ: {model_path}")
    assert os.path.exists(model_path), "File mô hình không tồn tại!"
    model = tf.keras.models.load_model(model_path)
    print(f"    - Input shape: {model.input_shape}")
    print(f"    - Output shape: {model.output_shape}")

    classes = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + ['del', 'nothing', 'space']
    assert len(classes) == 29, "Số lượng nhãn phải đúng 29!"

    # 2. Đọc ảnh thử nghiệm từ test_data
    test_files = [f for f in os.listdir('test_data') if f.endswith('.png')]
    test_img_path = os.path.join('test_data', test_files[0])
    img = cv2.imread(test_img_path)
    print(f"\n[2] Đọc ảnh kiểm thử: {test_files[0]} | Kích thước gốc: {img.shape}")

    # 3. Kiểm tra từng hàm tiền xử lý độc lập
    print("\n[3] Kiểm thử độc lập từng phương pháp:")
    # Contrast stretching
    cs_img = contrast_stretching(img)
    assert cs_img.shape == img.shape and cs_img.dtype == np.uint8
    print("    [✓] Contrast Stretching thành công.")

    # Histogram equalization
    he_img = histogram_equalization(img)
    assert he_img.shape == img.shape and he_img.dtype == np.uint8
    print("    [✓] Histogram Equalization thành công.")

    # Gaussian filter
    gf_img = gaussian_filter(img, ksize=5, sigma=1.0)
    assert gf_img.shape == img.shape and gf_img.dtype == np.uint8
    print("    [✓] Gaussian Filter thành công.")

    # Median filter
    mf_img = median_filter(img, ksize=5)
    assert mf_img.shape == img.shape and mf_img.dtype == np.uint8
    print("    [✓] Median Filter thành công.")

    # 4. Kiểm tra chuẩn hóa cho CNN (Tensor shape, dtype, value range)
    print("\n[4] Kiểm thử định dạng đầu vào cho CNN (prepare_for_cnn):")
    tensor = prepare_for_cnn(img)
    assert tensor.shape == (1, 100, 100, 3), f"Sai shape: {tensor.shape}"
    assert tensor.dtype == np.float32, f"Sai dtype: {tensor.dtype}"
    assert tensor.min() >= 0.0 and tensor.max() <= 1.0, f"Giá trị ngoài [0, 1]: min={tensor.min()}, max={tensor.max()}"
    print(f"    [✓] Tensor shape: {tensor.shape}")
    print(f"    [✓] Tensor dtype: {tensor.dtype}")
    print(f"    [✓] Tensor range: [{tensor.min():.4f}, {tensor.max():.4f}]")

    # 5. Chạy thử nghiệm trọn vẹn 5 phương án A-E với ExperimentRunner
    print("\n[5] Chạy thực nghiệm so sánh A - E qua cùng mô hình CNN:")
    runner = ExperimentRunner(model, classes)
    results = runner.run_all_variants(img)

    print("-" * 75)
    print(f"{'Phương án':<10} | {'Tên phương pháp':<24} | {'Dự đoán':<8} | {'Độ tin cậy':<10} | {'Thời gian':<10}")
    print("-" * 75)
    for k in ['A', 'B', 'C', 'D', 'E']:
        res = results[k]
        name = res['name']
        lbl = res['pred_label']
        conf = res['confidence'] * 100.0
        t_tot = res['total_time_ms']
        print(f"Phương án {k:<2} | {name:<24} | Chữ {lbl:<4} | {conf:>6.2f}%    | {t_tot:>6.2f} ms")
    print("-" * 75)
    print("\n[✓] Tất cả các bài kiểm tra tiền xử lý và suy luận đều ĐẠT!")

if __name__ == "__main__":
    test_preprocessing_pipeline()

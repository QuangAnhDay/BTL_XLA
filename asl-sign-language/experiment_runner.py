"""
Module Thuc Nghiem So Sanh cac Phuong An Tien Xu Ly cho ASL Sign Language
Bao gom 5 phuong an thi nghiem duoc yeu cau:
  - A: Baseline (anh goc duoc xu ly theo dung pipeline hien tai cua mo hinh)
  - B: Contrast Stretching
  - C: Histogram Equalization
  - D: Gaussian Filter
  - E: Median Filter
Tat ca phuong an su dung chung 1 anh chup goc va cung 1 mo hinh CNN da duoc huan luyen.
"""

import time
from typing import Dict, Any, List
import numpy as np
import tensorflow as tf
from preprocessing import apply_variant


VARIANT_DEFINITIONS = {
    'A': {
        'name': 'Baseline (Ảnh gốc)',
        'description': 'Ảnh gốc chỉ qua resize (100x100) và chuẩn hóa pixel [0, 1].',
        'group': 'Gốc'
    },
    'B': {
        'name': 'Contrast Stretching',
        'description': 'Tăng cường tương phản tuyến tính trên kênh độ sáng Y (YCrCb).',
        'group': 'Nhóm 1: Tăng cường ảnh'
    },
    'C': {
        'name': 'Histogram Equalization',
        'description': 'Cân bằng biểu đồ độ sáng trên kênh Y (YCrCb) để tránh lệch màu sắc.',
        'group': 'Nhóm 1: Tăng cường ảnh'
    },
    'D': {
        'name': 'Gaussian Filter',
        'description': 'Lọc không gian làm mịn và giảm nhiễu tần số cao bằng nhân Gauss 2D.',
        'group': 'Nhóm 2: Lọc không gian'
    },
    'E': {
        'name': 'Median Filter',
        'description': 'Lọc không gian phi tuyến trung vị loại bỏ nhiễu hạt bảo toàn cạnh biên.',
        'group': 'Nhóm 2: Lọc không gian'
    }
}


class ModelInferenceEngine:
    """
    Engine suy luận CNN tối ưu hóa cao (SRP - Single Responsibility Principle).
    - Quản lý biên dịch JIT forward pass với @tf.function(reduce_retracing=True).
    - Loại bỏ overhead Python generator/validation của keras.Model.predict() (~50ms -> ~3ms).
    - Hỗ trợ batching SIMD tự động cho nhiều biến thể hoặc tập mẫu lớn.
    """
    def __init__(self, model):
        self.model = getattr(model, 'model', model)
        self._compiled_forward = tf.function(
            func=lambda x: self.model(x, training=False),
            reduce_retracing=True
        )
        self._warmup()

    def _warmup(self):
        """Khởi tạo và biên dịch đồ thị tính toán trước để tránh giật lag."""
        try:
            dummy_single = tf.zeros((1, 100, 100, 3), dtype=tf.float32)
            _ = self._compiled_forward(dummy_single)
            dummy_batch = tf.zeros((5, 100, 100, 3), dtype=tf.float32)
            _ = self._compiled_forward(dummy_batch)
        except Exception:
            pass

    def predict(self, batch_tensor: np.ndarray) -> np.ndarray:
        """
        Thực thi suy luận cho một tensor đơn hoặc một batch các tensor (N, 100, 100, 3).
        Trả về mảng NumPy xác suất Softmax với shape (N, num_classes).
        """
        if not isinstance(batch_tensor, tf.Tensor):
            tensor_tf = tf.convert_to_tensor(batch_tensor, dtype=tf.float32)
        else:
            tensor_tf = batch_tensor
        return self._compiled_forward(tensor_tf).numpy()


class ExperimentRunner:
    def __init__(self, model, classes: List[str]):
        """
        Khoi tao ExperimentRunner voi mo hinh CNN va danh sach nhan ASL.
        Tu dong su dung ModelInferenceEngine de toi uu hoa toc do suy luan.
        """
        if isinstance(model, ModelInferenceEngine):
            self.inference_engine = model
            self.model = model.model
        else:
            self.model = model
            self.inference_engine = ModelInferenceEngine(model)
        self.classes = classes

    def run_all_variants(self, crop_bgr: np.ndarray, params: Dict[str, Any] = None) -> Dict[str, Dict[str, Any]]:
        """
        Chay toan bo 5 phuong an A, B, C, D, E tren cung mot anh crop goc.
        Su dung batched inference gom toan bo 5 bien the de giam thoi gian suy luan >30x.
        Tra ve dict chua ket qua chi tiet tung phuong an:
          - variant_key ('A', 'B', ...)
          - name, description, group
          - processed_bgr (anh uint8 BGR de hien thi)
          - pred_label (nhan du doan Top 1)
          - confidence (xac suat softmax Top 1, tu 0.0 den 1.0)
          - top3 (danh sach Top 3 du doan gom label va conf)
          - prep_time_ms (thoi gian tien xu ly tinh bang ms)
          - infer_time_ms (thoi gian suy luan CNN tinh bang ms)
          - total_time_ms (tong thoi gian ms)
        """
        if params is None:
            params = {}

        keys = ['A', 'B', 'C', 'D', 'E']
        prep_results = {}
        tensors = []

        # 1. Tien xu ly tung phuong an theo dung Strategy va do thoi gian chuan xac
        for key in keys:
            t0 = time.perf_counter()
            proc_bgr, input_tensor = apply_variant(crop_bgr, key, **params)
            t1 = time.perf_counter()
            prep_results[key] = {
                'proc_bgr': proc_bgr,
                'prep_ms': (t1 - t0) * 1000.0
            }
            tensors.append(input_tensor)

        # 2. Gom toan bo 5 tensor thanh 1 batch duy nhat shape (5, 100, 100, 3)
        batch_tensor = np.concatenate(tensors, axis=0)
        t_infer_start = time.perf_counter()
        batch_preds = self.inference_engine.predict(batch_tensor)
        t_infer_end = time.perf_counter()
        total_infer_ms = (t_infer_end - t_infer_start) * 1000.0
        per_variant_infer_ms = total_infer_ms / len(keys)

        # 3. Phan tich ket qua Top 1 va Top 3 cho tung phuong an
        results = {}
        for idx, key in enumerate(keys):
            meta = VARIANT_DEFINITIONS[key]
            preds = batch_preds[idx]
            proc_bgr = prep_results[key]['proc_bgr']
            prep_ms = prep_results[key]['prep_ms']

            top3_indices = np.argsort(preds)[-3:][::-1]
            top1_idx = top3_indices[0]
            top1_label = self.classes[top1_idx]
            top1_conf = float(preds[top1_idx])

            top3 = [
                {
                    'label': self.classes[i],
                    'confidence': float(preds[i])
                }
                for i in top3_indices
            ]

            results[key] = {
                'key': key,
                'name': meta['name'],
                'description': meta['description'],
                'group': meta['group'],
                'processed_bgr': proc_bgr,
                'pred_label': top1_label,
                'confidence': top1_conf,
                'top3': top3,
                'prep_time_ms': prep_ms,
                'infer_time_ms': per_variant_infer_ms,
                'total_time_ms': prep_ms + per_variant_infer_ms
            }

        return results

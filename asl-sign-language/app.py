import os
import sys
import warnings

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
warnings.filterwarnings('ignore')

_stderr_fd = sys.stderr.fileno()
with open(os.devnull, 'w') as _devnull:
    _old_stderr = os.dup(_stderr_fd)
    os.dup2(_devnull.fileno(), _stderr_fd)
    try:
        import tensorflow as tf
        tf.get_logger().setLevel('ERROR')
    finally:
        os.dup2(_old_stderr, _stderr_fd)
        os.close(_old_stderr)

import cv2
import numpy as np


class ASLRealtimeDetector:
    def __init__(self, model_filename="asl_classifier.keras"):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_path = os.path.join(self.base_dir, "models", model_filename)
        self.classes = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + ['del', 'nothing', 'space']
        self.model = self._load_model()

    def _load_model(self):
        if not os.path.exists(self.model_path):
            print(f"[X] Không tìm thấy mô hình tại: {self.model_path}")
            sys.exit(1)
        try:
            model = tf.keras.models.load_model(self.model_path)
            print(f"[✓] Tải thành công mô hình ASL từ: {self.model_path}")
            return model
        except Exception as err:
            print(f"[X] Lỗi tải mô hình: {err}")
            sys.exit(1)

    def preprocess_crop(self, crop_img):
        img = cv2.resize(crop_img, (100, 100))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.astype(np.float32) / 255.0
        return np.expand_dims(img, axis=0)

    def run(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("[X] Không thể kết nối với Webcam!")
            return

        print("[!] Đang chạy demo Webcam. Đưa bàn tay vào khung hình chữ nhật.")
        print("[!] Nhấn 'q' để thoát ứng dụng.")

        box_size = 250

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            h, w, _ = frame.shape
            x_min = int((w - box_size) / 2)
            y_min = int((h - box_size) / 2)
            x_max = x_min + box_size
            y_max = y_min + box_size

            cv2.rectangle(frame, (x_min - 2, y_min - 2), (x_max + 2, y_max + 2), (0, 255, 0), 2)
            cv2.putText(frame, "Dat tay vao khung nay", (x_min, y_min - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1, cv2.LINE_AA)

            hand_crop = frame[y_min:y_max, x_min:x_max]
            label_text = "Analyzing..."

            if hand_crop.size > 0:
                input_tensor = self.preprocess_crop(hand_crop)
                preds = self.model.predict(input_tensor, verbose=0)
                pred_idx = np.argmax(preds)
                confidence = preds[0][pred_idx]

                if confidence > 0.50:
                    label_text = f"Prediction: {self.classes[pred_idx]} ({confidence * 100:.1f}%)"
                else:
                    label_text = "Uncertain"

            cv2.putText(frame, label_text, (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)

            cv2.imshow("ASL Recognition System", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    detector = ASLRealtimeDetector()
    detector.run()
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

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np


class ASLClassifierGUI:
    def __init__(self, root, model_filename="asl_classifier.keras"):
        self.root = root
        self.root.title("ASL Sign Language Classifier")
        self.root.geometry("600x760")
        self.root.configure(bg="#F3F4F6")

        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_path = os.path.join(self.base_dir, "models", model_filename)
        self.classes = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + ['del', 'nothing', 'space']
        self.model = self._load_model()

        self._build_ui()

    def _load_model(self):
        if not os.path.exists(self.model_path):
            print(f"[X] Không tìm thấy file model tại: {self.model_path}")
            sys.exit(1)
        try:
            model = tf.keras.models.load_model(self.model_path)
            print(f"[✓] Tải thành công mô hình ASL từ: {self.model_path}")
            return model
        except Exception as err:
            print(f"[X] Lỗi tải mô hình: {err}")
            sys.exit(1)

    def _build_ui(self):
        title_label = tk.Label(
            self.root,
            text="NHẬN DIỆN NGÔN NGỮ KÝ HIỆU ASL",
            font=("Helvetica", 16, "bold"),
            fg="#111827",
            bg="#F3F4F6"
        )
        title_label.pack(pady=20)

        self.image_frame = tk.Frame(
            self.root,
            width=350,
            height=350,
            bg="#E5E7EB",
            relief="solid",
            bd=1
        )
        self.image_frame.pack_propagate(0)
        self.image_frame.pack(pady=10)

        self.image_label = tk.Label(
            self.image_frame,
            text="Chưa có ảnh được chọn",
            font=("Helvetica", 12),
            bg="#E5E7EB",
            fg="#6B7280"
        )
        self.image_label.pack(expand=True, fill="both")

        self.result_frame = tk.LabelFrame(
            self.root,
            text=" KẾT QUẢ DỰ ĐOÁN (TOP 3) ",
            font=("Helvetica", 10, "bold"),
            fg="#374151",
            bg="#F3F4F6",
            padx=20,
            pady=10
        )
        self.result_frame.pack(pady=15, fill="x", padx=60)

        self.top1_label = tk.Label(
            self.result_frame,
            text="Top 1: ---",
            font=("Helvetica", 14, "bold"),
            fg="#DC2626",
            bg="#F3F4F6"
        )
        self.top1_label.pack(anchor="w", pady=2)

        self.top2_label = tk.Label(
            self.result_frame,
            text="Top 2: ---",
            font=("Helvetica", 12, "bold"),
            fg="#2563EB",
            bg="#F3F4F6"
        )
        self.top2_label.pack(anchor="w", pady=2)

        self.top3_label = tk.Label(
            self.result_frame,
            text="Top 3: ---",
            font=("Helvetica", 12, "bold"),
            fg="#4B5563",
            bg="#F3F4F6"
        )
        self.top3_label.pack(anchor="w", pady=2)

        btn_select = tk.Button(
            self.root,
            text="📁 Chọn Ảnh Từ Máy Tính",
            font=("Helvetica", 12, "bold"),
            fg="white",
            bg="#10B981",
            activeforeground="white",
            activebackground="#059669",
            padx=25,
            pady=12,
            bd=0,
            cursor="hand2",
            command=self.upload_image
        )
        btn_select.pack(pady=15)

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
        )

        if not file_path:
            return

        img_pil = Image.open(file_path)
        img_display = img_pil.resize((350, 350))
        img_tk = ImageTk.PhotoImage(img_display)

        self.image_label.configure(image=img_tk, text="")
        self.image_label.image = img_tk

        img_model = img_pil.convert("RGB").resize((100, 100))
        img_array = np.array(img_model, dtype=np.float32) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        predictions = self.model.predict(img_array, verbose=0)[0]
        top_3_indices = np.argsort(predictions)[-3:][::-1]

        p1_class = self.classes[top_3_indices[0]]
        p1_conf = predictions[top_3_indices[0]] * 100

        p2_class = self.classes[top_3_indices[1]]
        p2_conf = predictions[top_3_indices[1]] * 100

        p3_class = self.classes[top_3_indices[2]]
        p3_conf = predictions[top_3_indices[2]] * 100

        self.top1_label.config(text=f"Top 1: Chữ {p1_class} ({p1_conf:.1f}%)")
        self.top2_label.config(text=f"Top 2: Chữ {p2_class} ({p2_conf:.1f}%)")
        self.top3_label.config(text=f"Top 3: Chữ {p3_class} ({p3_conf:.1f}%)")


if __name__ == "__main__":
    root = tk.Tk()
    app = ASLClassifierGUI(root)
    root.mainloop()

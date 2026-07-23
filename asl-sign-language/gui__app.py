import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import tensorflow as tf

# 1. Tự động lấy đường dẫn tuyệt đối của file model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'models', 'asl_classifier.keras')

# Load mô hình đã huấn luyện
try:
    model = tf.keras.models.load_model(model_path)
    print(f"Đã tải mô hình thành công từ: {model_path}")
except Exception as e:
    print("Lỗi load model:", e)
    exit()

# Định nghĩa 29 nhãn chữ cái
CLASSES = [chr(i) for i in range(ord('A'), ord('Z')+1)] + ['del', 'nothing', 'space']

# 2. Xây dựng giao diện ứng dụng (GUI)
class ASLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ASL Sign Language Classifier")
        self.root.geometry("600x760") # Tăng kích thước cửa sổ để chứa ảnh to hơn
        self.root.configure(bg="#F3F4F6")

        # Tiêu đề ứng dụng
        title_label = tk.Label(root, text="NHẬN DIỆN NGÔN NGỮ KÝ HIỆU ASL", font=("Helvetica", 16, "bold"), fg="#111827", bg="#F3F4F6")
        title_label.pack(pady=20)

        # KHUNG CONTAINER CỐ ĐỊNH KÍCH THƯỚC 350x350 CHO ẢNH (Chống bị bóp nhỏ)
        self.image_frame = tk.Frame(root, width=350, height=350, bg="#E5E7EB", relief="solid", bd=1)
        self.image_frame.pack_propagate(0) # Khóa kích thước frame, không cho co nhỏ theo widget con
        self.image_frame.pack(pady=10)

        # Nhãn hiển thị ảnh (nằm bên trong khung 350x350 ở trên)
        self.image_label = tk.Label(self.image_frame, text="Chưa có ảnh được chọn", font=("Helvetica", 12), bg="#E5E7EB", fg="#6B7280")
        self.image_label.pack(expand=True, fill="both")

        # Khung hiển thị kết quả dự đoán (Dạng danh sách giảm dần)
        self.result_frame = tk.LabelFrame(root, text=" KẾT QUẢ DỰ ĐOÁN (TOP 3) ", font=("Helvetica", 10, "bold"), fg="#374151", bg="#F3F4F6", padx=20, pady=10)
        self.result_frame.pack(pady=15, fill="x", padx=60)

        # Top 1 (Cao nhất - màu đỏ nổi bật)
        self.top1_label = tk.Label(self.result_frame, text="Top 1: ---", font=("Helvetica", 14, "bold"), fg="#DC2626", bg="#F3F4F6")
        self.top1_label.pack(anchor="w", pady=2)

        # Top 2 (màu xanh dương)
        self.top2_label = tk.Label(self.result_frame, text="Top 2: ---", font=("Helvetica", 12, "bold"), fg="#2563EB", bg="#F3F4F6")
        self.top2_label.pack(anchor="w", pady=2)

        # Top 3 (màu xám)
        self.top3_label = tk.Label(self.result_frame, text="Top 3: ---", font=("Helvetica", 12, "bold"), fg="#4B5563", bg="#F3F4F6")
        self.top3_label.pack(anchor="w", pady=2)

        # Nút bấm chọn ảnh
        btn_select = tk.Button(root, text="📁 Chọn Ảnh Từ Máy Tính", font=("Helvetica", 12, "bold"), fg="white", bg="#10B981", 
                               activeforeground="white", activebackground="#059669", padx=25, pady=12, bd=0, cursor="hand2", command=self.upload_image)
        btn_select.pack(pady=15)

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
        )
        
        if file_path:
            # 1. Đọc và hiển thị ảnh to rõ nét (350x350)
            img_pil = Image.open(file_path)
            img_display = img_pil.resize((350, 350)) # Tăng kích thước từ 250 lên 350
            img_tk = ImageTk.PhotoImage(img_display)
            
            self.image_label.configure(image=img_tk, text="")
            self.image_label.image = img_tk # Giữ tham chiếu

            # 2. Tiền xử lý ảnh cho AI (Vẫn resize về 100x100 để đúng chuẩn đầu vào của CNN)
            img_model = img_pil.convert("RGB")
            img_model = img_model.resize((100, 100))
            img_array = np.array(img_model) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            # 3. Dự đoán
            predictions = model.predict(img_array, verbose=0)[0]
            
            # Lấy vị trí của Top 3 giá trị cao nhất
            top_3_indices = np.argsort(predictions)[-3:][::-1]
            
            p1_class = CLASSES[top_3_indices[0]]
            p1_conf = predictions[top_3_indices[0]] * 100
            
            p2_class = CLASSES[top_3_indices[1]]
            p2_conf = predictions[top_3_indices[1]] * 100
            
            p3_class = CLASSES[top_3_indices[2]]
            p3_conf = predictions[top_3_indices[2]] * 100

            # Cập nhật kết quả dạng danh sách
            self.top1_label.config(text=f"Top 1: Chữ {p1_class} ({p1_conf:.1f}%)")
            self.top2_label.config(text=f"Top 2: Chữ {p2_class} ({p2_conf:.1f}%)")
            self.top3_label.config(text=f"Top 3: Chữ {p3_class} ({p3_conf:.1f}%)")

# Khởi chạy ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    app = ASLApp(root)
    root.mainloop()
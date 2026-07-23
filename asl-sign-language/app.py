import cv2
import numpy as np
import tensorflow as tf
import os

# 1. Tự động lấy đường dẫn tuyệt đối của file model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'models', 'asl_classifier.keras')

# Load mô hình đã huấn luyện
try:
    model = tf.keras.models.load_model(model_path)
    print(f"Đã tải mô hình thành công tại: {model_path}")
except Exception as e:
    print("Lỗi load model:", e)
    print(f"Không tìm thấy file model. Vui lòng đảm bảo file tồn tại ở: {model_path}")
    exit()

# Định nghĩa danh sách 29 nhãn chữ cái
CLASSES = [chr(i) for i in range(ord('A'), ord('Z')+1)] + ['del', 'nothing', 'space']

# 2. Khởi tạo Webcam
cap = cv2.VideoCapture(0)

print("Ứng dụng đang chạy. Đưa tay vào khung hình chữ nhật màu xanh trên màn hình. Nhấn phím 'q' để thoát.")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break
        
##    frame = cv2.flip(frame, 1) # Lật ảnh đối xứng như gương
    h, w, c = frame.shape
    
    # Định nghĩa tọa độ hộp tĩnh ở giữa màn hình (kích thước 250x250 pixel)
    box_size = 250
    x_min = int((w - box_size) / 2)
    y_min = int((h - box_size) / 2)
    x_max = x_min + box_size
    y_max = y_min + box_size
    
    # Vẽ khung chữ nhật hướng dẫn màu xanh lá cây
    cv2.rectangle(frame, (x_min - 2, y_min - 2), (x_max + 2, y_max + 2), (0, 255, 0), 2)
    cv2.putText(frame, "Dat tay vao khung nay", (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1, cv2.LINE_AA)
    
    # Cắt ảnh bàn tay bên trong khung tĩnh
    hand_crop = frame[y_min:y_max, x_min:x_max]
    
    label_text = "No prediction"
    
    if hand_crop.size > 0:
        # Tiền xử lý ảnh giống hệt lúc Train mô hình
        img = cv2.resize(hand_crop, (100, 100)) # Co về 100x100
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Chuyển sang RGB
        img = img / 255.0 # Chuẩn hóa pixel về [0, 1]
        img = np.expand_dims(img, axis=0) # Tăng chiều lên (1, 100, 100, 3)
        
        # Dự đoán bằng mô hình CNN
        predictions = model.predict(img, verbose=0)
        pred_class_idx = np.argmax(predictions)
        confidence = predictions[0][pred_class_idx]
        
        # Ngưỡng tin cậy hiển thị kết quả (lớn hơn 50%)
        if confidence > 0.50:
            label_text = f"Prediction: {CLASSES[pred_class_idx]} ({confidence*100:.1f}%)"
        else:
            label_text = "Uncertain"
            
    # Hiển thị kết quả dự đoán góc trên màn hình
    cv2.putText(frame, label_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
    
    # Hiển thị cửa sổ demo
    cv2.imshow("Sign Language Recognition (Static Box)", frame)
    
    # Nhấn q để thoát
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
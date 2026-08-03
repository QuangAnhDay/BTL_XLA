# Nhận diện Ngôn ngữ Ký hiệu ASL

Ứng dụng sử dụng mô hình CNN để nhận diện 29 lớp ký hiệu tay ASL (A-Z, del, nothing, space) qua Webcam và giao diện GUI.

## Cấu trúc thư mục

```
asl-sign-language/
├── models/
│   └── asl_classifier.keras
├── notebooks/
│   └── Bao_cao_TTNT.ipynb
├── docs/
├── app.py
├── gui_app.py
├── requirements.txt
└── README.md
```

## Cài đặt

```bash
pip install -r requirements.txt
```

## Chạy ứng dụng

Nhận diện qua Webcam:
```bash
python app.py
```

Nhận diện qua giao diện GUI (chọn ảnh từ máy):
```bash
python gui_app.py
```

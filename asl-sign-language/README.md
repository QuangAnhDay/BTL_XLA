# HỆ THỐNG NGHIÊN CỨU & ĐÁNH GIÁ TIỀN XỬ LÝ ẢNH ASL (ENTERPRISE SUITE)

> **Đồ án môn học: Xử lý ảnh (Digital Image Processing)**  
> **Kế thừa từ:** Bài tập lớn môn Nhập môn Trí tuệ Nhân tạo  
> **Nguyên tắc cốt lõi:** Bảo toàn 100% mô hình CNN gốc và bộ trọng số đã huấn luyện (`models/asl_classifier.keras`). Không huấn luyện lại, không thay đổi cấu trúc mạng, giữ nguyên điều kiện suy luận để so sánh khách quan.

---

## 1. TỔNG QUAN VÀ MỤC TIÊU NGHIÊN CỨU

Hệ thống được phát triển dưới dạng **Bộ công cụ Doanh nghiệp (Enterprise Research Suite)** với giao diện chuẩn Tone sáng (Light Theme) và thanh điều hướng Taskbar bên trái. Mục tiêu là nghiên cứu định lượng ảnh hưởng của các kỹ thuật tiền xử lý ảnh kinh điển đến hiệu năng phân loại của mạng nơ-ron tích chập (CNN) trên tập 29 ký hiệu bàn tay ASL (American Sign Language):

* **Phương án A — Baseline (Ảnh gốc):** Ảnh chuẩn hóa cơ bản `[0, 1]` tương thích với phân phối huấn luyện ban đầu của CNN.
* **Phương án B — Contrast Stretching (Dãn tương phản phân vị):** Mở rộng dải động mức xám tuyến tính (1% - 99%) trên kênh độ sáng $Y$ trong không gian màu $YCrCb$.
* **Phương án C — Histogram Equalization (Cân bằng biểu đồ độ sáng):** Tuyến tính hóa hàm phân bố tích lũy (CDF) trên kênh $Y$ để tối đa hóa độ tương phản toàn cục.

---

## 2. KIẾN TRÚC GIAO DIỆN & PHÂN HỆ CHỨC NĂNG

Ứng dụng được thiết kế theo cấu trúc ứng dụng phần mềm doanh nghiệp:

1. **🔍 Phân hệ Nhận diện & Tiền xử lý (Inference Engine):**
   * Cho phép chọn ảnh bất kỳ từ máy tính hoặc chọn nhanh từ danh mục 25 mẫu test có sẵn ($A \rightarrow Y$).
   * Tự động chạy song song 3 nhánh xử lý: Ảnh Gốc, Dãn Tương Phản, Cân Bằng Histogram.
   * **Hero Card (Best Prediction):** Tự động đánh giá và hiển thị kết quả dự đoán tối ưu nhất kèm độ tin cậy Softmax (%) và Top-3 phân lớp.
   * Hiển thị trực quan 3 ảnh đối chiếu song song để người dùng nhận thấy rõ sự khác biệt thị giác.

2. **📊 Phân hệ Dashboard Thực nghiệm (Visual Analytics Dashboard):**
   * Tích hợp 4 thẻ KPI chỉ số tổng quát (Tổng mẫu, Accuracy Baseline 100%, Accuracy Contrast 88%, Accuracy HistEq 68%).
   * Nhúng biểu đồ Matplotlib tương tác (`FigureCanvasTkAgg`):
     * Biểu đồ so sánh Độ chính xác (%) & Độ tin cậy trung bình (%).
     * Biểu đồ thời gian xử lý (Latency ms).
   * Bảng dữ liệu đối soát toàn bộ 25 mẫu ký hiệu từ $A$ đến $Y$.

3. **🚀 Phân hệ Hướng phát triển (AI Roadmap):**
   * Mở rộng Dataset đa dạng và thích nghi miền (Domain Adaptation & CLAHE).
   * Nhận diện ký hiệu ASL động (Dynamic gestures: chữ $J$ và $Z$) bằng mô hình chuỗi Spatial-Temporal (CNN-LSTM / Video Swin Transformer).
   * Tối ưu hóa suy luận trên thiết bị nhúng (TensorFlow Lite INT8, Edge AI).

4. **ℹ️ Phân hệ Thông tin Mô hình (System Info):**
   * Kiến trúc mạng CNN 2 khối Conv2D(64) + MaxPooling + Dense(128) + Dense(29, Softmax).
   * Mã băm bảo mật SHA-256 xác thực tính toàn vẹn của mô hình.

---

## 3. CẤU TRÚC THƯ MỤC DỰ ÁN

```
BTL_TTNT/
├── asl-sign-language/
│   ├── models/
│   │   └── asl_classifier.keras       # Mô hình CNN 29 lớp (GIỮ NGUYÊN GỐC 100%)
│   ├── notebooks/
│   │   └── Bao_cao_TTNT.ipynb         # Notebook huấn luyện ban đầu
│   ├── preprocessing.py               # Module chứa các giải thuật tiền xử lý ảnh độc lập
│   ├── experiment_runner.py           # Module thực thi suy luận đối chiếu A, B, C
│   ├── app.py                         # Điểm khởi chạy chính của ứng dụng
│   ├── gui_app.py                     # Giao diện Enterprise Desktop GUI hoàn chỉnh
│   ├── requirements.txt               # Danh sách thư viện phụ thuộc
│   └── README.md                      # Tài liệu đồ án
├── test_data/                         # Dữ liệu ảnh thực nghiệm trích xuất từ dataset (25 ký tự A-Y)
├── benchmark_results.json             # Dữ liệu lưu trữ kết quả kiểm thử định lượng
├── run_benchmark.py                   # Script chạy đánh giá tự động trên toàn bộ tập test
├── run_full_system_test.py            # Suite kiểm thử tự động toàn diện hệ thống (10 tiêu chí)
└── run_gui.bat                        # File batch khởi động giao diện 1-click trên Windows
```

---

## 4. HƯỚNG DẪN CÀI ĐẶT & KHỞI CHẠY

### 4.1. Khởi chạy nhanh bằng file Batch (Khuyến nghị)
Nhấp đúp chuột vào file:
```
run_gui.bat
```

### 4.2. Khởi chạy bằng dòng lệnh
Kích hoạt môi trường ảo Python và khởi chạy:
```powershell
cd "F:\OneDrive\hoc hanh\XLA\BTL_TTNT"
.\.venv\Scripts\python.exe asl-sign-language\gui_app.py
```

### 4.3. Chạy kiểm thử tự động toàn diện hệ thống
```powershell
.\.venv\Scripts\python.exe run_full_system_test.py
```

---

## 5. TỔNG KẾT KẾT QUẢ THỰC NGHIỆM ĐỊNH LƯỢNG (N = 25 MẪU)

| Phương pháp | Accuracy (%) | Độ tin cậy TB (%) | Thời gian xử lý (ms) | Hiện tượng quan sát được |
| :--- | :---: | :---: | :---: | :--- |
| **A: Baseline (Ảnh gốc)** | **100.0%** (25/25) | **99.06%** | **0.24 ms** | Trùng khớp phân phối huấn luyện ban đầu của CNN. |
| **B: Contrast Stretching** | **88.0%** (22/25) | **93.03%** | **0.81 ms** | Tăng tương phản rõ rệt, sai 3 chữ ($A, N, S$) do bóng kẽ tay bị sắc cạnh hóa. |
| **C: Histogram Equalization** | **68.0%** (17/25) | **78.90%** | **0.41 ms** | Xảy ra *Covariate Shift* mạnh, phá vỡ bóng mịn ngón tay, sai 8 chữ cái. |

### Luận điểm học thuật phục vụ bảo vệ đồ án:
1. **Tiền xử lý tăng tương phản mạnh (HistEq) không phải lúc nào cũng có lợi cho Deep Learning:** Khi ảnh đầu vào đã nằm trong điều kiện ánh sáng chuẩn của dataset, việc cân bằng histogram toàn cục làm méo mó các gradient bóng đổ tự nhiên, dẫn đến giảm độ chính xác từ $100\%$ xuống $68\%$.
2. **Nguyên tắc ứng dụng thực tiễn:** Tiền xử lý tăng cường ảnh chỉ nên kích hoạt có điều kiện khi phát hiện ảnh chụp bị thiếu sáng trầm trọng, không nên áp dụng đồng loạt lên mọi ảnh.

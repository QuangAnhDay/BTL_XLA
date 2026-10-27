THỜI LƯỢNG: 45 giây. Mốc dự kiến 6:00–6:45. Tổng bài nói 9 phút 40 giây; dành ~5 phút cho vấn đáp.
LỜI TRÌNH BÀY
Để chứng minh tác động sâu sắc của tiền xử lý lên không gian xác suất, slide này phân tích chi tiết trường hợp ký hiệu 'A'. Ở ảnh gốc, mạng rất tự tin: nhãn A đạt 99,9%, E gần như bằng 0. Khi qua Histogram Equalization, mô hình vẫn đoán đúng A nhưng độ tự tin rơi xuống 91,7%, và xác suất nhầm sang E tăng lên 8,3%. Đáng báo động nhất là Contrast Stretching: mô hình bị đảo chiều hoàn toàn, khẳng định 98,4% đây là chữ E và chỉ dành 1,6% cho chữ A. Đây là minh chứng kinh điển cho thấy độ tự tin Softmax cao không đồng nghĩa với dự đoán đúng.
ĐIỀU KHIỂN / DỰ PHÒNG
Chỉ vào thanh ngang màu cam ở trường hợp Contrast Stretching. Nhấn mạnh việc mạng rất tự tin (98,4%) vào một quyết định sai hoàn toàn.
NGUỒN VÀ PHẠM VI
Dữ liệu Softmax trích xuất cho ký hiệu A: Baseline (A 99.9%), CS (E 98.4%, A 1.6%), HE (A 91.7%, E 8.3%).

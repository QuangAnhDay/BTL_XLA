THỜI LƯỢNG: 45 giây. Mốc dự kiến 4:25–5:10. Tổng bài nói 9 phút 40 giây; dành ~5 phút cho vấn đáp.
LỜI TRÌNH BÀY
Để giải thích nguyên nhân tại sao ảnh rõ hơn lại khiến mô hình đoán sai nhiều hơn, chúng ta cần xem xét dưới góc nhìn Covariate Shift. Trong học máy, Covariate Shift là hiện tượng phân phối dữ liệu đầu vào P(X) bị thay đổi so với dữ liệu huấn luyện. Mạng CNN nhận diện bàn tay không phải bằng trực giác mà bằng hàng chục bộ lọc tích chập 3x3 nhạy cảm với độ chênh lệch cường độ pixel. Khi ta cân bằng lược đồ, các nếp gấp tự nhiên giữa các ngón tay có thể bị biến đổi độ dày, tạo ra các cạnh nhân tạo khiến các tầng Conv trích xuất ra đặc trưng sai lệch.
ĐIỀU KHIỂN / DỰ PHÒNG
Trình bày theo chuỗi 5 bước từ ảnh gốc đến kết quả Softmax. Nhấn mạnh khung lưu ý khoa học ở dưới.
NGUỒN VÀ PHẠM VI
Lý thuyết Covariate Shift trong Deep Learning. Khẳng định cơ chế Conv2D phản ứng với cạnh giả là giả thuyết suy diễn, chưa đo feature maps trực tiếp.

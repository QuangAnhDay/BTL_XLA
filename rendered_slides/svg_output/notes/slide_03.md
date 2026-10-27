THỜI LƯỢNG: 50 giây. Mốc dự kiến 1:15–2:05. Tổng bài nói 9 phút 40 giây; dành ~5 phút cho vấn đáp.
LỜI TRÌNH BÀY
Để đảm bảo tính khoa học và khách quan, toàn bộ trọng số của mô hình asl_classifier.keras được giữ nguyên vẹn, kiểm tra bằng mã băm SHA-256 không thay đổi. Mô hình gồm hai khối tích chập 64 bộ lọc kích thước 3 nhân 3, tiếp nối bởi tầng Flatten với 33.856 chiều đặc trưng và tầng Dense 128 nơ-ron trước khi phân loại qua Softmax 29 lớp. Tập kiểm thử gồm 25 ký hiệu bàn tay chuẩn đại diện cho bảng chữ cái A đến Y. Mục tiêu là kiểm chứng xem khi mô hình đã học xong, tiền xử lý tác động như thế nào đến phản ứng của các tầng tích chập này.
ĐIỀU KHIỂN / DỰ PHÒNG
Chỉ vào sơ đồ pipeline 5 bước kiến trúc. Nhắc nhở người nghe rằng trọng số mạng không hề được tái huấn luyện trong suốt thử nghiệm.
NGUỒN VÀ PHẠM VI
File mô hình: asl_classifier.keras. Dữ liệu: 25 ảnh kích thước 100x100x3 RGB. Không đưa ra nhận định vượt quá phạm vi kiểm thử.

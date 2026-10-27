THỜI LƯỢNG: 40 giây. Mốc dự kiến 6:45–7:25. Tổng bài nói 9 phút 40 giây; dành ~5 phút cho vấn đáp.
LỜI TRÌNH BÀY
Để kết luận, nghiên cứu của nhóm em đưa ra một thông điệp quan trọng: Trong các hệ thống thị giác máy tính hiện đại dựa trên Deep Learning, tiền xử lý ảnh không thể được áp dụng một cách cảm tính dựa trên việc mắt người nhìn thấy rõ hơn. Bất kỳ sự can thiệp nào làm thay đổi phân phối cường độ sáng đều có nguy cơ gây ra hiện tượng Covariate Shift, dẫn đến suy giảm độ chính xác và làm lệch lạc độ tự tin Softmax. Mọi giải pháp tiền xử lý phải được kiểm chứng bằng thực nghiệm định lượng. Nhóm em xin chân thành cảm ơn thầy cô và sẵn sàng lắng nghe câu hỏi.
ĐIỀU KHIỂN / DỰ PHÒNG
Kết thúc bài thuyết trình đúng 7 phút 25 giây (nằm trọn trong giới hạn 10 phút). Chuyển sang tư thế sẵn sàng cho phần hỏi đáp phản biện.
NGUỒN VÀ PHẠM VI
Tổng kết toàn bộ 10 slide. Dữ liệu và kết luận tuân thủ trung thực với kết quả thực nghiệm đã cung cấp.
PHẦN VẤN ĐÁP DỰ PHÒNG — KHÔNG ĐỌC TRONG BÀI NÓI
1. Vì sao không huấn luyện lại mô hình với dữ liệu đã tăng tương phản?
-> Mục tiêu đề tài là đánh giá tác động của tiền xử lý lên một mô hình đã triển khai sẵn (off-the-shelf). Nếu huấn luyện lại, mô hình sẽ học phân phối mới và không còn phản ánh được tác động của Covariate Shift.
2. Vì sao chỉ thử nghiệm trên 25 ảnh?
-> Đây là tập kiểm thử đại diện 25 chữ cái A-Y được cung cấp trong phạm vi bài tập lớn. Nhóm đã ghi rõ hạn chế này và đề xuất mở rộng tập dữ liệu trong hướng phát triển.
3. Có phải Contrast Stretching luôn tệ hơn ảnh gốc?
-> Không. Nếu ảnh đầu vào thực sự bị chụp trong môi trường quá tối và mô hình được huấn luyện kèm data augmentation tương phản, tiền xử lý có thể có lợi. Điểm mấu chốt là sự tương thích phân phối.
4. Vì sao Histogram Equalization lại giảm sâu đến 68%?
-> HE làm biến dạng phân phối phi tuyến tính rất mạnh, làm sáng các vùng tối tự nhiên giữa các kẽ ngón tay, triệt tiêu bóng đổ là đặc trưng biên quan trọng của CNN.
5. Độ tự tin 98,4% của chữ E nói lên điều gì?
-> Cho thấy mạng bị over-confident (quá tự tin) khi phân phối bị lệch, chứng minh hàm Softmax cần được cân chuẩn (calibration) bằng các kỹ thuật như Temperature Scaling trước khi tin cậy vào xác suất.

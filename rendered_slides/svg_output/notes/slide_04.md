THỜI LƯỢNG: 45 giây. Mốc dự kiến 2:05–2:50. Tổng bài nói 9 phút 40 giây; dành ~5 phút cho vấn đáp.
LỜI TRÌNH BÀY
Phương pháp đầu tiên là Contrast Stretching. Để tránh làm biến đổi tông màu da của bàn tay, nhóm chuyển ảnh từ không gian màu RGB sang YCrCb và chỉ can thiệp vào kênh độ sáng Y. Thay vì dùng giá trị Min và Max tuyệt đối vốn rất nhạy cảm với các điểm ảnh nhiễu, thuật toán sử dụng ngưỡng phân vị 1% và 99%. Công thức ánh xạ tuyến tính đưa các giá trị dưới P1% về 0, trên P99% về 255 và kéo giãn dải ở giữa. Về mặt thị giác, bức ảnh trở nên trong trẻo và tương phản rõ ràng hơn.
ĐIỀU KHIỂN / DỰ PHÒNG
Chỉ vào công thức ánh xạ và sơ đồ quy trình 4 bước bên phải. Giải thích vì sao cần giữ nguyên hai kênh màu Cr và Cb.
NGUỒN VÀ PHẠM VI
Mã nguồn triển khai: percentile clipping tại p=1 và p=99 trên numpy mảng 2 chiều. Chuyển đổi màu sử dụng chuẩn YCrCb tiêu chuẩn.

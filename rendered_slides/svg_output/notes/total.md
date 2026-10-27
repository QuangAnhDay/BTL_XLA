# Speaker Notes

## Slide 01

THỜI LƯỢNG: 30 giây. Mốc dự kiến 0:00–0:30. Tổng bài nói 9 phút 40 giây; dành ~5 phút cho vấn đáp.
LỜI TRÌNH BÀY
Kính chào thầy cô và các bạn. Trong thị giác máy tính, tiền xử lý ảnh như tăng độ tương phản thường được mặc định coi là bước có lợi để làm ảnh rõ nét hơn. Tuy nhiên, khi đưa vào các mô hình Deep Learning đã được huấn luyện sẵn, việc thay đổi phân phối cường độ sáng có thực sự giúp tăng độ chính xác hay ngược lại? Nhóm em xin trình bày đề tài đánh giá thực nghiệm tác động của Contrast Stretching và Histogram Equalization đến mô hình CNN nhận diện ký hiệu bàn tay ASL.
ĐIỀU KHIỂN / DỰ PHÒNG
Dừng 2 giây để người nghe quan sát dải ảnh 3 trạng thái của ký hiệu ASL. Giọng trình bày tự tin, rõ ràng.
NGUỒN VÀ PHẠM VI
Báo cáo dựa trên thực nghiệm kiểm thử 25 ảnh ký hiệu ASL A–Y với mô hình CNN asl_classifier.keras.

## Slide 02

THỜI LƯỢNG: 45 giây. Mốc dự kiến 0:30–1:15. Tổng bài nói 9 phút 40 giây; dành ~5 phút cho vấn đáp.
LỜI TRÌNH BÀY
Trong thực tế, khi đối mặt với ảnh chụp thiếu sáng hoặc mờ, phản xạ tự nhiên của kỹ sư xử lý ảnh là áp dụng các bộ lọc tăng tương phản. Tuy nhiên, mạng nơ-ron tích chập (CNN) hoạt động dựa trên các bộ lọc không gian học được từ một phân phối cường độ sáng cụ thể. Khi chúng ta thay đổi lược đồ mức xám, chúng ta vô tình gây ra hiện tượng dịch chuyển phân phối đầu vào. Câu hỏi đặt ra là: Liệu một bức ảnh trông rõ nét hơn với con người có thực sự giúp mạng CNN phân loại đúng hơn không?
ĐIỀU KHIỂN / DỰ PHÒNG
Nhấn mạnh vào câu hỏi nghiên cứu ở khung màu xanh. Nêu rõ ba trường hợp thực nghiệm sẽ so sánh xuyên suốt bài báo cáo.
NGUỒN VÀ PHẠM VI
Lý thuyết Covariate Shift (Shimodaira, 2000). Ba trường hợp đối chứng được thực hiện trên cùng tập 25 ảnh.

## Slide 03

THỜI LƯỢNG: 50 giây. Mốc dự kiến 1:15–2:05. Tổng bài nói 9 phút 40 giây; dành ~5 phút cho vấn đáp.
LỜI TRÌNH BÀY
Để đảm bảo tính khoa học và khách quan, toàn bộ trọng số của mô hình asl_classifier.keras được giữ nguyên vẹn, kiểm tra bằng mã băm SHA-256 không thay đổi. Mô hình gồm hai khối tích chập 64 bộ lọc kích thước 3 nhân 3, tiếp nối bởi tầng Flatten với 33.856 chiều đặc trưng và tầng Dense 128 nơ-ron trước khi phân loại qua Softmax 29 lớp. Tập kiểm thử gồm 25 ký hiệu bàn tay chuẩn đại diện cho bảng chữ cái A đến Y. Mục tiêu là kiểm chứng xem khi mô hình đã học xong, tiền xử lý tác động như thế nào đến phản ứng của các tầng tích chập này.
ĐIỀU KHIỂN / DỰ PHÒNG
Chỉ vào sơ đồ pipeline 5 bước kiến trúc. Nhắc nhở người nghe rằng trọng số mạng không hề được tái huấn luyện trong suốt thử nghiệm.
NGUỒN VÀ PHẠM VI
File mô hình: asl_classifier.keras. Dữ liệu: 25 ảnh kích thước 100x100x3 RGB. Không đưa ra nhận định vượt quá phạm vi kiểm thử.

## Slide 04

THỜI LƯỢNG: 45 giây. Mốc dự kiến 2:05–2:50. Tổng bài nói 9 phút 40 giây; dành ~5 phút cho vấn đáp.
LỜI TRÌNH BÀY
Phương pháp đầu tiên là Contrast Stretching. Để tránh làm biến đổi tông màu da của bàn tay, nhóm chuyển ảnh từ không gian màu RGB sang YCrCb và chỉ can thiệp vào kênh độ sáng Y. Thay vì dùng giá trị Min và Max tuyệt đối vốn rất nhạy cảm với các điểm ảnh nhiễu, thuật toán sử dụng ngưỡng phân vị 1% và 99%. Công thức ánh xạ tuyến tính đưa các giá trị dưới P1% về 0, trên P99% về 255 và kéo giãn dải ở giữa. Về mặt thị giác, bức ảnh trở nên trong trẻo và tương phản rõ ràng hơn.
ĐIỀU KHIỂN / DỰ PHÒNG
Chỉ vào công thức ánh xạ và sơ đồ quy trình 4 bước bên phải. Giải thích vì sao cần giữ nguyên hai kênh màu Cr và Cb.
NGUỒN VÀ PHẠM VI
Mã nguồn triển khai: percentile clipping tại p=1 và p=99 trên numpy mảng 2 chiều. Chuyển đổi màu sử dụng chuẩn YCrCb tiêu chuẩn.

## Slide 05

THỜI LƯỢNG: 45 giây. Mốc dự kiến 2:50–3:35. Tổng bài nói 9 phút 40 giây; dành ~5 phút cho vấn đáp.
LỜI TRÌNH BÀY
Phương pháp thứ hai là Histogram Equalization. Thay vì kéo giãn tuyến tính, thuật toán tính toán hàm phân phối tích lũy (CDF) của kênh độ sáng Y và dùng nó làm hàm ánh xạ. Các mức xám xuất hiện nhiều sẽ được trải rộng ra, giúp cực đại hóa entropy thông tin của ảnh. Tuy nhiên, trong nhận diện cử chỉ bàn tay, bóng đổ giữa các ngón tay và nếp nhăn ở khớp ngón là các tín hiệu biên rất quan trọng. Khi lược đồ bị san phẳng mạnh mẽ, các vùng bóng tối tự nhiên có thể bị làm sáng quá mức, dẫn đến mất mát các đặc trưng hình học tinh tế.
ĐIỀU KHIỂN / DỰ PHÒNG
Chỉ vào biểu đồ phân phối trước và sau cân bằng. Nhấn mạnh việc san phẳng mức xám có thể gây hại cho các đặc trưng biên cục bộ.
NGUỒN VÀ PHẠM VI
Triển khai thuật toán: cv2.equalizeHist trên kênh Y. Biểu đồ trên slide mang tính minh họa nguyên lý toán học.

## Slide 06

THỜI LƯỢNG: 50 giây. Mốc dự kiến 3:35–4:25. Tổng bài nói 9 phút 40 giây; dành ~5 phút cho vấn đáp.
LỜI TRÌNH BÀY
Đây là kết quả thực nghiệm trung tâm của bài báo cáo. Bảng số liệu cho thấy một sự tương phản rất rõ rệt: Trên tập kiểm thử 25 ảnh, ảnh gốc ban đầu đạt độ chính xác tuyệt đối 100% với confidence trung bình lên tới 99,06%. Khi áp dụng Contrast Stretching, độ chính xác giảm xuống 88% với 3 ảnh bị dự đoán sai. Đáng ngạc nhiên hơn, Histogram Equalization – phương pháp vốn tạo ra ảnh có tương phản thị giác rất mạnh – lại khiến độ chính xác sụt giảm nghiêm trọng xuống còn 68%, tức sai tới 8 trên 25 ảnh. Bên cạnh đó, thời gian xử lý cũng tăng từ 0,24 ms lên 0,81 ms.
ĐIỀU KHIỂN / DỰ PHÒNG
Chỉ vào 3 thẻ số liệu lớn phía trên và biểu đồ cột so sánh. Nhấn mạnh rằng mức giảm 32% của Histogram Equalization là rất lớn.
NGUỒN VÀ PHẠM VI
Báo cáo kết quả kiểm thử: Ảnh gốc 25/25, CS 22/25, HE 17/25. Thời gian đo lường bằng millisecond trên cùng phần cứng.

## Slide 07

THỜI LƯỢNG: 45 giây. Mốc dự kiến 4:25–5:10. Tổng bài nói 9 phút 40 giây; dành ~5 phút cho vấn đáp.
LỜI TRÌNH BÀY
Để giải thích nguyên nhân tại sao ảnh rõ hơn lại khiến mô hình đoán sai nhiều hơn, chúng ta cần xem xét dưới góc nhìn Covariate Shift. Trong học máy, Covariate Shift là hiện tượng phân phối dữ liệu đầu vào P(X) bị thay đổi so với dữ liệu huấn luyện. Mạng CNN nhận diện bàn tay không phải bằng trực giác mà bằng hàng chục bộ lọc tích chập 3x3 nhạy cảm với độ chênh lệch cường độ pixel. Khi ta cân bằng lược đồ, các nếp gấp tự nhiên giữa các ngón tay có thể bị biến đổi độ dày, tạo ra các cạnh nhân tạo khiến các tầng Conv trích xuất ra đặc trưng sai lệch.
ĐIỀU KHIỂN / DỰ PHÒNG
Trình bày theo chuỗi 5 bước từ ảnh gốc đến kết quả Softmax. Nhấn mạnh khung lưu ý khoa học ở dưới.
NGUỒN VÀ PHẠM VI
Lý thuyết Covariate Shift trong Deep Learning. Khẳng định cơ chế Conv2D phản ứng với cạnh giả là giả thuyết suy diễn, chưa đo feature maps trực tiếp.

## Slide 08

THỜI LƯỢNG: 50 giây. Mốc dự kiến 5:10–6:00. Tổng bài nói 9 phút 40 giây; dành ~5 phút cho vấn đáp.
LỜI TRÌNH BÀY
Khi đi sâu vào các ca dự đoán sai, chúng ta phát hiện một quy luật hình thái học rất thú vị. Với Contrast Stretching, toàn bộ 3 ca lỗi là A, N và S đều bị mô hình dự đoán nhầm thành chữ E. Trong ngôn ngữ ký hiệu ASL, A, E, N, S đều là các thế nắm tay chặt, điểm khác biệt duy nhất nằm ở vị trí ngón cái. Khi độ tương phản bị kéo giãn, ranh giới nếp gấp của ngón cái bị triệt tiêu, khiến mô hình nhầm lẫn sang chữ E. Tương tự với Histogram Equalization, 8 ca lỗi đều rơi vào các cặp có hình học cực kỳ giống nhau như G với H, R với U hay X với V.
ĐIỀU KHIỂN / DỰ PHÒNG
So sánh sự tập trung lỗi của Contrast Stretching (về chữ E) và sự phân tán lỗi của Histogram Equalization (8 cặp).
NGUỒN VÀ PHẠM VI
Ghi nhận thực nghiệm: CS lỗi A, N, S -> E. HE lỗi G->H, I->J, N->E, Q->G, R->U, S->E, U->R, X->V. Không tự vẽ thêm các ảnh nhầm lẫn chưa có.

## Slide 09

THỜI LƯỢNG: 45 giây. Mốc dự kiến 6:00–6:45. Tổng bài nói 9 phút 40 giây; dành ~5 phút cho vấn đáp.
LỜI TRÌNH BÀY
Để chứng minh tác động sâu sắc của tiền xử lý lên không gian xác suất, slide này phân tích chi tiết trường hợp ký hiệu 'A'. Ở ảnh gốc, mạng rất tự tin: nhãn A đạt 99,9%, E gần như bằng 0. Khi qua Histogram Equalization, mô hình vẫn đoán đúng A nhưng độ tự tin rơi xuống 91,7%, và xác suất nhầm sang E tăng lên 8,3%. Đáng báo động nhất là Contrast Stretching: mô hình bị đảo chiều hoàn toàn, khẳng định 98,4% đây là chữ E và chỉ dành 1,6% cho chữ A. Đây là minh chứng kinh điển cho thấy độ tự tin Softmax cao không đồng nghĩa với dự đoán đúng.
ĐIỀU KHIỂN / DỰ PHÒNG
Chỉ vào thanh ngang màu cam ở trường hợp Contrast Stretching. Nhấn mạnh việc mạng rất tự tin (98,4%) vào một quyết định sai hoàn toàn.
NGUỒN VÀ PHẠM VI
Dữ liệu Softmax trích xuất cho ký hiệu A: Baseline (A 99.9%), CS (E 98.4%, A 1.6%), HE (A 91.7%, E 8.3%).

## Slide 10

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

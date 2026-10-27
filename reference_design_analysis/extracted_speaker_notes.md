# Extracted Speaker Notes from Reference Deck

## Slide 1

```
THỜI LƯỢNG: 25 giây. Mốc dự kiến 0:00–0:25. Tổng bài nói 9 phút 40 giây; dành khoảng 5 phút cho vấn đáp.
LỜI TRÌNH BÀY
Kính chào thầy cô. Trên màn hình là một khung cảnh được ghép từ năm bức ảnh. Nếu chỉ nhìn kết quả, chúng ta có thể nghĩ rằng công việc này đơn giản là đặt các ảnh cạnh nhau. Nhưng để các chi tiết trùng khớp và vùng nối chuyển tiếp tự nhiên, hệ thống phải giải quyết nhiều bài toán xử lý ảnh. Nhóm em xin trình bày dự án Panorama Stitching và những giải pháp đã áp dụng.
ĐIỀU KHIỂN / DỰ PHÒNG
Dừng một nhịp để người nghe quan sát ảnh. Bìa có ba ô tên thành viên và một ô giảng viên theo yêu cầu người dùng; chưa được cung cấp tên thật.
NGUỒN VÀ PHẠM VI
Báo cáo lịch sử 24/10/2026: outputs/panorama_auto_100MP.json và outputs/verification_summary.md. Bộ 5 ảnh C:/Code/ngoai_nha/1, mỗi ảnh 1920 × 1440. Thời gian là stitch_seconds; không đồng nhất với thời gian mã hóa hay toàn bộ thao tác UI. Các cấu hình khác nhau không phải đối chứng tốc độ công bằng.
```

## Slide 2

```
THỜI LƯỢNG: 35 giây. Mốc dự kiến 0:25–1:00. Tổng bài nói 9 phút 40 giây; dành khoảng 5 phút cho vấn đáp.
LỜI TRÌNH BÀY
Hai bức ảnh này có một phần khung cảnh chung, nhưng vị trí các chi tiết đã thay đổi theo góc chụp. Độ sáng giữa các ảnh cũng có thể khác nhau. Nếu ghép trực tiếp, chúng ta dễ thấy ảnh bị lệch hoặc lộ đường nối. Dải ảnh phía dưới cho thấy một khó khăn khác: với góc nhìn rộng, phép chiếu phẳng có thể kéo giãn mạnh hai đầu. Vì vậy, nhóm chia bài toán thành ba việc: tìm đúng điểm tương ứng, chọn mô hình hình học phù hợp và xử lý vùng giao nhau.
NGUỒN VÀ PHẠM VI
Mã nguồn chỉ đọc: panorama/features.py, homography.py, ordering.py, camera.py, projection.py, rendering.py, seams.py, cropping.py, kernels.py; README.md. Thư mục dự án: C:/Users/Laptop/Downloads/panorama_stitching_source/panorama_stitching. Ảnh và panorama phẳng từ bộ dữ liệu thật. Không khẳng định mọi cặp ảnh đều có chênh lệch phơi sáng lớn.
```

## Slide 3

```
THỜI LƯỢNG: 40 giây. Mốc dự kiến 1:00–1:40. Tổng bài nói 9 phút 40 giây; dành khoảng 5 phút cho vấn đáp.
LỜI TRÌNH BÀY
Đây là pipeline của hệ thống. Trước hết, chương trình chuẩn bị ảnh và tìm những chi tiết có thể đối chiếu. Từ các cặp điểm đó, hệ thống ước lượng quan hệ hình học, xác định thứ tự và tinh chỉnh cả chuỗi ảnh. Tiếp theo là lựa chọn phép chiếu, rồi cân bằng sáng, tìm đường nối, trộn và xuất kết quả. OpenCV hỗ trợ phát hiện SIFT hoặc ORB. Các khâu matching, DLT, RANSAC, tối ưu, lấy mẫu và trộn ảnh được triển khai trong các module riêng, không gọi bộ ghép panorama có sẵn.
ĐIỀU KHIỂN / DỰ PHÒNG
Đoạn phim minh họa cấu trúc pipeline, không biểu diễn thời gian chạy hay kiến trúc phần cứng thật. Video nhúng dài 8 giây; bấm vào hình nếu muốn phát. Có ảnh poster tĩnh đầy đủ.
NGUỒN VÀ PHẠM VI
Mã nguồn chỉ đọc: panorama/features.py, homography.py, ordering.py, camera.py, projection.py, rendering.py, seams.py, cropping.py, kernels.py; README.md. Thư mục dự án: C:/Users/Laptop/Downloads/panorama_stitching_source/panorama_stitching.
```

## Slide 4

```
THỜI LƯỢNG: 35 giây. Mốc dự kiến 1:40–2:15. Tổng bài nói 9 phút 40 giây; dành khoảng 5 phút cho vấn đáp.
LỜI TRÌNH BÀY
Một quyết định quan trọng là tách ảnh dùng để phân tích khỏi ảnh dùng để dựng kết quả. Tìm đặc trưng trên ảnh thu nhỏ giúp giảm lượng tính toán. Tuy nhiên, ở bước xuất, hệ thống quay về lấy mẫu trên ảnh gốc. Nhờ đó, kích thước ảnh phân tích không trực tiếp giới hạn kích thước ảnh đầu ra. Điều cần làm chính xác là quy đổi tọa độ giữa hai độ phân giải, kể cả tỷ lệ thực tế theo từng chiều. Việc tăng số pixel đầu ra vẫn có thể cần nội suy và không tạo thêm chi tiết thật.
NGUỒN VÀ PHẠM VI
Mã nguồn chỉ đọc: panorama/features.py, homography.py, ordering.py, camera.py, projection.py, rendering.py, seams.py, cropping.py, kernels.py; README.md. Thư mục dự án: C:/Users/Laptop/Downloads/panorama_stitching_source/panorama_stitching. geometry.resize_to_limit và rendering.py; tỷ lệ resize theo từng chiều đã có kiểm thử.
```

## Slide 5

```
THỜI LƯỢNG: 40 giây. Mốc dự kiến 2:15–2:55. Tổng bài nói 9 phút 40 giây; dành khoảng 5 phút cho vấn đáp.
LỜI TRÌNH BÀY
Để nhận ra cùng một chi tiết, hệ thống cần hai loại thông tin. Thứ nhất là điểm đặc trưng, tức vị trí có thể nhận biết trong ảnh. Thứ hai là descriptor, một biểu diễn của vùng lân cận để so sánh với ảnh khác. Trên màn hình là các điểm SIFT được chọn lọc từ ảnh thật. Những vùng có nhiều kết cấu thường cung cấp nhiều thông tin hơn vùng trơn. Dự án hỗ trợ cả SIFT và ORB. Đây là phần sử dụng OpenCV; sau đó, descriptor được chuyển sang module matching do nhóm tự cài đặt.
NGUỒN VÀ PHẠM VI
Mã nguồn chỉ đọc: panorama/features.py, homography.py, ordering.py, camera.py, projection.py, rendering.py, seams.py, cropping.py, kernels.py; README.md. Thư mục dự án: C:/Users/Laptop/Downloads/panorama_stitching_source/panorama_stitching. Các điểm hiển thị được tạo lại bằng detect_features trên ảnh 0 (2).jpg; chỉ vẽ tập chọn lọc để dễ đọc.
```

## Slide 6

```
THỜI LƯỢNG: 45 giây. Mốc dự kiến 2:55–3:40. Tổng bài nói 9 phút 40 giây; dành khoảng 5 phút cho vấn đáp.
LỜI TRÌNH BÀY
Module matching tìm hai descriptor gần nhất cho mỗi điểm. Với SIFT, hệ thống dùng khoảng cách Euclid; với ORB, dùng khoảng cách Hamming. Tuy nhiên, nếu hai ứng viên có độ giống gần nhau, kết quả vẫn mơ hồ. Lowe ratio test giữ ứng viên đầu khi khoảng cách của nó nhỏ hơn không phẩy bảy lăm lần khoảng cách ứng viên thứ hai, theo cấu hình mặc định. Sau đó, kiểm tra hai chiều yêu cầu sự tương ứng được xác nhận theo cả hai hướng. Các đường nối trên hình là một phần các cặp thực tế, được chọn lọc để dễ quan sát.
NGUỒN VÀ PHẠM VI
Mã nguồn chỉ đọc: panorama/features.py, homography.py, ordering.py, camera.py, projection.py, rendering.py, seams.py, cropping.py, kernels.py; README.md. Thư mục dự án: C:/Users/Laptop/Downloads/panorama_stitching_source/panorama_stitching. features.nearest_two, match_features; ngưỡng 0,75 là cấu hình mặc định, không phải hằng số đúng cho mọi dữ liệu. Đường nối là inlier chọn lọc sau kiểm tra hình học để minh họa tương ứng.
```

## Slide 7

```
THỜI LƯỢNG: 50 giây. Mốc dự kiến 3:40–4:30. Tổng bài nói 9 phút 40 giây; dành khoảng 5 phút cho vấn đáp.
LỜI TRÌNH BÀY
Khi đã có các điểm tương ứng, chúng ta cần một phép biến đổi để đưa chúng về cùng hệ tọa độ. Trong mô hình phẳng, quan hệ này được biểu diễn bằng homography, một ma trận ba nhân ba. Normalized DLT chuẩn hóa tọa độ, lập hệ phương trình từ các cặp điểm và tìm nghiệm bằng SVD. Cần ít nhất bốn cặp điểm ở cấu hình không suy biến. Đoạn minh họa cho thấy một vùng ảnh được biến đổi để các điểm tương ứng trùng nhau. Homography phù hợp với cảnh gần phẳng hoặc mô hình camera quay quanh một tâm; nó không mô tả được mọi sai khác của cảnh ba chiều.
ĐIỀU KHIỂN / DỰ PHÒNG
Bấm vào hình để phát đoạn minh họa 6,3 giây; tiếp tục nói trong lúc hình chuyển động. Nếu không phát, dùng hình tĩnh để chỉ bốn điểm tương ứng.
NGUỒN VÀ PHẠM VI
Mã nguồn chỉ đọc: panorama/features.py, homography.py, ordering.py, camera.py, projection.py, rendering.py, seams.py, cropping.py, kernels.py; README.md. Thư mục dự án: C:/Users/Laptop/Downloads/panorama_stitching_source/panorama_stitching. homography.estimate_homography_dlt. Hoạt ảnh ManimGX là minh họa nguyên lý, không phải phép biến đổi đo được từ bộ ảnh thật.
```

## Slide 8

```
THỜI LƯỢNG: 55 giây. Mốc dự kiến 4:30–5:25. Tổng bài nói 9 phút 40 giây; dành khoảng 5 phút cho vấn đáp.
LỜI TRÌNH BÀY
Dù đã lọc descriptor, chúng ta vẫn có thể gặp các cặp khớp sai. RANSAC giải quyết vấn đề này bằng cách thử nhiều mô hình từ những tập nhỏ. Mỗi lần, thuật toán chọn bốn cặp điểm, tính homography, rồi kiểm tra bao nhiêu điểm có sai số nằm trong ngưỡng cho phép. Các điểm đó gọi là inlier. Mô hình được nhiều điểm đồng thuận sẽ được giữ lại và ước lượng lại từ tập inlier. Trong cặp ảnh đang minh họa, có hai trăm bốn mươi chín cặp khớp và hai trăm hai mươi sáu inlier. Ratio test kiểm tra mức tương đồng, còn RANSAC kiểm tra tính nhất quán hình học.
ĐIỀU KHIỂN / DỰ PHÒNG
Các đường màu nâu là cặp không phù hợp mô hình trong tập hiển thị. Chỉ số inlier cao không đủ để khẳng định không còn lệch cục bộ.
NGUỒN VÀ PHẠM VI
Mã nguồn chỉ đọc: panorama/features.py, homography.py, ordering.py, camera.py, projection.py, rendering.py, seams.py, cropping.py, kernels.py; README.md. Thư mục dự án: C:/Users/Laptop/Downloads/panorama_stitching_source/panorama_stitching. Báo cáo lịch sử 24/10/2026: outputs/panorama_auto_100MP.json và outputs/verification_summary.md. Bộ 5 ảnh C:/Code/ngoai_nha/1, mỗi ảnh 1920 × 1440. Thời gian là stitch_seconds; không đồng nhất với thời gian mã hóa hay toàn bộ thao tác UI. Các cấu hình khác nhau không phải đối chứng tốc độ công bằng. Số liệu cặp source=1, destination=2; lượt tái tạo hình minh họa cho cùng 249/226. Chỉ hiển thị tập con đường nối.
```

## Slide 9

```
THỜI LƯỢNG: 40 giây. Mốc dự kiến 5:25–6:05. Tổng bài nói 9 phút 40 giây; dành khoảng 5 phút cho vấn đáp.
LỜI TRÌNH BÀY
Với nhiều ảnh, một cặp khớp tốt vẫn chưa đủ. Hệ thống đánh giá liên kết bằng số inlier và dùng quy hoạch động Held–Karp để tìm thứ tự phù hợp. Sau đó, chương trình chọn ảnh tham chiếu và tinh chỉnh hình học chung. Nếu chỉ nối lần lượt từng cặp, sai số nhỏ có thể tích lũy dọc chuỗi. Tối ưu với Huber và Levenberg–Marquardt giúp giảm ảnh hưởng của sai số lớn và làm các quan hệ nhất quán hơn. Đây vẫn là tối ưu trong một mô hình hình học, nên không bảo đảm sửa được mọi lệch do parallax.
NGUỒN VÀ PHẠM VI
Mã nguồn chỉ đọc: panorama/features.py, homography.py, ordering.py, camera.py, projection.py, rendering.py, seams.py, cropping.py, kernels.py; README.md. Thư mục dự án: C:/Users/Laptop/Downloads/panorama_stitching_source/panorama_stitching. ordering.py, camera.refine_planar và estimate_cameras, optimization.py; ảnh tham chiếu là count//2 trong thứ tự đã xác định.
```

## Slide 10

```
THỜI LƯỢNG: 55 giây. Mốc dự kiến 6:05–7:00. Tổng bài nói 9 phút 40 giây; dành khoảng 5 phút cho vấn đáp.
LỜI TRÌNH BÀY
Đây là bước tạo khác biệt rõ nhất trên bộ ảnh thực tế. Ở phép chiếu phẳng, các chi tiết ở hai đầu bị kéo giãn mạnh. Với hình trụ, khung cảnh rộng được biểu diễn phù hợp hơn và mức giãn giảm. Báo cáo ghi nhận chỉ số giãn khoảng bốn phẩy không tám lần ở mô hình phẳng và một phẩy hai sáu lần ở hình trụ. Chế độ tự động không chỉ nhìn vào một chỉ số: nó còn xem sai số căn chỉnh và vùng giữ lại sau crop. Hình trụ cũng có đánh đổi: một số đường ngang có thể cong, và mô hình cần tiêu cự cùng hướng camera đủ tin cậy.
NGUỒN VÀ PHẠM VI
Mã nguồn chỉ đọc: panorama/features.py, homography.py, ordering.py, camera.py, projection.py, rendering.py, seams.py, cropping.py, kernels.py; README.md. Thư mục dự án: C:/Users/Laptop/Downloads/panorama_stitching_source/panorama_stitching. Báo cáo lịch sử 24/10/2026: outputs/panorama_auto_100MP.json và outputs/verification_summary.md. Bộ 5 ảnh C:/Code/ngoai_nha/1, mỗi ảnh 1920 × 1440. Thời gian là stitch_seconds; không đồng nhất với thời gian mã hóa hay toàn bộ thao tác UI. Các cấu hình khác nhau không phải đối chứng tốc độ công bằng. Hai ảnh giữ tỷ lệ nguyên gốc, cùng bộ nguồn; đầu ra có độ phân giải khác nhau nên dùng để đối chiếu hình dạng, không phải độ nét. Chỉ số stretch do projection.metrics tính, không phải phép đo mọi vật thể trong ảnh.
```

## Slide 11

```
THỜI LƯỢNG: 45 giây. Mốc dự kiến 7:00–7:45. Tổng bài nói 9 phút 40 giây; dành khoảng 5 phút cho vấn đáp.
LỜI TRÌNH BÀY
Sau căn chỉnh, vùng giao nhau vẫn có thể lộ đường nối do chênh lệch sáng hoặc sai lệch cục bộ. Hệ thống thực hiện ba việc. Đầu tiên là ước lượng gain để giảm khác biệt độ sáng. Tiếp theo, graph-cut với thuật toán Dinic tìm cách phân chia vùng đóng góp giữa các ảnh. Cuối cùng, feather blending trộn theo trọng số để chuyển tiếp mềm hơn. Trên hình bên phải, đường xanh đánh dấu ranh giới sở hữu vùng ảnh trên bản nháp. Đây là hình giải thích cách xử lý; đường xanh không xuất hiện trong panorama cuối. Vật chuyển động hoặc parallax vẫn có thể gây bóng ma.
NGUỒN VÀ PHẠM VI
Mã nguồn chỉ đọc: panorama/features.py, homography.py, ordering.py, camera.py, projection.py, rendering.py, seams.py, cropping.py, kernels.py; README.md. Thư mục dự án: C:/Users/Laptop/Downloads/panorama_stitching_source/panorama_stitching. Các hình được tái tạo từ Draft của pipeline trên cùng dữ liệu. Bên trái là phép ghép cứng tạo riêng để đối chiếu, không phải phiên bản trước được benchmark. Bên phải là hình minh họa gain + seam weights trên bản nháp, có overlay đường ranh; không thay thế đánh giá ảnh xuất.
```

## Slide 12

```
THỜI LƯỢNG: 50 giây. Mốc dự kiến 7:45–8:35. Tổng bài nói 9 phút 40 giây; dành khoảng 5 phút cho vấn đáp.
LỜI TRÌNH BÀY
Để dựng ảnh cuối, hệ thống duyệt pixel đầu ra và ánh xạ ngược về vị trí trong ảnh nguồn. Vì vị trí nguồn thường không nằm đúng tâm một pixel, nội suy song tuyến tính kết hợp bốn điểm lân cận để tính giá trị. Phần dựng ảnh chạy theo từng tile, giúp giới hạn bộ nhớ cho các mảng trung gian. Kết quả lớn có thể được lưu bằng memmap. Cuối cùng, hệ thống tìm hình chữ nhật nằm trong vùng dữ liệu hợp lệ và kiểm tra coverage ở độ phân giải xuất. Crop kín giúp loại khoảng trống, nhưng phải chấp nhận mất một phần cảnh ở mép; nó không chứng minh rằng ảnh đã hết sai lệch.
NGUỒN VÀ PHẠM VI
Mã nguồn chỉ đọc: panorama/features.py, homography.py, ordering.py, camera.py, projection.py, rendering.py, seams.py, cropping.py, kernels.py; README.md. Thư mục dự án: C:/Users/Laptop/Downloads/panorama_stitching_source/panorama_stitching. rendering.bilinear_sample, render_panorama; cropping.largest_valid_rectangle. Lưới nội suy là minh họa nguyên lý. Mask phía dưới là bản nháp thực tế; không dùng cường độ đen để xác định vùng thiếu dữ liệu.
```

## Slide 13

```
THỜI LƯỢNG: 40 giây. Mốc dự kiến 8:35–9:15. Tổng bài nói 9 phút 40 giây; dành khoảng 5 phút cho vấn đáp.
LỜI TRÌNH BÀY
Trên bộ năm ảnh thực tế, mỗi ảnh một nghìn chín trăm hai mươi nhân một nghìn bốn trăm bốn mươi pixel, báo cáo đã lưu ghi nhận lượt tự động chọn hình trụ xuất khoảng một trăm megapixel trong mười chín phẩy chín chín giây ghép. RAM đỉnh khoảng tám trăm ba mươi mốt megabyte. Đây là một lượt chạy cụ thể, không phải cam kết cho mọi máy hay mọi bộ ảnh. Một trăm megapixel có nội suy, nên không đồng nghĩa có thêm chi tiết thật. Hệ thống còn hạn chế với vật chuyển động và camera dịch chuyển.
NGUỒN VÀ PHẠM VI
Báo cáo lịch sử 24/10/2026: outputs/panorama_auto_100MP.json và outputs/verification_summary.md. Bộ 5 ảnh C:/Code/ngoai_nha/1, mỗi ảnh 1920 × 1440. Thời gian là stitch_seconds; không đồng nhất với thời gian mã hóa hay toàn bộ thao tác UI. Các cấu hình khác nhau không phải đối chứng tốc độ công bằng. Báo cáo cũng ghi nhận 34 kiểm thử đạt vào 24/10/2026; bài này không tuyên bố vừa chạy lại toàn bộ test. Giá trị RAM gốc 830,93 MB, được làm tròn thành 831 MB.
```

## Slide 14

```
THỜI LƯỢNG: 25 giây. Mốc dự kiến 9:15–9:40. Tổng bài nói 9 phút 40 giây; dành khoảng 5 phút cho vấn đáp.
LỜI TRÌNH BÀY
Từ năm bức ảnh rời rạc ban đầu, hệ thống đã tái tạo được một khung cảnh chung bằng chuỗi xử lý có thể quan sát và giải thích. Đóng góp chính của nhóm nằm ở việc tự cài đặt các thuật toán lõi và phối hợp chúng thành một pipeline hoàn chỉnh. Nhóm em xin kết lại bằng ba việc: tìm đúng điểm, căn đúng hình và làm mượt vùng nối. Nhóm em xin cảm ơn thầy cô và sẵn sàng trả lời câu hỏi.
ĐIỀU KHIỂN / DỰ PHÒNG
PHẦN VẤN ĐÁP DỰ PHÒNG — KHÔNG ĐỌC TRONG BÀI NÓI
1. Nhóm tự viết những gì?
Matching KNN theo block, ratio/mutual check, Normalized DLT, RANSAC, Held–Karp ordering, tối ưu hình học, phép chiếu, inverse mapping, nội suy, Dinic min-cut, feather blending và largest-valid-rectangle crop. OpenCV hỗ trợ IO, SIFT/ORB, resize và hình minh họa; NumPy hỗ trợ phép toán và đại số tuyến tính; Numba biên dịch vòng lặp tự viết.
2. Vì sao cần cả ratio test và RANSAC?
Ratio test lọc theo độ phân biệt descriptor. RANSAC kiểm tra tính nhất quán với một mô hình hình học, nên xử lý thêm các khớp sai còn sót.
3. Vì sao tối thiểu bốn cặp điểm?
Homography có tám bậc tự do vì xác định đến một hệ số tỷ lệ. Mỗi cặp điểm cho hai phương trình độc lập. Bốn cặp phải ở cấu hình không suy biến; thực tế cần nhiều điểm và RANSAC.
4. Vì sao dùng Normalized DLT?
Chuẩn hóa Hartley giúp hệ phương trình có điều kiện số tốt hơn. DLT xây dựng hệ tuyến tính đồng nhất và dùng SVD tìm null-space; sau đó giải chuẩn hóa.
5. Homography đúng với mọi cảnh không?
Không. Quan hệ chính xác trong các điều kiện như mặt phẳng hoặc camera quay quanh cùng tâm trong mô hình pinhole. Camera dịch chuyển cùng vật gần gây parallax, khó mô tả bằng một homography chung.
6. Hình trụ có luôn tốt hơn phẳng không?
Không. Phẳng phù hợp khi cần giữ đường thẳng và góc nhìn phù hợp. Hình trụ hữu ích với quét ngang rộng, nhưng có thể làm cong một số đường ngang và cần mô hình camera tin cậy.
7. Auto lựa chọn dựa vào gì?
Độ giãn và anisotropy ước lượng từ Jacobian, sai số mô hình camera, cùng tỷ lệ vùng giữ lại sau crop. Dựng bản nháp để đánh giá rồi chỉ xuất mô hình được chọn; không dựa vào dung lượng JPEG.
8. Vì sao ảnh 100 MP chưa chắc nét hơn?
Kích thước tự nhiên sau crop hình trụ trong báo cáo khoảng 5104 × 1295. Phóng lên mục tiêu 100 MP cần nội suy; số mẫu tăng không tạo ra thông tin chi tiết mới.
9. Crop kín có đồng nghĩa panorama hoàn hảo?
Không. Coverage kiểm tra dữ liệu tồn tại ở pixel đầu ra. Nó không chứng minh không có ghosting, sai màu hay lệch hình. Chất lượng vẫn cần đánh giá trực quan và đo thêm trên nhiều bộ dữ liệu.
10. Vì sao dùng ánh xạ ngược?
Mỗi pixel đích chủ động tìm mẫu trong ảnh nguồn, giúp tránh các khoảng bỏ sót do đẩy pixel nguồn sang đích. Nội suy song tuyến tính dùng bốn lân cận của tọa độ nguồn.
11. Đã đạt tỷ lệ thành công 80% chưa?
Tài liệu charter nêu đó là mục tiêu. Báo cáo hiện có chưa đủ thống kê nhiều bộ ảnh để kết luận đã đạt. Cần công bố bộ dữ liệu, định nghĩa thành công và số lượt thành công/thất bại.
12. Hướng cải thiện tiếp theo?
Mở rộng dữ liệu, định lượng chất lượng, xử lý chuyển động/parallax tốt hơn, thử multi-band blending và tối ưu bộ nhớ/tốc độ. Multi-band là hướng phát triển, không mô tả sai là thuật toán trộn hiện đang dùng.
NGUỒN THAM KHẢO KỸ THUẬT
Brown & Lowe, Automatic Panoramic Image Stitching using Invariant Features: https://mattabrown.github.io/pdf/ijcv2007.pdf
Szeliski, Image Alignment and Stitching: A Tutorial: https://www.microsoft.com/en-us/research/publication/image-alignment-and-stitching-a-tutorial/
Thiết kế cách kể: https://toastmasters.org/resources/public-speaking-tips/How-to-Write-and-Deliver-a-Speech
Workflow tham khảo: https://github.com/meiiie/meiiie_skillls/tree/main/motion-pptx-studio và https://github.com/hugohe3/ppt-master. Công cụ authoring chính: @oai/artifact-tool. Video minh họa: ManimGX và Anatomy. Không có nhạc/giọng đọc tự động.
NGUỒN VÀ PHẠM VI
Mã nguồn chỉ đọc: panorama/features.py, homography.py, ordering.py, camera.py, projection.py, rendering.py, seams.py, cropping.py, kernels.py; README.md. Thư mục dự án: C:/Users/Laptop/Downloads/panorama_stitching_source/panorama_stitching. Ảnh kết bài được dựng lại ở 2 MP để minh họa; không dùng làm bằng chứng thời gian xuất 100 MP.
```


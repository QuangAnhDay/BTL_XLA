import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# Output path
output_pptx = "ASL_Preprocessing_CNN_Evaluation.pptx"

# Initialize presentation
prs = Presentation()
prs.slide_width = Pt(960)
prs.slide_height = Pt(540)

# Color Palette Constants (Exact from DESIGN_GUIDE.md)
NAVY = RGBColor(0x13, 0x2E, 0x57)       # Primary Text & Titles (#132E57)
ROYAL_BLUE = RGBColor(0x16, 0x5D, 0xDE) # Accent Brand, Badges, Highlights (#165DDE)
SLATE = RGBColor(0x52, 0x69, 0x85)      # Subtitles, Meta, Captions, Numbers (#526985)
CYAN = RGBColor(0x23, 0xA8, 0xCE)       # Vector Inliers, Success (#23A8CE)
AMBER = RGBColor(0xB7, 0x6A, 0x12)      # Vector Outliers, Warnings (#B76A12)
ICE_BLUE = RGBColor(0xEA, 0xF2, 0xFF)   # Active Card Background (#EAF2FF)
SOFT_BG = RGBColor(0xF3, 0xF7, 0xFC)    # Secondary Card Background (#F3F7FC)
HAIRLINE = RGBColor(0xD8, 0xE4, 0xF2)   # Dividers, Borders (#D8E4F2)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)      # Background, White text (#FFFFFF)

blank_layout = prs.slide_layouts[6]

def set_slide_background_white(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = WHITE

def add_header(slide, title_text, subtitle_text=None, page_num=None):
    """Adds the standard header and page number matching DESIGN_GUIDE.md."""
    # 1. Kicker bar
    kicker = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Pt(48.0), Pt(33.0), Pt(27.0), Pt(3.75))
    kicker.fill.solid()
    kicker.fill.fore_color.rgb = ROYAL_BLUE
    kicker.line.fill.background()

    # 2. Title
    title_box = slide.shapes.add_textbox(Pt(48.0), Pt(46.0), Pt(864.0), Pt(46.0))
    tf = title_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = "Segoe UI"
    p.font.size = Pt(28.0)
    p.font.bold = True
    p.font.color.rgb = NAVY

    # 3. Subtitle (if present)
    if subtitle_text:
        sub_box = slide.shapes.add_textbox(Pt(48.0), Pt(96.0), Pt(864.0), Pt(30.0))
        stf = sub_box.text_frame
        stf.word_wrap = True
        stf.margin_left = stf.margin_top = stf.margin_right = stf.margin_bottom = 0
        sp = stf.paragraphs[0]
        sp.text = subtitle_text
        sp.font.name = "Segoe UI"
        sp.font.size = Pt(15.0)
        sp.font.bold = False
        sp.font.color.rgb = SLATE

    # 4. Page Number
    if page_num is not None:
        p_box = slide.shapes.add_textbox(Pt(892.5), Pt(510.0), Pt(25.0), Pt(18.0))
        ptf = p_box.text_frame
        ptf.margin_left = ptf.margin_top = ptf.margin_right = ptf.margin_bottom = 0
        pp = ptf.paragraphs[0]
        pp.text = f"{page_num:02d}"
        pp.font.name = "Segoe UI"
        pp.font.size = Pt(11.25)
        pp.font.color.rgb = SLATE

def add_card(slide, left, top, width, height, bg_color=None, border_color=None, border_width=1.0):
    card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Pt(left), Pt(top), Pt(width), Pt(height))
    if bg_color:
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
    else:
        card.fill.background()
        
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(border_width)
    else:
        card.line.fill.background()
    return card

def add_badge(slide, left, top, size, text, bg_color=ROYAL_BLUE, text_color=WHITE, font_size=11.25):
    badge = slide.shapes.add_shape(MSO_SHAPE.OVAL, Pt(left), Pt(top), Pt(size), Pt(size))
    badge.fill.solid()
    badge.fill.fore_color.rgb = bg_color
    badge.line.fill.background()
    tf = badge.text_frame
    tf.word_wrap = False
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = str(text)
    p.alignment = PP_ALIGN.CENTER
    p.font.name = "Segoe UI"
    p.font.size = Pt(font_size)
    p.font.bold = True
    p.font.color.rgb = text_color
    return badge

def add_notes(slide, duration_sec, time_range, script_text, staging_text, scope_text, backup_qa=None):
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    full_text = (
        f"THỜI LƯỢNG: {duration_sec} giây. Mốc dự kiến {time_range}. Tổng bài nói 9 phút 40 giây; dành ~5 phút cho vấn đáp.\n"
        f"LỜI TRÌNH BÀY\n{script_text}\n"
        f"ĐIỀU KHIỂN / DỰ PHÒNG\n{staging_text}\n"
        f"NGUỒN VÀ PHẠM VI\n{scope_text}"
    )
    if backup_qa:
        full_text += f"\nPHẦN VẤN ĐÁP DỰ PHÒNG — KHÔNG ĐỌC TRONG BÀI NÓI\n{backup_qa}"
    tf.text = full_text

print("Refining and building 10 slides...")

# ==============================================================================
# SLIDE 01: HERO COVER
# ==============================================================================
s1 = prs.slides.add_slide(blank_layout)
set_slide_background_white(s1)

k1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Pt(48.0), Pt(33.0), Pt(27.0), Pt(3.75))
k1.fill.solid()
k1.fill.fore_color.rgb = ROYAL_BLUE
k1.line.fill.background()

t_box = s1.shapes.add_textbox(Pt(48.0), Pt(46.0), Pt(864.0), Pt(90.0))
tf = t_box.text_frame
tf.word_wrap = True
tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

p1 = tf.paragraphs[0]
p1.text = "ĐÁNH GIÁ TÁC ĐỘNG CỦA TIỀN XỬ LÝ ẢNH"
p1.font.name = "Segoe UI"
p1.font.size = Pt(31.5)
p1.font.bold = True
p1.font.color.rgb = NAVY

p2 = tf.add_paragraph()
p2.text = "ĐẾN NHẬN DIỆN KÝ HIỆU ASL BẰNG CNN"
p2.font.name = "Segoe UI"
p2.font.size = Pt(31.5)
p2.font.bold = True
p2.font.color.rgb = ROYAL_BLUE

sub_box1 = s1.shapes.add_textbox(Pt(48.0), Pt(142.0), Pt(864.0), Pt(32.0))
stf = sub_box1.text_frame
stf.word_wrap = True
stf.margin_left = stf.margin_top = stf.margin_right = stf.margin_bottom = 0
sp = stf.paragraphs[0]
sp.text = "So sánh ảnh gốc, Contrast Stretching và Histogram Equalization trên mô hình đã huấn luyện"
sp.font.name = "Segoe UI"
sp.font.size = Pt(17.0)
sp.font.color.rgb = NAVY

if os.path.exists("assets/hero_banner.png"):
    s1.shapes.add_picture("assets/hero_banner.png", Pt(48.0), Pt(185.0), Pt(864.0), Pt(225.0))

meta_l = s1.shapes.add_textbox(Pt(48.0), Pt(445.0), Pt(400.0), Pt(50.0))
ml_tf = meta_l.text_frame
ml_tf.margin_left = ml_tf.margin_top = ml_tf.margin_right = ml_tf.margin_bottom = 0
lp1 = ml_tf.paragraphs[0]
lp1.text = "MÔN HỌC"
lp1.font.name = "Segoe UI"
lp1.font.size = Pt(12.0)
lp1.font.color.rgb = SLATE
lp2 = ml_tf.add_paragraph()
lp2.text = "Xử lý ảnh & Trí tuệ nhân tạo"
lp2.font.name = "Segoe UI"
lp2.font.size = Pt(15.0)
lp2.font.bold = True
lp2.font.color.rgb = NAVY

meta_r = s1.shapes.add_textbox(Pt(520.0), Pt(445.0), Pt(390.0), Pt(50.0))
mr_tf = meta_r.text_frame
mr_tf.margin_left = mr_tf.margin_top = mr_tf.margin_right = mr_tf.margin_bottom = 0
rp1 = mr_tf.paragraphs[0]
rp1.text = "BÁO CÁO THỰC NGHIỆM"
rp1.font.name = "Segoe UI"
rp1.font.size = Pt(12.0)
rp1.font.color.rgb = SLATE
rp2 = mr_tf.add_paragraph()
rp2.text = "Tập 25 ảnh ASL (A–Y) | Model: asl_classifier.keras"
rp2.font.name = "Segoe UI"
rp2.font.size = Pt(15.0)
rp2.font.bold = True
rp2.font.color.rgb = NAVY

p_box = s1.shapes.add_textbox(Pt(892.5), Pt(510.0), Pt(25.0), Pt(18.0))
ptf = p_box.text_frame
ptf.margin_left = ptf.margin_top = ptf.margin_right = ptf.margin_bottom = 0
pp = ptf.paragraphs[0]
pp.text = "01"
pp.font.name = "Segoe UI"
pp.font.size = Pt(11.25)
pp.font.color.rgb = SLATE

add_notes(
    s1, 30, "0:00–0:30",
    "Kính chào thầy cô và các bạn. Trong thị giác máy tính, tiền xử lý ảnh như tăng độ tương phản thường được mặc định coi là bước có lợi để làm ảnh rõ nét hơn. Tuy nhiên, khi đưa vào các mô hình Deep Learning đã được huấn luyện sẵn, việc thay đổi phân phối cường độ sáng có thực sự giúp tăng độ chính xác hay ngược lại? Nhóm em xin trình bày đề tài đánh giá thực nghiệm tác động của Contrast Stretching và Histogram Equalization đến mô hình CNN nhận diện ký hiệu bàn tay ASL.",
    "Dừng 2 giây để người nghe quan sát dải ảnh 3 trạng thái của ký hiệu ASL. Giọng trình bày tự tin, rõ ràng.",
    "Báo cáo dựa trên thực nghiệm kiểm thử 25 ảnh ký hiệu ASL A–Y với mô hình CNN asl_classifier.keras."
)

# ==============================================================================
# SLIDE 02: PROBLEM FRAMING & RESEARCH QUESTION
# ==============================================================================
s2 = prs.slides.add_slide(blank_layout)
set_slide_background_white(s2)
add_header(s2, "Cải thiện thị giác liệu có cải thiện độ chính xác?", 
           "Nghịch lý giữa khả năng quan sát của mắt người và phân phối đặc trưng mà mạng CNN đã học", 2)

card_w = 272.0
card_gap = 24.0
card_top = 145.0
card_h = 135.0

challenges = [
    ("01", "Tăng cường thị giác", "Tiền xử lý thường được áp dụng với giả định làm ảnh rõ nét, tăng độ tương phản cục bộ để mắt người dễ quan sát hơn."),
    ("02", "Lệch phân phối (Shift)", "Mô hình CNN được tối ưu trên phân phối ảnh huấn luyện ban đầu. Biến đổi độ sáng làm dịch chuyển phân phối pixel đầu vào."),
    ("03", "Nghịch lý trực quan", "Ảnh trông rõ nét hơn đối với mắt người không đồng nghĩa với việc mạng CNN sẽ trích xuất đặc trưng chính xác hơn.")
]

for i, (badge_num, head, desc) in enumerate(challenges):
    c_left = 48.0 + i * (card_w + card_gap)
    add_card(s2, c_left, card_top, card_w, card_h, bg_color=SOFT_BG, border_color=HAIRLINE)
    add_badge(s2, c_left + 16.0, card_top + 16.0, 24.0, badge_num, ROYAL_BLUE, WHITE, 11.0)
    
    tb = s2.shapes.add_textbox(Pt(c_left + 48.0), Pt(card_top + 16.0), Pt(card_w - 60.0), Pt(24.0))
    tbf = tb.text_frame
    tbf.word_wrap = True
    tbf.margin_left = tbf.margin_top = tbf.margin_right = tbf.margin_bottom = 0
    p = tbf.paragraphs[0]
    p.text = head
    p.font.name = "Segoe UI"
    p.font.size = Pt(14.0)
    p.font.bold = True
    p.font.color.rgb = NAVY
    
    tb_desc = s2.shapes.add_textbox(Pt(c_left + 16.0), Pt(card_top + 48.0), Pt(card_w - 32.0), Pt(75.0))
    tdf = tb_desc.text_frame
    tdf.word_wrap = True
    tdf.margin_left = tdf.margin_top = tdf.margin_right = tdf.margin_bottom = 0
    p2 = tdf.paragraphs[0]
    p2.text = desc
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(12.5)
    p2.font.color.rgb = SLATE

# Research Question Hero Card
q_box = add_card(s2, 48.0, 300.0, 864.0, 88.0, bg_color=ICE_BLUE, border_color=ROYAL_BLUE, border_width=1.5)
q_tb = s2.shapes.add_textbox(Pt(68.0), Pt(310.0), Pt(824.0), Pt(70.0))
qtf = q_tb.text_frame
qtf.word_wrap = True
qtf.margin_left = qtf.margin_top = qtf.margin_right = qtf.margin_bottom = 0

qp1 = qtf.paragraphs[0]
qp1.text = "CÂU HỎI NGHIÊN CỨU TRỌNG TÂM"
qp1.font.name = "Segoe UI"
qp1.font.size = Pt(12.0)
qp1.font.bold = True
qp1.font.color.rgb = ROYAL_BLUE

qp2 = qtf.add_paragraph()
qp2.text = "Contrast Stretching và Histogram Equalization ảnh hưởng như thế nào đến độ chính xác và phân phối xác suất Softmax của một CNN đã huấn luyện?"
qp2.font.name = "Segoe UI"
qp2.font.size = Pt(16.5)
qp2.font.bold = True
qp2.font.color.rgb = NAVY

# Bottom 3 Experimental Conditions
c_box = add_card(s2, 48.0, 408.0, 864.0, 75.0, bg_color=WHITE, border_color=HAIRLINE)
cond_tb = s2.shapes.add_textbox(Pt(68.0), Pt(416.0), Pt(824.0), Pt(60.0))
ctf = cond_tb.text_frame
ctf.word_wrap = True
ctf.margin_left = ctf.margin_top = ctf.margin_right = ctf.margin_bottom = 0

cp1 = ctf.paragraphs[0]
cp1.text = "BA TRƯỜNG HỢP SO SÁNH TRỰC DIỆN:"
cp1.font.name = "Segoe UI"
cp1.font.size = Pt(11.5)
cp1.font.bold = True
cp1.font.color.rgb = SLATE

cp2 = ctf.add_paragraph()
r1 = cp2.add_run()
r1.text = "1. Ảnh gốc (Baseline): "
r1.font.bold = True
r1.font.color.rgb = NAVY
r1_sub = cp2.add_run()
r1_sub.text = "Đối chứng nguyên bản.   "
r1_sub.font.color.rgb = SLATE

r2 = cp2.add_run()
r2.text = "2. Contrast Stretching: "
r2.font.bold = True
r2.font.color.rgb = ROYAL_BLUE
r2_sub = cp2.add_run()
r2_sub.text = "Kéo giãn tuyến tính P1–P99 kênh Y.   "
r2_sub.font.color.rgb = SLATE

r3 = cp2.add_run()
r3.text = "3. Histogram Equalization: "
r3.font.bold = True
r3.font.color.rgb = AMBER
r3_sub = cp2.add_run()
r3_sub.text = "Cân bằng tích lũy CDF kênh Y."
r3_sub.font.color.rgb = SLATE

add_notes(
    s2, 45, "0:30–1:15",
    "Trong thực tế, khi đối mặt với ảnh chụp thiếu sáng hoặc mờ, phản xạ tự nhiên của kỹ sư xử lý ảnh là áp dụng các bộ lọc tăng tương phản. Tuy nhiên, mạng nơ-ron tích chập (CNN) hoạt động dựa trên các bộ lọc không gian học được từ một phân phối cường độ sáng cụ thể. Khi chúng ta thay đổi lược đồ mức xám, chúng ta vô tình gây ra hiện tượng dịch chuyển phân phối đầu vào. Câu hỏi đặt ra là: Liệu một bức ảnh trông rõ nét hơn với con người có thực sự giúp mạng CNN phân loại đúng hơn không?",
    "Nhấn mạnh vào câu hỏi nghiên cứu ở khung màu xanh. Nêu rõ ba trường hợp thực nghiệm sẽ so sánh xuyên suốt bài báo cáo.",
    "Lý thuyết Covariate Shift (Shimodaira, 2000). Ba trường hợp đối chứng được thực hiện trên cùng tập 25 ảnh."
)

# ==============================================================================
# SLIDE 03: TESTING DATA & CNN ARCHITECTURE
# ==============================================================================
s3 = prs.slides.add_slide(blank_layout)
set_slide_background_white(s3)
add_header(s3, "Dữ liệu kiểm thử và kiến trúc mô hình CNN", 
           "Đánh giá khách quan tác động của tiền xử lý khi cấu trúc và trọng số mạng được cố định tuyệt đối", 3)

add_card(s3, 48.0, 142.0, 420.0, 95.0, bg_color=SOFT_BG, border_color=HAIRLINE)
d_tb = s3.shapes.add_textbox(Pt(64.0), Pt(152.0), Pt(390.0), Pt(75.0))
dtf = d_tb.text_frame
dtf.word_wrap = True
dtf.margin_left = dtf.margin_top = dtf.margin_right = dtf.margin_bottom = 0
dp1 = dtf.paragraphs[0]
dp1.text = "TẬP DỮ LIỆU KIỂM THỬ THỰC NGHIỆM"
dp1.font.name = "Segoe UI"
dp1.font.size = Pt(12.0)
dp1.font.bold = True
dp1.font.color.rgb = ROYAL_BLUE
dp2 = dtf.add_paragraph()
dp2.text = "• 25 ảnh ký hiệu bàn tay ASL tương ứng 25 chữ cái A–Y.\n• Định dạng: RGB, kích thước chuẩn hóa 100 × 100 pixel.\n• Cùng một tập ảnh nguồn được dùng cho cả 3 nhánh thử nghiệm."
dp2.font.name = "Segoe UI"
dp2.font.size = Pt(12.0)
dp2.font.color.rgb = NAVY

add_card(s3, 492.0, 142.0, 420.0, 95.0, bg_color=SOFT_BG, border_color=HAIRLINE)
m_tb = s3.shapes.add_textbox(Pt(508.0), Pt(152.0), Pt(390.0), Pt(75.0))
mtf = m_tb.text_frame
mtf.word_wrap = True
mtf.margin_left = mtf.margin_top = mtf.margin_right = mtf.margin_bottom = 0
mp1 = mtf.paragraphs[0]
mp1.text = "MÔ HÌNH THỰC NGHIỆM: asl_classifier.keras"
mp1.font.name = "Segoe UI"
mp1.font.size = Pt(12.0)
mp1.font.bold = True
mp1.font.color.rgb = NAVY
mp2 = mtf.add_paragraph()
mp2.text = "• Trọng số gốc được đóng băng hoàn toàn; mã SHA-256 cố định.\n• Đầu vào yêu cầu: Tensor chuẩn hóa [0, 1] kích thước (100, 100, 3).\n• Đầu ra phân loại: 29 lớp ký tự (26 chữ cái + ký hiệu phụ) qua Softmax."
mp2.font.name = "Segoe UI"
mp2.font.size = Pt(12.0)
mp2.font.color.rgb = SLATE

pipe_w = 160.0
pipe_gap = 16.0
pipe_top = 265.0
pipe_h = 175.0

conn_line = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Pt(60.0), Pt(pipe_top + 14.0), Pt(840.0), Pt(2.0))
conn_line.fill.solid()
conn_line.fill.fore_color.rgb = HAIRLINE
conn_line.line.fill.background()

stages = [
    ("01", "Input & Scale", "(100, 100, 3)", "Chuẩn hóa pixel về đoạn [0, 1] trước khi đưa vào mạng"),
    ("02", "Conv Block 1", "64 filters (3×3)", "ReLU activation kết hợp MaxPooling (2×2) giảm chiều"),
    ("03", "Conv Block 2", "64 filters (3×3)", "ReLU activation kết hợp MaxPooling (2×2) trích xuất sâu"),
    ("04", "Dense Layer", "128 units (ReLU)", "Flatten tạo 33.856 đặc trưng kết nối vào lớp Dense ẩn"),
    ("05", "Softmax Output", "29 classes", "Phân phối xác suất Softmax cho 29 lớp ký hiệu ngôn ngữ")
]

for i, (badge_num, title, param, note) in enumerate(stages):
    s_left = 48.0 + i * (pipe_w + pipe_gap)
    add_card(s3, s_left, pipe_top, pipe_w, pipe_h, bg_color=WHITE, border_color=HAIRLINE)
    add_badge(s3, s_left + 12.0, pipe_top + 8.0, 24.0, badge_num, ROYAL_BLUE, WHITE, 11.0)
    
    tb_stg = s3.shapes.add_textbox(Pt(s_left + 10.0), Pt(pipe_top + 38.0), Pt(pipe_w - 20.0), Pt(pipe_h - 45.0))
    stf = tb_stg.text_frame
    stf.word_wrap = True
    stf.margin_left = stf.margin_top = stf.margin_right = stf.margin_bottom = 0
    
    p = stf.paragraphs[0]
    p.text = title
    p.font.name = "Segoe UI"
    p.font.size = Pt(13.0)
    p.font.bold = True
    p.font.color.rgb = NAVY
    
    p_sub = stf.add_paragraph()
    p_sub.text = param
    p_sub.font.name = "Segoe UI"
    p_sub.font.size = Pt(11.5)
    p_sub.font.bold = True
    p_sub.font.color.rgb = ROYAL_BLUE
    
    p_note = stf.add_paragraph()
    p_note.text = note
    p_note.font.name = "Segoe UI"
    p_note.font.size = Pt(11.0)
    p_note.font.color.rgb = SLATE

disc_box = s3.shapes.add_textbox(Pt(48.0), Pt(465.0), Pt(864.0), Pt(30.0))
dtf = disc_box.text_frame
dtf.word_wrap = True
dtf.margin_left = dtf.margin_top = dtf.margin_right = dtf.margin_bottom = 0
dp = dtf.paragraphs[0]
dp.text = "Lưu ý khoa học: Trọng số mô hình được giữ cố định để cô lập hoàn toàn tác động của tiền xử lý. Chưa khẳng định tập 25 ảnh kiểm thử hoàn toàn độc lập với dữ liệu huấn luyện ban đầu do thiếu thông tin siêu dữ liệu nguồn."
dp.font.name = "Segoe UI"
dp.font.size = Pt(12.0)
dp.font.color.rgb = SLATE

add_notes(
    s3, 50, "1:15–2:05",
    "Để đảm bảo tính khoa học và khách quan, toàn bộ trọng số của mô hình asl_classifier.keras được giữ nguyên vẹn, kiểm tra bằng mã băm SHA-256 không thay đổi. Mô hình gồm hai khối tích chập 64 bộ lọc kích thước 3 nhân 3, tiếp nối bởi tầng Flatten với 33.856 chiều đặc trưng và tầng Dense 128 nơ-ron trước khi phân loại qua Softmax 29 lớp. Tập kiểm thử gồm 25 ký hiệu bàn tay chuẩn đại diện cho bảng chữ cái A đến Y. Mục tiêu là kiểm chứng xem khi mô hình đã học xong, tiền xử lý tác động như thế nào đến phản ứng của các tầng tích chập này.",
    "Chỉ vào sơ đồ pipeline 5 bước kiến trúc. Nhắc nhở người nghe rằng trọng số mạng không hề được tái huấn luyện trong suốt thử nghiệm.",
    "File mô hình: asl_classifier.keras. Dữ liệu: 25 ảnh kích thước 100x100x3 RGB. Không đưa ra nhận định vượt quá phạm vi kiểm thử."
)

# ==============================================================================
# SLIDE 04: METHOD 1 - CONTRAST STRETCHING
# ==============================================================================
s4 = prs.slides.add_slide(blank_layout)
set_slide_background_white(s4)
add_header(s4, "Phương pháp 1: Kéo giãn tương phản (Contrast Stretching)", 
           "Kéo giãn tuyến tính kênh độ sáng Y trong không gian màu YCrCb có cắt ngưỡng phân vị P1% và P99%", 4)

col_l = 48.0
col_w = 460.0

add_card(s4, col_l, 145.0, col_w, 105.0, bg_color=ICE_BLUE, border_color=ROYAL_BLUE, border_width=1.5)
f_tb = s4.shapes.add_textbox(Pt(col_l + 18.0), Pt(155.0), Pt(col_w - 36.0), Pt(85.0))
ftf = f_tb.text_frame
ftf.word_wrap = True
ftf.margin_left = ftf.margin_top = ftf.margin_right = ftf.margin_bottom = 0

fp1 = ftf.paragraphs[0]
fp1.text = "CÔNG THỨC ÁNH XẠ KÉO GIÃN TUYẾN TÍNH KÊNH Y"
fp1.font.name = "Segoe UI"
fp1.font.size = Pt(11.5)
fp1.font.bold = True
fp1.font.color.rgb = ROYAL_BLUE

fp2 = ftf.add_paragraph()
fp2.text = "s = clip( ((r − P1%) / (P99% − P1%)) × 255, 0, 255 )"
fp2.font.name = "Segoe UI"
fp2.font.size = Pt(18.0)
fp2.font.bold = True
fp2.font.color.rgb = NAVY

fp3 = ftf.add_paragraph()
fp3.text = "Trong đó: r là mức sáng đầu vào; P1% và P99% là ngưỡng phân vị 1% và 99%."
fp3.font.name = "Segoe UI"
fp3.font.size = Pt(11.5)
fp3.font.color.rgb = SLATE

principles = [
    ("Cắt ngưỡng phân vị (Percentile Clipping):", "Các giá trị cường độ < P1% được đưa về 0, > P99% đưa về 255 nhằm triệt tiêu các điểm nhiễu cực đại hoặc cực tiểu đơn lẻ."),
    ("Kéo giãn dải động tuyến tính:", "Khoảng cường độ giữa [P1%, P99%] được nhân phóng đại để trải rộng kín toàn bộ dải [0, 255], giúp tăng độ tương phản cục bộ."),
    ("Bảo toàn thông tin màu sắc:", "Chỉ can thiệp vào kênh độ sáng Y; hai kênh sắc độ Cr và Cb được giữ nguyên nhằm hạn chế hiện tượng sai lệch màu da tay.")
]

for i, (head, body) in enumerate(principles):
    y_pos = 265.0 + i * 62.0
    add_card(s4, col_l, y_pos, col_w, 54.0, bg_color=SOFT_BG, border_color=HAIRLINE)
    ptb = s4.shapes.add_textbox(Pt(col_l + 16.0), Pt(y_pos + 6.0), Pt(col_w - 32.0), Pt(42.0))
    ptf = ptb.text_frame
    ptf.word_wrap = True
    ptf.margin_left = ptf.margin_top = ptf.margin_right = ptf.margin_bottom = 0
    p = ptf.paragraphs[0]
    r_h = p.add_run()
    r_h.text = head + " "
    r_h.font.bold = True
    r_h.font.color.rgb = NAVY
    r_h.font.size = Pt(12.0)
    r_b = p.add_run()
    r_b.text = body
    r_b.font.color.rgb = SLATE
    r_b.font.size = Pt(11.5)

col_r = 532.0
col_rw = 380.0

add_card(s4, col_r, 145.0, col_rw, 290.0, bg_color=WHITE, border_color=HAIRLINE)
flow_tb = s4.shapes.add_textbox(Pt(col_r + 20.0), Pt(155.0), Pt(col_rw - 40.0), Pt(30.0))
fltf = flow_tb.text_frame
fltf.margin_left = fltf.margin_top = fltf.margin_right = fltf.margin_bottom = 0
flp = fltf.paragraphs[0]
flp.text = "QUY TRÌNH THỰC HIỆN 4 GIAI ĐOẠN"
flp.font.name = "Segoe UI"
flp.font.size = Pt(12.5)
flp.font.bold = True
flp.font.color.rgb = ROYAL_BLUE

steps = [
    ("1", "Ảnh gốc RGB", "Kích thước 100 × 100 pixel, dải mức xám tự nhiên"),
    ("2", "Chuyển sang YCrCb", "Tách riêng kênh độ sáng Y khỏi hai kênh màu Cr, Cb"),
    ("3", "Kéo giãn kênh Y", "Tính P1–P99, ánh xạ tuyến tính và clip về [0, 255]"),
    ("4", "Tái cấu trúc RGB", "Ghép Y đã xử lý với Cr, Cb gốc để đưa vào mạng CNN")
]

for i, (num, stitle, sdesc) in enumerate(steps):
    s_top = 195.0 + i * 55.0
    add_badge(s4, col_r + 20.0, s_top + 4.0, 24.0, num, ROYAL_BLUE, WHITE, 11.0)
    st_tb = s4.shapes.add_textbox(Pt(col_r + 55.0), Pt(s_top), Pt(col_rw - 75.0), Pt(45.0))
    sttf = st_tb.text_frame
    sttf.word_wrap = True
    sttf.margin_left = sttf.margin_top = sttf.margin_right = sttf.margin_bottom = 0
    p = sttf.paragraphs[0]
    p.text = stitle
    p.font.name = "Segoe UI"
    p.font.size = Pt(12.5)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p_desc = sttf.add_paragraph()
    p_desc.text = sdesc
    p_desc.font.name = "Segoe UI"
    p_desc.font.size = Pt(11.0)
    p_desc.font.color.rgb = SLATE

disc4 = s4.shapes.add_textbox(Pt(48.0), Pt(465.0), Pt(864.0), Pt(30.0))
d4_tf = disc4.text_frame
d4_tf.word_wrap = True
d4_tf.margin_left = d4_tf.margin_top = d4_tf.margin_right = d4_tf.margin_bottom = 0
dp4 = d4_tf.paragraphs[0]
dp4.text = "Lưu ý phương pháp: Contrast Stretching làm rõ chênh lệch sáng tối nhưng không đảm bảo loại bỏ hoàn toàn nhiễu và có thể làm phẳng các nếp nhăn nhỏ trên mu bàn tay nếu các điểm này rơi vào vùng clipping."
dp4.font.name = "Segoe UI"
dp4.font.size = Pt(12.0)
dp4.font.color.rgb = SLATE

add_notes(
    s4, 45, "2:05–2:50",
    "Phương pháp đầu tiên là Contrast Stretching. Để tránh làm biến đổi tông màu da của bàn tay, nhóm chuyển ảnh từ không gian màu RGB sang YCrCb và chỉ can thiệp vào kênh độ sáng Y. Thay vì dùng giá trị Min và Max tuyệt đối vốn rất nhạy cảm với các điểm ảnh nhiễu, thuật toán sử dụng ngưỡng phân vị 1% và 99%. Công thức ánh xạ tuyến tính đưa các giá trị dưới P1% về 0, trên P99% về 255 và kéo giãn dải ở giữa. Về mặt thị giác, bức ảnh trở nên trong trẻo và tương phản rõ ràng hơn.",
    "Chỉ vào công thức ánh xạ và sơ đồ quy trình 4 bước bên phải. Giải thích vì sao cần giữ nguyên hai kênh màu Cr và Cb.",
    "Mã nguồn triển khai: percentile clipping tại p=1 và p=99 trên numpy mảng 2 chiều. Chuyển đổi màu sử dụng chuẩn YCrCb tiêu chuẩn."
)

# ==============================================================================
# SLIDE 05: METHOD 2 - HISTOGRAM EQUALIZATION (Refined Equations)
# ==============================================================================
s5 = prs.slides.add_slide(blank_layout)
set_slide_background_white(s5)
add_header(s5, "Phương pháp 2: Cân bằng lược đồ (Histogram Equalization)", 
           "Tái phân bố các mức cường độ kênh Y dựa trên hàm phân phối tích lũy xác suất (CDF)", 5)

col5_l = 48.0
col5_w = 430.0

add_card(s5, col5_l, 145.0, col5_w, 105.0, bg_color=ICE_BLUE, border_color=ROYAL_BLUE, border_width=1.5)
f5_tb = s5.shapes.add_textbox(Pt(col5_l + 18.0), Pt(153.0), Pt(col5_w - 36.0), Pt(90.0))
f5_tf = f5_tb.text_frame
f5_tf.word_wrap = True
f5_tf.margin_left = f5_tf.margin_top = f5_tf.margin_right = f5_tf.margin_bottom = 0

p = f5_tf.paragraphs[0]
p.text = "CÔNG THỨC XÁC SUẤT VÀ ÁNH XẠ TÍCH LŨY (CDF)"
p.font.name = "Segoe UI"
p.font.size = Pt(11.5)
p.font.bold = True
p.font.color.rgb = ROYAL_BLUE

p_eq1 = f5_tf.add_paragraph()
p_eq1.text = "p_r(r_k) = n_k / N      (Xác suất mức xám k)"
p_eq1.font.name = "Segoe UI"
p_eq1.font.size = Pt(14.0)
p_eq1.font.bold = True
p_eq1.font.color.rgb = NAVY

p_eq2 = f5_tf.add_paragraph()
p_eq2.text = "s_k = ((L − 1) / N) × Σ_{j=0}^k n_j      (Ánh xạ CDF)"
p_eq2.font.name = "Segoe UI"
p_eq2.font.size = Pt(14.0)
p_eq2.font.bold = True
p_eq2.font.color.rgb = NAVY

p_sub = f5_tf.add_paragraph()
p_sub.text = "n_k: số pixel mức k; N = 10.000 pixel tổng (100×100); L = 256 mức xám."
p_sub.font.name = "Segoe UI"
p_sub.font.size = Pt(10.5)
p_sub.font.color.rgb = SLATE

add_card(s5, col5_l, 260.0, col5_w, 175.0, bg_color=SOFT_BG, border_color=HAIRLINE)
exp_tb = s5.shapes.add_textbox(Pt(col5_l + 18.0), Pt(270.0), Pt(col5_w - 36.0), Pt(155.0))
etf = exp_tb.text_frame
etf.word_wrap = True
etf.margin_left = etf.margin_top = etf.margin_right = etf.margin_bottom = 0

ep1 = etf.paragraphs[0]
ep1.text = "CƠ CHẾ TÁC ĐỘNG CỦA CÂN BẰNG LƯỢC ĐỒ:"
ep1.font.name = "Segoe UI"
ep1.font.size = Pt(12.0)
ep1.font.bold = True
ep1.font.color.rgb = NAVY

items5 = [
    ("San phẳng lược đồ mức xám: ", "Chuyển đổi lược đồ cường độ tập trung hẹp thành phân phối đều xấp xỉ trên toàn dải [0, 255]."),
    ("Tăng cường tương phản toàn cục: ", "Khuếch đại độ tương phản tại các vùng có mật độ pixel cao, làm nổi bật cấu trúc chính."),
    ("Tác dụng phụ đối với đặc trưng: ", "Có thể làm sáng quá mức các vùng tối tự nhiên, triệt tiêu bóng đổ giữa các ngón tay và khuếch đại nhiễu nền.")
]

for head, body in items5:
    ep = etf.add_paragraph()
    rh = ep.add_run()
    rh.text = "• " + head
    rh.font.bold = True
    rh.font.color.rgb = ROYAL_BLUE
    rh.font.size = Pt(11.5)
    rb = ep.add_run()
    rb.text = body
    rb.font.color.rgb = SLATE
    rb.font.size = Pt(11.0)

col5_r = 502.0
col5_rw = 410.0

if os.path.exists("assets/hist_concept.png"):
    s5.shapes.add_picture("assets/hist_concept.png", Pt(col5_r), Pt(155.0), Pt(col5_rw), Pt(245.0))

cpt5 = s5.shapes.add_textbox(Pt(col5_r), Pt(405.0), Pt(col5_rw), Pt(35.0))
cpt5_tf = cpt5.text_frame
cpt5_tf.word_wrap = True
cpt5_tf.margin_left = cpt5_tf.margin_top = cpt5_tf.margin_right = cpt5_tf.margin_bottom = 0
cp = cpt5_tf.paragraphs[0]
cp.text = "Biểu đồ minh họa khái niệm: Lược đồ ban đầu bị nén hẹp ở mức xám trung bình được trải đều tuyến tính hóa sau khi biến đổi bằng hàm CDF."
cp.font.name = "Segoe UI"
cp.font.size = Pt(11.0)
cp.font.color.rgb = SLATE

disc5 = s5.shapes.add_textbox(Pt(48.0), Pt(465.0), Pt(864.0), Pt(30.0))
d5_tf = disc5.text_frame
d5_tf.word_wrap = True
d5_tf.margin_left = d5_tf.margin_top = d5_tf.margin_right = d5_tf.margin_bottom = 0
dp5 = d5_tf.paragraphs[0]
dp5.text = "Ghi chú: Biểu đồ phân phối trên là hình minh họa khái niệm cho nguyên lý san phẳng lược đồ, không phải biểu đồ thực nghiệm trích xuất từ từng pixel của 25 ảnh."
dp5.font.name = "Segoe UI"
dp5.font.size = Pt(12.0)
dp5.font.color.rgb = SLATE

add_notes(
    s5, 45, "2:50–3:35",
    "Phương pháp thứ hai là Histogram Equalization. Thay vì kéo giãn tuyến tính, thuật toán tính toán hàm phân phối tích lũy (CDF) của kênh độ sáng Y và dùng nó làm hàm ánh xạ. Các mức xám xuất hiện nhiều sẽ được trải rộng ra, giúp cực đại hóa entropy thông tin của ảnh. Tuy nhiên, trong nhận diện cử chỉ bàn tay, bóng đổ giữa các ngón tay và nếp nhăn ở khớp ngón là các tín hiệu biên rất quan trọng. Khi lược đồ bị san phẳng mạnh mẽ, các vùng bóng tối tự nhiên có thể bị làm sáng quá mức, dẫn đến mất mát các đặc trưng hình học tinh tế.",
    "Chỉ vào biểu đồ phân phối trước và sau cân bằng. Nhấn mạnh việc san phẳng mức xám có thể gây hại cho các đặc trưng biên cục bộ.",
    "Triển khai thuật toán: cv2.equalizeHist trên kênh Y. Biểu đồ trên slide mang tính minh họa nguyên lý toán học."
)

# ==============================================================================
# SLIDE 06: EXPERIMENTAL RESULTS OVERVIEW (Refined 2-Line KPI Metrics)
# ==============================================================================
s6 = prs.slides.add_slide(blank_layout)
set_slide_background_white(s6)
add_header(s6, "Kết quả thực nghiệm tổng quan: Độ chính xác và Tốc độ", 
           "Trong tập kiểm thử 25 ảnh ASL, cả hai phương pháp tăng cường tương phản đều cho kết quả thấp hơn ảnh gốc", 6)

kpi_w = 272.0
kpi_gap = 24.0
kpi_top = 142.0
kpi_h = 100.0

kpis = [
    ("Ảnh gốc (Baseline)", "100%", "25 / 25 ảnh chính xác  •  Độ tự tin: 99,06%", "Thời gian tiền xử lý: 0,24 ms / ảnh", ROYAL_BLUE),
    ("Contrast Stretching", "88%", "22 / 25 ảnh (giảm 12%)  •  Độ tự tin: 93,03%", "Thời gian tiền xử lý: 0,81 ms / ảnh", SLATE),
    ("Histogram Equalization", "68%", "17 / 25 ảnh (giảm 32%)  •  Độ tự tin: 78,90%", "Thời gian tiền xử lý: 0,41 ms / ảnh", AMBER)
]

for i, (m_name, acc, line1, line2, clr) in enumerate(kpis):
    kx = 48.0 + i * (kpi_w + kpi_gap)
    add_card(s6, kx, kpi_top, kpi_w, kpi_h, bg_color=SOFT_BG, border_color=clr if clr != SLATE else HAIRLINE, border_width=1.5)
    
    ktb = s6.shapes.add_textbox(Pt(kx + 16.0), Pt(kpi_top + 8.0), Pt(kpi_w - 32.0), Pt(kpi_h - 16.0))
    ktf = ktb.text_frame
    ktf.word_wrap = True
    ktf.margin_left = ktf.margin_top = ktf.margin_right = ktf.margin_bottom = 0
    
    p_title = ktf.paragraphs[0]
    p_title.text = m_name
    p_title.font.name = "Segoe UI"
    p_title.font.size = Pt(12.0)
    p_title.font.bold = True
    p_title.font.color.rgb = NAVY
    
    p_acc = ktf.add_paragraph()
    p_acc.text = acc
    p_acc.font.name = "Segoe UI"
    p_acc.font.size = Pt(36.0)
    p_acc.font.bold = True
    p_acc.font.color.rgb = clr
    
    p_l1 = ktf.add_paragraph()
    p_l1.text = line1
    p_l1.font.name = "Segoe UI"
    p_l1.font.size = Pt(10.0)
    p_l1.font.color.rgb = SLATE
    
    p_l2 = ktf.add_paragraph()
    p_l2.text = line2
    p_l2.font.name = "Segoe UI"
    p_l2.font.size = Pt(10.0)
    p_l2.font.color.rgb = SLATE

if os.path.exists("assets/accuracy_chart.png"):
    s6.shapes.add_picture("assets/accuracy_chart.png", Pt(48.0), Pt(255.0), Pt(380.0), Pt(195.0))

add_card(s6, 452.0, 255.0, 460.0, 195.0, bg_color=ICE_BLUE, border_color=ROYAL_BLUE, border_width=1.5)
cf_tb = s6.shapes.add_textbox(Pt(472.0), Pt(265.0), Pt(420.0), Pt(175.0))
ctf = cf_tb.text_frame
ctf.word_wrap = True
ctf.margin_left = ctf.margin_top = ctf.margin_right = ctf.margin_bottom = 0

cp = ctf.paragraphs[0]
cp.text = "PHÁT HIỆN THỰC NGHIỆM THEN CHỐT"
cp.font.name = "Segoe UI"
cp.font.size = Pt(13.0)
cp.font.bold = True
cp.font.color.rgb = ROYAL_BLUE

points6 = [
    ("Suy giảm độ chính xác rõ rệt: ", "Cả hai kỹ thuật tiền xử lý đều làm giảm hiệu suất so với ảnh gốc (100% → 88% → 68%). Cân bằng lược đồ gây thiệt hại nặng nề nhất."),
    ("Sụt giảm độ tự tin (Confidence): ", "Độ tự tin trung bình giảm từ 99,06% xuống 93,03% ở Contrast Stretching và rơi mạnh xuống 78,90% ở Histogram Equalization."),
    ("Độ trễ tính toán tăng thêm: ", "Contrast Stretching tốn 0,81 ms/ảnh (gấp 3,38 lần ảnh gốc 0,24 ms) do phép tính phân vị P1/P99; Histogram Equalization tốn 0,41 ms/ảnh.")
]

for head, body in points6:
    p_pt = ctf.add_paragraph()
    rh = p_pt.add_run()
    rh.text = "• " + head
    rh.font.bold = True
    rh.font.color.rgb = NAVY
    rh.font.size = Pt(11.5)
    rb = p_pt.add_run()
    rb.text = body
    rb.font.color.rgb = SLATE
    rb.font.size = Pt(11.0)

disc6 = s6.shapes.add_textbox(Pt(48.0), Pt(465.0), Pt(864.0), Pt(30.0))
d6_tf = disc6.text_frame
d6_tf.word_wrap = True
d6_tf.margin_left = d6_tf.margin_top = d6_tf.margin_right = d6_tf.margin_bottom = 0
dp6 = d6_tf.paragraphs[0]
dp6.text = "Lưu ý khoa học: Kết quả đo đạc chính xác trên tập kiểm thử 25 ảnh đã cung cấp. Không khái quát hóa thành kết luận rằng tiền xử lý luôn làm giảm độ chính xác trên mọi tập dữ liệu hoặc kiến trúc CNN khác."
dp6.font.name = "Segoe UI"
dp6.font.size = Pt(12.0)
dp6.font.color.rgb = SLATE

add_notes(
    s6, 50, "3:35–4:25",
    "Đây là kết quả thực nghiệm trung tâm của bài báo cáo. Bảng số liệu cho thấy một sự tương phản rất rõ rệt: Trên tập kiểm thử 25 ảnh, ảnh gốc ban đầu đạt độ chính xác tuyệt đối 100% với confidence trung bình lên tới 99,06%. Khi áp dụng Contrast Stretching, độ chính xác giảm xuống 88% với 3 ảnh bị dự đoán sai. Đáng ngạc nhiên hơn, Histogram Equalization – phương pháp vốn tạo ra ảnh có tương phản thị giác rất mạnh – lại khiến độ chính xác sụt giảm nghiêm trọng xuống còn 68%, tức sai tới 8 trên 25 ảnh. Bên cạnh đó, thời gian xử lý cũng tăng từ 0,24 ms lên 0,81 ms.",
    "Chỉ vào 3 thẻ số liệu lớn phía trên và biểu đồ cột so sánh. Nhấn mạnh rằng mức giảm 32% của Histogram Equalization là rất lớn.",
    "Báo cáo kết quả kiểm thử: Ảnh gốc 25/25, CS 22/25, HE 17/25. Thời gian đo lường bằng millisecond trên cùng phần cứng."
)

# ==============================================================================
# SLIDE 07: COVARIATE SHIFT ANALYSIS
# ==============================================================================
s7 = prs.slides.add_slide(blank_layout)
set_slide_background_white(s7)
add_header(s7, "Phân tích hiện tượng Covariate Shift trong thị giác máy tính", 
           "Sự sai lệch giữa phân phối dữ liệu huấn luyện P_train(X) và dữ liệu kiểm thử P_test(X)", 7)

add_card(s7, 48.0, 142.0, 864.0, 68.0, bg_color=SOFT_BG, border_color=HAIRLINE)
def_tb = s7.shapes.add_textbox(Pt(68.0), Pt(148.0), Pt(824.0), Pt(55.0))
dtf = def_tb.text_frame
dtf.word_wrap = True
dtf.margin_left = dtf.margin_top = dtf.margin_right = dtf.margin_bottom = 0

dp1 = dtf.paragraphs[0]
dp1.text = "BẢN CHẤT TOÁN HỌC CỦA COVARIATE SHIFT"
dp1.font.name = "Segoe UI"
dp1.font.size = Pt(11.5)
dp1.font.bold = True
dp1.font.color.rgb = ROYAL_BLUE

dp2 = dtf.add_paragraph()
dp2.text = "Hiện tượng Covariate Shift xảy ra khi phân phối biên của đầu vào thay đổi: P_test(X) ≠ P_train(X), trong khi phân phối điều kiện P(Y | X) giả định giữ nguyên. Mạng CNN đã tối ưu các bộ lọc trọng số W theo P_train(X); do đó khi P_test(X) bị biến dạng do tiền xử lý, phản ứng tại các tầng tích chập không còn tối ưu."
dp2.font.name = "Segoe UI"
dp2.font.size = Pt(11.5)
dp2.font.color.rgb = NAVY

pipe7_w = 158.0
pipe7_gap = 18.0
pipe7_top = 225.0
pipe7_h = 145.0

c_line7 = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Pt(60.0), Pt(pipe7_top + 14.0), Pt(840.0), Pt(2.0))
c_line7.fill.solid()
c_line7.fill.fore_color.rgb = HAIRLINE
c_line7.line.fill.background()

chain = [
    ("01", "Ảnh gốc ASL", "Phân phối P_train(X)", "Ảnh ký hiệu tự nhiên với dải sáng và độ mờ gốc mà mạng đã học."),
    ("02", "Tiền xử lý", "Kéo giãn / Cân bằng Y", "Can thiệp tái phân bố pixel, thay đổi lược đồ mức xám toàn cục."),
    ("03", "Lệch phân phối", "P_test(X) bị biến dạng", "Ranh giới bóng đổ giữa các ngón tay và nếp nhăn bị khuếch đại hoặc mất."),
    ("04", "Feature Shift", "Dịch chuyển đặc trưng", "Các bộ lọc Conv2D 3×3 trích xuất ra feature maps sai lệch vị trí tâm."),
    ("05", "Sai lệch Softmax", "Phân loại nhầm lẫn", "Véc-tơ đặc trưng rơi vào vùng quyết định của lớp ký tự khác.")
]

for i, (badge_num, title, sub, note) in enumerate(chain):
    cx = 48.0 + i * (pipe7_w + pipe7_gap)
    add_card(s7, cx, pipe7_top, pipe7_w, pipe7_h, bg_color=WHITE, border_color=HAIRLINE)
    add_badge(s7, cx + 12.0, pipe7_top + 8.0, 24.0, badge_num, ROYAL_BLUE, WHITE, 11.0)
    
    tb = s7.shapes.add_textbox(Pt(cx + 10.0), Pt(pipe7_top + 38.0), Pt(pipe7_w - 20.0), Pt(pipe7_h - 45.0))
    tbf = tb.text_frame
    tbf.word_wrap = True
    tbf.margin_left = tbf.margin_top = tbf.margin_right = tbf.margin_bottom = 0
    
    p = tbf.paragraphs[0]
    p.text = title
    p.font.name = "Segoe UI"
    p.font.size = Pt(12.5)
    p.font.bold = True
    p.font.color.rgb = NAVY
    
    p_sub = tbf.add_paragraph()
    p_sub.text = sub
    p_sub.font.name = "Segoe UI"
    p_sub.font.size = Pt(11.0)
    p_sub.font.bold = True
    p_sub.font.color.rgb = ROYAL_BLUE
    
    p_note = tbf.add_paragraph()
    p_note.text = note
    p_note.font.name = "Segoe UI"
    p_note.font.size = Pt(10.5)
    p_note.font.color.rgb = SLATE

add_card(s7, 48.0, 385.0, 864.0, 75.0, bg_color=ICE_BLUE, border_color=ROYAL_BLUE, border_width=1.0)
sci_tb = s7.shapes.add_textbox(Pt(68.0), Pt(392.0), Pt(824.0), Pt(60.0))
stf = sci_tb.text_frame
stf.word_wrap = True
stf.margin_left = stf.margin_top = stf.margin_right = stf.margin_bottom = 0

sp1 = stf.paragraphs[0]
sp1.text = "LƯU Ý KHOA HỌC: PHÂN BIỆT GIỮA KẾT QUẢ THỰC ĐO VÀ GIẢ THUYẾT CƠ CHẾ"
sp1.font.name = "Segoe UI"
sp1.font.size = Pt(11.5)
sp1.font.bold = True
sp1.font.color.rgb = ROYAL_BLUE

sp2 = stf.add_paragraph()
sp2.text = "Kết quả suy giảm độ chính xác là hiện tượng thực nghiệm đã được ghi nhận chắc chắn. Tuy nhiên, việc các lớp Conv2D phản ứng với cạnh giả hoặc vector đặc trưng bị dịch chuyển hiện tại là giả thuyết cơ chế hợp lý; cần đo trực tiếp Feature Maps hoặc Activation tại từng tầng tích chập để chứng minh tuyệt đối."
sp2.font.name = "Segoe UI"
sp2.font.size = Pt(11.0)
sp2.font.color.rgb = NAVY

add_notes(
    s7, 45, "4:25–5:10",
    "Để giải thích nguyên nhân tại sao ảnh rõ hơn lại khiến mô hình đoán sai nhiều hơn, chúng ta cần xem xét dưới góc nhìn Covariate Shift. Trong học máy, Covariate Shift là hiện tượng phân phối dữ liệu đầu vào P(X) bị thay đổi so với dữ liệu huấn luyện. Mạng CNN nhận diện bàn tay không phải bằng trực giác mà bằng hàng chục bộ lọc tích chập 3x3 nhạy cảm với độ chênh lệch cường độ pixel. Khi ta cân bằng lược đồ, các nếp gấp tự nhiên giữa các ngón tay có thể bị biến đổi độ dày, tạo ra các cạnh nhân tạo khiến các tầng Conv trích xuất ra đặc trưng sai lệch.",
    "Trình bày theo chuỗi 5 bước từ ảnh gốc đến kết quả Softmax. Nhấn mạnh khung lưu ý khoa học ở dưới.",
    "Lý thuyết Covariate Shift trong Deep Learning. Khẳng định cơ chế Conv2D phản ứng với cạnh giả là giả thuyết suy diễn, chưa đo feature maps trực tiếp."
)

# ==============================================================================
# SLIDE 08: ERROR ANALYSIS (Redesigned with Modular Confusion Badges)
# ==============================================================================
s8 = prs.slides.add_slide(blank_layout)
set_slide_background_white(s8)
add_header(s8, "Phân tích chi tiết các ca nhận diện sai (Confusion Pairs)", 
           "Sự biến đổi nếp gấp và ranh giới ngón tay khiến các ký hiệu bàn tay tương đồng bị nhầm lẫn", 8)

# Left Column: Contrast Stretching Errors (width = 415 pt, left = 48 pt)
col8_l = 48.0
col8_w = 415.0

# Header card for CS
add_card(s8, col8_l, 142.0, col8_w, 40.0, bg_color=ICE_BLUE, border_color=ROYAL_BLUE, border_width=1.0)
cs_h_tb = s8.shapes.add_textbox(Pt(col8_l + 16.0), Pt(148.0), Pt(col8_w - 32.0), Pt(28.0))
cs_htf = cs_h_tb.text_frame
cs_htf.margin_left = cs_htf.margin_top = cs_htf.margin_right = cs_htf.margin_bottom = 0
p = cs_htf.paragraphs[0]
p.text = "CONTRAST STRETCHING — 3 LỖI / 25 ẢNH (88%)"
p.font.name = "Segoe UI"
p.font.size = Pt(12.5)
p.font.bold = True
p.font.color.rgb = ROYAL_BLUE

# 3 Distinct Confusion Cards
cs_cards = [
    ("Ký hiệu A → Dự đoán: E", "Nắm tay có ngón cái áp sát cạnh ngón trỏ. Khi kéo giãn tương phản mạnh, ranh giới ngón cái bị triệt tiêu khiến bàn tay trông giống dạng co cụm của chữ E."),
    ("Ký hiệu N → Dự đoán: E", "Nắm tay có hai ngón tay vắt qua ngón cái. Độ tương phản cao làm mất chi tiết bóng đổ dưới nếp gấp ngón, dẫn đến nhầm sang E."),
    ("Ký hiệu S → Dự đoán: E", "Nắm tay có ngón cái bắt ngang qua 4 ngón. Chi tiết nổi của ngón cái bị làm phẳng khiến mạng nhầm sang tư thế co cụm của chữ E.")
]

for i, (pair_title, desc) in enumerate(cs_cards):
    cy = 190.0 + i * 68.0
    add_card(s8, col8_l, cy, col8_w, 62.0, bg_color=SOFT_BG, border_color=AMBER, border_width=1.0)
    tb = s8.shapes.add_textbox(Pt(col8_l + 14.0), Pt(cy + 6.0), Pt(col8_w - 28.0), Pt(50.0))
    tbf = tb.text_frame
    tbf.word_wrap = True
    tbf.margin_left = tbf.margin_top = tbf.margin_right = tbf.margin_bottom = 0
    
    p = tbf.paragraphs[0]
    p.text = pair_title
    p.font.name = "Segoe UI"
    p.font.size = Pt(12.0)
    p.font.bold = True
    p.font.color.rgb = AMBER
    
    p_desc = tbf.add_paragraph()
    p_desc.text = desc
    p_desc.font.name = "Segoe UI"
    p_desc.font.size = Pt(10.5)
    p_desc.font.color.rgb = SLATE

# Takeaway note for CS
add_card(s8, col8_l, 400.0, col8_w, 55.0, bg_color=WHITE, border_color=HAIRLINE)
cst_tb = s8.shapes.add_textbox(Pt(col8_l + 14.0), Pt(406.0), Pt(col8_w - 28.0), Pt(45.0))
cstf = cst_tb.text_frame
cstf.word_wrap = True
cstf.margin_left = cstf.margin_top = cstf.margin_right = cstf.margin_bottom = 0
cp = cstf.paragraphs[0]
cp.text = "Nhận định: Cả 3 ca lỗi đều co cụm về chữ E. Điều này chứng minh các đặc trưng phân biệt vị trí ngón cái bị làm phẳng khi kéo giãn độ tương phản."
cp.font.name = "Segoe UI"
cp.font.size = Pt(11.0)
cp.font.color.rgb = NAVY

# Right Column: Histogram Equalization Errors (width = 425 pt, left = 487 pt)
col8_r = 487.0
col8_rw = 425.0

# Header card for HE
add_card(s8, col8_r, 142.0, col8_rw, 40.0, bg_color=SOFT_BG, border_color=AMBER, border_width=1.0)
he_h_tb = s8.shapes.add_textbox(Pt(col8_r + 16.0), Pt(148.0), Pt(col8_rw - 32.0), Pt(28.0))
he_htf = he_h_tb.text_frame
he_htf.margin_left = he_htf.margin_top = he_htf.margin_right = he_htf.margin_bottom = 0
p = he_htf.paragraphs[0]
p.text = "HISTOGRAM EQUALIZATION — 8 LỖI / 25 ẢNH (68%)"
p.font.name = "Segoe UI"
p.font.size = Pt(12.5)
p.font.bold = True
p.font.color.rgb = AMBER

# 4 Group Cards for 8 Confusion Pairs
he_groups = [
    ("G → H  ;  Q → G", "Nhóm ngón trỏ chỉ ngang: Mất chi tiết phân biệt ngón giữa"),
    ("I → J  ;  X → V", "Nhóm ngón út / ngón cong: Ranh giới đầu ngón bị khuếch đại sai lệch"),
    ("N → E  ;  S → E", "Nhóm nắm tay: Lặp lại hiện tượng co cụm đặc trưng ngón cái về E"),
    ("R → U  ;  U → R", "Nhóm ngón bắt chéo: Cân bằng mức xám triệt tiêu độ sâu giữa 2 ngón")
]

for i, (pairs, desc) in enumerate(he_groups):
    gy = 190.0 + i * 50.0
    add_card(s8, col8_r, gy, col8_rw, 45.0, bg_color=WHITE, border_color=HAIRLINE)
    tb = s8.shapes.add_textbox(Pt(col8_r + 14.0), Pt(gy + 4.0), Pt(col8_rw - 28.0), Pt(38.0))
    tbf = tb.text_frame
    tbf.word_wrap = True
    tbf.margin_left = tbf.margin_top = tbf.margin_right = tbf.margin_bottom = 0
    
    p = tbf.paragraphs[0]
    r_p = p.add_run()
    r_p.text = pairs + "  "
    r_p.font.name = "Segoe UI"
    r_p.font.size = Pt(12.0)
    r_p.font.bold = True
    r_p.font.color.rgb = NAVY
    
    r_d = p.add_run()
    r_d.text = desc
    r_d.font.name = "Segoe UI"
    r_d.font.size = Pt(10.5)
    r_d.font.color.rgb = SLATE

# Takeaway note for HE
add_card(s8, col8_r, 400.0, col8_rw, 55.0, bg_color=WHITE, border_color=HAIRLINE)
het_tb = s8.shapes.add_textbox(Pt(col8_r + 14.0), Pt(406.0), Pt(col8_rw - 28.0), Pt(45.0))
hetf = het_tb.text_frame
hetf.word_wrap = True
hetf.margin_left = hetf.margin_top = hetf.margin_right = hetf.margin_bottom = 0
hp = hetf.paragraphs[0]
hp.text = "Nhận định: Cân bằng lược đồ gây xáo trộn diện rộng trên các cặp ký hiệu có cấu trúc hình học tương đồng cao do triệt tiêu độ sâu không gian 3D."
hp.font.name = "Segoe UI"
hp.font.size = Pt(11.0)
hp.font.color.rgb = AMBER

# Bottom Disclaimer
disc8 = s8.shapes.add_textbox(Pt(48.0), Pt(465.0), Pt(864.0), Pt(30.0))
d8_tf = disc8.text_frame
d8_tf.word_wrap = True
d8_tf.margin_left = d8_tf.margin_top = d8_tf.margin_right = d8_tf.margin_bottom = 0
dp8 = d8_tf.paragraphs[0]
dp8.text = "Lưu ý phương pháp: Các cặp nhầm lẫn trên là số liệu thực tế được ghi nhận từ mô hình. Phần phân tích hình thái ngón tay là giải thích cơ chế thị giác dự kiến."
dp8.font.name = "Segoe UI"
dp8.font.size = Pt(12.0)
dp8.font.color.rgb = SLATE

add_notes(
    s8, 50, "5:10–6:00",
    "Khi đi sâu vào các ca dự đoán sai, chúng ta phát hiện một quy luật hình thái học rất thú vị. Với Contrast Stretching, toàn bộ 3 ca lỗi là A, N và S đều bị mô hình dự đoán nhầm thành chữ E. Trong ngôn ngữ ký hiệu ASL, A, E, N, S đều là các thế nắm tay chặt, điểm khác biệt duy nhất nằm ở vị trí ngón cái. Khi độ tương phản bị kéo giãn, ranh giới nếp gấp của ngón cái bị triệt tiêu, khiến mô hình nhầm lẫn sang chữ E. Tương tự với Histogram Equalization, 8 ca lỗi đều rơi vào các cặp có hình học cực kỳ giống nhau như G với H, R với U hay X với V.",
    "So sánh sự tập trung lỗi của Contrast Stretching (về chữ E) và sự phân tán lỗi của Histogram Equalization (8 cặp).",
    "Ghi nhận thực nghiệm: CS lỗi A, N, S -> E. HE lỗi G->H, I->J, N->E, Q->G, R->U, S->E, U->R, X->V. Không tự vẽ thêm các ảnh nhầm lẫn chưa có."
)

# ==============================================================================
# SLIDE 09: SOFTMAX PROBABILITY DEEP DIVE (Chart Collision Fixed)
# ==============================================================================
s9 = prs.slides.add_slide(blank_layout)
set_slide_background_white(s9)
add_header(s9, "Phân tích đầu ra xác suất Softmax trên ký hiệu 'A'", 
           "Đảo chiều nhãn dự đoán và sự xói mòn độ tự tin khi thay đổi phân phối cường độ sáng", 9)

if os.path.exists("assets/softmax_chart.png"):
    s9.shapes.add_picture("assets/softmax_chart.png", Pt(48.0), Pt(145.0), Pt(480.0), Pt(210.0))

col9_r = 548.0
col9_rw = 364.0

cases9 = [
    ("1. Ảnh gốc (Baseline): Đúng tuyệt đối", "Top-1: Ký hiệu 'A' với Confidence = 99,9%\nXác suất nhãn E < 0,1%. Mô hình hoàn toàn tự tin và dự đoán chính xác.", ROYAL_BLUE),
    ("2. Contrast Stretching: Đảo chiều dự đoán", "Top-1: Ký hiệu 'E' với Confidence = 98,4%\nXác suất nhãn đúng 'A' rơi xuống chỉ còn 1,6%. Mô hình tự tin cực cao vào một kết quả SAI!", AMBER),
    ("3. Histogram Equalization: Bào mòn niềm tin", "Top-1: Ký hiệu 'A' với Confidence = 91,7%\nXác suất nhãn E tăng lên 8,3%. Vẫn đoán đúng A nhưng độ tự tin sụt giảm rõ rệt.", SLATE)
]

for i, (head, body, clr) in enumerate(cases9):
    y_pos = 145.0 + i * 72.0
    add_card(s9, col9_r, y_pos, col9_rw, 64.0, bg_color=SOFT_BG, border_color=clr if clr != SLATE else HAIRLINE, border_width=1.5)
    tb = s9.shapes.add_textbox(Pt(col9_r + 14.0), Pt(y_pos + 6.0), Pt(col9_rw - 28.0), Pt(52.0))
    tbf = tb.text_frame
    tbf.word_wrap = True
    tbf.margin_left = tbf.margin_top = tbf.margin_right = tbf.margin_bottom = 0
    p = tbf.paragraphs[0]
    p.text = head
    p.font.name = "Segoe UI"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = clr
    p_b = tbf.add_paragraph()
    p_b.text = body
    p_b.font.name = "Segoe UI"
    p_b.font.size = Pt(10.5)
    p_b.font.color.rgb = NAVY

add_card(s9, 48.0, 370.0, 864.0, 85.0, bg_color=ICE_BLUE, border_color=ROYAL_BLUE, border_width=1.5)
calib_tb = s9.shapes.add_textbox(Pt(68.0), Pt(378.0), Pt(824.0), Pt(70.0))
ctf = calib_tb.text_frame
ctf.word_wrap = True
ctf.margin_left = ctf.margin_top = ctf.margin_right = ctf.margin_bottom = 0

cp1 = ctf.paragraphs[0]
cp1.text = "BÀI HỌC VỀ HIỆU CHUẨN XÁC SUẤT (MODEL CALIBRATION)"
cp1.font.name = "Segoe UI"
cp1.font.size = Pt(12.0)
cp1.font.bold = True
cp1.font.color.rgb = ROYAL_BLUE

cp2 = ctf.add_paragraph()
cp2.text = "Không được nhầm lẫn giữa Confidence (độ tự tin Softmax) và Accuracy (độ chính xác thực tế). Ở trường hợp Contrast Stretching, mô hình dự đoán nhầm sang 'E' với độ tự tin lên tới 98,4%. Điều này chứng minh Softmax cực đoan (over-confident) khi gặp dữ liệu bị dịch chuyển phân phối, và độ tự tin cao không bảo đảm cho tính đúng đắn của quyết định phân loại."
cp2.font.name = "Segoe UI"
cp2.font.size = Pt(11.0)
cp2.font.color.rgb = NAVY

disc9 = s9.shapes.add_textbox(Pt(48.0), Pt(465.0), Pt(864.0), Pt(30.0))
d9_tf = disc9.text_frame
d9_tf.word_wrap = True
d9_tf.margin_left = d9_tf.margin_top = d9_tf.margin_right = d9_tf.margin_bottom = 0
dp9 = d9_tf.paragraphs[0]
dp9.text = "Ghi chú: Số liệu xác suất Softmax được trích xuất trực tiếp từ véc-tơ đầu ra 29 chiều trên ca kiểm thử chữ 'A'. Các nhãn khác có xác suất xấp xỉ 0."
dp9.font.name = "Segoe UI"
dp9.font.size = Pt(12.0)
dp9.font.color.rgb = SLATE

add_notes(
    s9, 45, "6:00–6:45",
    "Để chứng minh tác động sâu sắc của tiền xử lý lên không gian xác suất, slide này phân tích chi tiết trường hợp ký hiệu 'A'. Ở ảnh gốc, mạng rất tự tin: nhãn A đạt 99,9%, E gần như bằng 0. Khi qua Histogram Equalization, mô hình vẫn đoán đúng A nhưng độ tự tin rơi xuống 91,7%, và xác suất nhầm sang E tăng lên 8,3%. Đáng báo động nhất là Contrast Stretching: mô hình bị đảo chiều hoàn toàn, khẳng định 98,4% đây là chữ E và chỉ dành 1,6% cho chữ A. Đây là minh chứng kinh điển cho thấy độ tự tin Softmax cao không đồng nghĩa với dự đoán đúng.",
    "Chỉ vào thanh ngang màu cam ở trường hợp Contrast Stretching. Nhấn mạnh việc mạng rất tự tin (98,4%) vào một quyết định sai hoàn toàn.",
    "Dữ liệu Softmax trích xuất cho ký hiệu A: Baseline (A 99.9%), CS (E 98.4%, A 1.6%), HE (A 91.7%, E 8.3%)."
)

# ==============================================================================
# SLIDE 10: CONCLUSION & FUTURE WORK (Refined Vertical Spacing)
# ==============================================================================
s10 = prs.slides.add_slide(blank_layout)
set_slide_background_white(s10)

k10 = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Pt(48.0), Pt(33.0), Pt(27.0), Pt(3.75))
k10.fill.solid()
k10.fill.fore_color.rgb = ROYAL_BLUE
k10.line.fill.background()

t10_box = s10.shapes.add_textbox(Pt(48.0), Pt(46.0), Pt(864.0), Pt(70.0))
t10_f = t10_box.text_frame
t10_f.word_wrap = True
t10_f.margin_left = t10_f.margin_top = t10_f.margin_right = t10_f.margin_bottom = 0

p1 = t10_f.paragraphs[0]
p1.text = "Tiền xử lý và CNN: Cần sự tương thích phân phối"
p1.font.name = "Segoe UI"
p1.font.size = Pt(28.0)
p1.font.bold = True
p1.font.color.rgb = NAVY

p2 = t10_f.add_paragraph()
p2.text = "Đánh giá bằng thực nghiệm định lượng, không dựa vào cảm quan thị giác của mắt người"
p2.font.name = "Segoe UI"
p2.font.size = Pt(15.0)
p2.font.color.rgb = ROYAL_BLUE

col10_l = 48.0
col10_w = 420.0

# 5 Conclusions
add_card(s10, col10_l, 125.0, col10_w, 310.0, bg_color=SOFT_BG, border_color=HAIRLINE)
c10_tb = s10.shapes.add_textbox(Pt(col10_l + 18.0), Pt(135.0), Pt(col10_w - 36.0), Pt(290.0))
ct10_f = c10_tb.text_frame
ct10_f.word_wrap = True
ct10_f.margin_left = ct10_f.margin_top = ct10_f.margin_right = ct10_f.margin_bottom = 0

p = ct10_f.paragraphs[0]
p.text = "5 KẾT LUẬN RÚT RA TỪ THỰC NGHIỆM"
p.font.name = "Segoe UI"
p.font.size = Pt(12.5)
p.font.bold = True
p.font.color.rgb = ROYAL_BLUE

conclusions = [
    ("1. Không phải lúc nào cũng tốt: ", "Tăng cường tương phản không đồng nghĩa với việc cải thiện độ chính xác phân loại của mạng CNN."),
    ("2. Ảnh gốc đạt tối ưu: ", "Trong tập kiểm thử 25 ảnh, ảnh gốc đạt 100% so với 88% (Contrast Stretching) và 68% (Histogram Equalization)."),
    ("3. Nhất quán phân phối P(X): ", "Độ nhạy của CNN đòi hỏi dữ liệu đầu vào phải tương thích chặt chẽ với phân phối ảnh đã học trong huấn luyện."),
    ("4. Khuyến nghị huấn luyện: ", "Nếu muốn dùng tiền xử lý trong triển khai thực tế, bắt buộc phải tích hợp chúng vào quy trình Data Augmentation."),
    ("5. Định lượng thay vì cảm quan: ", "Đánh giá pipeline thị giác máy tính phải dựa trên Accuracy và Loss định lượng, không dựa vào mắt nhìn con người.")
]

for head, body in conclusions:
    p_c = ct10_f.add_paragraph()
    p_c.space_before = Pt(12.0)
    rh = p_c.add_run()
    rh.text = head
    rh.font.bold = True
    rh.font.color.rgb = ROYAL_BLUE
    rh.font.size = Pt(11.5)
    rb = p_c.add_run()
    rb.text = body
    rb.font.color.rgb = NAVY
    rb.font.size = Pt(11.0)

# 4 Future Works
col10_r = 492.0
col10_rw = 420.0

add_card(s10, col10_r, 125.0, col10_rw, 310.0, bg_color=SOFT_BG, border_color=HAIRLINE)
f10_tb = s10.shapes.add_textbox(Pt(col10_r + 18.0), Pt(135.0), Pt(col10_rw - 36.0), Pt(290.0))
ft10_f = f10_tb.text_frame
ft10_f.word_wrap = True
ft10_f.margin_left = ft10_f.margin_top = ft10_f.margin_right = ft10_f.margin_bottom = 0

p = ft10_f.paragraphs[0]
p.text = "4 HƯỚNG PHÁT TRIỂN TIẾP THEO"
p.font.name = "Segoe UI"
p.font.size = Pt(12.5)
p.font.bold = True
p.font.color.rgb = NAVY

future_works = [
    ("1. Mở rộng tập kiểm thử: ", "Thực nghiệm trên tập dữ liệu hàng nghìn ảnh với nhiều điều kiện phơi sáng, màu da và bối cảnh chụp khác nhau."),
    ("2. Kiểm tra tính độc lập: ", "Xác minh mức độ độc lập giữa tập kiểm thử và tập huấn luyện gốc của mô hình để loại trừ hiện tượng ghi nhớ (memorization)."),
    ("3. Trích xuất Feature Maps: ", "Trực quan hóa activation maps tại các tầng Conv2D để kiểm chứng giả thuyết về việc hình thành cạnh giả hoặc mất nếp gấp."),
    ("4. Chuẩn hóa đo thời gian: ", "Lặp lại đo đạc thời gian trễ tiền xử lý trên phần cứng chuẩn hóa (CPU/GPU) với nhiều vòng lặp để tăng độ tin cậy thống kê.")
]

for head, body in future_works:
    p_f = ft10_f.add_paragraph()
    p_f.space_before = Pt(14.0)
    rh = p_f.add_run()
    rh.text = head
    rh.font.bold = True
    rh.font.color.rgb = NAVY
    rh.font.size = Pt(11.5)
    rb = p_f.add_run()
    rb.text = body
    rb.font.color.rgb = SLATE
    rb.font.size = Pt(11.0)

# Bottom Takeaway Motto
add_card(s10, 48.0, 450.0, 864.0, 48.0, bg_color=ICE_BLUE, border_color=ROYAL_BLUE, border_width=1.0)
motto_tb = s10.shapes.add_textbox(Pt(68.0), Pt(460.0), Pt(824.0), Pt(30.0))
mtf = motto_tb.text_frame
mtf.margin_left = mtf.margin_top = mtf.margin_right = mtf.margin_bottom = 0
mp = mtf.paragraphs[0]
mp.text = "Đúng phân phối. Chuẩn thực nghiệm. Vững độ tin cậy."
mp.font.name = "Segoe UI"
mp.font.size = Pt(16.0)
mp.font.bold = True
mp.font.color.rgb = NAVY

p_box10 = s10.shapes.add_textbox(Pt(892.5), Pt(510.0), Pt(25.0), Pt(18.0))
p10_tf = p_box10.text_frame
p10_tf.margin_left = p10_tf.margin_top = p10_tf.margin_right = p10_tf.margin_bottom = 0
pp10 = p10_tf.paragraphs[0]
pp10.text = "10"
pp10.font.name = "Segoe UI"
pp10.font.size = Pt(11.25)
pp10.font.color.rgb = SLATE

backup_qa_10 = (
    "1. Vì sao không huấn luyện lại mô hình với dữ liệu đã tăng tương phản?\n"
    "-> Mục tiêu đề tài là đánh giá tác động của tiền xử lý lên một mô hình đã triển khai sẵn (off-the-shelf). Nếu huấn luyện lại, mô hình sẽ học phân phối mới và không còn phản ánh được tác động của Covariate Shift.\n"
    "2. Vì sao chỉ thử nghiệm trên 25 ảnh?\n"
    "-> Đây là tập kiểm thử đại diện 25 chữ cái A-Y được cung cấp trong phạm vi bài tập lớn. Nhóm đã ghi rõ hạn chế này và đề xuất mở rộng tập dữ liệu trong hướng phát triển.\n"
    "3. Có phải Contrast Stretching luôn tệ hơn ảnh gốc?\n"
    "-> Không. Nếu ảnh đầu vào thực sự bị chụp trong môi trường quá tối và mô hình được huấn luyện kèm data augmentation tương phản, tiền xử lý có thể có lợi. Điểm mấu chốt là sự tương thích phân phối.\n"
    "4. Vì sao Histogram Equalization lại giảm sâu đến 68%?\n"
    "-> HE làm biến dạng phân phối phi tuyến tính rất mạnh, làm sáng các vùng tối tự nhiên giữa các kẽ ngón tay, triệt tiêu bóng đổ là đặc trưng biên quan trọng của CNN.\n"
    "5. Độ tự tin 98,4% của chữ E nói lên điều gì?\n"
    "-> Cho thấy mạng bị over-confident (quá tự tin) khi phân phối bị lệch, chứng minh hàm Softmax cần được cân chuẩn (calibration) bằng các kỹ thuật như Temperature Scaling trước khi tin cậy vào xác suất."
)

add_notes(
    s10, 40, "6:45–7:25",
    "Để kết luận, nghiên cứu của nhóm em đưa ra một thông điệp quan trọng: Trong các hệ thống thị giác máy tính hiện đại dựa trên Deep Learning, tiền xử lý ảnh không thể được áp dụng một cách cảm tính dựa trên việc mắt người nhìn thấy rõ hơn. Bất kỳ sự can thiệp nào làm thay đổi phân phối cường độ sáng đều có nguy cơ gây ra hiện tượng Covariate Shift, dẫn đến suy giảm độ chính xác và làm lệch lạc độ tự tin Softmax. Mọi giải pháp tiền xử lý phải được kiểm chứng bằng thực nghiệm định lượng. Nhóm em xin chân thành cảm ơn thầy cô và sẵn sàng lắng nghe câu hỏi.",
    "Kết thúc bài thuyết trình đúng 7 phút 25 giây (nằm trọn trong giới hạn 10 phút). Chuyển sang tư thế sẵn sàng cho phần hỏi đáp phản biện.",
    "Tổng kết toàn bộ 10 slide. Dữ liệu và kết luận tuân thủ trung thực với kết quả thực nghiệm đã cung cấp.",
    backup_qa=backup_qa_10
)

# Save presentation
prs.save(output_pptx)
print(f"Presentation successfully updated at: {output_pptx}")

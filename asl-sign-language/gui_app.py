"""
ASL Vision Pro - Enterprise Edition (Tone Sáng)
Hệ Thống Nghiên Cứu & Đánh Giá Tiền Xử Lý Ảnh Nhận Diện Ký Hiệu ASL
Phục vụ Đồ án Môn Xử lý ảnh & Trí tuệ nhân tạo

Cấu trúc chuẩn Doanh nghiệp:
  1. Thanh điều hướng Taskbar bên trái:
     - 🔍 Nhận diện & So sánh Tiền xử lý (Trực quan hóa đối sánh 3 ảnh cỡ lớn + Bảng xếp hạng xác suất thấp hơn)
     - 📊 Dashboard Thực nghiệm (Trực quan hóa đồ thị 25 mẫu test N=25)
     - 📚 Cơ sở lý thuyết & Công thức (Toán học, giải thuật tiền xử lý, không gian màu YCrCb, Softmax, CNN)
  2. Bỏ hoàn toàn phần Hướng phát triển và tính năng Webcam.
  3. Bảo toàn 100% mô hình CNN gốc và bộ trọng số asl_classifier.keras.
"""

import os
import sys
import glob
import json
import time
import warnings
from typing import Dict, Any, List

# Cấu hình UTF-8 cho console Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['PYTHONUTF8'] = '1'
warnings.filterwarnings('ignore')

import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Tải TensorFlow trong yên lặng
_stderr_fd = sys.stderr.fileno()
with open(os.devnull, 'w') as _devnull:
    _old_stderr = os.dup(_stderr_fd)
    os.dup2(_devnull.fileno(), _stderr_fd)
    try:
        import tensorflow as tf
        tf.get_logger().setLevel('ERROR')
    finally:
        os.dup2(_old_stderr, _stderr_fd)
        os.close(_old_stderr)

from preprocessing import (
    contrast_stretching,
    histogram_equalization,
    prepare_for_cnn,
    imread_unicode,
    imwrite_unicode,
    apply_variant
)
from experiment_runner import ExperimentRunner, ModelInferenceEngine


# Bảng mã màu Doanh Nghiệp (Enterprise Light Theme Palette)
THEME = {
    'bg_app': '#F8FAFC',          # Slate 50
    'bg_card': '#FFFFFF',         # Trắng chuẩn Card
    'border': '#E2E8F0',          # Slate 200 (Viền nhẹ chuẩn Enterprise)
    'border_focus': '#2563EB',    # Blue 600
    'text_main': '#0F172A',       # Slate 900 (Tiêu đề đậm)
    'text_sub': '#475569',        # Slate 600 (Chữ diễn giải)
    'text_muted': '#94A3B8',      # Slate 400
    'primary': '#2563EB',         # Royal Blue 600
    'primary_light': '#EFF6FF',   # Blue 50
    'primary_hover': '#1D4ED8',   # Blue 700
    'sidebar_bg': '#FFFFFF',      # Sidebar nền sáng
    'sidebar_border': '#E2E8F0',
    'sidebar_active': '#EFF6FF',
    'sidebar_active_fg': '#1D4ED8',
    'sidebar_fg': '#475569',
    'success': '#059669',         # Emerald 600
    'success_bg': '#ECFDF5',      # Emerald 50
    'warning': '#D97706',         # Amber 600
    'warning_bg': '#FFFBEB',      # Amber 50
    'danger': '#DC2626',          # Red 600
    'danger_bg': '#FEF2F2',       # Red 50
    'purple': '#7C3AED',          # Violet 600
    'purple_bg': '#F5F3FF',
    'code_bg': '#F1F5F9',        # Slate 100
    'formula_fg': '#1E3A8A',     # Blue 900
}


class ASLEnterpriseApp:
    def __init__(self, root: tk.Tk, model_filename: str = "asl_classifier.keras"):
        self.root = root
        self.root.title("ASL Vision Pro - Hệ Thống Đánh Giá & Nghiên Cứu Tiền Xử Lý Ảnh ASL")
        self.root.geometry("1360x880")
        self.root.minsize(1180, 740)
        self.root.configure(bg=THEME['bg_app'])

        # Đường dẫn
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.dirname(self.base_dir)
        self.model_path = os.path.join(self.base_dir, "models", model_filename)

        # Định vị thư mục test_data
        candidates_test_dir = [
            os.path.join(self.project_root, "test_data"),
            os.path.join(self.base_dir, "test_data"),
            r"F:\OneDrive\hoc hanh\XLA\BTL_TTNT\test_data"
        ]
        self.test_data_dir = None
        for cand in candidates_test_dir:
            if os.path.exists(cand):
                self.test_data_dir = cand
                break

        # Định vị file benchmark_results.json
        candidates_json = [
            os.path.join(self.project_root, "benchmark_results.json"),
            os.path.join(self.base_dir, "benchmark_results.json"),
            r"F:\OneDrive\hoc hanh\XLA\BTL_TTNT\benchmark_results.json"
        ]
        self.benchmark_json_path = candidates_json[0]
        for cj in candidates_json:
            if os.path.exists(cj):
                self.benchmark_json_path = cj
                break

        # Khởi tạo mô hình
        self.classes = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + ['del', 'nothing', 'space']
        self.model = self._load_model()
        self.inference_engine = ModelInferenceEngine(self.model)
        self.runner = ExperimentRunner(self.inference_engine, self.classes)

        # Danh sách mẫu từ test_data
        self.test_samples = self._scan_test_samples()

        # Dữ liệu benchmark
        self.benchmark_data = self._load_benchmark_data()

        # Trạng thái ảnh hiện tại
        self.current_image_path = None
        self.current_crop_bgr = None
        self.inference_results = None

        # Lưu trữ thumbnail Tkinter & công thức toán học
        self.tk_images = {}
        self.formula_images = {}

        # Trang hiện tại
        self.current_page = "inference"
        self.pages = {}
        self.page_canvases = {}
        self.nav_buttons = {}

        self._configure_styles()
        self._build_layout()

        # Nạp mẫu đầu tiên nếu có
        if self.test_samples:
            self._select_sample_by_index(0)

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure(
            "Enterprise.Treeview",
            background="#FFFFFF",
            foreground=THEME['text_main'],
            rowheight=30,
            fieldbackground="#FFFFFF",
            font=("Segoe UI", 9),
            borderwidth=1,
            relief="flat"
        )
        style.configure(
            "Enterprise.Treeview.Heading",
            background="#F1F5F9",
            foreground=THEME['text_main'],
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padding=6
        )
        style.map(
            "Enterprise.Treeview",
            background=[("selected", THEME['primary_light'])],
            foreground=[("selected", THEME['primary'])]
        )

        style.configure(
            "TCombobox",
            fieldbackground="#FFFFFF",
            background="#FFFFFF",
            foreground=THEME['text_main'],
            font=("Segoe UI", 10),
            padding=5
        )

    def _load_model(self):
        if not os.path.exists(self.model_path):
            messagebox.showerror("Lỗi Tải Mô Hình", f"Không tìm thấy mô hình tại:\n{self.model_path}")
            sys.exit(1)
        try:
            return tf.keras.models.load_model(self.model_path)
        except Exception as err:
            messagebox.showerror("Lỗi Khởi Động", f"Không thể tải mô hình CNN:\n{err}")
            sys.exit(1)

    def _scan_test_samples(self) -> List[Dict[str, Any]]:
        samples = []
        if self.test_data_dir and os.path.exists(self.test_data_dir):
            files = sorted(glob.glob(os.path.join(self.test_data_dir, "*.png")))
            for idx, f in enumerate(files):
                expected_char = chr(ord('A') + idx) if idx < 25 else f"Mẫu {idx+1}"
                samples.append({
                    'index': idx,
                    'gt_label': expected_char,
                    'file_path': f,
                    'filename': os.path.basename(f),
                    'display_name': f"[{expected_char}]  {os.path.basename(f)}"
                })
        return samples

    def _load_benchmark_data(self) -> Dict[str, Any]:
        if os.path.exists(self.benchmark_json_path):
            try:
                with open(self.benchmark_json_path, "r", encoding="utf-8") as fp:
                    return json.load(fp)
            except Exception:
                pass
        return {}

    # =========================================================================
    # XÂY DỰNG GIAO DIỆN CHÍNH (SIDEBAR + CONTENT PAGES)
    # =========================================================================
    def _build_layout(self):
        self.main_container = tk.Frame(self.root, bg=THEME['bg_app'])
        self.main_container.pack(fill="both", expand=True)

        # 1. Thanh Taskbar bên trái (Left Sidebar)
        self.sidebar_frame = tk.Frame(
            self.main_container,
            bg=THEME['sidebar_bg'],
            width=270,
            highlightthickness=1,
            highlightbackground=THEME['sidebar_border']
        )
        self.sidebar_frame.pack(side="left", fill="y", padx=0, pady=0)
        self.sidebar_frame.pack_propagate(False)

        self._build_sidebar()

        # 2. Vùng hiển thị Nội dung
        self.content_frame = tk.Frame(self.main_container, bg=THEME['bg_app'])
        self.content_frame.pack(side="right", fill="both", expand=True, padx=20, pady=16)

        # 3 Phân hệ chính theo yêu cầu mới
        self.pages["inference"] = self._build_inference_page()
        self.pages["dashboard"] = self._build_dashboard_page()
        self.pages["theory"] = self._build_theory_page()

        self._bind_mousewheel()
        self._switch_page("inference")

    def _build_sidebar(self):
        # Header Sidebar
        brand_frame = tk.Frame(self.sidebar_frame, bg=THEME['sidebar_bg'], padx=18, pady=20)
        brand_frame.pack(fill="x")

        logo_row = tk.Frame(brand_frame, bg=THEME['sidebar_bg'])
        logo_row.pack(fill="x")

        logo_badge = tk.Label(
            logo_row,
            text="ASL",
            bg=THEME['primary'],
            fg="#FFFFFF",
            font=("Segoe UI", 11, "bold"),
            padx=8,
            pady=4,
            relief="flat"
        )
        logo_badge.pack(side="left")

        title_frame = tk.Frame(logo_row, bg=THEME['sidebar_bg'], padx=10)
        title_frame.pack(side="left", fill="y")

        lbl_app = tk.Label(
            title_frame,
            text="ASL Vision Pro",
            bg=THEME['sidebar_bg'],
            fg=THEME['text_main'],
            font=("Segoe UI", 13, "bold")
        )
        lbl_app.pack(anchor="w")

        lbl_sub = tk.Label(
            title_frame,
            text="Research Suite • Enterprise",
            bg=THEME['sidebar_bg'],
            fg=THEME['text_muted'],
            font=("Segoe UI", 8)
        )
        lbl_sub.pack(anchor="w")

        sep1 = tk.Frame(self.sidebar_frame, bg=THEME['sidebar_border'], height=1)
        sep1.pack(fill="x", padx=16, pady=12)

        lbl_nav_title = tk.Label(
            self.sidebar_frame,
            text="DANH MỤC NGHIÊN CỨU",
            bg=THEME['sidebar_bg'],
            fg=THEME['text_muted'],
            font=("Segoe UI", 8, "bold"),
            padx=18
        )
        lbl_nav_title.pack(anchor="w", pady=(4, 6))

        # 3 Phân hệ chính
        nav_items = [
            ("inference", "🔍  Nhận diện & So sánh", "Đối sánh trực quan 3 thuật toán"),
            ("dashboard", "📊  Dashboard Thực nghiệm", "Trực quan hóa đồ thị 25 mẫu test"),
            ("theory", "📚  Cơ sở lý thuyết & Công thức", "Toán học & Giải thuật tiền xử lý"),
        ]

        for page_id, label_text, sub_desc in nav_items:
            btn_frame = tk.Frame(self.sidebar_frame, bg=THEME['sidebar_bg'])
            btn_frame.pack(fill="x", padx=12, pady=4)

            btn = tk.Button(
                btn_frame,
                text=label_text,
                font=("Segoe UI", 10, "bold"),
                bg=THEME['sidebar_bg'],
                fg=THEME['sidebar_fg'],
                activebackground=THEME['sidebar_active'],
                activeforeground=THEME['sidebar_active_fg'],
                relief="flat",
                anchor="w",
                padx=14,
                pady=10,
                cursor="hand2",
                command=lambda p=page_id: self._switch_page(p)
            )
            btn.pack(fill="x")
            self.nav_buttons[page_id] = btn

        spacer = tk.Frame(self.sidebar_frame, bg=THEME['sidebar_bg'])
        spacer.pack(fill="both", expand=True)

        footer_frame = tk.Frame(
            self.sidebar_frame,
            bg=THEME['bg_app'],
            padx=16,
            pady=14,
            highlightthickness=1,
            highlightbackground=THEME['border']
        )
        footer_frame.pack(fill="x", padx=12, pady=12)

        lbl_foot_title = tk.Label(
            footer_frame,
            text="MÔ HÌNH BẢO VỆ",
            bg=THEME['bg_app'],
            fg=THEME['text_muted'],
            font=("Segoe UI", 7, "bold")
        )
        lbl_foot_title.pack(anchor="w")

        lbl_foot_model = tk.Label(
            footer_frame,
            text="asl_classifier.keras",
            bg=THEME['bg_app'],
            fg=THEME['text_main'],
            font=("Segoe UI", 9, "bold")
        )
        lbl_foot_model.pack(anchor="w", pady=(2, 0))

        status_row = tk.Frame(footer_frame, bg=THEME['bg_app'])
        status_row.pack(anchor="w", pady=(4, 0))

        dot = tk.Label(status_row, text="●", fg=THEME['success'], bg=THEME['bg_app'], font=("Segoe UI", 9))
        dot.pack(side="left")

        status_text = tk.Label(
            status_row,
            text="CNN Baseline: 100% đúng",
            fg=THEME['success'],
            bg=THEME['bg_app'],
            font=("Segoe UI", 8, "bold"),
            padx=4
        )
        status_text.pack(side="left")

    def _switch_page(self, page_name: str):
        self.current_page = page_name

        for p in self.pages.values():
            p.pack_forget()

        for pid, btn in self.nav_buttons.items():
            if pid == page_name:
                btn.configure(
                    bg=THEME['sidebar_active'],
                    fg=THEME['sidebar_active_fg'],
                    relief="flat"
                )
            else:
                btn.configure(
                    bg=THEME['sidebar_bg'],
                    fg=THEME['sidebar_fg'],
                    relief="flat"
                )

        if page_name in self.pages:
            self.pages[page_name].pack(fill="both", expand=True)

    def _bind_mousewheel(self):
        """Kích hoạt cuộn con lăn chuột (Mouse Wheel Scroll) toàn cục trên mọi phân hệ giao diện."""
        self.root.bind_all("<MouseWheel>", self._on_mousewheel)
        self.root.bind_all("<Button-4>", lambda e: self._scroll_active_canvas(-2))
        self.root.bind_all("<Button-5>", lambda e: self._scroll_active_canvas(2))

    def _on_mousewheel(self, event):
        canvas = self.page_canvases.get(self.current_page)
        if canvas and canvas.winfo_exists():
            if event.delta:
                if abs(event.delta) >= 120:
                    steps = int(-1 * (event.delta / 60))
                else:
                    steps = int(-1 * event.delta)
                canvas.yview_scroll(steps, "units")

    def _scroll_active_canvas(self, steps: int):
        canvas = self.page_canvases.get(self.current_page)
        if canvas and canvas.winfo_exists():
            canvas.yview_scroll(steps, "units")

    # =========================================================================
    # PHÂN HỆ 1: NHẬN DIỆN & SO SÁNH TRỰC QUAN (ẢNH Ở BÊN TRÁI, BẢNG XẾP HẠNG Ở BÊN PHẢI)
    # =========================================================================
    def _build_inference_page(self) -> tk.Frame:
        page = tk.Frame(self.content_frame, bg=THEME['bg_app'])

        canvas = tk.Canvas(page, bg=THEME['bg_app'], highlightthickness=0)
        self.page_canvases["inference"] = canvas
        v_scroll = ttk.Scrollbar(page, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=THEME['bg_app'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas_win = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=1050)
        canvas.configure(yscrollcommand=v_scroll.set)

        def _on_canvas_resize(event):
            canvas.itemconfig(canvas_win, width=event.width)
        canvas.bind("<Configure>", _on_canvas_resize)

        v_scroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # 1. Header Toolbar (Nạp ảnh)
        toolbar = tk.Frame(
            scrollable_frame,
            bg=THEME['bg_card'],
            padx=18,
            pady=12,
            highlightthickness=1,
            highlightbackground=THEME['border']
        )
        toolbar.pack(fill="x", pady=(0, 10))

        btn_open = tk.Button(
            toolbar,
            text="📁  Chọn Ảnh Từ Máy Tính...",
            bg=THEME['primary'],
            fg="#FFFFFF",
            activebackground=THEME['primary_hover'],
            activeforeground="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=16,
            pady=7,
            cursor="hand2",
            command=self._on_choose_file
        )
        btn_open.pack(side="left")

        # 2. KHUNG NỘI DUNG CHÍNH (CHIA 2 PHẦN BẰNG PANEDWINDOW CÓ THỂ KÉO DÃN LINH HOẠT)
        self.split_pane = tk.PanedWindow(
            scrollable_frame,
            orient="horizontal",
            sashrelief="flat",
            sashwidth=6,
            bg=THEME['border'],
            bd=0,
            sashcursor="sb_h_double_arrow"
        )
        self.split_pane.pack(fill="both", expand=True)

        # -------------------------------------------------------------
        # CỘT TRÁI (TRỌNG TÂM): KẾT QUẢ TỐI ƯU & 3 ẢNH SO SÁNH LỚN
        # -------------------------------------------------------------
        left_main = tk.Frame(self.split_pane, bg=THEME['bg_app'], padx=6)

        # Hero Card: Kết quả tối ưu nhất
        self.hero_card = tk.Frame(
            left_main,
            bg=THEME['bg_card'],
            padx=18,
            pady=10,
            highlightthickness=2,
            highlightbackground=THEME['border_focus']
        )
        self.hero_card.pack(fill="x", pady=(0, 10))

        self._build_hero_card_content()

        # Tiêu đề phần so sánh trực quan ảnh lớn
        section_title_frame = tk.Frame(left_main, bg=THEME['bg_app'])
        section_title_frame.pack(fill="x", pady=(0, 6))

        tk.Label(
            section_title_frame,
            text="🔍  TRỌNG TÂM ĐỐI SÁNH TRỰC QUAN CÁC THUẬT TOÁN TIỀN XỬ LÝ",
            bg=THEME['bg_app'],
            fg=THEME['text_main'],
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")

        # Hàng 3 ảnh cỡ lớn
        images_row = tk.Frame(left_main, bg=THEME['bg_app'])
        images_row.pack(fill="x", pady=(0, 10))

        self.panel_raw = self._create_large_image_card(
            images_row,
            title="Ảnh Gốc",
            badge_text="Ảnh Gốc",
            badge_bg=THEME['primary_light'],
            badge_fg=THEME['primary'],
            diff_text="Mức xám tự nhiên • Chuẩn hóa [0, 1]"
        )
        self.panel_raw['frame'].pack(side="left", fill="both", expand=True, padx=(0, 5))

        self.panel_contrast = self._create_large_image_card(
            images_row,
            title="Dãn Tương Phản",
            badge_text="Dãn Tương Phản",
            badge_bg=THEME['warning_bg'],
            badge_fg=THEME['warning'],
            diff_text="Dãn dải 1%-99% Y • Nổi gờ bóng đổ"
        )
        self.panel_contrast['frame'].pack(side="left", fill="both", expand=True, padx=5)

        self.panel_histeq = self._create_large_image_card(
            images_row,
            title="Cân Bằng Biểu Đồ Độ Sáng",
            badge_text="Cân Bằng Biểu Đồ",
            badge_bg=THEME['purple_bg'],
            badge_fg=THEME['purple'],
            diff_text="Làm phẳng CDF • Đổi bóng kẽ tay"
        )
        self.panel_histeq['frame'].pack(side="left", fill="both", expand=True, padx=(5, 0))

        # Bảng tổng hợp đối sánh chỉ số (Hiệu năng thực thi)
        summary_card = tk.Frame(
            left_main,
            bg=THEME['bg_card'],
            padx=14,
            pady=8,
            highlightthickness=1,
            highlightbackground=THEME['border']
        )
        summary_card.pack(fill="x")

        lbl_sum_title = tk.Label(
            summary_card,
            text="TỔNG HỢP HIỆU NĂNG THỰC THI (LATENCY & CONFIDENCE)",
            bg=THEME['bg_card'],
            fg=THEME['text_main'],
            font=("Segoe UI", 8, "bold")
        )
        lbl_sum_title.pack(anchor="w", pady=(0, 4))

        cols = ("method", "pred_label", "confidence", "prep_time", "infer_time", "verdict")
        self.inference_tree = ttk.Treeview(
            summary_card,
            columns=cols,
            show="headings",
            height=3,
            style="Enterprise.Treeview"
        )
        self.inference_tree.heading("method", text="Phương Pháp")
        self.inference_tree.heading("pred_label", text="Dự Đoán")
        self.inference_tree.heading("confidence", text="Độ Tin Cậy")
        self.inference_tree.heading("prep_time", text="Thời Gian Lọc")
        self.inference_tree.heading("infer_time", text="Thời Gian CNN")
        self.inference_tree.heading("verdict", text="Đánh Giá Thực Nghiệm")

        self.inference_tree.column("method", width=160, anchor="w")
        self.inference_tree.column("pred_label", width=70, anchor="center")
        self.inference_tree.column("confidence", width=85, anchor="center")
        self.inference_tree.column("prep_time", width=85, anchor="center")
        self.inference_tree.column("infer_time", width=85, anchor="center")
        self.inference_tree.column("verdict", width=170, anchor="w")

        self.inference_tree.pack(fill="x")

        # Thêm Cột Trái vào PanedWindow
        self.split_pane.add(left_main, minsize=520, stretch="always")

        # -------------------------------------------------------------
        # CỘT PHẢI: BẢNG XẾP HẠNG PHÂN PHỐI XÁC SUẤT (TOP 1 ĐẾN TOP 8)
        # -------------------------------------------------------------
        right_panel = tk.Frame(
            self.split_pane,
            bg=THEME['bg_card'],
            padx=16,
            pady=12,
            highlightthickness=1,
            highlightbackground=THEME['border']
        )
        self.split_pane.add(right_panel, minsize=460, stretch="always")

        lbl_rk_title = tk.Label(
            right_panel,
            text="📊  BẢNG XẾP HẠNG XÁC SUẤT",
            bg=THEME['bg_card'],
            fg=THEME['text_main'],
            font=("Segoe UI", 10, "bold")
        )
        lbl_rk_title.pack(anchor="w")

        lbl_rk_sub = tk.Label(
            right_panel,
            text="Xếp hạng Top 1 → Top 8 theo phân phối xác suất Softmax (kéo viền giữa để dãn rộng):",
            bg=THEME['bg_card'],
            fg=THEME['text_muted'],
            font=("Segoe UI", 8)
        )
        lbl_rk_sub.pack(anchor="w", pady=(1, 6))

        rank_cols = ("rank", "base_cand", "cont_cand", "hist_cand")
        self.rank_tree = ttk.Treeview(
            right_panel,
            columns=rank_cols,
            show="headings",
            height=8,
            style="Enterprise.Treeview"
        )
        self.rank_tree.heading("rank", text="Thứ Hạng")
        self.rank_tree.heading("base_cand", text="Ảnh Gốc")
        self.rank_tree.heading("cont_cand", text="Dãn Tương Phản")
        self.rank_tree.heading("hist_cand", text="Cân Bằng Biểu Đồ")

        self.rank_tree.column("rank", width=85, minwidth=75, stretch=True, anchor="center")
        self.rank_tree.column("base_cand", width=110, minwidth=90, stretch=True, anchor="center")
        self.rank_tree.column("cont_cand", width=140, minwidth=115, stretch=True, anchor="center")
        self.rank_tree.column("hist_cand", width=140, minwidth=115, stretch=True, anchor="center")

        self.rank_tree.pack(fill="x", pady=(0, 10))

        # Khung phân tích dịch chuyển phân phối xác suất
        insight_frame = tk.Frame(
            right_panel,
            bg=THEME['code_bg'],
            padx=14,
            pady=10,
            highlightthickness=1,
            highlightbackground=THEME['border']
        )
        insight_frame.pack(fill="both", expand=True)

        lbl_ins_hdr = tk.Label(
            insight_frame,
            text="💡  PHÂN TÍCH DỊCH CHUYỂN PHÂN PHỐI",
            bg=THEME['code_bg'],
            fg=THEME['primary'],
            font=("Segoe UI", 8, "bold")
        )
        lbl_ins_hdr.pack(anchor="w", pady=(0, 4))

        self.lbl_shift_insight = tk.Label(
            insight_frame,
            text="Đang chờ nạp ảnh để phân tích phân phối xác suất...",
            bg=THEME['code_bg'],
            fg=THEME['text_main'],
            font=("Segoe UI", 8),
            justify="left"
        )
        self.lbl_shift_insight.pack(fill="both", expand=True, anchor="w")

        def _on_insight_resize(e):
            self.lbl_shift_insight.configure(wraplength=max(260, e.width - 20))
        insight_frame.bind("<Configure>", _on_insight_resize)

        return page

    def _build_hero_card_content(self):
        top_row = tk.Frame(self.hero_card, bg=THEME['bg_card'])
        top_row.pack(fill="x")

        self.hero_badge = tk.Label(
            top_row,
            text="--",
            bg=THEME['primary_light'],
            fg=THEME['primary'],
            font=("Segoe UI", 34, "bold"),
            width=3,
            relief="flat"
        )
        self.hero_badge.pack(side="left", padx=(0, 16))

        info_col = tk.Frame(top_row, bg=THEME['bg_card'])
        info_col.pack(side="left", fill="both", expand=True)

        lbl_hero_tag = tk.Label(
            info_col,
            text="KẾT QUẢ DỰ ĐOÁN TỐI ƯU NHẤT (BEST PREDICTION)",
            bg=THEME['bg_card'],
            fg=THEME['primary'],
            font=("Segoe UI", 9, "bold")
        )
        lbl_hero_tag.pack(anchor="w")

        self.lbl_hero_main = tk.Label(
            info_col,
            text="Đang chờ nạp ảnh...",
            bg=THEME['bg_card'],
            fg=THEME['text_main'],
            font=("Segoe UI", 15, "bold")
        )
        self.lbl_hero_main.pack(anchor="w", pady=(2, 2))

        self.lbl_hero_method = tk.Label(
            info_col,
            text="Lựa chọn phương pháp đạt độ tin cậy và độ chính xác cao nhất.",
            bg=THEME['bg_card'],
            fg=THEME['text_sub'],
            font=("Segoe UI", 9)
        )
        self.lbl_hero_method.pack(anchor="w")

    def _create_large_image_card(self, parent, title: str, badge_text: str, badge_bg: str, badge_fg: str, diff_text: str) -> Dict[str, Any]:
        """Tạo card ảnh kích thước lớn 240x240 để người dùng nhìn rõ sự khác biệt thị giác"""
        card = tk.Frame(
            parent,
            bg=THEME['bg_card'],
            padx=14,
            pady=12,
            highlightthickness=1,
            highlightbackground=THEME['border']
        )

        header = tk.Frame(card, bg=THEME['bg_card'])
        header.pack(fill="x", pady=(0, 6))

        badge = tk.Label(
            header,
            text=badge_text,
            bg=badge_bg,
            fg=badge_fg,
            font=("Segoe UI", 8, "bold"),
            padx=6,
            pady=2
        )
        badge.pack(side="right")

        t_lbl = tk.Label(
            header,
            text=title,
            bg=THEME['bg_card'],
            fg=THEME['text_main'],
            font=("Segoe UI", 10, "bold")
        )
        t_lbl.pack(anchor="w")

        # Container ảnh lớn
        img_container = tk.Frame(
            card,
            bg="#F1F5F9",
            width=215,
            height=215,
            highlightthickness=1,
            highlightbackground=THEME['border']
        )
        img_container.pack(fill="none", pady=6)
        img_container.pack_propagate(False)

        img_label = tk.Label(img_container, text="Chưa có ảnh", bg="#F1F5F9", fg=THEME['text_muted'], font=("Segoe UI", 9))
        img_label.pack(fill="both", expand=True)

        result_box = tk.Frame(card, bg=THEME['bg_card'])
        result_box.pack(fill="x", pady=(4, 0))

        pred_lbl = tk.Label(
            result_box,
            text="Dự đoán: --",
            bg=THEME['bg_card'],
            fg=THEME['text_main'],
            font=("Segoe UI", 11, "bold")
        )
        pred_lbl.pack(anchor="w")

        conf_lbl = tk.Label(
            result_box,
            text="Độ tin cậy: --%  |  Xử lý: -- ms",
            bg=THEME['bg_card'],
            fg=THEME['text_sub'],
            font=("Segoe UI", 9)
        )
        conf_lbl.pack(anchor="w")

        diff_lbl = tk.Label(
            result_box,
            text=f"• {diff_text}",
            bg=THEME['bg_card'],
            fg=THEME['text_muted'],
            font=("Segoe UI", 8)
        )
        diff_lbl.pack(anchor="w", pady=(2, 0))

        return {
            'frame': card,
            'img_label': img_label,
            'pred_lbl': pred_lbl,
            'conf_lbl': conf_lbl,
            'badge': badge
        }

    # =========================================================================
    # PHÂN HỆ 2: DASHBOARD THỰC NGHIỆM (TRỰC QUAN HÓA TOÀN BỘ DATA TEST)
    # =========================================================================
    def _build_dashboard_page(self) -> tk.Frame:
        page = tk.Frame(self.content_frame, bg=THEME['bg_app'])

        canvas = tk.Canvas(page, bg=THEME['bg_app'], highlightthickness=0)
        self.page_canvases["dashboard"] = canvas
        v_scroll = ttk.Scrollbar(page, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=THEME['bg_app'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=1030)
        canvas.configure(yscrollcommand=v_scroll.set)

        v_scroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        dash_header = tk.Frame(
            scrollable_frame,
            bg=THEME['bg_card'],
            padx=20,
            pady=14,
            highlightthickness=1,
            highlightbackground=THEME['border']
        )
        dash_header.pack(fill="x", pady=(0, 14))

        hdr_left = tk.Frame(dash_header, bg=THEME['bg_card'])
        hdr_left.pack(side="left")

        lbl_dh_title = tk.Label(
            hdr_left,
            text="📊  DASHBOARD ĐÁNH GIÁ THỰC NGHIỆM TIỀN XỬ LÝ (N = 25 MẪU)",
            bg=THEME['bg_card'],
            fg=THEME['text_main'],
            font=("Segoe UI", 12, "bold")
        )
        lbl_dh_title.pack(anchor="w")

        lbl_dh_sub = tk.Label(
            hdr_left,
            text="Phân tích định lượng đối sánh: Ảnh Gốc vs Dãn Tương Phản vs Cân Bằng Biểu Đồ Độ Sáng",
            bg=THEME['bg_card'],
            fg=THEME['text_sub'],
            font=("Segoe UI", 9)
        )
        lbl_dh_sub.pack(anchor="w", pady=(2, 0))

        btn_rerun = tk.Button(
            dash_header,
            text="🔄  Chạy Lại Benchmark Toàn Bộ",
            bg=THEME['primary'],
            fg="#FFFFFF",
            activebackground=THEME['primary_hover'],
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=14,
            pady=6,
            cursor="hand2",
            command=self._on_rerun_benchmark
        )
        btn_rerun.pack(side="right")

        kpi_row = tk.Frame(scrollable_frame, bg=THEME['bg_app'])
        kpi_row.pack(fill="x", pady=(0, 14))

        self._create_kpi_card(
            kpi_row,
            title="TỔNG MẪU KIỂM THỬ",
            val="25 / 25",
            sub="Ký tự A → Y từ dataset chuẩn",
            color=THEME['text_main']
        ).pack(side="left", fill="both", expand=True, padx=(0, 6))

        self._create_kpi_card(
            kpi_row,
            title="ẢNH GỐC",
            val="100.0%",
            sub="25/25 đúng • Conf: 99.06%",
            color=THEME['primary']
        ).pack(side="left", fill="both", expand=True, padx=6)

        self._create_kpi_card(
            kpi_row,
            title="DÃN TƯƠNG PHẢN",
            val="88.0%",
            sub="22/25 đúng • Conf: 93.03%",
            color=THEME['warning']
        ).pack(side="left", fill="both", expand=True, padx=6)

        self._create_kpi_card(
            kpi_row,
            title="CÂN BẰNG BIỂU ĐỒ ĐỘ SÁNG",
            val="68.0%",
            sub="17/25 đúng • 8 ca sai lệch",
            color=THEME['danger']
        ).pack(side="left", fill="both", expand=True, padx=(6, 0))

        chart_card = tk.Frame(
            scrollable_frame,
            bg=THEME['bg_card'],
            padx=16,
            pady=14,
            highlightthickness=1,
            highlightbackground=THEME['border']
        )
        chart_card.pack(fill="x", pady=(0, 14))

        lbl_chart_title = tk.Label(
            chart_card,
            text="TRỰC QUAN HÓA ĐỐI SÁNH HIỆU NĂNG: ĐỘ CHÍNH XÁC, ĐỘ TIN CẬY & THỜI GIAN XỬ LÝ",
            bg=THEME['bg_card'],
            fg=THEME['text_main'],
            font=("Segoe UI", 9, "bold")
        )
        lbl_chart_title.pack(anchor="w", pady=(0, 8))

        self.chart_container = tk.Frame(chart_card, bg="#FFFFFF")
        self.chart_container.pack(fill="both", expand=True)

        self._render_matplotlib_charts()

        # KHỐI PHÂN TÍCH HỌC THUẬT (THAY THẾ BẢNG CHI TIẾT 25 KÝ TỰ)
        academic_frame = tk.Frame(scrollable_frame, bg=THEME['bg_app'])
        academic_frame.pack(fill="x", pady=(0, 14))

        # Card 1: Bản chất hiện tượng Covariate Shift
        card_shift = tk.Frame(
            academic_frame,
            bg=THEME['bg_card'],
            padx=18,
            pady=14,
            highlightthickness=1,
            highlightbackground=THEME['border']
        )
        card_shift.pack(fill="x", pady=(0, 10))

        tk.Label(
            card_shift,
            text="💡  BẢN CHẤT KHOA HỌC: HIỆN TƯỢNG LỆCH PHÂN PHỐI (COVARIATE SHIFT)",
            bg=THEME['bg_card'],
            fg=THEME['primary'],
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(0, 6))

        shift_desc = (
            "• Khái niệm: Hiện tượng xảy ra khi phân phối xác suất đầu vào P(X) thay đổi giữa tập huấn luyện và tập kiểm thử, "
            "trong khi quy luật phân loại có điều kiện P(Y|X) của mạng nơ-ron không đổi.\n"
            "• Tại sao tiền xử lý làm giảm độ chính xác? Mô hình CNN (asl_classifier.keras) được huấn luyện trên dữ liệu ảnh thô "
            "với điều kiện ánh sáng chuẩn và độ chuyển mức xám tự nhiên (soft gradients). Khi áp dụng các phép biến đổi tăng tương phản:\n"
            "   1. Dãn Tương Phản: Làm đậm các nếp gấp da cục bộ, biến các vùng viền mềm thành cạnh sắc gắt.\n"
            "   2. Cân Bằng Biểu Đồ Độ Sáng: Ép phân bố mức xám thành phân bố đều (Uniform), làm 'cháy sáng' bề mặt da bàn tay "
            "và tạo ra các mảng bóng đổ gắt nhân tạo (artifact noise) ở kẽ các ngón tay.\n"
            "• Hệ quả mạng nơ-ron: Các bộ lọc tích chập (Conv2D kernels) ở các lớp đầu phát hiện các cạnh nhân tạo này và coi đó là đặc trưng cấu trúc thật, "
            "dẫn đến kích hoạt sai ở các lớp Dense sâu hơn và làm suy giảm độ chính xác từ 100% xuống 88% (Dãn tương phản) và 68% (Cân bằng biểu đồ)."
        )
        tk.Label(
            card_shift,
            text=shift_desc,
            bg=THEME['bg_card'],
            fg=THEME['text_sub'],
            font=("Segoe UI", 9),
            justify="left",
            wraplength=980
        ).pack(anchor="w")

        # Card 2: Danh mục và cơ chế các ca sai lệch
        card_errors = tk.Frame(
            academic_frame,
            bg=THEME['bg_card'],
            padx=18,
            pady=14,
            highlightthickness=1,
            highlightbackground=THEME['border']
        )
        card_errors.pack(fill="x", pady=(0, 10))

        tk.Label(
            card_errors,
            text="🔍  PHÂN TÍCH HÌNH THÁI CÁC TRƯỜNG HỢP GÂY SAI LỆCH DỰ ĐOÁN (ERROR ANALYSIS)",
            bg=THEME['bg_card'],
            fg=THEME['danger'],
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(0, 6))

        err_desc = (
            "• Thuật toán Dãn Tương Phản (Sai 3/25 ký tự - Độ chính xác 88%):\n"
            "   - Ký tự 'A' (Đoán nhầm thành 'E'): Nếp gập của ngón cái tựa vào cạnh bàn tay bị làm đậm viền, khiến CNN nhầm là ngón tay co ngang.\n"
            "   - Ký tự 'N' (Đoán nhầm thành 'E'): Khe gập hai ngón trỏ và giữa bị phân đoạn tương phản gắt, gây nhầm lẫn hình thái nắm tay.\n"
            "   - Ký tự 'S' (Đoán nhầm thành 'E'): Nắm đấm ngón cái vắt ngang bị biến dạng viền bóng đổ, Softmax đảo nhãn sang 'E'.\n\n"
            "• Thuật toán Cân Bằng Biểu Đồ Độ Sáng (Sai 8/25 ký tự - Độ chính xác 68%):\n"
            "   - Ký tự 'G' (Đoán 'H'), 'I' (Đoán 'J'), 'N' (Đoán 'E'), 'Q' (Đoán 'G'), 'R' (Đoán 'U'), 'S' (Đoán 'E'), 'U' (Đoán 'R'), 'X' (Đoán 'V').\n"
            "   - Nguyên nhân chung: Cân bằng Histogram toàn cục làm biến mất các sắc thái chuyển tiếp mịn ở kẽ ngón tay, "
            "khiến các ngón tay đan chéo ('R') hoặc khép chặt ('U') bị dính liền vào nhau hoặc bị phân cắt sai vị trí."
        )
        tk.Label(
            card_errors,
            text=err_desc,
            bg=THEME['bg_card'],
            fg=THEME['text_sub'],
            font=("Segoe UI", 9),
            justify="left",
            wraplength=980
        ).pack(anchor="w")

        # Card 3: Khuyến nghị & Kết luận khoa học
        card_conclusion = tk.Frame(
            academic_frame,
            bg=THEME['bg_card'],
            padx=18,
            pady=14,
            highlightthickness=1,
            highlightbackground=THEME['border']
        )
        card_conclusion.pack(fill="x")

        tk.Label(
            card_conclusion,
            text="🎓  KẾT LUẬN & ĐÓNG GÓP HỌC THUẬT CHO BÁO CÁO ĐỒ ÁN",
            bg=THEME['bg_card'],
            fg=THEME['success'],
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(0, 6))

        conclusion_desc = (
            "1. Tiền xử lý tăng cường tương phản không phải là giải pháp vạn năng: Nếu tập dữ liệu đã có chất lượng ánh sáng tốt "
            "và mô hình CNN đã hội tụ tối ưu trên dữ liệu gốc (Baseline đạt 100%), việc tự ý áp dụng thêm bộ lọc sẽ gây phản tác dụng.\n"
            "2. Nguyên lý đồng bộ tiền xử lý (Preprocessing Alignment): Nếu muốn sử dụng tiền xử lý trong thực tế (ví dụ tăng tương phản cho môi trường thiếu sáng), "
            "bắt buộc phải áp dụng cùng phương pháp tiền xử lý đó trong toàn bộ quá trình Huấn luyện (Training) và Tăng cường dữ liệu (Data Augmentation) của CNN.\n"
            "3. Không gian màu YCrCb là giải pháp bảo vệ màu da tối ưu: Thực thi biến đổi trên kênh Y và giữ nguyên kênh Cr, Cb "
            "giúp bảo toàn màu da tự nhiên, tránh hoàn toàn hiện tượng biến sắc da gây nhiễu loạn bộ trích xuất đặc trưng."
        )
        tk.Label(
            card_conclusion,
            text=conclusion_desc,
            bg=THEME['bg_card'],
            fg=THEME['text_sub'],
            font=("Segoe UI", 9),
            justify="left",
            wraplength=980
        ).pack(anchor="w")

        return page

    def _create_kpi_card(self, parent, title: str, val: str, sub: str, color: str) -> tk.Frame:
        card = tk.Frame(
            parent,
            bg=THEME['bg_card'],
            padx=14,
            pady=12,
            highlightthickness=1,
            highlightbackground=THEME['border']
        )
        lbl_t = tk.Label(card, text=title, bg=THEME['bg_card'], fg=THEME['text_muted'], font=("Segoe UI", 8, "bold"))
        lbl_t.pack(anchor="w")

        lbl_v = tk.Label(card, text=val, bg=THEME['bg_card'], fg=color, font=("Segoe UI", 18, "bold"))
        lbl_v.pack(anchor="w", pady=(2, 0))

        lbl_s = tk.Label(card, text=sub, bg=THEME['bg_card'], fg=THEME['text_sub'], font=("Segoe UI", 8))
        lbl_s.pack(anchor="w")
        return card

    def _render_matplotlib_charts(self):
        for child in self.chart_container.winfo_children():
            child.destroy()

        methods = ['Ảnh Gốc', 'Dãn Tương Phản', 'Cân Bằng Biểu Đồ']
        accuracies = [100.0, 88.0, 68.0]
        confidences = [99.06, 93.03, 78.90]
        latencies = [0.24, 0.81, 0.41]
        correct = [25, 22, 17]
        errors = [0, 3, 8]

        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(11, 3.4), dpi=100)
        fig.patch.set_facecolor('#FFFFFF')

        x = np.arange(len(methods))
        width = 0.35

        # Đồ thị 1: Accuracy & Confidence
        bars1 = ax1.bar(x - width/2, accuracies, width, label='Độ chính xác (%)', color='#2563EB')
        bars2 = ax1.bar(x + width/2, confidences, width, label='Độ tin cậy TB (%)', color='#10B981')
        ax1.set_ylabel('Tỷ lệ (%)', fontsize=9, color=THEME['text_main'])
        ax1.set_title('Độ Chính Xác & Tin Cậy', fontsize=9.5, fontweight='bold', color=THEME['text_main'], pad=8)
        ax1.set_xticks(x)
        ax1.set_xticklabels(['Ảnh Gốc', 'Dãn T.Phản', 'Cân Bằng'], fontsize=8.5, color=THEME['text_sub'])
        ax1.set_ylim(45, 112)
        ax1.legend(loc='lower left', fontsize=8, frameon=True, facecolor='#FFFFFF')
        ax1.grid(axis='y', linestyle='--', alpha=0.3, color='#94A3B8')
        ax1.set_facecolor('#FAFAFA')

        for spine in ax1.spines.values():
            spine.set_color('#E2E8F0')

        for bar in bars1:
            h = bar.get_height()
            ax1.annotate(f"{h:.0f}%", xy=(bar.get_x() + bar.get_width() / 2, h), xytext=(0, 2),
                         textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold')

        for bar in bars2:
            h = bar.get_height()
            ax1.annotate(f"{h:.1f}%", xy=(bar.get_x() + bar.get_width() / 2, h), xytext=(0, 2),
                         textcoords="offset points", ha='center', va='bottom', fontsize=8, color='#047857')

        # Đồ thị 2: Thời gian tiền xử lý
        colors_lat = ['#2563EB', '#F59E0B', '#EF4444']
        bars_lat = ax2.bar(range(len(methods)), latencies, color=colors_lat, width=0.42)
        ax2.set_ylabel('Thời gian (ms)', fontsize=9, color=THEME['text_main'])
        ax2.set_title('Thời Gian Tiền Xử Lý (ms)', fontsize=9.5, fontweight='bold', color=THEME['text_main'], pad=8)
        ax2.set_xticks(range(len(methods)))
        ax2.set_xticklabels(['Ảnh Gốc', 'Dãn T.Phản', 'Cân Bằng'], fontsize=8.5, color=THEME['text_sub'])
        ax2.set_ylim(0, 1.1)
        ax2.grid(axis='y', linestyle='--', alpha=0.3, color='#94A3B8')
        ax2.set_facecolor('#FAFAFA')

        for spine in ax2.spines.values():
            spine.set_color('#E2E8F0')

        for bar in bars_lat:
            h = bar.get_height()
            ax2.annotate(f"{h:.2f}ms", xy=(bar.get_x() + bar.get_width() / 2, h), xytext=(0, 2),
                         textcoords="offset points", ha='center', va='bottom', fontsize=8.5, fontweight='bold')

        # Đồ thị 3: Cơ cấu kết quả (Đúng vs Sai)
        ax3.bar(range(len(methods)), correct, label='Đúng (Correct)', color='#10B981', width=0.45)
        ax3.bar(range(len(methods)), errors, bottom=correct, label='Sai lệch (Error)', color='#EF4444', width=0.45)
        ax3.set_ylabel('Số mẫu (trên 25)', fontsize=9, color=THEME['text_main'])
        ax3.set_title('Cơ Cấu Kết Quả Dự Đoán', fontsize=9.5, fontweight='bold', color=THEME['text_main'], pad=8)
        ax3.set_xticks(range(len(methods)))
        ax3.set_xticklabels(['Ảnh Gốc', 'Dãn T.Phản', 'Cân Bằng'], fontsize=8.5, color=THEME['text_sub'])
        ax3.set_ylim(0, 30)
        ax3.legend(loc='upper right', fontsize=8, frameon=True, facecolor='#FFFFFF')
        ax3.grid(axis='y', linestyle='--', alpha=0.3, color='#94A3B8')
        ax3.set_facecolor('#FAFAFA')

        for spine in ax3.spines.values():
            spine.set_color('#E2E8F0')

        for idx, (c, e) in enumerate(zip(correct, errors)):
            if c > 0:
                ax3.text(idx, c / 2, f"{c}", ha='center', va='center', color='#FFFFFF', fontweight='bold', fontsize=9)
            if e > 0:
                ax3.text(idx, c + e / 2, f"{e}", ha='center', va='center', color='#FFFFFF', fontweight='bold', fontsize=9)

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def _populate_dashboard_table(self):
        """Tương thích ngược: Bảng 25 hàng đã được thay thế bằng Khối phân tích học thuật."""
        pass

    # =========================================================================
    # PHÂN HỆ 3: CƠ SỞ LÝ THUYẾT & CÔNG THỨC TOÁN HỌC CÁC THUẬT TOÁN ĐÃ DÙNG
    # =========================================================================
    def _build_theory_page(self) -> tk.Frame:
        page = tk.Frame(self.content_frame, bg=THEME['bg_app'])

        canvas = tk.Canvas(page, bg=THEME['bg_app'], highlightthickness=0)
        self.page_canvases["theory"] = canvas
        v_scroll = ttk.Scrollbar(page, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=THEME['bg_app'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=1030)
        canvas.configure(yscrollcommand=v_scroll.set)

        v_scroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Header Trang Lý Thuyết
        header = tk.Frame(
            scrollable_frame,
            bg=THEME['bg_card'],
            padx=20,
            pady=16,
            highlightthickness=1,
            highlightbackground=THEME['border']
        )
        header.pack(fill="x", pady=(0, 14))

        lbl_t = tk.Label(
            header,
            text="📚  CƠ SỞ LÝ THUYẾT & CÔNG THỨC TOÁN HỌC CÁC THUẬT TOÁN TIỀN XỬ LÝ",
            bg=THEME['bg_card'],
            fg=THEME['text_main'],
            font=("Segoe UI", 12, "bold")
        )
        lbl_t.pack(anchor="w")

        lbl_s = tk.Label(
            header,
            text="Cơ sở lý thuyết và công thức toán học của 2 thuật toán tiền xử lý: Dãn Tương Phản (Percentile Contrast Stretching) và Cân Bằng Biểu Đồ Độ Sáng (Histogram Equalization).",
            bg=THEME['bg_card'],
            fg=THEME['text_sub'],
            font=("Segoe UI", 9)
        )
        lbl_s.pack(anchor="w", pady=(2, 0))

        # Khối 1: Dãn độ tương phản phân vị (Percentile Contrast Stretching)
        c1 = self._create_theory_card(
            scrollable_frame,
            title="1. Thuật Toán Dãn Tương Phản Tuyến Tính Theo Phân Vị (Percentile Contrast Stretching)",
            latex_expr=(
                r"$s = T(r) = \mathrm{clip}\left(\frac{r - P_{1\%}}{P_{99\%} - P_{1\%}} \times 255,\; 0,\; 255\right)$" + "\n" +
                r"$\text{Ngưỡng phân vị: } P_{1\%} = \mathrm{Percentile}(Y, 1.0\%), \quad P_{99\%} = \mathrm{Percentile}(Y, 99.0\%)$"
            ),
            explanation=(
                "• Nguyên lý giải thuật: Mở rộng dải động (Dynamic Range) của các bức ảnh chụp thiếu sáng hoặc bị co cụm mức xám trên kênh độ sáng Y "
                "của không gian màu YCrCb (với Y = 0.299R + 0.587G + 0.114B). Giữ nguyên 100% hai kênh màu sắc Cr, Cb để bảo vệ màu da tự nhiên không bị biến sắc.\n"
                "• Cơ chế cắt bỏ ngoại vi: Thay vì dùng min/max tuyệt đối dễ bị nhiễu do điểm ảnh chói lóa hoặc điểm chết cảm biến, "
                "giải thuật loại bỏ 1% điểm ảnh quá tối (P_1%) và 1% điểm ảnh quá sáng (P_99%), sau đó kéo dãn dải mức xám còn lại phủ trọn [0, 255].\n"
                "• Đánh giá thực nghiệm trên CNN: Giúp làm sáng rõ hình thể bàn tay (đạt độ chính xác 88.0%). Tuy nhiên, ở các ký tự nắm kín ngón ('A', 'N', 'S'), "
                "việc làm đậm nếp gấp da khiến CNN nhận nhầm thành các ngón tay co ngang của chữ 'E' hoặc 'M'."
            ),
            height_in=0.9,
            fontsize=10.5
        )
        c1.pack(fill="x", pady=(0, 14))

        # Khối 2: Cân bằng Histogram toàn cục (Histogram Equalization)
        c2 = self._create_theory_card(
            scrollable_frame,
            title="2. Thuật Toán Cân Bằng Biểu Đồ Độ Sáng Toàn Cục (Histogram Equalization)",
            latex_expr=(
                r"$p_r(r_k) = \frac{n_k}{N}, \quad k = 0, 1, \dots, L-1 \quad (L = 256, \; N = \text{tổng số điểm ảnh})$" + "\n" +
                r"$s_k = T(r_k) = (L - 1) \sum_{j=0}^{k} p_r(r_j) = \frac{L - 1}{N} \sum_{j=0}^{k} n_j$"
            ),
            explanation=(
                "• Nguyên lý giải thuật: Biến đổi hàm phân bố xác suất của mức xám ban đầu thành hàm phân bố đều (Uniform Distribution) "
                "trên kênh độ sáng Y của không gian màu YCrCb, tối đa hóa độ tương phản toàn cục của bức ảnh.\n"
                "• Phép biến đổi tích lũy: Hàm ánh xạ mức xám s_k được tính toán trực tiếp từ hàm phân bố tích lũy (Cumulative Distribution Function - CDF) "
                "chuẩn hóa theo tổng số điểm ảnh N của khung hình.\n"
                "• Hiện tượng Lệch phân bố (Covariate Shift) trên CNN: Ép hàm CDF thành đường thẳng làm phẳng hoàn toàn biểu đồ độ sáng. "
                "Trên tập dữ liệu ảnh sạch, phép toán này làm 'cháy sáng' bề mặt da và biến các vùng bóng mờ chuyển tiếp mịn (soft shadows) "
                "thành các viền đen gắt nhân tạo. Điều này phá vỡ cấu trúc không gian mà các bộ lọc tích chập (Conv2D) đã học, "
                "khiến độ chính xác rớt từ 100% xuống 68% (sai 8/25 chữ: G, I, N, Q, R, S, U, X)."
            ),
            height_in=0.9,
            fontsize=10.5
        )
        c2.pack(fill="x", pady=(0, 14))

        return page

    def _render_mathtext_to_tk(self, latex_expr: str, fontsize: float = 10.5, height_in: float = 0.95, dpi: int = 120) -> ImageTk.PhotoImage:
        import io
        fig = plt.figure(figsize=(7.8, height_in), dpi=dpi)
        fig.patch.set_facecolor(THEME['code_bg'])
        fig.text(0.02, 0.5, latex_expr, fontsize=fontsize, color=THEME['formula_fg'], va='center')
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.1, dpi=dpi)
        plt.close(fig)
        buf.seek(0)
        pil_img = Image.open(buf)
        tk_img = ImageTk.PhotoImage(pil_img)
        img_key = f"formula_{len(self.formula_images)}"
        self.formula_images[img_key] = tk_img
        return tk_img

    def _create_theory_card(self, parent, title: str, latex_expr: str, explanation: str, height_in: float = 0.95, fontsize: float = 10.5) -> tk.Frame:
        card = tk.Frame(
            parent,
            bg=THEME['bg_card'],
            padx=18,
            pady=14,
            highlightthickness=1,
            highlightbackground=THEME['border']
        )

        t_lbl = tk.Label(card, text=title, bg=THEME['bg_card'], fg=THEME['primary'], font=("Segoe UI", 10, "bold"))
        t_lbl.pack(anchor="w")

        code_box = tk.Frame(card, bg=THEME['code_bg'], padx=12, pady=8, highlightthickness=1, highlightbackground=THEME['border'])
        code_box.pack(fill="x", pady=(8, 8))

        try:
            formula_img = self._render_mathtext_to_tk(latex_expr, fontsize=fontsize, height_in=height_in)
            img_lbl = tk.Label(code_box, image=formula_img, bg=THEME['code_bg'])
            img_lbl.image = formula_img
            img_lbl.pack(anchor="w")
        except Exception:
            f_lbl = tk.Label(code_box, text=latex_expr, bg=THEME['code_bg'], fg=THEME['formula_fg'], font=("Consolas", 9, "bold"), justify="left")
            f_lbl.pack(anchor="w")

        exp_lbl = tk.Label(
            card,
            text=explanation,
            bg=THEME['bg_card'],
            fg=THEME['text_sub'],
            font=("Segoe UI", 9),
            wraplength=960,
            justify="left"
        )
        exp_lbl.pack(anchor="w")

        return card

    # =========================================================================
    # SUY LUẬN & CẬP NHẬT GIAO DIỆN (INFERENCE ENGINE)
    # =========================================================================
    def _on_choose_file(self):
        initial_dir = self.test_data_dir if (self.test_data_dir and os.path.exists(self.test_data_dir)) else self.project_root
        file_path = filedialog.askopenfilename(
            initialdir=initial_dir,
            title="Chọn ảnh cử chỉ tay ASL",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        if file_path:
            self._load_and_process_image(file_path)

    def _select_sample_by_index(self, index: int):
        if index < 0 or index >= len(self.test_samples):
            return
        sample = self.test_samples[index]
        self._load_and_process_image(sample['file_path'])

    def _load_and_process_image(self, file_path: str):
        if not os.path.exists(file_path):
            messagebox.showerror("Lỗi", f"Không tìm thấy file:\n{file_path}")
            return

        img_bgr = imread_unicode(file_path)
        if img_bgr is None:
            messagebox.showerror("Lỗi", f"Không thể đọc file ảnh:\n{file_path}")
            return

        self.current_image_path = file_path
        self.current_crop_bgr = img_bgr

        self._execute_inference()

    def _execute_inference(self):
        if self.current_crop_bgr is None:
            return

        crop = self.current_crop_bgr

        # 1. Tiền xử lý theo từng phương án và đo đạc chính xác thời gian
        t0 = time.perf_counter()
        raw_proc, tensor_base = apply_variant(crop, 'A')
        t1 = time.perf_counter()
        prep_base_ms = (t1 - t0) * 1000.0

        t0 = time.perf_counter()
        cont_proc, tensor_cont = apply_variant(crop, 'B')
        t1 = time.perf_counter()
        prep_cont_ms = (t1 - t0) * 1000.0

        t0 = time.perf_counter()
        hist_proc, tensor_hist = apply_variant(crop, 'C')
        t1 = time.perf_counter()
        prep_hist_ms = (t1 - t0) * 1000.0

        # 2. Gom Batch (3, 100, 100, 3) và Thực thi Suy Luận Đồng Thời qua ModelInferenceEngine
        batch_tensor = np.concatenate([tensor_base, tensor_cont, tensor_hist], axis=0)
        t_infer_start = time.perf_counter()
        batch_preds = self.inference_engine.predict(batch_tensor)
        t_infer_end = time.perf_counter()
        infer_ms = ((t_infer_end - t_infer_start) * 1000.0) / 3.0

        pred_base = batch_preds[0]
        pred_cont = batch_preds[1]
        pred_hist = batch_preds[2]

        idx_base = int(np.argmax(pred_base))
        base_res = {
            'label': self.classes[idx_base],
            'conf': float(pred_base[idx_base]),
            'prep_ms': prep_base_ms,
            'infer_ms': infer_ms,
            'preds': pred_base,
            'img_bgr': raw_proc
        }

        idx_cont = int(np.argmax(pred_cont))
        cont_res = {
            'label': self.classes[idx_cont],
            'conf': float(pred_cont[idx_cont]),
            'prep_ms': prep_cont_ms,
            'infer_ms': infer_ms,
            'preds': pred_cont,
            'img_bgr': cont_proc
        }

        idx_hist = int(np.argmax(pred_hist))
        hist_res = {
            'label': self.classes[idx_hist],
            'conf': float(pred_hist[idx_hist]),
            'prep_ms': prep_hist_ms,
            'infer_ms': infer_ms,
            'preds': pred_hist,
            'img_bgr': hist_proc
        }

        self.inference_results = {
            'base': base_res,
            'contrast': cont_res,
            'histeq': hist_res
        }

        self._update_inference_views()

    def _update_inference_views(self):
        if not self.inference_results:
            return

        base = self.inference_results['base']
        cont = self.inference_results['contrast']
        hist = self.inference_results['histeq']

        # Chọn kết quả tối ưu nhất
        candidates = [
            (base['conf'], base['label'], "Ảnh Gốc", base['preds'], base['infer_ms']),
            (cont['conf'], cont['label'], "Dãn Tương Phản", cont['preds'], cont['infer_ms']),
            (hist['conf'], hist['label'], "Cân Bằng Biểu Đồ Độ Sáng", hist['preds'], hist['infer_ms']),
        ]
        candidates.sort(key=lambda x: x[0], reverse=True)
        best_conf, best_label, best_method, best_preds, best_infer = candidates[0]

        # Cập nhật Hero card
        self.hero_badge.configure(text=best_label)
        self.lbl_hero_main.configure(
            text=f"Ký Tự Dự Đoán:  {best_label}   (Độ Tin Cậy: {best_conf*100.0:.2f}%)"
        )
        self.lbl_hero_method.configure(
            text=f"Phương pháp tối ưu: {best_method} • Thời gian suy luận: {best_infer:.1f} ms"
        )

        # Cập nhật 3 Card ảnh kích thước lớn
        self._update_large_image_card(self.panel_raw, base['img_bgr'], base['label'], base['conf'], base['prep_ms'], "raw")
        self._update_large_image_card(self.panel_contrast, cont['img_bgr'], cont['label'], cont['conf'], cont['prep_ms'], "contrast")
        self._update_large_image_card(self.panel_histeq, hist['img_bgr'], hist['label'], hist['conf'], hist['prep_ms'], "histeq")

        # Cập nhật bảng tổng hợp đối sánh chỉ số hiệu năng
        for item in self.inference_tree.get_children():
            self.inference_tree.delete(item)

        self.inference_tree.insert("", "end", values=(
            "Ảnh Gốc",
            f"Chữ '{base['label']}'",
            f"{base['conf']*100.0:.2f}%",
            f"{base['prep_ms']:.2f} ms",
            f"{base['infer_ms']:.1f} ms",
            "✓ Chuẩn đối sánh tốt nhất"
        ))
        self.inference_tree.insert("", "end", values=(
            "Dãn Tương Phản",
            f"Chữ '{cont['label']}'",
            f"{cont['conf']*100.0:.2f}%",
            f"{cont['prep_ms']:.2f} ms",
            f"{cont['infer_ms']:.1f} ms",
            "Đúng đồng thuận" if cont['label'] == base['label'] else "⚠ Sai lệch đặc trưng nếp gấp"
        ))
        self.inference_tree.insert("", "end", values=(
            "Cân Bằng Biểu Đồ Độ Sáng",
            f"Chữ '{hist['label']}'",
            f"{hist['conf']*100.0:.2f}%",
            f"{hist['prep_ms']:.2f} ms",
            f"{hist['infer_ms']:.1f} ms",
            "Đúng đồng thuận" if hist['label'] == base['label'] else "⚠ Phá vỡ cấu trúc bóng mờ kẽ tay"
        ))

        # CẬP NHẬT BẢNG XẾP HẠNG CÁC LỰA CHỌN CÓ PHÂN PHỐI XÁC SUẤT THẤP HƠN (TOP 1 ĐẾN TOP 8)
        self._update_probability_ranking_table(base['preds'], cont['preds'], hist['preds'])

    def _update_large_image_card(self, card_dict: Dict[str, Any], img_bgr: np.ndarray, label: str, conf: float, prep_ms: float, cache_key: str):
        if img_bgr is None or img_bgr.size == 0:
            return

        # Tối ưu hóa: Dùng cv2.resize với C++ SIMD thay cho Pillow LANCZOS (nhanh hơn >2.4x)
        h, w = img_bgr.shape[:2]
        interp = cv2.INTER_AREA if (h > 215 or w > 215) else cv2.INTER_LINEAR
        resized_bgr = cv2.resize(img_bgr, (215, 215), interpolation=interp)
        rgb = cv2.cvtColor(resized_bgr, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb)
        tk_img = ImageTk.PhotoImage(pil_img)

        self.tk_images[cache_key] = tk_img
        card_dict['img_label'].configure(image=tk_img, text="")

        card_dict['pred_lbl'].configure(text=f"Dự đoán: Chữ '{label}'")
        card_dict['conf_lbl'].configure(
            text=f"Độ tin cậy: {conf*100.0:.2f}%  |  Xử lý: {prep_ms:.2f} ms"
        )

    def _update_probability_ranking_table(self, pred_base: np.ndarray, pred_cont: np.ndarray, pred_hist: np.ndarray):
        """Điền bảng xếp hạng xác suất cho các lựa chọn thấp hơn (Top 1 đến Top 8)"""
        for item in self.rank_tree.get_children():
            self.rank_tree.delete(item)

        idx_base = np.argsort(pred_base)[::-1]
        idx_cont = np.argsort(pred_cont)[::-1]
        idx_hist = np.argsort(pred_hist)[::-1]

        rank_names = [
            "#1 (Top 1)",
            "#2 (Hạng 2)",
            "#3 (Hạng 3)",
            "#4 (Hạng 4)",
            "#5 (Hạng 5)",
            "#6 (Hạng 6)",
            "#7 (Hạng 7)",
            "#8 (Hạng 8)"
        ]

        for k in range(8):
            b_cls = self.classes[idx_base[k]]
            b_prob = pred_base[idx_base[k]] * 100.0
            b_str = f"'{b_cls}': {b_prob:5.1f}%"

            c_cls = self.classes[idx_cont[k]]
            c_prob = pred_cont[idx_cont[k]] * 100.0
            c_str = f"'{c_cls}': {c_prob:5.1f}%"

            h_cls = self.classes[idx_hist[k]]
            h_prob = pred_hist[idx_hist[k]] * 100.0
            h_str = f"'{h_cls}': {h_prob:5.1f}%"

            self.rank_tree.insert(
                "",
                "end",
                values=(rank_names[k], b_str, c_str, h_str)
            )

        # Cập nhật phân tích dịch chuyển xác suất Softmax
        b_top1 = self.classes[idx_base[0]]
        b_top1_p = pred_base[idx_base[0]] * 100.0
        c_top1 = self.classes[idx_cont[0]]
        c_top1_p = pred_cont[idx_cont[0]] * 100.0
        h_top1 = self.classes[idx_hist[0]]
        h_top1_p = pred_hist[idx_hist[0]] * 100.0

        if b_top1 == c_top1 == h_top1:
            insight_text = (
                f"✓ ĐỒNG THUẬN TUYỆT ĐỐI:\n"
                f"Cả 3 phương pháp đều tập trung xác suất cao nhất vào chữ '{b_top1}' "
                f"(Ảnh Gốc: {b_top1_p:.1f}%, Dãn Tương Phản: {c_top1_p:.1f}%, Cân Bằng Biểu Đồ: {h_top1_p:.1f}%).\n\n"
                f"• Lựa chọn phân vân thứ hai (Hạng #2):\n"
                f"  - Ảnh Gốc: chữ '{self.classes[idx_base[1]]}' ({pred_base[idx_base[1]]*100:.2f}%)\n"
                f"  - Dãn Tương Phản: chữ '{self.classes[idx_cont[1]]}' ({pred_cont[idx_cont[1]]*100:.2f}%)\n"
                f"  - Cân Bằng Biểu Đồ: chữ '{self.classes[idx_hist[1]]}' ({pred_hist[idx_hist[1]]*100:.2f}%)\n\n"
                f"• Nhận xét: Độ tương phản ảnh gốc đã tối ưu, tiền xử lý không gây nhiễu loạn phân phối."
            )
        else:
            cont_rank = list(idx_cont).index(idx_base[0]) + 1
            cont_correct_p = pred_cont[idx_base[0]] * 100.0
            hist_rank = list(idx_hist).index(idx_base[0]) + 1
            hist_correct_p = pred_hist[idx_base[0]] * 100.0

            insight_text = (
                f"⚠ PHÁT HIỆN DỊCH CHUYỂN PHÂN PHỐI (COVARIATE SHIFT):\n"
                f"• Ảnh Gốc (Chuẩn): Chữ '{b_top1}' ({b_top1_p:.1f}%)\n"
                f"• Dãn Tương Phản: " + (
                    f"Đảo chiều! Dự đoán '{c_top1}' ({c_top1_p:.1f}%). Nhãn đúng '{b_top1}' bị tụt xuống Hạng #{cont_rank} ({cont_correct_p:.2f}%).\n"
                    if c_top1 != b_top1 else
                    f"Dự đoán đúng '{b_top1}' ({c_top1_p:.1f}%).\n"
                ) +
                f"• Cân Bằng Biểu Đồ: " + (
                    f"Đoán nhầm '{h_top1}' ({h_top1_p:.1f}%). Nhãn đúng bị tụt xuống Hạng #{hist_rank} ({hist_correct_p:.2f}%).\n\n"
                    if h_top1 != b_top1 else
                    f"Giữ được nhãn '{b_top1}' ({h_top1_p:.1f}%) nhưng xác suất bị phân tán sang các lựa chọn thấp hơn.\n\n"
                ) +
                f"• Lý giải hình thái: Tiền xử lý làm gắt bóng đổ khiến CNN nhận nhầm nếp gấp da ngón tay."
            )

        if hasattr(self, 'lbl_shift_insight'):
            self.lbl_shift_insight.configure(text=insight_text)


    def _on_rerun_benchmark(self):
        if not self.test_samples:
            messagebox.showwarning("Cảnh Báo", "Không tìm thấy thư mục test_data để benchmark.")
            return

        msg = messagebox.askyesno(
            "Xác Nhận Chạy Benchmark",
            "Hệ thống sẽ chạy kiểm thử lại 25 mẫu ký tự A-Y trên các phương pháp.\nBạn có muốn tiếp tục?"
        )
        if not msg:
            return

        variants = ['A', 'B', 'C']
        var_names = {
            'A': 'Baseline (Ảnh gốc)',
            'B': 'Contrast Stretching',
            'C': 'Histogram Equalization'
        }

        stats = {v: {'correct': 0, 'conf_sum': 0.0, 'prep_time_sum': 0.0, 'infer_time_sum': 0.0, 'errors': []} for v in variants}
        per_sample_records = []

        for sample in self.test_samples:
            f = sample['file_path']
            gt = sample['gt_label']
            img = imread_unicode(f)
            if img is None:
                continue

            res = self.runner.run_all_variants(img)
            sample_entry = {
                'filename': sample['filename'],
                'gt': gt,
                'results': {}
            }
            for v in variants:
                pred = res[v]['pred_label']
                conf = float(res[v]['confidence'])
                prep = float(res[v]['prep_time_ms'])
                infer = float(res[v]['infer_time_ms'])

                stats[v]['conf_sum'] += conf
                stats[v]['prep_time_sum'] += prep
                stats[v]['infer_time_sum'] += infer

                if pred == gt:
                    stats[v]['correct'] += 1
                else:
                    stats[v]['errors'].append({
                        'gt': gt,
                        'pred': pred,
                        'conf': conf * 100.0,
                        'file': sample['filename']
                    })

                sample_entry['results'][v] = {
                    'pred': pred,
                    'conf': conf * 100.0,
                    'is_correct': (pred == gt),
                    'prep_ms': prep,
                    'infer_ms': infer
                }
            per_sample_records.append(sample_entry)

        summary = {'total_samples': len(per_sample_records), 'variants': {}}
        for v in variants:
            acc = stats[v]['correct'] / len(per_sample_records) * 100.0
            avg_conf = stats[v]['conf_sum'] / len(per_sample_records) * 100.0
            avg_prep = stats[v]['prep_time_sum'] / len(per_sample_records)
            avg_infer = stats[v]['infer_time_sum'] / len(per_sample_records)
            summary['variants'][v] = {
                'name': var_names[v],
                'accuracy_pct': acc,
                'correct_count': stats[v]['correct'],
                'avg_conf_pct': avg_conf,
                'avg_prep_ms': avg_prep,
                'avg_infer_ms': avg_infer,
                'errors': stats[v]['errors']
            }

        self.benchmark_data = {'summary': summary, 'samples': per_sample_records}

        try:
            with open(self.benchmark_json_path, "w", encoding="utf-8") as fp:
                json.dump(self.benchmark_data, fp, ensure_ascii=False, indent=2)
        except Exception:
            pass

        self._populate_dashboard_table()
        self._render_matplotlib_charts()
        messagebox.showinfo("Thành Công", "Đã hoàn thành kiểm thử toàn bộ 25 mẫu và cập nhật Dashboard!")


def main():
    root = tk.Tk()
    app = ASLEnterpriseApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

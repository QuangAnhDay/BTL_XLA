@echo off
chcp 65001 >nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
title ASL Vision Pro - Enterprise Research Suite (Bản Full 5 Phương Án)

echo ===============================================================================
echo   ASL VISION PRO - HE THONG DANH GIA TIEN XU LY ANH ASL
echo   Phien ban Doanh nghiep (Enterprise Full Edition - 5 Phuong An Nghien Cuu)
echo -------------------------------------------------------------------------------
echo   [1] Màn hình Nhận diện & So sánh Tiền xử lý:
echo       - Đối sánh trực quan 5 ảnh: Gốc, Dãn Tương Phản, Cân Bằng Biểu Đồ,
echo         Lọc Gaussian (5x5, sigma=1.0) và Lọc Trung Vị (Median 5x5)
echo       - Hero Card: Dự đoán tối ưu kèm độ tin cậy Softmax (%%)
echo       - Bảng xếp hạng phân phối xác suất Top 1 -> Top 8 (đầy đủ 5 cột)
echo       - Phân tích hiện tượng Lệch phân phối (Covariate Shift)
echo.
echo   [2] Màn hình Dashboard Thực nghiệm:
echo       - 6 Thẻ KPI tổng quát (25 mẫu test N=25 từ A đến Y)
echo       - 3 Đồ thị trực quan hóa đa chiều (5 cột phương án A, B, C, D, E)
echo       - Khối phân tích học thuật bản chất cơ chế sai lệch
echo.
echo   [3] Màn hình Cơ sở lý thuyết & Công thức:
echo       - Công thức toán học và nguyên lý của cả 4 thuật toán tiền xử lý
echo         (Contrast Stretching, Histogram Equalization, Gaussian, Median)
echo ===============================================================================
echo Dang khoi dong giao dien ung dung...
echo.

cd /d "%~dp0asl-sign-language"

if exist "%~dp0.venv\Scripts\python.exe" (
    "%~dp0.venv\Scripts\python.exe" gui_app.py
) else (
    python gui_app.py
)

if errorlevel 1 (
    echo.
    echo [!] Co loi xay ra khi chay ung dung.
    pause
)

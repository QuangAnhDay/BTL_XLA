@echo off
chcp 65001 >nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
title ASL Vision Pro - Enterprise Research Suite
echo ===============================================================================
echo   DANG KHOI DONG ASL VISION PRO (ENTERPRISE EDITION - TONE SANG)
echo   - Thanh dieu huong Taskbar chuyen nghiep ben trai
echo   - Nhan dien & Tien xu ly: So sanh Tuong phan va Histogram voi Anh Goc
echo   - Dashboard Thuc nghiem: Truc quan hoa do thi toan bo tap test data (25 mau)
echo   - Co so ly thuyet: Cong thuc YCrCb, Dan tuong phan, Histogram Eq & Softmax CNN
echo ===============================================================================
cd /d "%~dp0asl-sign-language"
"%~dp0.venv\Scripts\python.exe" gui_app.py
pause

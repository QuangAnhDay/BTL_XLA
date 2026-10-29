@echo off
chcp 65001 >nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
title ASL Vision Pro - Enterprise Research Suite (Ban Full 5 Phuong An)

echo ===============================================================================
echo   ASL VISION PRO - HE THONG DANH GIA TIEN XU LY ANH ASL
echo   Phien ban Doanh nghiep (Enterprise Full Edition - 5 Phuong An Nghien Cuu)
echo -------------------------------------------------------------------------------
echo   [1] Man hinh Nhan dien va So sanh Tien xu ly:
echo       - Doi sanh truc quan 5 anh: Goc, Dan Tuong Phan, Can Bang Bieu Do,
echo         Loc Gaussian (5x5, sigma=1.0) va Loc Trung Vi (Median 5x5)
echo       - Hero Card: Du doan toi uu kem do tin cay Softmax (%%)
echo       - Bang xep hang phan phoi xac suat Top 1 den Top 8 (day du 5 cot)
echo       - Phan tich hien tuong Lech phan phoi (Covariate Shift)
echo.
echo   [2] Man hinh Dashboard Thuc nghiem:
echo       - 6 The KPI tong quat (25 mau test N=25 tu A den Y)
echo       - 3 Do thi truc quan hoa da chieu (5 cot phuong an A, B, C, D, E)
echo       - Khoi phan tich hoc thuat ban chat co che sai lech
echo.
echo   [3] Man hinh Co so ly thuyet va Cong thuc:
echo       - Cong thuc toan hoc va nguyen ly cua ca 4 thuat toan tien xu ly
echo         (Contrast Stretching, Histogram Equalization, Gaussian, Median)
echo ===============================================================================
echo Dang khoi dong giao dien ung dung...
echo.

cd /d "%~dp0asl-sign-language"

set "PY_EXE="

:: 1. Kiem tra python trong .venv hien co co chay duoc khong
if exist "%~dp0.venv\Scripts\python.exe" (
    "%~dp0.venv\Scripts\python.exe" --version >nul 2>&1
    if not errorlevel 1 (
        set "PY_EXE=%~dp0.venv\Scripts\python.exe"
    )
)

:: 2. Neu .venv khong chay duoc, tim python tren may
if "%PY_EXE%"=="" (
    if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
        set "PY_EXE=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    ) else if exist "C:\Program Files\Python312\python.exe" (
        set "PY_EXE=C:\Program Files\Python312\python.exe"
    ) else (
        python --version >nul 2>&1
        if not errorlevel 1 (
            set "PY_EXE=python"
        ) else (
            py -3.12 --version >nul 2>&1
            if not errorlevel 1 (
                set "PY_EXE=py -3.12"
            )
        )
    )
)

if "%PY_EXE%"=="" (
    echo [!] KHONG TIM THAY PYTHON 3.12 HOP LE TREN HE THONG!
    echo [!] Vui long cai dat Python 3.12 de tiep tuc.
    pause
    exit /b 1
)

if exist "%PY_EXE%" (
    "%PY_EXE%" gui_app.py
) else (
    %PY_EXE% gui_app.py
)

if errorlevel 1 (
    echo.
    echo [!] Co loi xay ra khi chay ung dung.
    pause
)

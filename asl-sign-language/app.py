"""
ASL Vision Pro - Main Application Entry Point
Khoi chay Giao dien Nghien cuu & Danh gia Tien xu ly anh ASL (Enterprise Edition)
Phuc vu Do an Mon Xu ly anh & Tri tue nhan tao.
"""

import os
import sys
import tkinter as tk

# Dam bao import duoc cac module trong thu muc hien tai
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from gui_app import ASLEnterpriseApp, main

if __name__ == "__main__":
    main()

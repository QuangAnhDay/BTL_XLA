import os
import matplotlib.pyplot as plt
import numpy as np

os.makedirs("assets", exist_ok=True)

plt.rcParams['font.sans-serif'] = 'Segoe UI'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.edgecolor'] = '#D8E4F2'
plt.rcParams['axes.linewidth'] = 1.0

# ------------------------------------------------------------------------------
# 1. Slide 1: Hero Banner (Professional 3-Panel Scientific Comparison)
# ------------------------------------------------------------------------------
fig, axs = plt.subplots(1, 3, figsize=(10.8, 2.7), dpi=300)
fig.patch.set_facecolor('white')

panel_data = [
    ("1. Ảnh gốc (Baseline)", "#132E57", "#EAF2FF", "#165DDE", "Tự nhiên [0, 255]", "Độ chính xác: 100%"),
    ("2. Contrast Stretching", "#165DDE", "#F3F7FC", "#132E57", "Kéo giãn P1–P99 kênh Y", "Độ chính xác: 88%"),
    ("3. Histogram Equalization", "#B76A12", "#EAF2FF", "#23A8CE", "Cân bằng tích lũy CDF", "Độ chính xác: 68%")
]

for i, (ax, (title, title_clr, fill_clr, edge_clr, desc1, desc2)) in enumerate(zip(axs, panel_data)):
    ax.set_facecolor('white')
    
    # Draw hand sign 'A' vector silhouette (fist with vertical thumb along side)
    # Palm base + 4 curled fingers + thumb
    theta = np.linspace(0, 2*np.pi, 300)
    # create realistic fist contour
    if i == 0:
        # smooth natural contrast
        r = 1.0 + 0.15*np.cos(theta) + 0.2*np.sin(2*theta) - 0.1*np.cos(3*theta)
        alpha_val = 0.8
        line_w = 2.2
    elif i == 1:
        # high contrast sharp edges
        r = 1.0 + 0.22*np.cos(theta) + 0.28*np.sin(2*theta) - 0.15*np.cos(3*theta)
        alpha_val = 0.95
        line_w = 3.0
    else:
        # equalized flattened tonal shape
        r = 1.0 + 0.12*np.cos(theta) + 0.15*np.sin(2*theta) - 0.08*np.cos(3*theta)
        alpha_val = 0.9
        line_w = 2.2

    x_c = r * np.cos(theta)
    y_c = r * np.sin(theta)
    
    ax.fill(x_c, y_c, color=fill_clr, alpha=alpha_val)
    ax.plot(x_c, y_c, color=edge_clr, lw=line_w)
    
    # Internal detail lines (finger crease indication)
    if i == 0:
        ax.plot([-0.3, 0.4], [0.1, 0.1], color=edge_clr, lw=1.2, alpha=0.6)
        ax.plot([-0.2, 0.3], [-0.2, -0.2], color=edge_clr, lw=1.2, alpha=0.6)
    elif i == 1:
        # sharp harsh crease
        ax.plot([-0.4, 0.5], [0.1, 0.1], color=edge_clr, lw=2.0)
        ax.plot([-0.3, 0.4], [-0.2, -0.2], color=edge_clr, lw=2.0)
    else:
        # faint / washed out crease
        ax.plot([-0.2, 0.2], [0.1, 0.1], color=edge_clr, lw=0.8, alpha=0.4)
        ax.plot([-0.1, 0.1], [-0.2, -0.2], color=edge_clr, lw=0.8, alpha=0.4)
        
    ax.text(0, -1.6, desc1, ha='center', va='center', color='#526985', fontsize=9.5, fontweight='normal')
    ax.text(0, -2.0, desc2, ha='center', va='center', color=title_clr, fontsize=10.5, fontweight='bold')
    
    ax.set_title(title, fontsize=11.5, fontweight='bold', color=title_clr, pad=12)
    ax.set_xlim(-1.8, 1.8)
    ax.set_ylim(-2.3, 1.6)
    ax.set_aspect('equal')
    ax.axis('off')

    # Border around each card
    rect = plt.Rectangle((-1.75, -2.25), 3.5, 3.8, fill=False, edgecolor='#D8E4F2', lw=1.2, transform=ax.transData)
    ax.add_patch(rect)

plt.tight_layout()
plt.savefig("assets/hero_banner.png", dpi=300, facecolor='white', bbox_inches='tight')
plt.close()
print("Saved assets/hero_banner.png")

# ------------------------------------------------------------------------------
# 2. Slide 5: Conceptual Histogram (Before vs After)
# ------------------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 2.6), dpi=300)
fig.patch.set_facecolor('white')

x = np.arange(256)
raw_hist = np.exp(-((x - 120)**2) / (2 * 25**2)) + 0.3 * np.exp(-((x - 160)**2) / (2 * 15**2))
raw_hist = raw_hist / raw_hist.max()

ax1.set_facecolor('white')
ax1.fill_between(x, raw_hist, color='#EAF2FF', alpha=0.9)
ax1.plot(x, raw_hist, color='#165DDE', lw=2)
ax1.set_title("Histogram Kênh Y (Ảnh gốc - Cụm hẹp)", fontsize=11, fontweight='bold', color='#132E57', pad=10)
ax1.set_xlim(0, 255)
ax1.set_ylim(0, 1.1)
ax1.set_xlabel("Mức xám (0 - 255)", fontsize=9, color='#526985')
ax1.set_ylabel("Tần suất chuẩn hóa", fontsize=9, color='#526985')
ax1.tick_params(colors='#526985', labelsize=8)
for spine in ax1.spines.values():
    spine.set_color('#D8E4F2')

eq_hist = np.ones_like(x) * 0.45 + 0.08 * np.sin(x / 8.0) + 0.05 * np.cos(x / 3.0)
eq_hist = np.clip(eq_hist, 0.25, 0.65)

ax2.set_facecolor('white')
ax2.fill_between(x, eq_hist, color='#EAF2FF', alpha=0.9)
ax2.plot(x, eq_hist, color='#23A8CE', lw=2)
ax2.set_title("Sau Histogram Equalization (Tái phân bố đều)", fontsize=11, fontweight='bold', color='#132E57', pad=10)
ax2.set_xlim(0, 255)
ax2.set_ylim(0, 1.1)
ax2.set_xlabel("Mức xám (0 - 255)", fontsize=9, color='#526985')
ax2.set_ylabel("Tần suất chuẩn hóa", fontsize=9, color='#526985')
ax2.tick_params(colors='#526985', labelsize=8)
for spine in ax2.spines.values():
    spine.set_color('#D8E4F2')

plt.tight_layout()
plt.savefig("assets/hist_concept.png", dpi=300, facecolor='white', bbox_inches='tight')
plt.close()
print("Saved assets/hist_concept.png")

# ------------------------------------------------------------------------------
# 3. Slide 6: Accuracy Comparison Bar Chart
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(4.8, 3.2), dpi=300)
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

methods = ['Ảnh gốc\n(Baseline)', 'Contrast\nStretching', 'Histogram\nEqualization']
accuracies = [100.0, 88.0, 68.0]
colors = ['#165DDE', '#526985', '#B76A12']

bars = ax.bar(methods, accuracies, color=colors, width=0.52, edgecolor='none', zorder=3)
ax.grid(axis='y', linestyle='--', color='#D8E4F2', alpha=0.8, zorder=0)

for bar, acc in zip(bars, accuracies):
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 2.5, f"{int(acc)}%", 
            ha='center', va='bottom', fontsize=13, fontweight='bold', color='#132E57')

ax.set_ylim(0, 118)
ax.set_ylabel("Độ chính xác Top-1 (%)", fontsize=10, fontweight='bold', color='#132E57')
ax.tick_params(colors='#526985', labelsize=9.5)
for spine in ['top', 'right', 'left']:
    ax.spines[spine].set_visible(False)
ax.spines['bottom'].set_color('#D8E4F2')

plt.tight_layout()
plt.savefig("assets/accuracy_chart.png", dpi=300, facecolor='white', bbox_inches='tight')
plt.close()
print("Saved assets/accuracy_chart.png")

# ------------------------------------------------------------------------------
# 4. Slide 9: Softmax Distribution Comparison Chart (Fixed Collision)
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.5, 3.1), dpi=300)
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

scenarios = ['Histogram Equalization', 'Contrast Stretching', 'Ảnh gốc (Baseline)']
p_A = [91.7, 1.6, 99.9]
p_E = [8.3, 98.4, 0.05]

y = np.arange(len(scenarios))
height = 0.42

bars_A = ax.barh(y, p_A, height, label='Xác suất Nhãn A (Nhãn đúng)', color='#165DDE', zorder=3)
bars_E = ax.barh(y, p_E, height, left=p_A, label='Xác suất Nhãn E (Nhầm lẫn)', color='#B76A12', zorder=3)

ax.grid(axis='x', linestyle='--', color='#D8E4F2', alpha=0.8, zorder=0)

# Labels inside/beside bars - positioned carefully with zero collision
# Baseline (y=2)
ax.text(50, 2, "A: 99.9% (Dự đoán đúng)", ha='center', va='center', color='white', fontweight='bold', fontsize=10)

# Contrast Stretching (y=1): p_A is only 1.6%, p_E is 98.4%
# Place E label inside the big amber bar
ax.text(52, 1, "E: 98.4% (Dự đoán sai)", ha='center', va='center', color='white', fontweight='bold', fontsize=10)
# Place A label with a clean text tag at the far right or above bar
ax.text(102, 1, "A: 1.6%", ha='left', va='center', color='#165DDE', fontweight='bold', fontsize=9.5)

# Histogram Equalization (y=0): p_A is 91.7%, p_E is 8.3%
ax.text(45, 0, "A: 91.7% (Đúng)", ha='center', va='center', color='white', fontweight='bold', fontsize=10)
ax.text(96, 0, "8.3%", ha='center', va='center', color='white', fontweight='bold', fontsize=8.5)

ax.set_yticks(y)
ax.set_yticklabels(scenarios, fontsize=10, fontweight='bold', color='#132E57')
ax.set_xlim(0, 115)
ax.set_xlabel("Phân phối xác suất Softmax (%)", fontsize=10, fontweight='bold', color='#132E57')
ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.05), ncol=2, frameon=False, fontsize=9.5)

for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
ax.spines['bottom'].set_color('#D8E4F2')
ax.spines['left'].set_color('#D8E4F2')
ax.tick_params(colors='#526985', labelsize=9.5)

plt.tight_layout()
plt.savefig("assets/softmax_chart.png", dpi=300, facecolor='white', bbox_inches='tight')
plt.close()
print("Saved assets/softmax_chart.png (Fixed collision)")

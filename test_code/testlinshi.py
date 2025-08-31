import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# 设置MacOS系统自带的中文字体
plt.rcParams['font.sans-serif'] = ['PingFang TC', 'Heiti TC', 'STHeiti', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# 创建画布
fig, axes = plt.subplots(1, 2, figsize=(12, 6))

# 定义颜色
old_data_color = "#a6cee3"
new_data_color = "#1f78b4"
meta_color = "#b2df8a"

# ---------- 左边：COW ----------
ax = axes[0]
ax.set_title("COW (Copy-On-Write)", fontsize=12, fontweight="bold")

# 原始数据块
ax.add_patch(plt.Rectangle((0.2, 0.6), 0.2, 0.1, facecolor=old_data_color, edgecolor="black"))
ax.text(0.3, 0.65, "旧数据", ha="center", va="center", fontsize=10)

# 新数据块
ax.add_patch(plt.Rectangle((0.6, 0.6), 0.2, 0.1, facecolor=new_data_color, edgecolor="black"))
ax.text(0.7, 0.65, "新副本", ha="center", va="center", fontsize=10, color="white")

# 元数据指针
ax.add_patch(plt.Rectangle((0.4, 0.3), 0.2, 0.1, facecolor=meta_color, edgecolor="black"))
ax.text(0.5, 0.35, "元数据", ha="center", va="center", fontsize=10)

# 指针箭头
ax.annotate("", xy=(0.3, 0.6), xytext=(0.5, 0.4), arrowprops=dict(arrowstyle="->"))
ax.annotate("", xy=(0.7, 0.6), xytext=(0.5, 0.4), arrowprops=dict(arrowstyle="->", linestyle="dashed"))

ax.axis("off")

# ---------- 右边：ROW ----------
ax = axes[1]
ax.set_title("ROW (Redirect-On-Write)", fontsize=12, fontweight="bold")

# 原始数据块
ax.add_patch(plt.Rectangle((0.2, 0.6), 0.2, 0.1, facecolor=old_data_color, edgecolor="black"))
ax.text(0.3, 0.65, "旧数据", ha="center", va="center", fontsize=10)

# 新数据块（直接写到新位置）
ax.add_patch(plt.Rectangle((0.6, 0.4), 0.2, 0.1, facecolor=new_data_color, edgecolor="black"))
ax.text(0.7, 0.45, "新数据", ha="center", va="center", fontsize=10, color="white")

# 元数据指针
ax.add_patch(plt.Rectangle((0.4, 0.2), 0.2, 0.1, facecolor=meta_color, edgecolor="black"))
ax.text(0.5, 0.25, "元数据", ha="center", va="center", fontsize=10)

# 指针箭头
ax.annotate("", xy=(0.3, 0.6), xytext=(0.5, 0.3), arrowprops=dict(arrowstyle="->", linestyle="dashed"))
ax.annotate("", xy=(0.7, 0.4), xytext=(0.5, 0.3), arrowprops=dict(arrowstyle="->"))

ax.axis("off")

plt.tight_layout()
plt.savefig('cow_vs_row.png', dpi=300, bbox_inches='tight')
print("图像已保存为 cow_vs_row.png")
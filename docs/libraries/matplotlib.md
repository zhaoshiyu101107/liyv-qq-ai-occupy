# matplotlib 库文档

## 概述
matplotlib 是一个用于创建静态、动态和交互式可视化的 Python 库。

## 主要用途
- 创建各种类型的图表（线图、柱状图、散点图等）
- 数据可视化
- 科学计算结果展示

## 如何使用

### 基本用法
```python
import matplotlib.pyplot as plt

# 创建简单线图
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]
plt.plot(x, y)
plt.title('简单线图')
plt.xlabel('X 轴')
plt.ylabel('Y 轴')
plt.show()

# 创建柱状图
categories = ['A', 'B', 'C', 'D']
values = [10, 20, 15, 25]
plt.bar(categories, values)
plt.title('柱状图')
plt.show()
```

### 高级用法
```python
# 子图
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

ax1.plot(x, y)
ax1.set_title('子图1')

ax2.bar(categories, values)
ax2.set_title('子图2')

plt.tight_layout()
plt.show()

# 保存图表
plt.savefig('chart.png', dpi=300, bbox_inches='tight')
```

## 目录结构
matplotlib 的典型安装目录结构：
```
matplotlib/
├── __init__.py          # 主模块
├── _api.py              # API
├── _version.py          # 版本
├── animation.py         # 动画
├── artist.py            # 艺术家
├── axes/                # 坐标轴
│   ├── __init__.py
│   ├── _axes.py
│   ├── _base.py
│   └── ...
├── backend_bases.py     # 后端基础
├── backends/            # 后端
│   ├── __init__.py
│   ├── _backend_agg.py
│   ├── _backend_pdf.py
│   ├── _backend_svg.py
│   └── ...
├── cbook.py             # 实用工具
├── cm.py                # 颜色映射
├── collections.py       # 集合
├── colorbar.py          # 颜色条
├── colors.py            # 颜色
├── contour.py           # 等高线
├── dates.py             # 日期
├── figure.py            # 图形
├── font_manager.py      # 字体管理
├── image.py             # 图像
├── legend.py            # 图例
├── lines.py             # 线条
├── markers.py           # 标记
├── patches.py           # 补丁
├── path.py              # 路径
├── pyplot.py            # pyplot 接口
├── rcsetup.py           # RC 设置
├── scale.py             # 尺度
├── spines.py            # 脊柱
├── style/               # 样式
│   ├── __init__.py
│   └── ...
├── text.py              # 文本
├── ticker.py            # 刻度
├── transforms.py        # 变换
├── tri/                 # 三角剖分
│   ├── __init__.py
│   └── ...
└── widgets.py           # 小部件
```

## 注意事项
- 使用 plt.show() 显示图表，在非交互环境中可能需要保存到文件
- 支持多种输出格式：PNG, PDF, SVG 等
- 许可证：PSF (Python Software Foundation)</content>
<parameter name="filePath">/home/zhaoshiyu/data/liyu-pc-ai/occupy/docs/libraries/matplotlib.md
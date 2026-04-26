# occupy 项目 README

## 项目概述
这是一个系统资源监控项目，用于实时监控CPU、内存、磁盘、网络等系统资源的使用情况。项目使用Python开发，主要用于Linux环境下的系统监控。

## 依赖库介绍

### 核心依赖

#### psutil>=5.9.0
**用途**: psutil是一个跨平台的Python库，用于获取系统和进程的信息，如CPU使用率、内存使用、磁盘I/O、网络统计等。
**如何使用**:
```python
import psutil

# 获取CPU使用率
cpu_percent = psutil.cpu_percent(interval=1)
print(f"CPU使用率: {cpu_percent}%")

# 获取内存信息
memory = psutil.virtual_memory()
print(f"内存使用率: {memory.percent}%")

# 获取磁盘使用情况
disk = psutil.disk_usage('/')
print(f"磁盘使用率: {disk.percent}%")
```

详细文档：[psutil.md](docs/libraries/psutil.md)

### 可选依赖

#### matplotlib>=3.5.0
**用途**: Matplotlib是一个Python的绘图库，用于创建静态、动态、交互式的可视化图表。
**如何使用**:
```python
import matplotlib.pyplot as plt

# 创建简单图表
x = [1, 2, 3, 4]
y = [10, 20, 25, 30]
plt.plot(x, y)
plt.title("简单图表")
plt.show()
```

详细文档：[matplotlib.md](docs/libraries/matplotlib.md)

#### pandas>=1.4.0
**用途**: Pandas是一个强大的数据分析和操作库，提供数据结构和操作工具。
**如何使用**:
```python
import pandas as pd

# 创建DataFrame
data = {'Name': ['Alice', 'Bob'], 'Age': [25, 30]}
df = pd.DataFrame(data)
print(df)
```

详细文档：[pandas.md](docs/libraries/pandas.md)

#### numpy>=1.21.0
**用途**: NumPy是一个用于科学计算的基础包，提供多维数组对象和各种派生对象。
**如何使用**:
```python
import numpy as np

# 创建数组
arr = np.array([1, 2, 3, 4])
print(arr.mean())  # 计算平均值
```

详细文档：[numpy.md](docs/libraries/numpy.md)

# 创建DataFrame
data = {'Name': ['Alice', 'Bob'], 'Age': [25, 30]}
df = pd.DataFrame(data)
print(df)
```

#### numpy>=1.21.0
**用途**: NumPy是一个用于科学计算的基础包，提供多维数组对象和各种派生对象。
**如何使用**:
```python
import numpy as np

# 创建数组
arr = np.array([1, 2, 3, 4])
print(arr.mean())  # 计算平均值
```

## 安装和使用
1. 安装依赖：`pip install -r requirements.txt`
2. 运行主程序：`python main.py`

## 注意事项
- 确保Python版本>=3.6
- psutil库在某些系统上可能需要额外的权限来访问某些信息</content>
<parameter name="filePath">/home/zhaoshiyu/data/liyu-pc-ai/occupy/README.md
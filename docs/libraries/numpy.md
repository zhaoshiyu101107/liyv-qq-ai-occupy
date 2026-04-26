# numpy 库文档

## 概述
NumPy (Numerical Python) 是一个用于科学计算的基础包，提供多维数组对象和各种派生对象。

## 主要用途
- 多维数组操作
- 数学函数库
- 线性代数、傅里叶变换等
- 随机数生成

## 如何使用

### 基本用法
```python
import numpy as np

# 创建数组
arr = np.array([1, 2, 3, 4, 5])
print(arr)

# 创建多维数组
matrix = np.array([[1, 2], [3, 4]])
print(matrix)

# 数组操作
print(arr + 10)  # 加法
print(arr * 2)   # 乘法
print(arr.sum()) # 求和
print(arr.mean()) # 平均值
```

### 高级用法
```python
# 数组形状操作
arr = np.arange(12)
reshaped = arr.reshape(3, 4)
print(reshaped)

# 线性代数
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
print(np.dot(A, B))  # 矩阵乘法

# 随机数
random_arr = np.random.rand(3, 3)
print(random_arr)

# 统计函数
data = np.random.normal(0, 1, 1000)
print(f"均值: {np.mean(data)}")
print(f"标准差: {np.std(data)}")
print(f"中位数: {np.median(data)}")
```

## 目录结构
NumPy 的典型安装目录结构：
```
numpy/
├── __init__.py          # 主模块
├── __config__.py        # 配置
├── _core/               # 核心
│   ├── __init__.py
│   ├── _internal.py
│   ├── arrayprint.py
│   ├── defchararray.py
│   ├── dtype.py
│   ├── einsumfunc.py
│   ├── fromnumeric.py
│   ├── function_base.py
│   ├── getlimits.py
│   ├── memmap.py
│   ├── multiarray.py
│   ├── numeric.py
│   ├── records.py
│   ├── shape_base.py
│   ├── umath.py
│   └── ...
├── _distributor_init.py # 分发器初始化
├── _globals.py          # 全局变量
├── _pytesttester.py     # 测试器
├── _version.py          # 版本
├── array_api/           # 数组 API
│   ├── __init__.py
│   └── ...
├── compat/              # 兼容性
│   ├── __init__.py
│   └── ...
├── core/                # 核心 (别名)
├── ctypeslib.py         # ctypes 库
├── doc/                 # 文档
│   ├── __init__.py
│   └── ...
├── f2py/                # Fortran to Python
│   ├── __init__.py
│   └── ...
├── fft/                 # 快速傅里叶变换
│   ├── __init__.py
│   └── ...
├── lib/                 # 库函数
│   ├── __init__.py
│   ├── arraysetops.py
│   ├── function_base.py
│   ├── histograms.py
│   ├── index_tricks.py
│   ├── nanfunctions.py
│   ├── npyio.py
│   ├── polynomial.py
│   ├── recfunctions.py
│   ├── scimath.py
│   ├── stride_tricks.py
│   ├── twodim_base.py
│   ├── type_check.py
│   ├── ufunclike.py
│   ├── utils.py
│   └── ...
├── linalg/              # 线性代数
│   ├── __init__.py
│   └── ...
├── ma/                  # 掩码数组
│   ├── __init__.py
│   └── ...
├── matrixlib/           # 矩阵库
│   ├── __init__.py
│   └── ...
├── polynomial/          # 多项式
│   ├── __init__.py
│   └── ...
├── random/              # 随机数
│   ├── __init__.py
│   └── ...
├── testing/             # 测试
│   ├── __init__.py
│   └── ...
└── version.py           # 版本
```

## 注意事项
- NumPy 数组比 Python 列表更高效
- 支持广播 (broadcasting) 操作
- 许可证：BSD</content>
<parameter name="filePath">/home/zhaoshiyu/data/liyu-pc-ai/occupy/docs/libraries/numpy.md
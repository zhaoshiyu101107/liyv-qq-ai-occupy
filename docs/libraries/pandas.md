# pandas 库文档

## 概述
pandas 是一个强大的 Python 数据分析和操作库，提供数据结构和操作工具。

## 主要用途
- 数据清洗和预处理
- 数据分析和统计
- 数据可视化
- 时间序列分析

## 如何使用

### 基本用法
```python
import pandas as pd

# 创建 DataFrame
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'London', 'Tokyo']
}
df = pd.DataFrame(data)
print(df)

# 读取 CSV 文件
df = pd.read_csv('data.csv')
print(df.head())

# 基本统计
print(df.describe())
```

### 高级用法
```python
# 数据选择和过滤
print(df[df['Age'] > 25])

# 分组和聚合
grouped = df.groupby('City')['Age'].mean()
print(grouped)

# 处理缺失值
df.dropna()  # 删除缺失值
df.fillna(0)  # 填充缺失值

# 数据透视表
pivot = df.pivot_table(values='Age', index='City', aggfunc='mean')
print(pivot)

# 时间序列
dates = pd.date_range('2023-01-01', periods=100, freq='D')
ts = pd.Series(range(100), index=dates)
print(ts.resample('M').mean())
```

## 目录结构
pandas 的典型安装目录结构：
```
pandas/
├── __init__.py          # 主模块
├── _config.py           # 配置
├── _libs/               # C 扩展
│   ├── __init__.py
│   ├── lib.pyx
│   └── ...
├── _testing.py          # 测试工具
├── _version.py          # 版本
├── api/                 # API
│   ├── __init__.py
│   └── ...
├── arrays/              # 数组
│   ├── __init__.py
│   ├── array.py
│   └── ...
├── compat/              # 兼容性
│   ├── __init__.py
│   └── ...
├── core/                # 核心
│   ├── __init__.py
│   ├── algorithms.py
│   ├── api.py
│   ├── array.py
│   ├── arrays.py
│   ├── construction.py
│   ├── dtypes/          # 数据类型
│   ├── frame.py         # DataFrame
│   ├── generic.py
│   ├── groupby/         # 分组
│   ├── indexing.py      # 索引
│   ├── internals/       # 内部
│   ├── nanops.py
│   ├── reshape/         # 重塑
│   ├── series.py        # Series
│   ├── sorting.py       # 排序
│   ├── strings.py       # 字符串
│   └── ...
├── errors/              # 错误
│   ├── __init__.py
│   └── ...
├── io/                  # 输入输出
│   ├── __init__.py
│   ├── clipboard.py
│   ├── common.py
│   ├── excel.py
│   ├── feather.py
│   ├── formats/         # 格式
│   ├── gbq.py
│   ├── html.py
│   ├── json.py
│   ├── parquet.py
│   ├── pickle.py
│   ├── sas.py
│   ├── spss.py
│   ├── sql.py
│   ├── stata.py
│   ├── xml.py
│   └── ...
├── plotting/            # 绘图
│   ├── __init__.py
│   ├── _core.py
│   └── ...
├── tests/               # 测试
│   ├── __init__.py
│   └── ...
├── tseries/             # 时间序列
│   ├── __init__.py
│   ├── api.py
│   ├── frequencies.py
│   ├── holiday.py
│   ├── offset.py
│   └── ...
└── util/                # 工具
    ├── __init__.py
    └── ...
```

## 注意事项
- DataFrame 和 Series 是核心数据结构
- 支持多种文件格式的读写
- 许可证：BSD-3-Clause</content>
<parameter name="filePath">/home/zhaoshiyu/data/liyu-pc-ai/occupy/docs/libraries/pandas.md
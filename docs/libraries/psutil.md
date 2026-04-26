# psutil 库文档

## 概述
psutil (Python system and process utilities) 是一个跨平台的库，用于获取系统和进程的信息。

## 主要用途
- 获取 CPU 使用率、内存使用、磁盘 I/O 等系统信息
- 监控进程状态、资源使用
- 管理系统进程

## 如何使用

### 基本用法
```python
import psutil

# CPU 信息
print(f"CPU 核心数: {psutil.cpu_count()}")
print(f"CPU 使用率: {psutil.cpu_percent(interval=1)}%")

# 内存信息
memory = psutil.virtual_memory()
print(f"总内存: {memory.total / (1024**3):.2f} GB")
print(f"可用内存: {memory.available / (1024**3):.2f} GB")
print(f"内存使用率: {memory.percent}%")

# 磁盘信息
disk = psutil.disk_usage('/')
print(f"磁盘总容量: {disk.total / (1024**3):.2f} GB")
print(f"磁盘使用率: {disk.percent}%")

# 进程信息
for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
    print(proc.info)
```

### 高级用法
```python
# 获取特定进程信息
pid = 1234
p = psutil.Process(pid)
print(f"进程名称: {p.name()}")
print(f"进程 CPU 使用率: {p.cpu_percent()}")
print(f"进程内存使用: {p.memory_info().rss / (1024**2):.2f} MB")

# 网络信息
net = psutil.net_io_counters()
print(f"发送字节: {net.bytes_sent}")
print(f"接收字节: {net.bytes_recv}")
```

## 目录结构
psutil 的典型安装目录结构：
```
psutil/
├── __init__.py          # 主模块
├── _common.py           # 公共函数
├── _compat.py           # 兼容性
├── _psaix.py            # AIX 平台支持
├── _psbsd.py            # BSD 平台支持
├── _pslinux.py          # Linux 平台支持
├── _psosx.py            # macOS 平台支持
├── _psposix.py          # POSIX 平台支持
├── _pssunos.py          # SunOS 平台支持
├── _pswindows.py        # Windows 平台支持
├── _psutil_common.c     # 公共 C 代码
├── _psutil_linux.c      # Linux C 代码
├── _psutil_posix.c      # POSIX C 代码
├── _psutil_windows.c    # Windows C 代码
├── arch/                # 架构相关
│   ├── __init__.py
│   └── ...
├── tests/               # 测试
│   ├── __init__.py
│   └── ...
└── setup.py             # 安装脚本
```

## 注意事项
- 在某些系统上可能需要 root 权限来访问某些信息
- 支持多种操作系统：Linux, Windows, macOS, FreeBSD 等
- 许可证：BSD</content>
<parameter name="filePath">/home/zhaoshiyu/data/liyu-pc-ai/occupy/docs/libraries/psutil.md
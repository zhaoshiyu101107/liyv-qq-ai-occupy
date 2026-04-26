"""
base_utils.py - 基础工具函数
"""
import psutil
import time
from datetime import datetime

def bytes_to_gb(bytes_value):
    """将字节转换为GB"""
    return bytes_value / (1024**3)

def bytes_to_mb(bytes_value):
    """将字节转换为MB"""
    return bytes_value / (1024**2)

def format_time(seconds):
    """格式化时间"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def print_section(title):
    """打印章节标题"""
    print("\n" + "=" * 50)
    print(f"{title}")
    print("=" * 50)

def get_timestamp():
    """获取当前时间戳"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
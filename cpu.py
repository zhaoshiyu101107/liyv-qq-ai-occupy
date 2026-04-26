"""
cpu_monitor.py - CPU监控模块
"""
import psutil
from base_utils import print_section

def get_cpu_info():
    """获取CPU信息"""
    print_section("CPU 监控信息")
    
    # CPU总体使用率
    cpu_percent = psutil.cpu_percent(interval=1)
    print(f"CPU总体使用率: {cpu_percent}%")
    
    # 核心数
    cpu_count_logical = psutil.cpu_count()  # 逻辑核心数
    cpu_count_physical = psutil.cpu_count(logical=False)  # 物理核心数
    print(f"逻辑核心数: {cpu_count_logical}")
    print(f"物理核心数: {cpu_count_physical}")
    
    # 每个核心的使用率
    cpu_percent_per_core = psutil.cpu_percent(interval=1, percpu=True)
    print("\n各核心使用率:")
    for i, percent in enumerate(cpu_percent_per_core):
        print(f"  核心 {i}: {percent}%")
    
    # CPU频率
    try:
        cpu_freq = psutil.cpu_freq()
        if cpu_freq:
            print(f"\nCPU频率:")
            print(f"  当前: {cpu_freq.current:.2f} MHz")
            print(f"  最小: {cpu_freq.min:.2f} MHz")
            print(f"  最大: {cpu_freq.max:.2f} MHz")
    except:
        print("CPU频率信息不可用")
    
    # CPU统计信息
    cpu_stats = psutil.cpu_stats()
    print(f"\nCPU统计信息:")
    print(f"  上下文切换: {cpu_stats.ctx_switches:,}")
    print(f"  中断次数: {cpu_stats.interrupts:,}")
    print(f"  软中断次数: {cpu_stats.soft_interrupts:,}")
    
    # CPU时间信息
    cpu_times = psutil.cpu_times()
    print(f"\nCPU时间统计:")
    print(f"  用户时间: {cpu_times.user:.2f}秒")
    print(f"  系统时间: {cpu_times.system:.2f}秒")
    print(f"  空闲时间: {cpu_times.idle:.2f}秒")
    
    return {
        "cpu_percent": cpu_percent,
        "cpu_percent_per_core": cpu_percent_per_core,
        "cpu_count_logical": cpu_count_logical,
        "cpu_count_physical": cpu_count_physical
    }

def get_cpu_usage_history(interval=1, count=5):
    """获取CPU使用率历史记录"""
    print_section("CPU 使用率历史记录")
    
    history = []
    for i in range(count):
        usage = psutil.cpu_percent(interval=interval)
        history.append(usage)
        print(f"采样 {i+1}: {usage}%")
    
    avg_usage = sum(history) / len(history)
    max_usage = max(history)
    min_usage = min(history)
    
    print(f"\n统计:")
    print(f"  平均使用率: {avg_usage:.2f}%")
    print(f"  最高使用率: {max_usage:.2f}%")
    print(f"  最低使用率: {min_usage:.2f}%")
    
    return history
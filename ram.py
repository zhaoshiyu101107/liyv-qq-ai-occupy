"""
memory_monitor.py - 内存监控模块
"""
import psutil
from base_utils import bytes_to_gb, print_section

def get_memory_info():
    """获取内存信息"""
    print_section("内存监控信息")
    
    # 物理内存
    memory = psutil.virtual_memory()
    total_gb = bytes_to_gb(memory.total)
    used_gb = bytes_to_gb(memory.used)
    available_gb = bytes_to_gb(memory.available)
    free_gb = bytes_to_gb(memory.free)
    
    print("物理内存:")
    print(f"  总计: {total_gb:.2f} GB")
    print(f"  已使用: {used_gb:.2f} GB ({memory.percent}%)")
    print(f"  可用: {available_gb:.2f} GB")
    print(f"  空闲: {free_gb:.2f} GB")
    
    # 内存使用率图表
    print("\n内存使用率图表:")
    bar_length = 40
    used_length = int(memory.percent * bar_length / 100)
    free_length = bar_length - used_length
    print(f"  [{'█' * used_length}{'░' * free_length}] {memory.percent}%")
    
    # 内存详细统计
    print(f"\n详细统计:")
    print(f"  活动内存: {bytes_to_gb(getattr(memory, 'active', 0)):.2f} GB")
    print(f"  非活动内存: {bytes_to_gb(getattr(memory, 'inactive', 0)):.2f} GB")
    print(f"  缓冲区: {bytes_to_gb(getattr(memory, 'buffers', 0)):.2f} GB")
    print(f"  缓存: {bytes_to_gb(getattr(memory, 'cached', 0)):.2f} GB")
    
    # 交换内存
    swap = psutil.swap_memory()
    if swap.total > 0:
        swap_total_gb = bytes_to_gb(swap.total)
        swap_used_gb = bytes_to_gb(swap.used)
        
        print("\n交换内存 (虚拟内存):")
        print(f"  总计: {swap_total_gb:.2f} GB")
        print(f"  已使用: {swap_used_gb:.2f} GB ({swap.percent}%)")
        print(f"  空闲: {bytes_to_gb(swap.free):.2f} GB")
        
        # 交换内存图表
        print("\n交换内存使用率图表:")
        used_length_swap = int(swap.percent * bar_length / 100)
        free_length_swap = bar_length - used_length_swap
        print(f"  [{'█' * used_length_swap}{'░' * free_length_swap}] {swap.percent}%")
    else:
        print("\n交换内存: 未启用或不可用")
    
    return {
        "memory_percent": memory.percent,
        "memory_total_gb": total_gb,
        "memory_used_gb": used_gb,
        "memory_available_gb": available_gb,
        "swap_percent": swap.percent if swap.total > 0 else 0,
        "swap_total_gb": bytes_to_gb(swap.total) if swap.total > 0 else 0
    }
"""
disk_monitor.py - 磁盘监控模块
"""
import psutil
from base_utils import bytes_to_gb, bytes_to_mb, print_section

def get_disk_info():
    """获取磁盘信息"""
    print_section("磁盘监控信息")
    
    # 磁盘分区信息
    partitions = psutil.disk_partitions()
    
    disk_info = {}
    print(f"发现 {len(partitions)} 个磁盘分区:\n")
    
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            
            total_gb = bytes_to_gb(usage.total)
            used_gb = bytes_to_gb(usage.used)
            free_gb = bytes_to_gb(usage.free)
            
            print(f"设备: {partition.device}")
            print(f"挂载点: {partition.mountpoint}")
            print(f"文件系统: {partition.fstype}")
            print(f"总计: {total_gb:.2f} GB")
            print(f"已使用: {used_gb:.2f} GB ({usage.percent}%)")
            print(f"可用: {free_gb:.2f} GB")
            
            # 使用率图表
            bar_length = 40
            used_length = int(usage.percent * bar_length / 100)
            free_length = bar_length - used_length
            print(f"  [{'█' * used_length}{'░' * free_length}] {usage.percent}%\n")
            
            disk_info[partition.mountpoint] = {
                "total_gb": total_gb,
                "used_gb": used_gb,
                "free_gb": free_gb,
                "percent": usage.percent
            }
            
        except (PermissionError, FileNotFoundError) as e:
            print(f"无法访问分区 {partition.mountpoint}: {e}\n")
            continue
    
    # 磁盘IO统计
    try:
        disk_io = psutil.disk_io_counters()
        if disk_io:
            print("磁盘 I/O 统计:")
            print(f"  读取次数: {disk_io.read_count:,}")
            print(f"  写入次数: {disk_io.write_count:,}")
            print(f"  读取字节: {bytes_to_mb(disk_io.read_bytes):.2f} MB")
            print(f"  写入字节: {bytes_to_mb(disk_io.write_bytes):.2f} MB")
            print(f"  读取时间: {disk_io.read_time} ms")
            print(f"  写入时间: {disk_io.write_time} ms")
    except:
        print("磁盘 I/O 统计不可用")
    
    return disk_info

def get_disk_io_counters():
    """获取磁盘IO计数器"""
    try:
        io_counters = psutil.disk_io_counters(perdisk=True)
        if io_counters:
            print_section("各磁盘 I/O 统计")
            
            for disk_name, counters in io_counters.items():
                print(f"\n磁盘: {disk_name}")
                print(f"  读取次数: {counters.read_count:,}")
                print(f"  写入次数: {counters.write_count:,}")
                print(f"  读取字节: {bytes_to_mb(counters.read_bytes):.2f} MB")
                print(f"  写入字节: {bytes_to_mb(counters.write_bytes):.2f} MB")
                
            return io_counters
    except:
        print("各磁盘 I/O 统计不可用")
        return None
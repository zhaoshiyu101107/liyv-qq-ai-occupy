"""
process_monitor.py - 进程监控模块
"""
import psutil
from base_utils import bytes_to_mb, print_section

def get_process_info(max_processes=10):
    """获取进程信息"""
    print_section("进程监控信息")
    
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 
                                     'memory_percent', 'memory_info', 'status',
                                     'create_time', 'num_threads']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    print(f"运行中的进程总数: {len(processes)}")
    
    # 按CPU使用率排序
    print(f"\nCPU使用率最高的 {max_processes} 个进程:")
    processes_sorted_cpu = sorted(processes, 
                                  key=lambda p: p.get('cpu_percent', 0) or 0, 
                                  reverse=True)
    
    for i, proc in enumerate(processes_sorted_cpu[:max_processes]):
        pid = proc.get('pid', 'N/A')
        name = proc.get('name', 'N/A')[:30]  # 限制名称长度
        cpu = proc.get('cpu_percent', 0) or 0
        user = proc.get('username', 'N/A')
        
        print(f"{i+1:2d}. PID: {pid:>6} | CPU: {cpu:>5.1f}% | "
              f"用户: {user[:15]:<15} | 进程: {name}")
    
    # 按内存使用率排序
    print(f"\n内存使用率最高的 {max_processes} 个进程:")
    processes_sorted_mem = sorted(processes, 
                                  key=lambda p: p.get('memory_percent', 0) or 0, 
                                  reverse=True)
    
    for i, proc in enumerate(processes_sorted_mem[:max_processes]):
        pid = proc.get('pid', 'N/A')
        name = proc.get('name', 'N/A')[:30]
        mem_percent = proc.get('memory_percent', 0) or 0
        mem_info = proc.get('memory_info')
        mem_rss = bytes_to_mb(mem_info.rss) if mem_info else 0
        
        print(f"{i+1:2d}. PID: {pid:>6} | 内存: {mem_percent:>5.1f}% "
              f"({mem_rss:>6.1f} MB) | 进程: {name}")
    
    # 进程统计
    print("\n进程状态统计:")
    status_count = {}
    for proc in processes:
        status = proc.get('status', 'unknown')
        status_count[status] = status_count.get(status, 0) + 1
    
    for status, count in status_count.items():
        print(f"  {status}: {count}")
    
    return {
        "total_processes": len(processes),
        "top_cpu_processes": processes_sorted_cpu[:5],
        "top_memory_processes": processes_sorted_mem[:5]
    }

def get_process_details(pid):
    """获取特定进程的详细信息"""
    try:
        proc = psutil.Process(pid)
        info = proc.as_dict(attrs=['pid', 'name', 'exe', 'cmdline', 'username',
                                   'cpu_percent', 'memory_percent', 'memory_info',
                                   'status', 'create_time', 'num_threads',
                                   'connections', 'open_files'])
        
        print_section(f"进程详细信息 (PID: {pid})")
        
        print(f"名称: {info.get('name', 'N/A')}")
        print(f"路径: {info.get('exe', 'N/A')}")
        print(f"命令行: {' '.join(info.get('cmdline', []))}")
        print(f"用户: {info.get('username', 'N/A')}")
        print(f"CPU使用率: {info.get('cpu_percent', 0)}%")
        print(f"内存使用率: {info.get('memory_percent', 0)}%")
        
        mem_info = info.get('memory_info')
        if mem_info:
            print(f"内存 RSS: {bytes_to_mb(mem_info.rss):.2f} MB")
            print(f"内存 VMS: {bytes_to_mb(mem_info.vms):.2f} MB")
        
        print(f"状态: {info.get('status', 'N/A')}")
        print(f"创建时间: {info.get('create_time', 0)}")
        print(f"线程数: {info.get('num_threads', 0)}")
        
        return info
    except psutil.NoSuchProcess:
        print(f"进程 {pid} 不存在")
        return None
    except psutil.AccessDenied:
        print(f"无权限访问进程 {pid}")
        return None
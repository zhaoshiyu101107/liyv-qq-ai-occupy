"""
main.py - 主程序入口（自动获取全部信息并保存到JSON文件）
"""
import time
import json
import psutil
import platform
import socket
from datetime import datetime
from base_utils import bytes_to_gb, bytes_to_mb

def collect_all_info():
    """收集所有系统信息"""
    current_time = datetime.now()
    
    all_info = {
        "timestamp": current_time.timestamp(),
        "datetime": current_time.strftime('%Y-%m-%d %H:%M:%S'),
        "date": current_time.strftime('%Y-%m-%d'),
        "time": current_time.strftime('%H:%M:%S')
    }
    
    # 1. CPU信息
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_percent_per_core = psutil.cpu_percent(interval=1, percpu=True)
    cpu_count_logical = psutil.cpu_count()
    cpu_count_physical = psutil.cpu_count(logical=False)
    
    try:
        cpu_freq = psutil.cpu_freq()
        cpu_freq_info = {
            "current": cpu_freq.current if cpu_freq else None,
            "min": cpu_freq.min if cpu_freq else None,
            "max": cpu_freq.max if cpu_freq else None
        }
    except:
        cpu_freq_info = None
    
    cpu_stats = psutil.cpu_stats()
    cpu_times = psutil.cpu_times()
    
    all_info["cpu"] = {
        "percent": cpu_percent,
        "percent_per_core": cpu_percent_per_core,
        "count_logical": cpu_count_logical,
        "count_physical": cpu_count_physical,
        "frequency": cpu_freq_info,
        "stats": {
            "ctx_switches": cpu_stats.ctx_switches,
            "interrupts": cpu_stats.interrupts,
            "soft_interrupts": cpu_stats.soft_interrupts
        },
        "times": {
            "user": cpu_times.user,
            "system": cpu_times.system,
            "idle": cpu_times.idle
        }
    }
    
    # 2. 内存信息
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    all_info["memory"] = {
        "physical": {
            "total_gb": bytes_to_gb(memory.total),
            "used_gb": bytes_to_gb(memory.used),
            "available_gb": bytes_to_gb(memory.available),
            "free_gb": bytes_to_gb(memory.free),
            "percent": memory.percent
        },
        "swap": {
            "total_gb": bytes_to_gb(swap.total),
            "used_gb": bytes_to_gb(swap.used),
            "free_gb": bytes_to_gb(swap.free),
            "percent": swap.percent
        } if swap.total > 0 else None
    }
    
    # 3. 磁盘信息
    disk_info = {}
    partitions = psutil.disk_partitions()
    
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_info[partition.mountpoint] = {
                "device": partition.device,
                "filesystem": partition.fstype,
                "total_gb": bytes_to_gb(usage.total),
                "used_gb": bytes_to_gb(usage.used),
                "free_gb": bytes_to_gb(usage.free),
                "percent": usage.percent
            }
        except:
            continue
    
    all_info["disk"] = disk_info
    
    # 4. 磁盘IO信息
    try:
        disk_io = psutil.disk_io_counters()
        all_info["disk_io"] = {
            "read_count": disk_io.read_count,
            "write_count": disk_io.write_count,
            "read_bytes_mb": bytes_to_mb(disk_io.read_bytes),
            "write_bytes_mb": bytes_to_mb(disk_io.write_bytes),
            "read_time": disk_io.read_time,
            "write_time": disk_io.write_time
        } if disk_io else None
    except:
        all_info["disk_io"] = None
    
    # 5. 网络信息
    try:
        net_io = psutil.net_io_counters()
        all_info["network"] = {
            "bytes_sent_mb": bytes_to_mb(net_io.bytes_sent),
            "bytes_recv_mb": bytes_to_mb(net_io.bytes_recv),
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv,
            "errin": net_io.errin,
            "errout": net_io.errout,
            "dropin": net_io.dropin,
            "dropout": net_io.dropout
        }
    except:
        all_info["network"] = None
    
    # 6. 进程信息
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 
                                     'memory_percent', 'memory_info', 'status']):
        try:
            processes.append(proc.info)
        except:
            continue
    
    # 按CPU和内存排序
    processes_sorted_cpu = sorted(processes, 
                                  key=lambda p: p.get('cpu_percent', 0) or 0, 
                                  reverse=True)
    processes_sorted_mem = sorted(processes, 
                                  key=lambda p: p.get('memory_percent', 0) or 0, 
                                  reverse=True)
    
    all_info["process"] = {
        "total": len(processes),
        "top_cpu": [
            {
                "pid": p.get('pid'),
                "name": p.get('name'),
                "cpu_percent": p.get('cpu_percent', 0),
                "user": p.get('username')
            }
            for p in processes_sorted_cpu[:10]
        ],
        "top_memory": [
            {
                "pid": p.get('pid'),
                "name": p.get('name'),
                "memory_percent": p.get('memory_percent', 0),
                "memory_mb": bytes_to_mb(p.get('memory_info').rss) if p.get('memory_info') else 0
            }
            for p in processes_sorted_mem[:10]
        ]
    }
    
    # 7. 系统信息
    try:
        hostname = socket.gethostname()
        try:
            ip_address = socket.gethostbyname(hostname)
        except:
            ip_address = None
        
        boot_time = psutil.boot_time()
        boot_time_str = datetime.fromtimestamp(boot_time).strftime('%Y-%m-%d %H:%M:%S')
        uptime = datetime.now().timestamp() - boot_time
        
        users = psutil.users()
        users_list = [
            {
                "name": user.name,
                "terminal": user.terminal,
                "host": user.host,
                "started": datetime.fromtimestamp(user.started).strftime('%Y-%m-%d %H:%M:%S')
            }
            for user in users
        ] if users else []
        
        all_info["system"] = {
            "os_name": platform.system(),
            "os_release": platform.release(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "hostname": hostname,
            "ip_address": ip_address,
            "boot_time": boot_time_str,
            "uptime_seconds": uptime,
            "users": users_list,
            "users_count": len(users_list)
        }
    except Exception as e:
        all_info["system"] = {"error": str(e)}
    
    # 8. 温度传感器信息（如果可用）
    try:
        temperatures = psutil.sensors_temperatures()
        if temperatures:
            temp_info = {}
            for name, entries in temperatures.items():
                temp_info[name] = [
                    {
                        "label": entry.label or f"sensor_{i}",
                        "current": entry.current,
                        "high": entry.high,
                        "critical": entry.critical
                    }
                    for i, entry in enumerate(entries)
                ]
            all_info["temperature"] = temp_info
    except AttributeError:
        pass
    
    # 9. 电池信息（如果可用）
    try:
        battery = psutil.sensors_battery()
        if battery:
            all_info["battery"] = {
                "percent": battery.percent,
                "power_plugged": battery.power_plugged,
                "secsleft": battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else None
            }
    except AttributeError:
        pass
    
    return all_info

def save_to_json(data, filename="occupy.json"):
    """保存数据到JSON文件"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        return True
    except Exception as e:
        return False

def main():
    """主函数"""
    try:
        # 收集所有信息
        all_data = collect_all_info()
        
        # 保存到文件
        if save_to_json(all_data, "occupy.json"):
            # 保存成功，无打印输出
            pass
        else:
            # 保存失败，无打印输出
            pass
    except Exception as e:
        # 发生错误，无打印输出
        pass

if __name__ == "__main__":
    main()
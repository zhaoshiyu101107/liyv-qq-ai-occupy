"""
main.py - 主程序入口（自动获取全部信息并保存到JSON文件）
"""
import json
import psutil
import platform
import socket
from datetime import datetime
from base_utils_zh import bytes_to_gb, bytes_to_mb

def collect_all_info():
    """收集所有系统信息"""
    current_time = datetime.now()
    
    all_info = {
        "时间戳": current_time.timestamp(),
        "日期时间": current_time.strftime('%Y年%m月%d日 %H:%M:%S'),
        "日期": current_time.strftime('%Y年%m月%d日'),
        "时间": current_time.strftime('%H:%M:%S')
    }
    
    # 1. CPU信息
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_percent_per_core = psutil.cpu_percent(interval=1, percpu=True)
    cpu_count_logical = psutil.cpu_count()
    cpu_count_physical = psutil.cpu_count(logical=False)
    
    # 将各核心使用率转换为中文显示
    cpu_cores_dict = {}
    for i, percent in enumerate(cpu_percent_per_core):
        core_name = f"核心{i+1}"
        cpu_cores_dict[core_name] = percent
    
    try:
        cpu_freq = psutil.cpu_freq()
        cpu_freq_info = {
            "当前频率_MHz": cpu_freq.current if cpu_freq else None,
            "最小频率_MHz": cpu_freq.min if cpu_freq else None,
            "最大频率_MHz": cpu_freq.max if cpu_freq else None
        }
    except:
        cpu_freq_info = None
    
    cpu_stats = psutil.cpu_stats()
    cpu_times = psutil.cpu_times()
    
    all_info["CPU信息"] = {
        "总体使用率_百分比": cpu_percent,
        "各核心使用率": cpu_cores_dict,  # 改为字典形式，使用中文核心名称
        "逻辑核心数": cpu_count_logical,
        "物理核心数": cpu_count_physical,
        "频率信息": cpu_freq_info,
        "统计信息": {
            "上下文切换次数": cpu_stats.ctx_switches,
            "中断次数": cpu_stats.interrupts,
            "软中断次数": cpu_stats.soft_interrupts
        },
        "时间统计": {
            "用户时间_秒": cpu_times.user,
            "系统时间_秒": cpu_times.system,
            "空闲时间_秒": cpu_times.idle
        },
        "核心使用率分析": {
            "核心数量": len(cpu_percent_per_core),
            "平均使用率": round(sum(cpu_percent_per_core) / len(cpu_percent_per_core), 2) if cpu_percent_per_core else 0,
            "最高使用率核心": f"核心{cpu_percent_per_core.index(max(cpu_percent_per_core)) + 1}" if cpu_percent_per_core else "无",
            "最高使用率": max(cpu_percent_per_core) if cpu_percent_per_core else 0,
            "最低使用率核心": f"核心{cpu_percent_per_core.index(min(cpu_percent_per_core)) + 1}" if cpu_percent_per_core else "无",
            "最低使用率": min(cpu_percent_per_core) if cpu_percent_per_core else 0
        }
    }
    
    # 2. 内存信息
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    all_info["内存信息"] = {
        "物理内存": {
            "总容量_GB": round(bytes_to_gb(memory.total), 2),
            "已使用_GB": round(bytes_to_gb(memory.used), 2),
            "可用容量_GB": round(bytes_to_gb(memory.available), 2),
            "空闲容量_GB": round(bytes_to_gb(memory.free), 2),
            "使用率_百分比": memory.percent
        },
        "交换内存": {
            "总容量_GB": round(bytes_to_gb(swap.total), 2),
            "已使用_GB": round(bytes_to_gb(swap.used), 2),
            "空闲容量_GB": round(bytes_to_gb(swap.free), 2),
            "使用率_百分比": swap.percent
        } if swap.total > 0 else None
    }
    
    # 3. 磁盘信息
    disk_info = {}
    partitions = psutil.disk_partitions()
    
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_info[partition.mountpoint] = {
                "设备名称": partition.device,
                "文件系统": partition.fstype,
                "总容量_GB": round(bytes_to_gb(usage.total), 2),
                "已使用_GB": round(bytes_to_gb(usage.used), 2),
                "空闲容量_GB": round(bytes_to_gb(usage.free), 2),
                "使用率_百分比": usage.percent
            }
        except:
            continue
    
    all_info["磁盘信息"] = disk_info
    
    # 4. 磁盘IO信息
    try:
        disk_io = psutil.disk_io_counters()
        all_info["磁盘IO统计"] = {
            "读取次数": disk_io.read_count,
            "写入次数": disk_io.write_count,
            "读取数据_MB": round(bytes_to_mb(disk_io.read_bytes), 2),
            "写入数据_MB": round(bytes_to_mb(disk_io.write_bytes), 2),
            "读取时间_ms": disk_io.read_time,
            "写入时间_ms": disk_io.write_time
        } if disk_io else None
    except:
        all_info["磁盘IO统计"] = None
    
    # 5. 网络信息
    try:
        net_io = psutil.net_io_counters()
        all_info["网络统计"] = {
            "发送数据_MB": round(bytes_to_mb(net_io.bytes_sent), 2),
            "接收数据_MB": round(bytes_to_mb(net_io.bytes_recv), 2),
            "发送数据包数": net_io.packets_sent,
            "接收数据包数": net_io.packets_recv,
            "接收错误数": net_io.errin,
            "发送错误数": net_io.errout,
            "接收丢弃数": net_io.dropin,
            "发送丢弃数": net_io.dropout
        }
    except:
        all_info["网络统计"] = None
    
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
    
    all_info["进程信息"] = {
        "进程总数": len(processes),
        "CPU使用率最高的10个进程": [
            {
                "进程ID": p.get('pid'),
                "进程名称": p.get('name'),
                "CPU使用率_百分比": p.get('cpu_percent', 0),
                "用户": p.get('username')
            }
            for p in processes_sorted_cpu[:10]
        ],
        "内存使用率最高的10个进程": [
            {
                "进程ID": p.get('pid'),
                "进程名称": p.get('name'),
                "内存使用率_百分比": p.get('memory_percent', 0),
                "内存占用_MB": round(bytes_to_mb(p.get('memory_info').rss), 2) if p.get('memory_info') else 0
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
            ip_address = "无法获取"
        
        boot_time = psutil.boot_time()
        boot_time_str = datetime.fromtimestamp(boot_time).strftime('%Y年%m月%d日 %H:%M:%S')
        uptime = datetime.now().timestamp() - boot_time
        
        # 格式化运行时间
        uptime_hours = int(uptime // 3600)
        uptime_minutes = int((uptime % 3600) // 60)
        uptime_seconds = int(uptime % 60)
        uptime_str = f"{uptime_hours}小时{uptime_minutes}分钟{uptime_seconds}秒"
        
        users = psutil.users()
        users_list = [
            {
                "用户名": user.name,
                "终端": user.terminal,
                "主机": user.host,
                "登录时间": datetime.fromtimestamp(user.started).strftime('%Y年%m月%d日 %H:%M:%S')
            }
            for user in users
        ] if users else []
        
        all_info["系统信息"] = {
            "操作系统": platform.system(),
            "系统版本": platform.release(),
            "详细版本": platform.version(),
            "系统架构": platform.machine(),
            "处理器": platform.processor(),
            "Python版本": platform.python_version(),
            "Python实现": platform.python_implementation(),
            "主机名": hostname,
            "IP地址": ip_address,
            "系统启动时间": boot_time_str,
            "系统运行时间_秒": round(uptime, 2),
            "系统运行时间": uptime_str,
            "登录用户列表": users_list,
            "登录用户数": len(users_list)
        }
    except Exception as e:
        all_info["系统信息"] = {"错误": str(e)}
    
    # 8. 温度传感器信息（如果可用）
    try:
        temperatures = psutil.sensors_temperatures()
        if temperatures:
            temp_info = {}
            for name, entries in temperatures.items():
                temp_info[name] = [
                    {
                        "传感器名称": entry.label or f"传感器_{i+1}",
                        "当前温度_℃": entry.current,
                        "高温阈值_℃": entry.high,
                        "临界阈值_℃": entry.critical
                    }
                    for i, entry in enumerate(entries)
                ]
            all_info["温度信息"] = temp_info
    except AttributeError:
        pass
    
    # 9. 电池信息（如果可用）
    try:
        battery = psutil.sensors_battery()
        if battery:
            if battery.secsleft == psutil.POWER_TIME_UNLIMITED:
                secsleft_str = "电源已连接"
            elif battery.secsleft < 0:
                secsleft_str = "正在计算"
            else:
                hours = battery.secsleft // 3600
                minutes = (battery.secsleft % 3600) // 60
                secsleft_str = f"{int(hours)}小时{int(minutes)}分钟"
            
            all_info["电池信息"] = {
                "电量百分比": battery.percent,
                "电源连接状态": "已连接" if battery.power_plugged else "未连接",
                "剩余时间": secsleft_str,
                "剩余时间_秒": battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else None
            }
    except AttributeError:
        pass
    
    # 10. 在文件中添加摘要信息
    all_info["系统占用摘要"] = {
        "收集时间": all_info["日期时间"],
        "CPU使用率_百分比": cpu_percent,
        "内存使用率_百分比": memory.percent,
        "内存使用情况": f"{round(bytes_to_gb(memory.used), 2)}GB / {round(bytes_to_gb(memory.total), 2)}GB",
        "磁盘使用情况": {mount: f"{info['使用率_百分比']}% ({round(info['已使用_GB'], 2)}GB/{round(info['总容量_GB'], 2)}GB)" 
                       for mount, info in disk_info.items()},
        "核心使用率": {core: f"{percent}%" for core, percent in cpu_cores_dict.items()},
        "运行进程数": len(processes),
        "系统运行时间": uptime_str if '系统信息' in all_info and '系统运行时间' in all_info['系统信息'] else "未知"
    }
    
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
        filename = "occupy.json"
        if save_to_json(all_data, filename):
            print("系统占用信息收集完成")
        else:
            print("保存文件时发生错误")
    except Exception as e:
        print(f"收集系统信息时发生错误: {e}")

if __name__ == "__main__":
    main()
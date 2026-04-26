"""
system_info.py - 系统信息模块
"""
import psutil
import platform
import socket
from datetime import datetime
from base_utils import format_time, print_section

def get_system_info():
    """获取系统信息"""
    print_section("系统信息")
    
    # 操作系统信息
    print("操作系统:")
    print(f"  系统: {platform.system()} {platform.release()}")
    print(f"  版本: {platform.version()}")
    print(f"  架构: {platform.machine()}")
    print(f"  处理器: {platform.processor()}")
    
    # Python信息
    print(f"\nPython信息:")
    print(f"  版本: {platform.python_version()}")
    print(f"  实现: {platform.python_implementation()}")
    
    # 主机名和IP
    print(f"\n网络标识:")
    hostname = socket.gethostname()
    print(f"  主机名: {hostname}")
    
    try:
        ip_address = socket.gethostbyname(hostname)
        print(f"  IP地址: {ip_address}")
    except:
        print("  IP地址: 无法获取")
    
    # 系统启动时间
    boot_time = psutil.boot_time()
    boot_time_str = datetime.fromtimestamp(boot_time).strftime('%Y-%m-%d %H:%M:%S')
    print(f"\n系统启动时间: {boot_time_str}")
    
    uptime = datetime.now().timestamp() - boot_time
    print(f"系统运行时间: {format_time(uptime)}")
    
    # 用户信息
    users = psutil.users()
    if users:
        print(f"\n当前登录用户 ({len(users)}):")
        for user in users:
            print(f"  用户: {user.name}, 终端: {user.terminal}, "
                  f"登录时间: {datetime.fromtimestamp(user.started).strftime('%H:%M:%S')}")
    
    # 温度传感器（如果可用）
    try:
        temperatures = psutil.sensors_temperatures()
        if temperatures:
            print(f"\n温度传感器:")
            for name, entries in temperatures.items():
                for entry in entries:
                    print(f"  {name}: {entry.current}°C")
    except AttributeError:
        pass  # 某些平台不支持
    
    # 电池信息（如果可用）
    try:
        battery = psutil.sensors_battery()
        if battery:
            print(f"\n电池信息:")
            print(f"  电量: {battery.percent}%")
            print(f"  电源连接: {'是' if battery.power_plugged else '否'}")
            if battery.secsleft != psutil.POWER_TIME_UNLIMITED:
                print(f"  剩余时间: {format_time(battery.secsleft)}")
    except AttributeError:
        pass  # 某些平台不支持
    
    return {
        "os_name": platform.system(),
        "os_version": platform.version(),
        "hostname": hostname,
        "boot_time": boot_time_str,
        "uptime": uptime,
        "users_count": len(users)
    }
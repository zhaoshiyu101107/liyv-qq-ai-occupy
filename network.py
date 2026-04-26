"""
network_monitor.py - 网络监控模块
"""
import psutil
from base_utils import bytes_to_mb, print_section

def get_network_info():
    """获取网络信息"""
    print_section("网络监控信息")
    
    # 网络接口信息
    net_if_addrs = psutil.net_if_addrs()
    net_if_stats = psutil.net_if_stats()
    
    print("网络接口信息:")
    for interface_name, addresses in net_if_addrs.items():
        print(f"\n接口: {interface_name}")
        
        # 接口状态
        if interface_name in net_if_stats:
            stats = net_if_stats[interface_name]
            status = "已连接" if stats.isup else "未连接"
            print(f"  状态: {status}")
            print(f"  MTU: {stats.mtu}")
        
        # IP地址
        for addr in addresses:
            if addr.family.name == 'AF_INET':
                print(f"  IPv4地址: {addr.address}")
                if addr.netmask:
                    print(f"  子网掩码: {addr.netmask}")
            elif addr.family.name == 'AF_INET6':
                print(f"  IPv6地址: {addr.address}")
    
    # 网络IO统计
    net_io = psutil.net_io_counters()
    print("\n网络 I/O 统计:")
    print(f"  发送字节: {bytes_to_mb(net_io.bytes_sent):.2f} MB")
    print(f"  接收字节: {bytes_to_mb(net_io.bytes_recv):.2f} MB")
    print(f"  发送包数: {net_io.packets_sent:,}")
    print(f"  接收包数: {net_io.packets_recv:,}")
    print(f"  发送错误: {net_io.errout}")
    print(f"  接收错误: {net_io.errin}")
    print(f"  发送丢弃: {net_io.dropout}")
    print(f"  接收丢弃: {net_io.dropin}")
    
    # 网络连接
    try:
        connections = psutil.net_connections()
        print(f"\n网络连接数: {len(connections)}")
        
        # 按状态统计连接数
        conn_by_state = {}
        for conn in connections:
            state = conn.status
            conn_by_state[state] = conn_by_state.get(state, 0) + 1
        
        print("连接状态统计:")
        for state, count in conn_by_state.items():
            print(f"  {state}: {count}")
    except (psutil.AccessDenied, PermissionError):
        print("\n网络连接信息需要管理员权限")
    
    return {
        "bytes_sent_mb": bytes_to_mb(net_io.bytes_sent),
        "bytes_recv_mb": bytes_to_mb(net_io.bytes_recv),
        "interfaces_count": len(net_if_addrs)
    }

def get_network_io_by_interface():
    """获取各网络接口的IO统计"""
    try:
        net_io_per_nic = psutil.net_io_counters(pernic=True)
        if net_io_per_nic:
            print_section("各网络接口 I/O 统计")
            
            for interface_name, counters in net_io_per_nic.items():
                print(f"\n接口: {interface_name}")
                print(f"  发送字节: {bytes_to_mb(counters.bytes_sent):.2f} MB")
                print(f"  接收字节: {bytes_to_mb(counters.bytes_recv):.2f} MB")
                print(f"  发送包数: {counters.packets_sent:,}")
                print(f"  接收包数: {counters.packets_recv:,}")
            
            return net_io_per_nic
    except:
        print("各网络接口 I/O 统计不可用")
        return None
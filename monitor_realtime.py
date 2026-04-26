#!/usr/bin/env python3
"""实时系统占用监控脚本

运行方式：
    python3 monitor_realtime.py

显示内容：CPU、内存、交换区、磁盘、负载、前5个CPU/内存占用进程。
"""

import os
import time
from datetime import datetime

import psutil


def format_bytes(value: float) -> str:
    """将字节数量格式化为人类可读形式。"""
    units = ["B", "KB", "MB", "GB", "TB"]
    for unit in units:
        if value < 1024.0 or unit == units[-1]:
            return f"{value:.2f} {unit}"
        value /= 1024.0
    return f"{value:.2f} PB"


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def get_top_processes(count: int = 5):
    procs = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            cpu_percent = proc.cpu_percent(interval=None)
            mem_percent = proc.memory_percent()
            procs.append({
                'pid': proc.pid,
                'name': proc.info.get('name') or 'unknown',
                'username': proc.info.get('username') or 'unknown',
                'cpu_percent': cpu_percent,
                'mem_percent': mem_percent,
                'rss': proc.memory_info().rss,
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    top_cpu = sorted(procs, key=lambda p: p['cpu_percent'], reverse=True)[:count]
    top_mem = sorted(procs, key=lambda p: p['mem_percent'], reverse=True)[:count]
    return top_cpu, top_mem


def print_header():
    print("实时系统占用监控 - 按 Ctrl+C 退出")
    print("时间：", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("=" * 80)


def print_system_usage(interval: float = 1.0):
    cpu_percent = psutil.cpu_percent(interval=interval, percpu=False)
    cpu_per_core = psutil.cpu_percent(interval=None, percpu=True)
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    disk = psutil.disk_usage('/')
    load_avg = os.getloadavg() if hasattr(os, 'getloadavg') else (0.0, 0.0, 0.0)

    print(f"CPU 总使用率：{cpu_percent:.1f}%  负载：{load_avg[0]:.2f} {load_avg[1]:.2f} {load_avg[2]:.2f}")
    print("CPU 各核心：", " | ".join(f"核心{i+1}:{pct:.1f}%" for i, pct in enumerate(cpu_per_core)))
    print(f"内存：{format_bytes(mem.used)} / {format_bytes(mem.total)}  使用率：{mem.percent:.1f}%")
    print(f"交换区：{format_bytes(swap.used)} / {format_bytes(swap.total)}  使用率：{swap.percent:.1f}%")
    print(f"磁盘(/)：{format_bytes(disk.used)} / {format_bytes(disk.total)}  使用率：{disk.percent:.1f}%")
    print("=" * 80)


def print_top_processes(top_cpu, top_mem):
    print("CPU 占用最高进程")
    print(f"{'PID':>6} {'CPU%':>6} {'MEM%':>6} {'RSS':>10}  名称")
    for proc in top_cpu:
        print(f"{proc['pid']:>6} {proc['cpu_percent']:>6.1f} {proc['mem_percent']:>6.1f} {format_bytes(proc['rss']):>10}  {proc['name']}")
    print("-" * 80)
    print("内存占用最高进程")
    print(f"{'PID':>6} {'CPU%':>6} {'MEM%':>6} {'RSS':>10}  名称")
    for proc in top_mem:
        print(f"{proc['pid']:>6} {proc['cpu_percent']:>6.1f} {proc['mem_percent']:>6.1f} {format_bytes(proc['rss']):>10}  {proc['name']}")
    print("=" * 80)


def main():
    try:
        # 预热一次进程 CPU 计数
        for proc in psutil.process_iter(['pid']):
            try:
                proc.cpu_percent(interval=None)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        while True:
            clear_screen()
            print_header()
            print_system_usage(interval=1.0)
            top_cpu, top_mem = get_top_processes(count=5)
            print_top_processes(top_cpu, top_mem)
            time.sleep(1)
    except KeyboardInterrupt:
        print('\n已退出实时监控。')


if __name__ == '__main__':
    main()

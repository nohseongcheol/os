#!/usr/bin/env python3
"""기존 路径 호환 条目分. 实际数据 实现: ../工具集/网络桥接.py"""
import importlib as 取用值
import sys as 运行系统值
from pathlib import Path as 路径
运行系统值.path.insert(0, str(路径(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 运行器
    运行器.run_module('网络桥接', run_name='__main__', alter_sys=True)
else:
    实现 = 取用值.import_module('网络桥接')
    映射值 = {'response': '响应', 'parts': '路径组件', 's': '字符串数据', 'i': '序数索引', 'close': '关闭', 'forward': '转发中规则', 'slip_input': '串行线路_Internet_协议输入', 'self': '自身值', 'item': '条目值', 'flags': '配置项位列', 'ftp_port': '文件传送端口编号', 'args': '参数数组', 'server': '服务器值', 'data': '数据', 'ethernet_input': '以太网输入', 'trace_packet': '追踪数据包', 'GATEWAY': '网关硬件地址', 'rule': '规则值', 'protocol': '网络ABI', 'forwards': '转发中规则列', 'occupied': '已占用', 'host': '宿主', 'ack': '确认状态编号', 'serial_port': '串行端口编号', 'readers': '读取器集', 'guest': '客户机', 'destination': '目的地址数据地址', 'ethernet_port': '以太网端口', 'b': '第二值', 'MAC': '计算机地址', 'arp': '地址分辨率数据包', 'writable': '可写', 'direction': '方向', 'seq': '排序编号', 'frame': '执行状态帧', 'loop': '周期值', 'port': '端口编号', 'offset': '偏移值', 'readable': '能够读取', 'c': '字符代码', 'p': '数据位置', 'writers': '写入器集', 'IP': '互联网地址值', 'e': '辅助条目', 'n': '项目个数', 'packet': '数据包数据', 'arguments': '已转发参数', 'source': '原始数据', 'NetworkBridge': '网络桥接', 'window': '窗口', 'capture': '捕获'}
    for 上一个项目, 当前项目 in 映射值.items():
        if hasattr(实现, 当前项目): globals()[上一个项目] = getattr(实现, 当前项目)

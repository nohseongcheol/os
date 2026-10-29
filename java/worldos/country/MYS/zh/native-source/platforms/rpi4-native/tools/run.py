#!/usr/bin/env python3
"""기존 路径 호환 条目分. 实际数据 实现: ../工具集/执行命令.py"""
import importlib as 取用值
import sys as 运行系统值
from pathlib import Path as 路径
运行系统值.path.insert(0, str(路径(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 运行器
    运行器.run_module('执行命令', run_name='__main__', alter_sys=True)
else:
    实现 = 取用值.import_module('执行命令')
    映射值 = {'supported': '支持功能列', 'parser': '参数解析器', 'qemu': '测试替身计算机', 'run_desktop': '运行桌面', 'main': '运行', 'host': '宿主', 'status': '状态值', 'NetworkBridge': '网络桥接', 'ROOT': '项目根', 'bridge': '桥接', 'loader': '加载器', 'base': '背景值', 'options': '选择项集', 'binary': '二进制', 'args': '参数数组', 'command': '命令'}
    for 上一个项目, 当前项目 in 映射值.items():
        if hasattr(实现, 当前项目): globals()[上一个项目] = getattr(实现, 当前项目)

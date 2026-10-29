#!/usr/bin/env python3
"""기존 路径 호환 条目分. 实际数据 实现: ../工具集/SDK编译.py"""
import importlib as 取用值
import sys as 运行系统值
from pathlib import Path as 路径
运行系统值.path.insert(0, str(路径(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 运行器
    运行器.run_module('SDK编译', run_name='__main__', alter_sys=True)
else:
    实现 = 取用值.import_module('SDK编译')
    映射值 = {'compiler': '编译器工具', 'obj': '目的地址文件', 'sdk': '开发工具套件', 'output': '输出结果', 'main': '运行', 'elf': '可执行文件文件', 'is_c': '是否C语言', 'parser': '参数解析器', 'language': '语言', 'work': '工作中路径', 'args': '参数数组'}
    for 上一个项目, 当前项目 in 映射值.items():
        if hasattr(实现, 当前项目): globals()[上一个项目] = getattr(实现, 当前项目)

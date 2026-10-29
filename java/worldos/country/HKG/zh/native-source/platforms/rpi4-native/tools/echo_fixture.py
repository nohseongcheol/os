#!/usr/bin/env python3
"""기존 路径 호환 条目分. 实际数据 实现: ../工具集/回显测试夹具.py"""
import importlib as 取用值
import sys as 运行系统值
from pathlib import Path as 路径
运行系统值.path.insert(0, str(路径(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 运行器
    运行器.run_module('回显测试夹具', run_name='__main__', alter_sys=True)
else:
    实现 = 取用值.import_module('回显测试夹具')
    映射值 = {'data': '数据', 'e': '辅助条目', 'connection': '接通状态', 'f': '文件条目', 'peer': '对端值', 'self': '自身值', 'udp': '数据报控制', 't': '终端条目', 'tcp': '连接状态控制', 'EchoFixture': '回显测试夹具', 'args': '参数数组', 'chunk': '片段值'}
    for 上一个项目, 当前项目 in 映射值.items():
        if hasattr(实现, 当前项目): globals()[上一个项目] = getattr(实现, 当前项目)

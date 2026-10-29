#!/usr/bin/env python3
"""기존 路径 호환 条目分. 实际数据 实现: ../工具集/构建网络.py"""
import importlib as 取用值
import sys as 运行系统值
from pathlib import Path as 路径
运行系统值.path.insert(0, str(路径(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 运行器
    运行器.run_module('构建网络', run_name='__main__', alter_sys=True)
else:
    实现 = 取用值.import_module('构建网络')
    映射值 = {'obj': '目的地址文件', 'objects': '目的地址文件集', 'library': '库', 'output': '输出结果', 'port': '端口编号', 'root': '根地址', 'files': '文件列表', 'source': '原始数据', 'run': '执行命令', 'flags': '配置项位列', 'path': '路径', 'build_network': '创建网络', 'cc': 'C编译器', 'ar': '存档工具'}
    for 上一个项目, 当前项目 in 映射值.items():
        if hasattr(实现, 当前项目): globals()[上一个项目] = getattr(实现, 当前项目)

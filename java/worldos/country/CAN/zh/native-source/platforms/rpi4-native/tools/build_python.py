#!/usr/bin/env python3
"""기존 路径 호환 条目分. 实际数据 实现: ../工具集/构建Python.py"""
import importlib as 取用值
import sys as 运行系统值
from pathlib import Path as 路径
运行系统值.path.insert(0, str(路径(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 运行器
    运行器.run_module('构建Python', run_name='__main__', alter_sys=True)
else:
    实现 = 取用值.import_module('构建Python')
    映射值 = {'ld': '链接器工具', 'archive': '存档', 'SHA256': '有效性验证哈希', 'build_python': '创建Python', 'root': '根地址', 'source': '原始数据', 'name': '名称', 'path': '路径', 'VERSION': '版本版次值', 'cc': 'C编译器', 'tar': 'TAR捆绑', 'newlib': 'Newlib包含路径', 'member': '成员'}
    for 上一个项目, 当前项目 in 映射值.items():
        if hasattr(实现, 当前项目): globals()[上一个项目] = getattr(实现, 当前项目)

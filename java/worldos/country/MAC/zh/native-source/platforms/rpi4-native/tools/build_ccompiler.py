#!/usr/bin/env python3
"""기존 路径 호환 条目分. 实际数据 实现: ../工具集/构建C编译器.py"""
import importlib as 取用值
import sys as 运行系统值
from pathlib import Path as 路径
运行系统值.path.insert(0, str(路径(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 运行器
    运行器.run_module('构建C编译器', run_name='__main__', alter_sys=True)
else:
    实现 = 取用值.import_module('构建C编译器')
    映射值 = {'out': '结果数据', 'builtins': '内建项集', 'header': '头部值', 'sdk': '开发工具套件', 'build_ccompiler': '创建C编译器', 'i': '序数索引', 'elf': '可执行文件文件', 'run': '执行命令', 'flags': '配置项位列', 'path': '路径', 'p': '数据位置', 'cc': 'C编译器', 'obj': '目的地址文件', 'flag': '设置值', 'ld': '链接器工具', 'objects': '目的地址文件集', 'repo': '代码库路径', 'v': '临时数据', 'upstream': '上游', 'root': '根地址', 'assets': '资源素材', 'source': '原始数据', 'name': '名称', 'includes': '包含项'}
    for 上一个项目, 当前项目 in 映射值.items():
        if hasattr(实现, 当前项目): globals()[上一个项目] = getattr(实现, 当前项目)

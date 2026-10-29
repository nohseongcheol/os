#!/usr/bin/env python3
"""기존 路径 호환 条目分. 实际数据 实现: ../工具集/导出SDK.py"""
import importlib as 取用值
import sys as 运行系统值
from pathlib import Path as 路径
运行系统值.path.insert(0, str(路径(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 运行器
    运行器.run_module('导出SDK', run_name='__main__', alter_sys=True)
else:
    实现 = 取用值.import_module('导出SDK')
    映射值 = {'out': '结果数据', 'obj': '目的地址文件', 'relative': '相对路径', 'compiler_archive': '编译器存档', 'sdk': '开发工具套件', 'dist': '分发路径', 'archive': '存档', 'main': '运行', 'posix': 'POSIX', 'files': '文件列表', 'source': '原始数据', 'name': '名称', 'target': '目标值', 'ROOT': '项目根', 'destination': '目的地址数据地址', 'manifest': '捆绑构建清单', 'work': '工作中路径'}
    for 上一个项目, 当前项目 in 映射值.items():
        if hasattr(实现, 当前项目): globals()[上一个项目] = getattr(实现, 当前项目)

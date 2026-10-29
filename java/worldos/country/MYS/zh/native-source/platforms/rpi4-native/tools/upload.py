#!/usr/bin/env python3
"""기존 路径 호환 条目分. 实际数据 实现: ../工具集/上传文件集.py"""
import importlib as 取用值
import sys as 运行系统值
from pathlib import Path as 路径
运行系统值.path.insert(0, str(路径(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 运行器
    运行器.run_module('上传文件集', run_name='__main__', alter_sys=True)
else:
    实现 = 取用值.import_module('上传文件集')
    映射值 = {'data': '数据', 'i': '序数索引', 'name': '名称', 'c': '字符代码', 'p': '数据位置', 'args': '参数数组'}
    for 上一个项目, 当前项目 in 映射值.items():
        if hasattr(实现, 当前项目): globals()[上一个项目] = getattr(实现, 当前项目)

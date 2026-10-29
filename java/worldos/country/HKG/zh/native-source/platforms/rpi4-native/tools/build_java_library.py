#!/usr/bin/env python3
"""기존 路径 호환 条目分. 实际数据 实现: ../工具集/构建Java库.py"""
import importlib as 取用值
import sys as 运行系统值
from pathlib import Path as 路径
运行系统值.path.insert(0, str(路径(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 运行器
    运行器.run_module('构建Java库', run_name='__main__', alter_sys=True)
else:
    实现 = 取用值.import_module('构建Java库')
    映射值 = {'header': '头部值', 'sources': '源代码列表', 'i': '序数索引', 'info': '系统信息', 'payload': '载荷数据数据', 'src': '原始地址', 'run': '执行命令', 'build_java_library': '创建Java库', 'relative': '相对路径', 'classes': '类路径', 'dist': '分发路径', 'archive': '存档', 'output': '输出结果', 'root': '根地址', 'name': '名称', 'jar': 'Java捆绑', 'b': '第二值', 'entries': '条目列列表'}
    for 上一个项目, 当前项目 in 映射值.items():
        if hasattr(实现, 当前项目): globals()[上一个项目] = getattr(实现, 当前项目)

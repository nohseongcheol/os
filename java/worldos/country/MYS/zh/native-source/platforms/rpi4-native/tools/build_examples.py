#!/usr/bin/env python3
"""기존 路径 호환 条目分. 实际数据 实现: ../工具集/构建用例集.py"""
import importlib as 取用值
import sys as 运行系统值
from pathlib import Path as 路径
运行系统值.path.insert(0, str(路径(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 运行器
    运行器.run_module('构建用例集', run_name='__main__', alter_sys=True)
else:
    实现 = 取用值.import_module('构建用例集')
    映射值 = {'out': '结果数据', 'build_examples': '创建用例集', 'files': '文件列表', 'java': '执行Java', 'run': '执行命令', 'path': '路径', 'p': '数据位置', 'readme': '自述文件', 'build_java_library': '创建Java库', 'code': '指令序列', 'index': '查找索引', 'classes': '类路径', 'repo': '代码库路径', 'root': '根地址', 'content': '内容值', 'source': '原始数据', 'name': '名称', 'target': '目标值', 'manifest': '捆绑构建清单', 'language': '语言'}
    for 上一个项目, 当前项目 in 映射值.items():
        if hasattr(实现, 当前项目): globals()[上一个项目] = getattr(实现, 当前项目)

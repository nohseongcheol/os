#!/usr/bin/env python3
"""기존 路径 호환 条目分. 实际数据 实现: ../工具集/测试ELF.py"""
import importlib as 取用值
import sys as 运行系统值
from pathlib import Path as 路径
运行系统值.path.insert(0, str(路径(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 运行器
    运行器.run_module('测试ELF', run_name='__main__', alter_sys=True)
else:
    实现 = 取用值.import_module('测试ELF')
    映射值 = {'out': '结果数据', 'expected': '预期', 'phoff': '程序头部偏移', 'offset': '偏移值', 'invalid': '无效数据', 'path': '路径', 'executable': '可执行文件映像', 'rejected': '拒绝状态结果', 'linux_example': 'Linux示例', 'original': '原始', 'result': '结果', 'format_': '格式指定', 'main': '运行', 'content': '内容值', 'source': '原始数据', 'name': '名称', 'reference': '比较基线', 'ROOT': '项目根', 'value': '值', 'report': '有效性验证报告'}
    for 上一个项目, 当前项目 in 映射值.items():
        if hasattr(实现, 当前项目): globals()[上一个项目] = getattr(实现, 当前项目)

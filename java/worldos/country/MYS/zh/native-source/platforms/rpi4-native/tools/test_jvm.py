#!/usr/bin/env python3
"""기존 路径 호환 条目分. 实际数据 实现: ../工具集/测试JVM.py"""
import importlib as 取用值
import sys as 运行系统值
from pathlib import Path as 路径
运行系统值.path.insert(0, str(路径(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 运行器
    运行器.run_module('测试JVM', run_name='__main__', alter_sys=True)
else:
    实现 = 取用值.import_module('测试JVM')
    映射值 = {'message': '通知文本', 's': '字符串数据', 'actual': '实际结果', 'match': '是否相等', 'payload': '载荷数据数据', 'cases': '测试情况', 'fixture': '测试数据', 'main': '运行', 'ROOT': '项目根', 'text': '文本', 'valid': '有效', 'includes': '包含项', 'include': '包含条目', 'expected': '预期', 'sources': '源代码列表', 'tmp': '临时路径', 'done': '已完成总量', 'classes': '类路径', 'output': '输出结果', 'result': '结果', 'cmd': '命令参数列', 'name': '名称', 'jar': 'Java捆绑', 'report': '有效性验证报告', 'tests': '测试列表'}
    for 上一个项目, 当前项目 in 映射值.items():
        if hasattr(实现, 当前项目): globals()[上一个项目] = getattr(实现, 当前项目)

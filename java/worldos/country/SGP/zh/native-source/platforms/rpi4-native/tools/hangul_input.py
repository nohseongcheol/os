#!/usr/bin/env python3
"""기존 路径 호환 条目分. 实际数据 实现: ../工具集/韩文字母输入.py"""
import importlib as 取用值
import sys as 运行系统值
from pathlib import Path as 路径
运行系统值.path.insert(0, str(路径(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 运行器
    运行器.run_module('韩文字母输入', run_name='__main__', alter_sys=True)
else:
    实现 = 取用值.import_module('韩文字母输入')
    映射值 = {'old': '上一个项目', 'backspace': '退格', 'committed': '已提交', 'KEYS': '键导航', 'self': '自身值', 'FINALS': '复合最终字母构件', 'VOWELS': '复合中声字母构件', 'INITIAL': '初始字母构件表', 'initial': '初始字母构件', 'commit': '提交合成状态', 'feed': '供给键', 'vowel': '中声字母构件', 'Hangul': '合成韩文字母', 'SPLIT': '分割最终字母构件', 'final': '最终字母构件', 'key': '已按下值', 'send': '发送', 'left': '左侧', 'FINAL': '最终字母构件表', 'history': '历史记录', 'pair': '一一对', 'char': '字符数据', 'VOWEL': '中声字母构件表', 'right': '右', 'value': '值', 'text': '文本'}
    for 上一个项目, 当前项目 in 映射值.items():
        if hasattr(实现, 当前项目): globals()[上一个项目] = getattr(实现, 当前项目)

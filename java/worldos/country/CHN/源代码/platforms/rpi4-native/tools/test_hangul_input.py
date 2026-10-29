#!/usr/bin/env python3
"""기존 路径 호환 条目分. 实际数据 实现: ../工具集/测试韩文字母输入.py"""
import importlib as 取用值
import sys as 运行系统值
from pathlib import Path as 路径
运行系统值.path.insert(0, str(路径(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 运行器
    运行器.run_module('测试韩文字母输入', run_name='__main__', alter_sys=True)
else:
    实现 = 取用值.import_module('测试韩文字母输入')
    映射值 = {'expected': '预期', 'Keyboard': '键盘', 'press': '按下键', 'self': '自身值', 'test_modes_repeat_and_commit': '测试模式列重复与提交', 'keys': '已按下键列', 'test_paste_and_unicode': '测试粘贴与Unicode', 'data': '数据', 'key': '已按下值', 'send': '发送', 'test_words': '测试单词列', 'InputTests': '测试韩文字母输入', 'test_backspace': '测试退格', 'symbol': '符号值', 'char': '字符数据', 'type': '类型分类'}
    for 上一个项目, 当前项目 in 映射值.items():
        if hasattr(实现, 当前项目): globals()[上一个项目] = getattr(实现, 当前项目)

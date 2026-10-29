#!/usr/bin/env python3
"""기존 路径 호환 条目分. 实际数据 实现: ../工具集/测试窗口列.py"""
import importlib as 取用值
import sys as 运行系统值
from pathlib import Path as 路径
运行系统值.path.insert(0, str(路径(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 运行器
    运行器.run_module('测试窗口列', run_name='__main__', alter_sys=True)
else:
    实现 = 取用值.import_module('测试窗口列')
    映射值 = {'wait': '等待', 'x': '横坐标坐标', 's': '字符串数据', 'xy': '坐标一对', 'sel': '选择器', 'seconds': '秒数单位', 'log': '日志记录', 'at': '当前位置', 'send': '发送', 'main': '运行', 'req': '申请值', 'hot': '快捷操作值', 'pump': '句柄事件', 'ROOT': '项目根', 'marker': '标记', 'b': '第二值', 'command': '命令', 'shell': '命令壳', 'f': '文件条目', 'color': '像素颜色', 'click': '单击按钮', 'k': '第三索引', 'c': '字符代码', 'r': '已返回值', 'p': '数据位置', 'done': '已完成总量', 'end': '结束偏移', 'command_mode': '命令模式', 'key': '已按下值', 'y': 'Y_按钮坐标', 'pixels': '像素列列表', 'result': '结果', 'report': '有效性验证报告', 'dest': '目的地址值位置', 'work': '工作中路径', 'qmp': '测试替身控制连接状态'}
    for 上一个项目, 当前项目 in 映射值.items():
        if hasattr(实现, 当前项目): globals()[上一个项目] = getattr(实现, 当前项目)

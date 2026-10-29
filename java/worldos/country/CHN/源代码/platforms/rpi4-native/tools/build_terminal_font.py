#!/usr/bin/env python3
"""기존 路径 호환 条目分. 实际数据 实现: ../工具集/构建终端字体.py"""
import importlib as 取用值
import sys as 运行系统值
from pathlib import Path as 路径
运行系统值.path.insert(0, str(路径(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 运行器
    运行器.run_module('构建终端字体', run_name='__main__', alter_sys=True)
else:
    实现 = 取用值.import_module('构建终端字体')
    映射值 = {'data': '数据', 'img': '绘图', 'bits': '位列列表', 'x': '横坐标坐标', 'draw': '绘制屏幕', 'licences': '许可列', 'paths': '路径列表', 'y': 'Y_按钮坐标', 'main': '运行', 'src': '原始地址', 'fonts': '字体列表', 'ROOT': '项目根', 'p': '数据位置', 'cp': '字符编码状态', 'target': '目标值'}
    for 上一个项目, 当前项目 in 映射值.items():
        if hasattr(实现, 当前项目): globals()[上一个项目] = getattr(实现, 当前项目)

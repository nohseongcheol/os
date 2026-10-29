#!/usr/bin/env python3
"""기존 路径 호환 条目分. 实际数据 实现: ../工具集/测试桌面.py"""
import importlib as 取用值
import sys as 运行系统值
from pathlib import Path as 路径
运行系统值.path.insert(0, str(路径(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 运行器
    运行器.run_module('测试桌面', run_name='__main__', alter_sys=True)
else:
    实现 = 取用值.import_module('测试桌面')
    映射值 = {'x': '横坐标坐标', 'typing': '已输入字符', 'message': '通知文本', 'start': '运行', 'down': '是否按下中', 'exact': '精确值', 'i': '序数索引', 'press': '按下键', 'rectangles': '矩形列列表', 'sym': '符号', 'j': '内部侧序数', 'deadline': '截止时间时间', 'proc': '进程', 'data': '数据', 'main': '运行', 'w': '已请求宽度值', 'init': '初始值', 'block': '数据块', 'ROOT': '项目根', 'text': '文本', 'marker': '标记', 'report': '有效性验证报告', 'until': '直到', 'clipboard': '剪贴板值', 'dst': '目的地址地址', 'seen': '已看见条目列', 'poll': '就绪情况监视器', 'transcript': '执行记录', 'port': '端口编号', 'offset': '偏移值', 'h': '已请求高度值', 'src': '原始地址', 'event': '事件', 'encoding': '字符设定', 'size': '大小', 'key': '已按下值', 'pixels': '像素列列表', 'y': 'Y_按钮坐标', 'output': '输出结果', 'symbol': '符号值', 'client': '客户端', 'char': '字符数据', 'rgb': '红_绿_蓝颜色'}
    for 上一个项目, 当前项目 in 映射值.items():
        if hasattr(实现, 当前项目): globals()[上一个项目] = getattr(实现, 当前项目)

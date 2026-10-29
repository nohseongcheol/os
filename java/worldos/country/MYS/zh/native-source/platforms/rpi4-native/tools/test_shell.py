#!/usr/bin/env python3
"""기존 路径 호환 条目分. 实际数据 实现: ../工具集/测试命令壳.py"""
import importlib as 取用值
import sys as 运行系统值
from pathlib import Path as 路径
运行系统值.path.insert(0, str(路径(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 运行器
    运行器.run_module('测试命令壳', run_name='__main__', alter_sys=True)
else:
    实现 = 取用值.import_module('测试命令壳')
    映射值 = {'timeout': '执行状态超时', 'x': '横坐标坐标', 'msg': '网络消息', 'i': '序数索引', 'reply': '回复', 'call': '调用', 'args': '参数数组', 'chunk': '片段值', 'data': '数据', 'proc': '进程', 'long_text': '长整数文本', 'restored': '已恢复数据', 'send': '发送', 'file': '文件', 'main': '运行', 'found': '搜索结果', 'ROOT': '项目根', 'text': '文本', 'marker': '标记', 'command': '命令', 'expected': '预期', 'pixel': '像素', 'shell': '命令壳', 'poll': '就绪情况监视器', 'transcript': '执行记录', 'end': '结束偏移', 'image': '映像', 'key': '已按下值', 'y': 'Y_按钮坐标', 'output': '输出结果', 'result': '结果', 'client': '客户端', 'line': '行', 'stream': '流值', 'name': '名称', 'value': '值', 'receive': '接收消息', 'report': '有效性验证报告', 'work': '工作中路径', 'qmp': '测试替身控制连接状态'}
    for 上一个项目, 当前项目 in 映射值.items():
        if hasattr(实现, 当前项目): globals()[上一个项目] = getattr(实现, 当前项目)

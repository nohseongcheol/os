#!/usr/bin/env python3
"""기존 路径 호환 条目分. 实际数据 实现: ../工具集/测试用例集.py"""
import importlib as 取用值
import sys as 运行系统值
from pathlib import Path as 路径
运行系统值.path.insert(0, str(路径(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 运行器
    运行器.run_module('测试用例集', run_name='__main__', alter_sys=True)
else:
    实现 = 取用值.import_module('测试用例集')
    映射值 = {'count': '条目个数', 'exact': '精确值', 'expected_file': '预期文件', 'ftp_port': '文件传送端口编号', 'data': '数据', 'graphics_command': '图形命令', 'main': '运行', 'row': '行位置', 'init': '初始值', 'target': '目标值', 'ROOT': '项目根', 'text': '文本', 'binary': '二进制', 'out': '结果数据', 'entry': '条目分', 'got': '已接收个数', 'port': '端口编号', 'graphics_start': '开始绘图', 'col': '列位置', 'begin': '开始偏移', 'kind': '分类值', 'selector': '就绪选择器', 'n': '项目个数', 'key': '已按下值', 'y': 'Y_按钮坐标', 'client': '客户端', 'line': '行', 'report': '有效性验证报告', 'language': '语言', 'x': '横坐标坐标', 'start': '运行', 'rgb': '红_绿_蓝颜色', 'down': '是否按下中', 'listing': '发送列表', 'payload': '载荷数据数据', 'proc': '进程', 'w': '已请求宽度值', 'temporary': '临时', 'echo': '回显服务器条目', 'label': '名称表', 'content': '内容值', 'argument': '已转发值', 'EchoServers': '回显服务器列', 'marker': '标记', 'expected': '预期', 'test_language': '测试语言', 'filename': '文件条目名称', 'shell': '命令壳', 'color': '像素颜色', 'transcript': '执行记录', 'offset': '偏移值', 'h': '已请求高度值', 'run': '执行命令', 'c': '字符代码', 'path': '路径', 'encoding': '字符设定', 'end': '结束偏移', 'ftp': '文件传送连接状态', 'pixels': '像素列列表', 'symbol': '符号值', 'source': '原始数据', 'name': '名称', 'receive': '接收消息', 'manifest': '捆绑构建清单'}
    for 上一个项目, 当前项目 in 映射值.items():
        if hasattr(实现, 当前项目): globals()[上一个项目] = getattr(实现, 当前项目)

#!/usr/bin/env python3
"""기존 路径 호환 条目分. 实际数据 实现: ../工具集/启动测试.py"""
import importlib as 取用值
import sys as 运行系统值
from pathlib import Path as 路径
运行系统值.path.insert(0, str(路径(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 运行器
    运行器.run_module('启动测试', run_name='__main__', alter_sys=True)
else:
    实现 = 取用值.import_module('启动测试')
    映射值 = {'timeout': '执行状态超时', 'response': '响应', 'msg': '网络消息', 'exact': '精确值', 'markers': '标记列', 'i': '序数索引', 'match': '是否相等', 'execute': '执行任务', 'cancel': '取消操作', 'cmd_byte': '命令字节', 'reply': '回复', 'points': '点列', 'server': '服务器值', 'data': '数据', 'prompt': '提示', 'enter': '进入', 'imported': '已导入', 'send': '发送', 'main': '运行', 'ROOT': '项目根', 'text': '文本', 'first_gui': '首位GUI', 'pixel': '像素', 'java_class': 'Java类', 'upload': '上传文件集', 'pixels_file': '像素文件', 'pixels_data': '像素数据', 'edit': '编辑值', 'receive_until': '接收直到', 'selector': '就绪选择器', 'size': '大小', 'qmp_path': 'QMP路径', 'key': '已按下值', 'second_gui': '第二GUI', 'y': 'Y_按钮坐标', 'result': '结果', 'samples': '示例条目列', 'client': '客户端', 'line': '行', 'report': '有效性验证报告', 'work': '工作中路径', 'x': '横坐标坐标', 'python_checks': 'Python检查项', 'download': '下载', 'greeting': '问候例', 'dims': '尺寸值', 'chunk': '片段值', 'deadline': '截止时间时间', 'proc': '进程', 'content': '内容值', 'block': '数据块', 'marker': '标记', 'command': '命令', 'expected': '预期', 'shell': '命令壳', 'drawing': '绘图路径', 'f': '文件条目', 'transcript': '执行记录', 'offset': '偏移值', 'path': '路径', 'screenshot': '屏幕剪辑', 'arguments': '已转发参数', 'pixels': '像素列列表', 'viewer': '屏幕客户端', 'output': '输出结果', 'stream': '流值', 'cmd': '命令参数列', 'name': '名称', 'qmp': '测试替身控制连接状态'}
    for 上一个项目, 当前项目 in 映射值.items():
        if hasattr(实现, 当前项目): globals()[上一个项目] = getattr(实现, 当前项目)

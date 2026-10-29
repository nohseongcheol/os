#!/usr/bin/env python3
"""기존 路径 호환 条目分. 实际数据 实现: ../工具集/执行文件.py"""
import importlib as 取用值
import sys as 运行系统值
from pathlib import Path as 路径
运行系统值.path.insert(0, str(路径(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 运行器
    运行器.run_module('执行文件', run_name='__main__', alter_sys=True)
else:
    实现 = 取用值.import_module('执行文件')
    映射值 = {'timeout': '执行状态超时', 's': '字符串数据', 'i': '序数索引', 'match': '是否相等', 'files': '文件列表', 'program': '执行条目', 'executable': '可执行文件映像', 'args': '参数数组', 'chunk': '片段值', 'data': '数据', 'proc': '进程', 'send': '发送', 'main': '运行', 'marker': '标记', 'command': '命令', 'include': '包含条目', 'dumped': '已转储', 'run': '执行命令', 'p': '数据位置', 'parser': '参数解析器', 'options': '选择项集', 'kind': '分类值', 'selector': '就绪选择器', 'upload_data': '上传数据', 'end': '结束偏移', 'n': '项目个数', 'd': '目的地址数据', 'key': '已按下值', 'output': '输出结果', 'line': '行', 'name': '名称', 'upload_name': '上传名称', 'receive': '接收消息'}
    for 上一个项目, 当前项目 in 映射值.items():
        if hasattr(实现, 当前项目): globals()[上一个项目] = getattr(实现, 当前项目)

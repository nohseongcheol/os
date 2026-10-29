#!/usr/bin/env python3
"""기존 路径 호환 条目分. 实际数据 实现: ../工具集/测试FTP.py"""
import importlib as 取用值
import sys as 运行系统值
from pathlib import Path as 路径
运行系统值.path.insert(0, str(路径(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 运行器
    运行器.run_module('测试FTP', run_name='__main__', alter_sys=True)
else:
    实现 = 取用值.import_module('测试FTP')
    映射值 = {'timeout': '执行状态超时', 'payload': '载荷数据数据', 'broken': '已损坏', 'linux_example': 'Linux示例', 'chunk': '片段值', 'data': '数据', 'proc': '进程', 'code': '指令序列', 'linux': 'Linux文件', 'archive': '存档', 'main': '运行', 'net_source': '网络层源代码', 'temporary': '临时', 'static_source': '静态源代码', 'java_source': 'Java源代码', 'echo': '回显服务器条目', 'ROOT': '项目根', 'text': '文本', 'marker': '标记', 'EchoFixture': '回显测试夹具', 'command': '命令', 'out': '结果数据', 'expected': '预期', 'server_source': '服务器源代码', 'shell': '命令壳', 'upload': '上传文件集', 'transcript': '执行记录', 'port': '端口编号', 'native': '原生', 'elf': '可执行文件文件', 'server_udp_port': '服务器数据报端口', 'packed': '已打包', 'bridge': '桥接', 'selector': '就绪选择器', 'end': '结束偏移', 'e': '辅助条目', 'ftp': '文件传送连接状态', 'key': '已按下值', 'bytecode': '字节码', 'peer': '对端值', 'result': '结果', 'unchanged': '已保留数据', 'line': '行', 'server_tcp_port': '服务器流端口', 'source': '原始数据', 'NetworkBridge': '网络桥接', 'jar': 'Java捆绑', 'receive': '接收消息', 'report': '有效性验证报告'}
    for 上一个项目, 当前项目 in 映射值.items():
        if hasattr(实现, 当前项目): globals()[上一个项目] = getattr(实现, 当前项目)

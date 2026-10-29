#!/usr/bin/env python3
"""기존 路径 호환 条目分. 实际数据 实现: ../工具集/桌面视图.py"""
import importlib as 取用值
import sys as 运行系统值
from pathlib import Path as 路径
运行系统值.path.insert(0, str(路径(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 运行器
    运行器.run_module('桌面视图', run_name='__main__', alter_sys=True)
else:
    实现 = 取用值.import_module('桌面视图')
    映射值 = {'count': '条目个数', 'special': '特殊键', 'error': '错误', 'exact': '精确值', 'network': '使用网络', 'closed': '是否已关闭', 'length': '长度', 'opened': '已打开', 'ftp_port': '文件传送端口编号', 'server': '服务器值', 'resources': '资源集', 'data': '数据', 'shift': '移位键', 'send': '发送', 'run_desktop': '运行桌面', 'protocol': '网络ABI', 'forwards': '转发中规则列', 'host': '宿主', 'text': '文本', 'korean': '韩语', 'port': '端口编号', 'signum': '信号编号', 'version': '版本编号', 'parser': '参数解析器', 'bridge': '桥接', 'kind': '分类值', 'tail': '结尾部分', 'size': '大小', 'previous_buttons': '上一个按钮列', 'key': '已按下值', 'y': 'Y_按钮坐标', 'prefix': '前导部分', 'client': '客户端', 'char': '字符数据', 'work': '工作中路径', 'Keyboard': '键盘', 'x': '横坐标坐标', 'down': '是否按下中', 'net': '网络桥接条目', 'self': '自身值', 'mode_changed': '模式已更改', 'serial': '串行输入输出', 'args': '参数数组', 'Hangul': '合成韩文字母', 'chunk': '片段值', 'proc': '进程', 'Desktop': '连接桌面', 'buttons': '按钮列', 'thread': '后台任务', 'pressed': '是否已按下', 'previous': '上一个', 'toggle': '切换模式', 'command': '命令', 'sock': '套接字值', 'frame': '执行状态帧', 'ctrl': '控制键', 'path': '路径', 'cp': '字符编码状态', 'terminate': '终止', 'security': '安全性', 'vnc_port': 'VNC端口', 'body': '主体文本', 'index': '查找索引', 'exited': '拥有已退出', 'keysym': '键符号', 'output': '输出结果', 'keyboard': '键盘条目', 'interrupted': '已中断', 'listener': '接收端口', 'reader': '读取器', 'NetworkBridge': '网络桥接', 'gui': '绘图屏幕', 'worker': '处理任务'}
    for 上一个项目, 当前项目 in 映射值.items():
        if hasattr(实现, 当前项目): globals()[上一个项目] = getattr(实现, 当前项目)

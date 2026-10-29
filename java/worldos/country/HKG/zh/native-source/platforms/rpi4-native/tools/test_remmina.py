#!/usr/bin/env python3
"""기존 路径 호환 条目分. 实际数据 实现: ../工具集/测试Remmina.py"""
import importlib as 取用值
import sys as 运行系统值
from pathlib import Path as 路径
运行系统值.path.insert(0, str(路径(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 运行器
    运行器.run_module('测试Remmina', run_name='__main__', alter_sys=True)
else:
    实现 = 取用值.import_module('测试Remmina')
    映射值 = {'wait': '等待', 'typing': '已输入字符', 'start': '运行', 'profile': '配置档', 'focused': '已聚焦', 'serial': '串行输入输出', 'keys': '已按下键列', 'server': '服务器值', 'log': '日志记录', 'args': '参数数组', 'deadline': '截止时间时间', 'data': '数据', 'candidate': '候选', 'logs': '日志记录列', 'kw': '已命名参数', 'number': '数值值', 'main': '运行', 'ready': '准备状态完成', 'found': '搜索结果', 'guest': '客户机', 'ROOT': '项目根', 'marker': '标记', 'text': '文本', 'out': '结果数据', 'env': '环境', 'f': '文件条目', 'port': '端口编号', 'offset': '偏移值', 'version': '版本编号', 'p': '数据位置', 'selector': '就绪选择器', 'xvfb': '虚拟显示操作', 'display': '显示操作设备', 'n': '项目个数', 'key': '已按下值', 'processes': '运行中进程列', 'rootfs': '根文件系统', 'xdo': '虚拟输入工具', 'name': '名称', 'window': '窗口', 'report': '有效性验证报告', 'work': '工作中路径'}
    for 上一个项目, 当前项目 in 映射值.items():
        if hasattr(实现, 当前项目): globals()[上一个项目] = getattr(实现, 当前项目)

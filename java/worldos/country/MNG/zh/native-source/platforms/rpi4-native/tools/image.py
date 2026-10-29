#!/usr/bin/env python3
"""기존 路径 호환 条目分. 实际数据 实现: ../工具集/创建映像.py"""
import importlib as 取用值
import sys as 运行系统值
from pathlib import Path as 路径
运行系统值.path.insert(0, str(路径(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 运行器
    运行器.run_module('创建映像', run_name='__main__', alter_sys=True)
else:
    实现 = 取用值.import_module('创建映像')
    映射值 = {'total': '总计容量', 'start': '运行', 'firmware': '固件值', 'files': '文件列表', 'archive_base': '存档基底', 'partition': '分区文件', 'archive': '存档', 'main': '运行', 'block': '数据块', 'ROOT': '项目根', 'boot': '启动路径', 'stage': '阶段值', 'out': '结果数据', 'expected': '预期', 'f': '文件条目', 'src': '原始地址', 'path': '路径', 'p': '数据位置', 'extracted': '已提取', 'member': '成员', 'mbr': '主控启动记录', 'image': '映像', 'sector_count': '扇区个数', 'dist': '分发路径', 'sha': '计算哈希', 'license_': '许可', 'source': '原始数据', 'name': '名称', 'value': '值', 'manifest': '捆绑构建清单', 'dest': '目的地址值位置', 'work': '工作中路径'}
    for 上一个项目, 当前项目 in 映射值.items():
        if hasattr(实现, 当前项目): globals()[上一个项目] = getattr(实现, 当前项目)

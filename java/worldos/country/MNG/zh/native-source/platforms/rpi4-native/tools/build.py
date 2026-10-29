#!/usr/bin/env python3
"""기존 路径 호환 条目分. 实际数据 实现: ../工具集/构建系统.py"""
import importlib as 取用值
import sys as 运行系统值
from pathlib import Path as 路径
运行系统值.path.insert(0, str(路径(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 运行器
    运行器.run_module('构建系统', run_name='__main__', alter_sys=True)
else:
    实现 = 取用值.import_module('构建系统')
    映射值 = {'network': '使用网络', 'BUILD': '构建路径', 'ar': '存档工具', 'build_examples': '创建用例集', 'posix': 'POSIX', 'font_data': '字体数据', 'flags': '配置项位列', 'a': '首位值', 'cc': 'C编译器', 'args': '参数数组', 'source_flags': '原始配置项', 'ld': '链接器工具', 'method': '方法条目', 'main': '运行', 'objcopy': '对象文件转换器', 'ROOT': '项目根', 'cxx': 'Cpp编译器', 'includes': '包含项', 'compiler': '编译器工具', 'build_users': '创建用户空间', 'f': '文件条目', 'extra': '附加区域', 'exports': '导出表', 'jobs': '构建作业列', 'run': '执行命令', 'path': '路径', 'REPO': '代码库根', 'tool': '工具集', 'classes': '类路径', 'output': '输出结果', 'samples': '示例条目列', 'symbol': '符号值', 'source': '原始数据', 'name': '名称', 'build_network': '创建网络', 'font_info': '字体信息', 'manifest': '捆绑构建清单', 'work': '工作中路径'}
    for 上一个项目, 当前项目 in 映射值.items():
        if hasattr(实现, 当前项目): globals()[上一个项目] = getattr(实现, 当前项目)

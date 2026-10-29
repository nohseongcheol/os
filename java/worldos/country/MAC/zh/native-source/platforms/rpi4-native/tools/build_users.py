#!/usr/bin/env python3
"""기존 路径 호환 条目分. 实际数据 实现: ../工具集/构建用户空间.py"""
import importlib as 取用值
import sys as 运行系统值
from pathlib import Path as 路径
运行系统值.path.insert(0, str(路径(__file__).resolve().parents[1] / '工具集'))
if __name__ == '__main__':
    import runpy as 运行器
    运行器.run_module('构建用户空间', run_name='__main__', alter_sys=True)
else:
    实现 = 取用值.import_module('构建用户空间')
    映射值 = {'mode': '方法模式', 'header': '头部值', 'i': '序数索引', 'build_ccompiler': '创建C编译器', 'ar': '存档工具', 'posix': 'POSIX', 'payload': '载荷数据数据', 'flags': '配置项位列', 'cases': '测试情况', 'cc': 'C编译器', 'data': '数据', 'build_java_library': '创建Java库', 'ld': '链接器工具', 'repo': '代码库路径', 'build_python': '创建Python', 'inc': '包含路径', 'argument': '已转发值', 'text': '文本', 'headers': '头部列表', 'cxx': 'Cpp编译器', 'valid': '有效', 'build': '构建', 'build_users': '创建用户空间', 'compiler': '编译器工具', 'uzlib': '解压库', 'extra': '附加区域', 'phoff': '程序头部偏移', 'offset': '偏移值', 'text_address': '命令地址', 'abi': '调用ABI', 'assembly': '汇编', 'run': '执行命令', 'path': '路径', 'p': '数据位置', 'changed': '已更改', 'n': '项目个数', 'flag': '设置值', 'index': '查找索引', 'classes': '类路径', 'output': '输出结果', 'loads': '载入项', 'data_address': '数据地址', 'symbol': '符号值', 'root': '根地址', 'patches': '修改列', 'source': '原始数据', 'sizes': '大小列', 'blobs': '二进制块集', 'name': '名称', 'value': '值', 'fmt': '数据格式', 'work': '工作中路径'}
    for 上一个项目, 当前项目 in 映射值.items():
        if hasattr(实现, 当前项目): globals()[上一个项目] = getattr(实现, 当前项目)

#!/usr/bin/env python3
"""上一个项目 Python 경로를 Java 미리 번역기에 연결한다. 翻译源代码 구현은 Java工具/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from 编译器 import 编译过程错误

项目根 = Path(__file__).resolve().parent

class 计算机代码编译器:
    def __init__(自身值, 输入类集, 执行状态目标='kernel', 堆机器字个数=262144):
        自身值.路径列表 = [数据.路径 for 数据 in 输入类集]
        自身值.执行状态目标 = 执行状态目标
        自身值.堆机器字个数 = 堆机器字个数

    def 生成(自身值, 条目分, 导出条目列, 通用字符表示法=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 任务:
            结果路径 = Path(任务)/'generated.c'
            命令 = ['sh', str(项目根/'提前所属时间.sh'), '--entry', 条目分,
                    '--profile', 自身值.执行状态目标, '--heap-words', str(自身值.堆机器字个数), '-o', str(结果路径)]
            if 通用字符表示法: 命令.append('--ucn')
            for 赋值值 in 导出条目列: 命令.extend(['--export', 赋值值])
            命令.extend(str(路径) for 路径 in 自身值.路径列表)
            结果 = subprocess.run(命令, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if 结果.returncode: raise 编译过程错误(结果.stderr.decode('utf-8', 'replace'))
            return 结果路径.read_text()

def 运行():
    raise SystemExit(subprocess.call(['sh', str(项目根/'提前所属时间.sh')] + sys.argv[1:]))

if __name__ == '__main__': 运行()

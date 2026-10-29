#!/usr/bin/env python3
"""追加条目 Python 패키지 없이 中文 Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def 代码分个数(内容值, 库, 类目录):
    结果 = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(库), str(类目录)]), '字符命令', 内容值],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(结果.stdout.strip())


if __name__ == '__main__':
    解析参数列 = argparse.ArgumentParser(description=__doc__)
    解析参数列.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/中文Java.jar'))
    解析参数列.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    解析参数列.add_argument('--text', default='한글 😀')
    实参 = 解析参数列.parse_args()
    print('Python → 中文.Java.字符.代码分个数:',
          代码分个数(实参.text, 实参.jar, 实参.classes))

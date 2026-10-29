#!/usr/bin/env python3
"""入口追記 Python 패키지 없이 日本語 Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def コード点個数(内容物値, ライブラリ, クラスディレクトリ):
    結果 = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(ライブラリ), str(クラスディレクトリ)]), '文字命令', 内容物値],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(結果.stdout.strip())


if __name__ == '__main__':
    引数列解析 = argparse.ArgumentParser(description=__doc__)
    引数列解析.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/日本語Java.jar'))
    引数列解析.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    引数列解析.add_argument('--text', default='한글 😀')
    引数 = 引数列解析.parse_args()
    print('Python → 日本語.Java.文字.コード点個数:',
          コード点個数(引数.text, 引数.jar, 引数.classes))

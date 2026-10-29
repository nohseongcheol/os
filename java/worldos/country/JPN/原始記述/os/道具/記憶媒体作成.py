#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 格納値 매체를 만든다. 기존 ファイル/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def 入口作成(経路):
    with Path(経路).open('xb') as 出力:
        先頭部値 = bytearray(512)
        struct.pack_into('<8sII', 先頭部値, 0, b'JKSTORE1', 2048, 0x3153464a)
        出力.write(先頭部値)
        出力.truncate(2048 * 512)

if __name__ == '__main__':
    構文解析器 = argparse.ArgumentParser(description=__doc__)
    構文解析器.add_argument('経路')
    引数 = 構文解析器.parse_args()
    入口作成(引数.経路)

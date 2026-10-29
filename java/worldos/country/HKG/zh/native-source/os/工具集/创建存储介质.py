#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 存储值 매체를 만든다. 기존 文件/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def 创建条目(路径):
    with Path(路径).open('xb') as 输出:
        头值 = bytearray(512)
        struct.pack_into('<8sII', 头值, 0, b'JKSTORE1', 2048, 0x3153464a)
        输出.write(头值)
        输出.truncate(2048 * 512)

if __name__ == '__main__':
    解析器 = argparse.ArgumentParser(description=__doc__)
    解析器.add_argument('路径')
    实参 = 解析器.parse_args()
    创建条目(实参.路径)

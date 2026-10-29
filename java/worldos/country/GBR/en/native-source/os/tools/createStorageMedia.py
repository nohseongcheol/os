#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 storeValue 매체를 만든다. 기존 file/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def createEntry(path):
    with Path(path).open('xb') as Output:
        headValue = bytearray(512)
        struct.pack_into('<8sII', headValue, 0, b'JKSTORE1', 2048, 0x3153464a)
        Output.write(headValue)
        Output.truncate(2048 * 512)

if __name__ == '__main__':
    Parser = argparse.ArgumentParser(description=__doc__)
    Parser.add_argument('path')
    arguments = Parser.parse_args()
    createEntry(arguments.path)

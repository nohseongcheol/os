#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 存儲值 매체를 만든다. 기존 檔案/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def 創建條目(路徑):
    with Path(路徑).open('xb') as 輸出:
        頭值 = bytearray(512)
        struct.pack_into('<8sII', 頭值, 0, b'JKSTORE1', 2048, 0x3153464a)
        輸出.write(頭值)
        輸出.truncate(2048 * 512)

if __name__ == '__main__':
    解析器 = argparse.ArgumentParser(description=__doc__)
    解析器.add_argument('路徑')
    實參 = 解析器.parse_args()
    創建條目(實參.路徑)

#!/usr/bin/env python3
"""명시한 使用者 ELF만 讀取 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 可執行束打包():
    解析值 = argparse.ArgumentParser()
    解析值.add_argument('-o', required=True)
    解析值.add_argument('files', nargs='+', help='名稱=ELF경로')
    形式參數實際參數 = 解析值.parse_args()
    if len(形式參數實際參數.files) > 32:
        解析值.error('程式 最大值 32개')
    條目列列表 = []
    名稱列列表 = set()
    for 條目值 in 形式參數實際參數.files:
        名稱, 路徑 = 條目值.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', 名稱) or 名稱 in 名稱列列表:
            解析值.error('執行命令 이름이 잘못되었거나 중복됨: ' + 名稱)
        名稱列列表.add(名稱)
        資料 = Path(路徑).read_bytes()
        if len(資料) > 2 * 1024 * 1024:
            解析值.error('執行命令 파일이 너무 큼')
        條目列列表.append((名稱.encode(), 資料))
    結果 = bytearray(8 + 24 * len(條目列列表))
    struct.pack_into('<II', 結果, 0, 0x50414b4a, len(條目列列表))
    for 編號, (名稱, 資料) in enumerate(條目列列表):
        結果.extend(bytes((-len(結果)) % 16))
        struct.pack_into('<16sII', 結果, 8 + 編號 * 24, 名稱, len(結果), len(資料))
        結果.extend(資料)
    Path(形式參數實際參數.o).write_bytes(結果)

if __name__ == '__main__':
    可執行束打包()

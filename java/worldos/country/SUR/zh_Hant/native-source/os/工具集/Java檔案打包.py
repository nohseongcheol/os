#!/usr/bin/env python3
"""명시한 Java 原始碼樹/類別值 파일을 啓動 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 可執行束打包(條目列列表):
    檔案條目列 = []
    名稱列列表 = {'Hello.java'}
    顯式名稱列 = set()
    for 條目值 in 條目列列表:
        if '=' not in 條目值:
            raise ValueError('expected NAME=PATH: ' + 條目值)
        名稱, 路徑 = 條目值.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', 名稱) or 名稱 in 顯式名稱列:
            raise ValueError('invalid or duplicate file name: ' + 名稱)
        顯式名稱列.add(名稱)
        名稱列列表.add(名稱)
        資料 = Path(路徑).read_bytes()
        if len(資料) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + 名稱)
        檔案條目列.append((名稱.encode('ascii'), 資料))
    if len(名稱列列表) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    結果 = bytearray(struct.pack('<4sI', b'JKJF', len(檔案條目列)))
    結果.extend(bytes(72 * len(檔案條目列)))
    for 數, (名稱, 資料) in enumerate(檔案條目列):
        struct.pack_into('<64sII', 結果, 8 + 數 * 72, 名稱, len(結果), len(資料))
        結果.extend(資料)
    return bytes(結果)


if __name__ == '__main__':
    解析值 = argparse.ArgumentParser(description=__doc__)
    解析值.add_argument('-o', required=True)
    解析值.add_argument('files', nargs='*', help='NAME=PATH')
    實參 = 解析值.parse_args()
    try:
        資料 = 可執行束打包(實參.files)
        目的地址值 = Path(實參.o)
        if not 目的地址值.exists() or 目的地址值.read_bytes() != 資料:
            臨時值 = 目的地址值.with_name(目的地址值.name + '.tmp')
            臨時值.write_bytes(資料)
            臨時值.replace(目的地址值)
    except (ValueError, OSError) as 錯誤:
        解析值.error(str(錯誤))

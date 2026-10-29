#!/usr/bin/env python3
"""명시한 利用者 ELF만 読取 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 実行束梱包():
    値解析 = argparse.ArgumentParser()
    値解析.add_argument('-o', required=True)
    値解析.add_argument('files', nargs='+', help='名前=ELF경로')
    仮引数引数 = 値解析.parse_args()
    if len(仮引数引数.files) > 32:
        値解析.error('プログラム 最大値 32개')
    登録項目一覧一覧 = []
    名前一覧一覧 = set()
    for 入口値 in 仮引数引数.files:
        名前, 経路 = 入口値.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', 名前) or 名前 in 名前一覧一覧:
            値解析.error('命令実行 이름이 잘못되었거나 중복됨: ' + 名前)
        名前一覧一覧.add(名前)
        データ = Path(経路).read_bytes()
        if len(データ) > 2 * 1024 * 1024:
            値解析.error('命令実行 파일이 너무 큼')
        登録項目一覧一覧.append((名前.encode(), データ))
    結果 = bytearray(8 + 24 * len(登録項目一覧一覧))
    struct.pack_into('<II', 結果, 0, 0x50414b4a, len(登録項目一覧一覧))
    for 番号, (名前, データ) in enumerate(登録項目一覧一覧):
        結果.extend(bytes((-len(結果)) % 16))
        struct.pack_into('<16sII', 結果, 8 + 番号 * 24, 名前, len(結果), len(データ))
        結果.extend(データ)
    Path(仮引数引数.o).write_bytes(結果)

if __name__ == '__main__':
    実行束梱包()

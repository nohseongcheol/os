#!/usr/bin/env python3
"""명시한 Java ソース木/クラス値 파일을 起動 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 実行束梱包(登録項目一覧一覧):
    ファイル登録項目一覧 = []
    名前一覧一覧 = {'Hello.java'}
    明示名前一覧 = set()
    for 入口値 in 登録項目一覧一覧:
        if '=' not in 入口値:
            raise ValueError('expected NAME=PATH: ' + 入口値)
        名前, 経路 = 入口値.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', 名前) or 名前 in 明示名前一覧:
            raise ValueError('invalid or duplicate file name: ' + 名前)
        明示名前一覧.add(名前)
        名前一覧一覧.add(名前)
        データ = Path(経路).read_bytes()
        if len(データ) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + 名前)
        ファイル登録項目一覧.append((名前.encode('ascii'), データ))
    if len(名前一覧一覧) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    結果 = bytearray(struct.pack('<4sI', b'JKJF', len(ファイル登録項目一覧)))
    結果.extend(bytes(72 * len(ファイル登録項目一覧)))
    for 数, (名前, データ) in enumerate(ファイル登録項目一覧):
        struct.pack_into('<64sII', 結果, 8 + 数 * 72, 名前, len(結果), len(データ))
        結果.extend(データ)
    return bytes(結果)


if __name__ == '__main__':
    値解析 = argparse.ArgumentParser(description=__doc__)
    値解析.add_argument('-o', required=True)
    値解析.add_argument('files', nargs='*', help='NAME=PATH')
    引数 = 値解析.parse_args()
    try:
        データ = 実行束梱包(引数.files)
        宛先値 = Path(引数.o)
        if not 宛先値.exists() or 宛先値.read_bytes() != データ:
            一時値 = 宛先値.with_name(宛先値.name + '.tmp')
            一時値.write_bytes(データ)
            一時値.replace(宛先値)
    except (ValueError, OSError) as エラー:
        値解析.error(str(エラー))

#!/usr/bin/env python3
"""日本語 C 식별자만 UCN으로 옮긴다. 文字列·文字·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

トークン値 = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<識別子値>[^\W\d]\w*)', re.S | re.M)

def 値変換(ソース):
    def 値置換(判定等価):
        if 判定等価.lastgroup == '보존':
            return 判定等価[0]
        return ''.join(文字値 if ord(文字値) < 128 else
                       ('\\u%04x' if ord(文字値) <= 65535 else '\\U%08x') % ord(文字値)
                       for 文字値 in 判定等価[0])
    return トークン値.sub(値置換, ソース)

def 命令実行():
    構文解析器 = argparse.ArgumentParser()
    構文解析器.add_argument('原本', type=Path)
    構文解析器.add_argument('出力', type=Path)
    引数 = 構文解析器.parse_args()
    for ファイル in sorted(引数.原本.rglob('*')):
        if ファイル.suffix not in ('.c', '.h'):
            continue
        出力 = 引数.出力 / ファイル.relative_to(引数.原本)
        出力.parent.mkdir(parents=True, exist_ok=True)
        新規ソース = 値変換(ファイル.read_text())
        if not 出力.exists() or 出力.read_text() != 新規ソース:
            出力.write_text(新規ソース)

if __name__ == '__main__':
    命令実行()

#!/usr/bin/env python3
"""한국어 C 식별자만 UCN으로 옮긴다. sreang_VALUE·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

tòcan_VALUE = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<aithnichear_VALUE>[^\W\d]\w*)', re.S | re.M)

def CONVERT_VALUE(tùs):
    def REPLACE_VALUE(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(caractar_VALUE if ord(caractar_VALUE) < 128 else
                       ('\\u%04x' if ord(caractar_VALUE) <= 65535 else '\\U%08x') % ord(caractar_VALUE)
                       for caractar_VALUE in 일치[0])
    return tòcan_VALUE.sub(REPLACE_VALUE, tùs)

def gnìomhaich_àithne():
    해석기 = argparse.ArgumentParser()
    해석기.add_argument('원본', type=Path)
    해석기.add_argument('출력', type=Path)
    인수 = 해석기.parse_args()
    for faidhle in sorted(인수.원본.rglob('*')):
        if faidhle.suffix not in ('.c', '.h'):
            continue
        출력 = 인수.출력 / faidhle.relative_to(인수.원본)
        출력.parent.mkdir(parents=True, exist_ok=True)
        새원문 = CONVERT_VALUE(faidhle.read_text())
        if not 출력.exists() or 출력.read_text() != 새원문:
            출력.write_text(새원문)

if __name__ == '__main__':
    gnìomhaich_àithne()

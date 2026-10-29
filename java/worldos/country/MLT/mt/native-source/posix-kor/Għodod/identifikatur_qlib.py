#!/usr/bin/env python3
"""Malti C 식별자만 UCN으로 옮긴다. string_VALUE·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

token_VALUE = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<identifikatur_VALUE>[^\W\d]\w*)', re.S | re.M)

def CONVERT_VALUE(sors):
    def REPLACE_VALUE(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(karattru_VALUE if ord(karattru_VALUE) < 128 else
                       ('\\u%04x' if ord(karattru_VALUE) <= 65535 else '\\U%08x') % ord(karattru_VALUE)
                       for karattru_VALUE in 일치[0])
    return token_VALUE.sub(REPLACE_VALUE, sors)

def eżegwixxa_kmand():
    해석기 = argparse.ArgumentParser()
    해석기.add_argument('원본', type=Path)
    해석기.add_argument('출력', type=Path)
    인수 = 해석기.parse_args()
    for fajl in sorted(인수.원본.rglob('*')):
        if fajl.suffix not in ('.c', '.h'):
            continue
        출력 = 인수.출력 / fajl.relative_to(인수.원본)
        출력.parent.mkdir(parents=True, exist_ok=True)
        새원문 = CONVERT_VALUE(fajl.read_text())
        if not 출력.exists() or 출력.read_text() != 새원문:
            출력.write_text(새원문)

if __name__ == '__main__':
    eżegwixxa_kmand()

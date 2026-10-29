#!/usr/bin/env python3
"""Татарча C 식별자만 UCN으로 옮긴다. юл_VALUE_6ca8363c·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

токен_VALUE = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<күрсәткеч_VALUE>[^\W\d]\w*)', re.S | re.M)

def CONVERT_VALUE(чыганак):
    def REPLACE_VALUE(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(символ_VALUE_068c2631 if ord(символ_VALUE_068c2631) < 128 else
                       ('\\u%04x' if ord(символ_VALUE_068c2631) <= 65535 else '\\U%08x') % ord(символ_VALUE_068c2631)
                       for символ_VALUE_068c2631 in 일치[0])
    return токен_VALUE.sub(REPLACE_VALUE, чыганак)

def үтәргә_команда():
    해석기 = argparse.ArgumentParser()
    해석기.add_argument('원본', type=Path)
    해석기.add_argument('출력', type=Path)
    인수 = 해석기.parse_args()
    for Birem in sorted(인수.원본.rglob('*')):
        if Birem.suffix not in ('.c', '.h'):
            continue
        출력 = 인수.출력 / Birem.relative_to(인수.원본)
        출력.parent.mkdir(parents=True, exist_ok=True)
        새원문 = CONVERT_VALUE(Birem.read_text())
        if not 출력.exists() or 출력.read_text() != 새원문:
            출력.write_text(새원문)

if __name__ == '__main__':
    үтәргә_команда()

#!/usr/bin/env python3
"""Македонски C 식별자만 UCN으로 옮긴다. низа_VALUE_6ca8363c·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

токен_VALUE = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<идентификатор_VALUE>[^\W\d]\w*)', re.S | re.M)

def CONVERT_VALUE(ИЗВОР):
    def замени_VALUE(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(знак_VALUE if ord(знак_VALUE) < 128 else
                       ('\\u%04x' if ord(знак_VALUE) <= 65535 else '\\U%08x') % ord(знак_VALUE)
                       for знак_VALUE in 일치[0])
    return токен_VALUE.sub(замени_VALUE, ИЗВОР)

def Изврши_наредба():
    анализатор_48ee4b1b = argparse.ArgumentParser()
    анализатор_48ee4b1b.add_argument('원본', type=Path)
    анализатор_48ee4b1b.add_argument('출력', type=Path)
    Аргументи = анализатор_48ee4b1b.parse_args()
    for Датотека in sorted(Аргументи.원본.rglob('*')):
        if Датотека.suffix not in ('.c', '.h'):
            continue
        출력 = Аргументи.출력 / Датотека.relative_to(Аргументи.원본)
        출력.parent.mkdir(parents=True, exist_ok=True)
        새원문 = CONVERT_VALUE(Датотека.read_text())
        if not 출력.exists() or 출력.read_text() != 새원문:
            출력.write_text(새원문)

if __name__ == '__main__':
    Изврши_наредба()

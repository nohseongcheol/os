#!/usr/bin/env python3
"""한국어 C 식별자만 UCN으로 옮긴다. varg_VALUE·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

kodi_VALUE = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<identifikues_VALUE>[^\W\d]\w*)', re.S | re.M)

def CONVERT_VALUE(BURIMI):
    def REPLACE_VALUE(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(karakter_VALUE if ord(karakter_VALUE) < 128 else
                       ('\\u%04x' if ord(karakter_VALUE) <= 65535 else '\\U%08x') % ord(karakter_VALUE)
                       for karakter_VALUE in 일치[0])
    return kodi_VALUE.sub(REPLACE_VALUE, BURIMI)

def zbatoj_komandë():
    analizues_48ee4b1b = argparse.ArgumentParser()
    analizues_48ee4b1b.add_argument('원본', type=Path)
    analizues_48ee4b1b.add_argument('출력', type=Path)
    Argumente = analizues_48ee4b1b.parse_args()
    for Kartelë in sorted(Argumente.원본.rglob('*')):
        if Kartelë.suffix not in ('.c', '.h'):
            continue
        출력 = Argumente.출력 / Kartelë.relative_to(Argumente.원본)
        출력.parent.mkdir(parents=True, exist_ok=True)
        새원문 = CONVERT_VALUE(Kartelë.read_text())
        if not 출력.exists() or 출력.read_text() != 새원문:
            출력.write_text(새원문)

if __name__ == '__main__':
    zbatoj_komandë()

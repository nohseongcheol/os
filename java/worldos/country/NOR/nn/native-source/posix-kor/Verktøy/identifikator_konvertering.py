#!/usr/bin/env python3
"""한국어 C 식별자만 UCN으로 옮긴다. streng_VALUE·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

token_VALUE = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<identifikator_VALUE>[^\W\d]\w*)', re.S | re.M)

def CONVERT_VALUE(KJELDE):
    def REPLACE_VALUE(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(teikn_VALUE if ord(teikn_VALUE) < 128 else
                       ('\\u%04x' if ord(teikn_VALUE) <= 65535 else '\\U%08x') % ord(teikn_VALUE)
                       for teikn_VALUE in 일치[0])
    return token_VALUE.sub(REPLACE_VALUE, KJELDE)

def Utfør_kommando():
    해석기 = argparse.ArgumentParser()
    해석기.add_argument('원본', type=Path)
    해석기.add_argument('Utdata', type=Path)
    Argument = 해석기.parse_args()
    for Fil in sorted(Argument.원본.rglob('*')):
        if Fil.suffix not in ('.c', '.h'):
            continue
        Utdata = Argument.Utdata / Fil.relative_to(Argument.원본)
        Utdata.parent.mkdir(parents=True, exist_ok=True)
        새원문 = CONVERT_VALUE(Fil.read_text())
        if not Utdata.exists() or Utdata.read_text() != 새원문:
            Utdata.write_text(새원문)

if __name__ == '__main__':
    Utfør_kommando()

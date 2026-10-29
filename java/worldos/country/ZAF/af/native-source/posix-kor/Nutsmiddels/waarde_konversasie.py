#!/usr/bin/env python3
"""한국어 C 식별자만 UCN으로 옮긴다. string_VALUE·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

kenteken_VALUE = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<waarde_VALUE>[^\W\d]\w*)', re.S | re.M)

def CONVERT_VALUE(Bron):
    def REPLACE_VALUE(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(karakter_VALUE if ord(karakter_VALUE) < 128 else
                       ('\\u%04x' if ord(karakter_VALUE) <= 65535 else '\\U%08x') % ord(karakter_VALUE)
                       for karakter_VALUE in 일치[0])
    return kenteken_VALUE.sub(REPLACE_VALUE, Bron)

def uitvoer_bevel():
    ontleder_48ee4b1b = argparse.ArgumentParser()
    ontleder_48ee4b1b.add_argument('원본', type=Path)
    ontleder_48ee4b1b.add_argument('Afvoer', type=Path)
    인수 = ontleder_48ee4b1b.parse_args()
    for Lêer in sorted(인수.원본.rglob('*')):
        if Lêer.suffix not in ('.c', '.h'):
            continue
        Afvoer = 인수.Afvoer / Lêer.relative_to(인수.원본)
        Afvoer.parent.mkdir(parents=True, exist_ok=True)
        새원문 = CONVERT_VALUE(Lêer.read_text())
        if not Afvoer.exists() or Afvoer.read_text() != 새원문:
            Afvoer.write_text(새원문)

if __name__ == '__main__':
    uitvoer_bevel()

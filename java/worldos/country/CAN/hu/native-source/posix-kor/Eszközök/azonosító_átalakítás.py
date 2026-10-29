#!/usr/bin/env python3
"""magyar C 식별자만 UCN으로 옮긴다. sztring_ÉRTÉK·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

kód_ÉRTÉK = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<azonosító_ÉRTÉK>[^\W\d]\w*)', re.S | re.M)

def konvertál_ÉRTÉK(FORRÁS):
    def CSERE_ÉRTÉK(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(karakter_ÉRTÉK if ord(karakter_ÉRTÉK) < 128 else
                       ('\\u%04x' if ord(karakter_ÉRTÉK) <= 65535 else '\\U%08x') % ord(karakter_ÉRTÉK)
                       for karakter_ÉRTÉK in 일치[0])
    return kód_ÉRTÉK.sub(CSERE_ÉRTÉK, FORRÁS)

def végrehajt_parancs():
    elemző_48ee4b1b = argparse.ArgumentParser()
    elemző_48ee4b1b.add_argument('원본', type=Path)
    elemző_48ee4b1b.add_argument('Kimenet', type=Path)
    Argumentumok = elemző_48ee4b1b.parse_args()
    for Fájl in sorted(Argumentumok.원본.rglob('*')):
        if Fájl.suffix not in ('.c', '.h'):
            continue
        Kimenet = Argumentumok.Kimenet / Fájl.relative_to(Argumentumok.원본)
        Kimenet.parent.mkdir(parents=True, exist_ok=True)
        새원문 = konvertál_ÉRTÉK(Fájl.read_text())
        if not Kimenet.exists() or Kimenet.read_text() != 새원문:
            Kimenet.write_text(새원문)

if __name__ == '__main__':
    végrehajt_parancs()

#!/usr/bin/env python3
"""한국어 C 식별자만 UCN으로 옮긴다. string_VALUE·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

token_VALUE = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<identifikator_VALUE>[^\W\d]\w*)', re.S | re.M)

def CONVERT_VALUE(IZVOR):
    def REPLACE_VALUE(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(znak_VALUE if ord(znak_VALUE) < 128 else
                       ('\\u%04x' if ord(znak_VALUE) <= 65535 else '\\U%08x') % ord(znak_VALUE)
                       for znak_VALUE in 일치[0])
    return token_VALUE.sub(REPLACE_VALUE, IZVOR)

def Izvrši_komanda():
    해석기 = argparse.ArgumentParser()
    해석기.add_argument('원본', type=Path)
    해석기.add_argument('Ispis', type=Path)
    Argumenti = 해석기.parse_args()
    for Fajl in sorted(Argumenti.원본.rglob('*')):
        if Fajl.suffix not in ('.c', '.h'):
            continue
        Ispis = Argumenti.Ispis / Fajl.relative_to(Argumenti.원본)
        Ispis.parent.mkdir(parents=True, exist_ok=True)
        새원문 = CONVERT_VALUE(Fajl.read_text())
        if not Ispis.exists() or Ispis.read_text() != 새원문:
            Ispis.write_text(새원문)

if __name__ == '__main__':
    Izvrši_komanda()

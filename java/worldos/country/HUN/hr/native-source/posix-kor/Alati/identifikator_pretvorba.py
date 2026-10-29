#!/usr/bin/env python3
"""hrvatski C 식별자만 UCN으로 옮긴다. niz_VALUE·문자·주석·include 파일명은 보존한다."""
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

def Izvrši_naredba():
    analizator_48ee4b1b = argparse.ArgumentParser()
    analizator_48ee4b1b.add_argument('원본', type=Path)
    analizator_48ee4b1b.add_argument('Izlaz', type=Path)
    Argumenti = analizator_48ee4b1b.parse_args()
    for Datoteka in sorted(Argumenti.원본.rglob('*')):
        if Datoteka.suffix not in ('.c', '.h'):
            continue
        Izlaz = Argumenti.Izlaz / Datoteka.relative_to(Argumenti.원본)
        Izlaz.parent.mkdir(parents=True, exist_ok=True)
        새원문 = CONVERT_VALUE(Datoteka.read_text())
        if not Izlaz.exists() or Izlaz.read_text() != 새원문:
            Izlaz.write_text(새원문)

if __name__ == '__main__':
    Izvrši_naredba()

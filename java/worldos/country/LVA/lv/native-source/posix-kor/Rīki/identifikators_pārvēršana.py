#!/usr/bin/env python3
"""Latviešu C 식별자만 UCN으로 옮긴다. virkne_VALUE·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

daļiņa_VALUE = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<identifikators_VALUE>[^\W\d]\w*)', re.S | re.M)

def CONVERT_VALUE(AVOTS):
    def REPLACE_VALUE(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(rakstzīme_VALUE if ord(rakstzīme_VALUE) < 128 else
                       ('\\u%04x' if ord(rakstzīme_VALUE) <= 65535 else '\\U%08x') % ord(rakstzīme_VALUE)
                       for rakstzīme_VALUE in 일치[0])
    return daļiņa_VALUE.sub(REPLACE_VALUE, AVOTS)

def Izpildīt_komanda():
    parsētājs_48ee4b1b = argparse.ArgumentParser()
    parsētājs_48ee4b1b.add_argument('원본', type=Path)
    parsētājs_48ee4b1b.add_argument('Izvade', type=Path)
    Parametri = parsētājs_48ee4b1b.parse_args()
    for Fails in sorted(Parametri.원본.rglob('*')):
        if Fails.suffix not in ('.c', '.h'):
            continue
        Izvade = Parametri.Izvade / Fails.relative_to(Parametri.원본)
        Izvade.parent.mkdir(parents=True, exist_ok=True)
        새원문 = CONVERT_VALUE(Fails.read_text())
        if not Izvade.exists() or Izvade.read_text() != 새원문:
            Izvade.write_text(새원문)

if __name__ == '__main__':
    Izpildīt_komanda()

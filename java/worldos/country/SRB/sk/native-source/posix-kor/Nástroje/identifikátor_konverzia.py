#!/usr/bin/env python3
"""Slovenský C 식별자만 UCN으로 옮긴다. reťazec_VALUE·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

token_VALUE = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<identifikátor_VALUE>[^\W\d]\w*)', re.S | re.M)

def CONVERT_VALUE(ZDROJ):
    def REPLACE_VALUE(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(znak_VALUE if ord(znak_VALUE) < 128 else
                       ('\\u%04x' if ord(znak_VALUE) <= 65535 else '\\U%08x') % ord(znak_VALUE)
                       for znak_VALUE in 일치[0])
    return token_VALUE.sub(REPLACE_VALUE, ZDROJ)

def Vykonať_príkaz():
    analyzátor_48ee4b1b = argparse.ArgumentParser()
    analyzátor_48ee4b1b.add_argument('원본', type=Path)
    analyzátor_48ee4b1b.add_argument('Výstup', type=Path)
    Argumenty = analyzátor_48ee4b1b.parse_args()
    for Súbor in sorted(Argumenty.원본.rglob('*')):
        if Súbor.suffix not in ('.c', '.h'):
            continue
        Výstup = Argumenty.Výstup / Súbor.relative_to(Argumenty.원본)
        Výstup.parent.mkdir(parents=True, exist_ok=True)
        새원문 = CONVERT_VALUE(Súbor.read_text())
        if not Výstup.exists() or Výstup.read_text() != 새원문:
            Výstup.write_text(새원문)

if __name__ == '__main__':
    Vykonať_príkaz()

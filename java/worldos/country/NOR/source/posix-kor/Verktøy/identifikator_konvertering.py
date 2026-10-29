#!/usr/bin/env python3
"""norsk C 식별자만 UCN으로 옮긴다. streng_VERDI·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

token_VERDI = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<identifikator_VERDI>[^\W\d]\w*)', re.S | re.M)

def KONVERTER_VERDI(KILDE):
    def ERSTATT_VERDI(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(tegn_VERDI if ord(tegn_VERDI) < 128 else
                       ('\\u%04x' if ord(tegn_VERDI) <= 65535 else '\\U%08x') % ord(tegn_VERDI)
                       for tegn_VERDI in 일치[0])
    return token_VERDI.sub(ERSTATT_VERDI, KILDE)

def Utfør_kommando():
    parser_48ee4b1b = argparse.ArgumentParser()
    parser_48ee4b1b.add_argument('원본', type=Path)
    parser_48ee4b1b.add_argument('Utgang', type=Path)
    Argumenter = parser_48ee4b1b.parse_args()
    for Fil in sorted(Argumenter.원본.rglob('*')):
        if Fil.suffix not in ('.c', '.h'):
            continue
        Utgang = Argumenter.Utgang / Fil.relative_to(Argumenter.원본)
        Utgang.parent.mkdir(parents=True, exist_ok=True)
        새원문 = KONVERTER_VERDI(Fil.read_text())
        if not Utgang.exists() or Utgang.read_text() != 새원문:
            Utgang.write_text(새원문)

if __name__ == '__main__':
    Utfør_kommando()

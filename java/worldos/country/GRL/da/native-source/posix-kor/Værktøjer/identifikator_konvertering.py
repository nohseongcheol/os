#!/usr/bin/env python3
"""Dansk C 식별자만 UCN으로 옮긴다. streng_VÆRDI·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

token_VÆRDI = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<identifikator_VÆRDI>[^\W\d]\w*)', re.S | re.M)

def KONVERTER_VÆRDI(KILDE):
    def ERSTAT_VÆRDI(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(tegn_VÆRDI if ord(tegn_VÆRDI) < 128 else
                       ('\\u%04x' if ord(tegn_VÆRDI) <= 65535 else '\\U%08x') % ord(tegn_VÆRDI)
                       for tegn_VÆRDI in 일치[0])
    return token_VÆRDI.sub(ERSTAT_VÆRDI, KILDE)

def Udfør_kommando():
    parser_48ee4b1b = argparse.ArgumentParser()
    parser_48ee4b1b.add_argument('원본', type=Path)
    parser_48ee4b1b.add_argument('Udgang', type=Path)
    Argumenter = parser_48ee4b1b.parse_args()
    for Fil in sorted(Argumenter.원본.rglob('*')):
        if Fil.suffix not in ('.c', '.h'):
            continue
        Udgang = Argumenter.Udgang / Fil.relative_to(Argumenter.원본)
        Udgang.parent.mkdir(parents=True, exist_ok=True)
        새원문 = KONVERTER_VÆRDI(Fil.read_text())
        if not Udgang.exists() or Udgang.read_text() != 새원문:
            Udgang.write_text(새원문)

if __name__ == '__main__':
    Udfør_kommando()

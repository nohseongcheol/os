#!/usr/bin/env python3
"""Lietuvių C 식별자만 UCN으로 옮긴다. eilutė_VALUE·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

žetonas_VALUE = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<identifikatorius_VALUE>[^\W\d]\w*)', re.S | re.M)

def CONVERT_VALUE(ŠALTINIS):
    def REPLACE_VALUE(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(simbolis_VALUE_068c2631 if ord(simbolis_VALUE_068c2631) < 128 else
                       ('\\u%04x' if ord(simbolis_VALUE_068c2631) <= 65535 else '\\U%08x') % ord(simbolis_VALUE_068c2631)
                       for simbolis_VALUE_068c2631 in 일치[0])
    return žetonas_VALUE.sub(REPLACE_VALUE, ŠALTINIS)

def Vykdyti_komanda():
    analizatorius_48ee4b1b = argparse.ArgumentParser()
    analizatorius_48ee4b1b.add_argument('원본', type=Path)
    analizatorius_48ee4b1b.add_argument('Išvestis', type=Path)
    Argumentai = analizatorius_48ee4b1b.parse_args()
    for Failas in sorted(Argumentai.원본.rglob('*')):
        if Failas.suffix not in ('.c', '.h'):
            continue
        Išvestis = Argumentai.Išvestis / Failas.relative_to(Argumentai.원본)
        Išvestis.parent.mkdir(parents=True, exist_ok=True)
        새원문 = CONVERT_VALUE(Failas.read_text())
        if not Išvestis.exists() or Išvestis.read_text() != 새원문:
            Išvestis.write_text(새원문)

if __name__ == '__main__':
    Vykdyti_komanda()

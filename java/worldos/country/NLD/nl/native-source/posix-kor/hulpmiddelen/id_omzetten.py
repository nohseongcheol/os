#!/usr/bin/env python3
"""Nederlands C 식별자만 UCN으로 옮긴다. tekenreeks_WAARDE·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

token_WAARDE = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<id_WAARDE>[^\W\d]\w*)', re.S | re.M)

def CONVERTEREN_WAARDE(broncode):
    def VERVANGEN_WAARDE(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(teken_WAARDE if ord(teken_WAARDE) < 128 else
                       ('\\u%04x' if ord(teken_WAARDE) <= 65535 else '\\U%08x') % ord(teken_WAARDE)
                       for teken_WAARDE in 일치[0])
    return token_WAARDE.sub(VERVANGEN_WAARDE, broncode)

def Uitvoeren_opdracht():
    parser_48ee4b1b = argparse.ArgumentParser()
    parser_48ee4b1b.add_argument('원본', type=Path)
    parser_48ee4b1b.add_argument('tekstuitvoer', type=Path)
    argumenten = parser_48ee4b1b.parse_args()
    for bestand in sorted(argumenten.원본.rglob('*')):
        if bestand.suffix not in ('.c', '.h'):
            continue
        tekstuitvoer = argumenten.tekstuitvoer / bestand.relative_to(argumenten.원본)
        tekstuitvoer.parent.mkdir(parents=True, exist_ok=True)
        새원문 = CONVERTEREN_WAARDE(bestand.read_text())
        if not tekstuitvoer.exists() or tekstuitvoer.read_text() != 새원문:
            tekstuitvoer.write_text(새원문)

if __name__ == '__main__':
    Uitvoeren_opdracht()

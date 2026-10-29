#!/usr/bin/env python3
"""Svenska C 식별자만 UCN으로 옮긴다. sträng_värde·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

kod_värde = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<identifierare_värde>[^\W\d]\w*)', re.S | re.M)

def KONVERTERA_värde(källfil):
    def ERSÄTT_värde(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(tecken_värde if ord(tecken_värde) < 128 else
                       ('\\u%04x' if ord(tecken_värde) <= 65535 else '\\U%08x') % ord(tecken_värde)
                       for tecken_värde in 일치[0])
    return kod_värde.sub(ERSÄTT_värde, källfil)

def köra_kommando():
    parser_48ee4b1b = argparse.ArgumentParser()
    parser_48ee4b1b.add_argument('원본', type=Path)
    parser_48ee4b1b.add_argument('utmatningsposition', type=Path)
    argument = parser_48ee4b1b.parse_args()
    for filnamn in sorted(argument.원본.rglob('*')):
        if filnamn.suffix not in ('.c', '.h'):
            continue
        utmatningsposition = argument.utmatningsposition / filnamn.relative_to(argument.원본)
        utmatningsposition.parent.mkdir(parents=True, exist_ok=True)
        새원문 = KONVERTERA_värde(filnamn.read_text())
        if not utmatningsposition.exists() or utmatningsposition.read_text() != 새원문:
            utmatningsposition.write_text(새원문)

if __name__ == '__main__':
    köra_kommando()

#!/usr/bin/env python3
"""čeština C 식별자만 UCN으로 옮긴다. řetězec_HODNOTA·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

token_HODNOTA = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<identifikátor_HODNOTA>[^\W\d]\w*)', re.S | re.M)

def CONVERT_HODNOTA(zdrojový_soubor):
    def NAHRADIT_HODNOTA(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(znak_HODNOTA if ord(znak_HODNOTA) < 128 else
                       ('\\u%04x' if ord(znak_HODNOTA) <= 65535 else '\\U%08x') % ord(znak_HODNOTA)
                       for znak_HODNOTA in 일치[0])
    return token_HODNOTA.sub(NAHRADIT_HODNOTA, zdrojový_soubor)

def Provést_příkaz():
    analyzátor_48ee4b1b = argparse.ArgumentParser()
    analyzátor_48ee4b1b.add_argument('원본', type=Path)
    analyzátor_48ee4b1b.add_argument('výstupní_pozice', type=Path)
    argumenty = analyzátor_48ee4b1b.parse_args()
    for název_souboru in sorted(argumenty.원본.rglob('*')):
        if název_souboru.suffix not in ('.c', '.h'):
            continue
        výstupní_pozice = argumenty.výstupní_pozice / název_souboru.relative_to(argumenty.원본)
        výstupní_pozice.parent.mkdir(parents=True, exist_ok=True)
        새원문 = CONVERT_HODNOTA(název_souboru.read_text())
        if not výstupní_pozice.exists() or výstupní_pozice.read_text() != 새원문:
            výstupní_pozice.write_text(새원문)

if __name__ == '__main__':
    Provést_příkaz()

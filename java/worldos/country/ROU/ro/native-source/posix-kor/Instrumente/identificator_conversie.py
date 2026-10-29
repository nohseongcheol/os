#!/usr/bin/env python3
"""Română C 식별자만 UCN으로 옮긴다. șir_VALUE·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

token_VALUE = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<identificator_VALUE>[^\W\d]\w*)', re.S | re.M)

def CONVERT_VALUE(SURSĂ):
    def REPLACE_VALUE(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(caracter_VALUE if ord(caracter_VALUE) < 128 else
                       ('\\u%04x' if ord(caracter_VALUE) <= 65535 else '\\U%08x') % ord(caracter_VALUE)
                       for caracter_VALUE in 일치[0])
    return token_VALUE.sub(REPLACE_VALUE, SURSĂ)

def executa_comandă():
    parser_48ee4b1b = argparse.ArgumentParser()
    parser_48ee4b1b.add_argument('원본', type=Path)
    parser_48ee4b1b.add_argument('Rezultat', type=Path)
    Argumente = parser_48ee4b1b.parse_args()
    for Fișier in sorted(Argumente.원본.rglob('*')):
        if Fișier.suffix not in ('.c', '.h'):
            continue
        Rezultat = Argumente.Rezultat / Fișier.relative_to(Argumente.원본)
        Rezultat.parent.mkdir(parents=True, exist_ok=True)
        새원문 = CONVERT_VALUE(Fișier.read_text())
        if not Rezultat.exists() or Rezultat.read_text() != 새원문:
            Rezultat.write_text(새원문)

if __name__ == '__main__':
    executa_comandă()

#!/usr/bin/env python3
"""Euskara C 식별자만 UCN으로 옮긴다. kate_balio·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

token_balio = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<identifikatzaile_balio>[^\W\d]\w*)', re.S | re.M)

def BIHURTU_balio(ITURBURUA):
    def ORDEZTU_balio(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(karaktere_balio if ord(karaktere_balio) < 128 else
                       ('\\u%04x' if ord(karaktere_balio) <= 65535 else '\\U%08x') % ord(karaktere_balio)
                       for karaktere_balio in 일치[0])
    return token_balio.sub(ORDEZTU_balio, ITURBURUA)

def exekutatu_komando():
    analizatzaile_48ee4b1b = argparse.ArgumentParser()
    analizatzaile_48ee4b1b.add_argument('원본', type=Path)
    analizatzaile_48ee4b1b.add_argument('Irteera', type=Path)
    Argumentuak = analizatzaile_48ee4b1b.parse_args()
    for Fitxategia in sorted(Argumentuak.원본.rglob('*')):
        if Fitxategia.suffix not in ('.c', '.h'):
            continue
        Irteera = Argumentuak.Irteera / Fitxategia.relative_to(Argumentuak.원본)
        Irteera.parent.mkdir(parents=True, exist_ok=True)
        새원문 = BIHURTU_balio(Fitxategia.read_text())
        if not Irteera.exists() or Irteera.read_text() != 새원문:
            Irteera.write_text(새원문)

if __name__ == '__main__':
    exekutatu_komando()

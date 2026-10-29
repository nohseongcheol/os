#!/usr/bin/env python3
"""Italiano C 식별자만 UCN으로 옮긴다. stringa_VALORE·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

token_VALORE = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<identificatore_VALORE>[^\W\d]\w*)', re.S | re.M)

def CONVERTI_VALORE(codiceSorgente):
    def RIMPIAZZA_VALORE(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(carattere_VALORE if ord(carattere_VALORE) < 128 else
                       ('\\u%04x' if ord(carattere_VALORE) <= 65535 else '\\U%08x') % ord(carattere_VALORE)
                       for carattere_VALORE in 일치[0])
    return token_VALORE.sub(RIMPIAZZA_VALORE, codiceSorgente)

def Esegui_comando():
    parser_48ee4b1b = argparse.ArgumentParser()
    parser_48ee4b1b.add_argument('원본', type=Path)
    parser_48ee4b1b.add_argument('uscitaTesto', type=Path)
    argomenti = parser_48ee4b1b.parse_args()
    for file in sorted(argomenti.원본.rglob('*')):
        if file.suffix not in ('.c', '.h'):
            continue
        uscitaTesto = argomenti.uscitaTesto / file.relative_to(argomenti.원본)
        uscitaTesto.parent.mkdir(parents=True, exist_ok=True)
        새원문 = CONVERTI_VALORE(file.read_text())
        if not uscitaTesto.exists() or uscitaTesto.read_text() != 새원문:
            uscitaTesto.write_text(새원문)

if __name__ == '__main__':
    Esegui_comando()

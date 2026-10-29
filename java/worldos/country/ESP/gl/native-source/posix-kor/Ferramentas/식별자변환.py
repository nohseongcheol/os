#!/usr/bin/env python3
"""Galego C 식별자만 UCN으로 옮긴다. cadea_VALOR·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

ficha_VALOR = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<식별자>[^\W\d]\w*)', re.S | re.M)

def CONVERTER_VALOR(FONTE):
    def SUBSTITUÍR_VALOR(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(carácter_VALOR if ord(carácter_VALOR) < 128 else
                       ('\\u%04x' if ord(carácter_VALOR) <= 65535 else '\\U%08x') % ord(carácter_VALOR)
                       for carácter_VALOR in 일치[0])
    return ficha_VALOR.sub(SUBSTITUÍR_VALOR, FONTE)

def executar_comando():
    analizador_48ee4b1b = argparse.ArgumentParser()
    analizador_48ee4b1b.add_argument('원본', type=Path)
    analizador_48ee4b1b.add_argument('Saída', type=Path)
    Argumentos = analizador_48ee4b1b.parse_args()
    for Ficheiro in sorted(Argumentos.원본.rglob('*')):
        if Ficheiro.suffix not in ('.c', '.h'):
            continue
        Saída = Argumentos.Saída / Ficheiro.relative_to(Argumentos.원본)
        Saída.parent.mkdir(parents=True, exist_ok=True)
        새원문 = CONVERTER_VALOR(Ficheiro.read_text())
        if not Saída.exists() or Saída.read_text() != 새원문:
            Saída.write_text(새원문)

if __name__ == '__main__':
    executar_comando()

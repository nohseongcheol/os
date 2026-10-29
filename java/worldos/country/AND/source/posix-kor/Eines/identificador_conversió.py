#!/usr/bin/env python3
"""Català C 식별자만 UCN으로 옮긴다. cadena_VALOR·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

testimoni_VALOR = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<identificador_VALOR>[^\W\d]\w*)', re.S | re.M)

def CONVERT_VALOR(FONT):
    def REEMPLAÇA_VALOR(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(caràcter_VALOR if ord(caràcter_VALOR) < 128 else
                       ('\\u%04x' if ord(caràcter_VALOR) <= 65535 else '\\U%08x') % ord(caràcter_VALOR)
                       for caràcter_VALOR in 일치[0])
    return testimoni_VALOR.sub(REEMPLAÇA_VALOR, FONT)

def Executa_ordre():
    analitzador_48ee4b1b = argparse.ArgumentParser()
    analitzador_48ee4b1b.add_argument('원본', type=Path)
    analitzador_48ee4b1b.add_argument('Sortida', type=Path)
    인수 = analitzador_48ee4b1b.parse_args()
    for Fitxer in sorted(인수.원본.rglob('*')):
        if Fitxer.suffix not in ('.c', '.h'):
            continue
        Sortida = 인수.Sortida / Fitxer.relative_to(인수.원본)
        Sortida.parent.mkdir(parents=True, exist_ok=True)
        새원문 = CONVERT_VALOR(Fitxer.read_text())
        if not Sortida.exists() or Sortida.read_text() != 새원문:
            Sortida.write_text(새원문)

if __name__ == '__main__':
    Executa_ordre()

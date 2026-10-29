#!/usr/bin/env python3
"""Português C 식별자만 UCN으로 옮긴다. cadeia_VALOR·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

token_VALOR = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<identificador_VALOR>[^\W\d]\w*)', re.S | re.M)

def CONVERTER_VALOR(códigoFonte):
    def MUDAR_VALOR(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(caractere_VALOR if ord(caractere_VALOR) < 128 else
                       ('\\u%04x' if ord(caractere_VALOR) <= 65535 else '\\U%08x') % ord(caractere_VALOR)
                       for caractere_VALOR in 일치[0])
    return token_VALOR.sub(MUDAR_VALOR, códigoFonte)

def Executar_comando():
    analisador_48ee4b1b = argparse.ArgumentParser()
    analisador_48ee4b1b.add_argument('원본', type=Path)
    analisador_48ee4b1b.add_argument('saídaTexto', type=Path)
    argumentos = analisador_48ee4b1b.parse_args()
    for ficheiro in sorted(argumentos.원본.rglob('*')):
        if ficheiro.suffix not in ('.c', '.h'):
            continue
        saídaTexto = argumentos.saídaTexto / ficheiro.relative_to(argumentos.원본)
        saídaTexto.parent.mkdir(parents=True, exist_ok=True)
        새원문 = CONVERTER_VALOR(ficheiro.read_text())
        if not saídaTexto.exists() or saídaTexto.read_text() != 새원문:
            saídaTexto.write_text(새원문)

if __name__ == '__main__':
    Executar_comando()

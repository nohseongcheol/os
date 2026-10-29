#!/usr/bin/env python3
"""español C 식별자만 UCN으로 옮긴다. Cadena·Caracteres·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

valorTokenLéxico = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<valorIdentificador>[^\W\d]\w*)', re.S | re.M)

def convertirValor(fuente):
    def reemplazarValor(esIgual):
        if esIgual.lastgroup == '보존':
            return esIgual[0]
        return ''.join(valorCarácter if ord(valorCarácter) < 128 else
                       ('\\u%04x' if ord(valorCarácter) <= 65535 else '\\U%08x') % ord(valorCarácter)
                       for valorCarácter in esIgual[0])
    return valorTokenLéxico.sub(reemplazarValor, fuente)

def ejecutarComando():
    Analizador = argparse.ArgumentParser()
    Analizador.add_argument('original', type=Path)
    Analizador.add_argument('Salida', type=Path)
    argumentos = Analizador.parse_args()
    for Archivo in sorted(argumentos.original.rglob('*')):
        if Archivo.suffix not in ('.c', '.h'):
            continue
        Salida = argumentos.Salida / Archivo.relative_to(argumentos.original)
        Salida.parent.mkdir(parents=True, exist_ok=True)
        fuenteNuevo = convertirValor(Archivo.read_text())
        if not Salida.exists() or Salida.read_text() != fuenteNuevo:
            Salida.write_text(fuenteNuevo)

if __name__ == '__main__':
    ejecutarComando()

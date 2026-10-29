#!/usr/bin/env python3
"""명시한 Java fonte_árvore/aula_VALOR 파일을 arranque_da_máquina 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def BIND_empresa(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for entrada_VALOR_962f286b in 항목들:
        if '=' not in entrada_VALOR_962f286b:
            raise ValueError('expected NAME=PATH: ' + entrada_VALOR_962f286b)
        Nome, caminho = entrada_VALOR_962f286b.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Nome) or Nome in 명시:
            raise ValueError('invalid or duplicate file name: ' + Nome)
        명시.add(Nome)
        이름들.add(Nome)
        dados = Path(caminho).read_bytes()
        if len(dados) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Nome)
        파일들.append((Nome.encode('ascii'), dados))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    resultado = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    resultado.extend(bytes(72 * len(파일들)))
    for número, (Nome, dados) in enumerate(파일들):
        struct.pack_into('<64sII', resultado, 8 + número * 72, Nome, len(resultado), len(dados))
        resultado.extend(dados)
    return bytes(resultado)


if __name__ == '__main__':
    analisar_VALOR = argparse.ArgumentParser(description=__doc__)
    analisar_VALOR.add_argument('-o', required=True)
    analisar_VALOR.add_argument('files', nargs='*', help='NAME=PATH')
    argumentos = analisar_VALOR.parse_args()
    try:
        dados = BIND_empresa(argumentos.files)
        destino_VALOR = Path(argumentos.o)
        if not destino_VALOR.exists() or destino_VALOR.read_bytes() != dados:
            임시 = destino_VALOR.with_name(destino_VALOR.name + '.tmp')
            임시.write_bytes(dados)
            임시.replace(destino_VALOR)
    except (ValueError, OSError) as erro:
        analisar_VALOR.error(str(erro))

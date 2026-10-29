#!/usr/bin/env python3
"""명시한 Java fonte_árbore/Clase_VALOR 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def ligar_extremo(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for introdución_VALOR in 항목들:
        if '=' not in introdución_VALOR:
            raise ValueError('expected NAME=PATH: ' + introdución_VALOR)
        Nome, CAMIÑO = introdución_VALOR.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Nome) or Nome in 명시:
            raise ValueError('invalid or duplicate file name: ' + Nome)
        명시.add(Nome)
        이름들.add(Nome)
        datos = Path(CAMIÑO).read_bytes()
        if len(datos) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Nome)
        파일들.append((Nome.encode('ascii'), datos))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    RESULTANTE = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    RESULTANTE.extend(bytes(72 * len(파일들)))
    for 수, (Nome, datos) in enumerate(파일들):
        struct.pack_into('<64sII', RESULTANTE, 8 + 수 * 72, Nome, len(RESULTANTE), len(datos))
        RESULTANTE.extend(datos)
    return bytes(RESULTANTE)


if __name__ == '__main__':
    analizar_VALOR = argparse.ArgumentParser(description=__doc__)
    analizar_VALOR.add_argument('-o', required=True)
    analizar_VALOR.add_argument('files', nargs='*', help='NAME=PATH')
    Argumentos = analizar_VALOR.parse_args()
    try:
        datos = ligar_extremo(Argumentos.files)
        destino_VALOR = Path(Argumentos.o)
        if not destino_VALOR.exists() or destino_VALOR.read_bytes() != datos:
            임시 = destino_VALOR.with_name(destino_VALOR.name + '.tmp')
            임시.write_bytes(datos)
            임시.replace(destino_VALOR)
    except (ValueError, OSError) as ERRO:
        analizar_VALOR.error(str(ERRO))

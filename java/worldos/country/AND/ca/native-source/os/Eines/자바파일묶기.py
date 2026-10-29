#!/usr/bin/env python3
"""명시한 Java font_arbre/Classe_VALOR 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def enllaçar_extrem(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for introducció_VALOR in 항목들:
        if '=' not in introducció_VALOR:
            raise ValueError('expected NAME=PATH: ' + introducció_VALOR)
        Nom, Camí = introducció_VALOR.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Nom) or Nom in 명시:
            raise ValueError('invalid or duplicate file name: ' + Nom)
        명시.add(Nom)
        이름들.add(Nom)
        dades = Path(Camí).read_bytes()
        if len(dades) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Nom)
        파일들.append((Nom.encode('ascii'), dades))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    RESULTAT = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    RESULTAT.extend(bytes(72 * len(파일들)))
    for 수, (Nom, dades) in enumerate(파일들):
        struct.pack_into('<64sII', RESULTAT, 8 + 수 * 72, Nom, len(RESULTAT), len(dades))
        RESULTAT.extend(dades)
    return bytes(RESULTAT)


if __name__ == '__main__':
    analitzar_VALOR = argparse.ArgumentParser(description=__doc__)
    analitzar_VALOR.add_argument('-o', required=True)
    analitzar_VALOR.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = analitzar_VALOR.parse_args()
    try:
        dades = enllaçar_extrem(인수.files)
        destinació_VALOR = Path(인수.o)
        if not destinació_VALOR.exists() or destinació_VALOR.read_bytes() != dades:
            임시 = destinació_VALOR.with_name(destinació_VALOR.name + '.tmp')
            임시.write_bytes(dades)
            임시.replace(destinació_VALOR)
    except (ValueError, OSError) as s_ha_produït_un_error:
        analitzar_VALOR.error(str(s_ha_produït_un_error))

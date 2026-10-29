#!/usr/bin/env python3
"""명시한 Java zdroj_strom/Třída_HODNOTA 파일을 spuštění_stroje 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def vázat_účastník(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for položka_HODNOTA in 항목들:
        if '=' not in položka_HODNOTA:
            raise ValueError('expected NAME=PATH: ' + položka_HODNOTA)
        Název, cesta_2 = položka_HODNOTA.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Název) or Název in 명시:
            raise ValueError('invalid or duplicate file name: ' + Název)
        명시.add(Název)
        이름들.add(Název)
        data = Path(cesta_2).read_bytes()
        if len(data) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Název)
        파일들.append((Název.encode('ascii'), data))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    VÝSLEDEK = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    VÝSLEDEK.extend(bytes(72 * len(파일들)))
    for číslo, (Název, data) in enumerate(파일들):
        struct.pack_into('<64sII', VÝSLEDEK, 8 + číslo * 72, Název, len(VÝSLEDEK), len(data))
        VÝSLEDEK.extend(data)
    return bytes(VÝSLEDEK)


if __name__ == '__main__':
    parsovat_HODNOTA = argparse.ArgumentParser(description=__doc__)
    parsovat_HODNOTA.add_argument('-o', required=True)
    parsovat_HODNOTA.add_argument('files', nargs='*', help='NAME=PATH')
    argumenty = parsovat_HODNOTA.parse_args()
    try:
        data = vázat_účastník(argumenty.files)
        cíl_HODNOTA = Path(argumenty.o)
        if not cíl_HODNOTA.exists() or cíl_HODNOTA.read_bytes() != data:
            임시 = cíl_HODNOTA.with_name(cíl_HODNOTA.name + '.tmp')
            임시.write_bytes(data)
            임시.replace(cíl_HODNOTA)
    except (ValueError, OSError) as chyba:
        parsovat_HODNOTA.error(str(chyba))

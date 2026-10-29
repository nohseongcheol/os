#!/usr/bin/env python3
"""명시한 Java vir_drevo/Razred_VALUE 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def BIND_končna_točka(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for vnos_VALUE in 항목들:
        if '=' not in vnos_VALUE:
            raise ValueError('expected NAME=PATH: ' + vnos_VALUE)
        Ime, POT = vnos_VALUE.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Ime) or Ime in 명시:
            raise ValueError('invalid or duplicate file name: ' + Ime)
        명시.add(Ime)
        이름들.add(Ime)
        podatki = Path(POT).read_bytes()
        if len(podatki) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Ime)
        파일들.append((Ime.encode('ascii'), podatki))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    REZULTAT = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    REZULTAT.extend(bytes(72 * len(파일들)))
    for 수, (Ime, podatki) in enumerate(파일들):
        struct.pack_into('<64sII', REZULTAT, 8 + 수 * 72, Ime, len(REZULTAT), len(podatki))
        REZULTAT.extend(podatki)
    return bytes(REZULTAT)


if __name__ == '__main__':
    razčlenjevati_VALUE = argparse.ArgumentParser(description=__doc__)
    razčlenjevati_VALUE.add_argument('-o', required=True)
    razčlenjevati_VALUE.add_argument('files', nargs='*', help='NAME=PATH')
    Argumenti = razčlenjevati_VALUE.parse_args()
    try:
        podatki = BIND_končna_točka(Argumenti.files)
        cilj_VALUE = Path(Argumenti.o)
        if not cilj_VALUE.exists() or cilj_VALUE.read_bytes() != podatki:
            임시 = cilj_VALUE.with_name(cilj_VALUE.name + '.tmp')
            임시.write_bytes(podatki)
            임시.replace(cilj_VALUE)
    except (ValueError, OSError) as NAPAKA:
        razčlenjevati_VALUE.error(str(NAPAKA))

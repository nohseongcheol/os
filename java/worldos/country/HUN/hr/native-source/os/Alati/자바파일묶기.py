#!/usr/bin/env python3
"""명시한 Java izvor_stablo/poduka_VALUE 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def BIND_sudionik(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for unos_VALUE in 항목들:
        if '=' not in unos_VALUE:
            raise ValueError('expected NAME=PATH: ' + unos_VALUE)
        Ime, PUTANJA = unos_VALUE.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Ime) or Ime in 명시:
            raise ValueError('invalid or duplicate file name: ' + Ime)
        명시.add(Ime)
        이름들.add(Ime)
        podaci = Path(PUTANJA).read_bytes()
        if len(podaci) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Ime)
        파일들.append((Ime.encode('ascii'), podaci))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    REZULTAT = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    REZULTAT.extend(bytes(72 * len(파일들)))
    for 수, (Ime, podaci) in enumerate(파일들):
        struct.pack_into('<64sII', REZULTAT, 8 + 수 * 72, Ime, len(REZULTAT), len(podaci))
        REZULTAT.extend(podaci)
    return bytes(REZULTAT)


if __name__ == '__main__':
    rastavljati_VALUE = argparse.ArgumentParser(description=__doc__)
    rastavljati_VALUE.add_argument('-o', required=True)
    rastavljati_VALUE.add_argument('files', nargs='*', help='NAME=PATH')
    Argumenti = rastavljati_VALUE.parse_args()
    try:
        podaci = BIND_sudionik(Argumenti.files)
        odredište_VALUE = Path(Argumenti.o)
        if not odredište_VALUE.exists() or odredište_VALUE.read_bytes() != podaci:
            임시 = odredište_VALUE.with_name(odredište_VALUE.name + '.tmp')
            임시.write_bytes(podaci)
            임시.replace(odredište_VALUE)
    except (ValueError, OSError) as GREŠKA:
        rastavljati_VALUE.error(str(GREŠKA))

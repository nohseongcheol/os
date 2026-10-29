#!/usr/bin/env python3
"""명시한 Java izvor_stablo/klasa_VALUE 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def BIND_završna_tačka(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for unos_VALUE in 항목들:
        if '=' not in unos_VALUE:
            raise ValueError('expected NAME=PATH: ' + unos_VALUE)
        Naziv, Putanja = unos_VALUE.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Naziv) or Naziv in 명시:
            raise ValueError('invalid or duplicate file name: ' + Naziv)
        명시.add(Naziv)
        이름들.add(Naziv)
        podaci = Path(Putanja).read_bytes()
        if len(podaci) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Naziv)
        파일들.append((Naziv.encode('ascii'), podaci))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    mjera = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    mjera.extend(bytes(72 * len(파일들)))
    for 수, (Naziv, podaci) in enumerate(파일들):
        struct.pack_into('<64sII', mjera, 8 + 수 * 72, Naziv, len(mjera), len(podaci))
        mjera.extend(podaci)
    return bytes(mjera)


if __name__ == '__main__':
    raščlanjivati_VALUE = argparse.ArgumentParser(description=__doc__)
    raščlanjivati_VALUE.add_argument('-o', required=True)
    raščlanjivati_VALUE.add_argument('files', nargs='*', help='NAME=PATH')
    Argumenti = raščlanjivati_VALUE.parse_args()
    try:
        podaci = BIND_završna_tačka(Argumenti.files)
        odredište_VALUE = Path(Argumenti.o)
        if not odredište_VALUE.exists() or odredište_VALUE.read_bytes() != podaci:
            임시 = odredište_VALUE.with_name(odredište_VALUE.name + '.tmp')
            임시.write_bytes(podaci)
            임시.replace(odredište_VALUE)
    except (ValueError, OSError) as GRESKA:
        raščlanjivati_VALUE.error(str(GRESKA))

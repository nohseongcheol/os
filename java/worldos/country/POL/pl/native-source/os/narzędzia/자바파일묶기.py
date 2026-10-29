#!/usr/bin/env python3
"""명시한 Java źródło_drzewo/Klasa_WARTOŚĆ 파일을 rozruch_maszyny 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def BIND_uczestnik(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for wpis_WARTOŚĆ in 항목들:
        if '=' not in wpis_WARTOŚĆ:
            raise ValueError('expected NAME=PATH: ' + wpis_WARTOŚĆ)
        Nazwa, ścieżka_2 = wpis_WARTOŚĆ.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Nazwa) or Nazwa in 명시:
            raise ValueError('invalid or duplicate file name: ' + Nazwa)
        명시.add(Nazwa)
        이름들.add(Nazwa)
        dane = Path(ścieżka_2).read_bytes()
        if len(dane) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Nazwa)
        파일들.append((Nazwa.encode('ascii'), dane))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    WYNIK = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    WYNIK.extend(bytes(72 * len(파일들)))
    for identyfikator, (Nazwa, dane) in enumerate(파일들):
        struct.pack_into('<64sII', WYNIK, 8 + identyfikator * 72, Nazwa, len(WYNIK), len(dane))
        WYNIK.extend(dane)
    return bytes(WYNIK)


if __name__ == '__main__':
    analizować_WARTOŚĆ = argparse.ArgumentParser(description=__doc__)
    analizować_WARTOŚĆ.add_argument('-o', required=True)
    analizować_WARTOŚĆ.add_argument('files', nargs='*', help='NAME=PATH')
    argumenty = analizować_WARTOŚĆ.parse_args()
    try:
        dane = BIND_uczestnik(argumenty.files)
        cel_WARTOŚĆ = Path(argumenty.o)
        if not cel_WARTOŚĆ.exists() or cel_WARTOŚĆ.read_bytes() != dane:
            임시 = cel_WARTOŚĆ.with_name(cel_WARTOŚĆ.name + '.tmp')
            임시.write_bytes(dane)
            임시.replace(cel_WARTOŚĆ)
    except (ValueError, OSError) as błąd:
        analizować_WARTOŚĆ.error(str(błąd))

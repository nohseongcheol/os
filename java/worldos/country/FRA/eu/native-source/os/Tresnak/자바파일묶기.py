#!/usr/bin/env python3
"""명시한 Java iturburu_zuhaitz/Gela_balio 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def lotu_amaiera_puntu(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for sarrera_balio in 항목들:
        if '=' not in sarrera_balio:
            raise ValueError('expected NAME=PATH: ' + sarrera_balio)
        Izena, Bide_izena = sarrera_balio.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Izena) or Izena in 명시:
            raise ValueError('invalid or duplicate file name: ' + Izena)
        명시.add(Izena)
        이름들.add(Izena)
        datuak = Path(Bide_izena).read_bytes()
        if len(datuak) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Izena)
        파일들.append((Izena.encode('ascii'), datuak))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    EMAITZA = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    EMAITZA.extend(bytes(72 * len(파일들)))
    for 수, (Izena, datuak) in enumerate(파일들):
        struct.pack_into('<64sII', EMAITZA, 8 + 수 * 72, Izena, len(EMAITZA), len(datuak))
        EMAITZA.extend(datuak)
    return bytes(EMAITZA)


if __name__ == '__main__':
    analizatu_balio = argparse.ArgumentParser(description=__doc__)
    analizatu_balio.add_argument('-o', required=True)
    analizatu_balio.add_argument('files', nargs='*', help='NAME=PATH')
    Argumentuak = analizatu_balio.parse_args()
    try:
        datuak = lotu_amaiera_puntu(Argumentuak.files)
        helburu_balio_a0fbc067 = Path(Argumentuak.o)
        if not helburu_balio_a0fbc067.exists() or helburu_balio_a0fbc067.read_bytes() != datuak:
            임시 = helburu_balio_a0fbc067.with_name(helburu_balio_a0fbc067.name + '.tmp')
            임시.write_bytes(datuak)
            임시.replace(helburu_balio_a0fbc067)
    except (ValueError, OSError) as errorea:
        analizatu_balio.error(str(errorea))

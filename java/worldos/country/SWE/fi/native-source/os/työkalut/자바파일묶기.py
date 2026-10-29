#!/usr/bin/env python3
"""명시한 Java lähde_puu/Luokka_ARVO 파일을 koneen_käynnistys 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def BIND_päätepiste(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for merkintä_ARVO_962f286b in 항목들:
        if '=' not in merkintä_ARVO_962f286b:
            raise ValueError('expected NAME=PATH: ' + merkintä_ARVO_962f286b)
        Nimi, polku_2 = merkintä_ARVO_962f286b.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Nimi) or Nimi in 명시:
            raise ValueError('invalid or duplicate file name: ' + Nimi)
        명시.add(Nimi)
        이름들.add(Nimi)
        data = Path(polku_2).read_bytes()
        if len(data) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Nimi)
        파일들.append((Nimi.encode('ascii'), data))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    TULOS = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    TULOS.extend(bytes(72 * len(파일들)))
    for numero, (Nimi, data) in enumerate(파일들):
        struct.pack_into('<64sII', TULOS, 8 + numero * 72, Nimi, len(TULOS), len(data))
        TULOS.extend(data)
    return bytes(TULOS)


if __name__ == '__main__':
    jäsentää_ARVO = argparse.ArgumentParser(description=__doc__)
    jäsentää_ARVO.add_argument('-o', required=True)
    jäsentää_ARVO.add_argument('files', nargs='*', help='NAME=PATH')
    argumentit = jäsentää_ARVO.parse_args()
    try:
        data = BIND_päätepiste(argumentit.files)
        kohde_ARVO = Path(argumentit.o)
        if not kohde_ARVO.exists() or kohde_ARVO.read_bytes() != data:
            임시 = kohde_ARVO.with_name(kohde_ARVO.name + '.tmp')
            임시.write_bytes(data)
            임시.replace(kohde_ARVO)
    except (ValueError, OSError) as VIRHE:
        jäsentää_ARVO.error(str(VIRHE))

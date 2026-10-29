#!/usr/bin/env python3
"""명시한 Java zdroj_strom/lekcia_VALUE 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def BIND_účastník(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for položka_VALUE in 항목들:
        if '=' not in položka_VALUE:
            raise ValueError('expected NAME=PATH: ' + položka_VALUE)
        Názov, Cesta = položka_VALUE.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Názov) or Názov in 명시:
            raise ValueError('invalid or duplicate file name: ' + Názov)
        명시.add(Názov)
        이름들.add(Názov)
        údaje = Path(Cesta).read_bytes()
        if len(údaje) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Názov)
        파일들.append((Názov.encode('ascii'), údaje))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    KR = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    KR.extend(bytes(72 * len(파일들)))
    for 수, (Názov, údaje) in enumerate(파일들):
        struct.pack_into('<64sII', KR, 8 + 수 * 72, Názov, len(KR), len(údaje))
        KR.extend(údaje)
    return bytes(KR)


if __name__ == '__main__':
    analyzovať_VALUE = argparse.ArgumentParser(description=__doc__)
    analyzovať_VALUE.add_argument('-o', required=True)
    analyzovať_VALUE.add_argument('files', nargs='*', help='NAME=PATH')
    Argumenty = analyzovať_VALUE.parse_args()
    try:
        údaje = BIND_účastník(Argumenty.files)
        cieľ_VALUE = Path(Argumenty.o)
        if not cieľ_VALUE.exists() or cieľ_VALUE.read_bytes() != údaje:
            임시 = cieľ_VALUE.with_name(cieľ_VALUE.name + '.tmp')
            임시.write_bytes(údaje)
            임시.replace(cieľ_VALUE)
    except (ValueError, OSError) as chyba:
        analyzovať_VALUE.error(str(chyba))

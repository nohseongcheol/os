#!/usr/bin/env python3
"""명시한 Java forrás_fa/tanóra_ÉRTÉK 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def BIND_végpont(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for bejegyzés_ÉRTÉK in 항목들:
        if '=' not in bejegyzés_ÉRTÉK:
            raise ValueError('expected NAME=PATH: ' + bejegyzés_ÉRTÉK)
        Név, ÚTVONAL = bejegyzés_ÉRTÉK.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Név) or Név in 명시:
            raise ValueError('invalid or duplicate file name: ' + Név)
        명시.add(Név)
        이름들.add(Név)
        adat = Path(ÚTVONAL).read_bytes()
        if len(adat) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Név)
        파일들.append((Név.encode('ascii'), adat))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    KR = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    KR.extend(bytes(72 * len(파일들)))
    for szám, (Név, adat) in enumerate(파일들):
        struct.pack_into('<64sII', KR, 8 + szám * 72, Név, len(KR), len(adat))
        KR.extend(adat)
    return bytes(KR)


if __name__ == '__main__':
    elemez_ÉRTÉK = argparse.ArgumentParser(description=__doc__)
    elemez_ÉRTÉK.add_argument('-o', required=True)
    elemez_ÉRTÉK.add_argument('files', nargs='*', help='NAME=PATH')
    Argumentumok = elemez_ÉRTÉK.parse_args()
    try:
        adat = BIND_végpont(Argumentumok.files)
        cél_ÉRTÉK = Path(Argumentumok.o)
        if not cél_ÉRTÉK.exists() or cél_ÉRTÉK.read_bytes() != adat:
            임시 = cél_ÉRTÉK.with_name(cél_ÉRTÉK.name + '.tmp')
            임시.write_bytes(adat)
            임시.replace(cél_ÉRTÉK)
    except (ValueError, OSError) as HIBA:
        elemez_ÉRTÉK.error(str(HIBA))

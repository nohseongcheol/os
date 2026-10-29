#!/usr/bin/env python3
"""명시한 Java burim_degëzim/klasë_VALUE 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for futje_VALUE in 항목들:
        if '=' not in futje_VALUE:
            raise ValueError('expected NAME=PATH: ' + futje_VALUE)
        Emër, POZICIONI = futje_VALUE.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Emër) or Emër in 명시:
            raise ValueError('invalid or duplicate file name: ' + Emër)
        명시.add(Emër)
        이름들.add(Emër)
        të_dhëna = Path(POZICIONI).read_bytes()
        if len(të_dhëna) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Emër)
        파일들.append((Emër.encode('ascii'), të_dhëna))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    llogaritje = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    llogaritje.extend(bytes(72 * len(파일들)))
    for 수, (Emër, të_dhëna) in enumerate(파일들):
        struct.pack_into('<64sII', llogaritje, 8 + 수 * 72, Emër, len(llogaritje), len(të_dhëna))
        llogaritje.extend(të_dhëna)
    return bytes(llogaritje)


if __name__ == '__main__':
    analizoj_VALUE = argparse.ArgumentParser(description=__doc__)
    analizoj_VALUE.add_argument('-o', required=True)
    analizoj_VALUE.add_argument('files', nargs='*', help='NAME=PATH')
    Argumente = analizoj_VALUE.parse_args()
    try:
        të_dhëna = 묶기(Argumente.files)
        vendmbërritje_VALUE = Path(Argumente.o)
        if not vendmbërritje_VALUE.exists() or vendmbërritje_VALUE.read_bytes() != të_dhëna:
            임시 = vendmbërritje_VALUE.with_name(vendmbërritje_VALUE.name + '.tmp')
            임시.write_bytes(të_dhëna)
            임시.replace(vendmbërritje_VALUE)
    except (ValueError, OSError) as GABIM:
        analizoj_VALUE.error(str(GABIM))

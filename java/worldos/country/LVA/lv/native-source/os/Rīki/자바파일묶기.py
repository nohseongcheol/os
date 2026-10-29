#!/usr/bin/env python3
"""명시한 Java avots_koks/klase_VALUE 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def BIND_dalībnieks(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for ievade_VALUE in 항목들:
        if '=' not in ievade_VALUE:
            raise ValueError('expected NAME=PATH: ' + ievade_VALUE)
        Nosaukums, CEĻŠ = ievade_VALUE.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Nosaukums) or Nosaukums in 명시:
            raise ValueError('invalid or duplicate file name: ' + Nosaukums)
        명시.add(Nosaukums)
        이름들.add(Nosaukums)
        dati = Path(CEĻŠ).read_bytes()
        if len(dati) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Nosaukums)
        파일들.append((Nosaukums.encode('ascii'), dati))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    mērs = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    mērs.extend(bytes(72 * len(파일들)))
    for numurs, (Nosaukums, dati) in enumerate(파일들):
        struct.pack_into('<64sII', mērs, 8 + numurs * 72, Nosaukums, len(mērs), len(dati))
        mērs.extend(dati)
    return bytes(mērs)


if __name__ == '__main__':
    parsēt_VALUE = argparse.ArgumentParser(description=__doc__)
    parsēt_VALUE.add_argument('-o', required=True)
    parsēt_VALUE.add_argument('files', nargs='*', help='NAME=PATH')
    Parametri = parsēt_VALUE.parse_args()
    try:
        dati = BIND_dalībnieks(Parametri.files)
        mērķis_VALUE = Path(Parametri.o)
        if not mērķis_VALUE.exists() or mērķis_VALUE.read_bytes() != dati:
            임시 = mērķis_VALUE.with_name(mērķis_VALUE.name + '.tmp')
            임시.write_bytes(dati)
            임시.replace(mērķis_VALUE)
    except (ValueError, OSError) as Kļūda:
        parsēt_VALUE.error(str(Kļūda))

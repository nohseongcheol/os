#!/usr/bin/env python3
"""명시한 Java sursă_arborescență/Clasă_VALUE 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def BIND_participant(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for intrare_VALUE in 항목들:
        if '=' not in intrare_VALUE:
            raise ValueError('expected NAME=PATH: ' + intrare_VALUE)
        Nume, Cale = intrare_VALUE.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Nume) or Nume in 명시:
            raise ValueError('invalid or duplicate file name: ' + Nume)
        명시.add(Nume)
        이름들.add(Nume)
        date = Path(Cale).read_bytes()
        if len(date) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Nume)
        파일들.append((Nume.encode('ascii'), date))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    KR = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    KR.extend(bytes(72 * len(파일들)))
    for 수, (Nume, date) in enumerate(파일들):
        struct.pack_into('<64sII', KR, 8 + 수 * 72, Nume, len(KR), len(date))
        KR.extend(date)
    return bytes(KR)


if __name__ == '__main__':
    analiza_VALUE = argparse.ArgumentParser(description=__doc__)
    analiza_VALUE.add_argument('-o', required=True)
    analiza_VALUE.add_argument('files', nargs='*', help='NAME=PATH')
    Argumente = analiza_VALUE.parse_args()
    try:
        date = BIND_participant(Argumente.files)
        destinație_VALUE = Path(Argumente.o)
        if not destinație_VALUE.exists() or destinație_VALUE.read_bytes() != date:
            임시 = destinație_VALUE.with_name(destinație_VALUE.name + '.tmp')
            임시.write_bytes(date)
            임시.replace(destinație_VALUE)
    except (ValueError, OSError) as eroare:
        analiza_VALUE.error(str(eroare))

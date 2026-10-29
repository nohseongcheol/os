#!/usr/bin/env python3
"""명시한 Java foinse_crann/aicme_VALUE 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for iontráil_VALUE in 항목들:
        if '=' not in iontráil_VALUE:
            raise ValueError('expected NAME=PATH: ' + iontráil_VALUE)
        Ainm, CONAIR = iontráil_VALUE.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Ainm) or Ainm in 명시:
            raise ValueError('invalid or duplicate file name: ' + Ainm)
        명시.add(Ainm)
        이름들.add(Ainm)
        sonraí = Path(CONAIR).read_bytes()
        if len(sonraí) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Ainm)
        파일들.append((Ainm.encode('ascii'), sonraí))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    tomhas = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    tomhas.extend(bytes(72 * len(파일들)))
    for 수, (Ainm, sonraí) in enumerate(파일들):
        struct.pack_into('<64sII', tomhas, 8 + 수 * 72, Ainm, len(tomhas), len(sonraí))
        tomhas.extend(sonraí)
    return bytes(tomhas)


if __name__ == '__main__':
    parsáil_VALUE = argparse.ArgumentParser(description=__doc__)
    parsáil_VALUE.add_argument('-o', required=True)
    parsáil_VALUE.add_argument('files', nargs='*', help='NAME=PATH')
    Argóintí = parsáil_VALUE.parse_args()
    try:
        sonraí = 묶기(Argóintí.files)
        sprioc_VALUE = Path(Argóintí.o)
        if not sprioc_VALUE.exists() or sprioc_VALUE.read_bytes() != sonraí:
            임시 = sprioc_VALUE.with_name(sprioc_VALUE.name + '.tmp')
            임시.write_bytes(sonraí)
            임시.replace(sprioc_VALUE)
    except (ValueError, OSError) as ERREÁID:
        parsáil_VALUE.error(str(ERREÁID))

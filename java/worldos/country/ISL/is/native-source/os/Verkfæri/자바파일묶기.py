#!/usr/bin/env python3
"""명시한 Java uppruni_tré/klasi_VALUE 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def BIND_endastöð(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for færsla_VALUE in 항목들:
        if '=' not in færsla_VALUE:
            raise ValueError('expected NAME=PATH: ' + færsla_VALUE)
        Heiti, SLÓÐ = færsla_VALUE.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Heiti) or Heiti in 명시:
            raise ValueError('invalid or duplicate file name: ' + Heiti)
        명시.add(Heiti)
        이름들.add(Heiti)
        gögn = Path(SLÓÐ).read_bytes()
        if len(gögn) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Heiti)
        파일들.append((Heiti.encode('ascii'), gögn))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    NIÐURSTAÐA = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    NIÐURSTAÐA.extend(bytes(72 * len(파일들)))
    for númer, (Heiti, gögn) in enumerate(파일들):
        struct.pack_into('<64sII', NIÐURSTAÐA, 8 + númer * 72, Heiti, len(NIÐURSTAÐA), len(gögn))
        NIÐURSTAÐA.extend(gögn)
    return bytes(NIÐURSTAÐA)


if __name__ == '__main__':
    þátta_VALUE = argparse.ArgumentParser(description=__doc__)
    þátta_VALUE.add_argument('-o', required=True)
    þátta_VALUE.add_argument('files', nargs='*', help='NAME=PATH')
    Viðföng = þátta_VALUE.parse_args()
    try:
        gögn = BIND_endastöð(Viðföng.files)
        endastaður_VALUE = Path(Viðföng.o)
        if not endastaður_VALUE.exists() or endastaður_VALUE.read_bytes() != gögn:
            임시 = endastaður_VALUE.with_name(endastaður_VALUE.name + '.tmp')
            임시.write_bytes(gögn)
            임시.replace(endastaður_VALUE)
    except (ValueError, OSError) as Villa:
        þátta_VALUE.error(str(Villa))

#!/usr/bin/env python3
"""명시한 Java lähe_puu/tund_VALUE 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def BIND_osaleja(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for kirje_VALUE in 항목들:
        if '=' not in kirje_VALUE:
            raise ValueError('expected NAME=PATH: ' + kirje_VALUE)
        Nimi_2, RADA = kirje_VALUE.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Nimi_2) or Nimi_2 in 명시:
            raise ValueError('invalid or duplicate file name: ' + Nimi_2)
        명시.add(Nimi_2)
        이름들.add(Nimi_2)
        andmed = Path(RADA).read_bytes()
        if len(andmed) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Nimi_2)
        파일들.append((Nimi_2.encode('ascii'), andmed))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    TULEMUS = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    TULEMUS.extend(bytes(72 * len(파일들)))
    for number, (Nimi_2, andmed) in enumerate(파일들):
        struct.pack_into('<64sII', TULEMUS, 8 + number * 72, Nimi_2, len(TULEMUS), len(andmed))
        TULEMUS.extend(andmed)
    return bytes(TULEMUS)


if __name__ == '__main__':
    sõeluma_VALUE = argparse.ArgumentParser(description=__doc__)
    sõeluma_VALUE.add_argument('-o', required=True)
    sõeluma_VALUE.add_argument('files', nargs='*', help='NAME=PATH')
    Argumendid = sõeluma_VALUE.parse_args()
    try:
        andmed = BIND_osaleja(Argumendid.files)
        sihtkoht_VALUE = Path(Argumendid.o)
        if not sihtkoht_VALUE.exists() or sihtkoht_VALUE.read_bytes() != andmed:
            임시 = sihtkoht_VALUE.with_name(sihtkoht_VALUE.name + '.tmp')
            임시.write_bytes(andmed)
            임시.replace(sihtkoht_VALUE)
    except (ValueError, OSError) as VIGA:
        sõeluma_VALUE.error(str(VIGA))

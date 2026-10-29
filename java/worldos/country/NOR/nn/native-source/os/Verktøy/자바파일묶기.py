#!/usr/bin/env python3
"""명시한 Java kjelde_tre/time_VALUE 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def BIND_endepunkt(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for oppføring_VALUE in 항목들:
        if '=' not in oppføring_VALUE:
            raise ValueError('expected NAME=PATH: ' + oppføring_VALUE)
        Namn, STIGE = oppføring_VALUE.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Namn) or Namn in 명시:
            raise ValueError('invalid or duplicate file name: ' + Namn)
        명시.add(Namn)
        이름들.add(Namn)
        data = Path(STIGE).read_bytes()
        if len(data) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Namn)
        파일들.append((Namn.encode('ascii'), data))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    forretningsmål = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    forretningsmål.extend(bytes(72 * len(파일들)))
    for 수, (Namn, data) in enumerate(파일들):
        struct.pack_into('<64sII', forretningsmål, 8 + 수 * 72, Namn, len(forretningsmål), len(data))
        forretningsmål.extend(data)
    return bytes(forretningsmål)


if __name__ == '__main__':
    dele_opp_VALUE = argparse.ArgumentParser(description=__doc__)
    dele_opp_VALUE.add_argument('-o', required=True)
    dele_opp_VALUE.add_argument('files', nargs='*', help='NAME=PATH')
    Argument = dele_opp_VALUE.parse_args()
    try:
        data = BIND_endepunkt(Argument.files)
        mål_VALUE = Path(Argument.o)
        if not mål_VALUE.exists() or mål_VALUE.read_bytes() != data:
            임시 = mål_VALUE.with_name(mål_VALUE.name + '.tmp')
            임시.write_bytes(data)
            임시.replace(mål_VALUE)
    except (ValueError, OSError) as FEIL:
        dele_opp_VALUE.error(str(FEIL))

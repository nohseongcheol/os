#!/usr/bin/env python3
"""명시한 Java kilde_tre/time_VERDI 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def BIND_deltaker(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for oppføring_VERDI in 항목들:
        if '=' not in oppføring_VERDI:
            raise ValueError('expected NAME=PATH: ' + oppføring_VERDI)
        Navn, Sti = oppføring_VERDI.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Navn) or Navn in 명시:
            raise ValueError('invalid or duplicate file name: ' + Navn)
        명시.add(Navn)
        이름들.add(Navn)
        data = Path(Sti).read_bytes()
        if len(data) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Navn)
        파일들.append((Navn.encode('ascii'), data))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    KR = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    KR.extend(bytes(72 * len(파일들)))
    for nummer, (Navn, data) in enumerate(파일들):
        struct.pack_into('<64sII', KR, 8 + nummer * 72, Navn, len(KR), len(data))
        KR.extend(data)
    return bytes(KR)


if __name__ == '__main__':
    dele_opp_VERDI = argparse.ArgumentParser(description=__doc__)
    dele_opp_VERDI.add_argument('-o', required=True)
    dele_opp_VERDI.add_argument('files', nargs='*', help='NAME=PATH')
    Argumenter = dele_opp_VERDI.parse_args()
    try:
        data = BIND_deltaker(Argumenter.files)
        mål_VERDI = Path(Argumenter.o)
        if not mål_VERDI.exists() or mål_VERDI.read_bytes() != data:
            임시 = mål_VERDI.with_name(mål_VERDI.name + '.tmp')
            임시.write_bytes(data)
            임시.replace(mål_VERDI)
    except (ValueError, OSError) as feil:
        dele_opp_VERDI.error(str(feil))

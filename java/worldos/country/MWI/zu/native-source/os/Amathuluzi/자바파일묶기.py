#!/usr/bin/env python3
"""명시한 Java umthombo_isihlahla/uhlobo_inani 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for okufakwayo_inani in 항목들:
        if '=' not in okufakwayo_inani:
            raise ValueError('expected NAME=PATH: ' + okufakwayo_inani)
        Igama, Indlela_2 = okufakwayo_inani.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Igama) or Igama in 명시:
            raise ValueError('invalid or duplicate file name: ' + Igama)
        명시.add(Igama)
        이름들.add(Igama)
        imininingwane = Path(Indlela_2).read_bytes()
        if len(imininingwane) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Igama)
        파일들.append((Igama.encode('ascii'), imininingwane))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    결과 = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    결과.extend(bytes(72 * len(파일들)))
    for 수, (Igama, imininingwane) in enumerate(파일들):
        struct.pack_into('<64sII', 결과, 8 + 수 * 72, Igama, len(결과), len(imininingwane))
        결과.extend(imininingwane)
    return bytes(결과)


if __name__ == '__main__':
    zawula_inani = argparse.ArgumentParser(description=__doc__)
    zawula_inani.add_argument('-o', required=True)
    zawula_inani.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = zawula_inani.parse_args()
    try:
        imininingwane = 묶기(인수.files)
        isikhumulo_inani = Path(인수.o)
        if not isikhumulo_inani.exists() or isikhumulo_inani.read_bytes() != imininingwane:
            임시 = isikhumulo_inani.with_name(isikhumulo_inani.name + '.tmp')
            임시.write_bytes(imininingwane)
            임시.replace(isikhumulo_inani)
    except (ValueError, OSError) as Iphutha:
        zawula_inani.error(str(Iphutha))

#!/usr/bin/env python3
"""명시한 Java ebensìbịa_èsèrèsè_osisi/klaàsị_valuu 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for ndebà_valuu in 항목들:
        if '=' not in ndebà_valuu:
            raise ValueError('expected NAME=PATH: ' + ndebà_valuu)
        Aha, ụzọ_ozi = ndebà_valuu.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Aha) or Aha in 명시:
            raise ValueError('invalid or duplicate file name: ' + Aha)
        명시.add(Aha)
        이름들.add(Aha)
        datà = Path(ụzọ_ozi).read_bytes()
        if len(datà) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Aha)
        파일들.append((Aha.encode('ascii'), datà))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    결과 = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    결과.extend(bytes(72 * len(파일들)))
    for 수, (Aha, datà) in enumerate(파일들):
        struct.pack_into('<64sII', 결과, 8 + 수 * 72, Aha, len(결과), len(datà))
        결과.extend(datà)
    return bytes(결과)


if __name__ == '__main__':
    kerìsịa_valuu = argparse.ArgumentParser(description=__doc__)
    kerìsịa_valuu.add_argument('-o', required=True)
    kerìsịa_valuu.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = kerìsịa_valuu.parse_args()
    try:
        datà = 묶기(인수.files)
        ebemwèga_valuu = Path(인수.o)
        if not ebemwèga_valuu.exists() or ebemwèga_valuu.read_bytes() != datà:
            임시 = ebemwèga_valuu.with_name(ebemwèga_valuu.name + '.tmp')
            임시.write_bytes(datà)
            임시.replace(ebemwèga_valuu)
    except (ValueError, OSError) as mmejọ:
        kerìsịa_valuu.error(str(mmejọ))

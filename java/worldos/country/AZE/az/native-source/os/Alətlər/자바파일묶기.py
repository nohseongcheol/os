#!/usr/bin/env python3
"""명시한 Java mənbə_ağac/Sinif_VALUE 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for daxiletmə_VALUE in 항목들:
        if '=' not in daxiletmə_VALUE:
            raise ValueError('expected NAME=PATH: ' + daxiletmə_VALUE)
        Ad, Cığır = daxiletmə_VALUE.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Ad) or Ad in 명시:
            raise ValueError('invalid or duplicate file name: ' + Ad)
        명시.add(Ad)
        이름들.add(Ad)
        verilənlər = Path(Cığır).read_bytes()
        if len(verilənlər) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Ad)
        파일들.append((Ad.encode('ascii'), verilənlər))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    ölçü = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    ölçü.extend(bytes(72 * len(파일들)))
    for 수, (Ad, verilənlər) in enumerate(파일들):
        struct.pack_into('<64sII', ölçü, 8 + 수 * 72, Ad, len(ölçü), len(verilənlər))
        ölçü.extend(verilənlər)
    return bytes(ölçü)


if __name__ == '__main__':
    parselləmək_VALUE = argparse.ArgumentParser(description=__doc__)
    parselləmək_VALUE.add_argument('-o', required=True)
    parselləmək_VALUE.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = parselləmək_VALUE.parse_args()
    try:
        verilənlər = 묶기(인수.files)
        təyinat_VALUE_a0fbc067 = Path(인수.o)
        if not təyinat_VALUE_a0fbc067.exists() or təyinat_VALUE_a0fbc067.read_bytes() != verilənlər:
            임시 = təyinat_VALUE_a0fbc067.with_name(təyinat_VALUE_a0fbc067.name + '.tmp')
            임시.write_bytes(verilənlər)
            임시.replace(təyinat_VALUE_a0fbc067)
    except (ValueError, OSError) as XƏTA:
        parselləmək_VALUE.error(str(XƏTA))

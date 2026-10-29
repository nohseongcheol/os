#!/usr/bin/env python3
"""명시한 Java gor_agaç/klas_baha 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for girizmeklik_baha in 항목들:
        if '=' not in girizmeklik_baha:
            raise ValueError('expected NAME=PATH: ' + girizmeklik_baha)
        Ad, Ýol = girizmeklik_baha.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Ad) or Ad in 명시:
            raise ValueError('invalid or duplicate file name: ' + Ad)
        명시.add(Ad)
        이름들.add(Ad)
        maglumat = Path(Ýol).read_bytes()
        if len(maglumat) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Ad)
        파일들.append((Ad.encode('ascii'), maglumat))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    결과 = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    결과.extend(bytes(72 * len(파일들)))
    for 수, (Ad, maglumat) in enumerate(파일들):
        struct.pack_into('<64sII', 결과, 8 + 수 * 72, Ad, len(결과), len(maglumat))
        결과.extend(maglumat)
    return bytes(결과)


if __name__ == '__main__':
    seljer_baha = argparse.ArgumentParser(description=__doc__)
    seljer_baha.add_argument('-o', required=True)
    seljer_baha.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = seljer_baha.parse_args()
    try:
        maglumat = 묶기(인수.files)
        barylmaly_ýer_baha = Path(인수.o)
        if not barylmaly_ýer_baha.exists() or barylmaly_ýer_baha.read_bytes() != maglumat:
            임시 = barylmaly_ýer_baha.with_name(barylmaly_ýer_baha.name + '.tmp')
            임시.write_bytes(maglumat)
            임시.replace(barylmaly_ýer_baha)
    except (ValueError, OSError) as Hata:
        seljer_baha.error(str(Hata))

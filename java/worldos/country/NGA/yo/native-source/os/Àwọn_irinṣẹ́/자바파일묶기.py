#!/usr/bin/env python3
"""명시한 Java orísun_ètò_afigijúwe/ọ̀wọ́_iye 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for ìgbéwọlé_iye in 항목들:
        if '=' not in ìgbéwọlé_iye:
            raise ValueError('expected NAME=PATH: ' + ìgbéwọlé_iye)
        Orúkọ, ọ̀nà = ìgbéwọlé_iye.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Orúkọ) or Orúkọ in 명시:
            raise ValueError('invalid or duplicate file name: ' + Orúkọ)
        명시.add(Orúkọ)
        이름들.add(Orúkọ)
        détà = Path(ọ̀nà).read_bytes()
        if len(détà) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Orúkọ)
        파일들.append((Orúkọ.encode('ascii'), détà))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    결과 = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    결과.extend(bytes(72 * len(파일들)))
    for 수, (Orúkọ, détà) in enumerate(파일들):
        struct.pack_into('<64sII', 결과, 8 + 수 * 72, Orúkọ, len(결과), len(détà))
        결과.extend(détà)
    return bytes(결과)


if __name__ == '__main__':
    ìpínsíwẹ́wẹ́_iye = argparse.ArgumentParser(description=__doc__)
    ìpínsíwẹ́wẹ́_iye.add_argument('-o', required=True)
    ìpínsíwẹ́wẹ́_iye.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = ìpínsíwẹ́wẹ́_iye.parse_args()
    try:
        détà = 묶기(인수.files)
        èbúté_iye = Path(인수.o)
        if not èbúté_iye.exists() or èbúté_iye.read_bytes() != détà:
            임시 = èbúté_iye.with_name(èbúté_iye.name + '.tmp')
            임시.write_bytes(détà)
            임시.replace(èbúté_iye)
    except (ValueError, OSError) as àṣìṣe:
        ìpínsíwẹ́wẹ́_iye.error(str(àṣìṣe))

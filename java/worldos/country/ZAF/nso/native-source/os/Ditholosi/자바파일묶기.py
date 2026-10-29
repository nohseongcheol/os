#!/usr/bin/env python3
"""명시한 Java mohlodi_mohlare/legoro_boleng_55654bf1 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for go_tsenya_tshedimošo_boleng in 항목들:
        if '=' not in go_tsenya_tshedimošo_boleng:
            raise ValueError('expected NAME=PATH: ' + go_tsenya_tshedimošo_boleng)
        Leina, Tsejana = go_tsenya_tshedimošo_boleng.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Leina) or Leina in 명시:
            raise ValueError('invalid or duplicate file name: ' + Leina)
        명시.add(Leina)
        이름들.add(Leina)
        data = Path(Tsejana).read_bytes()
        if len(data) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Leina)
        파일들.append((Leina.encode('ascii'), data))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    결과 = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    결과.extend(bytes(72 * len(파일들)))
    for 수, (Leina, data) in enumerate(파일들):
        struct.pack_into('<64sII', 결과, 8 + 수 * 72, Leina, len(결과), len(data))
        결과.extend(data)
    return bytes(결과)


if __name__ == '__main__':
    ripaganya_boleng = argparse.ArgumentParser(description=__doc__)
    ripaganya_boleng.add_argument('-o', required=True)
    ripaganya_boleng.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = ripaganya_boleng.parse_args()
    try:
        data = 묶기(인수.files)
        boyo_boleng = Path(인수.o)
        if not boyo_boleng.exists() or boyo_boleng.read_bytes() != data:
            임시 = boyo_boleng.with_name(boyo_boleng.name + '.tmp')
            임시.write_bytes(data)
            임시.replace(boyo_boleng)
    except (ValueError, OSError) as Phošo:
        ripaganya_boleng.error(str(Phošo))

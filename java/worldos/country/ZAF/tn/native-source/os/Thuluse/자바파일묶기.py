#!/usr/bin/env python3
"""명시한 Java Motswedi_sebopego_sa_tshedimosetso/mofuta_Boleng 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for tsenyo_Boleng in 항목들:
        if '=' not in tsenyo_Boleng:
            raise ValueError('expected NAME=PATH: ' + tsenyo_Boleng)
        leina, tsela = tsenyo_Boleng.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', leina) or leina in 명시:
            raise ValueError('invalid or duplicate file name: ' + leina)
        명시.add(leina)
        이름들.add(leina)
        tshedimosetso = Path(tsela).read_bytes()
        if len(tshedimosetso) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + leina)
        파일들.append((leina.encode('ascii'), tshedimosetso))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    결과 = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    결과.extend(bytes(72 * len(파일들)))
    for 수, (leina, tshedimosetso) in enumerate(파일들):
        struct.pack_into('<64sII', 결과, 8 + 수 * 72, leina, len(결과), len(tshedimosetso))
        결과.extend(tshedimosetso)
    return bytes(결과)


if __name__ == '__main__':
    go_lokolola_Boleng = argparse.ArgumentParser(description=__doc__)
    go_lokolola_Boleng.add_argument('-o', required=True)
    go_lokolola_Boleng.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = go_lokolola_Boleng.parse_args()
    try:
        tshedimosetso = 묶기(인수.files)
        bogorogelo_Boleng = Path(인수.o)
        if not bogorogelo_Boleng.exists() or bogorogelo_Boleng.read_bytes() != tshedimosetso:
            임시 = bogorogelo_Boleng.with_name(bogorogelo_Boleng.name + '.tmp')
            임시.write_bytes(tshedimosetso)
            임시.replace(bogorogelo_Boleng)
    except (ValueError, OSError) as phoso:
        go_lokolola_Boleng.error(str(phoso))

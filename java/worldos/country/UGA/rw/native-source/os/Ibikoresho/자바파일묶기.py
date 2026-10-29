#!/usr/bin/env python3
"""명시한 Java inkomoko_igiti/icyiciro_agaciro_55654bf1 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for icyinjizwa_agaciro in 항목들:
        if '=' not in icyinjizwa_agaciro:
            raise ValueError('expected NAME=PATH: ' + icyinjizwa_agaciro)
        Izina, Inzira = icyinjizwa_agaciro.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Izina) or Izina in 명시:
            raise ValueError('invalid or duplicate file name: ' + Izina)
        명시.add(Izina)
        이름들.add(Izina)
        amakurushingiro = Path(Inzira).read_bytes()
        if len(amakurushingiro) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Izina)
        파일들.append((Izina.encode('ascii'), amakurushingiro))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    결과 = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    결과.extend(bytes(72 * len(파일들)))
    for 수, (Izina, amakurushingiro) in enumerate(파일들):
        struct.pack_into('<64sII', 결과, 8 + 수 * 72, Izina, len(결과), len(amakurushingiro))
        결과.extend(amakurushingiro)
    return bytes(결과)


if __name__ == '__main__':
    gusesengura_agaciro = argparse.ArgumentParser(description=__doc__)
    gusesengura_agaciro.add_argument('-o', required=True)
    gusesengura_agaciro.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = gusesengura_agaciro.parse_args()
    try:
        amakurushingiro = 묶기(인수.files)
        aho_ijya_agaciro = Path(인수.o)
        if not aho_ijya_agaciro.exists() or aho_ijya_agaciro.read_bytes() != amakurushingiro:
            임시 = aho_ijya_agaciro.with_name(aho_ijya_agaciro.name + '.tmp')
            임시.write_bytes(amakurushingiro)
            임시.replace(aho_ijya_agaciro)
    except (ValueError, OSError) as IKOSA:
        gusesengura_agaciro.error(str(IKOSA))

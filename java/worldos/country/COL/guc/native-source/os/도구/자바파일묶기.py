#!/usr/bin/env python3
"""명시한 Java eejeejetülein_wunu_ulia/akotchijuushi_ajutuu_55654bf1 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for ekeroliaa_ajutuu in 항목들:
        if '=' not in ekeroliaa_ajutuu:
            raise ValueError('expected NAME=PATH: ' + ekeroliaa_ajutuu)
        이름, wopu_a_ttaaleemüin = ekeroliaa_ajutuu.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', 이름) or 이름 in 명시:
            raise ValueError('invalid or duplicate file name: ' + 이름)
        명시.add(이름)
        이름들.add(이름)
        atijaaya = Path(wopu_a_ttaaleemüin).read_bytes()
        if len(atijaaya) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + 이름)
        파일들.append((이름.encode('ascii'), atijaaya))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    결과 = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    결과.extend(bytes(72 * len(파일들)))
    for 수, (이름, atijaaya) in enumerate(파일들):
        struct.pack_into('<64sII', 결과, 8 + 수 * 72, 이름, len(결과), len(atijaaya))
        결과.extend(atijaaya)
    return bytes(결과)


if __name__ == '__main__':
    akatajaa_ajutuu = argparse.ArgumentParser(description=__doc__)
    akatajaa_ajutuu.add_argument('-o', required=True)
    akatajaa_ajutuu.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = akatajaa_ajutuu.parse_args()
    try:
        atijaaya = 묶기(인수.files)
        jalamüinjatü_ajutuu = Path(인수.o)
        if not jalamüinjatü_ajutuu.exists() or jalamüinjatü_ajutuu.read_bytes() != atijaaya:
            임시 = jalamüinjatü_ajutuu.with_name(jalamüinjatü_ajutuu.name + '.tmp')
            임시.write_bytes(atijaaya)
            임시.replace(jalamüinjatü_ajutuu)
    except (ValueError, OSError) as ajachitia:
        akatajaa_ajutuu.error(str(ajachitia))

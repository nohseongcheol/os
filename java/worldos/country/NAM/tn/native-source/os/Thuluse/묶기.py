#!/usr/bin/env python3
"""명시한 modirisi ELF만 읽기 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    go_lokolola_Boleng = argparse.ArgumentParser()
    go_lokolola_Boleng.add_argument('-o', required=True)
    go_lokolola_Boleng.add_argument('files', nargs='+', help='leina=ELF경로')
    인자 = go_lokolola_Boleng.parse_args()
    if len(인자.files) > 32:
        go_lokolola_Boleng.error('Tiriso_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for tsenyo_Boleng in 인자.files:
        leina, tsela = tsenyo_Boleng.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', leina) or leina in 이름들:
            go_lokolola_Boleng.error('diragatsa_Taelo 이름이 잘못되었거나 중복됨: ' + leina)
        이름들.add(leina)
        tshedimosetso = Path(tsela).read_bytes()
        if len(tshedimosetso) > 2 * 1024 * 1024:
            go_lokolola_Boleng.error('diragatsa_Taelo 파일이 너무 큼')
        항목들.append((leina.encode(), tshedimosetso))
    결과 = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', 결과, 0, 0x50414b4a, len(항목들))
    for tshupane, (leina, tshedimosetso) in enumerate(항목들):
        결과.extend(bytes((-len(결과)) % 16))
        struct.pack_into('<16sII', 결과, 8 + tshupane * 24, leina, len(결과), len(tshedimosetso))
        결과.extend(tshedimosetso)
    Path(인자.o).write_bytes(결과)

if __name__ == '__main__':
    묶기()

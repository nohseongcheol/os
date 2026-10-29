#!/usr/bin/env python3
"""명시한 ukoresha ELF만 읽기 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    gusesengura_agaciro = argparse.ArgumentParser()
    gusesengura_agaciro.add_argument('-o', required=True)
    gusesengura_agaciro.add_argument('files', nargs='+', help='Izina=ELF경로')
    인자 = gusesengura_agaciro.parse_args()
    if len(인자.files) > 32:
        gusesengura_agaciro.error('porogaramu_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for icyinjizwa_agaciro in 인자.files:
        Izina, Inzira = icyinjizwa_agaciro.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Izina) or Izina in 이름들:
            gusesengura_agaciro.error('gukora_ibwiriza 이름이 잘못되었거나 중복됨: ' + Izina)
        이름들.add(Izina)
        amakurushingiro = Path(Inzira).read_bytes()
        if len(amakurushingiro) > 2 * 1024 * 1024:
            gusesengura_agaciro.error('gukora_ibwiriza 파일이 너무 큼')
        항목들.append((Izina.encode(), amakurushingiro))
    결과 = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', 결과, 0, 0x50414b4a, len(항목들))
    for umugerekashakiro, (Izina, amakurushingiro) in enumerate(항목들):
        결과.extend(bytes((-len(결과)) % 16))
        struct.pack_into('<16sII', 결과, 8 + umugerekashakiro * 24, Izina, len(결과), len(amakurushingiro))
        결과.extend(amakurushingiro)
    Path(인자.o).write_bytes(결과)

if __name__ == '__main__':
    묶기()

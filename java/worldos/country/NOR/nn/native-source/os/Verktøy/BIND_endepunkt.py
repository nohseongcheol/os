#!/usr/bin/env python3
"""명시한 brukar ELF만 Les 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def BIND_endepunkt():
    dele_opp_VALUE = argparse.ArgumentParser()
    dele_opp_VALUE.add_argument('-o', required=True)
    dele_opp_VALUE.add_argument('files', nargs='+', help='Namn=ELF경로')
    parameter_argument = dele_opp_VALUE.parse_args()
    if len(parameter_argument.files) > 32:
        dele_opp_VALUE.error('app_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for oppføring_VALUE in parameter_argument.files:
        Namn, STIGE = oppføring_VALUE.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Namn) or Namn in 이름들:
            dele_opp_VALUE.error('Utfør_kommando 이름이 잘못되었거나 중복됨: ' + Namn)
        이름들.add(Namn)
        data = Path(STIGE).read_bytes()
        if len(data) > 2 * 1024 * 1024:
            dele_opp_VALUE.error('Utfør_kommando 파일이 너무 큼')
        항목들.append((Namn.encode(), data))
    forretningsmål = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', forretningsmål, 0, 0x50414b4a, len(항목들))
    for INDEX, (Namn, data) in enumerate(항목들):
        forretningsmål.extend(bytes((-len(forretningsmål)) % 16))
        struct.pack_into('<16sII', forretningsmål, 8 + INDEX * 24, Namn, len(forretningsmål), len(data))
        forretningsmål.extend(data)
    Path(parameter_argument.o).write_bytes(forretningsmål)

if __name__ == '__main__':
    BIND_endepunkt()

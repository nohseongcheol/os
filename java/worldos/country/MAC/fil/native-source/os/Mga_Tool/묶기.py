#!/usr/bin/env python3
"""명시한 gumagamit ELF만 읽기 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    mag_parse_VALUE = argparse.ArgumentParser()
    mag_parse_VALUE.add_argument('-o', required=True)
    mag_parse_VALUE.add_argument('files', nargs='+', help='pangalan=ELF경로')
    parameter_argumento = mag_parse_VALUE.parse_args()
    if len(parameter_argumento.files) > 32:
        mag_parse_VALUE.error('app_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for pagpasok_VALUE in parameter_argumento.files:
        pangalan, path = pagpasok_VALUE.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', pangalan) or pangalan in 이름들:
            mag_parse_VALUE.error('Mag_execute_utos 이름이 잘못되었거나 중복됨: ' + pangalan)
        이름들.add(pangalan)
        data = Path(path).read_bytes()
        if len(data) > 2 * 1024 * 1024:
            mag_parse_VALUE.error('Mag_execute_utos 파일이 너무 큼')
        항목들.append((pangalan.encode(), data))
    sukat = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', sukat, 0, 0x50414b4a, len(항목들))
    for INDEX, (pangalan, data) in enumerate(항목들):
        sukat.extend(bytes((-len(sukat)) % 16))
        struct.pack_into('<16sII', sukat, 8 + INDEX * 24, pangalan, len(sukat), len(data))
        sukat.extend(data)
    Path(parameter_argumento.o).write_bytes(sukat)

if __name__ == '__main__':
    묶기()

#!/usr/bin/env python3
"""명시한 utent ELF만 읽기 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    analizza_VALUE = argparse.ArgumentParser()
    analizza_VALUE.add_argument('-o', required=True)
    analizza_VALUE.add_argument('files', nargs='+', help='isem=ELF경로')
    인자 = analizza_VALUE.parse_args()
    if len(인자.files) > 32:
        analizza_VALUE.error('programm_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for entrata_VALUE in 인자.files:
        isem, mogħdija = entrata_VALUE.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', isem) or isem in 이름들:
            analizza_VALUE.error('eżegwixxa_kmand 이름이 잘못되었거나 중복됨: ' + isem)
        이름들.add(isem)
        data = Path(mogħdija).read_bytes()
        if len(data) > 2 * 1024 * 1024:
            analizza_VALUE.error('eżegwixxa_kmand 파일이 너무 큼')
        항목들.append((isem.encode(), data))
    miżura = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', miżura, 0, 0x50414b4a, len(항목들))
    for INDEX, (isem, data) in enumerate(항목들):
        miżura.extend(bytes((-len(miżura)) % 16))
        struct.pack_into('<16sII', miżura, 8 + INDEX * 24, isem, len(miżura), len(data))
        miżura.extend(data)
    Path(인자.o).write_bytes(miżura)

if __name__ == '__main__':
    묶기()

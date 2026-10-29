#!/usr/bin/env python3
"""명시한 mošomiši ELF만 Bala 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    ripaganya_boleng = argparse.ArgumentParser()
    ripaganya_boleng.add_argument('-o', required=True)
    ripaganya_boleng.add_argument('files', nargs='+', help='Leina=ELF경로')
    인자 = ripaganya_boleng.parse_args()
    if len(인자.files) > 32:
        ripaganya_boleng.error('tirišo_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for go_tsenya_tshedimošo_boleng in 인자.files:
        Leina, Tsejana = go_tsenya_tshedimošo_boleng.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Leina) or Leina in 이름들:
            ripaganya_boleng.error('phethagatša_taelo 이름이 잘못되었거나 중복됨: ' + Leina)
        이름들.add(Leina)
        data = Path(Tsejana).read_bytes()
        if len(data) > 2 * 1024 * 1024:
            ripaganya_boleng.error('phethagatša_taelo 파일이 너무 큼')
        항목들.append((Leina.encode(), data))
    결과 = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', 결과, 0, 0x50414b4a, len(항목들))
    for lokela, (Leina, data) in enumerate(항목들):
        결과.extend(bytes((-len(결과)) % 16))
        struct.pack_into('<16sII', 결과, 8 + lokela * 24, Leina, len(결과), len(data))
        결과.extend(data)
    Path(인자.o).write_bytes(결과)

if __name__ == '__main__':
    묶기()

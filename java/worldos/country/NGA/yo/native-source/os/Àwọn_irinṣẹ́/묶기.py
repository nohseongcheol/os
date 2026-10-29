#!/usr/bin/env python3
"""명시한 aṣàmúlò ELF만 Kàá 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    ìpínsíwẹ́wẹ́_iye = argparse.ArgumentParser()
    ìpínsíwẹ́wẹ́_iye.add_argument('-o', required=True)
    ìpínsíwẹ́wẹ́_iye.add_argument('files', nargs='+', help='Orúkọ=ELF경로')
    인자 = ìpínsíwẹ́wẹ́_iye.parse_args()
    if len(인자.files) > 32:
        ìpínsíwẹ́wẹ́_iye.error('àtòjọ_ètò_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for ìgbéwọlé_iye in 인자.files:
        Orúkọ, ọ̀nà = ìgbéwọlé_iye.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Orúkọ) or Orúkọ in 이름들:
            ìpínsíwẹ́wẹ́_iye.error('ṣiṣẹ́_àṣẹ 이름이 잘못되었거나 중복됨: ' + Orúkọ)
        이름들.add(Orúkọ)
        détà = Path(ọ̀nà).read_bytes()
        if len(détà) > 2 * 1024 * 1024:
            ìpínsíwẹ́wẹ́_iye.error('ṣiṣẹ́_àṣẹ 파일이 너무 큼')
        항목들.append((Orúkọ.encode(), détà))
    결과 = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', 결과, 0, 0x50414b4a, len(항목들))
    for wá_atọ̀ka_àkóónú, (Orúkọ, détà) in enumerate(항목들):
        결과.extend(bytes((-len(결과)) % 16))
        struct.pack_into('<16sII', 결과, 8 + wá_atọ̀ka_àkóónú * 24, Orúkọ, len(결과), len(détà))
        결과.extend(détà)
    Path(인자.o).write_bytes(결과)

if __name__ == '__main__':
    묶기()

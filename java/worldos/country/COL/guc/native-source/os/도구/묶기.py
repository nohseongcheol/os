#!/usr/bin/env python3
"""명시한 ka_yataayakalü ELF만 읽기 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    akatajaa_ajutuu = argparse.ArgumentParser()
    akatajaa_ajutuu.add_argument('-o', required=True)
    akatajaa_ajutuu.add_argument('files', nargs='+', help='이름=ELF경로')
    인자 = akatajaa_ajutuu.parse_args()
    if len(인자.files) > 32:
        akatajaa_ajutuu.error('akumajiaa_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for ekeroliaa_ajutuu in 인자.files:
        이름, wopu_a_ttaaleemüin = ekeroliaa_ajutuu.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', 이름) or 이름 in 이름들:
            akatajaa_ajutuu.error('실행 이름이 잘못되었거나 중복됨: ' + 이름)
        이름들.add(이름)
        atijaaya = Path(wopu_a_ttaaleemüin).read_bytes()
        if len(atijaaya) > 2 * 1024 * 1024:
            akatajaa_ajutuu.error('실행 파일이 너무 큼')
        항목들.append((이름.encode(), atijaaya))
    결과 = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', 결과, 0, 0x50414b4a, len(항목들))
    for ee_iyatialujuna, (이름, atijaaya) in enumerate(항목들):
        결과.extend(bytes((-len(결과)) % 16))
        struct.pack_into('<16sII', 결과, 8 + ee_iyatialujuna * 24, 이름, len(결과), len(atijaaya))
        결과.extend(atijaaya)
    Path(인자.o).write_bytes(결과)

if __name__ == '__main__':
    묶기()

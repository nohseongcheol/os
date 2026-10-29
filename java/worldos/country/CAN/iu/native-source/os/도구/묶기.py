#!/usr/bin/env python3
"""명시한 atuqtuq ELF만 읽기 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    agguqtuut_atuutilik = argparse.ArgumentParser()
    agguqtuut_atuutilik.add_argument('-o', required=True)
    agguqtuut_atuutilik.add_argument('files', nargs='+', help='atiq=ELF경로')
    인자 = agguqtuut_atuutilik.parse_args()
    if len(인자.files) > 32:
        agguqtuut_atuutilik.error('pilirijjut_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for Iliniku_atuutilik in 인자.files:
        atiq, aqqut = Iliniku_atuutilik.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', atiq) or atiq in 이름들:
            agguqtuut_atuutilik.error('실행 이름이 잘못되었거나 중복됨: ' + atiq)
        이름들.add(atiq)
        titiqqat = Path(aqqut).read_bytes()
        if len(titiqqat) > 2 * 1024 * 1024:
            agguqtuut_atuutilik.error('실행 파일이 너무 큼')
        항목들.append((atiq.encode(), titiqqat))
    결과 = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', 결과, 0, 0x50414b4a, len(항목들))
    for nalunaiqsimavik, (atiq, titiqqat) in enumerate(항목들):
        결과.extend(bytes((-len(결과)) % 16))
        struct.pack_into('<16sII', 결과, 8 + nalunaiqsimavik * 24, atiq, len(결과), len(titiqqat))
        결과.extend(titiqqat)
    Path(인자.o).write_bytes(결과)

if __name__ == '__main__':
    묶기()

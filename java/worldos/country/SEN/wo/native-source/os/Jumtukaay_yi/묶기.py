#!/usr/bin/env python3
"""명시한 kiy_jariñoo_internet ELF만 읽기 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    Segg_xëyma = argparse.ArgumentParser()
    Segg_xëyma.add_argument('-o', required=True)
    Segg_xëyma.add_argument('files', nargs='+', help='tur_253d1510=ELF경로')
    인자 = Segg_xëyma.parse_args()
    if len(인자.files) > 32:
        Segg_xëyma.error('jëfekaay_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for dugal_xabaar_xëyma in 인자.files:
        tur_253d1510, Yoonu_jëmale = dugal_xabaar_xëyma.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', tur_253d1510) or tur_253d1510 in 이름들:
            Segg_xëyma.error('def_ndigel 이름이 잘못되었거나 중복됨: ' + tur_253d1510)
        이름들.add(tur_253d1510)
        mbir = Path(Yoonu_jëmale).read_bytes()
        if len(mbir) > 2 * 1024 * 1024:
            Segg_xëyma.error('def_ndigel 파일이 너무 큼')
        항목들.append((tur_253d1510.encode(), mbir))
    결과 = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', 결과, 0, 0x50414b4a, len(항목들))
    for àlluwa_tur, (tur_253d1510, mbir) in enumerate(항목들):
        결과.extend(bytes((-len(결과)) % 16))
        struct.pack_into('<16sII', 결과, 8 + àlluwa_tur * 24, tur_253d1510, len(결과), len(mbir))
        결과.extend(mbir)
    Path(인자.o).write_bytes(결과)

if __name__ == '__main__':
    묶기()

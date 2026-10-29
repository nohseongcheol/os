#!/usr/bin/env python3
"""명시한 mtumiaji ELF만 읽기 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    changanua_thamani = argparse.ArgumentParser()
    changanua_thamani.add_argument('-o', required=True)
    changanua_thamani.add_argument('files', nargs='+', help='Jina=ELF경로')
    parameta_hoja = changanua_thamani.parse_args()
    if len(parameta_hoja.files) > 32:
        changanua_thamani.error('programu_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for ingizo_thamani in parameta_hoja.files:
        Jina, njia = ingizo_thamani.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Jina) or Jina in 이름들:
            changanua_thamani.error('tekeleza_amri 이름이 잘못되었거나 중복됨: ' + Jina)
        이름들.add(Jina)
        data = Path(njia).read_bytes()
        if len(data) > 2 * 1024 * 1024:
            changanua_thamani.error('tekeleza_amri 파일이 너무 큼')
        항목들.append((Jina.encode(), data))
    결과 = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', 결과, 0, 0x50414b4a, len(항목들))
    for kielezo, (Jina, data) in enumerate(항목들):
        결과.extend(bytes((-len(결과)) % 16))
        struct.pack_into('<16sII', 결과, 8 + kielezo * 24, Jina, len(결과), len(data))
        결과.extend(data)
    Path(parameta_hoja.o).write_bytes(결과)

if __name__ == '__main__':
    묶기()

#!/usr/bin/env python3
"""명시한 umsebenzisi ELF만 Funda 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    ingcaciso_yegama_ixabiso = argparse.ArgumentParser()
    ingcaciso_yegama_ixabiso.add_argument('-o', required=True)
    ingcaciso_yegama_ixabiso.add_argument('files', nargs='+', help='Igama=ELF경로')
    인자 = ingcaciso_yegama_ixabiso.parse_args()
    if len(인자.files) > 32:
        ingcaciso_yegama_ixabiso.error('inkqubo_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for ufako_nkcukacha_ixabiso in 인자.files:
        Igama, INDLELA = ufako_nkcukacha_ixabiso.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Igama) or Igama in 이름들:
            ingcaciso_yegama_ixabiso.error('ukwenza_umyalelo 이름이 잘못되었거나 중복됨: ' + Igama)
        이름들.add(Igama)
        iingcombolo = Path(INDLELA).read_bytes()
        if len(iingcombolo) > 2 * 1024 * 1024:
            ingcaciso_yegama_ixabiso.error('ukwenza_umyalelo 파일이 너무 큼')
        항목들.append((Igama.encode(), iingcombolo))
    결과 = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', 결과, 0, 0x50414b4a, len(항목들))
    for indeksa, (Igama, iingcombolo) in enumerate(항목들):
        결과.extend(bytes((-len(결과)) % 16))
        struct.pack_into('<16sII', 결과, 8 + indeksa * 24, Igama, len(결과), len(iingcombolo))
        결과.extend(iingcombolo)
    Path(인자.o).write_bytes(결과)

if __name__ == '__main__':
    묶기()

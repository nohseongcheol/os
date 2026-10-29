#!/usr/bin/env python3
"""명시한 వినియోగదారు ELF만 చదువు 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    పార్స్_మూల్యం = argparse.ArgumentParser()
    పార్స్_మూల్యం.add_argument('-o', required=True)
    పార్స్_మూల్యం.add_argument('files', nargs='+', help='పేరు=ELF경로')
    పారామీటర్_కారకం = పార్స్_మూల్యం.parse_args()
    if len(పారామీటర్_కారకం.files) > 32:
        పార్స్_మూల్యం.error('అనువర్తనం_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for ప్రవేశం_మూల్యం in పారామీటర్_కారకం.files:
        పేరు, పాత్ = ప్రవేశం_మూల్యం.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', పేరు) or పేరు in 이름들:
            పార్స్_మూల్యం.error('అమలు_చేయి_ఆదేశం 이름이 잘못되었거나 중복됨: ' + పేరు)
        이름들.add(పేరు)
        డేటా = Path(పాత్).read_bytes()
        if len(డేటా) > 2 * 1024 * 1024:
            పార్స్_మూల్యం.error('అమలు_చేయి_ఆదేశం 파일이 너무 큼')
        항목들.append((పేరు.encode(), డేటా))
    ప్రమాణం = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', ప్రమాణం, 0, 0x50414b4a, len(항목들))
    for సూచీ, (పేరు, డేటా) in enumerate(항목들):
        ప్రమాణం.extend(bytes((-len(ప్రమాణం)) % 16))
        struct.pack_into('<16sII', ప్రమాణం, 8 + సూచీ * 24, పేరు, len(ప్రమాణం), len(డేటా))
        ప్రమాణం.extend(డేటా)
    Path(పారామీటర్_కారకం.o).write_bytes(ప్రమాణం)

if __name__ == '__main__':
    묶기()

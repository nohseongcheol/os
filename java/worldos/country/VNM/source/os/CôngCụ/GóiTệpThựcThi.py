#!/usr/bin/env python3
"""명시한 NgườiDùng ELF만 đọc 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def GóiTệpThựcThi():
    phânTíchCúPhápGiáTrị = argparse.ArgumentParser()
    phânTíchCúPhápGiáTrị.add_argument('-o', required=True)
    phânTíchCúPhápGiáTrị.add_argument('files', nargs='+', help='tên=ELF경로')
    đốiSốThamSố = phânTíchCúPhápGiáTrị.parse_args()
    if len(đốiSốThamSố.files) > 32:
        phânTíchCúPhápGiáTrị.error('ChươngTrình giáTrịTốiĐa 32개')
    danhSáchCácMục = []
    danhSáchCácTên = set()
    for giáTrịMục in đốiSốThamSố.files:
        tên, đườngDẫn = giáTrịMục.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', tên) or tên in danhSáchCácTên:
            phânTíchCúPhápGiáTrị.error('thựcThiLệnh 이름이 잘못되었거나 중복됨: ' + tên)
        danhSáchCácTên.add(tên)
        DữLiệu = Path(đườngDẫn).read_bytes()
        if len(DữLiệu) > 2 * 1024 * 1024:
            phânTíchCúPhápGiáTrị.error('thựcThiLệnh 파일이 너무 큼')
        danhSáchCácMục.append((tên.encode(), DữLiệu))
    kếtQuả = bytearray(8 + 24 * len(danhSáchCácMục))
    struct.pack_into('<II', kếtQuả, 0, 0x50414b4a, len(danhSáchCácMục))
    for sốHiệu, (tên, DữLiệu) in enumerate(danhSáchCácMục):
        kếtQuả.extend(bytes((-len(kếtQuả)) % 16))
        struct.pack_into('<16sII', kếtQuả, 8 + sốHiệu * 24, tên, len(kếtQuả), len(DữLiệu))
        kếtQuả.extend(DữLiệu)
    Path(đốiSốThamSố.o).write_bytes(kếtQuả)

if __name__ == '__main__':
    GóiTệpThựcThi()

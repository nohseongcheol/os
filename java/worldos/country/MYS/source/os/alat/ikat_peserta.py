#!/usr/bin/env python3
"""명시한 ruang_pengguna ELF만 Baca 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def ikat_peserta():
    hurai_VALUE = argparse.ArgumentParser()
    hurai_VALUE.add_argument('-o', required=True)
    hurai_VALUE.add_argument('files', nargs='+', help='Nama=ELF경로')
    parameter_argumen = hurai_VALUE.parse_args()
    if len(parameter_argumen.files) > 32:
        hurai_VALUE.error('aplikasi_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for pemasukan_VALUE in parameter_argumen.files:
        Nama, LALUAN = pemasukan_VALUE.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Nama) or Nama in 이름들:
            hurai_VALUE.error('laksanakan_perintah 이름이 잘못되었거나 중복됨: ' + Nama)
        이름들.add(Nama)
        data = Path(LALUAN).read_bytes()
        if len(data) > 2 * 1024 * 1024:
            hurai_VALUE.error('laksanakan_perintah 파일이 너무 큼')
        항목들.append((Nama.encode(), data))
    ukuran = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', ukuran, 0, 0x50414b4a, len(항목들))
    for INDEX, (Nama, data) in enumerate(항목들):
        ukuran.extend(bytes((-len(ukuran)) % 16))
        struct.pack_into('<16sII', ukuran, 8 + INDEX * 24, Nama, len(ukuran), len(data))
        ukuran.extend(data)
    Path(parameter_argumen.o).write_bytes(ukuran)

if __name__ == '__main__':
    ikat_peserta()

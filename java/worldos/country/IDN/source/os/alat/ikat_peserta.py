#!/usr/bin/env python3
"""명시한 ruang_pengguna ELF만 Baca 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def ikat_peserta():
    urai_VALUE = argparse.ArgumentParser()
    urai_VALUE.add_argument('-o', required=True)
    urai_VALUE.add_argument('files', nargs='+', help='Nama_2=ELF경로')
    parameter_argumen = urai_VALUE.parse_args()
    if len(parameter_argumen.files) > 32:
        urai_VALUE.error('apl_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for entri_VALUE in parameter_argumen.files:
        Nama_2, jalur = entri_VALUE.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Nama_2) or Nama_2 in 이름들:
            urai_VALUE.error('Jalankan_perintah 이름이 잘못되었거나 중복됨: ' + Nama_2)
        이름들.add(Nama_2)
        data = Path(jalur).read_bytes()
        if len(data) > 2 * 1024 * 1024:
            urai_VALUE.error('Jalankan_perintah 파일이 너무 큼')
        항목들.append((Nama_2.encode(), data))
    hasil = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', hasil, 0, 0x50414b4a, len(항목들))
    for INDEX, (Nama_2, data) in enumerate(항목들):
        hasil.extend(bytes((-len(hasil)) % 16))
        struct.pack_into('<16sII', hasil, 8 + INDEX * 24, Nama_2, len(hasil), len(data))
        hasil.extend(data)
    Path(parameter_argumen.o).write_bytes(hasil)

if __name__ == '__main__':
    ikat_peserta()

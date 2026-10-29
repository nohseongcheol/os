#!/usr/bin/env python3
"""명시한 хэрэглэгч ELF만 Унших 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    задлан_ялгал_хийх_утга = argparse.ArgumentParser()
    задлан_ялгал_хийх_утга.add_argument('-o', required=True)
    задлан_ялгал_хийх_утга.add_argument('files', nargs='+', help='Нэр=ELF경로')
    인자 = задлан_ялгал_хийх_утга.parse_args()
    if len(인자.files) > 32:
        задлан_ялгал_хийх_утга.error('програм_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for оролт_утга in 인자.files:
        Нэр, ЗАМ = оролт_утга.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Нэр) or Нэр in 이름들:
            задлан_ялгал_хийх_утга.error('Гүйцэтгэх_команд 이름이 잘못되었거나 중복됨: ' + Нэр)
        이름들.add(Нэр)
        өгөгдөл = Path(ЗАМ).read_bytes()
        if len(өгөгдөл) > 2 * 1024 * 1024:
            задлан_ялгал_хийх_утга.error('Гүйцэтгэх_команд 파일이 너무 큼')
        항목들.append((Нэр.encode(), өгөгдөл))
    결과 = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', 결과, 0, 0x50414b4a, len(항목들))
    for индекс, (Нэр, өгөгдөл) in enumerate(항목들):
        결과.extend(bytes((-len(결과)) % 16))
        struct.pack_into('<16sII', 결과, 8 + индекс * 24, Нэр, len(결과), len(өгөгдөл))
        결과.extend(өгөгдөл)
    Path(인자.o).write_bytes(결과)

if __name__ == '__main__':
    묶기()

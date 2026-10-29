#!/usr/bin/env python3
"""명시한 Java эх_мод/класс_утга 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for оролт_утга in 항목들:
        if '=' not in оролт_утга:
            raise ValueError('expected NAME=PATH: ' + оролт_утга)
        Нэр, ЗАМ = оролт_утга.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Нэр) or Нэр in 명시:
            raise ValueError('invalid or duplicate file name: ' + Нэр)
        명시.add(Нэр)
        이름들.add(Нэр)
        өгөгдөл = Path(ЗАМ).read_bytes()
        if len(өгөгдөл) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Нэр)
        파일들.append((Нэр.encode('ascii'), өгөгдөл))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    결과 = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    결과.extend(bytes(72 * len(파일들)))
    for 수, (Нэр, өгөгдөл) in enumerate(파일들):
        struct.pack_into('<64sII', 결과, 8 + 수 * 72, Нэр, len(결과), len(өгөгдөл))
        결과.extend(өгөгдөл)
    return bytes(결과)


if __name__ == '__main__':
    задлан_ялгал_хийх_утга = argparse.ArgumentParser(description=__doc__)
    задлан_ялгал_хийх_утга.add_argument('-o', required=True)
    задлан_ялгал_хийх_утга.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = задлан_ялгал_хийх_утга.parse_args()
    try:
        өгөгдөл = 묶기(인수.files)
        товлосон_газар_утга = Path(인수.o)
        if not товлосон_газар_утга.exists() or товлосон_газар_утга.read_bytes() != өгөгдөл:
            임시 = товлосон_газар_утга.with_name(товлосон_газар_утга.name + '.tmp')
            임시.write_bytes(өгөгдөл)
            임시.replace(товлосон_газар_утга)
    except (ValueError, OSError) as Алдаа:
        задлан_ялгал_хийх_утга.error(str(Алдаа))

#!/usr/bin/env python3
"""명시한 Java แหล่ง_ทรี/คลาส_ค่า 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def ผูก_ปลายทาง(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for รายการ_ค่า in 항목들:
        if '=' not in รายการ_ค่า:
            raise ValueError('expected NAME=PATH: ' + รายการ_ค่า)
        ชื่อ, เส้นทาง = รายการ_ค่า.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', ชื่อ) or ชื่อ in 명시:
            raise ValueError('invalid or duplicate file name: ' + ชื่อ)
        명시.add(ชื่อ)
        이름들.add(ชื่อ)
        ข้อมูล = Path(เส้นทาง).read_bytes()
        if len(ข้อมูล) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + ชื่อ)
        파일들.append((ชื่อ.encode('ascii'), ข้อมูล))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    ผลลัพธ์ = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    ผลลัพธ์.extend(bytes(72 * len(파일들)))
    for หมายเลข, (ชื่อ, ข้อมูล) in enumerate(파일들):
        struct.pack_into('<64sII', ผลลัพธ์, 8 + หมายเลข * 72, ชื่อ, len(ผลลัพธ์), len(ข้อมูล))
        ผลลัพธ์.extend(ข้อมูล)
    return bytes(ผลลัพธ์)


if __name__ == '__main__':
    แยกวิเคราะห์_ค่า = argparse.ArgumentParser(description=__doc__)
    แยกวิเคราะห์_ค่า.add_argument('-o', required=True)
    แยกวิเคราะห์_ค่า.add_argument('files', nargs='*', help='NAME=PATH')
    อาร์กิวเมนต์ = แยกวิเคราะห์_ค่า.parse_args()
    try:
        ข้อมูล = ผูก_ปลายทาง(อาร์กิวเมนต์.files)
        ปลายทาง_ค่า_a0fbc067 = Path(อาร์กิวเมนต์.o)
        if not ปลายทาง_ค่า_a0fbc067.exists() or ปลายทาง_ค่า_a0fbc067.read_bytes() != ข้อมูล:
            임시 = ปลายทาง_ค่า_a0fbc067.with_name(ปลายทาง_ค่า_a0fbc067.name + '.tmp')
            임시.write_bytes(ข้อมูล)
            임시.replace(ปลายทาง_ค่า_a0fbc067)
    except (ValueError, OSError) as ข้อผิดพลาด:
        แยกวิเคราะห์_ค่า.error(str(ข้อผิดพลาด))

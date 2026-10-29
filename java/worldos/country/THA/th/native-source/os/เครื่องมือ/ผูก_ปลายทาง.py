#!/usr/bin/env python3
"""명시한 ผู้ใช้ ELF만 อ่าน 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def ผูก_ปลายทาง():
    แยกวิเคราะห์_ค่า = argparse.ArgumentParser()
    แยกวิเคราะห์_ค่า.add_argument('-o', required=True)
    แยกวิเคราะห์_ค่า.add_argument('files', nargs='+', help='ชื่อ=ELF경로')
    พารามิเตอร์_อาร์กิวเมนต์ = แยกวิเคราะห์_ค่า.parse_args()
    if len(พารามิเตอร์_อาร์กิวเมนต์.files) > 32:
        แยกวิเคราะห์_ค่า.error('แอป_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for รายการ_ค่า in พารามิเตอร์_อาร์กิวเมนต์.files:
        ชื่อ, เส้นทาง = รายการ_ค่า.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', ชื่อ) or ชื่อ in 이름들:
            แยกวิเคราะห์_ค่า.error('ดําเนินการ_คําสั่ง 이름이 잘못되었거나 중복됨: ' + ชื่อ)
        이름들.add(ชื่อ)
        ข้อมูล = Path(เส้นทาง).read_bytes()
        if len(ข้อมูล) > 2 * 1024 * 1024:
            แยกวิเคราะห์_ค่า.error('ดําเนินการ_คําสั่ง 파일이 너무 큼')
        항목들.append((ชื่อ.encode(), ข้อมูล))
    ผลลัพธ์ = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', ผลลัพธ์, 0, 0x50414b4a, len(항목들))
    for ดัชนี, (ชื่อ, ข้อมูล) in enumerate(항목들):
        ผลลัพธ์.extend(bytes((-len(ผลลัพธ์)) % 16))
        struct.pack_into('<16sII', ผลลัพธ์, 8 + ดัชนี * 24, ชื่อ, len(ผลลัพธ์), len(ข้อมูล))
        ผลลัพธ์.extend(ข้อมูล)
    Path(พารามิเตอร์_อาร์กิวเมนต์.o).write_bytes(ผลลัพธ์)

if __name__ == '__main__':
    ผูก_ปลายทาง()

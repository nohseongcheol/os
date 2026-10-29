#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 เก็บ_ค่า 매체를 만든다. 기존 แฟ้ม/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def เปิด_รายการ(เส้นทาง):
    with Path(เส้นทาง).open('xb') as ข้อความออก:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        ข้อความออก.write(머리)
        ข้อความออก.truncate(2048 * 512)

if __name__ == '__main__':
    ตัวแยกวิเคราะห์_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ตัวแยกวิเคราะห์_48ee4b1b.add_argument('เส้นทาง')
    อาร์กิวเมนต์ = ตัวแยกวิเคราะห์_48ee4b1b.parse_args()
    เปิด_รายการ(อาร์กิวเมนต์.เส้นทาง)

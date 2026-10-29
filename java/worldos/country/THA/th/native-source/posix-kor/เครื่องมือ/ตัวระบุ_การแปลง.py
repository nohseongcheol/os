#!/usr/bin/env python3
"""ไทย C 식별자만 UCN으로 옮긴다. สตริง_ค่า·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

โทเค็น_ค่า = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<ตัวระบุ_ค่า>[^\W\d]\w*)', re.S | re.M)

def แปลง_ค่า_4633b7f3(รหัสต้นฉบับ):
    def 바꾸기(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(อักขระ_ค่า if ord(อักขระ_ค่า) < 128 else
                       ('\\u%04x' if ord(อักขระ_ค่า) <= 65535 else '\\U%08x') % ord(อักขระ_ค่า)
                       for อักขระ_ค่า in 일치[0])
    return โทเค็น_ค่า.sub(바꾸기, รหัสต้นฉบับ)

def ดําเนินการ_คําสั่ง():
    ตัวแยกวิเคราะห์_48ee4b1b = argparse.ArgumentParser()
    ตัวแยกวิเคราะห์_48ee4b1b.add_argument('원본', type=Path)
    ตัวแยกวิเคราะห์_48ee4b1b.add_argument('ข้อความออก', type=Path)
    อาร์กิวเมนต์ = ตัวแยกวิเคราะห์_48ee4b1b.parse_args()
    for แฟ้ม in sorted(อาร์กิวเมนต์.원본.rglob('*')):
        if แฟ้ม.suffix not in ('.c', '.h'):
            continue
        ข้อความออก = อาร์กิวเมนต์.ข้อความออก / แฟ้ม.relative_to(อาร์กิวเมนต์.원본)
        ข้อความออก.parent.mkdir(parents=True, exist_ok=True)
        새원문 = แปลง_ค่า_4633b7f3(แฟ้ม.read_text())
        if not ข้อความออก.exists() or ข้อความออก.read_text() != 새원문:
            ข้อความออก.write_text(새원문)

if __name__ == '__main__':
    ดําเนินการ_คําสั่ง()

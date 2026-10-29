#!/usr/bin/env python3
"""명시한 فضاء_المستخدم ELF만 قراءة 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def يربط_المشارك():
    يوزّع_قيمة = argparse.ArgumentParser()
    يوزّع_قيمة.add_argument('-o', required=True)
    يوزّع_قيمة.add_argument('files', nargs='+', help='اسم=ELF경로')
    معلمة_وسيطة = يوزّع_قيمة.parse_args()
    if len(معلمة_وسيطة.files) > 32:
        يوزّع_قيمة.error('تطبيق_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for إدخال_قيمة_962f286b in معلمة_وسيطة.files:
        اسم, مسار = إدخال_قيمة_962f286b.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', اسم) or اسم in 이름들:
            يوزّع_قيمة.error('ينفذ_أمر 이름이 잘못되었거나 중복됨: ' + اسم)
        이름들.add(اسم)
        بيانات = Path(مسار).read_bytes()
        if len(بيانات) > 2 * 1024 * 1024:
            يوزّع_قيمة.error('ينفذ_أمر 파일이 너무 큼')
        항목들.append((اسم.encode(), بيانات))
    نتيجة = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', نتيجة, 0, 0x50414b4a, len(항목들))
    for فهرس, (اسم, بيانات) in enumerate(항목들):
        نتيجة.extend(bytes((-len(نتيجة)) % 16))
        struct.pack_into('<16sII', نتيجة, 8 + فهرس * 24, اسم, len(نتيجة), len(بيانات))
        نتيجة.extend(بيانات)
    Path(معلمة_وسيطة.o).write_bytes(نتيجة)

if __name__ == '__main__':
    يربط_المشارك()

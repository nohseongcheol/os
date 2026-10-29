#!/usr/bin/env python3
"""명시한 Java مصدر_شجرة/فئة_قيمة_55654bf1 파일을 إقلاع_الآلة 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def يربط_المشارك(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for إدخال_قيمة_962f286b in 항목들:
        if '=' not in إدخال_قيمة_962f286b:
            raise ValueError('expected NAME=PATH: ' + إدخال_قيمة_962f286b)
        اسم, مسار = إدخال_قيمة_962f286b.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', اسم) or اسم in 명시:
            raise ValueError('invalid or duplicate file name: ' + اسم)
        명시.add(اسم)
        이름들.add(اسم)
        بيانات = Path(مسار).read_bytes()
        if len(بيانات) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + اسم)
        파일들.append((اسم.encode('ascii'), بيانات))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    نتيجة = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    نتيجة.extend(bytes(72 * len(파일들)))
    for رقم, (اسم, بيانات) in enumerate(파일들):
        struct.pack_into('<64sII', نتيجة, 8 + رقم * 72, اسم, len(نتيجة), len(بيانات))
        نتيجة.extend(بيانات)
    return bytes(نتيجة)


if __name__ == '__main__':
    يوزّع_قيمة = argparse.ArgumentParser(description=__doc__)
    يوزّع_قيمة.add_argument('-o', required=True)
    يوزّع_قيمة.add_argument('files', nargs='*', help='NAME=PATH')
    وسائط = يوزّع_قيمة.parse_args()
    try:
        بيانات = يربط_المشارك(وسائط.files)
        وجهة_قيمة = Path(وسائط.o)
        if not وجهة_قيمة.exists() or وجهة_قيمة.read_bytes() != بيانات:
            임시 = وجهة_قيمة.with_name(وجهة_قيمة.name + '.tmp')
            임시.write_bytes(بيانات)
            임시.replace(وجهة_قيمة)
    except (ValueError, OSError) as خطأ:
        يوزّع_قيمة.error(str(خطأ))

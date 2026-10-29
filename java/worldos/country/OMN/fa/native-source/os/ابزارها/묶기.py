#!/usr/bin/env python3
"""명시한 کاربر ELF만 خواندن 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    تفسیر_مقدار = argparse.ArgumentParser()
    تفسیر_مقدار.add_argument('-o', required=True)
    تفسیر_مقدار.add_argument('files', nargs='+', help='نام=ELF경로')
    پارامتر_آرگومان = تفسیر_مقدار.parse_args()
    if len(پارامتر_آرگومان.files) > 32:
        تفسیر_مقدار.error('برنامه_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for ورودی_مقدار in پارامتر_آرگومان.files:
        نام, مسیر = ورودی_مقدار.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', نام) or نام in 이름들:
            تفسیر_مقدار.error('اجرا_فرمان 이름이 잘못되었거나 중복됨: ' + نام)
        이름들.add(نام)
        داده_ها = Path(مسیر).read_bytes()
        if len(داده_ها) > 2 * 1024 * 1024:
            تفسیر_مقدار.error('اجرا_فرمان 파일이 너무 큼')
        항목들.append((نام.encode(), داده_ها))
    سنجش = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', سنجش, 0, 0x50414b4a, len(항목들))
    for فهرست, (نام, داده_ها) in enumerate(항목들):
        سنجش.extend(bytes((-len(سنجش)) % 16))
        struct.pack_into('<16sII', سنجش, 8 + فهرست * 24, نام, len(سنجش), len(داده_ها))
        سنجش.extend(داده_ها)
    Path(پارامتر_آرگومان.o).write_bytes(سنجش)

if __name__ == '__main__':
    묶기()

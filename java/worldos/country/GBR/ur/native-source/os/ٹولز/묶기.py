#!/usr/bin/env python3
"""명시한 صارف ELF만 پڑھیں 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    پارس_قدر = argparse.ArgumentParser()
    پارس_قدر.add_argument('-o', required=True)
    پارس_قدر.add_argument('files', nargs='+', help='نام=ELF경로')
    پیرا_میٹر_دلائل = پارس_قدر.parse_args()
    if len(پیرا_میٹر_دلائل.files) > 32:
        پارس_قدر.error('ایپ_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for اندراج_قدر in پیرا_میٹر_دلائل.files:
        نام, راستہ_2 = اندراج_قدر.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', نام) or نام in 이름들:
            پارس_قدر.error('نفاذ_کریں_حکم 이름이 잘못되었거나 중복됨: ' + نام)
        이름들.add(نام)
        کوائف = Path(راستہ_2).read_bytes()
        if len(کوائف) > 2 * 1024 * 1024:
            پارس_قدر.error('نفاذ_کریں_حکم 파일이 너무 큼')
        항목들.append((نام.encode(), کوائف))
    پیمائش = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', پیمائش, 0, 0x50414b4a, len(항목들))
    for اشاریہ, (نام, کوائف) in enumerate(항목들):
        پیمائش.extend(bytes((-len(پیمائش)) % 16))
        struct.pack_into('<16sII', پیمائش, 8 + اشاریہ * 24, نام, len(پیمائش), len(کوائف))
        پیمائش.extend(کوائف)
    Path(پیرا_میٹر_دلائل.o).write_bytes(پیمائش)

if __name__ == '__main__':
    묶기()

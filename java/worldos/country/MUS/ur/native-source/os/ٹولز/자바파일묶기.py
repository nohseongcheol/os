#!/usr/bin/env python3
"""명시한 Java ماخذ_شجر/صنف_قدر 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for اندراج_قدر in 항목들:
        if '=' not in اندراج_قدر:
            raise ValueError('expected NAME=PATH: ' + اندراج_قدر)
        نام, راستہ_2 = اندراج_قدر.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', نام) or نام in 명시:
            raise ValueError('invalid or duplicate file name: ' + نام)
        명시.add(نام)
        이름들.add(نام)
        کوائف = Path(راستہ_2).read_bytes()
        if len(کوائف) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + نام)
        파일들.append((نام.encode('ascii'), کوائف))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    پیمائش = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    پیمائش.extend(bytes(72 * len(파일들)))
    for 수, (نام, کوائف) in enumerate(파일들):
        struct.pack_into('<64sII', پیمائش, 8 + 수 * 72, نام, len(پیمائش), len(کوائف))
        پیمائش.extend(کوائف)
    return bytes(پیمائش)


if __name__ == '__main__':
    پارس_قدر = argparse.ArgumentParser(description=__doc__)
    پارس_قدر.add_argument('-o', required=True)
    پارس_قدر.add_argument('files', nargs='*', help='NAME=PATH')
    دلائل = پارس_قدر.parse_args()
    try:
        کوائف = 묶기(دلائل.files)
        منزل_مقصود_قدر = Path(دلائل.o)
        if not منزل_مقصود_قدر.exists() or منزل_مقصود_قدر.read_bytes() != کوائف:
            임시 = منزل_مقصود_قدر.with_name(منزل_مقصود_قدر.name + '.tmp')
            임시.write_bytes(کوائف)
            임시.replace(منزل_مقصود_قدر)
    except (ValueError, OSError) as غلطی:
        پارس_قدر.error(str(غلطی))

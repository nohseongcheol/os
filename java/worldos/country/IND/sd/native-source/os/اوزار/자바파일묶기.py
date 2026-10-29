#!/usr/bin/env python3
"""명시한 Java ماخذ_شجرو/درجو_قدر 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for داخلا_قدر in 항목들:
        if '=' not in داخلا_قدر:
            raise ValueError('expected NAME=PATH: ' + داخلا_قدر)
        نالو, راههه = داخلا_قدر.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', نالو) or نالو in 명시:
            raise ValueError('invalid or duplicate file name: ' + نالو)
        명시.add(نالو)
        이름들.add(نالو)
        ڪوائف = Path(راههه).read_bytes()
        if len(ڪوائف) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + نالو)
        파일들.append((نالو.encode('ascii'), ڪوائف))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    결과 = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    결과.extend(bytes(72 * len(파일들)))
    for 수, (نالو, ڪوائف) in enumerate(파일들):
        struct.pack_into('<64sII', 결과, 8 + 수 * 72, نالو, len(결과), len(ڪوائف))
        결과.extend(ڪوائف)
    return bytes(결과)


if __name__ == '__main__':
    해석 = argparse.ArgumentParser(description=__doc__)
    해석.add_argument('-o', required=True)
    해석.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = 해석.parse_args()
    try:
        ڪوائف = 묶기(인수.files)
        منزل_مقصود_قدر = Path(인수.o)
        if not منزل_مقصود_قدر.exists() or منزل_مقصود_قدر.read_bytes() != ڪوائف:
            임시 = منزل_مقصود_قدر.with_name(منزل_مقصود_قدر.name + '.tmp')
            임시.write_bytes(ڪوائف)
            임시.replace(منزل_مقصود_قدر)
    except (ValueError, OSError) as نقص:
        해석.error(str(نقص))

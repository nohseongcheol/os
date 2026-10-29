#!/usr/bin/env python3
"""명시한 Java ماخذ_شجرہ/درجہ_قدر 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for داخلہ_قدر in 항목들:
        if '=' not in داخلہ_قدر:
            raise ValueError('expected NAME=PATH: ' + داخلہ_قدر)
        ناں, راہ = داخلہ_قدر.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', ناں) or ناں in 명시:
            raise ValueError('invalid or duplicate file name: ' + ناں)
        명시.add(ناں)
        이름들.add(ناں)
        کوائف = Path(راہ).read_bytes()
        if len(کوائف) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + ناں)
        파일들.append((ناں.encode('ascii'), کوائف))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    결과 = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    결과.extend(bytes(72 * len(파일들)))
    for 수, (ناں, کوائف) in enumerate(파일들):
        struct.pack_into('<64sII', 결과, 8 + 수 * 72, ناں, len(결과), len(کوائف))
        결과.extend(کوائف)
    return bytes(결과)


if __name__ == '__main__':
    해석 = argparse.ArgumentParser(description=__doc__)
    해석.add_argument('-o', required=True)
    해석.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = 해석.parse_args()
    try:
        کوائف = 묶기(인수.files)
        منزل_مقصود_قدر = Path(인수.o)
        if not منزل_مقصود_قدر.exists() or منزل_مقصود_قدر.read_bytes() != کوائف:
            임시 = منزل_مقصود_قدر.with_name(منزل_مقصود_قدر.name + '.tmp')
            임시.write_bytes(کوائف)
            임시.replace(منزل_مقصود_قدر)
    except (ValueError, OSError) as نقص:
        해석.error(str(نقص))

#!/usr/bin/env python3
"""명시한 Java উৎস_ট্ৰি/শ্ৰেণী_মান 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for প্রবিষ্ট_মান in 항목들:
        if '=' not in প্রবিষ্ট_মান:
            raise ValueError('expected NAME=PATH: ' + প্রবিষ্ট_মান)
        নাম, পথ = প্রবিষ্ট_মান.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', নাম) or নাম in 명시:
            raise ValueError('invalid or duplicate file name: ' + নাম)
        명시.add(নাম)
        이름들.add(নাম)
        ডাটা = Path(পথ).read_bytes()
        if len(ডাটা) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + নাম)
        파일들.append((নাম.encode('ascii'), ডাটা))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    পৰিমাপ = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    পৰিমাপ.extend(bytes(72 * len(파일들)))
    for 수, (নাম, ডাটা) in enumerate(파일들):
        struct.pack_into('<64sII', পৰিমাপ, 8 + 수 * 72, নাম, len(পৰিমাপ), len(ডাটা))
        পৰিমাপ.extend(ডাটা)
    return bytes(পৰিমাপ)


if __name__ == '__main__':
    পাৰ্ছ_কৰক_মান = argparse.ArgumentParser(description=__doc__)
    পাৰ্ছ_কৰক_মান.add_argument('-o', required=True)
    পাৰ্ছ_কৰক_মান.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = পাৰ্ছ_কৰক_মান.parse_args()
    try:
        ডাটা = 묶기(인수.files)
        গন্তব্য_স্থান_মান = Path(인수.o)
        if not গন্তব্য_স্থান_মান.exists() or গন্তব্য_স্থান_মান.read_bytes() != ডাটা:
            임시 = গন্তব্য_স্থান_মান.with_name(গন্তব্য_স্থান_মান.name + '.tmp')
            임시.write_bytes(ডাটা)
            임시.replace(গন্তব্য_স্থান_মান)
    except (ValueError, OSError) as ত্ৰুটি:
        পাৰ্ছ_কৰক_মান.error(str(ত্ৰুটি))

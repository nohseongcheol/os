#!/usr/bin/env python3
"""명시한 Java উত্স_ট্রী/শ্রেণী_মান 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for ভুক্তি_মান in 항목들:
        if '=' not in ভুক্তি_মান:
            raise ValueError('expected NAME=PATH: ' + ভুক্তি_মান)
        নাম, পথ_2 = ভুক্তি_মান.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', নাম) or নাম in 명시:
            raise ValueError('invalid or duplicate file name: ' + নাম)
        명시.add(নাম)
        이름들.add(নাম)
        ডাটা = Path(পথ_2).read_bytes()
        if len(ডাটা) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + নাম)
        파일들.append((নাম.encode('ascii'), ডাটা))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    পরিমাপ = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    পরিমাপ.extend(bytes(72 * len(파일들)))
    for 수, (নাম, ডাটা) in enumerate(파일들):
        struct.pack_into('<64sII', পরিমাপ, 8 + 수 * 72, নাম, len(পরিমাপ), len(ডাটা))
        পরিমাপ.extend(ডাটা)
    return bytes(পরিমাপ)


if __name__ == '__main__':
    বিভাজন_করা_মান = argparse.ArgumentParser(description=__doc__)
    বিভাজন_করা_মান.add_argument('-o', required=True)
    বিভাজন_করা_মান.add_argument('files', nargs='*', help='NAME=PATH')
    আর্গুমেন্ট_তালিকা = বিভাজন_করা_মান.parse_args()
    try:
        ডাটা = 묶기(আর্গুমেন্ট_তালিকা.files)
        গন্তব্য_মান = Path(আর্গুমেন্ট_তালিকা.o)
        if not গন্তব্য_মান.exists() or গন্তব্য_মান.read_bytes() != ডাটা:
            임시 = গন্তব্য_মান.with_name(গন্তব্য_মান.name + '.tmp')
            임시.write_bytes(ডাটা)
            임시.replace(গন্তব্য_মান)
    except (ValueError, OSError) as ত্রুটি:
        বিভাজন_করা_মান.error(str(ত্রুটি))

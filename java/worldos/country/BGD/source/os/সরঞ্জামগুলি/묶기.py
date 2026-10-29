#!/usr/bin/env python3
"""명시한 ব্যবহারকারী ELF만 পড়া 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    বিভাজন_করা_মান = argparse.ArgumentParser()
    বিভাজন_করা_মান.add_argument('-o', required=True)
    বিভাজন_করা_মান.add_argument('files', nargs='+', help='নাম=ELF경로')
    প্যারামিটার_যুক্তি = বিভাজন_করা_মান.parse_args()
    if len(প্যারামিটার_যুক্তি.files) > 32:
        বিভাজন_করা_মান.error('অ্যাপ_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for ভুক্তি_মান in প্যারামিটার_যুক্তি.files:
        নাম, পথ_2 = ভুক্তি_মান.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', নাম) or নাম in 이름들:
            বিভাজন_করা_মান.error('কার্যকর_করুন_আদেশ 이름이 잘못되었거나 중복됨: ' + নাম)
        이름들.add(নাম)
        ডাটা = Path(পথ_2).read_bytes()
        if len(ডাটা) > 2 * 1024 * 1024:
            বিভাজন_করা_মান.error('কার্যকর_করুন_আদেশ 파일이 너무 큼')
        항목들.append((নাম.encode(), ডাটা))
    পরিমাপ = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', পরিমাপ, 0, 0x50414b4a, len(항목들))
    for সূচি, (নাম, ডাটা) in enumerate(항목들):
        পরিমাপ.extend(bytes((-len(পরিমাপ)) % 16))
        struct.pack_into('<16sII', পরিমাপ, 8 + সূচি * 24, নাম, len(পরিমাপ), len(ডাটা))
        পরিমাপ.extend(ডাটা)
    Path(প্যারামিটার_যুক্তি.o).write_bytes(পরিমাপ)

if __name__ == '__main__':
    묶기()

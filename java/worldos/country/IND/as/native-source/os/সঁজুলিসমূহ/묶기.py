#!/usr/bin/env python3
"""명시한 ব্যৱহাৰকৰ্তা ELF만 পড়া 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    পাৰ্ছ_কৰক_মান = argparse.ArgumentParser()
    পাৰ্ছ_কৰক_মান.add_argument('-o', required=True)
    পাৰ্ছ_কৰক_মান.add_argument('files', nargs='+', help='নাম=ELF경로')
    인자 = পাৰ্ছ_কৰক_মান.parse_args()
    if len(인자.files) > 32:
        পাৰ্ছ_কৰক_মান.error('এপ্প্_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for প্রবিষ্ট_মান in 인자.files:
        নাম, পথ = প্রবিষ্ট_মান.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', নাম) or নাম in 이름들:
            পাৰ্ছ_কৰক_মান.error('নিষ্পাদন_আদেশ 이름이 잘못되었거나 중복됨: ' + নাম)
        이름들.add(নাম)
        ডাটা = Path(পথ).read_bytes()
        if len(ডাটা) > 2 * 1024 * 1024:
            পাৰ্ছ_কৰক_মান.error('নিষ্পাদন_আদেশ 파일이 너무 큼')
        항목들.append((নাম.encode(), ডাটা))
    পৰিমাপ = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', পৰিমাপ, 0, 0x50414b4a, len(항목들))
    for ইনডেক্স, (নাম, ডাটা) in enumerate(항목들):
        পৰিমাপ.extend(bytes((-len(পৰিমাপ)) % 16))
        struct.pack_into('<16sII', পৰিমাপ, 8 + ইনডেক্স * 24, নাম, len(পৰিমাপ), len(ডাটা))
        পৰিমাপ.extend(ডাটা)
    Path(인자.o).write_bytes(পৰিমাপ)

if __name__ == '__main__':
    묶기()

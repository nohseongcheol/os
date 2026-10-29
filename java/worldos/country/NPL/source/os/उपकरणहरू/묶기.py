#!/usr/bin/env python3
"""명시한 प्रयोगकर्ता ELF만 पढनुहोस् 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    पदच्छेद_गर्नुहोस्_मान = argparse.ArgumentParser()
    पदच्छेद_गर्नुहोस्_मान.add_argument('-o', required=True)
    पदच्छेद_गर्नुहोस्_मान.add_argument('files', nargs='+', help='नाम=ELF경로')
    인자 = पदच्छेद_गर्नुहोस्_मान.parse_args()
    if len(인자.files) > 32:
        पदच्छेद_गर्नुहोस्_मान.error('अनुप्रयोग_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for प्रविष्टि_मान in 인자.files:
        नाम, मार्ग = प्रविष्टि_मान.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', नाम) or नाम in 이름들:
            पदच्छेद_गर्नुहोस्_मान.error('कार्यान्वयन_गर्नुहोस्_आदेश 이름이 잘못되었거나 중복됨: ' + नाम)
        이름들.add(नाम)
        लगत = Path(मार्ग).read_bytes()
        if len(लगत) > 2 * 1024 * 1024:
            पदच्छेद_गर्नुहोस्_मान.error('कार्यान्वयन_गर्नुहोस्_आदेश 파일이 너무 큼')
        항목들.append((नाम.encode(), लगत))
    मापन = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', मापन, 0, 0x50414b4a, len(항목들))
    for अनुक्रमणिका, (नाम, लगत) in enumerate(항목들):
        मापन.extend(bytes((-len(मापन)) % 16))
        struct.pack_into('<16sII', मापन, 8 + अनुक्रमणिका * 24, नाम, len(मापन), len(लगत))
        मापन.extend(लगत)
    Path(인자.o).write_bytes(मापन)

if __name__ == '__main__':
    묶기()

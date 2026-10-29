#!/usr/bin/env python3
"""명시한 ئىشلەتكۈچى ELF만 ئوقۇ 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    해석 = argparse.ArgumentParser()
    해석.add_argument('-o', required=True)
    해석.add_argument('files', nargs='+', help='ئاتى=ELF경로')
    인자 = 해석.parse_args()
    if len(인자.files) > 32:
        해석.error('ئەپ_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for كىرگۈزۈش_قىممىتى in 인자.files:
        ئاتى, يول = كىرگۈزۈش_قىممىتى.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', ئاتى) or ئاتى in 이름들:
            해석.error('ئىجرا_قىلىش_بۇيرۇق 이름이 잘못되었거나 중복됨: ' + ئاتى)
        이름들.add(ئاتى)
        مەلۇمات = Path(يول).read_bytes()
        if len(مەلۇمات) > 2 * 1024 * 1024:
            해석.error('ئىجرا_قىلىش_بۇيرۇق 파일이 너무 큼')
        항목들.append((ئاتى.encode(), مەلۇمات))
    ئۆلچەم = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', ئۆلچەم, 0, 0x50414b4a, len(항목들))
    for ئىندېكس, (ئاتى, مەلۇمات) in enumerate(항목들):
        ئۆلچەم.extend(bytes((-len(ئۆلچەم)) % 16))
        struct.pack_into('<16sII', ئۆلچەم, 8 + ئىندېكس * 24, ئاتى, len(ئۆلچەم), len(مەلۇمات))
        ئۆلچەم.extend(مەلۇمات)
    Path(인자.o).write_bytes(ئۆلچەم)

if __name__ == '__main__':
    묶기()

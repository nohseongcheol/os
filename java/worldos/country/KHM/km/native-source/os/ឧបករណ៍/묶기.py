#!/usr/bin/env python3
"""명시한 អ្នកប្រើ ELF만 អាន 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    ញែក_តំលៃ = argparse.ArgumentParser()
    ញែក_តំលៃ.add_argument('-o', required=True)
    ញែក_តំលៃ.add_argument('files', nargs='+', help='ឈ្មោះ=ELF경로')
    ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់ = ញែក_តំលៃ.parse_args()
    if len(ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.files) > 32:
        ញែក_តំលៃ.error('កម្មវិធី_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for ការបញ្ចូល_តំលៃ in ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.files:
        ឈ្មោះ, ផ្លូវ = ការបញ្ចូល_តំលៃ.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', ឈ្មោះ) or ឈ្មោះ in 이름들:
            ញែក_តំលៃ.error('អនុវត្ត_ពាក្យបញ្ជា 이름이 잘못되었거나 중복됨: ' + ឈ្មោះ)
        이름들.add(ឈ្មោះ)
        ទិន្នន័យ = Path(ផ្លូវ).read_bytes()
        if len(ទិន្នន័យ) > 2 * 1024 * 1024:
            ញែក_តំលៃ.error('អនុវត្ត_ពាក្យបញ្ជា 파일이 너무 큼')
        항목들.append((ឈ្មោះ.encode(), ទិន្នន័យ))
    ការវាស់វែង = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', ការវាស់វែង, 0, 0x50414b4a, len(항목들))
    for សន្ទស្សន៏, (ឈ្មោះ, ទិន្នន័យ) in enumerate(항목들):
        ការវាស់វែង.extend(bytes((-len(ការវាស់វែង)) % 16))
        struct.pack_into('<16sII', ការវាស់វែង, 8 + សន្ទស្សន៏ * 24, ឈ្មោះ, len(ការវាស់វែង), len(ទិន្នន័យ))
        ការវាស់វែង.extend(ទិន្នន័យ)
    Path(ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.o).write_bytes(ការវាស់វែង)

if __name__ == '__main__':
    묶기()

#!/usr/bin/env python3
"""명시한 Java ប្រភព_មែកធាង/ថ្នាក់_តំលៃ 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for ការបញ្ចូល_តំលៃ in 항목들:
        if '=' not in ការបញ្ចូល_តំលៃ:
            raise ValueError('expected NAME=PATH: ' + ការបញ្ចូល_តំលៃ)
        ឈ្មោះ, ផ្លូវ = ការបញ្ចូល_តំលៃ.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', ឈ្មោះ) or ឈ្មោះ in 명시:
            raise ValueError('invalid or duplicate file name: ' + ឈ្មោះ)
        명시.add(ឈ្មោះ)
        이름들.add(ឈ្មោះ)
        ទិន្នន័យ = Path(ផ្លូវ).read_bytes()
        if len(ទិន្នន័យ) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + ឈ្មោះ)
        파일들.append((ឈ្មោះ.encode('ascii'), ទិន្នន័យ))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    ការវាស់វែង = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    ការវាស់វែង.extend(bytes(72 * len(파일들)))
    for 수, (ឈ្មោះ, ទិន្នន័យ) in enumerate(파일들):
        struct.pack_into('<64sII', ការវាស់វែង, 8 + 수 * 72, ឈ្មោះ, len(ការវាស់វែង), len(ទិន្នន័យ))
        ការវាស់វែង.extend(ទិន្នន័យ)
    return bytes(ការវាស់វែង)


if __name__ == '__main__':
    ញែក_តំលៃ = argparse.ArgumentParser(description=__doc__)
    ញែក_តំលៃ.add_argument('-o', required=True)
    ញែក_តំលៃ.add_argument('files', nargs='*', help='NAME=PATH')
    អាគុយម៉ង់ = ញែក_តំលៃ.parse_args()
    try:
        ទិន្នន័យ = 묶기(អាគុយម៉ង់.files)
        ទិសដៅ_តំលៃ = Path(អាគុយម៉ង់.o)
        if not ទិសដៅ_តំលៃ.exists() or ទិសដៅ_តំលៃ.read_bytes() != ទិន្នន័យ:
            임시 = ទិសដៅ_តំលៃ.with_name(ទិសដៅ_តំលៃ.name + '.tmp')
            임시.write_bytes(ទិន្នន័យ)
            임시.replace(ទិសដៅ_តំលៃ)
    except (ValueError, OSError) as កំហុស:
        ញែក_តំលៃ.error(str(កំហុស))

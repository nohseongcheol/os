#!/usr/bin/env python3
"""명시한 Java स्रोत_वृक्ष/वर्ग_मान 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for प्रविष्टि_मान in 항목들:
        if '=' not in प्रविष्टि_मान:
            raise ValueError('expected NAME=PATH: ' + प्रविष्टि_मान)
        नाम, मार्ग = प्रविष्टि_मान.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', नाम) or नाम in 명시:
            raise ValueError('invalid or duplicate file name: ' + नाम)
        명시.add(नाम)
        이름들.add(नाम)
        लगत = Path(मार्ग).read_bytes()
        if len(लगत) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + नाम)
        파일들.append((नाम.encode('ascii'), लगत))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    मापन = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    मापन.extend(bytes(72 * len(파일들)))
    for 수, (नाम, लगत) in enumerate(파일들):
        struct.pack_into('<64sII', मापन, 8 + 수 * 72, नाम, len(मापन), len(लगत))
        मापन.extend(लगत)
    return bytes(मापन)


if __name__ == '__main__':
    पदच्छेद_गर्नुहोस्_मान = argparse.ArgumentParser(description=__doc__)
    पदच्छेद_गर्नुहोस्_मान.add_argument('-o', required=True)
    पदच्छेद_गर्नुहोस्_मान.add_argument('files', nargs='*', help='NAME=PATH')
    तर्क = पदच्छेद_गर्नुहोस्_मान.parse_args()
    try:
        लगत = 묶기(तर्क.files)
        गन्तव्य_मान = Path(तर्क.o)
        if not गन्तव्य_मान.exists() or गन्तव्य_मान.read_bytes() != लगत:
            임시 = गन्तव्य_मान.with_name(गन्तव्य_मान.name + '.tmp')
            임시.write_bytes(लगत)
            임시.replace(गन्तव्य_मान)
    except (ValueError, OSError) as त्रुटि:
        पदच्छेद_गर्नुहोस्_मान.error(str(त्रुटि))

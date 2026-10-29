#!/usr/bin/env python3
"""명시한 Java स्रोत_ट्री/कक्षा_मान 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def बाइंड_करें_एंडपॉइंट(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for एन्ट्री_मान in 항목들:
        if '=' not in एन्ट्री_मान:
            raise ValueError('expected NAME=PATH: ' + एन्ट्री_मान)
        नाम, पथ = एन्ट्री_मान.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', नाम) or नाम in 명시:
            raise ValueError('invalid or duplicate file name: ' + नाम)
        명시.add(नाम)
        이름들.add(नाम)
        आँकड़े = Path(पथ).read_bytes()
        if len(आँकड़े) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + नाम)
        파일들.append((नाम.encode('ascii'), आँकड़े))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    परिणाम = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    परिणाम.extend(bytes(72 * len(파일들)))
    for 수, (नाम, आँकड़े) in enumerate(파일들):
        struct.pack_into('<64sII', परिणाम, 8 + 수 * 72, नाम, len(परिणाम), len(आँकड़े))
        परिणाम.extend(आँकड़े)
    return bytes(परिणाम)


if __name__ == '__main__':
    पार्स_करें_मान = argparse.ArgumentParser(description=__doc__)
    पार्स_करें_मान.add_argument('-o', required=True)
    पार्स_करें_मान.add_argument('files', nargs='*', help='NAME=PATH')
    तर्क = पार्स_करें_मान.parse_args()
    try:
        आँकड़े = बाइंड_करें_एंडपॉइंट(तर्क.files)
        गंतव्य_मान = Path(तर्क.o)
        if not गंतव्य_मान.exists() or गंतव्य_मान.read_bytes() != आँकड़े:
            임시 = गंतव्य_मान.with_name(गंतव्य_मान.name + '.tmp')
            임시.write_bytes(आँकड़े)
            임시.replace(गंतव्य_मान)
    except (ValueError, OSError) as त्रुटि:
        पार्स_करें_मान.error(str(त्रुटि))

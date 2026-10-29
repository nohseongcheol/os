#!/usr/bin/env python3
"""명시한 उपयोगकर्ता ELF만 पढ़ें 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def बाइंड_करें_एंडपॉइंट():
    पार्स_करें_मान = argparse.ArgumentParser()
    पार्स_करें_मान.add_argument('-o', required=True)
    पार्स_करें_मान.add_argument('files', nargs='+', help='नाम=ELF경로')
    पैरामीटर_तर्क = पार्स_करें_मान.parse_args()
    if len(पैरामीटर_तर्क.files) > 32:
        पार्स_करें_मान.error('ऐप_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for एन्ट्री_मान in पैरामीटर_तर्क.files:
        नाम, पथ = एन्ट्री_मान.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', नाम) or नाम in 이름들:
            पार्स_करें_मान.error('निष्पादित_करें_आदेश 이름이 잘못되었거나 중복됨: ' + नाम)
        이름들.add(नाम)
        आँकड़े = Path(पथ).read_bytes()
        if len(आँकड़े) > 2 * 1024 * 1024:
            पार्स_करें_मान.error('निष्पादित_करें_आदेश 파일이 너무 큼')
        항목들.append((नाम.encode(), आँकड़े))
    परिणाम = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', परिणाम, 0, 0x50414b4a, len(항목들))
    for इंडेक्स, (नाम, आँकड़े) in enumerate(항목들):
        परिणाम.extend(bytes((-len(परिणाम)) % 16))
        struct.pack_into('<16sII', परिणाम, 8 + इंडेक्स * 24, नाम, len(परिणाम), len(आँकड़े))
        परिणाम.extend(आँकड़े)
    Path(पैरामीटर_तर्क.o).write_bytes(परिणाम)

if __name__ == '__main__':
    बाइंड_करें_एंडपॉइंट()

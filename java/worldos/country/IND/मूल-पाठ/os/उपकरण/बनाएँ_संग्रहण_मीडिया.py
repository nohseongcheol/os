#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 स्टोर_मान 매체를 만든다. 기존 संचिका/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def बनाएँ_एन्ट्री(पथ):
    with Path(पथ).open('xb') as निर्गम:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        निर्गम.write(머리)
        निर्गम.truncate(2048 * 512)

if __name__ == '__main__':
    पार्सर_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    पार्सर_48ee4b1b.add_argument('पथ')
    तर्क = पार्सर_48ee4b1b.parse_args()
    बनाएँ_एन्ट्री(तर्क.पथ)

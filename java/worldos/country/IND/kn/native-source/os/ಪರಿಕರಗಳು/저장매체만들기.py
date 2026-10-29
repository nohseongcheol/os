#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 ಸ್ಟೋರ್_ಮೌಲ್ಯ 매체를 만든다. 기존 ಕಡತ/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def ರಚಿಸು_ನಮೂದು(ಮಾರ್ಗ):
    with Path(ಮಾರ್ಗ).open('xb') as ಔಟ್_ಪುಟ್:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        ಔಟ್_ಪುಟ್.write(머리)
        ಔಟ್_ಪುಟ್.truncate(2048 * 512)

if __name__ == '__main__':
    ಪಾರ್ಸರ್_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ಪಾರ್ಸರ್_48ee4b1b.add_argument('ಮಾರ್ಗ')
    인수 = ಪಾರ್ಸರ್_48ee4b1b.parse_args()
    ರಚಿಸು_ನಮೂದು(인수.ಮಾರ್ಗ)

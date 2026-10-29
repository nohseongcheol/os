#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 சேகரி_மதிப்பு 매체를 만든다. 기존 கோப்பின்_பெயர்/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def உருவாக்கு_உள்ளீடு(பாதை_2):
    with Path(பாதை_2).open('xb') as வெளியீட்டு_இடம்:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        வெளியீட்டு_இடம்.write(머리)
        வெளியீட்டு_இடம்.truncate(2048 * 512)

if __name__ == '__main__':
    பார்சர்_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    பார்சர்_48ee4b1b.add_argument('பாதை_2')
    செயலுருபுகள் = பார்சர்_48ee4b1b.parse_args()
    உருவாக்கு_உள்ளீடு(செயலுருபுகள்.பாதை_2)

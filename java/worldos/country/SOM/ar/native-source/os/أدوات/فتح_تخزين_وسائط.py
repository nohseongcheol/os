#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 مخزن_قيمة 매체를 만든다. 기존 ملف/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def فتح_إدخال(مسار):
    with Path(مسار).open('xb') as مخرجات:
        رأس_قيمة = bytearray(512)
        struct.pack_into('<8sII', رأس_قيمة, 0, b'JKSTORE1', 2048, 0x3153464a)
        مخرجات.write(رأس_قيمة)
        مخرجات.truncate(2048 * 512)

if __name__ == '__main__':
    المحلل_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    المحلل_48ee4b1b.add_argument('مسار')
    وسائط = المحلل_48ee4b1b.parse_args()
    فتح_إدخال(وسائط.مسار)

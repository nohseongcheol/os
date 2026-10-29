#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 מאגר_ערך 매체를 만든다. 기존 קובץ/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def ליצור_ערך(נתיב):
    with Path(נתיב).open('xb') as פלטטקסט:
        ראש_ערך = bytearray(512)
        struct.pack_into('<8sII', ראש_ערך, 0, b'JKSTORE1', 2048, 0x3153464a)
        פלטטקסט.write(ראש_ערך)
        פלטטקסט.truncate(2048 * 512)

if __name__ == '__main__':
    מנתח_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    מנתח_48ee4b1b.add_argument('נתיב')
    ארגומנטים = מנתח_48ee4b1b.parse_args()
    ליצור_ערך(ארגומנטים.נתיב)

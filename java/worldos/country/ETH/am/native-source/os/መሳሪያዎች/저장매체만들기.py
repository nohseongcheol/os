#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 ማከማቻ_እሴት 매체를 만든다. 기존 ፋይል/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def ፍጠር_ምዝግብ(መተላለፊያ):
    with Path(መተላለፊያ).open('xb') as ውጤት:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        ውጤት.write(머리)
        ውጤት.truncate(2048 * 512)

if __name__ == '__main__':
    አግልሎ_ማስቀመጥ_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('መተላለፊያ')
    인수 = አግልሎ_ማስቀመጥ_48ee4b1b.parse_args()
    ፍጠር_ምዝግብ(인수.መተላለፊያ)

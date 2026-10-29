#!/usr/bin/env python3
"""명시한 ተጠቃሚ ELF만 ማንበቢያ 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    ተንትን_እሴት = argparse.ArgumentParser()
    ተንትን_እሴት.add_argument('-o', required=True)
    ተንትን_እሴት.add_argument('files', nargs='+', help='ስም=ELF경로')
    ግቤት_ነጋሪ_እሴት = ተንትን_እሴት.parse_args()
    if len(ግቤት_ነጋሪ_እሴት.files) > 32:
        ተንትን_እሴት.error('ፕሮግራም_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for ምዝግብ_እሴት in ግቤት_ነጋሪ_እሴት.files:
        ስም, መተላለፊያ = ምዝግብ_እሴት.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', ስም) or ስም in 이름들:
            ተንትን_እሴት.error('ፈጽም_ትእዛዝ 이름이 잘못되었거나 중복됨: ' + ስም)
        이름들.add(ስም)
        ውሂብ = Path(መተላለፊያ).read_bytes()
        if len(ውሂብ) > 2 * 1024 * 1024:
            ተንትን_እሴት.error('ፈጽም_ትእዛዝ 파일이 너무 큼')
        항목들.append((ስም.encode(), ውሂብ))
    ልኬት = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', ልኬት, 0, 0x50414b4a, len(항목들))
    for መረጃ_ጠቆመ, (ስም, ውሂብ) in enumerate(항목들):
        ልኬት.extend(bytes((-len(ልኬት)) % 16))
        struct.pack_into('<16sII', ልኬት, 8 + መረጃ_ጠቆመ * 24, ስም, len(ልኬት), len(ውሂብ))
        ልኬት.extend(ውሂብ)
    Path(ግቤት_ነጋሪ_እሴት.o).write_bytes(ልኬት)

if __name__ == '__main__':
    묶기()

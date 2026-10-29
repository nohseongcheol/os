#!/usr/bin/env python3
"""명시한 පරිශීලක ELF만 කියවීම 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    විශ්ලේෂණය_කරන්න_අගය = argparse.ArgumentParser()
    විශ්ලේෂණය_කරන්න_අගය.add_argument('-o', required=True)
    විශ්ලේෂණය_කරන්න_අගය.add_argument('files', nargs='+', help='නම=ELF경로')
    인자 = විශ්ලේෂණය_කරන්න_අගය.parse_args()
    if len(인자.files) > 32:
        විශ්ලේෂණය_කරන්න_අගය.error('යෙදු_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for පිවිසුම_අගය in 인자.files:
        නම, මාර්_ගය = පිවිසුම_අගය.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', නම) or නම in 이름들:
            විශ්ලේෂණය_කරන්න_අගය.error('ක්_රියාත්මක_කරන්න_විධානය 이름이 잘못되었거나 중복됨: ' + නම)
        이름들.add(නම)
        දත්ත = Path(මාර්_ගය).read_bytes()
        if len(දත්ත) > 2 * 1024 * 1024:
            විශ්ලේෂණය_කරන්න_අගය.error('ක්_රියාත්මක_කරන්න_විධානය 파일이 너무 큼')
        항목들.append((නම.encode(), දත්ත))
    결과 = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', 결과, 0, 0x50414b4a, len(항목들))
    for සූචිය, (නම, දත්ත) in enumerate(항목들):
        결과.extend(bytes((-len(결과)) % 16))
        struct.pack_into('<16sII', 결과, 8 + සූචිය * 24, නම, len(결과), len(දත්ත))
        결과.extend(දත්ත)
    Path(인자.o).write_bytes(결과)

if __name__ == '__main__':
    묶기()

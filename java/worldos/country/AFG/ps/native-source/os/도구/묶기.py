#!/usr/bin/env python3
"""명시한 کارن ELF만 لوستل 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    تجزیه_ارزښت = argparse.ArgumentParser()
    تجزیه_ارزښت.add_argument('-o', required=True)
    تجزیه_ارزښت.add_argument('files', nargs='+', help='نوم=ELF경로')
    인자 = تجزیه_ارزښت.parse_args()
    if len(인자.files) > 32:
        تجزیه_ارزښت.error('کاريال_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for ننوت_ارزښت in 인자.files:
        نوم, يونلور = ننوت_ارزښت.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', نوم) or نوم in 이름들:
            تجزیه_ارزښت.error('실행 이름이 잘못되었거나 중복됨: ' + نوم)
        이름들.add(نوم)
        اومتوک = Path(يونلور).read_bytes()
        if len(اومتوک) > 2 * 1024 * 1024:
            تجزیه_ارزښت.error('실행 파일이 너무 큼')
        항목들.append((نوم.encode(), اومتوک))
    결과 = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', 결과, 0, 0x50414b4a, len(항목들))
    for لړیال, (نوم, اومتوک) in enumerate(항목들):
        결과.extend(bytes((-len(결과)) % 16))
        struct.pack_into('<16sII', 결과, 8 + لړیال * 24, نوم, len(결과), len(اومتوک))
        결과.extend(اومتوک)
    Path(인자.o).write_bytes(결과)

if __name__ == '__main__':
    묶기()

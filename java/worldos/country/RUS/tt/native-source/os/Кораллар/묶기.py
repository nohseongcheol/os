#!/usr/bin/env python3
"""명시한 кулланучы ELF만 읽기 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    бүлү_VALUE = argparse.ArgumentParser()
    бүлү_VALUE.add_argument('-o', required=True)
    бүлү_VALUE.add_argument('files', nargs='+', help='исем=ELF경로')
    인자 = бүлү_VALUE.parse_args()
    if len(인자.files) > 32:
        бүлү_VALUE.error('кушымта_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for кертү_VALUE in 인자.files:
        исем, Yul = кертү_VALUE.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', исем) or исем in 이름들:
            бүлү_VALUE.error('үтәргә_команда 이름이 잘못되었거나 중복됨: ' + исем)
        이름들.add(исем)
        мәгълүмат = Path(Yul).read_bytes()
        if len(мәгълүмат) > 2 * 1024 * 1024:
            бүлү_VALUE.error('үтәргә_команда 파일이 너무 큼')
        항목들.append((исем.encode(), мәгълүмат))
    үлчәм = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', үлчәм, 0, 0x50414b4a, len(항목들))
    for INDEX, (исем, мәгълүмат) in enumerate(항목들):
        үлчәм.extend(bytes((-len(үлчәм)) % 16))
        struct.pack_into('<16sII', үлчәм, 8 + INDEX * 24, исем, len(үлчәм), len(мәгълүмат))
        үлчәм.extend(мәгълүмат)
    Path(인자.o).write_bytes(үлчәм)

if __name__ == '__main__':
    묶기()

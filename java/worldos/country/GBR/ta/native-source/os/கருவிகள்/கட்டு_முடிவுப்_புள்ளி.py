#!/usr/bin/env python3
"""명시한 பயனர் ELF만 படி 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def கட்டு_முடிவுப்_புள்ளி():
    அலகிடு_மதிப்பு = argparse.ArgumentParser()
    அலகிடு_மதிப்பு.add_argument('-o', required=True)
    அலகிடு_மதிப்பு.add_argument('files', nargs='+', help='பெயர்=ELF경로')
    அளவுரு_மதிப்புரு = அலகிடு_மதிப்பு.parse_args()
    if len(அளவுரு_மதிப்புரு.files) > 32:
        அலகிடு_மதிப்பு.error('நிரல்_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for உள்ளீடு_மதிப்பு in அளவுரு_மதிப்புரு.files:
        பெயர், பாதை_2 = உள்ளீடு_மதிப்பு.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', பெயர்) or பெயர் in 이름들:
            அலகிடு_மதிப்பு.error('இயக்கு_கட்டளை 이름이 잘못되었거나 중복됨: ' + பெயர்)
        이름들.add(பெயர்)
        தரவு = Path(பாதை_2).read_bytes()
        if len(தரவு) > 2 * 1024 * 1024:
            அலகிடு_மதிப்பு.error('இயக்கு_கட்டளை 파일이 너무 큼')
        항목들.append((பெயர்.encode(), தரவு))
    அளவிடக்கூடியது = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', அளவிடக்கூடியது, 0, 0x50414b4a, len(항목들))
    for அடைவு, (பெயர், தரவு) in enumerate(항목들):
        அளவிடக்கூடியது.extend(bytes((-len(அளவிடக்கூடியது)) % 16))
        struct.pack_into('<16sII', அளவிடக்கூடியது, 8 + அடைவு * 24, பெயர், len(அளவிடக்கூடியது), len(தரவு))
        அளவிடக்கூடியது.extend(தரவு)
    Path(அளவுரு_மதிப்புரு.o).write_bytes(அளவிடக்கூடியது)

if __name__ == '__main__':
    கட்டு_முடிவுப்_புள்ளி()

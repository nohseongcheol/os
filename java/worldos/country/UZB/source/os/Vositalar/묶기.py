#!/usr/bin/env python3
"""명시한 foydalanuvchi ELF만 Oʻqish 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    tahlil_qilmoq_VALUE = argparse.ArgumentParser()
    tahlil_qilmoq_VALUE.add_argument('-o', required=True)
    tahlil_qilmoq_VALUE.add_argument('files', nargs='+', help='Nomi=ELF경로')
    인자 = tahlil_qilmoq_VALUE.parse_args()
    if len(인자.files) > 32:
        tahlil_qilmoq_VALUE.error('ilova_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for kiritish_VALUE in 인자.files:
        Nomi, yo_l = kiritish_VALUE.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Nomi) or Nomi in 이름들:
            tahlil_qilmoq_VALUE.error('bajarmoq_buyruq 이름이 잘못되었거나 중복됨: ' + Nomi)
        이름들.add(Nomi)
        ma_lumotlar = Path(yo_l).read_bytes()
        if len(ma_lumotlar) > 2 * 1024 * 1024:
            tahlil_qilmoq_VALUE.error('bajarmoq_buyruq 파일이 너무 큼')
        항목들.append((Nomi.encode(), ma_lumotlar))
    o_lchov = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', o_lchov, 0, 0x50414b4a, len(항목들))
    for INDEX, (Nomi, ma_lumotlar) in enumerate(항목들):
        o_lchov.extend(bytes((-len(o_lchov)) % 16))
        struct.pack_into('<16sII', o_lchov, 8 + INDEX * 24, Nomi, len(o_lchov), len(ma_lumotlar))
        o_lchov.extend(ma_lumotlar)
    Path(인자.o).write_bytes(o_lchov)

if __name__ == '__main__':
    묶기()

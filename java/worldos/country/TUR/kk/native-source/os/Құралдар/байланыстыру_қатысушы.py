#!/usr/bin/env python3
"""명시한 пайдаланушы ELF만 Оқу 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def байланыстыру_қатысушы():
    талдау_мән = argparse.ArgumentParser()
    талдау_мән.add_argument('-o', required=True)
    талдау_мән.add_argument('files', nargs='+', help='Аты=ELF경로')
    параметр_аргумент = талдау_мән.parse_args()
    if len(параметр_аргумент.files) > 32:
        талдау_мән.error('бағдарлама_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for енгізу_мән in параметр_аргумент.files:
        Аты, Жол_2 = енгізу_мән.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Аты) or Аты in 이름들:
            талдау_мән.error('орындау_пәрмен 이름이 잘못되었거나 중복됨: ' + Аты)
        이름들.add(Аты)
        деректер = Path(Жол_2).read_bytes()
        if len(деректер) > 2 * 1024 * 1024:
            талдау_мән.error('орындау_пәрмен 파일이 너무 큼')
        항목들.append((Аты.encode(), деректер))
    НӘТИЖЕ = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', НӘТИЖЕ, 0, 0x50414b4a, len(항목들))
    for индекс, (Аты, деректер) in enumerate(항목들):
        НӘТИЖЕ.extend(bytes((-len(НӘТИЖЕ)) % 16))
        struct.pack_into('<16sII', НӘТИЖЕ, 8 + индекс * 24, Аты, len(НӘТИЖЕ), len(деректер))
        НӘТИЖЕ.extend(деректер)
    Path(параметр_аргумент.o).write_bytes(НӘТИЖЕ)

if __name__ == '__main__':
    байланыстыру_қатысушы()

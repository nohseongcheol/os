#!/usr/bin/env python3
"""명시한 корисник ELF만 Читај 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    разложи_VALUE = argparse.ArgumentParser()
    разложи_VALUE.add_argument('-o', required=True)
    разложи_VALUE.add_argument('files', nargs='+', help='Име=ELF경로')
    параметар_аргумент = разложи_VALUE.parse_args()
    if len(параметар_аргумент.files) > 32:
        разложи_VALUE.error('програма_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for внес_VALUE in параметар_аргумент.files:
        Име, ПАТЕКА = внес_VALUE.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Име) or Име in 이름들:
            разложи_VALUE.error('Изврши_наредба 이름이 잘못되었거나 중복됨: ' + Име)
        이름들.add(Име)
        податоци = Path(ПАТЕКА).read_bytes()
        if len(податоци) > 2 * 1024 * 1024:
            разложи_VALUE.error('Изврши_наредба 파일이 너무 큼')
        항목들.append((Име.encode(), податоци))
    мерка = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', мерка, 0, 0x50414b4a, len(항목들))
    for INDEX, (Име, податоци) in enumerate(항목들):
        мерка.extend(bytes((-len(мерка)) % 16))
        struct.pack_into('<16sII', мерка, 8 + INDEX * 24, Име, len(мерка), len(податоци))
        мерка.extend(податоци)
    Path(параметар_аргумент.o).write_bytes(мерка)

if __name__ == '__main__':
    묶기()

#!/usr/bin/env python3
"""명시한 Java извор_дрво/класа_VALUE 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for внес_VALUE in 항목들:
        if '=' not in внес_VALUE:
            raise ValueError('expected NAME=PATH: ' + внес_VALUE)
        Име, ПАТЕКА = внес_VALUE.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Име) or Име in 명시:
            raise ValueError('invalid or duplicate file name: ' + Име)
        명시.add(Име)
        이름들.add(Име)
        податоци = Path(ПАТЕКА).read_bytes()
        if len(податоци) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Име)
        파일들.append((Име.encode('ascii'), податоци))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    мерка = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    мерка.extend(bytes(72 * len(파일들)))
    for 수, (Име, податоци) in enumerate(파일들):
        struct.pack_into('<64sII', мерка, 8 + 수 * 72, Име, len(мерка), len(податоци))
        мерка.extend(податоци)
    return bytes(мерка)


if __name__ == '__main__':
    разложи_VALUE = argparse.ArgumentParser(description=__doc__)
    разложи_VALUE.add_argument('-o', required=True)
    разложи_VALUE.add_argument('files', nargs='*', help='NAME=PATH')
    Аргументи = разложи_VALUE.parse_args()
    try:
        податоци = 묶기(Аргументи.files)
        одредиште_VALUE = Path(Аргументи.o)
        if not одредиште_VALUE.exists() or одредиште_VALUE.read_bytes() != податоци:
            임시 = одредиште_VALUE.with_name(одредиште_VALUE.name + '.tmp')
            임시.write_bytes(податоци)
            임시.replace(одредиште_VALUE)
    except (ValueError, OSError) as ГРЕШКА:
        разложи_VALUE.error(str(ГРЕШКА))

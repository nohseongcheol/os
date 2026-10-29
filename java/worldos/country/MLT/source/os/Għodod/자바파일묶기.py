#!/usr/bin/env python3
"""명시한 Java sors_siġra/klassi_VALUE 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for entrata_VALUE in 항목들:
        if '=' not in entrata_VALUE:
            raise ValueError('expected NAME=PATH: ' + entrata_VALUE)
        isem, mogħdija = entrata_VALUE.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', isem) or isem in 명시:
            raise ValueError('invalid or duplicate file name: ' + isem)
        명시.add(isem)
        이름들.add(isem)
        data = Path(mogħdija).read_bytes()
        if len(data) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + isem)
        파일들.append((isem.encode('ascii'), data))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    miżura = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    miżura.extend(bytes(72 * len(파일들)))
    for 수, (isem, data) in enumerate(파일들):
        struct.pack_into('<64sII', miżura, 8 + 수 * 72, isem, len(miżura), len(data))
        miżura.extend(data)
    return bytes(miżura)


if __name__ == '__main__':
    analizza_VALUE = argparse.ArgumentParser(description=__doc__)
    analizza_VALUE.add_argument('-o', required=True)
    analizza_VALUE.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = analizza_VALUE.parse_args()
    try:
        data = 묶기(인수.files)
        destinazzjoni_VALUE = Path(인수.o)
        if not destinazzjoni_VALUE.exists() or destinazzjoni_VALUE.read_bytes() != data:
            임시 = destinazzjoni_VALUE.with_name(destinazzjoni_VALUE.name + '.tmp')
            임시.write_bytes(data)
            임시.replace(destinazzjoni_VALUE)
    except (ValueError, OSError) as żball:
        analizza_VALUE.error(str(żball))

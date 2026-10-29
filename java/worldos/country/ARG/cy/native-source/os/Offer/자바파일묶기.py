#!/usr/bin/env python3
"""명시한 Java ffynhonnell_coeden/Dosbarth_VALUE 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for cofnod_VALUE in 항목들:
        if '=' not in cofnod_VALUE:
            raise ValueError('expected NAME=PATH: ' + cofnod_VALUE)
        Enw, LLWYBR = cofnod_VALUE.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Enw) or Enw in 명시:
            raise ValueError('invalid or duplicate file name: ' + Enw)
        명시.add(Enw)
        이름들.add(Enw)
        data = Path(LLWYBR).read_bytes()
        if len(data) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Enw)
        파일들.append((Enw.encode('ascii'), data))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    mesur = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    mesur.extend(bytes(72 * len(파일들)))
    for 수, (Enw, data) in enumerate(파일들):
        struct.pack_into('<64sII', mesur, 8 + 수 * 72, Enw, len(mesur), len(data))
        mesur.extend(data)
    return bytes(mesur)


if __name__ == '__main__':
    dosrannu_VALUE = argparse.ArgumentParser(description=__doc__)
    dosrannu_VALUE.add_argument('-o', required=True)
    dosrannu_VALUE.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = dosrannu_VALUE.parse_args()
    try:
        data = 묶기(인수.files)
        cyrchfan_VALUE = Path(인수.o)
        if not cyrchfan_VALUE.exists() or cyrchfan_VALUE.read_bytes() != data:
            임시 = cyrchfan_VALUE.with_name(cyrchfan_VALUE.name + '.tmp')
            임시.write_bytes(data)
            임시.replace(cyrchfan_VALUE)
    except (ValueError, OSError) as Gwall:
        dosrannu_VALUE.error(str(Gwall))

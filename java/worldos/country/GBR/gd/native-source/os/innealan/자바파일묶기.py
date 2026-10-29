#!/usr/bin/env python3
"""명시한 Java tùs_craobh/clas_VALUE 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for cur_a_steach_VALUE in 항목들:
        if '=' not in cur_a_steach_VALUE:
            raise ValueError('expected NAME=PATH: ' + cur_a_steach_VALUE)
        Ainm, Slighe = cur_a_steach_VALUE.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Ainm) or Ainm in 명시:
            raise ValueError('invalid or duplicate file name: ' + Ainm)
        명시.add(Ainm)
        이름들.add(Ainm)
        dàta = Path(Slighe).read_bytes()
        if len(dàta) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Ainm)
        파일들.append((Ainm.encode('ascii'), dàta))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    tomhas = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    tomhas.extend(bytes(72 * len(파일들)))
    for 수, (Ainm, dàta) in enumerate(파일들):
        struct.pack_into('<64sII', tomhas, 8 + 수 * 72, Ainm, len(tomhas), len(dàta))
        tomhas.extend(dàta)
    return bytes(tomhas)


if __name__ == '__main__':
    해석 = argparse.ArgumentParser(description=__doc__)
    해석.add_argument('-o', required=True)
    해석.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = 해석.parse_args()
    try:
        dàta = 묶기(인수.files)
        ceann_uidhe_VALUE = Path(인수.o)
        if not ceann_uidhe_VALUE.exists() or ceann_uidhe_VALUE.read_bytes() != dàta:
            임시 = ceann_uidhe_VALUE.with_name(ceann_uidhe_VALUE.name + '.tmp')
            임시.write_bytes(dàta)
            임시.replace(ceann_uidhe_VALUE)
    except (ValueError, OSError) as Mearachd:
        해석.error(str(Mearachd))

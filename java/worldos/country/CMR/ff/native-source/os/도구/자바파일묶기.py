#!/usr/bin/env python3
"""명시한 Java sewnde_lekki/fedde_njaru 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for naatnugol_njaru in 항목들:
        if '=' not in naatnugol_njaru:
            raise ValueError('expected NAME=PATH: ' + naatnugol_njaru)
        innde, laawol = naatnugol_njaru.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', innde) or innde in 명시:
            raise ValueError('invalid or duplicate file name: ' + innde)
        명시.add(innde)
        이름들.add(innde)
        keɓe = Path(laawol).read_bytes()
        if len(keɓe) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + innde)
        파일들.append((innde.encode('ascii'), keɓe))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    결과 = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    결과.extend(bytes(72 * len(파일들)))
    for 수, (innde, keɓe) in enumerate(파일들):
        struct.pack_into('<64sII', 결과, 8 + 수 * 72, innde, len(결과), len(keɓe))
        결과.extend(keɓe)
    return bytes(결과)


if __name__ == '__main__':
    해석 = argparse.ArgumentParser(description=__doc__)
    해석.add_argument('-o', required=True)
    해석.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = 해석.parse_args()
    try:
        keɓe = 묶기(인수.files)
        tiindaare_njaru = Path(인수.o)
        if not tiindaare_njaru.exists() or tiindaare_njaru.read_bytes() != keɓe:
            임시 = tiindaare_njaru.with_name(tiindaare_njaru.name + '.tmp')
            임시.write_bytes(keɓe)
            임시.replace(tiindaare_njaru)
    except (ValueError, OSError) as juumre:
        해석.error(str(juumre))

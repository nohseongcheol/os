#!/usr/bin/env python3
"""명시한 Java манбаъ_дарахт/синф_қимат 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for ворида_қимат in 항목들:
        if '=' not in ворида_қимат:
            raise ValueError('expected NAME=PATH: ' + ворида_қимат)
        Ном, масир = ворида_қимат.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Ном) or Ном in 명시:
            raise ValueError('invalid or duplicate file name: ' + Ном)
        명시.add(Ном)
        이름들.add(Ном)
        иттилоот = Path(масир).read_bytes()
        if len(иттилоот) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Ном)
        파일들.append((Ном.encode('ascii'), иттилоот))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    결과 = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    결과.extend(bytes(72 * len(파일들)))
    for 수, (Ном, иттилоот) in enumerate(파일들):
        struct.pack_into('<64sII', 결과, 8 + 수 * 72, Ном, len(결과), len(иттилоот))
        결과.extend(иттилоот)
    return bytes(결과)


if __name__ == '__main__':
    해석 = argparse.ArgumentParser(description=__doc__)
    해석.add_argument('-o', required=True)
    해석.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = 해석.parse_args()
    try:
        иттилоот = 묶기(인수.files)
        ҷои_таъинот_қимат = Path(인수.o)
        if not ҷои_таъинот_қимат.exists() or ҷои_таъинот_қимат.read_bytes() != иттилоот:
            임시 = ҷои_таъинот_қимат.with_name(ҷои_таъинот_қимат.name + '.tmp')
            임시.write_bytes(иттилоот)
            임시.replace(ҷои_таъинот_қимат)
    except (ValueError, OSError) as Хато:
        해석.error(str(Хато))

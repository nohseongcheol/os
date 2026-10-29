#!/usr/bin/env python3
"""명시한 Java pūtake_rākau/tauaha_uara 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for tāurunga_uara in 항목들:
        if '=' not in tāurunga_uara:
            raise ValueError('expected NAME=PATH: ' + tāurunga_uara)
        Ingoa, ara = tāurunga_uara.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Ingoa) or Ingoa in 명시:
            raise ValueError('invalid or duplicate file name: ' + Ingoa)
        명시.add(Ingoa)
        이름들.add(Ingoa)
        raraunga = Path(ara).read_bytes()
        if len(raraunga) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Ingoa)
        파일들.append((Ingoa.encode('ascii'), raraunga))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    mēhua = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    mēhua.extend(bytes(72 * len(파일들)))
    for 수, (Ingoa, raraunga) in enumerate(파일들):
        struct.pack_into('<64sII', mēhua, 8 + 수 * 72, Ingoa, len(mēhua), len(raraunga))
        mēhua.extend(raraunga)
    return bytes(mēhua)


if __name__ == '__main__':
    poroporo_uara = argparse.ArgumentParser(description=__doc__)
    poroporo_uara.add_argument('-o', required=True)
    poroporo_uara.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = poroporo_uara.parse_args()
    try:
        raraunga = 묶기(인수.files)
        ūnga_uara = Path(인수.o)
        if not ūnga_uara.exists() or ūnga_uara.read_bytes() != raraunga:
            임시 = ūnga_uara.with_name(ūnga_uara.name + '.tmp')
            임시.write_bytes(raraunga)
            임시.replace(ūnga_uara)
    except (ValueError, OSError) as Pōhēhē:
        poroporo_uara.error(str(Pōhēhē))

#!/usr/bin/env python3
"""명시한 Java manba_daraxt/Sinf_VALUE 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for kiritish_VALUE in 항목들:
        if '=' not in kiritish_VALUE:
            raise ValueError('expected NAME=PATH: ' + kiritish_VALUE)
        Nomi, yo_l = kiritish_VALUE.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Nomi) or Nomi in 명시:
            raise ValueError('invalid or duplicate file name: ' + Nomi)
        명시.add(Nomi)
        이름들.add(Nomi)
        ma_lumotlar = Path(yo_l).read_bytes()
        if len(ma_lumotlar) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Nomi)
        파일들.append((Nomi.encode('ascii'), ma_lumotlar))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    o_lchov = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    o_lchov.extend(bytes(72 * len(파일들)))
    for 수, (Nomi, ma_lumotlar) in enumerate(파일들):
        struct.pack_into('<64sII', o_lchov, 8 + 수 * 72, Nomi, len(o_lchov), len(ma_lumotlar))
        o_lchov.extend(ma_lumotlar)
    return bytes(o_lchov)


if __name__ == '__main__':
    tahlil_qilmoq_VALUE = argparse.ArgumentParser(description=__doc__)
    tahlil_qilmoq_VALUE.add_argument('-o', required=True)
    tahlil_qilmoq_VALUE.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = tahlil_qilmoq_VALUE.parse_args()
    try:
        ma_lumotlar = 묶기(인수.files)
        ko_chirish_joyi_VALUE = Path(인수.o)
        if not ko_chirish_joyi_VALUE.exists() or ko_chirish_joyi_VALUE.read_bytes() != ma_lumotlar:
            임시 = ko_chirish_joyi_VALUE.with_name(ko_chirish_joyi_VALUE.name + '.tmp')
            임시.write_bytes(ma_lumotlar)
            임시.replace(ko_chirish_joyi_VALUE)
    except (ValueError, OSError) as Xato:
        tahlil_qilmoq_VALUE.error(str(Xato))

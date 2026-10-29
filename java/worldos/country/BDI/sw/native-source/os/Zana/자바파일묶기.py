#!/usr/bin/env python3
"""명시한 Java chanzo_mti/tabaka_thamani_55654bf1 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for ingizo_thamani in 항목들:
        if '=' not in ingizo_thamani:
            raise ValueError('expected NAME=PATH: ' + ingizo_thamani)
        Jina, njia = ingizo_thamani.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Jina) or Jina in 명시:
            raise ValueError('invalid or duplicate file name: ' + Jina)
        명시.add(Jina)
        이름들.add(Jina)
        data = Path(njia).read_bytes()
        if len(data) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Jina)
        파일들.append((Jina.encode('ascii'), data))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    결과 = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    결과.extend(bytes(72 * len(파일들)))
    for 수, (Jina, data) in enumerate(파일들):
        struct.pack_into('<64sII', 결과, 8 + 수 * 72, Jina, len(결과), len(data))
        결과.extend(data)
    return bytes(결과)


if __name__ == '__main__':
    changanua_thamani = argparse.ArgumentParser(description=__doc__)
    changanua_thamani.add_argument('-o', required=True)
    changanua_thamani.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = changanua_thamani.parse_args()
    try:
        data = 묶기(인수.files)
        fikio_thamani = Path(인수.o)
        if not fikio_thamani.exists() or fikio_thamani.read_bytes() != data:
            임시 = fikio_thamani.with_name(fikio_thamani.name + '.tmp')
            임시.write_bytes(data)
            임시.replace(fikio_thamani)
    except (ValueError, OSError) as kosa:
        changanua_thamani.error(str(kosa))

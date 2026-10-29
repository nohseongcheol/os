#!/usr/bin/env python3
"""명시한 Java Cosaan_tëralinuy_pàcc/maas_xëyma 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for dugal_xabaar_xëyma in 항목들:
        if '=' not in dugal_xabaar_xëyma:
            raise ValueError('expected NAME=PATH: ' + dugal_xabaar_xëyma)
        tur_253d1510, Yoonu_jëmale = dugal_xabaar_xëyma.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', tur_253d1510) or tur_253d1510 in 명시:
            raise ValueError('invalid or duplicate file name: ' + tur_253d1510)
        명시.add(tur_253d1510)
        이름들.add(tur_253d1510)
        mbir = Path(Yoonu_jëmale).read_bytes()
        if len(mbir) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + tur_253d1510)
        파일들.append((tur_253d1510.encode('ascii'), mbir))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    결과 = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    결과.extend(bytes(72 * len(파일들)))
    for 수, (tur_253d1510, mbir) in enumerate(파일들):
        struct.pack_into('<64sII', 결과, 8 + 수 * 72, tur_253d1510, len(결과), len(mbir))
        결과.extend(mbir)
    return bytes(결과)


if __name__ == '__main__':
    Segg_xëyma = argparse.ArgumentParser(description=__doc__)
    Segg_xëyma.add_argument('-o', required=True)
    Segg_xëyma.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = Segg_xëyma.parse_args()
    try:
        mbir = 묶기(인수.files)
        jëmmukaay_xëyma = Path(인수.o)
        if not jëmmukaay_xëyma.exists() or jëmmukaay_xëyma.read_bytes() != mbir:
            임시 = jëmmukaay_xëyma.with_name(jëmmukaay_xëyma.name + '.tmp')
            임시.write_bytes(mbir)
            임시.replace(jëmmukaay_xëyma)
    except (ValueError, OSError) as njumte:
        Segg_xëyma.error(str(njumte))

#!/usr/bin/env python3
"""명시한 Java kilde_træ/Hold_VÆRDI 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def BIND_slutpunkt(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for post_VÆRDI_962f286b in 항목들:
        if '=' not in post_VÆRDI_962f286b:
            raise ValueError('expected NAME=PATH: ' + post_VÆRDI_962f286b)
        Navn, Sti = post_VÆRDI_962f286b.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Navn) or Navn in 명시:
            raise ValueError('invalid or duplicate file name: ' + Navn)
        명시.add(Navn)
        이름들.add(Navn)
        data = Path(Sti).read_bytes()
        if len(data) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Navn)
        파일들.append((Navn.encode('ascii'), data))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    KR = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    KR.extend(bytes(72 * len(파일들)))
    for tal, (Navn, data) in enumerate(파일들):
        struct.pack_into('<64sII', KR, 8 + tal * 72, Navn, len(KR), len(data))
        KR.extend(data)
    return bytes(KR)


if __name__ == '__main__':
    opdele_tekst_VÆRDI = argparse.ArgumentParser(description=__doc__)
    opdele_tekst_VÆRDI.add_argument('-o', required=True)
    opdele_tekst_VÆRDI.add_argument('files', nargs='*', help='NAME=PATH')
    Argumenter = opdele_tekst_VÆRDI.parse_args()
    try:
        data = BIND_slutpunkt(Argumenter.files)
        destination_VÆRDI = Path(Argumenter.o)
        if not destination_VÆRDI.exists() or destination_VÆRDI.read_bytes() != data:
            임시 = destination_VÆRDI.with_name(destination_VÆRDI.name + '.tmp')
            임시.write_bytes(data)
            임시.replace(destination_VÆRDI)
    except (ValueError, OSError) as fejl:
        opdele_tekst_VÆRDI.error(str(fejl))

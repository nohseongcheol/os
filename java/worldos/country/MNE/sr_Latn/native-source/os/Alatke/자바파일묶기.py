#!/usr/bin/env python3
"""명시한 Java izvor_stablo/Razred_VALUE 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def povezati_učesnik(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for stavka_VALUE in 항목들:
        if '=' not in stavka_VALUE:
            raise ValueError('expected NAME=PATH: ' + stavka_VALUE)
        ime, putanja = stavka_VALUE.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', ime) or ime in 명시:
            raise ValueError('invalid or duplicate file name: ' + ime)
        명시.add(ime)
        이름들.add(ime)
        podaci = Path(putanja).read_bytes()
        if len(podaci) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + ime)
        파일들.append((ime.encode('ascii'), podaci))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    KR = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    KR.extend(bytes(72 * len(파일들)))
    for 수, (ime, podaci) in enumerate(파일들):
        struct.pack_into('<64sII', KR, 8 + 수 * 72, ime, len(KR), len(podaci))
        KR.extend(podaci)
    return bytes(KR)


if __name__ == '__main__':
    raščlaniti_VALUE = argparse.ArgumentParser(description=__doc__)
    raščlaniti_VALUE.add_argument('-o', required=True)
    raščlaniti_VALUE.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = raščlaniti_VALUE.parse_args()
    try:
        podaci = povezati_učesnik(인수.files)
        odredište_VALUE = Path(인수.o)
        if not odredište_VALUE.exists() or odredište_VALUE.read_bytes() != podaci:
            임시 = odredište_VALUE.with_name(odredište_VALUE.name + '.tmp')
            임시.write_bytes(podaci)
            임시.replace(odredište_VALUE)
    except (ValueError, OSError) as greška:
        raščlaniti_VALUE.error(str(greška))

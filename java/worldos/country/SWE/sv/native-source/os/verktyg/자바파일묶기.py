#!/usr/bin/env python3
"""명시한 Java källa_träd/Kurs_värde 파일을 maskinstart 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def BIND_deltagare(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for post_värde in 항목들:
        if '=' not in post_värde:
            raise ValueError('expected NAME=PATH: ' + post_värde)
        Namn, sökväg_2 = post_värde.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Namn) or Namn in 명시:
            raise ValueError('invalid or duplicate file name: ' + Namn)
        명시.add(Namn)
        이름들.add(Namn)
        data = Path(sökväg_2).read_bytes()
        if len(data) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Namn)
        파일들.append((Namn.encode('ascii'), data))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    RESULTAT = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    RESULTAT.extend(bytes(72 * len(파일들)))
    for nummer, (Namn, data) in enumerate(파일들):
        struct.pack_into('<64sII', RESULTAT, 8 + nummer * 72, Namn, len(RESULTAT), len(data))
        RESULTAT.extend(data)
    return bytes(RESULTAT)


if __name__ == '__main__':
    parsa_värde = argparse.ArgumentParser(description=__doc__)
    parsa_värde.add_argument('-o', required=True)
    parsa_värde.add_argument('files', nargs='*', help='NAME=PATH')
    argument = parsa_värde.parse_args()
    try:
        data = BIND_deltagare(argument.files)
        mål_värde = Path(argument.o)
        if not mål_värde.exists() or mål_värde.read_bytes() != data:
            임시 = mål_värde.with_name(mål_värde.name + '.tmp')
            임시.write_bytes(data)
            임시.replace(mål_värde)
    except (ValueError, OSError) as fel:
        parsa_värde.error(str(fel))

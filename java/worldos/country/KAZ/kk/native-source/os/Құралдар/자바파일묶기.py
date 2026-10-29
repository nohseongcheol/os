#!/usr/bin/env python3
"""명시한 Java көз_дарақ/оқу_мән 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def байланыстыру_қатысушы(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for енгізу_мән in 항목들:
        if '=' not in енгізу_мән:
            raise ValueError('expected NAME=PATH: ' + енгізу_мән)
        Аты, Жол_2 = енгізу_мән.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Аты) or Аты in 명시:
            raise ValueError('invalid or duplicate file name: ' + Аты)
        명시.add(Аты)
        이름들.add(Аты)
        деректер = Path(Жол_2).read_bytes()
        if len(деректер) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Аты)
        파일들.append((Аты.encode('ascii'), деректер))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    НӘТИЖЕ = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    НӘТИЖЕ.extend(bytes(72 * len(파일들)))
    for 수, (Аты, деректер) in enumerate(파일들):
        struct.pack_into('<64sII', НӘТИЖЕ, 8 + 수 * 72, Аты, len(НӘТИЖЕ), len(деректер))
        НӘТИЖЕ.extend(деректер)
    return bytes(НӘТИЖЕ)


if __name__ == '__main__':
    талдау_мән = argparse.ArgumentParser(description=__doc__)
    талдау_мән.add_argument('-o', required=True)
    талдау_мән.add_argument('files', nargs='*', help='NAME=PATH')
    Аргументтер = талдау_мән.parse_args()
    try:
        деректер = байланыстыру_қатысушы(Аргументтер.files)
        тағайындау_мән = Path(Аргументтер.o)
        if not тағайындау_мән.exists() or тағайындау_мән.read_bytes() != деректер:
            임시 = тағайындау_мән.with_name(тағайындау_мән.name + '.tmp')
            임시.write_bytes(деректер)
            임시.replace(тағайындау_мән)
    except (ValueError, OSError) as Қате:
        талдау_мән.error(str(Қате))

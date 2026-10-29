#!/usr/bin/env python3
"""명시한 Java προέλευση_δέντρο/Τάξη_τιμή 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def συνδέω_τελικό_σημείο_bbe6b410(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for καταχώρηση_τιμή in 항목들:
        if '=' not in καταχώρηση_τιμή:
            raise ValueError('expected NAME=PATH: ' + καταχώρηση_τιμή)
        Όνομα, ΔΙΑΔΡΟΜΗ = καταχώρηση_τιμή.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Όνομα) or Όνομα in 명시:
            raise ValueError('invalid or duplicate file name: ' + Όνομα)
        명시.add(Όνομα)
        이름들.add(Όνομα)
        δεδομένα = Path(ΔΙΑΔΡΟΜΗ).read_bytes()
        if len(δεδομένα) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Όνομα)
        파일들.append((Όνομα.encode('ascii'), δεδομένα))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    μέτρηση = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    μέτρηση.extend(bytes(72 * len(파일들)))
    for 수, (Όνομα, δεδομένα) in enumerate(파일들):
        struct.pack_into('<64sII', μέτρηση, 8 + 수 * 72, Όνομα, len(μέτρηση), len(δεδομένα))
        μέτρηση.extend(δεδομένα)
    return bytes(μέτρηση)


if __name__ == '__main__':
    ανάλυση_τιμή_7cebddfb = argparse.ArgumentParser(description=__doc__)
    ανάλυση_τιμή_7cebddfb.add_argument('-o', required=True)
    ανάλυση_τιμή_7cebddfb.add_argument('files', nargs='*', help='NAME=PATH')
    Παράμετροι = ανάλυση_τιμή_7cebddfb.parse_args()
    try:
        δεδομένα = συνδέω_τελικό_σημείο_bbe6b410(Παράμετροι.files)
        προορισμός_τιμή = Path(Παράμετροι.o)
        if not προορισμός_τιμή.exists() or προορισμός_τιμή.read_bytes() != δεδομένα:
            임시 = προορισμός_τιμή.with_name(προορισμός_τιμή.name + '.tmp')
            임시.write_bytes(δεδομένα)
            임시.replace(προορισμός_τιμή)
    except (ValueError, OSError) as ΣΦΑΛΜΑ:
        ανάλυση_τιμή_7cebddfb.error(str(ΣΦΑΛΜΑ))

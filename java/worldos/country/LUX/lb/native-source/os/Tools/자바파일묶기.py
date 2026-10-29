#!/usr/bin/env python3
"""명시한 Java Quell_Bamstruktur/Klass_VALUE 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for Agab_VALUE in 항목들:
        if '=' not in Agab_VALUE:
            raise ValueError('expected NAME=PATH: ' + Agab_VALUE)
        Numm, Wee = Agab_VALUE.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Numm) or Numm in 명시:
            raise ValueError('invalid or duplicate file name: ' + Numm)
        명시.add(Numm)
        이름들.add(Numm)
        Daten = Path(Wee).read_bytes()
        if len(Daten) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Numm)
        파일들.append((Numm.encode('ascii'), Daten))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    Mooss = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    Mooss.extend(bytes(72 * len(파일들)))
    for 수, (Numm, Daten) in enumerate(파일들):
        struct.pack_into('<64sII', Mooss, 8 + 수 * 72, Numm, len(Mooss), len(Daten))
        Mooss.extend(Daten)
    return bytes(Mooss)


if __name__ == '__main__':
    analyséieren_VALUE = argparse.ArgumentParser(description=__doc__)
    analyséieren_VALUE.add_argument('-o', required=True)
    analyséieren_VALUE.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = analyséieren_VALUE.parse_args()
    try:
        Daten = 묶기(인수.files)
        Zil_VALUE = Path(인수.o)
        if not Zil_VALUE.exists() or Zil_VALUE.read_bytes() != Daten:
            임시 = Zil_VALUE.with_name(Zil_VALUE.name + '.tmp')
            임시.write_bytes(Daten)
            임시.replace(Zil_VALUE)
    except (ValueError, OSError) as Feeler:
        analyséieren_VALUE.error(str(Feeler))

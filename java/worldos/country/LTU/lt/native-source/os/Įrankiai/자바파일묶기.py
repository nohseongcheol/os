#!/usr/bin/env python3
"""명시한 Java šaltinis_medis/klasė_VALUE 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def BIND_dalyvis(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for įrašas_VALUE in 항목들:
        if '=' not in įrašas_VALUE:
            raise ValueError('expected NAME=PATH: ' + įrašas_VALUE)
        Pavadinimas_2, KELIAS = įrašas_VALUE.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Pavadinimas_2) or Pavadinimas_2 in 명시:
            raise ValueError('invalid or duplicate file name: ' + Pavadinimas_2)
        명시.add(Pavadinimas_2)
        이름들.add(Pavadinimas_2)
        duomenys = Path(KELIAS).read_bytes()
        if len(duomenys) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Pavadinimas_2)
        파일들.append((Pavadinimas_2.encode('ascii'), duomenys))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    REZULTATAS = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    REZULTATAS.extend(bytes(72 * len(파일들)))
    for numeris, (Pavadinimas_2, duomenys) in enumerate(파일들):
        struct.pack_into('<64sII', REZULTATAS, 8 + numeris * 72, Pavadinimas_2, len(REZULTATAS), len(duomenys))
        REZULTATAS.extend(duomenys)
    return bytes(REZULTATAS)


if __name__ == '__main__':
    analizuoti_sintaksę_VALUE = argparse.ArgumentParser(description=__doc__)
    analizuoti_sintaksę_VALUE.add_argument('-o', required=True)
    analizuoti_sintaksę_VALUE.add_argument('files', nargs='*', help='NAME=PATH')
    Argumentai = analizuoti_sintaksę_VALUE.parse_args()
    try:
        duomenys = BIND_dalyvis(Argumentai.files)
        vieta_VALUE = Path(Argumentai.o)
        if not vieta_VALUE.exists() or vieta_VALUE.read_bytes() != duomenys:
            임시 = vieta_VALUE.with_name(vieta_VALUE.name + '.tmp')
            임시.write_bytes(duomenys)
            임시.replace(vieta_VALUE)
    except (ValueError, OSError) as KLAIDA:
        analizuoti_sintaksę_VALUE.error(str(KLAIDA))

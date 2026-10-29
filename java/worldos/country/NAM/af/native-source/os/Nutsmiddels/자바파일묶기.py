#!/usr/bin/env python3
"""명시한 Java bron_boom/Klas_VALUE 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for inskrywing_VALUE in 항목들:
        if '=' not in inskrywing_VALUE:
            raise ValueError('expected NAME=PATH: ' + inskrywing_VALUE)
        Naam, Pad = inskrywing_VALUE.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Naam) or Naam in 명시:
            raise ValueError('invalid or duplicate file name: ' + Naam)
        명시.add(Naam)
        이름들.add(Naam)
        data = Path(Pad).read_bytes()
        if len(data) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Naam)
        파일들.append((Naam.encode('ascii'), data))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    maatreël = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    maatreël.extend(bytes(72 * len(파일들)))
    for 수, (Naam, data) in enumerate(파일들):
        struct.pack_into('<64sII', maatreël, 8 + 수 * 72, Naam, len(maatreël), len(data))
        maatreël.extend(data)
    return bytes(maatreël)


if __name__ == '__main__':
    ontleed_VALUE = argparse.ArgumentParser(description=__doc__)
    ontleed_VALUE.add_argument('-o', required=True)
    ontleed_VALUE.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = ontleed_VALUE.parse_args()
    try:
        data = 묶기(인수.files)
        bestemming_VALUE = Path(인수.o)
        if not bestemming_VALUE.exists() or bestemming_VALUE.read_bytes() != data:
            임시 = bestemming_VALUE.with_name(bestemming_VALUE.name + '.tmp')
            임시.write_bytes(data)
            임시.replace(bestemming_VALUE)
    except (ValueError, OSError) as Fout:
        ontleed_VALUE.error(str(Fout))

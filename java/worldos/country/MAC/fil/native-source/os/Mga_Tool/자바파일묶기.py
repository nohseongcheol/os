#!/usr/bin/env python3
"""명시한 Java pinagmulan_balangkas/kategorya_VALUE_55654bf1 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for pagpasok_VALUE in 항목들:
        if '=' not in pagpasok_VALUE:
            raise ValueError('expected NAME=PATH: ' + pagpasok_VALUE)
        pangalan, path = pagpasok_VALUE.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', pangalan) or pangalan in 명시:
            raise ValueError('invalid or duplicate file name: ' + pangalan)
        명시.add(pangalan)
        이름들.add(pangalan)
        data = Path(path).read_bytes()
        if len(data) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + pangalan)
        파일들.append((pangalan.encode('ascii'), data))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    sukat = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    sukat.extend(bytes(72 * len(파일들)))
    for 수, (pangalan, data) in enumerate(파일들):
        struct.pack_into('<64sII', sukat, 8 + 수 * 72, pangalan, len(sukat), len(data))
        sukat.extend(data)
    return bytes(sukat)


if __name__ == '__main__':
    mag_parse_VALUE = argparse.ArgumentParser(description=__doc__)
    mag_parse_VALUE.add_argument('-o', required=True)
    mag_parse_VALUE.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = mag_parse_VALUE.parse_args()
    try:
        data = 묶기(인수.files)
        patutunguhan_VALUE = Path(인수.o)
        if not patutunguhan_VALUE.exists() or patutunguhan_VALUE.read_bytes() != data:
            임시 = patutunguhan_VALUE.with_name(patutunguhan_VALUE.name + '.tmp')
            임시.write_bytes(data)
            임시.replace(patutunguhan_VALUE)
    except (ValueError, OSError) as error:
        mag_parse_VALUE.error(str(error))

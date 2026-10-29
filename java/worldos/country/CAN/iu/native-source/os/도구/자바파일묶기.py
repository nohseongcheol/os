#!/usr/bin/env python3
"""명시한 Java pivviujuq_attavigiit/naliannuungavik_atuutilik 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for Iliniku_atuutilik in 항목들:
        if '=' not in Iliniku_atuutilik:
            raise ValueError('expected NAME=PATH: ' + Iliniku_atuutilik)
        atiq, aqqut = Iliniku_atuutilik.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', atiq) or atiq in 명시:
            raise ValueError('invalid or duplicate file name: ' + atiq)
        명시.add(atiq)
        이름들.add(atiq)
        titiqqat = Path(aqqut).read_bytes()
        if len(titiqqat) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + atiq)
        파일들.append((atiq.encode('ascii'), titiqqat))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    결과 = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    결과.extend(bytes(72 * len(파일들)))
    for 수, (atiq, titiqqat) in enumerate(파일들):
        struct.pack_into('<64sII', 결과, 8 + 수 * 72, atiq, len(결과), len(titiqqat))
        결과.extend(titiqqat)
    return bytes(결과)


if __name__ == '__main__':
    agguqtuut_atuutilik = argparse.ArgumentParser(description=__doc__)
    agguqtuut_atuutilik.add_argument('-o', required=True)
    agguqtuut_atuutilik.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = agguqtuut_atuutilik.parse_args()
    try:
        titiqqat = 묶기(인수.files)
        namunngarvik_atuutilik = Path(인수.o)
        if not namunngarvik_atuutilik.exists() or namunngarvik_atuutilik.read_bytes() != titiqqat:
            임시 = namunngarvik_atuutilik.with_name(namunngarvik_atuutilik.name + '.tmp')
            임시.write_bytes(titiqqat)
            임시.replace(namunngarvik_atuutilik)
    except (ValueError, OSError) as tammarniq:
        agguqtuut_atuutilik.error(str(tammarniq))

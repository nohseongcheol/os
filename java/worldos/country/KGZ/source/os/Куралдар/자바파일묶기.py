#!/usr/bin/env python3
"""명시한 Java башат_дарак/класс_маани 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for киргизме_жазуу_маани in 항목들:
        if '=' not in киргизме_жазуу_маани:
            raise ValueError('expected NAME=PATH: ' + киргизме_жазуу_маани)
        Аты, ЖОЛ = киргизме_жазуу_маани.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Аты) or Аты in 명시:
            raise ValueError('invalid or duplicate file name: ' + Аты)
        명시.add(Аты)
        이름들.add(Аты)
        берилмелер = Path(ЖОЛ).read_bytes()
        if len(берилмелер) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Аты)
        파일들.append((Аты.encode('ascii'), берилмелер))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    결과 = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    결과.extend(bytes(72 * len(파일들)))
    for 수, (Аты, берилмелер) in enumerate(파일들):
        struct.pack_into('<64sII', 결과, 8 + 수 * 72, Аты, len(결과), len(берилмелер))
        결과.extend(берилмелер)
    return bytes(결과)


if __name__ == '__main__':
    талдоо_маани = argparse.ArgumentParser(description=__doc__)
    талдоо_маани.add_argument('-o', required=True)
    талдоо_маани.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = талдоо_маани.parse_args()
    try:
        берилмелер = 묶기(인수.files)
        көздөө_жайы_маани = Path(인수.o)
        if not көздөө_жайы_маани.exists() or көздөө_жайы_маани.read_bytes() != берилмелер:
            임시 = көздөө_жайы_маани.with_name(көздөө_жайы_маани.name + '.tmp')
            임시.write_bytes(берилмелер)
            임시.replace(көздөө_жайы_маани)
    except (ValueError, OSError) as Ката:
        талдоо_маани.error(str(Ката))

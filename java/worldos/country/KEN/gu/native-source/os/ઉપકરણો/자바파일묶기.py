#!/usr/bin/env python3
"""명시한 Java સ્રોત_ટ્રી/વર્ગ_મૂલ્ય 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for પ્રવેશ_મૂલ્ય in 항목들:
        if '=' not in પ્રવેશ_મૂલ્ય:
            raise ValueError('expected NAME=PATH: ' + પ્રવેશ_મૂલ્ય)
        નામ, પથ = પ્રવેશ_મૂલ્ય.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', નામ) or નામ in 명시:
            raise ValueError('invalid or duplicate file name: ' + નામ)
        명시.add(નામ)
        이름들.add(નામ)
        ડેટા = Path(પથ).read_bytes()
        if len(ડેટા) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + નામ)
        파일들.append((નામ.encode('ascii'), ડેટા))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    પરિમાણ = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    પરિમાણ.extend(bytes(72 * len(파일들)))
    for 수, (નામ, ડેટા) in enumerate(파일들):
        struct.pack_into('<64sII', પરિમાણ, 8 + 수 * 72, નામ, len(પરિમાણ), len(ડેટા))
        પરિમાણ.extend(ડેટા)
    return bytes(પરિમાણ)


if __name__ == '__main__':
    પાર્સ_કરો_મૂલ્ય = argparse.ArgumentParser(description=__doc__)
    પાર્સ_કરો_મૂલ્ય.add_argument('-o', required=True)
    પાર્સ_કરો_મૂલ્ય.add_argument('files', nargs='*', help='NAME=PATH')
    દલીલો = પાર્સ_કરો_મૂલ્ય.parse_args()
    try:
        ડેટા = 묶기(દલીલો.files)
        ગંતવ્ય_મૂલ્ય = Path(દલીલો.o)
        if not ગંતવ્ય_મૂલ્ય.exists() or ગંતવ્ય_મૂલ્ય.read_bytes() != ડેટા:
            임시 = ગંતવ્ય_મૂલ્ય.with_name(ગંતવ્ય_મૂલ્ય.name + '.tmp')
            임시.write_bytes(ડેટા)
            임시.replace(ગંતવ્ય_મૂલ્ય)
    except (ValueError, OSError) as ભૂલ:
        પાર્સ_કરો_મૂલ્ય.error(str(ભૂલ))

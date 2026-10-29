#!/usr/bin/env python3
"""명시한 Java աղբյուր_ծառ/դաս_արժեք 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for մուտքագրում_արժեք in 항목들:
        if '=' not in մուտքագրում_արժեք:
            raise ValueError('expected NAME=PATH: ' + մուտքագրում_արժեք)
        Անուն, Ճանապարհ = մուտքագրում_արժեք.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Անուն) or Անուն in 명시:
            raise ValueError('invalid or duplicate file name: ' + Անուն)
        명시.add(Անուն)
        이름들.add(Անուն)
        տվյալ = Path(Ճանապարհ).read_bytes()
        if len(տվյալ) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Անուն)
        파일들.append((Անուն.encode('ascii'), տվյալ))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    չափ = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    չափ.extend(bytes(72 * len(파일들)))
    for 수, (Անուն, տվյալ) in enumerate(파일들):
        struct.pack_into('<64sII', չափ, 8 + 수 * 72, Անուն, len(չափ), len(տվյալ))
        չափ.extend(տվյալ)
    return bytes(չափ)


if __name__ == '__main__':
    վերլուծել_արժեք = argparse.ArgumentParser(description=__doc__)
    վերլուծել_արժեք.add_argument('-o', required=True)
    վերլուծել_արժեք.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = վերլուծել_արժեք.parse_args()
    try:
        տվյալ = 묶기(인수.files)
        նպատակակետ_արժեք = Path(인수.o)
        if not նպատակակետ_արժեք.exists() or նպատակակետ_արժեք.read_bytes() != տվյալ:
            임시 = նպատակակետ_արժեք.with_name(նպատակակետ_արժեք.name + '.tmp')
            임시.write_bytes(տվյալ)
            임시.replace(նպատակակետ_արժեք)
    except (ValueError, OSError) as Սխալ:
        վերլուծել_արժեք.error(str(Սխալ))

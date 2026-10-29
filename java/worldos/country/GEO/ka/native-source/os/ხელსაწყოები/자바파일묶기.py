#!/usr/bin/env python3
"""명시한 Java წყარო_ხე/კლასი_მნიშვნელობა 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for შენატანი_მნიშვნელობა in 항목들:
        if '=' not in შენატანი_მნიშვნელობა:
            raise ValueError('expected NAME=PATH: ' + შენატანი_მნიშვნელობა)
        სახელი, გეზი = შენატანი_მნიშვნელობა.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', სახელი) or სახელი in 명시:
            raise ValueError('invalid or duplicate file name: ' + სახელი)
        명시.add(სახელი)
        이름들.add(სახელი)
        მონაცემები = Path(გეზი).read_bytes()
        if len(მონაცემები) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + სახელი)
        파일들.append((სახელი.encode('ascii'), მონაცემები))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    გაზომვა = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    გაზომვა.extend(bytes(72 * len(파일들)))
    for 수, (სახელი, მონაცემები) in enumerate(파일들):
        struct.pack_into('<64sII', გაზომვა, 8 + 수 * 72, სახელი, len(გაზომვა), len(მონაცემები))
        გაზომვა.extend(მონაცემები)
    return bytes(გაზომვა)


if __name__ == '__main__':
    ანალიზი_მნიშვნელობა = argparse.ArgumentParser(description=__doc__)
    ანალიზი_მნიშვნელობა.add_argument('-o', required=True)
    ანალიზი_მნიშვნელობა.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = ანალიზი_მნიშვნელობა.parse_args()
    try:
        მონაცემები = 묶기(인수.files)
        მიმართულება_მნიშვნელობა = Path(인수.o)
        if not მიმართულება_მნიშვნელობა.exists() or მიმართულება_მნიშვნელობა.read_bytes() != მონაცემები:
            임시 = მიმართულება_მნიშვნელობა.with_name(მიმართულება_მნიშვნელობა.name + '.tmp')
            임시.write_bytes(მონაცემები)
            임시.replace(მიმართულება_მნიშვნელობა)
    except (ValueError, OSError) as შეცდომა:
        ანალიზი_მნიშვნელობა.error(str(შეცდომა))

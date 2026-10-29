#!/usr/bin/env python3
"""명시한 Java مەنبە_دەرەخ/تۈركۈم_قىممىتى 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for كىرگۈزۈش_قىممىتى in 항목들:
        if '=' not in كىرگۈزۈش_قىممىتى:
            raise ValueError('expected NAME=PATH: ' + كىرگۈزۈش_قىممىتى)
        ئاتى, يول = كىرگۈزۈش_قىممىتى.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', ئاتى) or ئاتى in 명시:
            raise ValueError('invalid or duplicate file name: ' + ئاتى)
        명시.add(ئاتى)
        이름들.add(ئاتى)
        مەلۇمات = Path(يول).read_bytes()
        if len(مەلۇمات) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + ئاتى)
        파일들.append((ئاتى.encode('ascii'), مەلۇمات))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    ئۆلچەم = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    ئۆلچەم.extend(bytes(72 * len(파일들)))
    for 수, (ئاتى, مەلۇمات) in enumerate(파일들):
        struct.pack_into('<64sII', ئۆلچەم, 8 + 수 * 72, ئاتى, len(ئۆلچەم), len(مەلۇمات))
        ئۆلچەم.extend(مەلۇمات)
    return bytes(ئۆلچەم)


if __name__ == '__main__':
    해석 = argparse.ArgumentParser(description=__doc__)
    해석.add_argument('-o', required=True)
    해석.add_argument('files', nargs='*', help='NAME=PATH')
    ئۆزگەرگۈچىلەر = 해석.parse_args()
    try:
        مەلۇمات = 묶기(ئۆزگەرگۈچىلەر.files)
        نىشان_قىممىتى = Path(ئۆزگەرگۈچىلەر.o)
        if not نىشان_قىممىتى.exists() or نىشان_قىممىتى.read_bytes() != مەلۇمات:
            임시 = نىشان_قىممىتى.with_name(نىشان_قىممىتى.name + '.tmp')
            임시.write_bytes(مەلۇمات)
            임시.replace(نىشان_قىممىتى)
    except (ValueError, OSError) as خاتالىق:
        해석.error(str(خاتالىق))

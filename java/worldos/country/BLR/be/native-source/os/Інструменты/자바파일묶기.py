#!/usr/bin/env python3
"""명시한 Java крыніца_дрэва/клас_значэнне 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for увядзенне_значэнне in 항목들:
        if '=' not in увядзенне_значэнне:
            raise ValueError('expected NAME=PATH: ' + увядзенне_значэнне)
        Назва, ШЛЯХ = увядзенне_значэнне.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Назва) or Назва in 명시:
            raise ValueError('invalid or duplicate file name: ' + Назва)
        명시.add(Назва)
        이름들.add(Назва)
        дадзеныя = Path(ШЛЯХ).read_bytes()
        if len(дадзеныя) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Назва)
        파일들.append((Назва.encode('ascii'), дадзеныя))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    결과 = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    결과.extend(bytes(72 * len(파일들)))
    for 수, (Назва, дадзеныя) in enumerate(파일들):
        struct.pack_into('<64sII', 결과, 8 + 수 * 72, Назва, len(결과), len(дадзеныя))
        결과.extend(дадзеныя)
    return bytes(결과)


if __name__ == '__main__':
    해석 = argparse.ArgumentParser(description=__doc__)
    해석.add_argument('-o', required=True)
    해석.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = 해석.parse_args()
    try:
        дадзеныя = 묶기(인수.files)
        прызначэнне_значэнне_a0fbc067 = Path(인수.o)
        if not прызначэнне_значэнне_a0fbc067.exists() or прызначэнне_значэнне_a0fbc067.read_bytes() != дадзеныя:
            임시 = прызначэнне_значэнне_a0fbc067.with_name(прызначэнне_значэнне_a0fbc067.name + '.tmp')
            임시.write_bytes(дадзеныя)
            임시.replace(прызначэнне_значэнне_a0fbc067)
    except (ValueError, OSError) as ПАМЫЛКА:
        해석.error(str(ПАМЫЛКА))

#!/usr/bin/env python3
"""명시한 Java 소스/클래스 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for 항목 in 항목들:
        if '=' not in 항목:
            raise ValueError('expected NAME=PATH: ' + 항목)
        Ishina, 경로 = 항목.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Ishina) or Ishina in 명시:
            raise ValueError('invalid or duplicate file name: ' + Ishina)
        명시.add(Ishina)
        이름들.add(Ishina)
        자료 = Path(경로).read_bytes()
        if len(자료) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Ishina)
        파일들.append((Ishina.encode('ascii'), 자료))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    결과 = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    결과.extend(bytes(72 * len(파일들)))
    for 수, (Ishina, 자료) in enumerate(파일들):
        struct.pack_into('<64sII', 결과, 8 + 수 * 72, Ishina, len(결과), len(자료))
        결과.extend(자료)
    return bytes(결과)


if __name__ == '__main__':
    해석 = argparse.ArgumentParser(description=__doc__)
    해석.add_argument('-o', required=True)
    해석.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = 해석.parse_args()
    try:
        자료 = 묶기(인수.files)
        목적 = Path(인수.o)
        if not 목적.exists() or 목적.read_bytes() != 자료:
            임시 = 목적.with_name(목적.name + '.tmp')
            임시.write_bytes(자료)
            임시.replace(목적)
    except (ValueError, OSError) as 오류:
        해석.error(str(오류))

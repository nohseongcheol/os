#!/usr/bin/env python3
"""명시한 Java чыганак_агач/класс_VALUE 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for кертү_VALUE in 항목들:
        if '=' not in кертү_VALUE:
            raise ValueError('expected NAME=PATH: ' + кертү_VALUE)
        исем, Yul = кертү_VALUE.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', исем) or исем in 명시:
            raise ValueError('invalid or duplicate file name: ' + исем)
        명시.add(исем)
        이름들.add(исем)
        мәгълүмат = Path(Yul).read_bytes()
        if len(мәгълүмат) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + исем)
        파일들.append((исем.encode('ascii'), мәгълүмат))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    үлчәм = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    үлчәм.extend(bytes(72 * len(파일들)))
    for 수, (исем, мәгълүмат) in enumerate(파일들):
        struct.pack_into('<64sII', үлчәм, 8 + 수 * 72, исем, len(үлчәм), len(мәгълүмат))
        үлчәм.extend(мәгълүмат)
    return bytes(үлчәм)


if __name__ == '__main__':
    бүлү_VALUE = argparse.ArgumentParser(description=__doc__)
    бүлү_VALUE.add_argument('-o', required=True)
    бүлү_VALUE.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = бүлү_VALUE.parse_args()
    try:
        мәгълүмат = 묶기(인수.files)
        күчерү_урыны_VALUE = Path(인수.o)
        if not күчерү_урыны_VALUE.exists() or күчерү_урыны_VALUE.read_bytes() != мәгълүмат:
            임시 = күчерү_урыны_VALUE.with_name(күчерү_урыны_VALUE.name + '.tmp')
            임시.write_bytes(мәгълүмат)
            임시.replace(күчерү_урыны_VALUE)
    except (ValueError, OSError) as Хата:
        бүлү_VALUE.error(str(Хата))

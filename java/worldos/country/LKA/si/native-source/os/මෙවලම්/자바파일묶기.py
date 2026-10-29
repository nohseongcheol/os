#!/usr/bin/env python3
"""명시한 Java මූලය_රුක/පන්තිය_අගය 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for පිවිසුම_අගය in 항목들:
        if '=' not in පිවිසුම_අගය:
            raise ValueError('expected NAME=PATH: ' + පිවිසුම_අගය)
        නම, මාර්_ගය = පිවිසුම_අගය.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', නම) or නම in 명시:
            raise ValueError('invalid or duplicate file name: ' + නම)
        명시.add(නම)
        이름들.add(නම)
        දත්ත = Path(මාර්_ගය).read_bytes()
        if len(දත්ත) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + නම)
        파일들.append((නම.encode('ascii'), දත්ත))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    결과 = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    결과.extend(bytes(72 * len(파일들)))
    for 수, (නම, දත්ත) in enumerate(파일들):
        struct.pack_into('<64sII', 결과, 8 + 수 * 72, නම, len(결과), len(දත්ත))
        결과.extend(දත්ත)
    return bytes(결과)


if __name__ == '__main__':
    විශ්ලේෂණය_කරන්න_අගය = argparse.ArgumentParser(description=__doc__)
    විශ්ලේෂණය_කරන්න_අගය.add_argument('-o', required=True)
    විශ්ලේෂණය_කරන්න_අගය.add_argument('files', nargs='*', help='NAME=PATH')
    විස්තාරක = විශ්ලේෂණය_කරන්න_අගය.parse_args()
    try:
        දත්ත = 묶기(විස්තාරක.files)
        ගමනාන්තය_අගය = Path(විස්තාරක.o)
        if not ගමනාන්තය_අගය.exists() or ගමනාන්තය_අගය.read_bytes() != දත්ත:
            임시 = ගමනාන්තය_අගය.with_name(ගමනාන්තය_අගය.name + '.tmp')
            임시.write_bytes(දත්ත)
            임시.replace(ගමනාන්තය_අගය)
    except (ValueError, OSError) as දෝෂය:
        විශ්ලේෂණය_කරන්න_අගය.error(str(දෝෂය))

#!/usr/bin/env python3
"""명시한 Java سرچینه_ونه/پاړکى_ارزښت 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for ننوت_ارزښت in 항목들:
        if '=' not in ننوت_ارزښت:
            raise ValueError('expected NAME=PATH: ' + ننوت_ارزښت)
        نوم, يونلور = ننوت_ارزښت.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', نوم) or نوم in 명시:
            raise ValueError('invalid or duplicate file name: ' + نوم)
        명시.add(نوم)
        이름들.add(نوم)
        اومتوک = Path(يونلور).read_bytes()
        if len(اومتوک) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + نوم)
        파일들.append((نوم.encode('ascii'), اومتوک))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    결과 = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    결과.extend(bytes(72 * len(파일들)))
    for 수, (نوم, اومتوک) in enumerate(파일들):
        struct.pack_into('<64sII', 결과, 8 + 수 * 72, نوم, len(결과), len(اومتوک))
        결과.extend(اومتوک)
    return bytes(결과)


if __name__ == '__main__':
    تجزیه_ارزښت = argparse.ArgumentParser(description=__doc__)
    تجزیه_ارزښت.add_argument('-o', required=True)
    تجزیه_ارزښت.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = تجزیه_ارزښت.parse_args()
    try:
        اومتوک = 묶기(인수.files)
        موخه_ارزښت = Path(인수.o)
        if not موخه_ارزښت.exists() or موخه_ارزښت.read_bytes() != اومتوک:
            임시 = موخه_ارزښت.with_name(موخه_ارزښت.name + '.tmp')
            임시.write_bytes(اومتوک)
            임시.replace(موخه_ارزښت)
    except (ValueError, OSError) as تېروتنه:
        تجزیه_ارزښت.error(str(تېروتنه))

#!/usr/bin/env python3
"""명시한 Java మూలం_వృక్షాకృతి/తరగతి_మూల్యం 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for ప్రవేశం_మూల్యం in 항목들:
        if '=' not in ప్రవేశం_మూల్యం:
            raise ValueError('expected NAME=PATH: ' + ప్రవేశం_మూల్యం)
        పేరు, పాత్ = ప్రవేశం_మూల్యం.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', పేరు) or పేరు in 명시:
            raise ValueError('invalid or duplicate file name: ' + పేరు)
        명시.add(పేరు)
        이름들.add(పేరు)
        డేటా = Path(పాత్).read_bytes()
        if len(డేటా) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + పేరు)
        파일들.append((పేరు.encode('ascii'), డేటా))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    ప్రమాణం = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    ప్రమాణం.extend(bytes(72 * len(파일들)))
    for 수, (పేరు, డేటా) in enumerate(파일들):
        struct.pack_into('<64sII', ప్రమాణం, 8 + 수 * 72, పేరు, len(ప్రమాణం), len(డేటా))
        ప్రమాణం.extend(డేటా)
    return bytes(ప్రమాణం)


if __name__ == '__main__':
    పార్స్_మూల్యం = argparse.ArgumentParser(description=__doc__)
    పార్స్_మూల్యం.add_argument('-o', required=True)
    పార్స్_మూల్యం.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = పార్స్_మూల్యం.parse_args()
    try:
        డేటా = 묶기(인수.files)
        గమ్యం_మూల్యం = Path(인수.o)
        if not గమ్యం_మూల్యం.exists() or గమ్యం_మూల్యం.read_bytes() != డేటా:
            임시 = గమ్యం_మూల్యం.with_name(గమ్యం_మూల్యం.name + '.tmp')
            임시.write_bytes(డేటా)
            임시.replace(గమ్యం_మూల్యం)
    except (ValueError, OSError) as దోషం:
        పార్స్_మూల్యం.error(str(దోషం))

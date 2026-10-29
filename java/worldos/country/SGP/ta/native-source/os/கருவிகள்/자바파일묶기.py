#!/usr/bin/env python3
"""명시한 Java மூலம்_மரம்/பிரிவு_மதிப்பு_55654bf1 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def கட்டு_முடிவுப்_புள்ளி(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for உள்ளீடு_மதிப்பு in 항목들:
        if '=' not in உள்ளீடு_மதிப்பு:
            raise ValueError('expected NAME=PATH: ' + உள்ளீடு_மதிப்பு)
        பெயர், பாதை_2 = உள்ளீடு_மதிப்பு.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', பெயர்) or பெயர் in 명시:
            raise ValueError('invalid or duplicate file name: ' + பெயர்)
        명시.add(பெயர்)
        이름들.add(பெயர்)
        தரவு = Path(பாதை_2).read_bytes()
        if len(தரவு) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + பெயர்)
        파일들.append((பெயர்.encode('ascii'), தரவு))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    அளவிடக்கூடியது = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    அளவிடக்கூடியது.extend(bytes(72 * len(파일들)))
    for 수, (பெயர், தரவு) in enumerate(파일들):
        struct.pack_into('<64sII', அளவிடக்கூடியது, 8 + 수 * 72, பெயர், len(அளவிடக்கூடியது), len(தரவு))
        அளவிடக்கூடியது.extend(தரவு)
    return bytes(அளவிடக்கூடியது)


if __name__ == '__main__':
    அலகிடு_மதிப்பு = argparse.ArgumentParser(description=__doc__)
    அலகிடு_மதிப்பு.add_argument('-o', required=True)
    அலகிடு_மதிப்பு.add_argument('files', nargs='*', help='NAME=PATH')
    செயலுருபுகள் = அலகிடு_மதிப்பு.parse_args()
    try:
        தரவு = கட்டு_முடிவுப்_புள்ளி(செயலுருபுகள்.files)
        இலக்கு_மதிப்பு = Path(செயலுருபுகள்.o)
        if not இலக்கு_மதிப்பு.exists() or இலக்கு_மதிப்பு.read_bytes() != தரவு:
            임시 = இலக்கு_மதிப்பு.with_name(இலக்கு_மதிப்பு.name + '.tmp')
            임시.write_bytes(தரவு)
            임시.replace(இலக்கு_மதிப்பு)
    except (ValueError, OSError) as பிழை:
        அலகிடு_மதிப்பு.error(str(பிழை))

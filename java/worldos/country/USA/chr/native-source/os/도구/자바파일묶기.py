#!/usr/bin/env python3
"""명시한 Java ᎦᏟᏌᏅᎯ_ᏡᎬ/ᏄᏍᏛᎢ_ᏧᎬᏩᎶᏗᏯ 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ in 항목들:
        if '=' not in Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ:
            raise ValueError('expected NAME=PATH: ' + Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ)
        ᏚᏙᎥᎢ, ᎠᏍᏓᏩᏛᏍᏗ = Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', ᏚᏙᎥᎢ) or ᏚᏙᎥᎢ in 명시:
            raise ValueError('invalid or duplicate file name: ' + ᏚᏙᎥᎢ)
        명시.add(ᏚᏙᎥᎢ)
        이름들.add(ᏚᏙᎥᎢ)
        ᎦᏟᏌᏅᎯ = Path(ᎠᏍᏓᏩᏛᏍᏗ).read_bytes()
        if len(ᎦᏟᏌᏅᎯ) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + ᏚᏙᎥᎢ)
        파일들.append((ᏚᏙᎥᎢ.encode('ascii'), ᎦᏟᏌᏅᎯ))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    결과 = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    결과.extend(bytes(72 * len(파일들)))
    for 수, (ᏚᏙᎥᎢ, ᎦᏟᏌᏅᎯ) in enumerate(파일들):
        struct.pack_into('<64sII', 결과, 8 + 수 * 72, ᏚᏙᎥᎢ, len(결과), len(ᎦᏟᏌᏅᎯ))
        결과.extend(ᎦᏟᏌᏅᎯ)
    return bytes(결과)


if __name__ == '__main__':
    해석 = argparse.ArgumentParser(description=__doc__)
    해석.add_argument('-o', required=True)
    해석.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = 해석.parse_args()
    try:
        ᎦᏟᏌᏅᎯ = 묶기(인수.files)
        ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ = Path(인수.o)
        if not ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ.exists() or ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ.read_bytes() != ᎦᏟᏌᏅᎯ:
            임시 = ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ.with_name(ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ.name + '.tmp')
            임시.write_bytes(ᎦᏟᏌᏅᎯ)
            임시.replace(ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ)
    except (ValueError, OSError) as ᎦᎵᏓᏍᏔᏅ:
        해석.error(str(ᎦᎵᏓᏍᏔᏅ))

#!/usr/bin/env python3
"""명시한 Java ژێدەر_دار/کلاس_نرخ 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for تێنووسین_نرخ in 항목들:
        if '=' not in تێنووسین_نرخ:
            raise ValueError('expected NAME=PATH: ' + تێنووسین_نرخ)
        ناو, گوزەر = تێنووسین_نرخ.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', ناو) or ناو in 명시:
            raise ValueError('invalid or duplicate file name: ' + ناو)
        명시.add(ناو)
        이름들.add(ناو)
        دەیتا = Path(گوزەر).read_bytes()
        if len(دەیتا) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + ناو)
        파일들.append((ناو.encode('ascii'), دەیتا))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    결과 = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    결과.extend(bytes(72 * len(파일들)))
    for 수, (ناو, دەیتا) in enumerate(파일들):
        struct.pack_into('<64sII', 결과, 8 + 수 * 72, ناو, len(결과), len(دەیتا))
        결과.extend(دەیتا)
    return bytes(결과)


if __name__ == '__main__':
    해석 = argparse.ArgumentParser(description=__doc__)
    해석.add_argument('-o', required=True)
    해석.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = 해석.parse_args()
    try:
        دەیتا = 묶기(인수.files)
        جێمەبەست_نرخ = Path(인수.o)
        if not جێمەبەست_نرخ.exists() or جێمەبەست_نرخ.read_bytes() != دەیتا:
            임시 = جێمەبەست_نرخ.with_name(جێمەبەست_نرخ.name + '.tmp')
            임시.write_bytes(دەیتا)
            임시.replace(جێمەبەست_نرخ)
    except (ValueError, OSError) as هەڵە:
        해석.error(str(هەڵە))

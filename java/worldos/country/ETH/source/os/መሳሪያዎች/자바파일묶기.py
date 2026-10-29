#!/usr/bin/env python3
"""명시한 Java ምንጭ_ዛፍ/መደብ_እሴት 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for ምዝግብ_እሴት in 항목들:
        if '=' not in ምዝግብ_እሴት:
            raise ValueError('expected NAME=PATH: ' + ምዝግብ_እሴት)
        ስም, መተላለፊያ = ምዝግብ_እሴት.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', ስም) or ስም in 명시:
            raise ValueError('invalid or duplicate file name: ' + ስም)
        명시.add(ስም)
        이름들.add(ስም)
        ውሂብ = Path(መተላለፊያ).read_bytes()
        if len(ውሂብ) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + ስም)
        파일들.append((ስም.encode('ascii'), ውሂብ))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    ልኬት = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    ልኬት.extend(bytes(72 * len(파일들)))
    for 수, (ስም, ውሂብ) in enumerate(파일들):
        struct.pack_into('<64sII', ልኬት, 8 + 수 * 72, ስም, len(ልኬት), len(ውሂብ))
        ልኬት.extend(ውሂብ)
    return bytes(ልኬት)


if __name__ == '__main__':
    ተንትን_እሴት = argparse.ArgumentParser(description=__doc__)
    ተንትን_እሴት.add_argument('-o', required=True)
    ተንትን_እሴት.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = ተንትን_እሴት.parse_args()
    try:
        ውሂብ = 묶기(인수.files)
        መድረሻ_እሴት = Path(인수.o)
        if not መድረሻ_እሴት.exists() or መድረሻ_እሴት.read_bytes() != ውሂብ:
            임시 = መድረሻ_እሴት.with_name(መድረሻ_እሴት.name + '.tmp')
            임시.write_bytes(ውሂብ)
            임시.replace(መድረሻ_እሴት)
    except (ValueError, OSError) as ስህተት:
        ተንትን_እሴት.error(str(ስህተት))

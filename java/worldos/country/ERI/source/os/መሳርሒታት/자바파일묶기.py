#!/usr/bin/env python3
"""명시한 Java ምንጪ_ገረብ/ክፍሊ_ዋጋ 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for ምእታው_ዋጋ in 항목들:
        if '=' not in ምእታው_ዋጋ:
            raise ValueError('expected NAME=PATH: ' + ምእታው_ዋጋ)
        ሽም, መገዲ = ምእታው_ዋጋ.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', ሽም) or ሽም in 명시:
            raise ValueError('invalid or duplicate file name: ' + ሽም)
        명시.add(ሽም)
        이름들.add(ሽም)
        ሓበሬታ = Path(መገዲ).read_bytes()
        if len(ሓበሬታ) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + ሽም)
        파일들.append((ሽም.encode('ascii'), ሓበሬታ))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    결과 = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    결과.extend(bytes(72 * len(파일들)))
    for 수, (ሽም, ሓበሬታ) in enumerate(파일들):
        struct.pack_into('<64sII', 결과, 8 + 수 * 72, ሽም, len(결과), len(ሓበሬታ))
        결과.extend(ሓበሬታ)
    return bytes(결과)


if __name__ == '__main__':
    해석 = argparse.ArgumentParser(description=__doc__)
    해석.add_argument('-o', required=True)
    해석.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = 해석.parse_args()
    try:
        ሓበሬታ = 묶기(인수.files)
        መዓልቦ_ዋጋ = Path(인수.o)
        if not መዓልቦ_ዋጋ.exists() or መዓልቦ_ዋጋ.read_bytes() != ሓበሬታ:
            임시 = መዓልቦ_ዋጋ.with_name(መዓልቦ_ዋጋ.name + '.tmp')
            임시.write_bytes(ሓበሬታ)
            임시.replace(መዓልቦ_ዋጋ)
    except (ValueError, OSError) as ጌጋ:
        해석.error(str(ጌጋ))

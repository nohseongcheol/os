#!/usr/bin/env python3
"""명시한 Java ଉତ୍ସ_ବୃକ୍ଷ/ଶ୍ରେଣୀ_ମୂଲ୍ୟ_55654bf1 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ in 항목들:
        if '=' not in ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ:
            raise ValueError('expected NAME=PATH: ' + ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ)
        ନାମ, ପଥ = ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', ନାମ) or ନାମ in 명시:
            raise ValueError('invalid or duplicate file name: ' + ନାମ)
        명시.add(ନାମ)
        이름들.add(ନାମ)
        ଡାଟା = Path(ପଥ).read_bytes()
        if len(ଡାଟା) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + ନାମ)
        파일들.append((ନାମ.encode('ascii'), ଡାଟା))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    ମାପ = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    ମାପ.extend(bytes(72 * len(파일들)))
    for 수, (ନାମ, ଡାଟା) in enumerate(파일들):
        struct.pack_into('<64sII', ମାପ, 8 + 수 * 72, ନାମ, len(ମାପ), len(ଡାଟା))
        ମାପ.extend(ଡାଟା)
    return bytes(ମାପ)


if __name__ == '__main__':
    ପାର୍ସ_ମୂଲ୍ୟ = argparse.ArgumentParser(description=__doc__)
    ପାର୍ସ_ମୂଲ୍ୟ.add_argument('-o', required=True)
    ପାର୍ସ_ମୂଲ୍ୟ.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = ପାର୍ସ_ମୂଲ୍ୟ.parse_args()
    try:
        ଡାଟା = 묶기(인수.files)
        ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ = Path(인수.o)
        if not ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ.exists() or ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ.read_bytes() != ଡାଟା:
            임시 = ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ.with_name(ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ.name + '.tmp')
            임시.write_bytes(ଡାଟା)
            임시.replace(ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ)
    except (ValueError, OSError) as ତ୍ରୁଟି:
        ପାର୍ସ_ମୂଲ୍ୟ.error(str(ତ୍ରୁଟି))

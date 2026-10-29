#!/usr/bin/env python3
"""명시한 Java ਸਰੋਤ_ਟ੍ਰੀ/ਸ੍ਰੇਣੀ_ਕੀਮਤ 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for ਦਾਖਲਾ_ਕੀਮਤ in 항목들:
        if '=' not in ਦਾਖਲਾ_ਕੀਮਤ:
            raise ValueError('expected NAME=PATH: ' + ਦਾਖਲਾ_ਕੀਮਤ)
        ਨਾਂ, ਮਾਰਗ = ਦਾਖਲਾ_ਕੀਮਤ.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', ਨਾਂ) or ਨਾਂ in 명시:
            raise ValueError('invalid or duplicate file name: ' + ਨਾਂ)
        명시.add(ਨਾਂ)
        이름들.add(ਨਾਂ)
        ਸਮੱਗਰੀ = Path(ਮਾਰਗ).read_bytes()
        if len(ਸਮੱਗਰੀ) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + ਨਾਂ)
        파일들.append((ਨਾਂ.encode('ascii'), ਸਮੱਗਰੀ))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    ਮਾਪ = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    ਮਾਪ.extend(bytes(72 * len(파일들)))
    for 수, (ਨਾਂ, ਸਮੱਗਰੀ) in enumerate(파일들):
        struct.pack_into('<64sII', ਮਾਪ, 8 + 수 * 72, ਨਾਂ, len(ਮਾਪ), len(ਸਮੱਗਰੀ))
        ਮਾਪ.extend(ਸਮੱਗਰੀ)
    return bytes(ਮਾਪ)


if __name__ == '__main__':
    ਪਦ_ਵਿਆਖਿਆ_ਕਰੋ_ਕੀਮਤ = argparse.ArgumentParser(description=__doc__)
    ਪਦ_ਵਿਆਖਿਆ_ਕਰੋ_ਕੀਮਤ.add_argument('-o', required=True)
    ਪਦ_ਵਿਆਖਿਆ_ਕਰੋ_ਕੀਮਤ.add_argument('files', nargs='*', help='NAME=PATH')
    ਆਰਗੂਮੈਂਟ = ਪਦ_ਵਿਆਖਿਆ_ਕਰੋ_ਕੀਮਤ.parse_args()
    try:
        ਸਮੱਗਰੀ = 묶기(ਆਰਗੂਮੈਂਟ.files)
        ਮੰਜਿਲ_ਕੀਮਤ = Path(ਆਰਗੂਮੈਂਟ.o)
        if not ਮੰਜਿਲ_ਕੀਮਤ.exists() or ਮੰਜਿਲ_ਕੀਮਤ.read_bytes() != ਸਮੱਗਰੀ:
            임시 = ਮੰਜਿਲ_ਕੀਮਤ.with_name(ਮੰਜਿਲ_ਕੀਮਤ.name + '.tmp')
            임시.write_bytes(ਸਮੱਗਰੀ)
            임시.replace(ਮੰਜਿਲ_ਕੀਮਤ)
    except (ValueError, OSError) as ਗਲਤੀ:
        ਪਦ_ਵਿਆਖਿਆ_ਕਰੋ_ਕੀਮਤ.error(str(ਗਲਤੀ))

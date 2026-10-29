#!/usr/bin/env python3
"""명시한 Java منبع_درخت/کلاس_مقدار 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for ورودی_مقدار in 항목들:
        if '=' not in ورودی_مقدار:
            raise ValueError('expected NAME=PATH: ' + ورودی_مقدار)
        نام, مسیر = ورودی_مقدار.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', نام) or نام in 명시:
            raise ValueError('invalid or duplicate file name: ' + نام)
        명시.add(نام)
        이름들.add(نام)
        داده_ها = Path(مسیر).read_bytes()
        if len(داده_ها) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + نام)
        파일들.append((نام.encode('ascii'), داده_ها))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    سنجش = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    سنجش.extend(bytes(72 * len(파일들)))
    for 수, (نام, داده_ها) in enumerate(파일들):
        struct.pack_into('<64sII', سنجش, 8 + 수 * 72, نام, len(سنجش), len(داده_ها))
        سنجش.extend(داده_ها)
    return bytes(سنجش)


if __name__ == '__main__':
    تفسیر_مقدار = argparse.ArgumentParser(description=__doc__)
    تفسیر_مقدار.add_argument('-o', required=True)
    تفسیر_مقدار.add_argument('files', nargs='*', help='NAME=PATH')
    نشانوندها = تفسیر_مقدار.parse_args()
    try:
        داده_ها = 묶기(نشانوندها.files)
        مقصد_مقدار = Path(نشانوندها.o)
        if not مقصد_مقدار.exists() or مقصد_مقدار.read_bytes() != داده_ها:
            임시 = مقصد_مقدار.with_name(مقصد_مقدار.name + '.tmp')
            임시.write_bytes(داده_ها)
            임시.replace(مقصد_مقدار)
    except (ValueError, OSError) as خطا:
        تفسیر_مقدار.error(str(خطا))

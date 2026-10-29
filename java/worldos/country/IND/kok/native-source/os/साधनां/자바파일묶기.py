#!/usr/bin/env python3
"""명시한 Java स्त्रोत_ट्री/वर्ग_मोल_55654bf1 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for प्रवेश_मोल in 항목들:
        if '=' not in प्रवेश_मोल:
            raise ValueError('expected NAME=PATH: ' + प्रवेश_मोल)
        नांव, पाथ = प्रवेश_मोल.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', नांव) or नांव in 명시:
            raise ValueError('invalid or duplicate file name: ' + नांव)
        명시.add(नांव)
        이름들.add(नांव)
        डेटा = Path(पाथ).read_bytes()
        if len(डेटा) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + नांव)
        파일들.append((नांव.encode('ascii'), डेटा))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    मेजप = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    मेजप.extend(bytes(72 * len(파일들)))
    for 수, (नांव, डेटा) in enumerate(파일들):
        struct.pack_into('<64sII', मेजप, 8 + 수 * 72, नांव, len(मेजप), len(डेटा))
        मेजप.extend(डेटा)
    return bytes(मेजप)


if __name__ == '__main__':
    व्याकरणी_फोडणिशी_मोल = argparse.ArgumentParser(description=__doc__)
    व्याकरणी_फोडणिशी_मोल.add_argument('-o', required=True)
    व्याकरणी_फोडणिशी_मोल.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = व्याकरणी_फोडणिशी_मोल.parse_args()
    try:
        डेटा = 묶기(인수.files)
        नियुक्त_स्थान_मोल = Path(인수.o)
        if not नियुक्त_स्थान_मोल.exists() or नियुक्त_स्थान_मोल.read_bytes() != डेटा:
            임시 = नियुक्त_स्थान_मोल.with_name(नियुक्त_स्थान_मोल.name + '.tmp')
            임시.write_bytes(डेटा)
            임시.replace(नियुक्त_स्थान_मोल)
    except (ValueError, OSError) as चूक:
        व्याकरणी_फोडणिशी_मोल.error(str(चूक))

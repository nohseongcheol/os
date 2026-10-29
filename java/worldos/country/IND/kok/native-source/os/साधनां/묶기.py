#!/usr/bin/env python3
"""명시한 उपेगकर्तो ELF만 읽기 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    व्याकरणी_फोडणिशी_मोल = argparse.ArgumentParser()
    व्याकरणी_फोडणिशी_मोल.add_argument('-o', required=True)
    व्याकरणी_फोडणिशी_मोल.add_argument('files', nargs='+', help='नांव=ELF경로')
    인자 = व्याकरणी_फोडणिशी_मोल.parse_args()
    if len(인자.files) > 32:
        व्याकरणी_फोडणिशी_मोल.error('एप्लिकेशन_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for प्रवेश_मोल in 인자.files:
        नांव, पाथ = प्रवेश_मोल.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', नांव) or नांव in 이름들:
            व्याकरणी_फोडणिशी_मोल.error('पाळो_दिवचो_आदेश 이름이 잘못되었거나 중복됨: ' + नांव)
        이름들.add(नांव)
        डेटा = Path(पाथ).read_bytes()
        if len(डेटा) > 2 * 1024 * 1024:
            व्याकरणी_फोडणिशी_मोल.error('पाळो_दिवचो_आदेश 파일이 너무 큼')
        항목들.append((नांव.encode(), डेटा))
    मेजप = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', मेजप, 0, 0x50414b4a, len(항목들))
    for INDEX, (नांव, डेटा) in enumerate(항목들):
        मेजप.extend(bytes((-len(मेजप)) % 16))
        struct.pack_into('<16sII', मेजप, 8 + INDEX * 24, नांव, len(मेजप), len(डेटा))
        मेजप.extend(डेटा)
    Path(인자.o).write_bytes(मेजप)

if __name__ == '__main__':
    묶기()

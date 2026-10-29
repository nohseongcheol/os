#!/usr/bin/env python3
"""명시한 ଉପଭୋକ୍ତା ELF만 ପଢନ୍ତୁ 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    ପାର୍ସ_ମୂଲ୍ୟ = argparse.ArgumentParser()
    ପାର୍ସ_ମୂଲ୍ୟ.add_argument('-o', required=True)
    ପାର୍ସ_ମୂଲ୍ୟ.add_argument('files', nargs='+', help='ନାମ=ELF경로')
    ପାରାମିଟର୍_ଯୁକ୍ତି = ପାର୍ସ_ମୂଲ୍ୟ.parse_args()
    if len(ପାରାମିଟର୍_ଯୁକ୍ତି.files) > 32:
        ପାର୍ସ_ମୂଲ୍ୟ.error('ଅନୁପ୍ରୟୋଗ_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ in ପାରାମିଟର୍_ଯୁକ୍ତି.files:
        ନାମ, ପଥ = ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', ନାମ) or ନାମ in 이름들:
            ପାର୍ସ_ମୂଲ୍ୟ.error('ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ 이름이 잘못되었거나 중복됨: ' + ନାମ)
        이름들.add(ନାମ)
        ଡାଟା = Path(ପଥ).read_bytes()
        if len(ଡାଟା) > 2 * 1024 * 1024:
            ପାର୍ସ_ମୂଲ୍ୟ.error('ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ 파일이 너무 큼')
        항목들.append((ନାମ.encode(), ଡାଟା))
    ମାପ = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', ମାପ, 0, 0x50414b4a, len(항목들))
    for ଅନୁକ୍ରମଣିକା, (ନାମ, ଡାଟା) in enumerate(항목들):
        ମାପ.extend(bytes((-len(ମାପ)) % 16))
        struct.pack_into('<16sII', ମାପ, 8 + ଅନୁକ୍ରମଣିକା * 24, ନାମ, len(ମାପ), len(ଡାଟା))
        ମାପ.extend(ଡାଟା)
    Path(ପାରାମିଟର୍_ଯୁକ୍ତି.o).write_bytes(ମାପ)

if __name__ == '__main__':
    묶기()

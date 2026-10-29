#!/usr/bin/env python3
"""명시한 ਉਪਭੋਗਤਾ ELF만 ਪੜ੍ਹਨ 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    ਪਦ_ਵਿਆਖਿਆ_ਕਰੋ_ਕੀਮਤ = argparse.ArgumentParser()
    ਪਦ_ਵਿਆਖਿਆ_ਕਰੋ_ਕੀਮਤ.add_argument('-o', required=True)
    ਪਦ_ਵਿਆਖਿਆ_ਕਰੋ_ਕੀਮਤ.add_argument('files', nargs='+', help='ਨਾਂ=ELF경로')
    인자 = ਪਦ_ਵਿਆਖਿਆ_ਕਰੋ_ਕੀਮਤ.parse_args()
    if len(인자.files) > 32:
        ਪਦ_ਵਿਆਖਿਆ_ਕਰੋ_ਕੀਮਤ.error('ਐਪਲੀਕੇਸ਼_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for ਦਾਖਲਾ_ਕੀਮਤ in 인자.files:
        ਨਾਂ, ਮਾਰਗ = ਦਾਖਲਾ_ਕੀਮਤ.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', ਨਾਂ) or ਨਾਂ in 이름들:
            ਪਦ_ਵਿਆਖਿਆ_ਕਰੋ_ਕੀਮਤ.error('ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ 이름이 잘못되었거나 중복됨: ' + ਨਾਂ)
        이름들.add(ਨਾਂ)
        ਸਮੱਗਰੀ = Path(ਮਾਰਗ).read_bytes()
        if len(ਸਮੱਗਰੀ) > 2 * 1024 * 1024:
            ਪਦ_ਵਿਆਖਿਆ_ਕਰੋ_ਕੀਮਤ.error('ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ 파일이 너무 큼')
        항목들.append((ਨਾਂ.encode(), ਸਮੱਗਰੀ))
    ਮਾਪ = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', ਮਾਪ, 0, 0x50414b4a, len(항목들))
    for ਅਨੁਕ੍ਰਮਣਿਕਾ, (ਨਾਂ, ਸਮੱਗਰੀ) in enumerate(항목들):
        ਮਾਪ.extend(bytes((-len(ਮਾਪ)) % 16))
        struct.pack_into('<16sII', ਮਾਪ, 8 + ਅਨੁਕ੍ਰਮਣਿਕਾ * 24, ਨਾਂ, len(ਮਾਪ), len(ਸਮੱਗਰੀ))
        ਮਾਪ.extend(ਸਮੱਗਰੀ)
    Path(인자.o).write_bytes(ਮਾਪ)

if __name__ == '__main__':
    묶기()

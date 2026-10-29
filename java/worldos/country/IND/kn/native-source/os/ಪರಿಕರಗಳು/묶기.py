#!/usr/bin/env python3
"""명시한 ಬಳಕೆದಾರ ELF만 ಓದು 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    ಪಾರ್ಸ್_ಮಾಡಿ_ಮೌಲ್ಯ = argparse.ArgumentParser()
    ಪಾರ್ಸ್_ಮಾಡಿ_ಮೌಲ್ಯ.add_argument('-o', required=True)
    ಪಾರ್ಸ್_ಮಾಡಿ_ಮೌಲ್ಯ.add_argument('files', nargs='+', help='ಹೆಸರು=ELF경로')
    ಪ್ಯಾರಾಮೀಟರ್_ವಾದ = ಪಾರ್ಸ್_ಮಾಡಿ_ಮೌಲ್ಯ.parse_args()
    if len(ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.files) > 32:
        ಪಾರ್ಸ್_ಮಾಡಿ_ಮೌಲ್ಯ.error('ಅಪ್ಲಿ_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for ನಮೂದು_ಮೌಲ್ಯ in ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.files:
        ಹೆಸರು, ಮಾರ್ಗ = ನಮೂದು_ಮೌಲ್ಯ.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', ಹೆಸರು) or ಹೆಸರು in 이름들:
            ಪಾರ್ಸ್_ಮಾಡಿ_ಮೌಲ್ಯ.error('ಪೂರೈಸು_ಆದೇಶ 이름이 잘못되었거나 중복됨: ' + ಹೆಸರು)
        이름들.add(ಹೆಸರು)
        ಡೇಟಾ = Path(ಮಾರ್ಗ).read_bytes()
        if len(ಡೇಟಾ) > 2 * 1024 * 1024:
            ಪಾರ್ಸ್_ಮಾಡಿ_ಮೌಲ್ಯ.error('ಪೂರೈಸು_ಆದೇಶ 파일이 너무 큼')
        항목들.append((ಹೆಸರು.encode(), ಡೇಟಾ))
    ಮಾಪನ = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', ಮಾಪನ, 0, 0x50414b4a, len(항목들))
    for ಪದಸೂಚಿ, (ಹೆಸರು, ಡೇಟಾ) in enumerate(항목들):
        ಮಾಪನ.extend(bytes((-len(ಮಾಪನ)) % 16))
        struct.pack_into('<16sII', ಮಾಪನ, 8 + ಪದಸೂಚಿ * 24, ಹೆಸರು, len(ಮಾಪನ), len(ಡೇಟಾ))
        ಮಾಪನ.extend(ಡೇಟಾ)
    Path(ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.o).write_bytes(ಮಾಪನ)

if __name__ == '__main__':
    묶기()

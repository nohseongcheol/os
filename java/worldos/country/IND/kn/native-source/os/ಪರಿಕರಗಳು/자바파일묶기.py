#!/usr/bin/env python3
"""명시한 Java ಮೂಲ_ವೃಕ್ಷ/ವರ್ಗ_ಮೌಲ್ಯ_55654bf1 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def 묶기(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for ನಮೂದು_ಮೌಲ್ಯ in 항목들:
        if '=' not in ನಮೂದು_ಮೌಲ್ಯ:
            raise ValueError('expected NAME=PATH: ' + ನಮೂದು_ಮೌಲ್ಯ)
        ಹೆಸರು, ಮಾರ್ಗ = ನಮೂದು_ಮೌಲ್ಯ.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', ಹೆಸರು) or ಹೆಸರು in 명시:
            raise ValueError('invalid or duplicate file name: ' + ಹೆಸರು)
        명시.add(ಹೆಸರು)
        이름들.add(ಹೆಸರು)
        ಡೇಟಾ = Path(ಮಾರ್ಗ).read_bytes()
        if len(ಡೇಟಾ) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + ಹೆಸರು)
        파일들.append((ಹೆಸರು.encode('ascii'), ಡೇಟಾ))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    ಮಾಪನ = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    ಮಾಪನ.extend(bytes(72 * len(파일들)))
    for 수, (ಹೆಸರು, ಡೇಟಾ) in enumerate(파일들):
        struct.pack_into('<64sII', ಮಾಪನ, 8 + 수 * 72, ಹೆಸರು, len(ಮಾಪನ), len(ಡೇಟಾ))
        ಮಾಪನ.extend(ಡೇಟಾ)
    return bytes(ಮಾಪನ)


if __name__ == '__main__':
    ಪಾರ್ಸ್_ಮಾಡಿ_ಮೌಲ್ಯ = argparse.ArgumentParser(description=__doc__)
    ಪಾರ್ಸ್_ಮಾಡಿ_ಮೌಲ್ಯ.add_argument('-o', required=True)
    ಪಾರ್ಸ್_ಮಾಡಿ_ಮೌಲ್ಯ.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = ಪಾರ್ಸ್_ಮಾಡಿ_ಮೌಲ್ಯ.parse_args()
    try:
        ಡೇಟಾ = 묶기(인수.files)
        ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ = Path(인수.o)
        if not ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ.exists() or ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ.read_bytes() != ಡೇಟಾ:
            임시 = ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ.with_name(ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ.name + '.tmp')
            임시.write_bytes(ಡೇಟಾ)
            임시.replace(ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ)
    except (ValueError, OSError) as ದೋಷ:
        ಪಾರ್ಸ್_ಮಾಡಿ_ಮೌಲ್ಯ.error(str(ದೋಷ))

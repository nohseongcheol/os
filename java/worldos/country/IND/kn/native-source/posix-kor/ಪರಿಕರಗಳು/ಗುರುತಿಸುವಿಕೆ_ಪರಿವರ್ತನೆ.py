#!/usr/bin/env python3
"""ಕನ್ನಡ C 식별자만 UCN으로 옮긴다. ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

ಟೋಕನ್_ಮೌಲ್ಯ = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<ಗುರುತಿಸುವಿಕೆ_ಮೌಲ್ಯ>[^\W\d]\w*)', re.S | re.M)

def 변환(ಮೂಲ):
    def ಬದಲಾಯಿಸು_ಮೌಲ್ಯ(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(ಅಕ್ಷರ_ಮೌಲ್ಯ if ord(ಅಕ್ಷರ_ಮೌಲ್ಯ) < 128 else
                       ('\\u%04x' if ord(ಅಕ್ಷರ_ಮೌಲ್ಯ) <= 65535 else '\\U%08x') % ord(ಅಕ್ಷರ_ಮೌಲ್ಯ)
                       for ಅಕ್ಷರ_ಮೌಲ್ಯ in 일치[0])
    return ಟೋಕನ್_ಮೌಲ್ಯ.sub(ಬದಲಾಯಿಸು_ಮೌಲ್ಯ, ಮೂಲ)

def ಪೂರೈಸು_ಆದೇಶ():
    ಪಾರ್ಸರ್_48ee4b1b = argparse.ArgumentParser()
    ಪಾರ್ಸರ್_48ee4b1b.add_argument('원본', type=Path)
    ಪಾರ್ಸರ್_48ee4b1b.add_argument('ಔಟ್_ಪುಟ್', type=Path)
    인수 = ಪಾರ್ಸರ್_48ee4b1b.parse_args()
    for ಕಡತ in sorted(인수.원본.rglob('*')):
        if ಕಡತ.suffix not in ('.c', '.h'):
            continue
        ಔಟ್_ಪುಟ್ = 인수.ಔಟ್_ಪುಟ್ / ಕಡತ.relative_to(인수.원본)
        ಔಟ್_ಪುಟ್.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(ಕಡತ.read_text())
        if not ಔಟ್_ಪುಟ್.exists() or ಔಟ್_ಪುಟ್.read_text() != 새원문:
            ಔಟ್_ಪುಟ್.write_text(새원문)

if __name__ == '__main__':
    ಪೂರೈಸು_ಆದೇಶ()

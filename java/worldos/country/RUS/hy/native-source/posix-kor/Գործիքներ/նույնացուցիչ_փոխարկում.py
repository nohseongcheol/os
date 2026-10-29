#!/usr/bin/env python3
"""한국어 C 식별자만 UCN으로 옮긴다. տող_արժեք_6ca8363c·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

արժենիշ_արժեք = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<նույնացուցիչ_արժեք>[^\W\d]\w*)', re.S | re.M)

def 변환(ԱՂԲՅՈՒՐ):
    def փոխարինել_արժեք(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(գրանշան_արժեք if ord(գրանշան_արժեք) < 128 else
                       ('\\u%04x' if ord(գրանշան_արժեք) <= 65535 else '\\U%08x') % ord(գրանշան_արժեք)
                       for գրանշան_արժեք in 일치[0])
    return արժենիշ_արժեք.sub(փոխարինել_արժեք, ԱՂԲՅՈՒՐ)

def կատարել_հրաման():
    해석기 = argparse.ArgumentParser()
    해석기.add_argument('원본', type=Path)
    해석기.add_argument('Ելք', type=Path)
    인수 = 해석기.parse_args()
    for Ֆայլ in sorted(인수.원본.rglob('*')):
        if Ֆայլ.suffix not in ('.c', '.h'):
            continue
        Ելք = 인수.Ելք / Ֆայլ.relative_to(인수.원본)
        Ելք.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(Ֆայլ.read_text())
        if not Ելք.exists() or Ելք.read_text() != 새원문:
            Ելք.write_text(새원문)

if __name__ == '__main__':
    կատարել_հրաման()

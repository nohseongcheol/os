#!/usr/bin/env python3
"""नेपाली C 식별자만 UCN으로 옮긴다. स्ट्रिङ_मान·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

टोकन_मान = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<परिचायक_मान>[^\W\d]\w*)', re.S | re.M)

def 변환(स्रोत):
    def बदल्नुहोस्_मान(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(वर्ण_मान if ord(वर्ण_मान) < 128 else
                       ('\\u%04x' if ord(वर्ण_मान) <= 65535 else '\\U%08x') % ord(वर्ण_मान)
                       for वर्ण_मान in 일치[0])
    return टोकन_मान.sub(बदल्नुहोस्_मान, स्रोत)

def कार्यान्वयन_गर्नुहोस्_आदेश():
    해석기 = argparse.ArgumentParser()
    해석기.add_argument('원본', type=Path)
    해석기.add_argument('출력', type=Path)
    तर्क = 해석기.parse_args()
    for फाइल in sorted(तर्क.원본.rglob('*')):
        if फाइल.suffix not in ('.c', '.h'):
            continue
        출력 = तर्क.출력 / फाइल.relative_to(तर्क.원본)
        출력.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(फाइल.read_text())
        if not 출력.exists() or 출력.read_text() != 새원문:
            출력.write_text(새원문)

if __name__ == '__main__':
    कार्यान्वयन_गर्नुहोस्_आदेश()

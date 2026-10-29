#!/usr/bin/env python3
"""हिंदी C 식별자만 UCN으로 옮긴다. स्ट्रिंग_मान·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

टोकन_मान = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<पहचानकर्ता_मान>[^\W\d]\w*)', re.S | re.M)

def रूपांतरित_करें_मान(स्रोत):
    def बदलें_मान(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(कैरेक्टर_मान if ord(कैरेक्टर_मान) < 128 else
                       ('\\u%04x' if ord(कैरेक्टर_मान) <= 65535 else '\\U%08x') % ord(कैरेक्टर_मान)
                       for कैरेक्टर_मान in 일치[0])
    return टोकन_मान.sub(बदलें_मान, स्रोत)

def निष्पादित_करें_आदेश():
    पार्सर_48ee4b1b = argparse.ArgumentParser()
    पार्सर_48ee4b1b.add_argument('원본', type=Path)
    पार्सर_48ee4b1b.add_argument('निर्गम', type=Path)
    तर्क = पार्सर_48ee4b1b.parse_args()
    for संचिका in sorted(तर्क.원본.rglob('*')):
        if संचिका.suffix not in ('.c', '.h'):
            continue
        निर्गम = तर्क.निर्गम / संचिका.relative_to(तर्क.원본)
        निर्गम.parent.mkdir(parents=True, exist_ok=True)
        새원문 = रूपांतरित_करें_मान(संचिका.read_text())
        if not निर्गम.exists() or निर्गम.read_text() != 새원문:
            निर्गम.write_text(새원문)

if __name__ == '__main__':
    निष्पादित_करें_आदेश()

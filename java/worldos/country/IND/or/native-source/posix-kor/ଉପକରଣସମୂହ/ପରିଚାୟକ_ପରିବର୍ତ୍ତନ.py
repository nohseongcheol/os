#!/usr/bin/env python3
"""한국어 C 식별자만 UCN으로 옮긴다. ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

ଟୋକନ୍_ମୂଲ୍ୟ = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<ପରିଚାୟକ_ମୂଲ୍ୟ>[^\W\d]\w*)', re.S | re.M)

def 변환(ଉତ୍ସ):
    def ପ୍ରତିସ୍ଥାପନ_ମୂଲ୍ୟ(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(ବର୍ଣ୍ଣ_ମୂଲ୍ୟ if ord(ବର୍ଣ୍ଣ_ମୂଲ୍ୟ) < 128 else
                       ('\\u%04x' if ord(ବର୍ଣ୍ଣ_ମୂଲ୍ୟ) <= 65535 else '\\U%08x') % ord(ବର୍ଣ୍ଣ_ମୂଲ୍ୟ)
                       for ବର୍ଣ୍ଣ_ମୂଲ୍ୟ in 일치[0])
    return ଟୋକନ୍_ମୂଲ୍ୟ.sub(ପ୍ରତିସ୍ଥାପନ_ମୂଲ୍ୟ, ଉତ୍ସ)

def ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ():
    해석기 = argparse.ArgumentParser()
    해석기.add_argument('원본', type=Path)
    해석기.add_argument('ନିର୍ଗମ', type=Path)
    인수 = 해석기.parse_args()
    for ଫାଇଲ in sorted(인수.원본.rglob('*')):
        if ଫାଇଲ.suffix not in ('.c', '.h'):
            continue
        ନିର୍ଗମ = 인수.ନିର୍ଗମ / ଫାଇଲ.relative_to(인수.원본)
        ନିର୍ଗମ.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(ଫାଇଲ.read_text())
        if not ନିର୍ଗମ.exists() or ନିର୍ଗମ.read_text() != 새원문:
            ନିର୍ଗମ.write_text(새원문)

if __name__ == '__main__':
    ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ()

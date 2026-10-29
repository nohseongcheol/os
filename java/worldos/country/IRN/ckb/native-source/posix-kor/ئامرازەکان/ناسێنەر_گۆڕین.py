#!/usr/bin/env python3
"""한국어 C 식별자만 UCN으로 옮긴다. رست_نرخ·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

فیشە_نرخ = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<ناسێنەر_نرخ>[^\W\d]\w*)', re.S | re.M)

def 변환(ژێدەر):
    def جێنشین_کردن_نرخ(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(نووسە_نرخ if ord(نووسە_نرخ) < 128 else
                       ('\\u%04x' if ord(نووسە_نرخ) <= 65535 else '\\U%08x') % ord(نووسە_نرخ)
                       for نووسە_نرخ in 일치[0])
    return فیشە_نرخ.sub(جێنشین_کردن_نرخ, ژێدەر)

def جێبەجێکردن_فەرمان():
    해석기 = argparse.ArgumentParser()
    해석기.add_argument('원본', type=Path)
    해석기.add_argument('출력', type=Path)
    인수 = 해석기.parse_args()
    for فایل in sorted(인수.원본.rglob('*')):
        if فایل.suffix not in ('.c', '.h'):
            continue
        출력 = 인수.출력 / فایل.relative_to(인수.원본)
        출력.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(فایل.read_text())
        if not 출력.exists() or 출력.read_text() != 새원문:
            출력.write_text(새원문)

if __name__ == '__main__':
    جێبەجێکردن_فەرمان()

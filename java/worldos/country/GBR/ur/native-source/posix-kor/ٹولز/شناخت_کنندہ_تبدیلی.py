#!/usr/bin/env python3
"""اردو C 식별자만 UCN으로 옮긴다. سلک_قدر·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

ٹوکن_قدر = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<شناخت_کنندہ_قدر>[^\W\d]\w*)', re.S | re.M)

def 변환(ماخذ_فائل):
    def بدلیں_قدر(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(کریکٹر_قدر if ord(کریکٹر_قدر) < 128 else
                       ('\\u%04x' if ord(کریکٹر_قدر) <= 65535 else '\\U%08x') % ord(کریکٹر_قدر)
                       for کریکٹر_قدر in 일치[0])
    return ٹوکن_قدر.sub(بدلیں_قدر, ماخذ_فائل)

def نفاذ_کریں_حکم():
    해석기 = argparse.ArgumentParser()
    해석기.add_argument('원본', type=Path)
    해석기.add_argument('اخراج_کا_مقام', type=Path)
    دلائل = 해석기.parse_args()
    for فائل_کا_نام in sorted(دلائل.원본.rglob('*')):
        if فائل_کا_نام.suffix not in ('.c', '.h'):
            continue
        اخراج_کا_مقام = دلائل.اخراج_کا_مقام / فائل_کا_نام.relative_to(دلائل.원본)
        اخراج_کا_مقام.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(فائل_کا_نام.read_text())
        if not اخراج_کا_مقام.exists() or اخراج_کا_مقام.read_text() != 새원문:
            اخراج_کا_مقام.write_text(새원문)

if __name__ == '__main__':
    نفاذ_کریں_حکم()

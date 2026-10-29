#!/usr/bin/env python3
"""한국어 C 식별자만 UCN으로 옮긴다. سٹرنگ_قدر·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

ٹوکن_قدر = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<شناخت_کرنڑ_آلا_قدر>[^\W\d]\w*)', re.S | re.M)

def 변환(ماخذ):
    def بدلو_قدر(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(کریکٹر_قدر if ord(کریکٹر_قدر) < 128 else
                       ('\\u%04x' if ord(کریکٹر_قدر) <= 65535 else '\\U%08x') % ord(کریکٹر_قدر)
                       for کریکٹر_قدر in 일치[0])
    return ٹوکن_قدر.sub(بدلو_قدر, ماخذ)

def نفاذ_کرو_حکم():
    해석기 = argparse.ArgumentParser()
    해석기.add_argument('원본', type=Path)
    해석기.add_argument('출력', type=Path)
    인수 = 해석기.parse_args()
    for فائل in sorted(인수.원본.rglob('*')):
        if فائل.suffix not in ('.c', '.h'):
            continue
        출력 = 인수.출력 / فائل.relative_to(인수.원본)
        출력.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(فائل.read_text())
        if not 출력.exists() or 출력.read_text() != 새원문:
            출력.write_text(새원문)

if __name__ == '__main__':
    نفاذ_کرو_حکم()

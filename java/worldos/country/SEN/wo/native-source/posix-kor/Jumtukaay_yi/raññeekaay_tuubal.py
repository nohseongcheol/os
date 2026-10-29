#!/usr/bin/env python3
"""한국어 C 식별자만 UCN으로 옮긴다. araf_yu_bennoo_xëyma·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

jeton_xëyma = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<raññeekaay_xëyma>[^\W\d]\w*)', re.S | re.M)

def 변환(Cosaan):
    def delloosi_xëyma(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(Araf_xëyma if ord(Araf_xëyma) < 128 else
                       ('\\u%04x' if ord(Araf_xëyma) <= 65535 else '\\U%08x') % ord(Araf_xëyma)
                       for Araf_xëyma in 일치[0])
    return jeton_xëyma.sub(delloosi_xëyma, Cosaan)

def def_ndigel():
    해석기 = argparse.ArgumentParser()
    해석기.add_argument('원본', type=Path)
    해석기.add_argument('출력', type=Path)
    인수 = 해석기.parse_args()
    for bara_denc in sorted(인수.원본.rglob('*')):
        if bara_denc.suffix not in ('.c', '.h'):
            continue
        출력 = 인수.출력 / bara_denc.relative_to(인수.원본)
        출력.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(bara_denc.read_text())
        if not 출력.exists() or 출력.read_text() != 새원문:
            출력.write_text(새원문)

if __name__ == '__main__':
    def_ndigel()

#!/usr/bin/env python3
"""Isi_Zulu C 식별자만 UCN으로 옮긴다. uchunge_inani·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

ithokhini_inani = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<isivezi_inani>[^\W\d]\w*)', re.S | re.M)

def 변환(umthombo):
    def faka_endaweni_inani(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(uhlamvusimo_inani if ord(uhlamvusimo_inani) < 128 else
                       ('\\u%04x' if ord(uhlamvusimo_inani) <= 65535 else '\\U%08x') % ord(uhlamvusimo_inani)
                       for uhlamvusimo_inani in 일치[0])
    return ithokhini_inani.sub(faka_endaweni_inani, umthombo)

def yenza_umyalo():
    해석기 = argparse.ArgumentParser()
    해석기.add_argument('원본', type=Path)
    해석기.add_argument('출력', type=Path)
    인수 = 해석기.parse_args()
    for Ihele in sorted(인수.원본.rglob('*')):
        if Ihele.suffix not in ('.c', '.h'):
            continue
        출력 = 인수.출력 / Ihele.relative_to(인수.원본)
        출력.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(Ihele.read_text())
        if not 출력.exists() or 출력.read_text() != 새원문:
            출력.write_text(새원문)

if __name__ == '__main__':
    yenza_umyalo()

#!/usr/bin/env python3
"""Cymraeg C 식별자만 UCN으로 옮긴다. testun_VALUE·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

tocyn_VALUE_eb540501 = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<dynodwr_VALUE>[^\W\d]\w*)', re.S | re.M)

def CONVERT_VALUE(FFYNHONNELL):
    def REPLACE_VALUE(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(nod_VALUE if ord(nod_VALUE) < 128 else
                       ('\\u%04x' if ord(nod_VALUE) <= 65535 else '\\U%08x') % ord(nod_VALUE)
                       for nod_VALUE in 일치[0])
    return tocyn_VALUE_eb540501.sub(REPLACE_VALUE, FFYNHONNELL)

def Gweithredu_gorchymyn():
    해석기 = argparse.ArgumentParser()
    해석기.add_argument('원본', type=Path)
    해석기.add_argument('Allbwn', type=Path)
    인수 = 해석기.parse_args()
    for Ffeil in sorted(인수.원본.rglob('*')):
        if Ffeil.suffix not in ('.c', '.h'):
            continue
        Allbwn = 인수.Allbwn / Ffeil.relative_to(인수.원본)
        Allbwn.parent.mkdir(parents=True, exist_ok=True)
        새원문 = CONVERT_VALUE(Ffeil.read_text())
        if not Allbwn.exists() or Allbwn.read_text() != 새원문:
            Allbwn.write_text(새원문)

if __name__ == '__main__':
    Gweithredu_gorchymyn()

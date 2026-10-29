#!/usr/bin/env python3
"""한국어 C 식별자만 UCN으로 옮긴다. 문자열·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

토큰 = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<식별자>[^\W\d]\w*)', re.S | re.M)

def 변환(Born):
    def 바꾸기(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(글자 if ord(글자) < 128 else
                       ('\\u%04x' if ord(글자) <= 65535 else '\\U%08x') % ord(글자)
                       for 글자 in 일치[0])
    return 토큰.sub(바꾸기, Born)

def 실행():
    해석기 = argparse.ArgumentParser()
    해석기.add_argument('원본', type=Path)
    해석기.add_argument('Utgaav', type=Path)
    Argumenten = 해석기.parse_args()
    for Datei in sorted(Argumenten.원본.rglob('*')):
        if Datei.suffix not in ('.c', '.h'):
            continue
        Utgaav = Argumenten.Utgaav / Datei.relative_to(Argumenten.원본)
        Utgaav.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(Datei.read_text())
        if not Utgaav.exists() or Utgaav.read_text() != 새원문:
            Utgaav.write_text(새원문)

if __name__ == '__main__':
    실행()

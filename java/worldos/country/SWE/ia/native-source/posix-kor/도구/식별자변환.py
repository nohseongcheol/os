#!/usr/bin/env python3
"""한국어 C 식별자만 UCN으로 옮긴다. 문자열·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

토큰 = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<식별자>[^\W\d]\w*)', re.S | re.M)

def 변환(Fonte):
    def 바꾸기(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(글자 if ord(글자) < 128 else
                       ('\\u%04x' if ord(글자) <= 65535 else '\\U%08x') % ord(글자)
                       for 글자 in 일치[0])
    return 토큰.sub(바꾸기, Fonte)

def 실행():
    해석기 = argparse.ArgumentParser()
    해석기.add_argument('원본', type=Path)
    해석기.add_argument('Exito', type=Path)
    Argumentos = 해석기.parse_args()
    for 파일 in sorted(Argumentos.원본.rglob('*')):
        if 파일.suffix not in ('.c', '.h'):
            continue
        Exito = Argumentos.Exito / 파일.relative_to(Argumentos.원본)
        Exito.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(파일.read_text())
        if not Exito.exists() or Exito.read_text() != 새원문:
            Exito.write_text(새원문)

if __name__ == '__main__':
    실행()

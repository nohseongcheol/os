#!/usr/bin/env python3
"""한국어 C 식별자만 UCN으로 옮긴다. сатр_қимат_6ca8363c·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

токен_қимат = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<идентификатор_қимат>[^\W\d]\w*)', re.S | re.M)

def 변환(манбаъ):
    def ҷойгузин_кардан_қимат(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(аломат_қимат_068c2631 if ord(аломат_қимат_068c2631) < 128 else
                       ('\\u%04x' if ord(аломат_қимат_068c2631) <= 65535 else '\\U%08x') % ord(аломат_қимат_068c2631)
                       for аломат_қимат_068c2631 in 일치[0])
    return токен_қимат.sub(ҷойгузин_кардан_қимат, манбаъ)

def иҷро_кардан_фармон():
    해석기 = argparse.ArgumentParser()
    해석기.add_argument('원본', type=Path)
    해석기.add_argument('출력', type=Path)
    인수 = 해석기.parse_args()
    for Файл in sorted(인수.원본.rglob('*')):
        if Файл.suffix not in ('.c', '.h'):
            continue
        출력 = 인수.출력 / Файл.relative_to(인수.원본)
        출력.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(Файл.read_text())
        if not 출력.exists() or 출력.read_text() != 새원문:
            출력.write_text(새원문)

if __name__ == '__main__':
    иҷро_кардан_фармон()

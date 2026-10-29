#!/usr/bin/env python3
"""한국어 C 식별자만 UCN으로 옮긴다. qimiaq_atuutilik·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

토큰 = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<식별자>[^\W\d]\w*)', re.S | re.M)

def 변환(pivviujuq):
    def kinguvvirli_atuutilik(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(immikkuuqtuq_atuutilik if ord(immikkuuqtuq_atuutilik) < 128 else
                       ('\\u%04x' if ord(immikkuuqtuq_atuutilik) <= 65535 else '\\U%08x') % ord(immikkuuqtuq_atuutilik)
                       for immikkuuqtuq_atuutilik in 일치[0])
    return 토큰.sub(kinguvvirli_atuutilik, pivviujuq)

def 실행():
    해석기 = argparse.ArgumentParser()
    해석기.add_argument('원본', type=Path)
    해석기.add_argument('출력', type=Path)
    인수 = 해석기.parse_args()
    for ini in sorted(인수.원본.rglob('*')):
        if ini.suffix not in ('.c', '.h'):
            continue
        출력 = 인수.출력 / ini.relative_to(인수.원본)
        출력.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(ini.read_text())
        if not 출력.exists() or 출력.read_text() != 새원문:
            출력.write_text(새원문)

if __name__ == '__main__':
    실행()

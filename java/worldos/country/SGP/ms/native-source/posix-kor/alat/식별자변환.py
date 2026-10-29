#!/usr/bin/env python3
"""Melayu C 식별자만 UCN으로 옮긴다. rentetan_VALUE·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

token_VALUE = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<식별자>[^\W\d]\w*)', re.S | re.M)

def tukar_VALUE(SUMBER):
    def ganti_VALUE(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(aksara_VALUE if ord(aksara_VALUE) < 128 else
                       ('\\u%04x' if ord(aksara_VALUE) <= 65535 else '\\U%08x') % ord(aksara_VALUE)
                       for aksara_VALUE in 일치[0])
    return token_VALUE.sub(ganti_VALUE, SUMBER)

def laksanakan_perintah():
    penghurai_48ee4b1b = argparse.ArgumentParser()
    penghurai_48ee4b1b.add_argument('원본', type=Path)
    penghurai_48ee4b1b.add_argument('출력', type=Path)
    인수 = penghurai_48ee4b1b.parse_args()
    for Fail in sorted(인수.원본.rglob('*')):
        if Fail.suffix not in ('.c', '.h'):
            continue
        출력 = 인수.출력 / Fail.relative_to(인수.원본)
        출력.parent.mkdir(parents=True, exist_ok=True)
        새원문 = tukar_VALUE(Fail.read_text())
        if not 출력.exists() or 출력.read_text() != 새원문:
            출력.write_text(새원문)

if __name__ == '__main__':
    laksanakan_perintah()

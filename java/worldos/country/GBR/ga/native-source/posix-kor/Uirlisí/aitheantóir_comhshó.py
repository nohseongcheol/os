#!/usr/bin/env python3
"""Gaeilge C 식별자만 UCN으로 옮긴다. teaghrán_VALUE·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

licín_VALUE = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<aitheantóir_VALUE>[^\W\d]\w*)', re.S | re.M)

def CONVERT_VALUE(FOINSE):
    def REPLACE_VALUE(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(carachtar_VALUE if ord(carachtar_VALUE) < 128 else
                       ('\\u%04x' if ord(carachtar_VALUE) <= 65535 else '\\U%08x') % ord(carachtar_VALUE)
                       for carachtar_VALUE in 일치[0])
    return licín_VALUE.sub(REPLACE_VALUE, FOINSE)

def Rith_ordú():
    해석기 = argparse.ArgumentParser()
    해석기.add_argument('원본', type=Path)
    해석기.add_argument('Aschur', type=Path)
    Argóintí = 해석기.parse_args()
    for Comhad in sorted(Argóintí.원본.rglob('*')):
        if Comhad.suffix not in ('.c', '.h'):
            continue
        Aschur = Argóintí.Aschur / Comhad.relative_to(Argóintí.원본)
        Aschur.parent.mkdir(parents=True, exist_ok=True)
        새원문 = CONVERT_VALUE(Comhad.read_text())
        if not Aschur.exists() or Aschur.read_text() != 새원문:
            Aschur.write_text(새원문)

if __name__ == '__main__':
    Rith_ordú()

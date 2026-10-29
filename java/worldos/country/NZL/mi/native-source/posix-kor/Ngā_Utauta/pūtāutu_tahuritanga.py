#!/usr/bin/env python3
"""Reo_Māori C 식별자만 UCN으로 옮긴다. aho_uara·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

tohu_uara_eb540501 = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<pūtāutu_uara>[^\W\d]\w*)', re.S | re.M)

def CONVERT_uara(pūtake):
    def REPLACE_uara(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(pūāhua_uara if ord(pūāhua_uara) < 128 else
                       ('\\u%04x' if ord(pūāhua_uara) <= 65535 else '\\U%08x') % ord(pūāhua_uara)
                       for pūāhua_uara in 일치[0])
    return tohu_uara_eb540501.sub(REPLACE_uara, pūtake)

def kawe_tono():
    해석기 = argparse.ArgumentParser()
    해석기.add_argument('원본', type=Path)
    해석기.add_argument('출력', type=Path)
    인수 = 해석기.parse_args()
    for Kōnae in sorted(인수.원본.rglob('*')):
        if Kōnae.suffix not in ('.c', '.h'):
            continue
        출력 = 인수.출력 / Kōnae.relative_to(인수.원본)
        출력.parent.mkdir(parents=True, exist_ok=True)
        새원문 = CONVERT_uara(Kōnae.read_text())
        if not 출력.exists() or 출력.read_text() != 새원문:
            출력.write_text(새원문)

if __name__ == '__main__':
    kawe_tono()

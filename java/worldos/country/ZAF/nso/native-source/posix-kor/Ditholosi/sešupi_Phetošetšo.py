#!/usr/bin/env python3
"""한국어 C 식별자만 UCN으로 옮긴다. molokoloko_boleng·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

thokene_boleng = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<sešupi_boleng>[^\W\d]\w*)', re.S | re.M)

def 변환(mohlodi):
    def fetola_boleng(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(tlhaka_boleng if ord(tlhaka_boleng) < 128 else
                       ('\\u%04x' if ord(tlhaka_boleng) <= 65535 else '\\U%08x') % ord(tlhaka_boleng)
                       for tlhaka_boleng in 일치[0])
    return thokene_boleng.sub(fetola_boleng, mohlodi)

def phethagatša_taelo():
    해석기 = argparse.ArgumentParser()
    해석기.add_argument('원본', type=Path)
    해석기.add_argument('출력', type=Path)
    인수 = 해석기.parse_args()
    for Faele in sorted(인수.원본.rglob('*')):
        if Faele.suffix not in ('.c', '.h'):
            continue
        출력 = 인수.출력 / Faele.relative_to(인수.원본)
        출력.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(Faele.read_text())
        if not 출력.exists() or 출력.read_text() != 새원문:
            출력.write_text(새원문)

if __name__ == '__main__':
    phethagatša_taelo()

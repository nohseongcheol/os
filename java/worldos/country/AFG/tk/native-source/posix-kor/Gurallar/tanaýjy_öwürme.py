#!/usr/bin/env python3
"""한국어 C 식별자만 UCN으로 옮긴다. setir_baha_6ca8363c·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

token_baha = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<tanaýjy_baha>[^\W\d]\w*)', re.S | re.M)

def 변환(Çeşme):
    def çalşyr_baha(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(nyşan_baha_068c2631 if ord(nyşan_baha_068c2631) < 128 else
                       ('\\u%04x' if ord(nyşan_baha_068c2631) <= 65535 else '\\U%08x') % ord(nyşan_baha_068c2631)
                       for nyşan_baha_068c2631 in 일치[0])
    return token_baha.sub(çalşyr_baha, Çeşme)

def ýerine_ýetir_buýruk():
    해석기 = argparse.ArgumentParser()
    해석기.add_argument('원본', type=Path)
    해석기.add_argument('출력', type=Path)
    인수 = 해석기.parse_args()
    for Faýl in sorted(인수.원본.rglob('*')):
        if Faýl.suffix not in ('.c', '.h'):
            continue
        출력 = 인수.출력 / Faýl.relative_to(인수.원본)
        출력.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(Faýl.read_text())
        if not 출력.exists() or 출력.read_text() != 새원문:
            출력.write_text(새원문)

if __name__ == '__main__':
    ýerine_ýetir_buýruk()

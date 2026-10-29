#!/usr/bin/env python3
"""Ikinyarwanda C 식별자만 UCN으로 옮긴다. igicenteruro_agaciro·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

tike_agaciro = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<indanga_agaciro>[^\W\d]\w*)', re.S | re.M)

def 변환(Inkomoko):
    def gusimbuza_agaciro(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(inyuguti_agaciro if ord(inyuguti_agaciro) < 128 else
                       ('\\u%04x' if ord(inyuguti_agaciro) <= 65535 else '\\U%08x') % ord(inyuguti_agaciro)
                       for inyuguti_agaciro in 일치[0])
    return tike_agaciro.sub(gusimbuza_agaciro, Inkomoko)

def gukora_ibwiriza():
    해석기 = argparse.ArgumentParser()
    해석기.add_argument('원본', type=Path)
    해석기.add_argument('출력', type=Path)
    인수 = 해석기.parse_args()
    for Idosiye in sorted(인수.원본.rglob('*')):
        if Idosiye.suffix not in ('.c', '.h'):
            continue
        출력 = 인수.출력 / Idosiye.relative_to(인수.원본)
        출력.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(Idosiye.read_text())
        if not 출력.exists() or 출력.read_text() != 새원문:
            출력.write_text(새원문)

if __name__ == '__main__':
    gukora_ibwiriza()

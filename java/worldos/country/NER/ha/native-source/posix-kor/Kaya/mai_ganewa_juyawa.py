#!/usr/bin/env python3
"""한국어 C 식별자만 UCN으로 옮긴다. Zare_Daraja·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

token_Daraja = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<mai_ganewa_Daraja>[^\W\d]\w*)', re.S | re.M)

def 변환(tushe):
    def Maye_gurbi_Daraja(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(Harafi_Daraja if ord(Harafi_Daraja) < 128 else
                       ('\\u%04x' if ord(Harafi_Daraja) <= 65535 else '\\U%08x') % ord(Harafi_Daraja)
                       for Harafi_Daraja in 일치[0])
    return token_Daraja.sub(Maye_gurbi_Daraja, tushe)

def gudanar_Umarni():
    tatsar_manhaja_48ee4b1b = argparse.ArgumentParser()
    tatsar_manhaja_48ee4b1b.add_argument('원본', type=Path)
    tatsar_manhaja_48ee4b1b.add_argument('출력', type=Path)
    인수 = tatsar_manhaja_48ee4b1b.parse_args()
    for Fayil in sorted(인수.원본.rglob('*')):
        if Fayil.suffix not in ('.c', '.h'):
            continue
        출력 = 인수.출력 / Fayil.relative_to(인수.원본)
        출력.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(Fayil.read_text())
        if not 출력.exists() or 출력.read_text() != 새원문:
            출력.write_text(새원문)

if __name__ == '__main__':
    gudanar_Umarni()

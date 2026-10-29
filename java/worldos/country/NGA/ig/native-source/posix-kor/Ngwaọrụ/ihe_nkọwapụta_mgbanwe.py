#!/usr/bin/env python3
"""한국어 C 식별자만 UCN으로 옮긴다. ùsòròokwū_valuu·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

akara_valuu_eb540501 = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<ihe_nkọwapụta_valuu>[^\W\d]\w*)', re.S | re.M)

def 변환(ebensìbịa):
    def doghachi_valuu(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(mkpụrụedemede_valuu if ord(mkpụrụedemede_valuu) < 128 else
                       ('\\u%04x' if ord(mkpụrụedemede_valuu) <= 65535 else '\\U%08x') % ord(mkpụrụedemede_valuu)
                       for mkpụrụedemede_valuu in 일치[0])
    return akara_valuu_eb540501.sub(doghachi_valuu, ebensìbịa)

def mee_nnyemiwu():
    해석기 = argparse.ArgumentParser()
    해석기.add_argument('원본', type=Path)
    해석기.add_argument('출력', type=Path)
    인수 = 해석기.parse_args()
    for Faịlụ in sorted(인수.원본.rglob('*')):
        if Faịlụ.suffix not in ('.c', '.h'):
            continue
        출력 = 인수.출력 / Faịlụ.relative_to(인수.원본)
        출력.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(Faịlụ.read_text())
        if not 출력.exists() or 출력.read_text() != 새원문:
            출력.write_text(새원문)

if __name__ == '__main__':
    mee_nnyemiwu()

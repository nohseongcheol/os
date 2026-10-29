#!/usr/bin/env python3
"""isiXhosa C 식별자만 UCN으로 옮긴다. uluhlu_lweekharektha_ixabiso·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

ithokeni_ixabiso = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<isalathisi_ixabiso>[^\W\d]\w*)', re.S | re.M)

def 변환(UMTHOMBO):
    def faka_endaweni_yenye_ixabiso(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(ikharakhtha_ixabiso if ord(ikharakhtha_ixabiso) < 128 else
                       ('\\u%04x' if ord(ikharakhtha_ixabiso) <= 65535 else '\\U%08x') % ord(ikharakhtha_ixabiso)
                       for ikharakhtha_ixabiso in 일치[0])
    return ithokeni_ixabiso.sub(faka_endaweni_yenye_ixabiso, UMTHOMBO)

def ukwenza_umyalelo():
    해석기 = argparse.ArgumentParser()
    해석기.add_argument('원본', type=Path)
    해석기.add_argument('출력', type=Path)
    인수 = 해석기.parse_args()
    for iFayili in sorted(인수.원본.rglob('*')):
        if iFayili.suffix not in ('.c', '.h'):
            continue
        출력 = 인수.출력 / iFayili.relative_to(인수.원본)
        출력.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(iFayili.read_text())
        if not 출력.exists() or 출력.read_text() != 새원문:
            출력.write_text(새원문)

if __name__ == '__main__':
    ukwenza_umyalelo()

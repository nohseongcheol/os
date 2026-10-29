#!/usr/bin/env python3
"""한국어 C 식별자만 UCN으로 옮긴다. tungo_thamani·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

tuzo_thamani = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<kitambulishi_thamani>[^\W\d]\w*)', re.S | re.M)

def 변환(chanzo):
    def badilisha_thamani(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(kibambo_thamani if ord(kibambo_thamani) < 128 else
                       ('\\u%04x' if ord(kibambo_thamani) <= 65535 else '\\U%08x') % ord(kibambo_thamani)
                       for kibambo_thamani in 일치[0])
    return tuzo_thamani.sub(badilisha_thamani, chanzo)

def tekeleza_amri():
    kichanganuzi_48ee4b1b = argparse.ArgumentParser()
    kichanganuzi_48ee4b1b.add_argument('원본', type=Path)
    kichanganuzi_48ee4b1b.add_argument('출력', type=Path)
    인수 = kichanganuzi_48ee4b1b.parse_args()
    for faili in sorted(인수.원본.rglob('*')):
        if faili.suffix not in ('.c', '.h'):
            continue
        출력 = 인수.출력 / faili.relative_to(인수.원본)
        출력.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(faili.read_text())
        if not 출력.exists() or 출력.read_text() != 새원문:
            출력.write_text(새원문)

if __name__ == '__main__':
    tekeleza_amri()

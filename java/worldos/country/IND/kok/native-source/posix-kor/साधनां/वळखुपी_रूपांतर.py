#!/usr/bin/env python3
"""한국어 C 식별자만 UCN으로 옮긴다. स्ट्रिंग_मोल·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

टोकन_मोल = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<वळखुपी_मोल>[^\W\d]\w*)', re.S | re.M)

def CONVERT_मोल(स्त्रोत):
    def REPLACE_मोल(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(वर्ण_मोल if ord(वर्ण_मोल) < 128 else
                       ('\\u%04x' if ord(वर्ण_मोल) <= 65535 else '\\U%08x') % ord(वर्ण_मोल)
                       for वर्ण_मोल in 일치[0])
    return टोकन_मोल.sub(REPLACE_मोल, स्त्रोत)

def पाळो_दिवचो_आदेश():
    해석기 = argparse.ArgumentParser()
    해석기.add_argument('원본', type=Path)
    해석기.add_argument('출력', type=Path)
    인수 = 해석기.parse_args()
    for फायल in sorted(인수.원본.rglob('*')):
        if फायल.suffix not in ('.c', '.h'):
            continue
        출력 = 인수.출력 / फायल.relative_to(인수.원본)
        출력.parent.mkdir(parents=True, exist_ok=True)
        새원문 = CONVERT_मोल(फायल.read_text())
        if not 출력.exists() or 출력.read_text() != 새원문:
            출력.write_text(새원문)

if __name__ == '__main__':
    पाळो_दिवचो_आदेश()

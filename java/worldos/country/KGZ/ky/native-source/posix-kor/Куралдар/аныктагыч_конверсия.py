#!/usr/bin/env python3
"""한국어 C 식별자만 UCN으로 옮긴다. сап_маани·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

токен_маани = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<аныктагыч_маани>[^\W\d]\w*)', re.S | re.M)

def айландыруу_маани(Булак):
    def орун_алмаштыруу_маани(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(символ_маани_068c2631 if ord(символ_маани_068c2631) < 128 else
                       ('\\u%04x' if ord(символ_маани_068c2631) <= 65535 else '\\U%08x') % ord(символ_маани_068c2631)
                       for символ_маани_068c2631 in 일치[0])
    return токен_маани.sub(орун_алмаштыруу_маани, Булак)

def аткаруу_буйрук():
    해석기 = argparse.ArgumentParser()
    해석기.add_argument('원본', type=Path)
    해석기.add_argument('Чыгыш', type=Path)
    인수 = 해석기.parse_args()
    for Файл in sorted(인수.원본.rglob('*')):
        if Файл.suffix not in ('.c', '.h'):
            continue
        Чыгыш = 인수.Чыгыш / Файл.relative_to(인수.원본)
        Чыгыш.parent.mkdir(parents=True, exist_ok=True)
        새원문 = айландыруу_маани(Файл.read_text())
        if not Чыгыш.exists() or Чыгыш.read_text() != 새원문:
            Чыгыш.write_text(새원문)

if __name__ == '__main__':
    аткаруу_буйрук()

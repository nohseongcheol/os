#!/usr/bin/env python3
"""한국어 C 식별자만 UCN으로 옮긴다. радок_значэнне·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

маркер_значэнне_eb540501 = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<ідэнтыфікатар_значэнне>[^\W\d]\w*)', re.S | re.M)

def 변환(КРЫНІЦА):
    def замяніць_значэнне(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(сімвал_значэнне_068c2631 if ord(сімвал_значэнне_068c2631) < 128 else
                       ('\\u%04x' if ord(сімвал_значэнне_068c2631) <= 65535 else '\\U%08x') % ord(сімвал_значэнне_068c2631)
                       for сімвал_значэнне_068c2631 in 일치[0])
    return маркер_значэнне_eb540501.sub(замяніць_значэнне, КРЫНІЦА)

def выканаць_каманда():
    аналізатар_48ee4b1b = argparse.ArgumentParser()
    аналізатар_48ee4b1b.add_argument('원본', type=Path)
    аналізатар_48ee4b1b.add_argument('Выхад', type=Path)
    인수 = аналізатар_48ee4b1b.parse_args()
    for Файл in sorted(인수.원본.rglob('*')):
        if Файл.suffix not in ('.c', '.h'):
            continue
        Выхад = 인수.Выхад / Файл.relative_to(인수.원본)
        Выхад.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(Файл.read_text())
        if not Выхад.exists() or Выхад.read_text() != 새원문:
            Выхад.write_text(새원문)

if __name__ == '__main__':
    выканаць_каманда()

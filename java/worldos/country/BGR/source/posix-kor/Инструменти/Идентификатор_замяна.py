#!/usr/bin/env python3
"""Български C 식별자만 UCN으로 옮긴다. низ_стойност·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

код_стойност_eb540501 = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<Идентификатор_стойност>[^\W\d]\w*)', re.S | re.M)

def преобразувам_стойност(ИЗТОЧНИК):
    def 바꾸기(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(знак_стойност if ord(знак_стойност) < 128 else
                       ('\\u%04x' if ord(знак_стойност) <= 65535 else '\\U%08x') % ord(знак_стойност)
                       for знак_стойност in 일치[0])
    return код_стойност_eb540501.sub(바꾸기, ИЗТОЧНИК)

def изпълнявам_команда():
    анализатор_48ee4b1b = argparse.ArgumentParser()
    анализатор_48ee4b1b.add_argument('원본', type=Path)
    анализатор_48ee4b1b.add_argument('Изход', type=Path)
    Параметри = анализатор_48ee4b1b.parse_args()
    for Файл in sorted(Параметри.원본.rglob('*')):
        if Файл.suffix not in ('.c', '.h'):
            continue
        Изход = Параметри.Изход / Файл.relative_to(Параметри.원본)
        Изход.parent.mkdir(parents=True, exist_ok=True)
        새원문 = преобразувам_стойност(Файл.read_text())
        if not Изход.exists() or Изход.read_text() != 새원문:
            Изход.write_text(새원문)

if __name__ == '__main__':
    изпълнявам_команда()

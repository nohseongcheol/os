#!/usr/bin/env python3
"""українська C 식별자만 UCN으로 옮긴다. рядок_значення·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

токен_значення = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<ідентифікатор_значення>[^\W\d]\w*)', re.S | re.M)

def перетворити_значення(вихіднийКод):
    def 바꾸기(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(символ_значення_068c2631 if ord(символ_значення_068c2631) < 128 else
                       ('\\u%04x' if ord(символ_значення_068c2631) <= 65535 else '\\U%08x') % ord(символ_значення_068c2631)
                       for символ_значення_068c2631 in 일치[0])
    return токен_значення.sub(바꾸기, вихіднийКод)

def Виконати_команда():
    аналізатор_48ee4b1b = argparse.ArgumentParser()
    аналізатор_48ee4b1b.add_argument('원본', type=Path)
    аналізатор_48ee4b1b.add_argument('Вивід', type=Path)
    аргументи = аналізатор_48ee4b1b.parse_args()
    for файл in sorted(аргументи.원본.rglob('*')):
        if файл.suffix not in ('.c', '.h'):
            continue
        Вивід = аргументи.Вивід / файл.relative_to(аргументи.원본)
        Вивід.parent.mkdir(parents=True, exist_ok=True)
        새원문 = перетворити_значення(файл.read_text())
        if not Вивід.exists() or Вивід.read_text() != 새원문:
            Вивід.write_text(새원문)

if __name__ == '__main__':
    Виконати_команда()

#!/usr/bin/env python3
"""한국어 C 식별자만 UCN으로 옮긴다. ниска_вриједност·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

токен_вриједност = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<идентификатор_вриједност>[^\W\d]\w*)', re.S | re.M)

def конвертовати_вриједност(ИЗВОР):
    def замијенити_вриједност(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(знак_вриједност if ord(знак_вриједност) < 128 else
                       ('\\u%04x' if ord(знак_вриједност) <= 65535 else '\\U%08x') % ord(знак_вриједност)
                       for знак_вриједност in 일치[0])
    return токен_вриједност.sub(замијенити_вриједност, ИЗВОР)

def Изврши_команда():
    анализатор_48ee4b1b = argparse.ArgumentParser()
    анализатор_48ee4b1b.add_argument('원본', type=Path)
    анализатор_48ee4b1b.add_argument('Излаз', type=Path)
    Аргументи = анализатор_48ee4b1b.parse_args()
    for Датотека in sorted(Аргументи.원본.rglob('*')):
        if Датотека.suffix not in ('.c', '.h'):
            continue
        Излаз = Аргументи.Излаз / Датотека.relative_to(Аргументи.원본)
        Излаз.parent.mkdir(parents=True, exist_ok=True)
        새원문 = конвертовати_вриједност(Датотека.read_text())
        if not Излаз.exists() or Излаз.read_text() != 새원문:
            Излаз.write_text(새원문)

if __name__ == '__main__':
    Изврши_команда()

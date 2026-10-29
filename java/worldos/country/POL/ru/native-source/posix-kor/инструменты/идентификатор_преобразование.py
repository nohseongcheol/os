#!/usr/bin/env python3
"""русский C 식별자만 UCN으로 옮긴다. строка_ЗНАЧЕН·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

токен_ЗНАЧЕН = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<идентификатор_ЗНАЧЕН>[^\W\d]\w*)', re.S | re.M)

def ПРЕОБР_ЗНАЧЕН(исходныйКод):
    def ЗАМЕНИТЬ_ЗНАЧЕН(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(знак_ЗНАЧЕН if ord(знак_ЗНАЧЕН) < 128 else
                       ('\\u%04x' if ord(знак_ЗНАЧЕН) <= 65535 else '\\U%08x') % ord(знак_ЗНАЧЕН)
                       for знак_ЗНАЧЕН in 일치[0])
    return токен_ЗНАЧЕН.sub(ЗАМЕНИТЬ_ЗНАЧЕН, исходныйКод)

def 실행():
    анализатор_48ee4b1b = argparse.ArgumentParser()
    анализатор_48ee4b1b.add_argument('원본', type=Path)
    анализатор_48ee4b1b.add_argument('текстовыйВывод', type=Path)
    аргументы = анализатор_48ee4b1b.parse_args()
    for файл in sorted(аргументы.원본.rglob('*')):
        if файл.suffix not in ('.c', '.h'):
            continue
        текстовыйВывод = аргументы.текстовыйВывод / файл.relative_to(аргументы.원본)
        текстовыйВывод.parent.mkdir(parents=True, exist_ok=True)
        새원문 = ПРЕОБР_ЗНАЧЕН(файл.read_text())
        if not текстовыйВывод.exists() or текстовыйВывод.read_text() != 새원문:
            текстовыйВывод.write_text(새원문)

if __name__ == '__main__':
    실행()

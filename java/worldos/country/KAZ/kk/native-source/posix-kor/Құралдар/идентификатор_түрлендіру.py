#!/usr/bin/env python3
"""한국어 C 식별자만 UCN으로 옮긴다. жол_мән_6ca8363c·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

токен_мән = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<идентификатор_мән>[^\W\d]\w*)', re.S | re.M)

def Түрлендіру_мән(Неден):
    def ауыстыру_мән(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(таңба_мән if ord(таңба_мән) < 128 else
                       ('\\u%04x' if ord(таңба_мән) <= 65535 else '\\U%08x') % ord(таңба_мән)
                       for таңба_мән in 일치[0])
    return токен_мән.sub(ауыстыру_мән, Неден)

def орындау_пәрмен():
    талдау_құралы_48ee4b1b = argparse.ArgumentParser()
    талдау_құралы_48ee4b1b.add_argument('원본', type=Path)
    талдау_құралы_48ee4b1b.add_argument('Шығысы', type=Path)
    Аргументтер = талдау_құралы_48ee4b1b.parse_args()
    for Файл in sorted(Аргументтер.원본.rglob('*')):
        if Файл.suffix not in ('.c', '.h'):
            continue
        Шығысы = Аргументтер.Шығысы / Файл.relative_to(Аргументтер.원본)
        Шығысы.parent.mkdir(parents=True, exist_ok=True)
        새원문 = Түрлендіру_мән(Файл.read_text())
        if not Шығысы.exists() or Шығысы.read_text() != 새원문:
            Шығысы.write_text(새원문)

if __name__ == '__main__':
    орындау_пәрмен()

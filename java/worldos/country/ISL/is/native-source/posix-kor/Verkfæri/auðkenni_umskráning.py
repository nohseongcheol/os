#!/usr/bin/env python3
"""Íslenska C 식별자만 UCN으로 옮긴다. strengur_VALUE·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

tákn_VALUE_eb540501 = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<auðkenni_VALUE>[^\W\d]\w*)', re.S | re.M)

def CONVERT_VALUE(Uppruni):
    def REPLACE_VALUE(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(stafur_VALUE if ord(stafur_VALUE) < 128 else
                       ('\\u%04x' if ord(stafur_VALUE) <= 65535 else '\\U%08x') % ord(stafur_VALUE)
                       for stafur_VALUE in 일치[0])
    return tákn_VALUE_eb540501.sub(REPLACE_VALUE, Uppruni)

def keyra_skipun():
    þáttari_48ee4b1b = argparse.ArgumentParser()
    þáttari_48ee4b1b.add_argument('원본', type=Path)
    þáttari_48ee4b1b.add_argument('úttak', type=Path)
    Viðföng = þáttari_48ee4b1b.parse_args()
    for Skrá in sorted(Viðföng.원본.rglob('*')):
        if Skrá.suffix not in ('.c', '.h'):
            continue
        úttak = Viðföng.úttak / Skrá.relative_to(Viðföng.원본)
        úttak.parent.mkdir(parents=True, exist_ok=True)
        새원문 = CONVERT_VALUE(Skrá.read_text())
        if not úttak.exists() or úttak.read_text() != 새원문:
            úttak.write_text(새원문)

if __name__ == '__main__':
    keyra_skipun()

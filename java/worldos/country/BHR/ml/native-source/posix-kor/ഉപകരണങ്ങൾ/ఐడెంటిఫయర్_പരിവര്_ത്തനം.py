#!/usr/bin/env python3
"""한국어 C 식별자만 UCN으로 옮긴다. സ്ട്രിംഗ്_മൂല്യം·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

ടോക്കൺ_മൂല്യം = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<ఐడెంటిఫయర్_മൂല്യം>[^\W\d]\w*)', re.S | re.M)

def 변환(ഉറവിടം):
    def പകരംവയ്ക്കുക_മൂല്യം(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(പ്രതീകം_മൂല്യം if ord(പ്രതീകം_മൂല്യം) < 128 else
                       ('\\u%04x' if ord(പ്രതീകം_മൂല്യം) <= 65535 else '\\U%08x') % ord(പ്രതീകം_മൂല്യം)
                       for പ്രതീകം_മൂല്യം in 일치[0])
    return ടോക്കൺ_മൂല്യം.sub(പകരംവയ്ക്കുക_മൂല്യം, ഉറവിടം)

def നടപ്പാക്കുക_കമാന്_ഡ്():
    പാഴ്_സർ_48ee4b1b = argparse.ArgumentParser()
    പാഴ്_സർ_48ee4b1b.add_argument('원본', type=Path)
    പാഴ്_സർ_48ee4b1b.add_argument('ഫലം', type=Path)
    인수 = പാഴ്_സർ_48ee4b1b.parse_args()
    for ഫയല് in sorted(인수.원본.rglob('*')):
        if ഫയല്.suffix not in ('.c', '.h'):
            continue
        ഫലം = 인수.ഫലം / ഫയല്.relative_to(인수.원본)
        ഫലം.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(ഫയല്.read_text())
        if not ഫലം.exists() or ഫലം.read_text() != 새원문:
            ഫലം.write_text(새원문)

if __name__ == '__main__':
    നടപ്പാക്കുക_കമാന്_ഡ്()

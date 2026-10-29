#!/usr/bin/env python3
"""العربية C 식별자만 UCN으로 옮긴다. سلسلة_قيمة·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

رمز_مميز_قيمة = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<معرف_قيمة>[^\W\d]\w*)', re.S | re.M)

def تحويل_قيمة(مصدر):
    def 바꾸기(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(حرف_قيمة if ord(حرف_قيمة) < 128 else
                       ('\\u%04x' if ord(حرف_قيمة) <= 65535 else '\\U%08x') % ord(حرف_قيمة)
                       for حرف_قيمة in 일치[0])
    return رمز_مميز_قيمة.sub(바꾸기, مصدر)

def ينفذ_أمر():
    المحلل_48ee4b1b = argparse.ArgumentParser()
    المحلل_48ee4b1b.add_argument('원본', type=Path)
    المحلل_48ee4b1b.add_argument('مخرجات', type=Path)
    وسائط = المحلل_48ee4b1b.parse_args()
    for ملف in sorted(وسائط.원본.rglob('*')):
        if ملف.suffix not in ('.c', '.h'):
            continue
        مخرجات = وسائط.مخرجات / ملف.relative_to(وسائط.원본)
        مخرجات.parent.mkdir(parents=True, exist_ok=True)
        새원문 = تحويل_قيمة(ملف.read_text())
        if not مخرجات.exists() or مخرجات.read_text() != 새원문:
            مخرجات.write_text(새원문)

if __name__ == '__main__':
    ينفذ_أمر()

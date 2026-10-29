#!/usr/bin/env python3
"""فارسی C 식별자만 UCN으로 옮긴다. رشته_مقدار_6ca8363c·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

رمز_مقدار = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<شناسه_مقدار>[^\W\d]\w*)', re.S | re.M)

def 변환(مبداء):
    def تغییر_مکان_مقدار(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(نویسه_مقدار if ord(نویسه_مقدار) < 128 else
                       ('\\u%04x' if ord(نویسه_مقدار) <= 65535 else '\\U%08x') % ord(نویسه_مقدار)
                       for نویسه_مقدار in 일치[0])
    return رمز_مقدار.sub(تغییر_مکان_مقدار, مبداء)

def اجرا_فرمان():
    مفسر_48ee4b1b = argparse.ArgumentParser()
    مفسر_48ee4b1b.add_argument('원본', type=Path)
    مفسر_48ee4b1b.add_argument('خروجی', type=Path)
    نشانوندها = مفسر_48ee4b1b.parse_args()
    for پرونده in sorted(نشانوندها.원본.rglob('*')):
        if پرونده.suffix not in ('.c', '.h'):
            continue
        خروجی = نشانوندها.خروجی / پرونده.relative_to(نشانوندها.원본)
        خروجی.parent.mkdir(parents=True, exist_ok=True)
        새원문 = 변환(پرونده.read_text())
        if not خروجی.exists() or خروجی.read_text() != 새원문:
            خروجی.write_text(새원문)

if __name__ == '__main__':
    اجرا_فرمان()
